from .classStructure import PatternsClass, PatternsHistoryClass
import math, logging, textwrap
from itertools import combinations, permutations, product
from datetime import datetime, timedelta, date

logging.basicConfig(level=logging.DEBUG)

class PatternsModel:
    
    @classmethod
    def patternsAdd(cls, data):
        try:
            patterns = data["patterns"].replace("-", "")
            multipler = "X{}".format(int(data["multipler"]))
            
            patternsData = PatternsClass.getPatternsMultiple(patterns, multipler)
            last = None
            if "id" in patternsData:
                lastUpdatePatterns = PatternsClass.getPatternsLast(multipler)
                if lastUpdatePatterns is not None:
                    if patternsData["history"] is None or len(patternsData["history"]) == 51:
                        patternsData["history"] = lastUpdatePatterns["patterns"]
                        
                    if lastUpdatePatterns["history"] is None or len(lastUpdatePatterns["history"]) == 51:
                        lastUpdatePatterns["history"] = patternsData["patterns"]
                    elif len(lastUpdatePatterns["history"]) == 25:
                        lastUpdatePatterns["history"] = lastUpdatePatterns["history"]+"-"+patternsData["patterns"]
                        
                        updatePrevios = PatternsClass.getPatternsPut(lastUpdatePatterns["id"])
                        updatePrevios.history = lastUpdatePatterns["history"]
                        last = PatternsClass.putData(updatePrevios)            
                else:
                    patternsData["history"] = None
                    
                patternsData["quantity"] += 1
                
                if "average" in data:
                    patternsData["average"] = data["average"]
                    

                
                update = PatternsClass.getPatternsPut(patternsData["id"])
                update.multipler = multipler
                update.patterns = patterns
                update.history = patternsData["history"]
                update.quantity = patternsData["quantity"]
                update.average = patternsData["average"]
                update.datetime_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                response = {
                    "response":{
                        "Current":PatternsClass.putData(update),
                        "Last": last
                    },
                    "status_http": 201
                }
            else:
                raise Exception("Patron no encontrado")
            
        except Exception as e:
            response = {
                "response":{
                    "message":str(e)
                },
                "status_http": 400
            }
            
        return response
    
    
    @classmethod
    def patternsLike(cls, data):
        try:
            multipler = "X{}".format(int(data["multipler"]))
            search = data["patterns"].replace("-", "").replace("?", "_")
            
            patternsData = PatternsClass.getPatternsLike(multipler, search)
            if len(patternsData) > 0:
                for x in range(len(patternsData)):
                    patternsData[x].update({"historyVector":PatternsHistoryClass.getPatternsIdHistory(patternsData[x]["id"])})
                 
                last = PatternsClass.getPatternsLast(multipler)
                if last is not None:
                    historiLast = PatternsHistoryClass.getPatternsIdHistoryLast(multipler,last["patterns"]+"%") 
                    lasAux = {
                        "patterns"      :'-'.join(textwrap.wrap(last["patterns"] , 5)),
                        "patternsVector": textwrap.wrap(last["patterns"] , 5),
                        "history"       : historiLast
                    }
                    patternsData.append({"Last":lasAux})
                
                response = {
                    "response":patternsData,
                    "status_http":200
                }
            else:
                raise Exception("Sin datos")
                
        except Exception as e:
            response = {
                "response":{
                    "message":e.args[0] if len(e.args) > 1 else str(e)
                },
                "status_http": 400
            }
            
        return response
    
    
    @classmethod
    def patternsAll(cls, data):
        try:
            if "multipler" in data: 
                data["multipler"] = "X{}".format(int(data["multipler"]))
                
            if "patterns" in data:
                data["patterns"] = data["patterns"].replace("-", "")
                
            patternsData = PatternsClass.getData(**data)
            if len(patternsData) > 0:
                response = {
                    "response":patternsData,
                    "status_http":200
                }
            else:
                raise Exception("Sin datos")
                
        except Exception as e:
            response = {
                "response":{
                    "message":e.args[0] if len(e.args) > 1 else str(e)
                },
                "status_http": 400
            }
            
        return response
    
    
    @classmethod
    def combinations(cls, data):
        try:
            # Calcular el número de combinaciones
            combinaciones = math.comb(int(data["quantity"]), int(data["one"]))

            response = {
                "response":{
                    "message":"Numero de combinaciones posible: {}".format(str(combinaciones))
                },
                "status_http": 200
            }
        except Exception as e:
            response = {
                "response":{
                    "message":str(e)
                },
                "status_http": 400
            }
            
        return response
    
    
    @classmethod
    def combinationsString(cls, data):
        try:
            positions = list(permutations(range(25), int(data["multipler"])))

            combinations = []
            for pos in positions:
                combination = ['0'] * 25
                for i in range(len(pos)):
                    combination[pos[i]] = '1'

                combinations.append(''.join(combination))
                
            combinations = list(set(combinations))

            for c in range(len(combinations)):
                datapost = {
                    "multipler":"X{}".format(int(data["multipler"])),
                    "patterns":combinations[c]
                }
                
                PatternsClass.postData(**datapost)
                
            response = {
                "response":{
                    "message":combinations
                },
                "status_http": 200
            }
        except Exception as e:
            response = {
                "response":{
                    "message":str(e)
                },
                "status_http": 400
            }
            
        return response