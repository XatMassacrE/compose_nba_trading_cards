#coding=utf-8
__author__='xat'

import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw

need_manual_compose = []

team_path = './logo/'
player_path = './player_img/'
output_path = './trading_cards/'
font_file = './assets/msyh.ttf'
card_decorate_path = './assets/'

player_category = ["SUPER", "CORE", "BLUE", "SIX", "BENCH"]


mock_data = [
    {
        'id': 1966,
        'cn_name': '勒布朗-詹姆斯',
        'team_id': 5,
        'category': 'SUPER'
    },
    {
        'id': 1977,
        'cn_name': '克里斯-波什',
        'team_id': 14,
        'category': 'SUPER'
    }
]

def compose(player_img, name, team_logo, category_img, output_name):
    
    card_bg = card_decorate_path + 'bg.png'
    player_img_offset_height = 15

    if not os.path.isfile(player_path + player_img):
        need_manual_compose.append(player_img)
        print(player_path + player_img + ' is not exist')
        return 
 
    # deal with high player image
    h = calculateUsefulHeight(player_img)
    if h > 310:
        offset = h - 310
        player_img_offset_height += offset 

    player_img = Image.open(player_path + player_img).convert('RGBA')
    bg_img = Image.open(card_decorate_path + category_img).convert('RGBA')
    card_bg_img = Image.open(card_bg).convert('RGBA')
    logo = Image.open(team_path + team_logo).convert('RGBA')

    logo = logo.resize((100,100), Image.ANTIALIAS)

    card_bg_img.paste(player_img, (35,player_img_offset_height), player_img)
    card_bg_img.paste(bg_img, (0,0), bg_img)
    card_bg_img.paste(logo, (95,315), logo)

    font = ImageFont.truetype(font_file, 20)
    d = ImageDraw.Draw(card_bg_img) 

    try:
        name = unicode(name, 'utf-8')
    except NameError:
        name = name
    d.text((12, 12), name, font=font, fill=(255,255,255))
    
    card_bg_img.save(output_path + output_name, quality=100)

def compose_all(all):
    for player in all:
        id = player['id']
        # if id == 1966:
        if True:
            category = player['category']
            player_img =  str(id) + '.png'
            
            team_id = player['team_id']
            team_img = str(team_id) + '.png'
            name = player['cn_name']            
            category = player_category.index(category) + 1
            category_img = 'card_bg_' + str(category) + '.png'

            output_name = str(id) + '.png'
            print('start compose ' + str(id))
            compose(player_img, name, team_img, category_img, output_name)

def calculateUsefulHeight(img):
    img = Image.open(player_path + img).convert('RGBA')
    w, h = img.size
    mat = np.array(img)

    for i in range(mat.shape[0]):
        if not allEqual(mat[i]):
            return h - i
 
def allEqual(line):
    w = len(line)
    if not w:
        return True
    init_value = line[0][3]
    step = 10
    for i in range(int(round(w/step))):
        if line[i * step][3] == init_value:
            continue
        else:
            return False
    return True       

if __name__ == '__main__':
    
    compose_all(mock_data)
    if need_manual_compose:
        print(need_manual_compose)
