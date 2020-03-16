# File-Extract-Application
A small application that extracts information from a .csv or .json file and organizes key information while being able to execute via a simple command and take the file name as an input.

FileExtract is a small application in Python(3.X.X) that takes CSV and JSON files in it's own directory as an input.
The application can be launched with a simple command, eg.

```bash
./extractor.sh "file_name.csv" (population_sample.csv and population.csv are included)
OR
./extractor.sh "file_name.json" (population_sample.json and population.json are included)
```

Example csv file content:

```csv
first_name,last_name,siblings,favourite_food,birth_timezone,birth_timestamp
DELIA,MCCRAE,5,chicken,-08:00,601605300000
EUGENE,VANDERSTEEN,2,Yogurt,+01:00,853371780000
BERNARDINA,STWART,1,Mozzarella cheese,+10:30,285926100000
```

Example json file content:
```json
[
{ "first_name": "LEONEL", "last_name": "FERREL", "siblings": "1", "favourite_food": "Meatballs", "birth_timezone": "-01:00", "birth_timestamp": "917172960000" },
{ "first_name": "SHANNA", "last_name": "HILYER", "siblings": "5", "favourite_food": "Meatballs", "birth_timezone": "-05:00", "birth_timestamp": "884072160000" },
{ "first_name": "CARLI", "last_name": "NEWKIRK", "siblings": "5", "favourite_food": "Candy", "birth_timezone": "+01:00", "birth_timestamp": "600794820000" }
]
```

The application can parse the specified file and print out the following information:

* Average number of siblings (round up)
* Top 3 favourite foods and the number of people who like them
* How many people were born in each month of the year (uses the month of each person's respective timezone of birth)


Example output :
```
Average siblings: 2

Favourite foods:
- Pizza      74
- Meatballs  36
- Ice Cream  33

Births per Month:
- January   654
- February   45
- March      38
- April      28
- May        11
- June       16
- July       13
- August      7
- September  32
- October     5
- November   30
- December   31
```

The application also has a robust test suite written using the Python standard testing library can be executed with a simply command.

```bash
./test_extractor.sh
```

