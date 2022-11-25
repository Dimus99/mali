import requests
import sqlite3

conn = sqlite3.connect('data.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS blocks(
   id INT PRIMARY KEY,
   block_index INTEGER,
   hash TEXT,
   version TEXT,
   merkle_root TEXT,
   bits TEXT,
   time TEXT,
   nonce TEXT,
   prev_block TEXT);
""")
conn.commit()


def BE_TO_LE(num):
    num = num[::-1]
    res = []
    for i in range(0, len(num), 2):
        res.append(num[i + 1])
        res.append(num[i])
    return ''.join(res)


i = 1 + cur.execute("SELECT max(block_index) FROM blocks;").fetchone()[0]
while i <= 760650:
    try:
        response = requests.get(f"https://blockchain.info/rawblock/{i}")
        data = response.json()
    except Exception as e:
        print(i, e)
        continue
    index = i
    h = data["hash"]
    v = BE_TO_LE(str(hex(data["ver"])[2:]).zfill(8))
    prev_block = BE_TO_LE(data["prev_block"])
    merkle_root = BE_TO_LE(data["mrkl_root"])
    bits = BE_TO_LE(str(hex(data["bits"]))[2:])
    timestamp = BE_TO_LE(str(hex(data["time"]))[2:])
    nonce = BE_TO_LE(str(hex(data["nonce"]))[2:].zfill(8))
    values = (index, h, v, merkle_root, bits, timestamp, nonce, prev_block)
    cur.execute("""INSERT INTO blocks(block_index, hash, version, merkle_root, bits, time, nonce, prev_block)
       VALUES(?, ?, ?, ?, ?, ?, ?, ?);""", values)
    if i % 100 == 0:
        conn.commit()
    print(i)
    i += 1
