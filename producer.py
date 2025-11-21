from kafka import KafkaProducer
from json import dumps
import sqlite3
import time

# Conexión a SQLite
db_conn = sqlite3.connect('applications.db')

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda m: dumps(m).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8')
)

def total_investment():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT R.name AS region,
               D.name AS department,
               SUM(F.suma_EFA + F.suma_GEE) AS total_investment
        FROM Regions R
        INNER JOIN Departmnets D ON R.id = D.regionId
        INNER JOIN FactInversiones F ON F.region = R.id
        GROUP BY R.name, D.name
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="investment-region", value=record)

    producer.flush()
    cursor.close()

def investment_type():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT tipo_inversion, COUNT(*) AS total
        FROM FactInversiones
        GROUP BY tipo_inversion
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="investment-type", value=record)

    producer.flush()
    cursor.close()

def investment_total_type():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT tipo_inversion,
               SUM(suma_EFA + suma_GEE) AS total_investment
        FROM FactInversiones
        GROUP BY tipo_inversion
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="investment-total-type", value=record)

    producer.flush()
    cursor.close()

def total_discount_fnce():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT R.name AS region,
               D.name AS department,
               SUM(Descuento_FNCE) AS total_discount_fnce
        FROM Regions R
        INNER JOIN Departmnets D ON R.id = D.regionId
        INNER JOIN FactInversiones F ON F.region = R.id
        GROUP BY R.name, D.name
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="total-discount-fnce", value=record)

    producer.flush()
    cursor.close()

def avg_investment_year():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT año AS year,
               AVG(suma_GEE + suma_EFA) AS avg_investment
        FROM FactInversiones
        GROUP BY year
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="avg-investment-year", value=record)

    producer.flush()
    cursor.close()

def max_avg_investment_year():
    cursor = db_conn.cursor()
    rows = cursor.execute("""
        SELECT año AS year,
               AVG(suma_GEE + suma_EFA) AS avg_investment
        FROM FactInversiones
        GROUP BY year
        ORDER BY avg_investment DESC
        LIMIT 1
    """).fetchall()

    columns = [c[0] for c in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    for record in data:
        producer.send("streaming-dash", key="avg-investment-year-max", value=record)

    producer.flush()
    cursor.close()


print(" Producer ejecutándose en tiempo real... (Ctrl+C para detener)")

try:
    while True:
        investment_type()
        total_investment()
        total_discount_fnce()
        investment_total_type()
        avg_investment_year()
        max_avg_investment_year()

        print("Datos enviados... esperando 5s")
        time.sleep(5)

except KeyboardInterrupt:
    print("Producer detenido por el usuario")

finally:
    producer.close()
    db_conn.close()
