from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json

app = Flask(__name__)
app.app_context().push()
db = SQLAlchemy()
app.config["SECRET_KEY"] = "NIZAR"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////Users/Nizar/OneDrive - Hogeschool Rotterdam/Bureaublad/wp3 inhaalsopdracht/werkplaats-3---inhaalopdracht-Nizar-1012373/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


class applicaties(db.Model):
    __tablename__ = "applicaties"
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(120), nullable=False)
    ip = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"('{self.id}', '{self.naam}','{self.ip}')"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        id = request.form.get("id")
        naam = request.form.get("naam")
        ip = request.form.get("ip")

        return render_template("app1.html", naam=naam, ip=ip)
    else:
        return render_template("app1.html")


@app.route("/applicaties/<id>", methods=["GET", "POST"])
def apps(id):
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties WHERE id =?", (id,))
        result = cur.fetchone()
        if result:
            app = {"id": result[0], "naam": result[1]}
            return jsonify(app)
        else:
            return jsonify({"zet": "een cijfer na applicatie"})

    else:
        return "niks"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)