from typing import Optional

class ClasificadosOnlinePropertyClass:
    def __init__(self, url,title, price, bedrooms, 
                 bathrooms, pets: Optional[str] = None, parking: Optional[str] = None, 
                 license_agent=None, contact=None, 
                 description=None, images=None, optioned: Optional[bool] = False):
        self.url = url
        self.title = title
        self.price = price
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.pets = pets
        self.parking = parking
        self.license_agent  = license_agent
        self.contact = contact
        self.description = description
        self.images = images
        self.optioned = optioned
    
    def __str__(self):
        return f'''URL: {self.url}\n
        Title: {self.title}\n
        Price: {self.price}\n
        Bedrooms: {self.bedrooms}\n
        Bathrooms: {self.bathrooms}\n
        {'Pets Allowed: ' + self.pets if self.pets else 'Pets Allowed: None'}\n
        {'Parking: ' + self.parking if self.parking else 'Parking: None'}\n
        {'Optioned: ' + str(self.optioned) if self.optioned else 'Optioned: False'}\n
        License/Agent: {self.license_agent}\n
        Contact: {self.contact}\n
        Description: {self.description}\n
        Images: {", ".join(self.images)}'''