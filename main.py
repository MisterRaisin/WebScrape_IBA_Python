from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

LINKS_LIST = ['https://iba-world.com/category/iba-cocktails/the-unforgettables/',
              'https://iba-world.com/category/iba-cocktails/contemporary-classics/',
              'https://iba-world.com/category/iba-cocktails/new-era-drinks/']
EXPORT_TO_EXCEL = False

def fetch_cocktails(cocktail_list, link):

    url = link
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = bs(r.content, 'html.parser')


    main_text = soup.find_all('div', attrs={"id" : 'main-content'})[0]
    main_text = main_text.find_all('div', attrs = {'class' : 'et_pb_salvattore_content'})[0]

    for card in main_text.find_all('article', attrs = {'class' : re.compile('et_pb_post')}):
        cocktail = {}
        row1 = card.find('a', attrs = {'class' : 'entry-featured-image-url'})
        image = row1.find('img')
        img = image['src']
        name = image['alt']
        cocktail_link = row1['href']

        temp_r = requests.get(cocktail_link, headers=headers)
        temp_soup = bs(temp_r.content, 'html.parser')

        text =  temp_soup.find_all('div', attrs={"class" : 'et_pb_module et_pb_post_content et_pb_post_content_0_tb_body blog-post-content'})[0]
        info = text.find_all('p')

        method = info[1].get_text()
        garnish = info[2].get_text()

        ingredient_list = info[0].get_text().split('\n')
        


        cocktail['name'] = name
        cocktail['image'] = img
        cocktail['ingredient_list'] = ingredient_list
        cocktail['method'] = method
        cocktail['garnish'] = garnish
        cocktail['link'] = cocktail_link

        cocktail_list.append(cocktail)





cocktail_list = []
for LINK in LINKS_LIST:
    fetch_cocktails(cocktail_list, LINK)


if EXPORT_TO_EXCEL:
    df = pd.DataFrame(data=cocktail_list)
    df = df.sort_values('name')
    df.to_excel('cocktails.xlsx', index=False)

