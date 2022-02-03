import requests
from bs4 import BeautifulSoup
import pickle
import time
import telebot
import threading
from telebot import types


bot = telebot.TeleBot("2146149652:AAGBeImCPa7pUrksQjw21N6D3n9M_tkUe3U")
bot2 = telebot.TeleBot("2103027208:AAFedt2lIax0kZraXsqSgAe8VSW6VHLx8ZQ") #auktion 2


# 11111111111111111111111111111111111111111111111111111
with open('filters1.txt', encoding='utf-8') as file:
    filters1 = file.read().split("\n")
with open('filters2.txt', encoding='utf-8') as file:
    filters2 = file.read().split("\n")
with open('link.txt', encoding='utf-8') as file:
    links = file.read().split("\n")

def reset_memo():   #memo
    with open('cars.txt', 'wb') as f:
        pickle.dump([], f)
    print("memory")

def reset_users():
    with open('users.txt', 'wb') as f:
        pickle.dump([], f)
    print("users res")

#reset_memo()
#reset_users()

def check_car(link):
    with open('cars.txt', 'rb') as f:
        cars_mem = pickle.load(f)
    if link not in cars_mem:
        cars_mem.append(link)
        cars_mem = cars_mem[-100:]
        with open('cars.txt', 'wb') as f:
            pickle.dump(cars_mem, f)
        return True
    return False
# 111111111111111111111111111111111111111111111111



def main1():
    print("run main")
    while True:
        try:
            #filters1 parser
            for car_filter in filters1:
                print("oke")
                car_filter = car_filter.split(" ")
                use_link = links[0].replace("firm", car_filter[0]).replace("modl", car_filter[1]).replace("prce", car_filter[2]).replace("yfrom", car_filter[3]).replace("yto", car_filter[4]).replace("fel", car_filter[5]).replace("gearbx", car_filter[6])
                print(use_link)
                soup = BeautifulSoup(requests.get(use_link).text, 'lxml')
                all_cars = soup.find_all('ul', class_ = 'result-list uk-padding-remove')
                #print(all_cars)
                for car in all_cars:
                    car_link = car.find(class_='uk-width-medium-3-4').find('a').get('href')
                    print(car_link)
                    if check_car(car_link):
                        with open('users.txt', 'rb') as f:
                            users = pickle.load(f)
                        for user in users:
                            try:
                                print(f'Новая машина!\n{car_link}')
                            except Exception as ex:
                                try:
                                    bot.send_message(992579379, f"Local error: {ex}")
                                except:
                                    print(f"Local error: {ex}")
                    else:
                        break
                time.sleep(1)

            time.sleep(1)
                
            #filters2 parser
            for car_filter in filters2:
                car_filter = car_filter.split(" ")
                use_link = links[1].replace("firm", car_filter[0]).replace("modl", car_filter[1]).replace("prce", car_filter[2]).replace("yfrom", car_filter[3]).replace("yto", car_filter[4]).replace("fel", car_filter[5]).replace("gearbx", "")
                print(use_link)
                soup = BeautifulSoup(requests.get(use_link).text, 'lxml')
                all_cars = soup.find_all('ul', class_ = 'result-list uk-padding-remove')
                #print(all_cars)
                for car in all_cars:
                    car_link = "https://www.bytbil.com" + car.find(class_='uk-width-medium-3-4').find('a').get('href')
                    print("abbaba " + car_link)
                    if check_car(car_link):
                        with open('users.txt', 'rb') as f:
                            users = pickle.load(f)
                        for user in users:
                            try:
                                print(f'Новая машина!\n{car_link}')
                            except Exception as ex:
                                try:
                                    bot.send_message(992579379, f"Local error: {ex}")
                                except:
                                    print(f"Local error: {ex}")
                    else:
                        break
                time.sleep(1)
        except Exception as ex:
            try:
                #bot.send_message(992579379, f"Global error: {ex}")
                print(f"Global error: {ex}")
            except:
                print(f"Global error: {ex}")
            time.sleep(40)


auktion = threading.Thread(target=main1)
auktion.start()
#bot2.send_message(992579379, "2run2")
