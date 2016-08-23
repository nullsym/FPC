Florida Power Crawler
=====================

Florida Power Crawler is an application that logs on your behalf to www.fpl.com to retrieve useful information.

There are three main programs:

* main
* www/db/populate
* www/fpc.py

Main
----
The information given by this script will be sent to your Phone/Email/etc if two conditions are met:

1. The value of notifications is enabled in settings.ini
2. The money delta exceeds the configured threshold in settings.ini

The main script executes all the scripts found on notify/ and it passes the nofitication message as a command line argument. Thus, adding your preferred method of notification should be as simple as adding a script into notify/ and using sys.argv[1] as your message.

Output example

```
user in [dev/projects/FPC] # ./main
Bill to Date: $10.97
Projected Bill: $21.88

Bill to Date: 08/03/2016 - 08/18/2016
Bill Cycle: 08/03/2016 - 09/02/2016
user in [dev/projects/FPC] #
```

Populate
--------
This is the script that crawls the data for hourly usage from FPL's website and adds it into the database.
If the program is run without arguments it gets the data for yesterday (FPL has a delay of 1 day).
Run `populate -h` or `populate --help` to learn more.

Output example

```
user in [FPC/www/db] # ./populate
As we are not running in dry-run mode changes to the DB will be saved.
Friday Aug. 19, 2016
+-----------------------------------+
| Hour  | Money   | kWh   | Temp    |
+-----------------------------------+
|     0 | $0.01   | 0.79   | 75     |
|     1 | $0.11   | 0.26   | 75     |
|     2 | $0.01   | 0.17   | 74     |
|     3 | $0.01   | 0.19   | 74     |
|     4 | $0.01   | 0.18   | 74     |
|     5 | $0.01   | 0.16   | 73     |
|     6 | $0.01   | 0.16   | 75     |
|     7 | $0.11   | 0.29   | 81     |
|     8 | $0.01   | 0.2    | 85     |
|     9 | $0.01   | 0.17   | 88     |
|    10 | $0.11   | 0.5    | 89     |
|    11 | $0.01   | 0.16   | 91     |
|    12 | $0.01   | 0.2    | 92     |
|    13 | $0.01   | 0.22   | 93     |
|    14 | $0.01   | 0.22   | 95     |
|    15 | $0.11   | 0.25   | 94     |
|    16 | $0.01   | 0.22   | 91     |
|    17 | $0.01   | 0.26   | 89     |
|    18 | $0.01   | 0.26   | 86     |
|    19 | $0.11   | 0.52   | 84     |
|    20 | $0.01   | 0.23   | 83     |
|    21 | $0.01   | 0.25   | 83     |
|    22 | $0.11   | 0.22   | 81     |
|    23 | $0.01   | 0.25   | 80     |
+-----------------------------------+
The information for this date is already in the database.


user in [FPC/www/db] #
```

FPC.py
------
This is a website that makes use of the databases found on `db/<year>.db` and presents the information for a given week on a single page. Tables are used to present the information and the data on the columns can be sorted by clicking on the arrows.

<img src="https://cloud.githubusercontent.com/assets/1633888/17792930/d54612b8-6571-11e6-8ea8-03f0dda05515.png" alt="FPC Screenshot">

Database Schema
------------------

```
+----------------- File 2016.db --------+
+---------------------------------------+
|                   Table FPL           |
|-----------+---------+----+-----+------|
| Date      | Hour    | $  | kWh | Temp |
|-----------+---------+----+-----+------|
| 29-2      | 2       | 34 | 2   | 72   |
| 29-2      | 3       | 34 | 2   | 78   |
+---------------------------------------+
|                   Table SUMMARY       |
|-----------+-----+------+--------------|
| Date      | $    | kWh  | Comments    |
|---------------------------------------|
| 29-2      | 2.01 | 13   | None        |
+---------------------------------------+


+----------------- File 2015.db --------+
+---------------------------------------+
|                   Table FPL           |
|-----------+---------+----+-----+------|
| Date      | Hour    | $  | kWh | Temp |
|-----------+---------+----+-----+------|
| 29-2      | 2       | 34 | 2   | 80   |
| 29-2      | 3       | 34 | 2   | 88   |
+---------------------------------------+
|                   Table SUMMARY       |
|-----------+-----+------+--------------|
| Date      | $    | kWh  | Comments    |
|---------------------------------------|
| 29-2      | 2.01 | 13   | None        |
+---------------------------------------+
```

Crontab example
---------------

```
@daily python /home/user/FPC/main
@daily python /home/user/FPC/www/db/populate
```

Resources
---------
To learn more about FPL check the following URLs

* https://www.fpl.com/rates.html
* https://www.fpl.com/rates/time-of-use.html
* https://www.fpl.com/business/pdf/bill-charges.pdf