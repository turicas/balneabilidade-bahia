from pathlib import Path


ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH / "data"
DOWNLOAD_PATH = DATA_PATH / "download"
OUTPUT_PATH = DATA_PATH / "output"
TEST_DATA_PATH = ROOT_PATH / "tests/data"

# Ensure some directories exist
for path in (DATA_PATH, DOWNLOAD_PATH, OUTPUT_PATH):
    if not path.exists():
        path.mkdir()
