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
        cars_mem = cars_mem[-15:]
        with open('cars.txt', 'wb') as f:
            pickle.dump(cars_mem, f)
        return True
    return False
# 111111111111111111111111111111111111111111111111



# 222222222222222222222222222222222222222222222
with open('users.pickle', 'rb') as f:
    users = pickle.load(f)
    print(users)

def get_name(car):
    return car.find(class_='card__title').text

def get_price(car):
    return car.find(class_='caption__top currentBid').find('strong').text

def get_link(car):
    return "https://auktion.biliaoutlet.se" + car.find('a', class_='card__inner').get('href')

def reset_mem():
    with open('cars.dat', 'wb') as f:
        pickle.dump([], f)

def check_car2(link):
    with open('cars.dat', 'rb') as f:
        cars_mem = pickle.load(f)
    if link not in cars_mem:
        cars_mem.append(link)
        if len(cars_mem) > 30:
            cars_mem = cars_mem[-20:]
        with open('cars.dat', 'wb') as f:
            pickle.dump(cars_mem, f)
        return True
    return False
#22222222222222222222222222222222222222222222222



def main1():
    print("run main")
    while True:
        try:
            #filters1 parser
            for car_filter in filters1:
                car_filter = car_filter.split(" ")
                use_link = links[0].replace("firm", car_filter[0]).replace("modl", car_filter[1]).replace("prce", car_filter[2]).replace("yfrom", car_filter[3]).replace("yto", car_filter[4]).replace("fel", car_filter[5]).replace("gearbx", car_filter[6])
                #print(use_link)
                soup = BeautifulSoup(requests.get(use_link).text, 'lxml')
                all_cars = soup.find_all('ul', class_ = 'result-list uk-padding-remove')
                #print(all_cars)
                for car in all_cars:
                    car_link = car.find(class_='uk-width-medium-3-4').find('a').get('href')
                    if check_car(car_link):
                        with open('users.txt', 'rb') as f:
                            users = pickle.load(f)
                        for user in users:
                            try:
                                bot.send_message(user, f'Новая машина!\n{car_link}')
                                #print(f'Новая машина!\n{car_link}')
                            except Exception as ex:
                                try:
                                    bot.send_message(992579379, f"Local error: {ex}")
                                except:
                                    print(f"Local error: {ex}")
                    else:
                        break
                time.sleep(1.5)

            time.sleep(3)
                
            #filters2 parser
            for car_filter in filters2:
                car_filter = car_filter.split(" ")
                use_link = links[1].replace("firm", car_filter[0]).replace("modl", car_filter[1]).replace("prce", car_filter[2]).replace("yfrom", car_filter[3]).replace("yto", car_filter[4]).replace("fel", car_filter[5]).replace("gearbx", "")
                #print(use_link)
                soup = BeautifulSoup(requests.get(use_link).text, 'lxml')
                all_cars = soup.find_all('ul', class_ = 'result-list uk-padding-remove')
                #print(all_cars)
                for car in all_cars:
                    car_link = "https://www.bytbil.com" + car.find(class_='uk-width-medium-3-4').find('a').get('href')
                    if check_car(car_link):
                        with open('users.txt', 'rb') as f:
                            users = pickle.load(f)
                        for user in users:
                            try:
                                #print(f'Новая машина!\n{car_link}')
                                bot.send_message(user, f'Новая машина!\n{car_link}')
                            except Exception as ex:
                                try:
                                    bot.send_message(992579379, f"Local error: {ex}")
                                except:
                                    print(f"Local error: {ex}")
                    else:
                        break
                time.sleep(1.5)
        except Exception as ex:
            try:
                bot.send_message(992579379, f"Global error: {ex}")
            except:
                print(f"Global error: {ex}")
            time.sleep(40)

def main2():
    while True:
        try:
            r = requests.get('https://auktion.biliaoutlet.se/Home/Search?Search=&submit-button=Sök')
            soup = BeautifulSoup(r.text, 'lxml')
            cars = soup.find_all(class_='card') + BeautifulSoup(requests.get('https://auktion.biliaoutlet.se').text, 'lxml').find_all(class_='card')
            for car in cars[:5]:
                if check_car(get_link(car)):
                    with open('users.pickle', 'rb') as f:
                        users = pickle.load(f)
                    for user in users:
                        try:
                            bot2.send_message(user, f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}") #user
                            #print(f"Название: {get_name(car)}\nЦена: {get_price(car)}\nСсылка: {get_link(car)}")
                        except Exception as ex:
                            pass
        except Exception as ex:
            print("auktion error: " + str(ex))
            time.sleep(4)
        time.sleep(3)

            
bitbil = threading.Thread(target=main1)
bitbil.start()
bot.send_message(992579379, "1run1")

auktion = threading.Thread(target=main2)
auktion.start()
bot2.send_message(992579379, "2run2")


