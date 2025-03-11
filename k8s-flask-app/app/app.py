from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get database connection details from environment variables
db_host = os.environ.get('POSTGRES_HOST', 'postgres-service')
db_name = os.environ.get('POSTGRES_DB', 'myflaskappdb')
db_user = os.environ.get('POSTGRES_USER', 'myuser')
db_password = os.environ.get('POSTGRES_PASSWORD', '')


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    return conn

@app.route('/')
def hello_world():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"message": "Hello from Flask!", "database": f"Connected to PostgreSQL, version: {db_version[0]}"})
    else:
        return jsonify({"message": "Hello from Flask!", "database": "Failed to connect to database."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Listen on all interfaces