yadtcontroller [![Build Status](https://travis-ci.org/yadt/yadtcontroller.png?branch=master)](https://travis-ci.org/yadt/yadtcontroller)
==============



## Developer setup
This module uses the [pybuilder](http://pybuilder.github.com).
You will need ```virtualenv``` installed. (On Ubuntu : ```sudo apt-get install python-virtualenv```, on other machines ```sudo pip install virtualenv``` should do it).
```bash
git clone https://github.com/yadt/yadtcontroller
cd yadtcontroller
virtualenv venv
. venv/bin/activate
pip install pybuilder
pyb install_dependencies
```
Or you could use [pyb_init](https://github.com/mriehl/pyb_init) and run
```bash
pyb_init https://github.com/yadt/yadtcontroller
```

## Running the tests
```bash
pyb verify
```

## Generating a setup.py
```bash
pyb
cd target/dist/yadtcontroller-$VERSION
./setup.py <whatever you want>
```

## Looking at the coverage
```bash
pyb
cat target/reports/coverage
```
