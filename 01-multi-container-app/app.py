import os
import time
from flask import Flask
import redis
import psycopg2

# --- Environment Variable Setup ---
# These variables MUST be correctly set in your docker-compose.yml
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'myuser')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'mysecretpassword')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'mydb')
APP_PORT = int(os.environ.get('APP_PORT', 8080))

app = Flask(__name__)

# --- Global Connection Objects ---
# These are defined outside the route, but established inside for graceful failure
redis_client = None
pg_conn = None

def init_connections():
    """Attempts to establish Redis and PostgreSQL connections."""
    global redis_client, pg_conn
    
    # 1. Initialize Redis Connection
    try:
        redis_client = redis.Redis(host=REDIS_HOST,
                                   port=6379,
                                   password=os.environ.get('REDIS_PASSWORD'),
                                   socket_connect_timeout=1
                                   )
        # Attempt a simple ping to ensure connectivity
        redis_client.ping()
        print(f"Successfully connected to Redis at {REDIS_HOST}")
    except Exception as e:
        print(f"!!! REDIS CONNECTION FAILED at {REDIS_HOST}: {e}")
        redis_client = None

    # 2. Initialize PostgreSQL Connection
    try:
        pg_conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            connect_timeout=3
        )
        print(f"Successfully connected to PostgreSQL at {POSTGRES_HOST}")
        
        # Optional: Initialize DB table if it doesn't exist
        with pg_conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS hits (
                    id SERIAL PRIMARY KEY,
                    count INTEGER DEFAULT 0,
                    last_access TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            pg_conn.commit()
            
    except Exception as e:
        print(f"!!! POSTGRES CONNECTION FAILED at {POSTGRES_HOST}: {e}")
        pg_conn = None

@app.route('/')
def show_status():
    """Main route to display connection status and data interaction."""
    
    # Ensure connections are initialized
    init_connections() 
    
    status_output = '<h1>Multi-Container Status</h1>'
    
    # --- Redis Logic ---
    if redis_client:
        try:
            # Increment a counter key in Redis
            hit_count = redis_client.incr('web_hits')
            status_output += f'<p style="color: green;">✅ **REDIS SUCCESS!** Web Hits: **{hit_count}**</p>'
        except Exception as e:
            status_output += f'<p style="color: red;">❌ **REDIS ERROR:** Failed to interact with cache. ({e})</p>'
    else:
        status_output += '<p style="color: red;">❌ **REDIS FAILURE:** Check `REDIS_HOST` environment variable and container name.</p>'

    # --- PostgreSQL Logic ---
    if pg_conn:
        try:
            with pg_conn.cursor() as cur:
                # 1. Update the hit count in the database
                cur.execute("UPDATE hits SET count = count + 1, last_access = CURRENT_TIMESTAMP WHERE id = 1 RETURNING count, last_access;")
                
                # If no rows were updated (first time), insert the row
                if cur.rowcount == 0:
                    cur.execute("INSERT INTO hits (id, count) VALUES (1, 1) RETURNING count, last_access;")

                db_count, last_access = cur.fetchone()
                pg_conn.commit()

                status_output += f'<p style="color: green;">✅ **POSTGRES SUCCESS!** DB Count: **{db_count}** (Last Access: {last_access})</p>'
                
        except Exception as e:
            # Rollback any pending transaction if an error occurred
            pg_conn.rollback()
            status_output += f'<p style="color: red;">❌ **POSTGRES ERROR:** Failed to update database. ({e})</p>'
    else:
        status_output += '<p style="color: red;">❌ **POSTGRES FAILURE:** Check `POSTGRES_HOST/USER/PASSWORD` environment variables and container name.</p>'

    return status_output

if __name__ == '__main__':
    print(f"Flask App starting up on port {APP_PORT}...")
    init_connections() # Attempt initial connections at startup
    app.run(debug=True, host='0.0.0.0', port=APP_PORT)
