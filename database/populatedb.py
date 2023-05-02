import mysql.connector

# Establish a connection to the MariaDB server
conn = mysql.connector.connect(
    user="",
    password="",
    host="mysql.metropolia.fi",
    port=3306,
    database=""
)

# Open the SQL file and read the contents
with open('database\install_pma.sql', 'r', encoding="UTF-8") as sql_file:
    sql_script = sql_file.read()

# Split the SQL script into separate queries
queries = sql_script.split(';')

# Create a cursor object
cursor = conn.cursor()

# Execute each query
for query in queries:
    cursor.execute(query)
    cursor.fetchall() # fetch any results, even if it's just an empty result set

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
