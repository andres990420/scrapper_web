import re


def check_url_clasificadosonline():
    url_valid = False
    while not url_valid:
         url = input("Enter the URL to scrape: ")
         if not re.match(r'^https://www\.clasificadosonline\.com/UD(?:RentalsListing|REListing)(?:Adv)?\.asp\?[^"\'\s]+', url.strip()):
            print("Invalid URL format. Please enter a valid URL.")
            continue
         else:
            url_valid = True
            return url.strip()