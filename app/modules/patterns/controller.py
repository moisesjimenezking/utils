from flask import request, jsonify
from create_app import app
from .model import PatternsModel


#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/combinations', methods=['GET'])
def combinations():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        response = PatternsModel.combinations(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            },
            "status_http": 400
        }
        
    return response["response"], response["status_http"]

#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/combinationsString', methods=['GET'])
def combinationsString():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        response = PatternsModel.combinationsString(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            },
            "status_http": 400
        }
        
    return response["response"], response["status_http"]

#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/patternsAdd', methods=['POST'])
def patternsAdd():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        response = PatternsModel.patternsAdd(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            },
            "status_http": 400
        }
        
    return response["response"], response["status_http"]


#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/patternsAll', methods=['GET'])
def patternsAll():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        response = PatternsModel.patternsAll(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            },
            "status_http": 400
        }
        
    return response["response"], response["status_http"]

#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/patternsLike', methods=['GET'])
def patternsLike():
    try:
        try:
            data = request.args or request.values or request.form or request.json
            data = data.copy()
        except:
            data = dict()

        response = PatternsModel.patternsLike(data)
    except Exception as e:
        response = {
            "response":{
                "message":str(e)
            },
            "status_http": 400
        }
        
    return response["response"], response["status_http"]