from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route("/")
def home():
    nome_usuario = request.cookies.get("nome")
    tema_usuario = request.cookies.get("tema", "claro")

    return render_template(
        "inicio.html",
        nome=nome_usuario,
        tema=tema_usuario
    )


@app.route("/salvar_nome", methods=["POST"])
def salvar_nome():
    nome = request.form["nome"]

    resp = make_response(redirect("/"))

    # guarda o nome por 1 ano
    resp.set_cookie(
        "nome",
        nome,
        max_age=60 * 60 * 24 * 365
    )

    return resp


@app.route("/tema/<tema>")
def trocar_tema(tema):
    resp = make_response(redirect("/"))

    if tema == "claro" or tema == "escuro":
        # salva a preferência do usuário
        resp.set_cookie(
            "tema",
            tema,
            max_age=60 * 60 * 24 * 365
        )

    return resp


if __name__ == "__main__":
    app.run(debug=True)