from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import os

ZIP_REPOSITORY_MAIN_URL="https://github.com/MatheusHAS/bombcrypto-bot/archive/refs/heads/main.zip"
EXTRACT_TO="C:/"

if os.name != 'nt':
  EXTRACT_TO="~/"
FINAL_EXPORTED_PATH="{}bombcrypto-bot-main/".format(EXTRACT_TO)

def downloadFromUrl(url):
  print('Downloading data from URL:\n{}'.format(url))
  http_response = urlopen(url)
  return BytesIO(http_response.read())

def unzipTo(extract_to, file_bytes=None):
  print('Extracting data to: {}'.format(extract_to))
  zip = ZipFile(file_bytes)
  zip.extractall(path=extract_to)

def main():
  try:
    zip_content_bytes = downloadFromUrl(ZIP_REPOSITORY_MAIN_URL)
    unzipTo(extract_to=EXTRACT_TO, file_bytes=zip_content_bytes)
    print('Installed with success on folder: {}'.format(FINAL_EXPORTED_PATH))
  except Exception as e:
    print('Bombcrypto installer crashed...')
    print("Exception: %s" % (str(e)))
  input("Press Enter to continue...")

main()