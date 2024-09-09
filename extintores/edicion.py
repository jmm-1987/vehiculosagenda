from flask import render_template, request
import db
from datetime import datetime
from models import Extintor, Vehiculo


def register_extintoredit_routes(app):
    @app.route('/form_editar_extintor/<id>')
    def edicion_extintor(id):
        extintor_editar = db.session.query(Extintor).filter_by(id=(id)).first()
        extintor_editar_matricula = extintor_editar.matricula
        extintor_editar_id_ext = extintor_editar.id_ext
        extintor_editar_ano_ext = extintor_editar.ano_ext
        extintor_editar_rev_ext = extintor_editar.rev_ext
        extintor_editar_venc_ret_ext = extintor_editar.venc_ret_ext
        extintor_editar_venc_ext = extintor_editar.venc_ext
        extintor_editar_obs_ext = extintor_editar.obs_ext
        matriculas=db.session.query(Vehiculo.matricula).all()
        matriculas.insert(0,"")


        return render_template("form_editar_extintor.html", extintor_editar =extintor_editar,
                                                                              extintor_editar_matricula=extintor_editar_matricula,
                                                                              extintor_editar_id_ext=extintor_editar_id_ext,
                                                                              extintor_editar_ano_ext=extintor_editar_ano_ext,
                                                                              extintor_editar_rev_ext=extintor_editar_rev_ext,
                                                                              extintor_editar_venc_ret_ext=extintor_editar_venc_ret_ext,
                                                                              extintor_editar_venc_ext=extintor_editar_venc_ext,
                                                                              extintor_editar_obs_ext=extintor_editar_obs_ext,
                                                                              lista_matriculas=matriculas)

    @app.route("/modificar_extintor", methods=['POST'])
    def modificar_extintor():
        id = request.form["id"]
        mat_ext=request.form["matricula_ext_new"]
        ano_ext=request.form["ano_ext_new"]
        rev_ext=datetime.strptime(request.form["rev_ext_new"], "%Y-%m-%d")
        venc_ret_ext=datetime.strptime(request.form["venc_ret_ext_new"], "%Y-%m-%d")
        venc_ext = datetime.strptime(request.form["venc_ext_new"], "%Y-%m-%d")
        obs_ext = request.form["obs_ext_new"]
        extintor_modificar = db.session.query(Extintor).filter_by(id=(id)).first()
        extintor_modificar.ano_ext = ano_ext
        extintor_modificar.rev_ext = rev_ext
        extintor_modificar.venc_ret_ext = venc_ret_ext
        extintor_modificar.venc_ext = venc_ext
        extintor_modificar.obs_ext = obs_ext
        if mat_ext != "":
            extintor_modificar.matricula = mat_ext
        db.session.commit()
        todos_extintores = db.session.query(Extintor).all()
        return render_template("extintores.html", lista_extintores=todos_extintores)
