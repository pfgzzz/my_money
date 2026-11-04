import sqlite3
from datetime import date

DB = "money.db"

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

def add_record(d, amount, category, note=""):
    with conn() as c:
        c.execute("INSERT INTO records(date,amount,category,note) VALUES(?,?,?,?)",
                  (d, amount, category, note))

def list_records(month=None, category=None):
    sql, args = "SELECT * FROM records WHERE 1=1", []
    if month:
        sql += " AND date LIKE ?"; args.append(f"{month}%")
    if category:
        sql += " AND category=?"; args.append(category)
    sql += " ORDER BY date DESC, id DESC"
    with conn() as c:
        return c.execute(sql, args).fetchall()

def delete_record(rid):
    with conn() as c:
        c.execute("DELETE FROM records WHERE id=?", (rid,))

def month_total(month):
    with conn() as c:
        r = c.execute("SELECT COALESCE(SUM(amount),0) FROM records WHERE date LIKE ?",
                      (f"{month}%",)).fetchone()
        return r[0]

def category_sum(month):
    with conn() as c:
        return c.execute("""SELECT category, SUM(amount) s FROM records
                            WHERE date LIKE ? GROUP BY category ORDER BY s DESC""",
                         (f"{month}%",)).fetchall()