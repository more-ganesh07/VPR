import sqlite3
import csv
# Connect to or create a new database

conn = sqlite3.connect('streamlit-ui/my_database.db')

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS watch (
    id INTEGER PRIMARY KEY,
    company TEXT,
    product TEXT,
    link TEXT
)
'''
cursor.execute(create_table_query)
csv_file_path = r"C:\Users\HP\Desktop\VPR\streamlit-ui\my_database.db"
table_name = "watch"

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        # Assuming CSV columns are in order: name, email
        id = row[0]
        company = row[1]
        product = row[2]
        link = row[3]
        print("INSERT INTO {} (id, company,product, link) VALUES ({}, {}, {},{})".format(table_name,id, company,product, link))
        
        insert_query = "INSERT INTO {} (id, company,product, link) VALUES (?, ?, ?,?)".format(table_name)
        ext_link = cursor.execute(insert_query, (id, company,product, link))
        print(ext_link)
        conn.commit()
# to select all column we will use
# Define the SQL query
query = "SELECT link FROM watch WHERE company = ? AND product LIKE ?"

# Define the parameters for the query
company_name = 'CASIO'
product_prefix = 'Vintage%'

# Execute the query with parameters
cursor.execute(query, (company_name, product_prefix))
output = cursor.fetchall()
print(output)
for row in output:
  print(row)
conn.close()
