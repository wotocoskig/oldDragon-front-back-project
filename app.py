<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash
=======
from flask import Flask, render_template, request, redirect, url_for
>>>>>>> 673114b (implement css and fixed bugs)
from game import Personagem, RAÇAS, CLASSES, DistribuidorAtributos

app = Flask(__name__)
app.secret_key = "segredo"  # Necessário para usar flash messages


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

<<<<<<< HEAD
        # selecionar atributos (por enquanto tudo clássico)
        if estilo == "classico":
            atributos = DistribuidorAtributos.estilo_classico()
        elif estilo == "aventureiro":
            atributos = DistribuidorAtributos.estilo_aventureiro()  # pode adaptar depois
        elif estilo == "heroico":
            atributos = DistribuidorAtributos.estilo_heroico()  # pode adaptar depois
        else:
            atributos = DistribuidorAtributos.estilo_classico()

        raca = RAÇAS.get(raca_nome)
        classe = CLASSES.get(classe_nome)

        p = Personagem(nome, atributos, raca, classe)
        p.salvar()

        flash(f"Personagem {nome} criado com sucesso!")
        return redirect(url_for("list_personagens"))
=======
        raca = RAÇAS.get(raca_nome)
        classe = CLASSES.get(classe_nome)

        if estilo == "classico":
            atributos = DistribuidorAtributos.estilo_classico()
            p = Personagem(nome, atributos, raca, classe)
            p.salvar()
            return redirect(url_for("list_personagens"))

        elif estilo in ["aventureiro", "heroico"]:
            # Gerar os valores correspondentes
            if estilo == "aventureiro":
                valores = DistribuidorAtributos.rolar_aventureiro()
            else:
                valores = DistribuidorAtributos.rolar_heroico()

            # Renderizar o template distribuir.html
            return render_template(
                "distribuir.html",
                nome=nome,
                raca=raca_nome,
                classe=classe_nome,
                estilo=estilo,
                valores=valores,
                atributos=["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"]
            )
>>>>>>> 673114b (implement css and fixed bugs)

    return render_template("create.html", racas=RAÇAS.keys(), classes=CLASSES.keys())


<<<<<<< HEAD
=======

>>>>>>> 673114b (implement css and fixed bugs)
# ----------------- VER PERSONAGEM -----------------
@app.route("/personagem/<nome>")
def personagem(nome):
    p = Personagem.carregar(nome)
    if not p:
<<<<<<< HEAD
        flash("Personagem não encontrado!")
=======
>>>>>>> 673114b (implement css and fixed bugs)
        return redirect(url_for("list_personagens"))
    return render_template("personagem.html", personagem=p)


# ----------------- LISTAR PERSONAGENS -----------------
@app.route("/list")
def list_personagens():
    personagens = Personagem.listar_personagens()
    return render_template("list.html", personagens=personagens)


<<<<<<< HEAD
=======




@app.route("/distribuir", methods=["POST"])
def distribuir():
    nome = request.form["nome"]
    raca_nome = request.form["raca"]
    classe_nome = request.form["classe"]
    estilo = request.form["estilo"]

    atributos = {}
    for attr in ["Força","Destreza","Constituição","Inteligência","Sabedoria","Carisma"]:
        valor_str = request.form.get(attr)
        if not valor_str:
            return redirect(request.referrer)
        atributos[attr] = int(valor_str)

    raca = RAÇAS.get(raca_nome)
    classe = CLASSES.get(classe_nome)

    p = Personagem(nome, atributos, raca, classe)
    p.salvar()

    return redirect(url_for("list_personagens"))



>>>>>>> 673114b (implement css and fixed bugs)
if __name__ == "__main__":
    app.run(debug=True)
