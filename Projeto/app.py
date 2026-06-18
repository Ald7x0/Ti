from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "senha"


@app.route("/")
def inicio():
    tarefas = session.get("tarefas", [])
    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    tarefa = request.form["tarefa"]

    tarefas = session.get("tarefas", [])
    tarefas.append(tarefa)

    session["tarefas"] = tarefas

    return redirect("/")


@app.route("/limpar")
def limpar():
    session["tarefas"] = []
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)