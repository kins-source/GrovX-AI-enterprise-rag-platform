import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY", "default-dev-key")

# Create a dummy PDF file (we just need a valid extension to hit PyPDFLoader, wait, PyPDFLoader will fail if invalid PDF. 
# Better use text to test ingestion pipeline, wait, no, I'll test with text)
with open("test.txt", "w") as f:
    f.write("This is a test document.")

url = "http://localhost:8000/upload"
headers = {"X-API-KEY": API_KEY}
files = {"file": ("test.txt", open("test.txt", "rb"), "text/plain")}

response = requests.post(url, headers=headers, files=files)
print(response.status_code)
print(response.json())
