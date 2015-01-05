#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Response, request
from flask import Flask, url_for,redirect, session
import hashlib

app = Flask(__name__)
app.secret_key="clave admin"

@app.route('/',methods=['GET','POST'])
def login():
    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()
    error  = ''
    if request.method == 'POST':
        username = request.form['username']
        clave    = request.form['clave']

        result = c.execute('select salt from usuarios where username = ?',[username])

        matches = result.fetchall()

        if len(matches) > 0:
            user_data = matches[0]
            salt = user_data[0]

            clave = clave+salt
            clave_h = hashlib.sha224(clave.encode('utf-8')).hexdigest()

            result = c.execute('select * from usuarios where username=? and clave = ?',
                                [username,clave_h])
            matches = result.fetchall()
            if len(matches) > 0:
                session['logged_in'] = True
                session['username'] = username

                return redirect('index')
            else:
                error = "Clave erronea."
        else:
            error = "Usuario no existe."

    return render_template('login.html',error=error)


@app.route('/index')
def inicio():
    if 'username' in session:
        a = 0;
    else:
        return redirect('')

    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()
    ciclos = c.execute('SELECT nombre_ciclo FROM ciclos')
    return render_template('index.html',ciclos=ciclos)

@app.route('/ingresa_petroleo', methods=['GET', 'POST'])
def insertar():
    nvale = request.form['txt_nval']
    fecha = request.form['x_fecha1']
    petrolero = request.form['slc_petrolero']
    equipo = request.form['slc_equipo']
    predio = request.form['slc_predio']
    operador = request.form['txt_op']
    horometro = request.form['txt_hrs']
    kilometraje = request.form['txt_km']
    surtidor = request.form['txt_sur']
    litros = request.form['txt_lts']
    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()

    c.execute('INSERT INTO petroleo_vale (n_vale,fecha,petrolero,equipo,predio,operador,kilometraje,surtidor,litros) values (?,?,?,?,?,?,?,?,?)', [nvale,fecha,petrolero,equipo,predio,operador,kilometraje,surtidor,litros])

    conn.commit()
    conn.close()
    return redirect(url_for('ingresar_carga'))

@app.route('/ingresar_disponibilidad',methods=['GET','POST'])
def disponibilidad_equipos():

    if 'username' in session:
        a = 0;
    else:
        return redirect('')

    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()
    equipos = c.execute('SELECT Id,patente,cod_radial FROM  equipos WHERE tipo_equipo in (5,8,18,13,12,10,9,7)  AND estado = 0  ')

    return render_template('form_disponibilidad_equipos.html',equipos=equipos)

@app.route('/petroleo',methods=['GET','POST'])
def resumen_petroleo():
    if 'username' in session:
        a = 0;
    else:
        return redirect('')

    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()
    resumenes = c.execute('SELECT petroleo_vale.equipo ,equipos.cod_radial, tipo_equipos.nombre_equipo, sum(petroleo_vale.litros) as litros FROM petroleo_vale INNER JOIN equipos ON petroleo_vale.equipo  = equipos.patente INNER JOIN tipo_equipos ON tipo_equipos.Id=equipos.tipo_equipo  GROUP BY  petroleo_vale.equipo  ORDER BY petroleo_vale.equipo')
    return render_template('resumen_petroleo.html',resumenes=resumenes)

@app.route('/ingresar_carga')
def ingresar_carga():

    if 'username' in session:
        a = 0;
    else:
        return redirect('')

    import sqlite3
    conn = sqlite3.connect('pirineosBD.sqlite')
    c = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()
    usuarios = c.execute('SELECT equipos.Id , tipo_equipos.nombre_equipo,equipos.patente ,equipos.cod_radial FROM equipos INNER JOIN tipo_equipos ON tipo_equipos.Id = equipos.tipo_equipo AND equipos.tipo_equipo= 4 GROUP BY equipos.Id , tipo_equipos.nombre_equipo, equipos.patente , equipos.cod_radial  ORDER BY tipo_equipos.nombre_equipo, equipos.cod_radial, equipos.patente')
    usuarios2 = c2.execute('SELECT equipos.Id,tipo_equipos.nombre_equipo,equipos.patente,equipos.cod_radial FROM equipos INNER JOIN tipo_equipos ON tipo_equipos.Id = equipos.tipo_equipo GROUP BY equipos.Id,tipo_equipos.nombre_equipo,equipos.patente,equipos.cod_radial ORDER BY tipo_equipos.nombre_equipo,equipos.cod_radial,equipos.patente')
    usuarios3 = c3.execute('SELECT Id,cod_predio,nombre_predio FROM predio WHERE estado=0')

    return render_template('form_ingreso_carga.html',usuarios=usuarios,usuarios2=usuarios2,usuarios3=usuarios3)

@app.route('/salir')
def salir():
    session.pop('username', None)
    return redirect (url_for('login'))

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)


app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

if __name__ == '__main__':
    app.run(debug=True)