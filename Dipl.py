import requests
from lxml import html
import json
from pymongo import MongoClient


# Функция для скрейпинга табличных данных
def scrape_page_data(url, user_agent):
    response = requests.get(url, headers = {"User-Agent": user_agent})
    tree = html.fromstring(response.content)
    table_rows = tree.xpath('//table/tbody/tr')
    data = []
    for row in table_rows:
        name = ''.join(row.xpath(".//td/a/text()"))
        columns = row.xpath(".//td/text()")
        data.append({
            "country": name,
            "population": int(columns[1].replace(",","")),
            "net_change": int(columns[3].replace(",","")),
            "land_area_sq_km": int(columns[5].replace(",","")),
            "dencity": int(columns[4].strip().replace(",","")),
            "med_age": columns[8].strip().replace(",",""),
        })
    return data


# функция сохранения данных в json файл
def save_to_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


# функция сохранения данных из json файла в базу данных MongoDB
def upload_to_db (my_file):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['diploma'] # выбор базы данных
    collection = db['external_data']
    with open(my_file) as f:
        db_data = json.load(f)
    collection.insert_many(db_data)



def main():
    base_url = "https://www.worldometers.info/population/countries-in-europe-by-population/"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    data = scrape_page_data(base_url, user_agent)  #извлекаем данные из страницы 
    save_to_json(data)
    upload_to_db('data.json')
    print("Data loaded")




if __name__ == "__main__":
    main()
