from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

alunos = []

@app.route('/')
def index():
    return render_template('index.html', alunos=alunos)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']
        email = request.form['email']

        if nome and idade and curso and email:
            alunos.append({
                'nome': nome,
                'idade': idade,
                'curso': curso,
                'email': email
            })

        return redirect(url_for('index'))

    return render_template('cadastrar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    aluno = alunos[id]

    if request.method == 'POST':
        aluno['nome'] = request.form['nome']
        aluno['idade'] = request.form['idade']
        aluno['curso'] = request.form['curso']
        aluno['email'] = request.form['email']

        return redirect(url_for('index'))

    return render_template('editar.html', aluno=aluno, id=id)

@app.route('/excluir/<int:id>')
def excluir(id):
    alunos.pop(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)