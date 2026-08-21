import csv
from pathlib import Path


# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path to the datasets folder
DATASET_DIR = BASE_DIR / "datasets"


def load_laptops():
    """Load laptop data from laptops.csv"""

    laptops_file = DATASET_DIR / "laptops.csv"

    laptops = []

    with open(laptops_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            laptops.append(row)

    return laptops