import os
from dotenv import load_dotenv
from model.temporizador import Temporizador
from scrappers.clasificadosonline.main_clasificadosonline import main_clasificadosonline
load_dotenv()

def app():
    print(f"Welcome to the webs Scraper! ----{os.getenv('version')}----")
    list_of_pages = os.getenv('list_of_pages').strip('[]').split(', ')
    print("Available pages to scrape:")
    available_pages = {}
    for i, page in enumerate(list_of_pages, 1):
        available_pages[i] = page
        print(f"{i}. {page}")

    valid_input_pages = False
    while not valid_input_pages:
        page_to_scrape = input("Select the page you want to scrape: ")
        if not page_to_scrape.isdigit() or page_to_scrape.strip() == "":
            print("Invalid input. Please select a valid page.")
        else:
            if int(page_to_scrape) in available_pages:
                if available_pages[int(page_to_scrape)] == "clasificadosOnline":
                    print(f"You selected: {available_pages[int(page_to_scrape)]}")
                    valid_input_pages = True
                    # if valid_url:= check_url_clasificadosonline():
                    #     print(f"<----- Preparing the scraping ... ----->")
                        # with Temporizador():
                            # scraping_clasifiadosonline(valid_url)
                    main_clasificadosonline()
                                    
            else:
                print("Invalid page selection. Please choose a valid page from the list.")
    return 0

if __name__ == "__main__":
    app()