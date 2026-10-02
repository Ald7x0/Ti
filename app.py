import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, g

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "biblioteca.db"

app = Flask(__name__)
app.secret_key = "troque-esta-chave"


# ---------- Banco de dados ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria o banco a partir do schema.sql se ele ainda não existir."""
    if not DATABASE.exists():
        conn = sqlite3.connect(DATABASE)
        conn.executescript((BASE_DIR / "schema.sql").read_text(encoding="utf-8"))
        conn.commit()
        conn.close()


# ---------- Rotas ----------
@app.route("/")
def index():
    db = get_db()
    total_livros = db.execute("SELECT COUNT(*) FROM livros").fetchone()[0]
    total_autores = db.execute("SELECT COUNT(*) FROM autores").fetchone()[0]
    total_categorias = db.execute("SELECT COUNT(*) FROM categorias").fetchone()[0]
    return render_template("index.html", total_livros=total_livros,
                           total_autores=total_autores,
                           total_categorias=total_categorias)


@app.route("/livros/novo", methods=["GET", "POST"])
def novo_livro():
    db = get_db()
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        if not titulo:
            flash("Informe o título do livro.", "erro")
        else:
            db.execute(
                """INSERT INTO livros (titulo, ano_publicacao, isbn, quantidade,
                                       id_autor, id_categoria)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (titulo,
                 request.form.get("ano_publicacao") or None,
                 request.form.get("isbn", "").strip() or None,
                 request.form.get("quantidade") or 1,
                 request.form["id_autor"],
                 request.form["id_categoria"]),
            )
            db.commit()
            flash("Livro cadastrado com sucesso!", "ok")
            return redirect(url_for("acervo"))
    autores = db.execute("SELECT * FROM autores ORDER BY nome").fetchall()
    categorias = db.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    return render_template("livro_form.html", livro=None,
                           autores=autores, categorias=categorias)


@app.route("/livros")
def acervo():
    db = get_db()
    busca = request.args.get("q", "").strip()
    sql = """SELECT l.id_livro, l.titulo, l.ano_publicacao, l.isbn, l.quantidade,
                    a.nome AS autor, c.nome AS categoria
             FROM livros l
             JOIN autores a    ON a.id_autor = l.id_autor
             JOIN categorias c ON c.id_categoria = l.id_categoria"""
    params = ()
    if busca:
        sql += " WHERE l.titulo LIKE ? OR a.nome LIKE ? OR c.nome LIKE ?"
        params = (f"%{busca}%",) * 3
    sql += " ORDER BY l.titulo"
    livros = db.execute(sql, params).fetchall()
    return render_template("acervo.html", livros=livros, busca=busca)


@app.route("/livros/<int:id_livro>/editar", methods=["GET", "POST"])
def editar_livro(id_livro):
    db = get_db()
    livro = db.execute("SELECT * FROM livros WHERE id_livro = ?", (id_livro,)).fetchone()
    if livro is None:
        flash("Livro não encontrado.", "erro")
        return redirect(url_for("acervo"))
    if request.method == "POST":
        db.execute(
            """UPDATE livros SET titulo=?, ano_publicacao=?, isbn=?, quantidade=?,
                                 id_autor=?, id_categoria=?
               WHERE id_livro=?""",
            (request.form["titulo"].strip(),
             request.form.get("ano_publicacao") or None,
             request.form.get("isbn", "").strip() or None,
             request.form.get("quantidade") or 1,
             request.form["id_autor"],
             request.form["id_categoria"],
             id_livro),
        )
        db.commit()
        flash("Livro atualizado!", "ok")
        return redirect(url_for("acervo"))
    autores = db.execute("SELECT * FROM autores ORDER BY nome").fetchall()
    categorias = db.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    return render_template("livro_form.html", livro=livro,
                           autores=autores, categorias=categorias)


@app.route("/livros/<int:id_livro>/excluir", methods=["POST"])
def excluir_livro(id_livro):
    db = get_db()
    db.execute("DELETE FROM livros WHERE id_livro = ?", (id_livro,))
    db.commit()
    flash("Livro excluído.", "ok")
    return redirect(url_for("acervo"))


@app.route("/autores", methods=["GET", "POST"])
def autores():
    db = get_db()
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if nome:
            db.execute("INSERT INTO autores (nome, nacionalidade) VALUES (?, ?)",
                       (nome, request.form.get("nacionalidade", "").strip() or None))
            db.commit()
            flash("Autor cadastrado!", "ok")
        return redirect(url_for("autores"))
    lista = db.execute("SELECT * FROM autores ORDER BY nome").fetchall()
    return render_template("autores.html", autores=lista)


@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    db = get_db()
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if nome:
            try:
                db.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
                db.commit()
                flash("Categoria cadastrada!", "ok")
            except sqlite3.IntegrityError:
                flash("Essa categoria já existe.", "erro")
        return redirect(url_for("categorias"))
    lista = db.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    return render_template("categorias.html", categorias=lista)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
