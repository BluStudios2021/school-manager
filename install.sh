#!/bin/bash
mkdir -p ~/Documents/Scripts/assets;
mkdir -p ~/Pictures/Icons;
mkdir -p ~/Desktop;

cp ./school-manager.py ~/Documents/Scripts;
mv ~/Documents/Scripts/school-manager.py ~/Documents/Scripts/schoolManager.sh;

chmod +x ~/Documents/Scripts/schoolManager.sh

cp ./module_icon.png ~/Pictures/Icons;

cp ./manager.desktop ~/Desktop;

cp ./subjects.txt ~/Documents/Scripts/assets;

echo 'succesfully installed'