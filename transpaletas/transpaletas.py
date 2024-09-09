from flask import render_template, request, redirect, url_for
from flask_login import login_required
import db
from models import Transpaleta

def register_transpaletas_routes(app):
    @app.route('/transpaletas')
    @login_required
    def lista_transpaletas():
        todos_las_transpaletas = db.session.query(Transpaleta).all()
        return render_template('transpaletas.html', lista_transpaletas=todos_las_transpaletas)

    @app.route('/formulario_transpaleta')
    def formulario_transpaleta():
        return render_template("crear_transpaleta.html")

    @app.route('/crear_transpaleta', methods=['POST'])
    def crear_transpaleta():
        transpaleta = Transpaleta(alias=request.form['alias'],
                            marca=request.form['marca'],
                            modelo=request.form['modelo'],
                            bastidor=request.form['bastidor'],
                            asignada=request.form['asignada'])
        db.session.add(transpaleta)
        db.session.commit()
        return redirect(url_for('lista_transpaletas'))
