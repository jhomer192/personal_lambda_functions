import psycopg2
host = 'firstdatabase-1.cre6iuci2hb1.us-east-2.rds.amazonaws.com'
port = '5432'
dbname = 'example'
user = 'adminohmev'
password = 'QI#xyKOmtjnXc*1c'
try:
    # Connect to the RDS instance
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    print("Connected to PostgreSQL!")

    # Create a cursor object
    cur = conn.cursor()

    # Execute SQL queries
    cur.execute("SELECT * FROM test")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # Close communication with the RDS instance
    cur.close()
    conn.close()
    print("Connection closed.")

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL:", e)