# fronius
Fronius Inverter (symo) Data 

## Use at your own risk - the code may save you some typing :)

### doc

You will find the API doc from Fronius for reference. If things don't work as expected, read this document.

### fronius.py 

This code is still very much a work in progress and still largely untested.
The api functions are usable but it's not in a package.
There are a number of calls which I cannot test due to my install options.  I'm still trying to figure out what much of the data means.

Use at your own risk - some of the code may save you some typing :)

### collector.py

Collect data from the fronius Symo and log to sqlite database

Assumes you have host 'fronius'  your /etc/hosts file.

Creates a sqlite db called fronius.sqlite with 
two tables called _Site_ and _Inverters_

Queries the Inverter every 5 seconds. 

### Todo
1. Test and cleanup function options
2. Build option to return json or csv data
3. Create a Module.
4. Add code to check that Inverter is up before doing anything.  Necessary if powered by sunlight only

