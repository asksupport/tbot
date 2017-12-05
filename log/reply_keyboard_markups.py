import telebot
import random
from sql import SQL
from telebot.types import KeyboardButton as btn
from telebot.types import InlineKeyboardButton as createBtn
from vk import Session, API
import lang

users_db = SQL('users.db')

f = open('text.txt', 'r+')
categories = []
for line in f.readlines():
    temp = line.split('|')[0]
    if temp not in categories:
        categories.append(temp)
f.close()

class Keyboard:
    def __init__(self, bot):
        self.bot = bot


    def cancel_acception(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(createBtn(text=lang.us.order_return, callback_data='order_backto'),createBtn(text=lang.us.order_confirm, callback_data='order_cancel'))
        return keyboard

    def create_payment_inline(self, TLID):
        keyboard = telebot.types.InlineKeyboardMarkup()
        price_btc = users_db.GetUser(TLID)[6].split('_')[3]
        keyboard.row(createBtn(text=lang.us.bitcoin_as_message, callback_data='order_wallet'),createBtn(text=lang.us.price_as_message, callback_data='order_price_'+str(price_btc)))
        keyboard.row(createBtn(text=lang.us.cancel_order, callback_data='cancel_acception'))
        return keyboard

    def category_menu_inline(self):
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn = []

        f = open('text.txt', 'r+')
        categories = []
        for line in f.readlines():
            if line[0] != ' ':
                temp = line.split('|')
                if temp[0] not in categories:
                    categories.append(temp[0])
            else:
                pass
        categories = categories[:-1]
        f.close()

        for i in categories:
            btn.append(createBtn(text=i,callback_data='productlist_'+str(i)))
        if len(btn) % 2 == 0:
            for i in range(0,len(btn),2):
                keyboard.row(btn[i],btn[i+1])
        else:
            for i in range(0,len(btn)-1,2):
                keyboard.row(btn[i],btn[i+1])
            keyboard.row(btn[len(btn)-1])

        return keyboard

    def products_menu_inline(self,ProductCategory):
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn = []

        f = open('text.txt', 'r+')
        products = []
        for line in f.readlines():
            try:
                line = line.split('|')
                if line[1] not in products and line[0] ==ProductCategory:
                    products.append(line[1])
            except:
                pass
        f.close()

        for i in products:
            btn.append(createBtn(text=str(i),callback_data='productcount_'+ProductCategory+'_'+str(i)))


        if len(btn) % 2 == 0:
            for i in range(0,len(btn),2):
                keyboard.row(btn[i],btn[i+1])
        else:
            for i in range(0,len(btn)-1,2):
                keyboard.row(btn[i],btn[i+1])
            keyboard.row(btn[len(btn)-1])
        keyboard.row(createBtn(text=lang.us.escape_btn,callback_data='categorylist'))
        return keyboard


    def products_count_inline(self,data):
        keyboard = telebot.types.InlineKeyboardMarkup()
        btn = []
        data = data.split('_')
        ProductCategory = data[0]
        ProductName = data[1]

        f = open('text.txt', 'r+')
        counts = []
        for line in f.readlines():
            temp = line.split('|')
            if ProductCategory == temp[0] and ProductName == temp[1]:
                keyboard.row(createBtn(text=temp[2],callback_data='newpayment_'+temp[0]+'_'+temp[1]+'_'+temp[2]+'_'+str(float(temp[3])/lang.course)))
        f.close()
        keyboard.row(createBtn(text=lang.us.escape_btn,callback_data='productlist_'+ProductCategory))
        return keyboard


    def main_menu(self):
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row(lang.us.assortment_btn)
        keyboard.row(lang.us.order_status_btn, lang.us.bitcoin_wallet_btn)
        keyboard.row(lang.us.support_message_btn)
        return keyboard
