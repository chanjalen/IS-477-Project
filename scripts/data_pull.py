import hashlib
import requests
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

# data directory\
root = Path(__file__).resolve().parent.parent
data_dir = root / Path("data")
data_dir.mkdir(exist_ok=True)

# checksum function
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# state crime data download
crime_url = "https://corgis-edu.github.io/corgis/datasets/csv/state_crime/state_crime.csv"
crime_file = data_dir / "state_crime.csv"

r = requests.get(crime_url)
r.raise_for_status()
crime_file.write_bytes(r.content)

print("State crime SHA-256:", sha256(crime_file))

#kaggle dataset download
api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    "linzey/alcohol-consumption-us",
    path=data_dir,
    unzip=True
)

#checksums
with open(data_dir / "checksums.txt", "w") as f:
    for file in data_dir.iterdir():
        if file.is_file():
            f.write(f"{file.name}: {sha256(file)}\n")

print("Data downloaded and checksums created.")
