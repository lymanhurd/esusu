import sqlite3


def last_row_inserted(conn):
    res = conn.execute(f"SELECT last_insert_rowid();")
    data = res.fetchone()
    return data[0]


def create_apartment_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
            CREATE TABLE Apartment (
              Apartment_ID INTEGER primary key,
              Property_ID INTEGER,
              Unit INTEGER);
            CREATE TABLE Property (
              Property_ID INTEGER primary key,
              Manager_ID INTEGER,
              Name TEXT,
              Address TEXT);
            CREATE TABLE Tenant (
              Tenant_ID INTEGER primary key,
              Apartment_ID INTEGER,              
              Name TEXT,
              DateOfBirth TEXT,
              EncryptedSSN TEXT,
              IsPrimary INTEGER);
            CREATE TABLE Payment (
              Payment_ID INTEGER primary key,
              Tenant_ID INTEGER,              
              Year INTEGER,
              Month INTEGER,
              Day INTEGER,
              Amount INTEGER);                      
            """)
    return conn


def create_payment_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
            CREATE TABLE Payment (
              Payment_ID INTEGER primary key,
              Tenant_ID INTEGER,
              Year INTEGER,
              Month INTEGER,
              Day INTEGER,
              Amount INTEGER);             
            """)
    return conn
