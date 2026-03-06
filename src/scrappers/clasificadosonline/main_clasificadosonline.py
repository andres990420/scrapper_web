import re
from utils.utils import check_url_clasificadosonline
from model.temporizador import Temporizador
from scrappers.clasificadosonline.scraper import scraping_clasifiadosonline

def main_clasificadosonline():
    stop_scrap = False
    while not stop_scrap:
        if url:= check_url_clasificadosonline():
            print(f"<----- Preparing the scraping ... ----->")
            with Temporizador():
                scraping_clasifiadosonline(url)
            valid_response = False
            while not valid_response:
                response = str(input("Do you want to realize another scraping? (y/n): "))
                patter_yes_confirmation = r'\b(?:yes|y|si|s)\b'
                patter_no_confirmation = r'\b(?:n|no)\b'
                if re.search(patter_no_confirmation, response, re.IGNORECASE):
                    valid_response = True
                    stop_scrap = True
                elif re.search(patter_yes_confirmation, response, re.IGNORECASE):
                    valid_response = True
                else: print("Invalid response")



        # if not re.match(r'^https://www\.clasificadosonline\.com/UD(?:RentalsListing|REListing)(?:Adv)?\.asp\?[^"\'\s]+', URL.strip()):
        #     print("Invalid URL format. Please enter a valid URL.")
        #     continue
        # else:
        #     print(f"<----- Preparing the scraping ... ----->")                         
        #     # with Temporizador():
        #     #     scraping_clasifiadosonline(URL.strip())
            
            