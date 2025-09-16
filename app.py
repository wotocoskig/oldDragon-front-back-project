from flask import Flask, render_template, request, redirect, url_for
from game import Personagem, RAÇAS, CLASSES, DistribuidorAtributos

app = Flask(__name__)


# ----------------- HOME -----------------
@app.route("/")
def index():
    return render_template("index.html")  # agora a home só mostra o menu


# ----------------- CRIAR PERSONAGEM -----------------
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nome = request.form["nome"]
        raca_nome = request.form["raca"]
        classe_nome = request.form["classe"]
        estilo = request.form.get("estilo", "classico")

        if estilo == "classico":
            atributos = DistribuidorAtributos.estilo_classico()
            raca = RAÇAS.get(raca_nome)
            classe = CLASSES.get(classe_nome)
            p = Personagem(nome, atributos, raca, classe)
            p.salvar()
            return redirect(url_for("list_personagens"))

        elif estilo in ["aventureiro", "heroico"]:
            if estilo == "aventureiro":
                valores = DistribuidorAtributos.rolar_aventureiro()
            else:
                valores = DistribuidorAtributos.rolar_heroico()

            # renderiza página para o usuário escolher onde colocar
            return render_template(
                "distribuir.html",
                nome=nome,
                raca=raca_nome,
                classe=classe_nome,
                estilo=estilo,
                valores=valores,
                atributos=["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"]
            )

    return render_template("create.html", racas=RAÇAS.keys(), classes=CLASSES.keys())


# ----------------- VER PERSONAGEM -----------------
@app.route("/personagem/<nome>")
def personagem(nome):
    p = Personagem.carregar(nome)
    if not p:
        return redirect(url_for("list_personagens"))
    return render_template("personagem.html", personagem=p)


# ----------------- LISTAR PERSONAGENS -----------------
@app.route("/list")
def list_personagens():
    personagens = Personagem.listar_personagens()
    return render_template("list.html", personagens=personagens)

@app.route("/distribuir", methods=["POST"])
def distribuir():
    nome = request.form["nome"]
    raca_nome = request.form["raca"]
    classe_nome = request.form["classe"]
    estilo = request.form["estilo"]

    atributos = {
        "Força": int(request.form["Força"]),
        "Destreza": int(request.form["Destreza"]),
        "Constituição": int(request.form["Constituição"]),
        "Inteligência": int(request.form["Inteligência"]),
        "Sabedoria": int(request.form["Sabedoria"]),
        "Carisma": int(request.form["Carisma"])
    }

    raca = RAÇAS.get(raca_nome)
    classe = CLASSES.get(classe_nome)

    p = Personagem(nome, atributos, raca, classe)
    p.salvar()

    return redirect(url_for("list_personagens"))



if __name__ == "__main__":
    app.run(debug=True)

