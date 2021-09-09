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


class TransactionDB:
    """
    DB CRUD for transaction records
    """

    def __init__(self):
        """
        Creates internal DB store file if not present
        """
        db_file = Path('data.db').touch()
        if not os.path.isfile('data.db'):
            raise Exception(f"Database file could not be created: `{db_file}`")
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                date_str TEXT NOT NULL,
                deducted_from TEXT NOT NULL,
                deposited_to TEXT NOT NULL,
                amount NUMBER CHECK(amount >= 0))
            ''')
        self.conn.commit()

    def insert_transaction(self, transactionRecord):
        """
        Inserts transaction record into internal data file
        """
        params = (transactionRecord.date_str,
                  transactionRecord.deducted_from,
                  transactionRecord.deposited_to,
                  transactionRecord.amount)
        self.cursor.execute(f'''
            INSERT INTO transactions(
                date_str,
                deducted_from,
                deposited_to,
                amount)
            VALUES(
                ?,?,?,?)
            ''', params)
        self.conn.commit()

    def query_transaction_parties(self):
        """
        Returns list of transaction parties
        """
        self.cursor.execute('''
            SELECT DISTINCT
                deducted_from
            FROM transactions
            UNION 
            SELECT DISTINCT
                deposited_to
            FROM transactions
            ''')
        return self.cursor.fetchall()

    def query_ascending_dates(self):
        """
        Returns list of ascending dates to be present in transaction records
        """
        self.cursor.execute('''
            SELECT DISTINCT
                DATE(date_str)
            FROM transactions
            UNION
            SELECT
                MAX(DATE(date_str, '+1 day'))
            FROM transactions
            ORDER BY DATE(date_str)
            ''')
        return self.cursor.fetchall()

    def query_balance_at_given_datestr(self, entity_name, date_str):
        """
        Returns balance value for a given date_string and entity_name
        """
        self.cursor.execute(f'''
            SELECT
                SUM( 
                    CASE '{entity_name}'
                    WHEN deposited_to
                        THEN amount
                    WHEN deducted_from
                        THEN amount*-1
                    ELSE 0 END
            )
            FROM transactions
            WHERE DATE(date_str) < DATE('{date_str}')
        ''')
        return self.cursor.fetchall()


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


class TransactionsProcessingUtil:
    def print_balances_on_each_day(DB):
        transaction_parties = DB.query_transaction_parties()
        print(f"Transaction parties: {transaction_parties}")

        transaction_dates = DB.query_ascending_dates()
        print(f"Transaction dates: {transaction_dates}")

        balance_at_each_day = [[0 for _ in range(
            transaction_parties.__len__())] for _ in range(transaction_dates.__len__())]

        with open('statement.csv', 'w', newline='') as csvfile:
            balance_writer = csv.writer(
                csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            balance_writer.writerow(['Date'] + [x[0]
                                    for x in transaction_parties])
            for transaction_date in transaction_dates:
                party_balance_to_date = []
                for transaction_party in transaction_parties:
                    to_date_balance = DB.query_balance_at_given_datestr(
                        transaction_party[0], transaction_date[0])
                    party_balance_to_date.append(to_date_balance[0][0] or 0)
                    print(
                        f"{transaction_party[0]} balance on {transaction_date[0]} is {to_date_balance}")
                balance_writer.writerow(
                    [transaction_date[0]] + party_balance_to_date)


def main(transactions_filepath):
    DB = TransactionDB()

    transaction_records = TransactionsFileParser.yield_transaction_records(
        transactions_filepath)
    for transaction_record in transaction_records:
        DB.insert_transaction(transaction_record)


    DB.conn.close()


if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        # pass the transactions file path as an argument
        main(sys.argv[1])
    else:
        main('transactions.csv')
