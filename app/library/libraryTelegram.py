import requests
from flask import jsonify
from datetime import datetime
from create_app import tokenBiyuyoTelegram
from telegram import Bot, Update

class Telegram:
    
    @staticmethod
    def send_message(data):
        try:
            channel_id = data.get('chanel')
            if("message" in data):
                if isinstance(data.get('message'), dict):
                    message = ""
                    for key, value in data.get('message').items():
                        message = message + str(key) + ": " + str(value) + "\n"
                else:
                    message = data.get('message')
            else:
                response = {"response":{"message":"Envio Fallido. E"},"status_http":400}
        
            url = f'https://api.telegram.org/bot{tokenBiyuyoTelegram}/sendMessage'

            params = {
                'chat_id': channel_id,
                'parse_mode': 'HTML',
                'text': f"{message}"
            }
            
            response = requests.post(url, params=params)
            response = response.json()
            
            if response['ok']:
                response = {"response":{"message":"Envio exitoso."},"status_http":200}
            else:
                response = {"response":{"message":"Envio Fallido. V"},"status_http":400}
        except Exception as e:
            response = {"response":{"message":str(e)},"status_http":400}
            
        return response 
    
    @staticmethod
    def notify_in_test_canal(data):
        try:
            data = data.copy()
            data.update({'chanel':'-1000000000000'}) # Canal de testa
            response = Telegram.send_message(data)
        except:
            response = {"response":{"message":"Envio Fallido. E"},"status_http":400}
        return response
    
    @staticmethod
    def notifyInProxyChanel(data):
        try:
            data = data.copy()
            data.update({'chanel':'-1000000000000'}) # Canal de proxy
            response = Telegram.send_message(data)
        except:
            response = {"response":{"message":"Envio Fallido. E"},"status_http":400}
        return response
    
    @staticmethod
    def notifyRechargeCertificationApi(data):
        try:
            data = data.copy()
            data.update({'chanel':'-1000000000000'}) # Canal de certificación
            response = Telegram.send_message(data)
        except:
            response = {"response":{"message":"Envio Fallido. E"},"status_http":400}
        return response
    
    @staticmethod
    def notifyChanelGroupWhatsapp(data):
        try:
            listEmoticon = {
                "new"  : "🆕 chat: ",
                "close": "🔐 chat: ",
                "check": "✅ chat: ",
            }
            
            data = data.copy()
            
            if isinstance(data.get('message'), dict):
                message = ""
                for key, value in data.get('message').items():
                    if key == "type" and value in listEmoticon:
                        message = message + listEmoticon[value]
                    
                    if key == "message":
                        message = message + value
                        
                response = Telegram.send_message({'chanel':'-1000000000000','message':message})
            else:
                data.update({'chanel':'-1000000000000'})
                response = Telegram.send_message(data)
                
        except Exception as e:
            response = {"response":{"message":"Envio Fallido. E","error":str(e)},"status_http":400}
        return response