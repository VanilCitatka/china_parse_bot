#!/usr/bin/python3.9
import re
from classes.table import Table
from classes.itemlist import ItemList
from classes.item_watches import ItemWatches

id = 'watches'

def clear_text(title: str):
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


def is_price(item):
    title = item['title'].strip()
    arr = title.split('\n')
    pricestr = arr[0]

    if pricestr.find('ð°') != -1:
        return True
    elif re.search(r'([pPðï¸]?\s?)?\d+[.,ãï¼\n]?', pricestr) is not None:
        if re.search(r'([pPðï¸]?\s?)?\d+[.,ãï¼\n]?', pricestr).span()[0] in [0, 1, 2]:
            return True
    else:    
        return False


def diff_price(title):
    res = 1000
    price_str = title.split('\n')[0]
    allprices = re.findall(r'[+â]?\s?\d+', price_str)
    
    if len(allprices) > 1:
        fprice = allprices[0]
        sprice = allprices[1]
        if len(re.findall(r'20[12][0-9]', sprice)) != 0:
            return 2000
        if len(fprice) != len(sprice):
            return 1001
        findex = title.find(fprice)
        if fprice == sprice or fprice.find(sprice) != -1:
            return 1002
        sindex = title.find(sprice)
        res = sindex-findex-len(fprice)

    return res


def get_items(data):
    items = []
    for item in data['result']['items']:
        title = item['title']
        price = is_price(item)
        diff = diff_price(title)
        if 'tags' in item:
            if item['mark_code'] != '':
                if len(item['imgsSrc']) > 2:
                    if len(re.findall(r'[^\s0-9cmkLZPG_.:~\+\-\*\/\[#!]+', clear_text(title))) != 0:
                        if price == True:
                            if diff > 7 and diff != 0:
                                items.append(item)
    return items


def get_final_items(itemlist):
    imgs = dict()
    newlist = []
    val = []
    for it in itemlist:
        item = ItemWatches(it, id)
        img = item.imgs
        price = item.price
        if img[0] not in imgs:
            val.append(price)
            imgs[f'{img[0]}'] = val.copy()
            newlist.append(it)
        elif price not in imgs[f'{img[0]}']:
            val.append(price)
            imgs[f'{img[0]}'] = val.copy()
            newlist.append(it)
        val.clear()
    return newlist


def get_description(text): 
        rustr = text.split('\n')
        findesc = []
        if len(rustr) > 1:
            findesc.append('<p>')
            for str in rustr:
                findesc.append('<span>')
                findesc.append(str)
                findesc.append('</span>')
            findesc.append('</p>')
        else:
            findesc.append('<p>')
            findesc.append('<span>')
            findesc.append(rustr[0])
            findesc.append('</span>')
            findesc.append('</p>')
        return ''.join(findesc)
    

def new_product(item: ItemWatches, translation: str, table: Table):

    dic = dict()

    for i in range(1, 12):
        if i < len(item.imgs)+1:
            dic[f'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² {i}'] = f'{item.imgs[i-1]}'
        else:
            dic[f'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² {i}'] = ''

    data = {
        'Ð¢Ð¸Ð¿ ÑÑÑÐ¾ÐºÐ¸': 'product',
        'ÐÐ°Ð¸Ð¼ÐµÐ½Ð¾Ð²Ð°Ð½Ð¸Ðµ': f'{item.name}',
        'ÐÐ°Ð¸Ð¼ÐµÐ½Ð¾Ð²Ð°Ð½Ð¸Ðµ Ð°ÑÑÐ¸ÐºÑÐ»Ð°': f'{item.item["mark_code"]}',
        'ÐÐ¾Ð´ Ð°ÑÑÐ¸ÐºÑÐ»Ð°': f'{item.article}',
        'ÐÐ°Ð»ÑÑÐ°': 'CNY',
        'ÐÐ¾ÑÑÑÐ¿ÐµÐ½ Ð´Ð»Ñ Ð·Ð°ÐºÐ°Ð·Ð°': '1',
        'ÐÐ¸Ð´Ð¸Ð¼Ð¾ÑÑÑ Ð½Ð° Ð²Ð¸ÑÑÐ¸Ð½Ðµ': '1',
        'ÐÐ°ÑÐµÑÐºÐ½ÑÑÐ°Ñ ÑÐµÐ½Ð°': '0',
        'ÐÐ°ÐºÑÐ¿Ð¾ÑÐ½Ð°Ñ ÑÐµÐ½Ð°': f'{item.price}',
        'ÐÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ': f'{get_description(translation)}',
        'Ð Ð½Ð°Ð»Ð¸ÑÐ¸Ð¸ @ÐÐ°Ð»Ð¸ÑÐ¸Ðµ Ð² ÐÐ¾ÑÐºÐ²Ðµ': '0',
        'Ð¡ÑÐ°ÑÑÑ': '1',
        'ÐÑÐ±Ð¾Ñ Ð²Ð°ÑÐ¸Ð°Ð½ÑÐ¾Ð² ÑÐ¾Ð²Ð°ÑÐ°': '2',
        'Ð¢Ð¸Ð¿ ÑÐ¾Ð²Ð°ÑÐ¾Ð²': 'Ð§Ð°ÑÑ',
        'Ð¡ÑÑÐ»ÐºÐ° Ð½Ð° Ð²Ð¸ÑÑÐ¸Ð½Ñ': f'{item.article}',
        'ÐÑÐµÐ½Ð´': f'{item.brand}',
        'ÐÐ¾Ð»': 'Ð£Ð½Ð¸ÑÐµÐºÑ',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 1': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 1")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 2': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 2")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 3': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 3")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 4': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 4")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 5': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 5")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 6': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 6")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 7': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 7")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 8': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 8")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 9': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 9")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 10': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 10")}',
        'ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ñ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 11': f'{dic.get("ÐÐ·Ð¾Ð±ÑÐ°Ð¶ÐµÐ½Ð¸Ðµ ÑÐ¾Ð²Ð°ÑÐ¾Ð² 11")}',
        'ÐÐ°ÑÐ°': f'{item.date}'
    }

    table.new_row(data)


def w_main(data, counter):

    table = Table((counter//100)+1, id)

    if counter == 1:
        table.create_table()
        table.new_category('Ð§Ð°ÑÑ', 'watches')

    i = counter

    if i // 100 > 0 and i == i//100 * 100:
        count = i // 100
        table.num = count + 1
        table.create_table()
        table.new_category('Ð§Ð°ÑÑ', 'watches')

    itemlist = get_items(data)
    if len(itemlist) != 0:
        final_itemlist = get_final_items(itemlist)
        items = ItemList(final_itemlist)
        for j in range(len(items.il)):
            it = ItemWatches(items.il[j], id)
            if it.name != '':
                if re.sub(r'\d', '', it.name) != '':
                    if re.sub(r'[ZPG]', '', it.name) != '':
                        if re.sub(r'[\sF0-9cCnN]', '', it.name) != '':
                            if re.sub(r'(\)/361)|(9100 CNC)|(\/\/\/316 P)', '', it.name) != '':
                                if re.sub(r'[\dm]+', '', it.name) != '':
                                    new_product(it, items.tr[j], table)
    # print(i)
    

def main():
    pass


if __name__ == '__main__':
    main()