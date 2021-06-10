#!/bin/bash
# must be run from the root directory of the backend folder
sudo apt install python3
sudo apt install python3-pip
pip3 install -r config/requirements.txt
python3 config/nltk_init.py
cd server/main/ml
wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
gzip -d GoogleNews-vectors-negative300.bin.gz
cd -