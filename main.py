from bs4 import BeautifulSoup as BS
from pprint import pprint
import json
import requests
from fake_headers import Headers



def get_headers():

    return Headers(browser="firefox",os='win').generate()

def req_html(URL,params=""):
    r = requests.get(URL,headers=get_headers(), params=params).text
    return r



if __name__ == '__main__':


    url_cards = []
    d_f_urls = []
    base_hh = []
# получаем все ссылки на профессии в москве и питере на нужном количестве страниц
    for page in range(0,2):
        count = f'&page={page}'
        URL = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20{count}'
        main_url = req_html(URL)
        soup = BS(main_url,'lxml')
        h3_tag = soup.find_all('h3')
        for links in h3_tag:
            link = links.find('a')
            if link != None:
                href = link.get('href')
                if href in url_cards:
                    pass
                else:
                    url_cards.append(href)
            else:
                pass
# Фильтруем по jango и flask Оставляем только их
    for card in url_cards:
        l_lines = []
        main_card = req_html(card)
        soup = BS(main_card, 'lxml')
        items = soup.find('div',class_='bloko-tag-list')
        if items != None:
            l_lines = items.find_all('span')
        else:
            pass
        for l_line in l_lines:
            if 'django' in l_line.text.lower() or 'flask' in l_line.text.lower():
                if card in d_f_urls:
                    pass
                else:
                    d_f_urls.append(card)
            else:
                pass

# скрапим нужные данные, записываем в json
    for one_url in d_f_urls:
        main_card = req_html(one_url)
        soup = BS(main_card, 'lxml')
        h1_tag = soup.find('h1')
        position = h1_tag.text  # название вакансии
        div_vacancy = soup.find_all('div',class_='main-content')
        for span_tag in div_vacancy:
            position = span_tag.find('h1').text
            salary = span_tag.find('span', 'bloko-header-section-2 bloko-header-section-2_lite').text
            name_company = span_tag.find('span',class_='vacancy-company-name').text
            city = span_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]

            base_hh.append({
                "Должность": position,
                "Название компании": name_company.replace('\xa0',''),
                "Зарплата": salary.replace('\xa0',' '),
                "Город": city,
                "Ссылка": one_url
            })
    # pprint(base_hh)

    with open('base_hh.json','w', encoding='utf-8') as outfile:
        json.dump(base_hh, outfile, ensure_ascii=False, indent=5)

