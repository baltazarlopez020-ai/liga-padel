from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import (
    init_db, SessionLocal,
    User, Pareja, Fixture, Resultado, Posicion, Llave
)

app = Flask(__name__)
app.secret_key = "CLAVE_SECRETA_CAMBIALA"

# Inicializar DB
init_db()

# ----------------------------
# HELPER - Obtener sesión DB
# ----------------------------
def get_db():
    return SessionLocal()

# ----------------------------
# Rutas básicas
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------
# LOGIN / REGISTER
# ----------------------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        db = get_db()
        username = request.form["username"]
        password = request.form["password"]
        club = request.form["club"]

        if db.query(User).filter_by(username=username).first():
            flash("Usuario ya existe", "danger")
            return redirect(url_for("register"))

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            club=club
        )
        db.add(user)
        db.commit()
        flash("Usuario creado. Inicie sesión.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        db = get_db()
        username = request.form["username"]
        password = request.form["password"]

        user = db.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user"] = user.username
            flash("Bienvenido!", "success")
            return redirect(url_for("index"))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sesión cerrada", "info")
    return redirect(url_for("index"))

# ----------------------------
# PROTEGER RUTAS
# ----------------------------
def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Inicie sesión primero", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ----------------------------
# CRUD PAREJAS
# ----------------------------
@app.route("/parejas")
@login_required
def parejas():
    db = get_db()
    lista = db.query(Pareja).all()
    return render_template("parejas.html", parejas=lista)

@app.route("/parejas/add", methods=["POST"])
@login_required
def parejas_add():
    db = get_db()
    pareja = Pareja(
        jugador1=request.form["jugador1"],
        jugador2=request.form["jugador2"],
        categoria=request.form["categoria"]
    )
    db.add(pareja)
    db.commit()
    return redirect(url_for("parejas"))

# ----------------------------
# CRUD FIXTURE
# ----------------------------
@app.route("/fixture")
@login_required
def fixture():
    db = get_db()
    lista = db.query(Fixture).all()
    return render_template("fixture.html", fixture=lista)

@app.route("/fixture/add", methods=["POST"])
@login_required
def fixture_add():
    db = get_db()
    f = Fixture(
        pareja_a=request.form["pareja_a"],
        pareja_b=request.form["pareja_b"],
        fecha=request.form["fecha"],
        categoria=request.form["categoria"]
    )
    db.add(f)
    db.commit()
    return redirect(url_for("fixture"))

# ----------------------------
# CRUD RESULTADOS
# ----------------------------
@app.route("/resultados")
@login_required
def resultados():
    db = get_db()
    lista = db.query(Resultado).all()
    return render_template("resultados.html", resultados=lista)

@app.route("/resultados/add", methods=["POST"])
@login_required
def resultados_add():
    db = get_db()
    r = Resultado(
        partido_id=request.form["partido_id"],
        ganador=request.form["ganador"],
        set1=request.form["set1"],
        set2=request.form["set2"],
        set3=request.form["set3"]
    )
    db.add(r)
    db.commit()
    return redirect(url_for("resultados"))

# ----------------------------
# INICIO SERVIDOR
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)







