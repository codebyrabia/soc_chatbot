import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS threats")
cursor.execute("DROP TABLE IF EXISTS responses")

cursor.execute("""
CREATE TABLE threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    threat_type TEXT
)
""")

cursor.execute("""
CREATE TABLE responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    threat_type TEXT,
    response TEXT
)
""")

# DATA
cursor.execute("INSERT INTO threats VALUES (NULL,'failed login','Brute Force')")
cursor.execute("INSERT INTO threats VALUES (NULL,'sql injection','Injection')")
cursor.execute("INSERT INTO threats VALUES (NULL,'xss','XSS')")
cursor.execute("INSERT INTO threats VALUES (NULL,'ddos','DDoS')")

cursor.execute("INSERT INTO responses VALUES (NULL,'Brute Force','⚠ Brute force attack detected')")
cursor.execute("INSERT INTO responses VALUES (NULL,'Injection','🚨 SQL Injection detected')")
cursor.execute("INSERT INTO responses VALUES (NULL,'XSS','⚠ XSS attack detected')")
cursor.execute("INSERT INTO responses VALUES (NULL,'DDoS','🚨 DDoS attack detected')")

conn.commit()
conn.close()

print("DB READY")