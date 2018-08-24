Florida Power Crawler
=====================

Florida Power Crawler is an application that logs on your behalf to www.fpl.com to retrieve useful information.

There are two main programs:

* main
* www/fpc.py
  * www/db/comments
  * www/db/delete
  * www/db/populate
  * www/db/query

Main
----
The information given by this script will be sent to your Phone/Email/etc if the money delta exceeds the configured threshold in `settings.ini`.

The main script executes all the scripts found on notify/ and it passes the nofitication message as a command line argument. Thus, adding your preferred method of notification should be as simple as adding a script into notify/ and using sys.argv[1] as your message.

Output example

```
user in [dev/projects/FPC] # ./main -m
Bill to Date: $10.97
Projected Bill: $21.88

Bill to Date: 08/03/2016 - 08/18/2016
Bill Cycle: 08/03/2016 - 09/02/2016
user in [dev/projects/FPC] #
```

Output example 2

```
user in [dev/projects/FPC] # ./main -y
626 kWh used on Aug 2016. $ 69.62 (93.0 F)
750 kWh used on Jul 2016. $ 81.56 (90.0 F)
465 kWh used on Jun 2016. $ 54.14 (85.0 F)
247 kWh used on May 2016. $ 33.17 (81.0 F)
289 kWh used on Apr 2016. $  37.2 (79.0 F)
239 kWh used on Mar 2016. $ 32.56 (70.0 F)
228 kWh used on Feb 2016. $ 31.38 (66.0 F)
343 kWh used on Jan 2016. $ 42.65 (76.0 F)
448 kWh used on Dec 2015. $ 54.58 (80.0 F)
519 kWh used on Nov 2015. $ 61.79 (82.0 F)
678 kWh used on Oct 2015. $ 77.94 (86.0 F)
303 kWh used on Sep 2015. $ 34.12 (89.0 F)
user in [dev/projects/FPC] #
```

FPC.py
------
This is a website that makes use of the databases found on `db/<year>.db` and presents the information for a given week on a single page. Tables are used to present the information and the data on the columns can be sorted by clicking on the arrows.

<img src="https://cloud.githubusercontent.com/assets/1633888/17792930/d54612b8-6571-11e6-8ea8-03f0dda05515.png" alt="FPC Screenshot">

Database Schema
------------------

```
+----------------------- File data.db -------------------+
+--------------------------------------------------------+
|                         Table FPC                      |
|-----------+---------+----+-----+-----------+-----------|
| Date      | Hour    | $  | kWh | $ per kWh | Temp      |
|-----------+---------+----+-----+-----------|-----------|
| 29-2      | 2       | 34 | 2   |  0.39     | 80        |
| 29-2      | 3       | 34 | 2   |  1        | 88        |
+--------------------------------------------------------+
|             Table SUMMARY                  |
|-------+-----------+------+-----------------|
| Date  | dateprnt   | $    | kWh  | Comments|
|--------------------------------------------|
| 34-1  | Mon Aug 22 | 2.01 | 13   | None    |
+--------------------------------------------+

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

Crontab example
---------------

```
@daily python /home/user/FPC/main --monthly
@daily python /home/user/FPC/www/db/populate
```

Resources
---------
To learn more about FPL check the following URLs

* https://www.fpl.com/rates.html
* https://www.fpl.com/rates/time-of-use.html
* https://www.fpl.com/business/pdf/bill-charges.pdf


To-do list
------------------
* Add a calculator
* Fix the header and footer on the website
* Add what to do (lib/fpc.py) when the user hasn't configured settings.ini properly
* Allow adding comments from the website
* Finish --delete for populate
