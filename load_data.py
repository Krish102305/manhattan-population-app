import os
import re
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
CSV = "MESA - Public Datasets - Manhattan populations by neighborhood.csv"

df = pd.read_csv(CSV, dtype=str)
df.columns = [re.sub(r"[^a-z0-9]", "", c.lower()) for c in df.columns]
df = df.rename(columns={
    "fipscountycode": "fips_county_code",
    "ntacode": "nta_code",
    "ntaname": "nta_name",
})
df["population"] = df["population"].str.replace(",", "", regex=False).str.strip().astype(int)
df["year"] = df["year"].astype(int)
df["fips_county_code"] = df["fips_county_code"].astype(int)
cols = ["borough", "year", "fips_county_code", "nta_code", "nta_name", "population"]

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute(open("schema.sql").read())
for row in df[cols].itertuples(index=False):
    cur.execute(
        "INSERT INTO manhattan_populations (borough, year, fips_county_code, nta_code, nta_name, population) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        tuple(row),
    )
conn.commit()
cur.execute("SELECT COUNT(*) FROM manhattan_populations")
print("manhattan_populations rows:", cur.fetchone()[0])
cur.close()
conn.close()
