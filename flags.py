import json
import requests
from PIL import Image
import io
from random import randint

class random():
    def __init__(self, pos):
        self.x_pos = pos[0]
        self.y_pos = pos[1]

    global randomizer
    def randomizer():
        #retrieves json file
        with open('assets/flags.json') as fp:
            #sets var data to load json file
            data = json.load(fp)
            info = data["flags"]
            #picks a random number between the index of the array
            random_index = randint(0, len(info)-1)
            #returns json values for Country && URL at preditermined random number
            return info[random_index]["Country"], info[random_index]["URL"]
            
    @staticmethod
    def get_image_from_url(url):
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        return image
      
    # country, url = randomizer()
    # print(country, 'this is the Url', url)
    
    def flag_image(self):
        #appends country && url to the return values of randomizer 
        country, url = random.randomizer()
        return randomizer.get_image_from_url(url)
        #requests the image
        # response = requests.get(url)      
        # with open("image.jpg", "wb") as f:
        #     f.write(response.content)


        


