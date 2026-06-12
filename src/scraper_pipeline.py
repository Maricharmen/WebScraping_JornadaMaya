import re
from pathlib import Path
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Resolve path to the data directory 
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def get_links(url):
    """Fetches all article links from a given category overview page"""
    try:
        ua = UserAgent()
        headers = {"User-Agent" : ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html5lib")
        all_links = []
        
        contents = soup.find_all("div", class_="single-blog-content")
        for content in contents:
            link = content.find("a", target = "_blank")
            if link and link.get("href"):
                all_links.append(link.get("href"))
        
        return all_links
    
    except requests.exceptions.RequestException as e:
        print(f"[Error] Failed to fetch URL {url}: {e}")
        return []
    
def find_all_links_in_month(month):
    """Constructs the URL for a specific month and retrieves its links"""
    url = f"https://www.lajornadamaya.mx/k'iintsil/{month}-2021"
    return get_links(url)

def get_info(link):
    """Scrapes structured metadata and content from a single article link"""
    try:
        ua = UserAgent()
        headers = {"User-Agent" : ua.random}
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html5lib")
        
        # Extract Title
        try:
            title = soup.find("h1").get_text(strip=True) 
        except AttributeError:
            print(f"[Warning] Title not found: {link}")
            title = "Untitled"
            
        # Extract Date
        try:
            info = soup.find("div", class_="post-meta")
            if not info:
                raise ValueError("IPost metadata section not found")
            
            date_pattern = r"\d{2}/\d{2}/\d{4}"
            date_match = re.search(date_pattern, info.get_text())
            if not date_match:
                raise ValueError("Date pattern matching failed")
             
            date = date_match.group().strip() 
            
        except (AttributeError, ValueError) as e:
            print(f"[Warning] Error extracting data from {link} : {e}")
            date = "Unknown Date"
            
        # Extract Location
        try: 
            location = info.find_next("p").find_next("p").get_text(strip=True)[13:]
            if not location:
                location = "Unknown Location"
        except AttributeError:
            print(f"[Warning] Location not found: {link}")
            location = "Unknown Location"
            
        # Extract Article Body Content
        try:
            article = info.find_next("p").find_next("p")
            text = ""
            if not article:
                raise ValueError("Article body root element not found")
            
            paragraphs = article.find_all_next("p")
            for paragraph in paragraphs :
                if not paragraph.find("strong"):
                    text += paragraph.get_text() + "\n"
                
        except (AttributeError, ValueError) as e:
            print(f"[Warning] Error extracting article body from {link} : {e}")
            text = "Content Unavailable"
        
        # Extract Author
        try:
            author = info.find_next("p").get_text()
            if not author:
                author = "Unknown Author"
        except AttributeError:
            print(f"[Warning] Error extracting author from {link}")
            author = "Unknown Author"
        
        # Extract Maya Translator
        try:     
            content = soup.find_all("div", class_="single-blog-content")[-1]    
            translator_pattern = r"Xak'alutskíinsa'an tumen:\s+(\w+\s\w+\s\w+)"
            translator_match = re.search( translator_pattern, content.get_text())
            if translator_match:
                translator = translator_match.group(1).strip()
            else:
                translator = "Unknown Translator"
                
        except (IndexError, AttributeError):
            print(f"[Warning] Error extracting translator from {link}")
            translator = "Unknown Translator"
        
        return {
            "Date": date,
            "Autor": author,
            "Translator": translator,
            "Location": location,
            "Title": title,
            "Content": text.strip()
        }
         
    except requests.exceptions.RequestException as e:
        print(f"[Error] Network failure on URL {link}: {e}")
        return None

def start_scraping():
    """Main execution loop to pipeline scraping processes into CSV output"""
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio", 
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    dfs = []
    
    for month in months:
        all_links = find_all_links_in_month(month)
        data_month = []

        print(f"Processing Month:{month} | Total links found: {len(all_links)} \n")
        
        for link in all_links:
            if link: 
                info = get_info(link)
                if info:
                    data_month.append(info)
        
        if data_month:
            df_month = pd.DataFrame(data_month)
            dfs.append(df_month)
            
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        output_file = DATA_DIR / "processed_articles.csv"
        final_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"[Success] Scraping execution completed. Dataset saved to {output_file}")
    else: 
        print("[Info] No data extracted across the execution target.")
      
if __name__ == "__main__":
    start_scraping()

    
 