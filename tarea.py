#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Response, request
from flask import Flask, url_for,redirect

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def form():

    import sqlite3
    conn = sqlite3.connect('pirineos.sqlite')
    c = conn.cursor()
    c2 = conn.cursor()
    c3 = conn.cursor()
    usuarios = c.execute('SELECT equipos.Id , tipo_equipos.nombre_equipo,equipos.patente ,equipos.cod_radial FROM equipos INNER JOIN tipo_equipos ON tipo_equipos.Id = equipos.tipo_equipo AND equipos.tipo_equipo= 4 GROUP BY equipos.Id , tipo_equipos.nombre_equipo, equipos.patente , equipos.cod_radial  ORDER BY tipo_equipos.nombre_equipo, equipos.cod_radial, equipos.patente')
    usuarios2 = c2.execute('SELECT equipos.Id,tipo_equipos.nombre_equipo,equipos.patente,equipos.cod_radial FROM equipos INNER JOIN tipo_equipos ON tipo_equipos.Id = equipos.tipo_equipo GROUP BY equipos.Id,tipo_equipos.nombre_equipo,equipos.patente,equipos.cod_radial ORDER BY tipo_equipos.nombre_equipo,equipos.cod_radial,equipos.patente')
    usuarios3 = c3.execute('SELECT Id,cod_predio,nombre_predio FROM predio WHERE estado=0')

    return render_template('petroleo.html',usuarios=usuarios,usuarios2=usuarios2,usuarios3=usuarios3)



if __name__ == '__main__':
    app.run(debug=True)