# 8888888888888888888888888888888888888888888888888111111111111111111111111111111111111111111118888888888888888888888888888888888888888888888888888888888
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.split(" ")[0] == "yes":
        with open('users.txt', 'rb') as f:
            users = pickle.load(f)
            
        users.append( int(call.data.split(" ")[1]) )
        
        with open('users.txt', 'wb') as f:
                pickle.dump(users, f)

        bot.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос подтвердили. Теперь бот будет присылать вам ссылки.")
        
    elif call.data.split(" ")[0] == "no":
        bot.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос отклонили.")
        bot.send_message(call.from_user.id, "Запрос отклонен.")

    else:
        with open('users.txt', 'rb') as f:
            users = pickle.load(f)
            
        users.remove( int(call.data.split(" ")[1]) )
                     
        with open('users.txt', 'wb') as f:
                pickle.dump(users, f)

        bot.send_message(call.from_user.id, "Юзер отключен.")  

@bot.message_handler(commands=['removeuser'])
def remove_user(message):
    if message.from_user.id == 992579379 or message.from_user.id == 1639768908:
        with open('users.txt', 'rb') as f:
            users = pickle.load(f)
            
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        for user in users:
            markup.add(types.InlineKeyboardButton(user, callback_data=f'remove {user}'))
        
        bot.send_message(message.from_user.id, text=f'Укажите айди:', reply_markup=markup)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.from_user.id != 992579379 and message.from_user.id != 1639768908:
        with open('users.txt', 'rb') as f:
            users = pickle.load(f)

        if message.from_user.id not in users:
            bot.send_message(message.from_user.id, "Запрос на регистрацию отправлен админу. Ждите подтверждения")

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("подтвердить", callback_data=f'yes {message.from_user.id}')
            item2 = types.InlineKeyboardButton("отклонить", callback_data=f'no {message.from_user.id}')
            markup.add(item1, item2)
            
            bot.send_message(992579379, text=f'Запрос от {message.from_user.first_name}. Айди: {message.from_user.id}', reply_markup=markup)
            
        else:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы в боте, можете им пользоваться.")
    else:
        with open('users.txt', 'rb') as f:
            users = pickle.load(f)
        if message.text not in users:
            users.append(int(message.text))
            with open('users.txt', 'wb') as f:
                pickle.dump(users, f)
            bot.send_message(message.from_user.id, "Пользователь успешно добавлен.")
        else:
            bot.send_message(message.from_user.id, "Пользователь уже в базе.")
#888888888888888888888888888888888888888811111111111111111111111111111111111111111111111111111111111188888888888888888888888888888888888888888



#888888888888888888888888888888888888888222222222222222222222222222222222222222222222222222222222222222888888888888888888888888888888888888888888888888
@bot2.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.split(" ")[0] == "yes":
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        users.append( int(call.data.split(" ")[1]) )
        
        with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)

        bot2.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос подтвердили. Теперь бот будет присылать вам ссылки.")
        
    elif call.data.split(" ")[0] == "no":
        bot2.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Ваш запрос отклонили.")
        bot2.send_message(call.from_user.id, "Запрос отклонен.")

    else:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        users.remove( int(call.data.split(" ")[1]) )
                     
        with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)

        bot2.send_message(int(call.data.split(" ")[1]), "Здравствуйте. Вы были отключены от бота.")
        bot2.send_message(call.from_user.id, "Юзер отключен.")  

@bot2.message_handler(commands=['removeuser'])
def remove_user(message):
    if message.from_user.id == 992579379 or message.from_user.id == 1639768908:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
            
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        for user in users:
            markup.add(types.InlineKeyboardButton(user, callback_data=f'remove {user}'))
        
        bot2.send_message(message.from_user.id, text=f'Укажите айди:', reply_markup=markup)

@bot2.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.from_user.id != 992579379 and message.from_user.id != 1639768908:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)

        if message.from_user.id not in users:
            bot2.send_message(message.from_user.id, "Запрос на регистрацию отправлен админу. Ждите подтверждения")

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("подтвердить", callback_data=f'yes {message.from_user.id}')
            item2 = types.InlineKeyboardButton("отклонить", callback_data=f'no {message.from_user.id}')
            markup.add(item1, item2)
            
            bot2.send_message(992579379, text=f'Запрос от {message.from_user.first_name}. Айди: {message.from_user.id}', reply_markup=markup)
            
        else:
            bot2.send_message(message.from_user.id, "Вы уже зарегистрированы в боте, можете им пользоваться.")
    else:
        with open('users.pickle', 'rb') as f:
            users = pickle.load(f)
        if message.text not in users:
            users.append(int(message.text))
            with open('users.pickle', 'wb') as f:
                pickle.dump(users, f)
            bot2.send_message(message.from_user.id, "Пользователь успешно добавлен.")
        else:
            bot2.send_message(message.from_user.id, "Пользователь уже в базе.")
#888888888888888888888888888888888888888222222222222222222222222222222222222222222222222222222222222222888888888888888888888888888888888888888888888888

def start_bitbil():
    while True:
        try:
            bot.infinity_polling()
        except:
            time.sleep(60)
            
def start_auktion():
    while True:
        try:
            bot2.infinity_polling()
        except:
            time.sleep(60)

time.sleep(4)

bitbil = threading.Thread(target=start_bitbil)
bitbil.start()

start_auktion()
