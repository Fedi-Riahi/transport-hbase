import happybase
import csv

connection = happybase.Connection('localhost', port=9090)
table = connection.table('transport')

# Export to CSV including the row key
with open('hbase_export_with_rowkey.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write header - includes row_key as first column
    writer.writerow([
        'row_key',           # Full HBase row key (bus_id#timestamp)
        'bus_id',            # Extracted bus_id
        'timestamp',         # Extracted timestamp
        'bus_plate_number', 
        'bus_capacity', 
        'trip_id', 
        'trip_departure_time', 
        'trip_start_station', 
        'trip_end_station', 
        'latitude', 
        'longitude', 
        'status'
    ])
    
    # Scan and write all rows
    for key, data in table.scan():
        row_key = key.decode()
        bus_id, timestamp = row_key.split('#')  # Split the row key
        
        writer.writerow([
            row_key,                             # Full row key
            bus_id,                              # Bus ID part
            timestamp,                           # Timestamp part
            data.get(b'bus:plate_number', b'').decode(),
            data.get(b'bus:capacity', b'').decode(),
            data.get(b'trip:trip_id', b'').decode(),
            data.get(b'trip:departure_time', b'').decode(),
            data.get(b'trip:start_station', b'').decode(),
            data.get(b'trip:end_station', b'').decode(),
            data.get(b'geo:latitude', b'').decode(),
            data.get(b'geo:longitude', b'').decode(),
            data.get(b'meta:status', b'').decode()
        ])

print("✅ Exported to hbase_export_with_rowkey.csv")
print("   The CSV includes the full row_key column")