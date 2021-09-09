#!/usr/bin/python

import csv
import sqlite3
import os
from pathlib import Path
import sys


class TransactionRecord:
    """
    Parsed transaction record
    """

    def __init__(self, deducted_from, deposited_to, date_str, amount):
        self.date_str = date_str
        self.deducted_from = deducted_from
        self.deposited_to = deposited_to
        self.amount = amount


class TransactionsFileParser:
    def yield_transaction_records(
        transactions_filepath
    ):
        """
        Parses the transactions records using comma (,) separator.
        For example logs as per requirements contain `<datestamp>,<from>,<to>,<amount>:` in each record.
        """
        with open(transactions_filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if not row.__len__() == 4:
                    raise Exception(
                        f"Failed to parse transaction record: `{row}`")
                yield TransactionRecord(
                    date_str=row[0],
                    deducted_from=row[1],
                    deposited_to=row[2],
                    amount=row[3],
                )


def main(transactions_filepath):
    pass


if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        # pass the transactions file path as an argument
        main(sys.argv[1])
    else:
        main('transactions.csv')
