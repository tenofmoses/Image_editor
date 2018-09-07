from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import re 
import textwrap
import time
from token import token

group = -41682596
url = 'https://api.vk.com/method/'

def get_sources(url, token):
    method = 'wall.get'
    payload = { 'owner_id': group, 'count': '50', 'offset': '1350', 'v': '5.52', 'access_token': token}

    return requests.get(url + method, params=payload) 


def save_img(photo_name, image):
    out = open('input_img/' + photo_name + '.jpg', 'wb')
    out.write(image.content)
    out.close()


def add_text(text, combined_image):
    img_text = Image.new('RGB', (photo_size[0], photo_size[1]), color=(255,255,255,255))
    font = ImageFont.truetype('fonts/ProximaNova-Regular.ttf', 20)
    offset = 10
    photo_size = combined_image.size

    for line in textwrap.wrap(text, width=55):
        ImageDraw.Draw(img_text).text((20, offset), line, font=font, fill="#000000")
        offset += font.getsize(line)[1]

    img_end = Image.new('RGB', (photo_size[0], photo_size[1] + offset + 20))
    img_end.paste(img_text, (0, 0))
    img_end.paste(photo, (0, offset + 20))

    # ImageDraw.Draw(img_end).text((50, 200), 'vk.com/mammy_deti', font=font, fill=(255,255,255,300))

    img_end.save('output_img/' + photo_name + '.jpg')


def combine_images(first_image, second_image):
    first_photo = ImageOps.mirror(Image.open('input_img/' + first_image + '.jpg'))
    second_photo = ImageOps.mirror(Image.open('input_img/' + second_image + '.jpg'))


def search_relevance_image(text, url, token):
    time.sleep(1)
    method = 'newsfeed.search'
    payload = { 'q': text, 'count': '30', 'v': '5.52', 'access_token': token}

    res = requests.get(url + method, params=payload).json()

    for item in res['response']['items']: 
        try:
            return item['attachments'][0]['photo']['photo_604']
        except KeyError:
            continue
        except IndexError:
            continue


res = get_sources(url, token).json()['response']['items']

for item in res:
    text = item['text']
    try:
        first_photo_link = item['attachments'][0]['photo']['photo_604']
    except KeyError:
        continue
        
    image_name = re.findall('\w+', first_photo_link)[-2]

    try:
        relevance_image = search_relevance_image(text, url, token)
    except:
        continue

    if relevance_image:
        print(text)
        print(relevance_image)

        relevance_image_name = re.findall('\w+', relevance_image)[-2]

    first_image = requests.get(first_photo_link)
    save_img(image_name, first_image)

    second_image = requests.get(second_photo_link)
    save_img(relevance_image_name, relevance_image)

    combine_images(image_name, relevance_image_name)
    # add_text(text, photo_name)

