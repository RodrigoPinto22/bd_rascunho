import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = db.execute('''
        SELECT * FROM
            (SELECT COUNT(*) n_distritos FROM distritos)
        JOIN
            (SELECT COUNT(*) n_concelhos FROM concelhos)
    ''').fetchone()

    return render_template('index.html',stats=stats)

@APP.route('/cidadao')
def listar_populacao():
    cidadao = db.execute('''
        SELECT * FROM cidadao
    ''').fetchall()
    return render_template('listar_populacao.html', cidadao=cidadao)

@APP.route('/distritos/')
def listar_distritos():
    distritos = db.execute('''
        SELECT distritos.cod, distritos.designacao, COUNT(*) num_concelhos
        FROM distritos 
        JOIN concelhos ON concelhos.distrito = distritos.cod
        GROUP BY distritos.cod
        ORDER BY distritos.cod
    ''').fetchall()
    return render_template('listar_distritos.html', distritos=distritos)

@APP.route('/distritos/<int:codigo>/')
def distrito(codigo):
    # Obtém dados do distrito
    distrito = db.execute('''
        SELECT cod, designacao
        FROM distritos 
        WHERE cod = ?
    ''', [codigo]).fetchone()
    # Obtém concelhos no distrito
    concelhos = db.execute('''
        SELECT cod, designacao
        FROM concelhos WHERE distrito = ?
        ORDER BY cod
    ''', [codigo]).fetchall()
    return render_template('distrito.html',
                            distrito=distrito,
                            concelhos=concelhos)

@APP.route('/concelhos/')
def listar_concelhos():
    concelhos = db.execute('''
       SELECT c.cod, c.designacao, COUNT(*) as num_recintos, d.designacao as distrito
        FROM recintos r JOIN concelhos c
        ON r.concelho = c.cod
        JOIN distritos d
        ON d.cod = c.distrito
        GROUP BY c.cod
        ORDER BY c.cod, c.designacao
    ''').fetchall()
    return render_template('listar_concelhos.html', concelhos=concelhos)

@APP.route('/concelhos/<int:codigo>/')
def concelho(codigo):
    # Obtém dados do distrito
    concelho = db.execute('''
        SELECT cod, designacao
        FROM concelhos 
        WHERE cod = ?
    ''', [codigo]).fetchone()
    # Obtém concelhos no distrito
    recintos = db.execute('''
      SELECT r.id, r.nome
        FROM concelhos c JOIN distritos d
        ON c.distrito = d.cod
        JOIN recintos r
        ON r.concelho = c.cod
        WHERE concelho = ?
    ''', [codigo]).fetchall()
    return render_template('concelho.html',
                            concelho=concelho,
                            recintos=recintos)




# TODO
# ...
