#import os
import flask
import json
from flask import Flask,request,jsonify
from flask import render_template
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = flask.Flask('FuzzyODH')
app.debug = True


from controller.odhController import getOdh as odhController 


#@app.route('/')
#def raiz():
#    return "Para o cálculo ODH insira os parâmetros: (psicolicas,assistencia,amparo,transporte,ciclovia,esporte,alimento) /defuzzy/odh?psi=8&ass=7&apr=7&tra=7&cic=7&esp=7&ali=7"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/defuzzy/odh", methods=["POST"])
def getOdhPost():
    body = request.get_json()    
    return json.dumps( odhController(body), ensure_ascii=False ).encode('utf8')

#@app.route("/defuzzy/odh/<int:psi>/<int:ass>/<int:amp>/<int:tra>/<int:cic>/<int:esp>/<int:ali>", methods=["GET"])
#def getOdhGet(psi, ass, amp, tra, cic, esp, ali):  
#    return odhController(psi, ass, amp, tra, cic, esp, ali)


#/defuzzy/odh?psi=8&ass=7&amp=7&tra=7&cic=7&esp=7&ali=7
@app.route("/defuzzy/odh", methods=["GET"])
def getOdhGet(): 

    psi = request.args.get('psi', '') 
    ass = request.args.get('ass', '')
    amp = request.args.get('apr', '')
    tra = request.args.get('tra', '')
    cic = request.args.get('cic', '')
    esp = request.args.get('esp', '')
    ali = request.args.get('ali', '')

    return jsonify(odhController(psi, ass, amp, tra, cic, esp, ali))