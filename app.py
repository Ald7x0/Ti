import os
import sqlite3
from functools import wraps
from pathlib import Path

import click
from flask import (
    Flask, flash, jsonify, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-local-plenavida-trocar-em-producao")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("FLASK_ENV") == "production" or bool(os.environ.get("RENDER")),
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("DATABASE_PATH", BASE_DIR / "clinica.db"))


def conectar():
    """Abre uma conexão com o banco de dados da clínica."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    """Prepara as tabelas usadas pelo sistema."""
    with conectar() as banco:
        banco.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL UNIQUE,
                usuario TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                senha_hash TEXT NOT NULL
            )
        """)
        banco.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                data_nascimento TEXT
            )
        """)
        banco.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                data_consulta TEXT NOT NULL,
                horario TEXT NOT NULL,
                especialidade TEXT NOT NULL,
                observacoes TEXT,
                status TEXT NOT NULL DEFAULT 'Agendada',
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            )
        """)


def login_obrigatorio(funcao):
    """Impede o acesso às páginas internas sem uma sessão ativa."""
    @wraps(funcao)
    def verificar_login(*args, **kwargs):
        if "funcionario_id" not in session:
            return redirect(url_for("login"))
        return funcao(*args, **kwargs)
    return verificar_login


@app.context_processor
def dados_do_menu():
    """Deixa o nome do funcionário disponível no menu das páginas."""
    nome = session.get("funcionario_nome", "")
    iniciais = "".join(parte[0] for parte in nome.split()[:2]).upper() if nome else "PV"
    return {"funcionario_nome": nome, "funcionario_iniciais": iniciais}


@app.route("/login", methods=["GET", "POST"])
def login():
    if "funcionario_id" in session:
        return redirect(url_for("inicio"))

    if request.method == "POST":
        matricula = request.form.get("matricula", "").strip()
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        with conectar() as banco:
            funcionario = banco.execute(
                "SELECT * FROM funcionarios WHERE matricula = ? AND usuario = ?",
                (matricula, usuario)
            ).fetchone()

        if funcionario and check_password_hash(funcionario["senha_hash"], senha):
            session.clear()
            session.permanent = True
            session["funcionario_id"] = funcionario["id"]
            session["funcionario_nome"] = funcionario["nome"]
            return redirect(url_for("inicio"))

        flash("Não consegui confirmar esses dados. Confira a matrícula, o usuário e a senha.")

    return render_template("login.html")


@app.post("/sair")
@login_obrigatorio
def sair():
    session.clear()
    flash("Vc saiu do sistema. Até a próxima!")
    return redirect(url_for("login"))


@app.route("/")
@login_obrigatorio
def inicio():
    with conectar() as banco:
        total_pacientes = banco.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
        total_consultas = banco.execute("SELECT COUNT(*) FROM consultas").fetchone()[0]
        proximas = banco.execute("""
            SELECT consultas.*, pacientes.nome AS paciente
            FROM consultas
            JOIN pacientes ON pacientes.id = consultas.paciente_id
            WHERE consultas.data_consulta >= date('now')
            ORDER BY consultas.data_consulta, consultas.horario
            LIMIT 5
        """).fetchall()
    return render_template("inicio.html", total_pacientes=total_pacientes,
                           total_consultas=total_consultas, proximas=proximas)


@app.route("/pacientes")
@login_obrigatorio
def listar_pacientes():
    termo = request.args.get("q", "").strip()
    ordem = request.args.get("ordem", "nome")
    coluna = "id DESC" if ordem == "recentes" else "nome COLLATE NOCASE"

    with conectar() as banco:
        pacientes = banco.execute(
            f"""SELECT * FROM pacientes
                WHERE nome LIKE ? OR telefone LIKE ?
                ORDER BY {coluna}""",
            (f"%{termo}%", f"%{termo}%")
        ).fetchall()
    return render_template("pacientes.html", pacientes=pacientes, termo=termo, ordem=ordem)


