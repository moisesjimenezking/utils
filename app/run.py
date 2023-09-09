from create_app import app, tokenTestTelegram, es
from flask import redirect, request, jsonify

#? LibraryController
from library import controller
from modules.setting import controller
from modules.service_payment import controller
from modules.patterns import controller
from telegram import Bot, Update

#
# Metodo principal de prueba
#?
@app.route('/', methods=['GET'])
def index():
    return {"message": "API Utils Activa."}


#TODO: Se inicia la aplicacion
if __name__ == '__main__':
    # bot = Bot(tokenTestTelegram)
    app.run(host='0.0.0.0', port=5000)
