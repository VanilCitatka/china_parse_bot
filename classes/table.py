#!/usr/bin/python3.9
import csv
import datetime

fn = [
        'Тип строки',
        'Наименование',
        'Наименование артикула',
        'Код артикула',
        'Валюта',
        'Цена',
        'Доступен для заказа',
        'Видимость на витрине',
        'Зачеркнутая цена',
        'Закупочная цена',
        'В наличии',
        'В наличии @Наличие в Москве',
        'В наличии @Склад в Китае',
        'Описание',
        'Статус',
        'Выбор вариантов товара',
        'Тип товаров',
        'Ссылка на витрину',
        'Артикул модели',
        'Бренд',
        'Размер EU',
        'Размер (одежда)',
        'Пол',
        'Изображения товаров 1',
        'Изображения товаров 2',
        'Изображения товаров 3',
        'Изображения товаров 4',
        'Изображения товаров 5',
        'Изображения товаров 6',
        'Изображения товаров 7',
        'Изображения товаров 8',
        'Изображения товаров 9',
        'Изображения товаров 10',
        'Изображения товаров 11',
        'Дата'
    ]

class Table:

    def __init__(self, count, path):
        self.num = count
        self.name = path
        self.date = datetime.date.today().strftime('%Y%m%d')
    

    def create_table(self):
        with open(f'tables/{self.name}_{self.date}-{self.num}.csv', 'w', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=fn, delimiter=';')
            writer.writeheader()


    def new_category(self, category, path):
        with open(f'tables/{self.name}_{self.date}-{self.num}.csv', 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fn, delimiter=';')
            writer.writerow(
                {
                    'Тип строки': 'category',
                    'Наименование': f'{category}',
                    'Статус': 1,
                    'Ссылка на витрину': f'{path}'
                }
            )


    def new_subcategory(self, subcat, path):
        with open(f'tables/{self.name}_{self.date}-{self.num}.csv', 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fn, delimiter=';')
            writer.writerow(
                {
                    'Тип строки': 'category',
                    'Наименование': f'!{subcat}',
                    'Статус': 1,
                    'Ссылка на витрину': f'{path}'
                }
            )

    
    def new_row(self, data: dict):
        with open(f'tables/{self.name}_{self.date}-{self.num}.csv', 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fn, delimiter=';')
            writer.writerow(data)

