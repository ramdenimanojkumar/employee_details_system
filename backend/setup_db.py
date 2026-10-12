"""
PostgreSQL Database Setup & Verification Helper Script
Run this script to automatically create the 'employee_db' database in PostgreSQL.
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    import psycopg
    from psycopg import sql
except ImportError:
    print("[ERROR] Required packages not found. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables from .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

db_name = os.getenv("DB_NAME", "employee_db")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "5432")

def try_connect(user, password, host, port, dbname):
    try:
        conn = psycopg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            autocommit=True
        )
        return conn, None
    except Exception as e:
        return None, str(e)

def main():
    print("=" * 60)
    print("   PostgreSQL Database Setup for Employee Details System")
    print("=" * 60)
    print(f"Connecting to PostgreSQL host: {db_host}:{db_port} as user: '{db_user}'...")

    global db_password
    conn, err = try_connect(db_user, db_password, db_host, db_port, "postgres")

    if not conn:
        print(f"\n[WARNING] Could not connect using password from .env.")
        print(f"Error details: {err}\n")
        print("Please enter your PostgreSQL password (set during PostgreSQL installation):")
        try:
            entered_pw = input("Password: ").strip()
        except EOFError:
            entered_pw = ""

        if entered_pw:
            conn, err = try_connect(db_user, entered_pw, db_host, db_port, "postgres")
            if conn:
                db_password = entered_pw
                # Update .env file
                if env_path.exists():
                    content = env_path.read_text(encoding="utf-8")
                    lines = content.splitlines()
                    new_lines = []
                    found = False
                    for line in lines:
                        if line.startswith("DB_PASSWORD="):
                            new_lines.append(f"DB_PASSWORD={entered_pw}")
                            found = True
                        else:
                            new_lines.append(line)
                    if not found:
                        new_lines.append(f"DB_PASSWORD={entered_pw}")
                    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                    print(f"[OK] Updated .env file with your password.")
            else:
                print(f"[ERROR] Still unable to connect: {err}")
                print("Please check your PostgreSQL password and ensure the service is running.")
                sys.exit(1)
        else:
            print("[ERROR] No password provided. Exiting.")
            sys.exit(1)

    print("[OK] Successfully connected to PostgreSQL server!")

    with conn.cursor() as cur:
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        if exists:
            print(f"[OK] Database '{db_name}' already exists.")
        else:
            print(f"Creating database '{db_name}'...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"[OK] Database '{db_name}' created successfully!")

    conn.close()

    # Verify connection to the new database
    test_conn, test_err = try_connect(db_user, db_password, db_host, db_port, db_name)
    if test_conn:
        test_conn.close()
        print(f"[SUCCESS] Database '{db_name}' is ready for Django migrations!")
        print("Next step: Run 'python manage.py migrate'")
    else:
        print(f"[ERROR] Could not connect to '{db_name}': {test_err}")

if __name__ == "__main__":
    main()
