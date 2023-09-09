import requests, json, subprocess
from bs4 import BeautifulSoup
import re

#
#? Class Bcv
#
class Tasas:
    
    @classmethod
    def bcv(cls):
        try:
            url = "https://www.bcv.org.ve/"
            response = requests.get(url, verify=False)

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            element = soup.find('div', id='dolar')
            
            if element is not None:
                element = element.get_text().replace("\n", "").strip().split('  ')
                result = {
                    element[0] : round(float(element[1].replace(",",".")), 2)
                }
            else:
                raise Exception("Valor vacio.")
            
            response = {
                "response"      : result, 
                "status_http"   : 200
            }
        except Exception as e:
            response = {
                "response"      : {"message" : e},
                "status_http"   : 400
            }

        return response
    
    
    @classmethod
    def promedioBcv(cls):
        try:
            url = "https://monitordolarvenezuela.com/"
            response = requests.get(url, verify=False)

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.find_all('div', class_='col-12 col-sm-4 col-md-2 col-lg-2')
            
            result = list()
            for element in elements:
                aux = element.get_text().replace("\n", " ").strip().replace("@", "").replace("  ", " ")
                indexes = [i for i, c in enumerate(aux) if c == ' ']
                
                if str(aux[:2]) != "--":
                    if "www" not in aux[indexes[0]+1:indexes[1]]:
                        aux = aux[:indexes[0]]+aux[indexes[1]:]
                        indexes = [i for i, c in enumerate(aux) if c == ' ']
                        
                    if re.search('[a-zA-Z]',aux[indexes[3]+1:indexes[4]]):
                        cadenaAux = aux[indexes[3]+1:indexes[4]]
                        remplace = re.sub('[a-zA-Z:]', '', cadenaAux)+" "+re.sub('[0-9,]', '', cadenaAux)
                        aux = aux.replace(cadenaAux, remplace)
                    
                    splitData = aux.split(" ")
      
                    dictaux = {
                        "name": splitData[0],
                        "price": round(float(splitData[4].replace(",",".")), 2),
                        "datetime": splitData[6]+" "+splitData[7].replace("AM", "AM - ").replace("PM", "PM - ")
                    }

                    if(round(float(splitData[4].replace(",",".")), 2) > 1):
                        result.append(dictaux)

            response = {
                "response"      : result,
                "status_http"   : 200
            }
        except Exception as e:
            response = {
                "response"      : {"message" : e},
                "status_http"   : 400
            }

        return response

class Spider:
    
    @classmethod
    def consultCne(cls, data):
        try:
            elementsP = "http://www.cne.gob.ve/web/registro_electoral/ce.php?nacionalidad=|NA|&cedula=|NUM|".replace("|NA|", data.get('nationality').upper()).replace("|NUM|", data.get('number'))
            result = subprocess.run(["curl", elementsP],stdout=subprocess.PIPE, text=True)

            html_content = result.stdout
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.find_all('td')
            listAux = list()
            for element in elements:
                listAux.append(element.get_text().replace("\n", ""))

            if(listAux[14] != "Estado:"):
                message = listAux[14].split("...")[0].split(".")[0] if len(listAux[14].split("...")[0].split(".")[0]) > 3 else listAux[10].split(".")[0]
                raise Exception(message)
            
            consult = {
                "name"           : listAux[13].title(),
                "identification" : listAux[11],
                "state"          : listAux[15].split("EDO.")[1].title().strip(),
                "town"           : listAux[17].split("MP.")[1].title().strip()
            }
            
            response = {
                "response"      : consult,
                "status_http"   : 200
            }
        except Exception as e:
            response = {
                "response"      : {"message" : str(e)},
                "status_http"   : 400
            }

        return response
    
    @classmethod
    def consultPlayStoreVe(cls):
        try:
            url = "https://play.google.com/store/apps/details?id=com.giganovus.biyuyo&hl=es_VE&gl=US"
            response = requests.get(url, verify=False)

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            # boton = soup.find_all('div', class_="qZmL0")
            boton = soup.find('button', class_="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 aLey0c")
            # , class_='VfPpkd-u4ICaf'
            # Simular el evento de clic
            boton.click()
            soup = BeautifulSoup(boton, 'html.parser')
            # div class="VfPpkd-wzTsW"
            
            # listAux = list()
            # for element in elements:
            #     listAux.append(element.get_text().replace("\n", ""))

            # if(listAux[14] != "Estado:"):
            #     message = listAux[14].split("...")[0].split(".")[0] if len(listAux[14].split("...")[0].split(".")[0]) > 3 else listAux[10].split(".")[0]
            #     raise Exception(message)
            
            # consult = {
            #     "name"           : listAux[13].title(),
            #     "identification" : listAux[11],
            #     "state"          : listAux[15].split("EDO.")[1].title().strip(),
            #     "town"           : listAux[17].split("MP.")[1].title().strip()
            # }
            
            response = {
                "response"      : str(soup),
                "status_http"   : 200
            }
        except Exception as e:
            response = {
                "response"      : {"message" : str(e)},
                "status_http"   : 400
            }

        return response