import telebot
from database import dbapi
from database.dbapi import *

db_conn = DatabaseConnector("postgresql+psycopg2://postgres:postgres@localhost:5432/bot_base")
token = "6255448961:AAFK1ZfeZ9f-iwMMczddKnMsXYg-elxtSeM"  # заполните значением вашего токена, полученного от BotFather
bot = telebot.TeleBot(token)
dic1 = {}
dic2 = {}
dic3 = {}
dic4 = {}
dic5 = {}
 
@bot.message_handler(commands=['add'])  # указали команду, при которой запускается функция
def add_book(message):
    send = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(send, name)
 
def name(message):
    dic1["title"] = message.text.lower()
    send = bot.reply_to(message, "Введите автора:")
    bot.register_next_step_handler(send, year)
 
def year(message):
    dic1["author"] = message.text.lower()
    send = bot.reply_to(message, "Введите год издания:")
    bot.register_next_step_handler(send, fin)
 
def fin(message):
    dic1["published"] = message.text
    bot.reply_to(message, "Книга была успешно добавлена")
    db_conn.get_add(dic1)
 
 
@bot.message_handler(commands=['delete']) 
def delete_book(message):
    send = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(send, name_del)
 
def name_del(message):
    dic2["title"] = message.text.lower()
    send = bot.reply_to(message, "Введите автора:")
    bot.register_next_step_handler(send, year_del)
 
def year_del(message):
    dic2["author"] = message.text.lower()
    send = bot.reply_to(message, "Введите год издания:")
    bot.register_next_step_handler(send, confirm_del)
 
def confirm_del(message):
    dic2["published"] = message.text
    mas = []
    if db_conn.get_book(dic2):
        for v in dic2.values():
            mas.append(v)
        mas = " ".join(mas)
        send = bot.reply_to(message, f"Найдена книга: {mas}. Удаляем?")
        bot.register_next_step_handler(send, fin_del)
    else:
        send = bot.reply_to(message, f"Книга не найдена")
 
def fin_del(message):
    if message.text.lower() == "да":
        res = db_conn.get_delete(db_conn.get_book(dic2))
        if res:
            bot.reply_to(message, f"Книга удалена")
        else:
            bot.reply_to(message, f"Невозможно удалить книгу")
 
 
@bot.message_handler(commands=['list'])  # указали команду, при которой запускается функция
def list_books(message):
    check = db_conn.list_book()
    if len(check) < 1:
        bot.reply(message, "Список пустой")
    else:
        bot.reply_to(message, "\n".join(check))
 
 
@bot.message_handler(commands=['find'])  # указали команду, при которой запускается функция
def find_book(message):
    send = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(send, name_find)
 
def name_find(message):
    dic3["title"] = message.text.lower()
    send = bot.reply_to(message, "Введите автора:")
    bot.register_next_step_handler(send, year_find)
 
def year_find(message):
    dic3["author"] = message.text.lower()
    send = bot.reply_to(message, "Введите год издания:")
    bot.register_next_step_handler(send, fin_find)
 
def fin_find(message):
    dic3["published"] = message.text
    solved = db_conn.get_book(dic3)
    bot.reply_to(message, f"Book_id : {solved}")
 
 
 
@bot.message_handler(commands=['borrow']) 
def borrow_book(message):
    send = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(send, name_bor)
 
def name_bor(message):
    dic4["title"] = message.text.lower()
    send = bot.reply_to(message, "Введите автора:")
    bot.register_next_step_handler(send, year_bor)
 
def year_bor(message):
    dic4["author"] = message.text.lower()
    send = bot.reply_to(message, "Введите год издания:")
    bot.register_next_step_handler(send, confirm_bor)
 
def confirm_bor(message):
    dic4["published"] = message.text
    mas = []
    if db_conn.get_book(dic4):
        for v in dic4.values():
            mas.append(v)
        mas = " ".join(mas)
        send = bot.reply_to(message, f"Найдена книга: {mas}. Берем?")
        bot.register_next_step_handler(send, fin_bor)
    else:
        send = bot.reply_to(message, f"Книга не найдена")
 
def fin_bor(message):
    id = message.from_user.id
    if message.text.lower() == "да":
        res = db_conn.borrow(id, db_conn.get_book(dic4))
        if res:
            bot.reply_to(message, f"Вы взяли книгу")
        else:
            bot.reply_to(message, f"Книгу сейчас нельзя взять")
 
 
@bot.message_handler(commands=['retrieve']) 
def borrow_book(message):
    users_id = message.from_user.id
    ans = db_conn.retrieve(users_id)
    if len(ans) < 1:
        bot.reply_to(message, "У вас нет взятых книг")
    else:
        ans = " ".join(ans)
        bot.reply_to(message, f"Вы вернули книгу {ans}")
 

@bot.message_handler(commands=['stats'])
def stat_book(message):
    send = bot.reply_to(message, "Введите название книги:")
    bot.register_next_step_handler(send, stat_name)
 
def stat_name(message):
    dic5["title"] = message.text.lower()
    send = bot.reply_to(message, "Введите автора:")
    bot.register_next_step_handler(send, stat_year)
 
def stat_year(message):
    dic5["author"] = message.text.lower()
    send = bot.reply_to(message, "Введите год издания:")
    bot.register_next_step_handler(send, get_res_stat)
 
def get_res_stat(message):
    dic5["published"] = message.text
    book_id = db_conn.get_book(dic5)
    if book_id:
        download_url = f'http://localhost:8080/download/{book_id}'
        bot.reply_to(message, f"Статистика доступна по следующей ссылке: {download_url}")
    else:
        bot.reply_to(message, "Книга не найдена")


bot.infinity_polling()
