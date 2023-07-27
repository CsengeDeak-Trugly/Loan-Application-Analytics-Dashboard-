import sqlite3
import pandas as pd

db_file = 'C:/Users/cseni/Desktop/Tanulmányok/loans.db'
database = sqlite3.connect(db_file)
cursor = database.cursor()

dataframe = pd.read_excel('C:/Users/cseni/Desktop/Tanulmányok/project.xlsx', sheet_name='Database', usecols=['loanAmount', 'loanDuration', 'disbursedVolume', 'applicationStartedDate'])
dataframe_filled = dataframe.fillna("")
dataframe_filled.rename(columns={'loanAmount': 'loan_amount', 'loanDuration': 'loan_duration', 'disbursedVolume': 'disbursed_volume', 'applicationStartedDate': 'application_started_date'}, inplace=True)
print(dataframe_filled.columns) 

cursor.execute('''
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY,
        loan_amount INTEGER,
        disbursed_volume INTEGER,
        loan_duration INTEGER,
        application_started_date TEXT
    )
''')

dataframe_filled.to_sql('loans', database, if_exists='append', index=False)

query_with_duration = '''
    SELECT strftime('%Y-%m', application_started_date) AS month,
           SUM(loan_amount) AS total_loan_amount,
           SUM(disbursed_volume) AS total_disbursed_amount,
           loan_duration
    FROM loans
    WHERE loan_duration >= 24
    GROUP BY month, loan_duration
'''
query_without_duration = '''
    SELECT strftime('%Y-%m', application_started_date) AS month,
        SUM(loan_amount) AS total_loan_amount,
        SUM(disbursed_volume) AS total_disbursed_amount
    FROM loans
    WHERE loan_duration >= 24
    GROUP BY month
'''

result_with_duration = pd.read_sql_query(query_with_duration, database)
result_without_duration = pd.read_sql_query(query_without_duration, database)
database.close()

print("Result with duration:")
print(result_with_duration)

print("\nResult without duration:")
print(result_without_duration)

