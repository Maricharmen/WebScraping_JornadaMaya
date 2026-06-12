""" Utility script to download a raw HTML page layout for local parsing evaluation and test setups. """

from pathlib import Path
import requests

# Resolve root path to save the debugging HTML asset cleanly
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "pagina.html"

url = "https://www.lajornadamaya.mx/k'iintsil/35167/jk-im-xunaan-paula-juntuul-xk-am-paal-jach-k-ajoolta-an-zona-maya"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

try:
    print(f"Downloading testing target layout from: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"[Success] Test layout file written into: {OUTPUT_FILE}")
    
except requests.exceptions.RequestException as e:
    print(f"[Error] Failed to download testing environment target: {e}")