@app.route("/pacientes/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_paciente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        nascimento = request.form.get("data_nascimento", "")
        if not nome:
            flash("Informe o nome do paciente.")
            return render_template("form_paciente.html", paciente=None)
        with conectar() as banco:
            banco.execute("""
                INSERT INTO pacientes (nome, telefone, email, data_nascimento)
                VALUES (?, ?, ?, ?)
            """, (nome, telefone, email, nascimento))
        flash("Cadastro realizado. Paciente adicionado à lista!")
        return redirect(url_for("listar_pacientes"))
    return render_template("form_paciente.html", paciente=None)


@app.route("/pacientes/<int:paciente_id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_paciente(paciente_id):
    with conectar() as banco:
        paciente = banco.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,)).fetchone()
        if paciente is None:
            flash("Não encontrei esse paciente.")
            return redirect(url_for("listar_pacientes"))
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            if not nome:
                flash("O nome não pode ficar vazio.")
                return render_template("form_paciente.html", paciente=paciente)
            banco.execute("""
                UPDATE pacientes SET nome = ?, telefone = ?, email = ?, data_nascimento = ?
                WHERE id = ?
            """, (nome, request.form.get("telefone", "").strip(),
                  request.form.get("email", "").strip(),
                  request.form.get("data_nascimento", ""), paciente_id))
            flash("Prontinho, os dados foram atualizados.")
            return redirect(url_for("listar_pacientes"))
    return render_template("form_paciente.html", paciente=paciente)


@app.post("/pacientes/<int:paciente_id>/excluir")
@login_obrigatorio
def excluir_paciente(paciente_id):
    with conectar() as banco:
        banco.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    flash("Paciente removido do cadastro.")
    return redirect(url_for("listar_pacientes"))


@app.route("/consultas", methods=["GET", "POST"])
@login_obrigatorio
def consultas():
    with conectar() as banco:
        if request.method == "POST":
            paciente_id = request.form.get("paciente_id")
            data = request.form.get("data_consulta")
            horario = request.form.get("horario")
            especialidade = request.form.get("especialidade", "").strip()
            if not (paciente_id and data and horario and especialidade):
                flash("Faltou preencher algum campo obrigatório da consulta.")
            else:
                try:
                    banco.execute("""
                        INSERT INTO consultas
                        (paciente_id, data_consulta, horario, especialidade, observacoes)
                        VALUES (?, ?, ?, ?, ?)
                    """, (paciente_id, data, horario, especialidade,
                          request.form.get("observacoes", "").strip()))
                    flash("Consulta agendada com sucesso!")
                    return redirect(url_for("consultas"))
                except sqlite3.IntegrityError:
                    flash("Não encontrei o paciente selecionado. Atualize a página e tente de novo.")
        pacientes = banco.execute("SELECT id, nome FROM pacientes ORDER BY nome").fetchall()
        lista = banco.execute("""
            SELECT consultas.*, pacientes.nome AS paciente
            FROM consultas
            JOIN pacientes ON pacientes.id = consultas.paciente_id
            ORDER BY consultas.data_consulta DESC, consultas.horario
        """).fetchall()
    return render_template("consultas.html", pacientes=pacientes, consultas=lista)


@app.post("/consultas/<int:consulta_id>/status")
@login_obrigatorio
def alterar_status(consulta_id):
    novo_status = request.form.get("status")
    if novo_status not in ("Agendada", "Concluída", "Cancelada"):
        flash("Esse status não é válido.")
    else:
        with conectar() as banco:
            banco.execute("UPDATE consultas SET status = ? WHERE id = ?", (novo_status, consulta_id))
        flash("Status da consulta atualizado.")
    return redirect(url_for("consultas"))


@app.route("/api/pacientes")
@login_obrigatorio
def api_pacientes():
    """Retorna os pacientes cadastrados em formato JSON."""
    with conectar() as banco:
        registros = banco.execute(
            "SELECT id, nome, telefone, email FROM pacientes ORDER BY nome"
        ).fetchall()
    return jsonify([dict(registro) for registro in registros])


@app.cli.command("criar-funcionario")
def criar_funcionario():
    """Cadastra o primeiro funcionário pelo terminal, sem guardar senha em texto puro."""
    criar_banco()
    nome = click.prompt("Nome do funcionário")
    matricula = click.prompt("Matrícula / identificação")
    usuario = click.prompt("Nome de usuário")
    senha = click.prompt("Senha", hide_input=True, confirmation_prompt=True)
    if len(senha) < 6:
        raise click.ClickException("Use uma senha com pelo menos 6 caracteres.")
    try:
        with conectar() as banco:
            banco.execute(
                "INSERT INTO funcionarios (matricula, usuario, nome, senha_hash) VALUES (?, ?, ?, ?)",
                (matricula, usuario, nome, generate_password_hash(senha))
            )
        click.echo("Funcionário cadastrado. Agora já pode entrar no PlenaVida!")
    except sqlite3.IntegrityError:
        raise click.ClickException("Essa matrícula ou esse usuário já está cadastrado.")


criar_banco()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
