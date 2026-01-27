import os
from flask import Flask, render_template
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def make_mysql_url() -> str:
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port = os.getenv("MYSQL_PORT", "3306")
    db = os.getenv("MYSQL_DB", "gestion_heures")

    # charset utf8mb4 important
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"

engine = create_engine(make_mysql_url(), pool_pre_ping=True)

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("main.html")

@app.get("/affaires")
def affaires():
    # On lit la vue créée dans views.sql
    sql = text("""
        SELECT numero_affaire, client, budget_heures, heures_consommees, heures_restantes
        FROM v_suivi_affaires
        ORDER BY numero_affaire
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql).mappings().all()  # liste de dicts

    return render_template("affaire.html", affaires=rows)

@app.get("/health")
def health():
    # test simple de connexion
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
