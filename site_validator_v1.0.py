import advertools as adv
import pandas as pd
import requests
import csv
from mailer import Mailer


def sitemap_generator(url):
    sitemap_list = adv.sitemap_to_df(url)
    sitemap_list.to_csv('crawled_sitemap.csv', index=False)
    sitemap_list = pd.read_csv('crawled_sitemap.csv')
    sitemap_list.head(10)


def read_csv():
    path = "crawled_sitemap.csv"
    with open(path, 'r') as csv_file:
        read = csv.reader(csv_file, delimiter=',')
        data = list(read)
        row_count = len(data)
        print("Estimated URL count : " + str(row_count))
        site_array = []
        for row in data:
            site_array.append(row[4])
        site_array.remove(site_array[0])
        for url in site_array:
            get_status_code(url)


def path_selector(row):
    if row[1] == "200":
        path1 = "sts_200_url.csv"
        return path1
    else:
        path2 = "bad_urls.csv"
        return path2


def write_csv(url, sts_code):
    row = [url, sts_code]

    path = path_selector(row)
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)


def get_status_code(url):
    response = requests.get(url)
    print("\t" + url + "\t" + str(response.status_code))
    write_csv(url, str(response.status_code))




if __name__ == '__main__':
    url = 'https://www.kooness.com/sitemap.xml'
    sitemap_generator(url)
    read_csv()
