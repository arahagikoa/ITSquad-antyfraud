import openai
import os
import requests
from PIL import Image


openai.api_base = "https://arahagikoa.openai.azure.com/"
openai.api_key = "6ffbc6072d9e4853bfd085bf4c09d435"   
openai.api_version = '2023-06-01-preview'
openai.api_type = 'azure'

input_image = "as"
generation_response = openai.Image.create(
    prompt='You are supposed to tak the input Image, and change the persons face on it',   
    size='1024x1024',
    n=2
)

# Set the directory for the stored image
image_dir = os.path.join(os.curdir, 'images')

if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

image_path = os.path.join(image_dir, 'generated_image1.png')

image_url = generation_response["data"][0]["url"] 
generated_image = requests.get(image_url).content 
with open(image_path, "wb") as image_file:
    image_file.write(generated_image)


image = Image.open(image_path)
image.show()