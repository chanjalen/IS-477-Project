import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path("../data/IS477-Proj.db")
out_dir = Path("../data")
connect = sqlite3.connect(db_path)

# load tables from database
crime = pd.read_sql("SELECT * FROM state_crime", connect)
alcohol = pd.read_sql("SELECT * FROM alcohol_consumption", connect)

# integrate datasets
integrated = crime.merge(alcohol, on=["State", "Year"],how="inner") 

# store integrated table
integrated.to_sql("crime_alcohol_integrated", connect, if_exists="replace", index=False)


# List the tables you want to export
tables = ["state_crime","alcohol_consumption","crime_alcohol_integrated"]

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", connect)
    out_path = out_dir / f"{table}.csv"
    df.to_csv(out_path, index=False)
    print(f"Exported {table} → {out_path}")

connect.close()

print("All tables exported.")