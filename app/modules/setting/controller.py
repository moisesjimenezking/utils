from flask import request, jsonify
from create_app import app
from modules.setting.model import SettingModel


#
# Método para envio de mensajes a telegram
#? return @redirection
#
#
@app.route('/whatsapp_down', methods=['POST'])
def whatsappDown():
    try:
        data = request.args or request.values or request.form or request.json
        response = SettingModel.notificStatusWhatsapp(data)
    except:
        response = {"response":{"message":"Invalid Data"}, "status_http": 404}
        
    return jsonify(response["response"]), response["status_http"]