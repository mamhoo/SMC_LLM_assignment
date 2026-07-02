import sqlalchemy
from sqlalchemy import create_engine, text
import os

engine = create_engine("postgresql://postgres:postgres@localhost:5432/financial_db")

with open("data/financial_data.sql", "r", encoding="utf-8") as f:
    sql = f.read()

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("SQL data loaded successfully")