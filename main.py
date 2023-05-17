from flask import Flask, render_template, request, jsonify, redirect
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


class omgevingen(db.Model):
    __tablename__ = "omgevingen"
    id = db.Column(db.Integer, primary_key=True)
    test_omgeving = db.Column(db.String(120), nullable=False)
    productie_omgeving = db.Column(db.String(120), nullable=False)
    applicaties_id = db.Column(db.Integer, db.ForeignKey("applicaties.id"))
    applicatie = db.relationship(
        "applicaties", backref=db.backref("omgevingen", lazy=True)
    )

    def __repr__(self):
        return f"('{self.id}', '{self.test_omgeving}','{self.productie_omgeving}', '{self.applicaties_id}')"


class bestanden(db.Model):
    __tablename__ = "bestanden"
    id = db.Column(db.Integer, primary_key=True)
    bestand = db.Column(db.String(120), nullable=False)
    omgevingen_id = db.Column(db.Integer, db.ForeignKey("omgevingen.id"))
    omgevingen = db.relationship(
        "omgevingen", backref=db.backref("bestanden", lazy=True)
    )

    def __repr__(self):
        return f"('{self.id}', '{self.bestand}','{self.omgevingen_id}')"


@app.route("/")
@app.route("/index")
def index():
    return render_template("app1.html")


@app.route("/testcorrect")
def testCorrect():
    return render_template("testcorrect.html")


@app.route("/applicaties", methods=["POST", "GET"])
def scherm_applicaties():
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties")
        applications = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM omgevingen")
        omgevingen = cur.fetchall()
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bestanden")
        bestanden = cur.fetchall()
        return render_template(
            "applicaties.html",
            applications=applications,
            omgevingen=omgevingen,
            bestanden=bestanden,
        )
    if request.method == "POST":
        naam = request.form.get("naam")
        ip = request.form.get("ip")

        new_app = applicaties(naam=naam, ip=ip)

        db.session.add(new_app)

        db.session.commit()

        return render_template("applicaties.html", naam=naam, ip=ip)

    else:
        return render_template("applicaties.html", naam=naam, ip=ip)


@app.route("/pygame")
def pygame():
    return render_template("pygame.html")


@app.route("/applicaties/<id>", methods=["GET", "POST"])
def apps(id):
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM applicaties WHERE id =?", (id,))
        result = cur.fetchone()
        if result:
            app = {"id": result[0], "naam": result[1], "ip": result[2]}
            return render_template("applicatie.html", app=app)
        else:
            return render_template("applicatie.html", app=app)

    # if request.method == "POST":
    #     naam = request.form.get("naam")
    #     ip = request.form.get("ip")

    #     new_app = applicaties(naam=naam, ip=ip)

    #     db.session.add(new_app)

    #     db.session.commit()

    #     return render_template("app2.html", naam=naam, ip=ip)

    # else:
    #     return render_template("app2.html", naam=naam, ip=ip)


@app.route("/applicaties/<id>/omgevingen", methods=["GET", "POST"])
def saves_omgevingen(id):
    omgeving = None
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM omgevingen WHERE id=?", (id,))
        result = cur.fetchone()
        if result:
            omgeving = {
                "id": result[0],
                "testomgeving": result[1],
                "productieomgeving": result[2],
            }
            return render_template("app1.html", omgeving=omgeving)
        else:
            return render_template("app1.html", omgeving=omgeving)

    if request.method == "POST":
        test_omgeving = request.form.get("test_omgeving")
        productie_omgeving = request.form.get("productie_omgeving")

        new_omgeving = omgevingen(
            test_omgeving=test_omgeving, productie_omgeving=productie_omgeving
        )
        db.session.add(new_omgeving)
        db.session.commit()
        return redirect("/index")


@app.route("/application/<id>/omgevingen/<omgevingen_id>", methods=["GET", "POST"])
def open_bestand(id, omgevingen_id):
    bestand = None
    if request.method == "GET":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bestanden WHERE id =?", (id,))
        result = cur.fetchone()
        if result:
            bestand = {
                "id": result[0],
                "bestand": result[1],
                "omgevingen_id": result[2],
            }
            return render_template("bestand.html", bestand=bestand)
        else:
            return render_template("bestand.html", bestand=bestand)
    if request.method == "POST":
        id = request.form.get("id")
        omgevingen_id = request.form.get("omgevingen_id")
        bestand = request.form.get("bestand")
        nieuw_bestand = bestanden(id=id, omgevingen_id=omgevingen_id, bestand=bestand)
        db.session.add(nieuw_bestand)
        db.session.commit()
        return redirect("/index")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
