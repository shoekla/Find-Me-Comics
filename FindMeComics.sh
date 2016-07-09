#!/bin/sh
#chmod u+x
echo "Launching Find Me Comics\n"

BASEDIR=$(dirname "$0")
cd $BASEDIR
echo "Running Find Me Comics"
python getpip.py
pip install flask
pip install requests
pip install bs4
pip install BeautifulSoup

cd code
(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --enable-speech-input http://127.0.0.1:5000/) &
python launch.py


echo "Press enter to exit"
read "Press enter to exit"