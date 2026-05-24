import happybase
import csv
from hbase.redis_cache import cache_bus_position

connection = happybase.Connection('localhost', port=9090)
table = connection.table('transport')

buses = {}
with open("data/buses.csv") as f:
    for row in csv.DictReader(f):
        buses[row["bus_id"]] = row

stations = {}
with open("data/stations.csv") as f:
    for row in csv.DictReader(f):
        stations[row["station_id"]] = row

trips = {}
with open("data/trips.csv") as f:
    for row in csv.DictReader(f):
        trips[row["bus_id"]] = row

with open("data/positions.csv") as f:
    positions = list(csv.DictReader(f))

batch = table.batch()
for row in positions:
    bus_id = row["bus_id"]
    timestamp = row["timestamp"]
    row_key = f"{bus_id}#{timestamp}"
    bus = buses.get(bus_id, {})
    trip = trips.get(bus_id, {})
    start_station = stations.get(trip.get("start_station", ""), {})
    end_station = stations.get(trip.get("end_station", ""), {})
    batch.put(row_key.encode(), {
        b'bus:plate_number': bus.get("plate_number", "unknown").encode(),
        b'bus:capacity': str(bus.get("capacity", 0)).encode(),
        b'trip:trip_id': trip.get("trip_id", "").encode(),
        b'trip:departure_time': trip.get("departure_time", "").encode(),
        b'trip:start_station': start_station.get("name", "").encode(),
        b'trip:end_station': end_station.get("name", "").encode(),
        b'geo:latitude': row["latitude"].encode(),
        b'geo:longitude': row["longitude"].encode(),
        b'meta:status': b'moving'
    })
batch.send()

for row in positions:
    cache_bus_position(
        row["bus_id"],
        row["latitude"],
        row["longitude"],
        status="moving"
    )

print("All data inserted into HBase and cached in Redis")
