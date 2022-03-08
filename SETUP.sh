#!/usr/bin/env bash

echo "Installing... Please be patient..."
python3 -m pip install virtualenv &> /dev/null
python3 -m virtualenv venv &> /dev/null
. venv/bin/activate &> /dev/null
python -m pip install -r requirements.txt &> /dev/null
clear
echo "Finished installing"
echo
echo "INSTRUCTIONS:"
echo
echo "#################################################################################"
echo "CONFIGURE: MAKE YOUR src/bcfg/settings.py file LOOK something like this example"
echo "#################################################################################"
echo
echo
cat ./src/bcfg/settings_example.py
echo
echo
echo "#################################################################################"
read -p 'Press ENTER to edit the file' uservar
echo
export EDITOR="/usr/bin/nano"
$EDITOR ./src/bcfg/settings.py
bash ./START_DOWNLOADING.sh