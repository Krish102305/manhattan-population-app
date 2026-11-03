import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)


def query(sql):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()


@app.route("/")
def index():
    rows = query("SELECT nta_name, population FROM manhattan_populations ORDER BY population DESC")
    total = sum(r[1] for r in rows)
    avg = total / len(rows) if rows else 0
    return render_template("index.html", rows=rows, total=total, avg=avg, count=len(rows))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
