from flask import request, jsonify
from create_app import app
from library.libraryTelegram import Telegram
from library.libraryWhatsapp import Whatsapp
from library.scrapingScritp import Tasas, Spider
from library.supportApiBiyuyo import Support


#
# Método para envio de mensajes a telegram
#? return @redirection
#
@app.route('/sendMessageTelegram', methods=['POST'])
def sendMessageTelegram():
    try:
        try:
            data = request.args or request.values or request.form or request.json
        except:
            data = dict()
        
        if("type" in data):
            types = data.get('type').upper()
        else:
            return jsonify({"message":"El campo type es requerido"}), 400
            
        ## Type list
        listType = {
            "UP":"send_message",
            "DOWN":"notify_in_test_canal",
            "PROXY":"notifyInProxyChanel",
            "PROVIDER":"notifyRechargeCertificationApi",
            "GROUP_WHATSAPP":"notifyChanelGroupWhatsapp"
        }

        if(types in listType):
            method = getattr(Telegram, listType[types])
            if(callable(method)):
                response = method(data)
            else:
                response = {"response":{"message":"Envio Fallido. VC"},"status_http":400}
        else:
            response = {"response":{"message":"Envio Fallido. VC"},"status_http":400}        

    except Exception as e:
        response = {"response":{"message" : e},"status_http":400}
        
    return response["response"], response["status_http"] 
    

#
# Método para envio de mensaje definido a telegram whatsapp
#? return @redirection
# GET
#
@app.route('/whatsappMessageGroup', methods=['POST'])
def whatsappMessageGroup():
    try:
        message = request.form['message']
        type = 'up' if ('type' in request.form and request.form['type'].upper() == "UP") else 'down'
        
        group =  "120363143779953923@g.us" if type.upper() == "UP" else "120363133348179178@g.us"
        event = "production" if type.upper() == "UP" else "test"
        
        response = Whatsapp.eventGroup(message, group, event)
        
    except Exception as e:
        response = {
            "response":{"message" : e},
            "status_http" : 400
        }

    return response["response"], response["status_http"] 

#
#? return response
#
@app.route('/bcvTasa', methods=['GET'])
def bcv():
    try:        
        response = Tasas.bcv()
    except Exception as e:
        response = {
            "response":{"message" : e},
            "status_http" : 400
        }

    return response["response"], response["status_http"]


#
#? return response
#
@app.route('/promedioBcv', methods=['GET'])
def promedioBcv():
    try:        
        response = Tasas.promedioBcv()
    except Exception as e:
        response = {
            "response":{"message" : e},
            "status_http" : 400
        }

    return response["response"], response["status_http"]


#
#? return response
#
@app.route('/consultCne', methods=['GET'])
def consultCne():
    try:
        try:
            data = request.args or request.values or request.form or request.json
        except:
            raise Exception("No se suministraron datos.")
        
        if("nationality" in data and data["nationality"].upper() not in ["V","E"]):
            raise Exception("La nacionalidad suministrada no coincide con las permitidas en la busqueda Ej: V o E.")
        
        if("nationality" not in data):
            data["nationality"] = "V"
            
        if("number" not in data):
            raise Exception("Número de cédula no suministrado.")
            
        response = Spider.consultCne(data)
    except Exception as e:
        response = {
            "response":{"message" : str(e)},
            "status_http" : 400
        }

    return response["response"], response["status_http"]

#
#? return response
#
@app.route('/consult_play_store_ve', methods=['GET'])
def consultPlayStoreVe():
    try:        
        response = Spider.consultPlayStoreVe()
    except Exception as e:
        response = {
            "response":{"message" : e},
            "status_http" : 400
        }

    return response["response"], response["status_http"]