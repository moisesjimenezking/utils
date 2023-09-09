import requests
import json

class Whatsapp:
    
    @staticmethod
    def eventGroup(message, group, event):
        try:
            url = 'https://xclienttech/event_emit'
            eventName = event
            type = 'new_message_group'
            payload = {
                'msg': message,
                'from': group
            }
            
            result = requests.post(url, data={'eventName': eventName, 'payload':json.dumps(payload), 'type': type})
            
            response = {
                "response":{"message" : result.text},
                "status_http" : result.status_code
            }
            
        except Exception as e:
            response = {
                "response":{"message" : e},
                "status_http" : 400
            }
            
        return response
    
    @staticmethod
    def eventGroupTest(message):
        try:
            group = "120363133348179178@g.us"
            response = Whatsapp.eventGroup(message, group)
        except Exception as e:
            response = {
                "response":{"message" : e},
                "status_http" : 400
            }
        
        return response
        