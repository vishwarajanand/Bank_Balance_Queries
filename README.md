# Bank Balance Queries

This repository contains scripts for parsing transactions and displaying daily bank balances at the start of each day.

## Background

This software is developed to keep track of financial transactions between different parties — people and organisations. In our system, these parties are identified by a simple string such as "john" or "supermarket", and it will be provided with a ledger of transactions that looks like this:

```
2015-01-16,john,mary,125.00
2015-01-17,john,supermarket,20.00
2015-01-17,mary,insurance,100.00
```

In this example, John pays Mary §125.00 (§ is our fictional currency) on the 16th of January, and the next day he pays the supermarket §20.00, and Mary pays her insurance company, which costs her §100.00.

This software can process a ledger in this format, and provide access to the accounts of each of the named parties, assuming they all started with a balance of zero. For example, the supermarket has received §20.00, so that’s its balance. John has paid out §125.00 to Mary and §20.00 to the supermarket, so his balance is in debit by §145.00. In other words, his balance is §-145.00.

It is able to find out what each party’s balance is at a specified date. For example, Mary’s balance on the 16th of January is §0.00, but on the 17th it’s §125.00.

## Input

User needs to download the transactions in a CSV format and pass the file link to the script. The software assumes `transactions.csv` file in root folder contains the list of transactions as explained above.

## Output

Since there is no UI required, this software generates the daily balances of all parties in the CSV format in a file called `statement.csv`.

```
Date,insurance,john,mary,supermarket
2015-01-16,0,0,0,0
2015-01-17,0,-125,125,0
2015-01-18,100,-145,25,20

```

The program is tested against the sample input/output.

## Commands

`python3 -m venv venv`

`source venv/bin/activate`

`pip install requirements.txt`

`python parse_transactions.py [optional path to transactions file]`

## Notes

1. `data.db` is the sqlite3 internal storage which stores records across multiple sessions.

2. To refresh the data, rerun the program after deleting the `data.db` file.

3. If the same program is run across multiple sesions with the same file, it will keep on adding the transaction records to the same DB.

4. Since the software can digest muliple transaction files, we need to query the transactions multiple times.
