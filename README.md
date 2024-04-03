# py-automations
Handy automations written in Python!

## csvComp
A command line utility written with Python to compare two .csv files and save common rows.
Input: input1.csv input2.csv
Output: similarities.csv, differences,csv

## csvEmail
A command line utility written with Python to recursively copy an email subject, a username, and a device name to the clipboard to make sending bulk emails slightly easier.
Input: input1.csv

## Local Admin CS Killer
A command line utility written with Python to remove usernames from LocalAdmin on a Device using Crowdstrike. Set ACTION to REMOVE to remove, or PASS to skip. It outputs a CSV with results in STATUS column.
Input: input1.csv
CSV Structure: DEVICE,*,USERNAME,STATUS,ACTION
               Name,*,  User,   ,      ,REMOVE or PASS
