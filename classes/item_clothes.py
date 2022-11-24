#!/usr/bin/python3.9
import re
import json
from datetime import datetime



class ItemClothes:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = ''
        self.article = ''
        self.category = ''
        self.sub_category = ''
        self.brand = ''
        self.imgs = []
        self.date = ''
        self.item = {}


    def __init__(self, item: dict, id: str):
        self.item = item
        self.id = id
        self.name = self.__get_name()
        self.price = self.__get_price()
        self.article = self.__get_article()
        self.category = self.__get_category()
        self.sub_category = self.__get_subcategory()
        self.brand = self.__get_brand()
        self.imgs = self.__get_imgs().copy()
        self.date = self.__get_date()
        
    

    # Доработать
    def __get_name(self):
        name = ''
        name_str = self.get_description()
        if len(re.findall(r'\d+', name_str)) != 0:
            name = name_str.replace(re.findall(r'\d+', name_str)[0], '')
        return self.__clear_text(name).strip()


    # Доработать
    def __get_price(self):
        price = ''
        price_str = self.get_description()
        if 'priceArr' in self.item:
            price = str(self.item['priceArr'][0]['value'])[:-2]
        elif len(re.findall(r'[Pp💰]?\s?\d+', price_str)) != 0:
            price = re.findall(r'[Pp💰]?\s?\d+', price_str)[0]
        else:
            price = 'none000'
        return re.findall('\d+', price)[0]



    def __get_article(self):
        cat_codes = {
            'Одежда': 'c',
            'Аксессуары': 'a',
            'Часы': 'w'
        }
        code = self.item['mark_code']
        subcode = self.__get_subcode(self.__get_subcategory())
        category = self.__get_category()
        catcode = ''
        for cat in cat_codes:
            if cat == category:
                catcode = cat_codes[f'{cat}']
        article = f'1-{code}-{catcode}{subcode}'
        return article


    def __get_category(self):
        result = 'Nan'
        subcategory = self.__get_subcategory()
        with open('bc/cat_list.json', 'r', encoding='utf8') as file:
            cat_list = json.load(file)
        for category in cat_list:
            for subcat in cat_list[f'{category}']:
                if subcategory == subcat:
                    result = category
        return result


    def __get_subcategory(self):
        result = 'Другое'

        with open(f'bc/categories_{self.id}.json', 'r', encoding='utf8') as file:
            categories = json.load(file)
        if 'tags' in self.item:
            tags = self.item['tags']
            for tag in tags:
                for category in categories:
                    for it in categories[f"{category}"]:
                        if tag['tagName'] == it:
                            result = category
            
        else:
            result = 'Другое'
        return result


    def __get_brand(self):
        resarr = []
        strarr = []
        res = 'Nan'
        with open(f'bc/brands_{self.id}.json', 'r', encoding='utf8') as file:
            brands = json.load(file)

        if 'tags' in self.item:
            tags = self.item['tags']

            if len(tags) == 0:
                words = re.findall(r'[a-zA-Z]+', self.__clear_text(self.item['title']))
                for i in range(2):
                    resarr.append(words[i])
                print('не нашёл www.szwego.com' + self.item['link'])
                return ' '.join(resarr)

            
            for tag in tags:
                for brand in brands:
                    for it in brands[f'{brand}']:
                        if tag['tagName'] == it:
                            res = brand
                            return res

        words = re.findall(r'[a-zA-Z]+', self.__clear_text(self.item['title']))
        if len(words) < 2:
            for i in range(len(words)):
                strarr.append(words[i])
        else:
            for i in range(2):
                strarr.append(words[i])

        str = ' '.join(strarr)
        for brand in brands:
            if str.lower().find(brand.lower()) != -1:
                res = brand
                return res
        res = str
        return res


    def __get_imgs(self):
        srcimgs = self.item['imgsSrc']
        return srcimgs


    def __get_date(self):
        _time = self.item['time']

        if _time.find('Hour') != -1:
            date = datetime.today().strftime("%Y/%m/%d")
        elif len(_time.split('/')) == 3:
            date = _time
        else:
            date = f'2022/{_time}'

        return date

    
    def __clear_text(self, title: str):
        syms = []
        for sym in title:
            if sym.isascii() == True:
                syms.append(sym)
            else:
                syms.append(' ')
        cleartitle = ''.join(syms)
        words = re.findall(r'\S+', cleartitle)
        res = []
        for word in words:
            lenght = len(re.findall(r'\W+', word))
            if lenght == 0 or len(re.findall(r'\W+', word)[0]) != len(word):
                res.append(word)
        return ' '.join(res).strip()


    def __get_subcode(self, subcat: str):
        with open(f'bc/subcodes.json', 'r', encoding='utf8') as file:
            sub_codes = json.load(file)
        result = ''
        for _sub in sub_codes:
            if subcat == _sub:
                result = sub_codes[f'{_sub}']
        return result


    def get_description(self):
        title = self.item['title']
        if re.search(r'[iI][nN][fF][oO][rR][mM][aA][tT][iI][oO][nN]', title) is not None:
            desc = re.split(r'[iI][nN][fF][oO][rR][mM][aA][tT][iI][oO][nN]', title)[0]
        elif re.search('color', title.lower()) is not None:
            desc = re.split(r'[cC][oO][lL][oO][rR]', title)[0]
        elif re.search(r'[sS][iI][zZ][eE]', title) is not None:
            desc = re.split(r'[sS][iI][zZ][eE]', title)[0]
        elif re.search('尺码', title) is not None:
            desc = re.split('尺码', title)[0]
        else:
            desc = title
        return desc


    def is_valid(self):
        pass