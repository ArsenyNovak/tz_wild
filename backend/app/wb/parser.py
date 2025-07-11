import requests

from .models import Product

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    'Accept': '*/*',
  }

def download_catalogue():
  url = 'https://static-basket-01.wbbasket.ru/vol0/data/main-menu-by-ru-v3.json'
  response = requests.get(url, headers=HEADERS)
  return response.json()


def flatten_catalogue(catalogue, flat_list):
  for category in catalogue:
    try:
      flat_list.append({
        'name': category['name'],
        'url': category['url'],
        'shard': category['shard'],
        'query': category['query']
      })
    except KeyError:
      pass
    if 'childs' in category:
      flatten_catalogue(category['childs'], flat_list)


def extract_category(flat_catalogue, user_input):
    for cat in flat_catalogue:
        if user_input == cat['name']:
            return cat['name'], cat['shard'], cat['query']
    return None


def add_data_from_page(url, session):
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()

        # Process successful response
        data = response.json()
        for item in data['products']:
            product = Product(name=item['name'],
                              price=str(item['sizes'][0]['price']['basic'] / 100),
                              price_sale=str((item['sizes'][0]['price']['product'] +
                                              item['sizes'][0]['price']['logistics']) / 100),
                              rating=item['reviewRating'],
                              count_comment=item['feedbacks']
                              )
            product.save()
        if data['products']:
            print(f"Добавлено товаров: {len(data['products'])}")
        else:
            print('Загрузка товаров завершена')
            return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {str(e)}")



def get_all_products_in_category(category_data):
    session = requests.Session()
    for page in range(1, 100):
        print(f"Загружаю товары со страницы {page}")
        url = (f"https://catalog.wb.ru/catalog/{category_data[1]}/v4/catalog?ab_testing=false&appType=1"
               f"&{category_data[2]}&curr=byn&dest=-59202&lang=ru&page={page}&sort=popular&spp=30")
        if add_data_from_page(url, session):
            break


def get_all_products_in_search(user_input):
    session = requests.Session()
    for page in range(1, 61):
        print(f"Загружаю товары со страницы {page}")
        url = (f"https://search.wb.ru/exactmatch/sng/common/v14/search?ab_testing=false&appType=1&curr=byn&dest=-59202"
               f"&lang=ru&page={page}&query={'%20'.join(user_input.split())}&resultset=catalog"
               f"&sort=popular&spp=30&suppressSpellcheck=false")
        if add_data_from_page(url, session):
            break

def start():
    Product.objects.all().delete()
    search = input("Введите 1 - для поиска по категории и  2 - для поиска по запросу:")
    if search == '1':
      catalogue = download_catalogue()
      flat_catalogue = []
      flatten_catalogue(catalogue, flat_catalogue)
      user_input = input("Введите название категории: ").capitalize()
      category_data = extract_category(flat_catalogue, user_input)
      if not category_data:
        print("Категория не найдена")
        return
      print(f"Найдена категория: {category_data[0]}")
      get_all_products_in_category(category_data)
    elif search == '2':
        user_input = input("Введите запрос: ")
        get_all_products_in_search(user_input)
    else:
        print('введено не корректное значение')



