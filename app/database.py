import psycopg2
# Example function to test connection
async def test_connection():
    connection_string = "postgresql://aya:JrZOAayLhUvBGlVyAkt06w@text-summarizer8-6889.j77.aws-eu-central-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

    try:
     # Connect to the CockroachDB cluster
     conn = psycopg2.connect(connection_string)

     # Create a cursor object
     cursor = conn.cursor()

    # Execute a simple query to test the connection
     cursor.execute("SELECT version();")
     version = cursor.fetchone()
     print("Connected to CockroachDB!")
     print("Database version:", version)

    # Close the cursor and connection
     cursor.close()
     conn.close()

    except Exception as e:
     print("Error connecting to the database:", e)
