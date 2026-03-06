import sys
from pathlib import Path

# Añadimos la carpeta 'src' al camino de búsqueda de Python
ruta_src = str(Path(__file__).resolve().parent.parent.parent)
if ruta_src not in sys.path:
    sys.path.append(ruta_src)

import requests
import re
from bs4 import BeautifulSoup
from helpers.helpers import HEADERS
from model.clasificadosonline_model import ClasificadosOnlinePropertyClass

# Busqueda del titulo del anuncio
def _scrape_title(soup, type):
    if type == "rental":
        title = soup.find("table", class_="translate").find("span", class_="Roboto Size16") # title
        return title.get_text(' ',strip=True) if title else "No title found"
    else:
        title = soup.find("p", class_="Tahoma12grisClanounder") # title
        return title.get_text(' ',strip=True) if title else "No title found"

# Busqueda informacion de la propiedad
def _scrape_info(soup, type):
    info = {"price": None, "bedrooms": None, "bathrooms": None, "pets": None, "parking": None, "license_agent": None, "optioned": None}
    if type == "rental":
        
        info_list = soup.find_all("span", class_="Roboto Size14", style="color:#888;") # Busqueda de info de precio de renta, cuartos, baños, mascotas, parqueo
        for element in info_list:
            if not element.a:
                for i in element:
                    if i.get_text(' ',strip=True).startswith("$"):
                        info["price"] = i.get_text(' ',strip=True)
                    elif i.get_text(' ',strip=True).startswith("Cuartos"):
                        info["bedrooms"] = i.next.get_text(' ',strip=True)
                    elif i.get_text(' ',strip=True).startswith("Baños"):
                        info["bathrooms"] = i.next.get_text(' ',strip=True)
                    elif i.get_text(' ',strip=True).startswith("Mascotas"):
                        info["pets"] = i.next.get_text(' ',strip=True)
                    elif i.get_text(' ',strip=True).startswith("Parking"):
                        info["parking"] = i.next.get_text(' ',strip=True)

        info_agent = soup.find_all("p") # Busqueda de info de license/agent
        for element in info_agent:
            if element.find("span", class_ = "Roboto Size14"):
                info["license_agent"] = element.span.get_text(' ',strip=True)
        
        return info
    else:

        price_info = soup.find("span", class_ = "Ver11C").strong.get_text(' ',strip=True) # Busqueda del precio de la propiedad
        info["price"] = price_info
    
        info_list = soup.find_all("div", class_="Roboto Size14") # Busqueda de info de cuartos, baños
        for element in info_list:
            if not element.a:
                for i in element:
                    if i.get_text(' ',strip=True).startswith("Cuartos"):
                        info["bedrooms"] = i.next.get_text(' ',strip=True).replace("-", "").strip()
                    elif i.get_text(' ',strip=True).startswith("Baños"):
                        info["bathrooms"] = i.strong.get_text(' ',strip=True).replace("-", "").strip()
        
        info_agent = soup.find_all("div", class_="translate", style="padding-left:8px") # Busqueda de info de license/agent
        for element in info_agent:
            if element.find("span", class_ = "Tahoma14BrownNound"):
                info["license_agent"] = element.span.get_text(' ',strip=True)

        info_optioned = soup.find("font", class_="Ver12C") # Busqueda si la propiedad esta opcionada
        if info_optioned:
            info["optioned"] = info_optioned.get_text(' ',strip=True)

        return info

# Busqueda del numero de contacto
def _scrape_contact(soup):
    contacts = []

    contact_list = soup.find_all("a", href=lambda x: x and x.startswith("tel:")) # contact
    if len(contact_list) > 1:
        for contact in contact_list:
            contacts.append(contact.get_text(' ',strip=True))
        return contacts
    else:
        return contact_list[0].get_text(' ',strip=True) if contact_list else "No contact found"

 # Busqueda de la descripcion del anuncio
def _scrape_description(soup, type):
    if type == "rental":
        description = soup.find_all("p", class_="Tahoma12grisClanounder", align="center") # description
        return description[3].get_text(' ',strip=True)
    else:
        description = soup.find_all("p", class_="Tahoma12grisClanounder", align="center") # description
        return description[1].get_text(' ',strip=True).replace("\r\n\r\n", " ").strip().replace("\r\n", " ").strip()

# Busqueda de las imagenes del anuncio
def _scrape_images(soup, response):
    urls_imagenes = re.findall(r'https://imgcache\.clasificadosonline\.com/(?:PP|FF)/(?:FR|FS)/[^"\']+_Big\.(?:jpg|jpeg)', response.text, re.IGNORECASE)
    # Eliminamos duplicados
    urls_unicas = list(set(urls_imagenes))
    return urls_unicas 

def scrape_page_clasificados(url):
    response = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    type = "rental" if url.startswith("https://www.clasificadosonline.com/UDRentalsDetail.asp?ReForRentAdID=") else "sale"

    title = _scrape_title(soup, type)
    info = _scrape_info(soup, type)
    contact = _scrape_contact(soup)
    description = _scrape_description(soup, type)
    images = _scrape_images(soup, response)

    return ClasificadosOnlinePropertyClass(
        url=url,
        title=title,
        price=info["price"],
        bedrooms=info["bedrooms"],
        bathrooms=info["bathrooms"],
        pets=info["pets"] if type == "rental" else None,
        parking=info["parking"] if type == "rental" else None,
        license_agent=info["license_agent"],
        contact=contact,
        description=description,
        images=images,
        optioned= False if type == "rental" else info["optioned"] if "optioned" in info else False
    )


if __name__ == "__main__":
    URL = "https://www.clasificadosonline.com/UDRealEstateDetail.asp?ID=4815016"
    propiedad = scrape_page_clasificados(URL)
    print(propiedad)