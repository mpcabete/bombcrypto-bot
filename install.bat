@echo off

echo INSTALL IN PROGRESS...
pip install -r requirements.txt

python ./scripts/download_and_extract.py

