import datetime
from pathlib import Path
import requests
from model.clasificadosonline_model import ClasificadosOnlinePropertyClass
from helpers.helpers import HEADERS

PROPERTIES_FOLDER = Path.cwd() / "properties"

def create_folders(properties: ClasificadosOnlinePropertyClass):
    #Chequeamos si existe la carpeta "properties", si no existe, se crea.
    
    if not (PROPERTIES_FOLDER).exists():
        (Path.cwd().parent / "properties").mkdir(parents=True, exist_ok=True)
        print("The 'properties' folder has been created.")    
    
    # Creamos la carpeta para cada busqueda usando la fecha y hora actual para evitar duplicados.
    new_folder_for_property = PROPERTIES_FOLDER / ("clasificadosOnline_" + datetime.datetime.now().strftime("%Y-%m-%d_%Hh-%Mm-%Ss"))
    new_folder_for_property.mkdir(parents=True, exist_ok=True)
    print(f"New folder created for property: {("clasificadosOnline_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))}")

    # Creamos la carpeta para cada propiedad usando un contador para evitar duplicados.
    counter = 1
    print(f"<----- Downloading and saving property information and images... ----->")
    for property in properties:
        property_folder = new_folder_for_property / f"property_{counter}"
        property_folder.mkdir(parents=True, exist_ok=True)
        counter += 1

        # Guardamos la url y la info de la propiedad en un archivo dentro de la carpeta de la propiedad. 
        url_file = property_folder / "info.txt"
        with open(property_folder / "info.txt", "w", encoding="utf-8") as archive:
            archive.write("Url: " + str(property.url) + "\n")
            archive.write("Title: " + str(property.title) + "\n")
            archive.write("Price: " + str(property.price) + "\n")
            archive.write("Bedrooms: " + str(property.bedrooms) + "\n")
            archive.write("Bathrooms: " + str(property.bathrooms) + "\n")
            archive.write("Pets Allowed: " + str(property.pets) + "\n")
            archive.write("Parking: " + str(property.parking) + "\n")
            archive.write("License/Agent: " + str(property.license_agent) + "\n")
            archive.write("Contact: " + str(property.contact) + "\n")
            if property.optioned:
                archive.write("Optioned: " + str(property.optioned) + "\n")
            archive.write("Description: " + str(property.description) + "\n")

        # Guardamos las imagenes de la propiedad en la carpeta de la propiedad.
        for index, image_url in enumerate(property.images):
            image_response = requests.get(image_url, headers=HEADERS, timeout=15)
            if image_response.status_code == 200:
                with open(property_folder / f"image_{index + 1}.jpeg", "wb") as img_file:
                    img_file.write(image_response.content)

    print(f"{len(properties)} folders created for properties in {new_folder_for_property}.")



if __name__ == "__main__":
    create_folders([])