import requests
from bs4 import BeautifulSoup
from model.clasificadosonline_model import ClasificadosOnlinePropertyClass
from scrappers.clasificadosonline.scraper_property_page import scrape_page_clasificados
from pathlib import Path
from scrappers.clasificadosonline.create_folder_for_urls import create_folders
from helpers.helpers import HEADERS, BASE_URL_CLASIFICADOSONLINE

WHITELIST_FILE = Path.cwd() / "whitelist.txt"

def scraping_clasifiadosonline(URL):
    list_urls = []
    list_properties = []
    
    # Revisamos si la url tiene el parametro "offset=0" para saber si existe mas de una pagina de resultados, 
    # si no lo tiene, significa que solo tiene 1 pagina de resultados para hacer scraping de las urls 
    # y se procede a comparar con la whitelist de urls para añadir las nuevas urls y crear las carpetas para cada propiedad.
    
    if URL.endswith("offset=0"):
        not_in_list = True
        offset = 0
        search_url = URL
        current_search = []
        
        while not_in_list == True:
            
            # Scraping de la lista de urls de las propiedades
            response = requests.get(search_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            tables = soup.find_all("table", class_="tbl-main-photo")
            for table in tables:
                current_search.append(f'{BASE_URL_CLASIFICADOSONLINE}{table.a.get("href")}')
            
            # Se compara la lista de urls encontradas en la busqueda actual con la lista de urls encontradas en las busquedas anteriores, 
            # si alguna url de la busqueda actual se encuentra en la lista de urls anteriores, 
            # significa que ya se han encontrado todas las urls y se termina el proceso de busqueda, 
            # si no se añaden las urls encontradas en la busqueda actual a la lista de urls encontradas y se continua con la siguiente busqueda.
            
            if current_search[0] in list_urls:
                not_in_list = False
                break
            
            list_urls.extend(current_search)
            current_search = []
            offset += 30
            search_url = URL.split("offset=")[0] + "offset=" + str(offset)
    else:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table", class_="tbl-main-photo")
        for table in tables:
            list_urls.append(f'{BASE_URL_CLASIFICADOSONLINE}{table.a.get("href")}')
        
    print(f"Total URLs found: {len(list_urls)}")

    # !--- Creando/Actualizando la whitelist de urls y creando carpetas de cada propiedad ---!

    # Si no existe el archivo whitelist.txt, se crea y se añaden las urls y se crean las carpetas para cada propiedad.
    if not WHITELIST_FILE.exists():
        with open(WHITELIST_FILE, "w", encoding="utf-8") as archive:
            for url in list_urls:
                archive.write(str(url) + "\n")           
        print(f"New whitelist with {len(list_urls)} URLs added.")
        
        # Scraping de cada url para obtener la info de cada propiedad y crear las carpetas para cada propiedad.
        for url in list_urls:
            property_info = scrape_page_clasificados(url)
            list_properties.append(property_info)
        
        create_folders(list_properties)
    
    # Si el archivo de whitelist.txt existe, se compara con las urls nuevas y se añaden las nuevas al archivo.
    else:
        # Se copia el contendio actual del archivo whitelist.txt en una lista para comparar con las urls nuevas.
        content= []        
        with open(WHITELIST_FILE, "r", encoding="utf-8") as archive:
            for line in archive.read().splitlines():
                content.append(line)
        
        new_content = []
        # Se comparan las urls nuevas con las urls del archivo
        for url in list_urls:
            if url not in content:
                new_content.append(url)

        # Si hay urls nuevas, se añaden al archivo y se crean las carpetas para cada propiedad.
        if new_content != []:
            counter_new_urls = 0
            with open(WHITELIST_FILE, "a", encoding="utf-8") as archive:
                for url in new_content:
                    archive.write(url + "\n")
                    counter_new_urls += 1
            
            print(f"{counter_new_urls} new URLs added to whitelist.")
            
            for url in new_content:
                property_info = scrape_page_clasificados(url)
                list_properties.append(property_info)
            
            create_folders(list_properties)
        else:
            print("No new URLs to add.")

if __name__ == "__main__":
    URL = "https://www.clasificadosonline.com/UDRentalsListingAdv.asp?RentalsPueblos=Guaynabo&Category=Apartamento&Bedrooms=2&LowPrice=0&HighPrice=9999999999999999&IncPrecio=1&Area=&redirecturl=%2FUDRentalsListingAdvMap%2Easp&BtnSearchListing=Listado&offset=0"
    scraping_clasifiadosonline(URL)