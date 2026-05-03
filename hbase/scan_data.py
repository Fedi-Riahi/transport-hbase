import happybase
import argparse

connection = happybase.Connection('localhost', port=9090)
table = connection.table('transport')

parser = argparse.ArgumentParser()
parser.add_argument('--bus', type=str, help='Bus ID')
parser.add_argument('--limit', type=int, default=20)
args = parser.parse_args()

# Scan
if args.bus:
    start = f"{args.bus}#"
    end = f"{args.bus}#~"
    data = table.scan(row_start=start.encode(), row_stop=end.encode())
else:
    data = table.scan()

count = 0
for key, row in data:
    print(f" {key.decode()}")
    for col, val in sorted(row.items()):
        print(f" {col.decode()} => {val.decode()}")
    print("")
    count += 1
    if count >= args.limit:
        break

print(f"{count} row(s) in set")