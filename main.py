from lxml import html
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

 
ua = UserAgent()


class Parser():
    def __init__(self) -> None:
        self.cat_urls = []
        self.product_urls = []

    # ПОЛУЧЕНИЕ ССЫЛОК НА КАТЕГОРИИ    
    def cat_ursl_pars(self):
        url = 'https://maritim.fi/en/'
        req = requests.get(url, headers={'User-Agent': ua.random})
        tree = html.fromstring(req.content)
        for n in range(2, 24):  
            elements = tree.xpath(f'//*[@id="menu-product-menu"]/li[{n}]/a')
            self.cat_urls.append(elements[0].attrib['href'])
        print('Категории собраны')

    # ОПРЕДЕЛЕНИЕ КОЛ-ВА СТРАНИЦ
    def page_amount(self, url):
        req = requests.get(url=url, headers={'User-Agent': ua.random})
        soup = BeautifulSoup(req.text, 'lxml')    
        page_list = soup.find('ul', class_='pagination')
        pages = page_list.find_all('li') 
        return pages[-2].text   

    #ПОЛУЧЕНИЕ ССЫЛОК НА ТОВАРЫ ПОЛУЧЕННЫХ КАТ-ИЙ
    def product_urlsPars(self):
        for url in self.cat_urls:
            count_page = self.page_amount(url=url)
            for n in range(1, count_page+1):
                req = requests.get(url=f'{url}page/{n}/', headers={'User-Agent': ua.random})
                soup = BeautifulSoup(req.text, 'lxml')
                products = soup.find('div', 'isotope-wrapper grid-wrapper single-gutter')
                product = products.find_all('h3', class_='maritim-loop-title')
                [self.product_urls.append(i.find('a')['href']) for i in product]
    
    # ПАРСИНГ ТОВАРОВ ПО ССЫЛКАМ
    def parsProduct(self):
        for url in self.product_urls:
            req = requests.get(url=url, headers={'User-Agent': ua.random})
            soup = BeautifulSoup(req.text, 'lxml')
            name = soup.find('h1', 'h2 text-capitalize').text
            price = soup.find('span', 'woocommerce-Price-amount amount').text
            sku = soup.find('span', 'sku detail-value').text
            weight = soup.find('tr', 'maritim-meta _weight_text').find('td', 'maritim-meta-value').text #есть не у всех товаров, поэтому иногда выдает ошибку

            #далее осталось только скомпоновать все в ответ 
            #  