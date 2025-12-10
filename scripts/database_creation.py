import sqlite3
import pandas as pd
from pathlib import Path

#paths
data_dir = Path("../data")
db_path = data_dir / "IS477-Proj.db"

connect = sqlite3.connect(db_path)

# load state crime data

crime_df = pd.read_csv(data_dir / "state_crime.csv")
crime_df.to_sql("state_crime", connect, if_exists="replace", index=False)

# load alcohol consumption data

alcohol_df = pd.read_csv(data_dir / "Alcohol_Consumption_US.csv")
alcohol_df.to_sql("alcohol_consumption", connect, if_exists="replace", index=False)

connect.close()