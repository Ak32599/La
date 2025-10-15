import psycopg2
import hidden
import requests
import json

# load secrets
secrets = hidden.secrets()

# connect to database
conn = psycopg2.connect(
    host=secrets['host'],
    port=secrets['port'],
    database=secrets['database'],
    user=secrets['user'],
    password=secrets['password']
)
cur = conn.cursor()

# create table
cur.execute('''
CREATE TABLE IF NOT EXISTS pokeapi (
    id INTEGER PRIMARY KEY,
    body JSONB
);
''')
conn.commit()

# loop through first 100 Pokémon
for i in range(1, 101):
    url = f'https://pokeapi.co/api/v2/pokemon/{i}'
    print("Retrieving:", url)

    response = requests.get(url)
    if response.status_code != 200:
        print("Error on id", i)
        continue

    data = response.json()

    # insert into table
    cur.execute('''
        INSERT INTO pokeapi (id, body) VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING;
    ''', (i, json.dumps(data)))

    conn.commit()

print("✅ Done inserting 100 Pokémon!")

cur.close()
conn.close()
