'''
Descargar una el .html de la pagina para hacer pruebas
'''
import requests

url = "https://www.lajornadamaya.mx/k'iintsil/35167/jk-im-xunaan-paula-juntuul-xk-am-paal-jach-k-ajoolta-an-zona-maya"
response = requests.get(url)

with open("pagina.html", "w", encoding="utf-8") as file:
    file.write(response.text)

'''
    with open("pagina.html", "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html5lib")
'''

