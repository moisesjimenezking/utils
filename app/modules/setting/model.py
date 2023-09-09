from modules.setting.classStructure import Setting
from library.libraryTelegram import Telegram


#
#
# class SettingModel
#
#
class SettingModel:
    
    @classmethod
    def notificStatusWhatsapp(cls, data):
        try:
            listStatus = {
                "FAILED":"🆘 - Plataforma de WhatsApp caída.",
                "RUNNING":"✅ - Plataforma de WhatsApp funcionando con normalidad.",
                "INTERMITENT":"⚠️ - Plataforma de WhatsApp intermitente."
            }
            code = "WHATSAPP"
            last_state = Setting.getCode("WHATSAPP")
            
            if("status" in data and str(data.get("status").upper()) != str(last_state.value)):
                status = data.get("status").upper()
                
                last_state.value = status
                Setting.putData(last_state)
                recent_state = Setting.getCode("WHATSAPP")
                
                if(str(recent_state.value) == str(status) and status in listStatus):
                    data = {
                        "message": listStatus[status],
                        "chanel": "-1001818909594" if 'type' in data else "-1001519155334"
                    }
                    
                    telegram = Telegram.send_message(data)
                    
                    response = {"response":{"message" : "Update", "Telegram":telegram["response"]}, "status_http":200}
                else:
                    response = {"response":{"message" : "No Update"}, "status_http":400}
            else:
                response = {"response":{"message" : "No Update"}, "status_http":400}
        except Exception as e:
            response = {"response":{"message":str(e)}, "status_http": 400}
            
        return response