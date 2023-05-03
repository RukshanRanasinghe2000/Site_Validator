import advertools as adv
import pandas as pd
import requests
import csv
import send_mail as mail
import pyautogui
import threading
import sys
from datetime import datetime


def sitemap_generator(url):
    global start_time
    try:
        start_time = datetime.now()
        sitemap_list = adv.sitemap_to_df(url)
        sitemap_list.to_csv('crawled_sitemap.csv', index=False)
        sitemap_list = pd.read_csv('crawled_sitemap.csv')
        sitemap_list.head(10)

    except Exception as e:
        print(f"ERROR : {e}")
        main_function()


def read_csv(file):
    path = file
    with open(path, 'r') as csv_file:
        read = csv.reader(csv_file, delimiter=',')
        data = list(read)
        return data


def read_site_csv():
    try:
        global row_count
        data = read_csv("crawled_sitemap.csv")
        row_count = len(data)
        print("Estimated URL count : " + str(row_count))
        site_array = []
        # [site_array.append(row[4]) for row in data]
        # [get_status_code(url) for url in site_array]
        for row in data:
            site_array.append(row[0])
        site_array.remove(site_array[0])
        for url in site_array:
            get_status_code(url)


    except Exception as e:
        print(f"ERROR : {e}")


def path_selector(row):
    if row[1] == "200":
        path1 = "sts_200_url.csv"
        # mail.send_smtp_msg(row[0],row[1])
        # print(pyautogui.alert("Attention..!!\nStatus Code : "+row[1]+"\nURL : "+row[0]))

        return path1
    else:
        path2 = "bad_urls.csv"
        mail.send_smtp_msg(row[0], row[1])
        print(pyautogui.alert("Attention..!!\nStatus Code : " + row[1] + "\nURL : " + row[0]))

        return path2


def write_csv(url, sts_code):
    try:
        row = [url, sts_code]

        path = path_selector(row)
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    except Exception as e:
        print(f"ERROR : {e}")


def get_status_code(url):
    response = requests.get(url)
    print("\t" + url + "\t" + str(response.content))
    write_csv(url, str(response.status_code))


def main_function():
    url = str(input("Enter URL : "))
    # email_receiver = str(input("Enter receiver email : "))
    if url != "":
        while (True):
            sitemap_generator(url)
            read_site_csv()


def site_report():
    sts_200 = len(read_csv("sts_200_url.csv"))
    bad_sts = len(read_csv("bad_urls.csv"))
    count = row_count - (sts_200 + bad_sts)
    total_time = datetime.now() - start_time

    print("...Process finished...\nNumber of scanned URLS : " + str(count) + "\nTotal time : " + str(total_time))


def program_controller():
    usr_input = str(input("Enter"))
    if usr_input == "0":
        site_report()
        sys.exit(0)


if __name__ == '__main__':
    # url = 'https://www.kooness.com/sitemap.xml'
    # url = 'https://www.kooness.com/shipping-boxes'
    "https://www.kooness.com/it/stitemap.xml"

    thread_1 = threading.Thread(target=main_function())
    thread_2 = threading.Thread(target=program_controller())

    thread_1.start()
    thread_2.start()
    #
    # thread_1.join()
    # thread_2.join()

    # main_function()
