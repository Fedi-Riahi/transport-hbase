import happybase
import csv

connection = happybase.Connection('localhost', port=9090)
table = connection.table('transport')


# Load buses
buses = {}
with open("data/buses.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        buses[row["bus_id"]] = row


# Load stations
stations = {}
with open("data/stations.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stations[row["station_id"]] = row


# Load trips
trips = {}
with open("data/trips.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trips[row["bus_id"]] = row   # assume one active trip per bus


# Load users
users = {}
with open("data/users.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        users[row["user_id"]] = row


# Insert positions 
with open("data/positions.csv") as f:
    reader = csv.DictReader(f)
    batch = table.batch()

    for row in reader:
        bus_id = row["bus_id"]
        timestamp = row["timestamp"]

        row_key = f"{bus_id}#{timestamp}"

        bus = buses.get(bus_id, {})
        trip = trips.get(bus_id, {})
        start_station = stations.get(trip.get("start_station", ""), {})
        end_station = stations.get(trip.get("end_station", ""), {})

        batch.put(row_key.encode(), {

            # BUS
            b'bus:plate_number': bus.get("plate_number", "unknown").encode(),
            b'bus:capacity': str(bus.get("capacity", 0)).encode(),

            # TRIP
            b'trip:trip_id': trip.get("trip_id", "").encode(),
            b'trip:departure_time': trip.get("departure_time", "").encode(),

            # STATIONS (DENORMALIZED 🔥)
            b'trip:start_station': start_station.get("name", "").encode(),
            b'trip:end_station': end_station.get("name", "").encode(),

            # GEO
            b'geo:latitude': row["latitude"].encode(),
            b'geo:longitude': row["longitude"].encode(),

            # META
            b'meta:status': b'moving'
        })

    batch.send()

print("All data merged into one HBase table")