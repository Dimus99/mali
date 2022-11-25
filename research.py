import csv
import sqlite3


conn = sqlite3.connect('/Users/dmitriy/Desktop/data.db')
cur = conn.cursor()
names = ["block_index", "hash", "version", "merkle_root", "bits", "time", "nonce", "prev_block"]

res = cur.execute(f"SELECT {', '.join(names)} FROM blocks").fetchall()
s = set(res)
res = [[str(i) for i in row] for row in res]
data = [names] + res

writer = csv.writer(open("/Users/dmitriy/Desktop/data.csv", 'w'))
for row in data:
    writer.writerow(row)
print(', '.join(names))