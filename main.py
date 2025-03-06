import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_links(url):
    
    try:
        ua = UserAgent()
        headers = {"User-Agent" : ua.random}
        data = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(data.text, "html5lib")
        
        all_links = []
        
        contents = soup.find_all("div", class_="single-blog-content")
        
        for content in contents:
            link = content.find("a", target = "_blank")
            all_links.append(link.get("href"))
        
        return all_links
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la URL {url}: {e}")
        return []
    
def find_all_links_in_month(month):
    url = "https://www.lajornadamaya.mx/k'iintsil/{}-2021".format(month)
    return get_links(url)

def get_info(link):
    
    try:
        ua = UserAgent()
        headers = {"User-Agent" : ua.random}
        data = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(data.text, "html5lib")
        
        # Titulo
        try:
            title = soup.find("h1").get_text(strip=True) 
        except AttributeError:
            print(f"Título no encontrado: {link}")
            title = "Sin Titulo"
        # Fecha
        try:
            info = soup.find("div", class_="post-meta")
            if not info:
                raise ValueError("Informacion no encontrada")
            
            date_pattern = r"\d{2}/\d{2}/\d{4}"
            date_match = re.search(date_pattern, info.get_text())
            if not date_match:
                raise ValueError("Fecha no encontrada")
             
            date = date_match.group().strip() 
            
        except (AttributeError, ValueError) as e:
            print(f"Error al extraer la fecha: {link}")
            date = "Fecha desconocida"
        # Ubicacion
        try: 
            location = info.find_next("p").find_next("p").get_text(strip=True)[13:]
        
        except AttributeError:
            print(f"Ubicacion no encontrada: {link}")
            location = "Sin Ubicacion"
        # Contenido
        try:
            article = info.find_next("p").find_next("p")
            text = ""
            if not article:
                raise ValueError("Articulo no encontrado")
            
            paragraphs = article.find_all_next("p")
            for paragraph in paragraphs :
                if not paragraph.find("strong"):
                    text += paragraph.get_text() + "\n"
                
        except (AttributeError, ValueError) as e:
            print(f"Error al extraer el articulo: {link}")
            text = "Contenido no disponible"
        
        # Autor
        try:
            author = info.find_next("p").get_text()
        except AttributeError:
            print(f"Error al extraer el autor: {link}")
            author = "Desconocido"
        
        # Traductora
        try:     
            content = soup.find_all("div", class_="single-blog-content")[-1]    
            translator_pattern = r"Xak'alutskíinsa'an tumen:\s+(\w+\s\w+\s\w+)"
            translator_match = re.search( translator_pattern, content.get_text())
            traductor = translator_match.group(1).strip()
            
        except (IndexError, AttributeError):
            print(f"Error al extraer el traductor: {link}")
            traductor = "Desconocido"
        
        return {
            "Fecha": date,
            #"Autor": author,
            #"Traductor": traductor,
            #"Ubicacion": location,
            "Titulo": title,
            "Contenido": text.strip()
        }
         
    except requests.exceptions.RequestException as e:
        print(f"Error en la URL {link}: {e}")
        return None

def scraping():
    #months = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    months = ["enero"]
    df = pd.DataFrame()
    dfs = []
    
    for month in months:
        all_links = find_all_links_in_month(month)
        
        data_month = []
    
        print(f"Mes:{month}, Total: {len(all_links)} \n")
        
        for link in all_links:
            if link: 
                info = get_info(link)
                if info:
                    data_month.append(info)
            
        df_month = pd.DataFrame(data_month)
        dfs.append(df_month)
        
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv("datos_analisis.csv", index=False, encoding='utf-8')
    
scraping()

    
 