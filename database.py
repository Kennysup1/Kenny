import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="kennydb",
    user="postgres",
    password="kenny123",
    port="5432"
)

cursor = conn.cursor()
print("Connected to PostgreSQL! ✅")

# Create a users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
print("Users table created! ✅")

# Insert some data
users = [
    ('Kenny', 'kenny@example.com', 22),
    ('Alice', 'alice@example.com', 25),
    ('Bob', 'bob@example.com', 30),
    ('Carol', 'carol@example.com', 28),
    ('David', 'david@example.com', 35)
]

cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING",
    users
)
conn.commit()
print("Users inserted! ✅")

# Query all users
cursor.execute("SELECT * FROM users ORDER BY id")
rows = cursor.fetchall()
print("\n--- All Users in Database ---")
print(f"{'ID':<5} {'Name':<10} {'Email':<25} {'Age':<5} {'Created'}")
print("-" * 60)
for row in rows:
    print(f"{row[0]:<5} {row[1]:<10} {row[2]:<25} {row[3]:<5} {str(row[4])[:19]}")

# Query specific user
cursor.execute("SELECT * FROM users WHERE name = %s", ('Kenny',))
kenny = cursor.fetchone()
print(f"\nFound user: {kenny[1]} - {kenny[2]}")

# Update a user
cursor.execute("UPDATE users SET age = %s WHERE name = %s", (23, 'Kenny'))
conn.commit()
print("Kenny's age updated to 23! ✅")

# Count users
cursor.execute("SELECT COUNT(*) FROM users")
count = cursor.fetchone()[0]
print(f"Total users in database: {count}")

cursor.close()
conn.close()
print("\nDatabase connection closed! ✅")