#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Response, request
from flask import Flask, url_for,redirect

app = Flask(__name__)

@app.route('/')
def inicio():
      return render_template('index.html')

@app.route('/ingresar_carga')
def formulario():
    return render_template('form_ingreso_carga.html')

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

if __name__ == '__main__':
    app.run(debug=True)