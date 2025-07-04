import requests
from bs4 import BeautifulSoup
import datetime
import csv
import time
import json

start_time = time.time()

cookies = {
    "_gid": "GA1.2.91982725.1751608416",
    "_ym_uid": "1751608416822113380",
    "_ym_d": "1751608416",
    "_ym_isad": "2",
    "_gat": "1",
    "_ym_visorc": "w",
    "cart_id": "01jz9zyr0jczbep3e2rt4wa1cp",
    "ss_utm_data": "%7B%22uid%22%3A%2275bb6a9c-9f6e-46bd-8eca-0eb4fa50e243%22%2C%22type%22%3A%22other%22%2C%22channel%22%3Anull%2C%22datetime%22%3A%222025-07-04T08%3A53%3A38%2B03%3A00%22%2C%22utmData%22%3A%5B%5D%2C%22domainReferral%22%3A%22www.google.com%22%2C%22pageReferral%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com%5C%2F%22%2C%22visitorDevice%22%3A%22desktop%22%7D",
    "_ga_1PJHLKC6BD": "GS2.1.s1751608417$o1$g0$t1751608417$j60$l0$h0",
    "_ga": "GA1.2.328636303.1751608416",
    "_gat_gtag_UA_3006239_4": "1",
    "_cmg_csstqSDyT": "1751608418",
    "_comagic_idqSDyT": "10745822691.15034818761.1751608419",
}

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.google.com/",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    # 'cookie': '_gid=GA1.2.91982725.1751608416; _ym_uid=1751608416822113380; _ym_d=1751608416; _ym_isad=2; _gat=1; _ym_visorc=w; cart_id=01jz9zyr0jczbep3e2rt4wa1cp; ss_utm_data=%7B%22uid%22%3A%2275bb6a9c-9f6e-46bd-8eca-0eb4fa50e243%22%2C%22type%22%3A%22other%22%2C%22channel%22%3Anull%2C%22datetime%22%3A%222025-07-04T08%3A53%3A38%2B03%3A00%22%2C%22utmData%22%3A%5B%5D%2C%22domainReferral%22%3A%22www.google.com%22%2C%22pageReferral%22%3A%22https%3A%5C%2F%5C%2Fwww.google.com%5C%2F%22%2C%22visitorDevice%22%3A%22desktop%22%7D; _ga_1PJHLKC6BD=GS2.1.s1751608417$o1$g0$t1751608417$j60$l0$h0; _ga=GA1.2.328636303.1751608416; _gat_gtag_UA_3006239_4=1; _cmg_csstqSDyT=1751608418; _comagic_idqSDyT=10745822691.15034818761.1751608419',
}


def get_data():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    with open(f"omskshinservice_{cur_time}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(("Модель", "Ссылка", "Цена", "Харак-ки", "Оценки"))

    url = "https://omsk.shinservice.ru/catalog/tyres/"
    data = []

    r = requests.get(url=url, cookies=cookies, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

    pages_count = int(
        soup.find(attrs={"data-testid": "pagination"}).find_all("a")[-1].text
    )

    #for page in range(1, pages_count + 1):
    for page in range(1, 20+1):
        url = f"https://omsk.shinservice.ru/catalog/tyres/?page={page}"
        r = requests.get(url=url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        cards = soup.find_all(attrs={"data-js": "card"})
        for card in cards:
            tyre_url = "https://omsk.shinservice.ru/" + card.find(
                attrs={"data-testid": "catalog-item.title"}
            ).get("href")
            tyre_title = card.find(attrs={"data-testid": "tyre.title"}).getText()
            tyre_price = card.find(attrs={"data-testid": "card.price"}).getText()
            tyre_value = card.select_one("[class='goods-attribute-value']").getText()
            try:
                tyre_rate = card.select_one(
                    "[class='d_flex items_center gap_5px font_600']"
                ).getText()
            except:
                tyre_rate = "Нет оценок"
            try:
                tyre_rateQ = card.select_one(
                    "[class='text_grey.400 catalog-card-review-link']"
                ).getText()
            except:
                tyre_rateQ = "Нет отзывов"

            tyre_rating = f"{tyre_rate} {tyre_rateQ}"

            data.append(
                {
                    "Модель": tyre_title,
                    "Ссылка": tyre_url,
                    "Цена": tyre_price,
                    "Харак-ки": tyre_value,
                    "Рейтинг": tyre_rating,
                }
            )
            with open(f"omskshinservice_{cur_time}.csv", "a", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(
                    (tyre_title, tyre_url, tyre_price, tyre_value, tyre_rating)
                )
        print(f"Обработано: {page}/{pages_count}")
        time.sleep(1)
    with open(f"omskshinservice_{cur_time}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Время исполнения скрипта: {finish_time}")


if __name__ == "__main__":
    main()
