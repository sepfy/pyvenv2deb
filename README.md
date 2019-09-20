# pyvenv2deb
Convert Python package in virtualenv to Debian package.

Becuase I have a project which needs to setup a apt-get server and manage the package for python. I met some problems with others tools, like py2deb and dh-virtual. For example, py2deb needs to downgrade the version of pip. The dh-virtualenv will package all virutalenv to a package (Mayby I don't understand how to use that). So I create a simple script(python) to help me to package a lot of python package to deb seprately. 

## How to use
1. Install virtualenv
```bash
apt-get install virtualenv
```
3. Download your package in virtualenv
```bash
virtualenv -p python3 venv
source venv/bin/active
pip3 install <your package>
```
4. Freeze your package to a list
```bash
pip3 freeze > requirements.txt
```
5. Convert your virutalenv package to debian package
```bash
git clone https://github.com/sepfy/pyvenv2deb
python3 pyvenv2deb
```
You can check the Debian package source code in outputs. If there are something you want to change, like description..., You can modify it. 
And run the following commnad to package it to .deb file
```bash
python3 pack2deb
```
6. Find your package in directory outputs
