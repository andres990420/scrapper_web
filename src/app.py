from model.temporizador import Temporizador
from scrappers.clasificadosonline.main_clasificadosonline import main_clasificadosonline
import json

def app():
    with open("basic_config.json", "r") as a:
        basic_config = json.load(a)
    print(f"Welcome to the webs Scraper! ----{basic_config['version']}----")
    list_of_pages = basic_config['list_pages']
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
                    main_clasificadosonline()
                                    
            else:
                print("Invalid page selection. Please choose a valid page from the list.")
    return 0

if __name__ == "__main__":
    app()