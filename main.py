import telebot, requests, urllib
import lang,time,threading
import time
import json
from sql import SQL
from reply_keyboard_markups import Keyboard
superusers = [246007355, 279528391, 241241093, 402996311]
btc_adress = '1D46K1BTMajR1r6thDwYqXdhuq7s15sBiE'
token = '491826003:AAGCjLxDB81rm21a7EWDj86noNFG5fvwpIU'
tg = telebot.TeleBot(token)

users_db = SQL('users.db')
keyboard = Keyboard(tg)

def BalanceUpdater():
    while True:
        users_db = SQL('users.db')
        paylist = users_db.SelectAllUsers()
        for i in paylist:
            users_db.UpdateBalance(i[0],i[2])
            if users_db.GetUser(i[0])[4] > i[4]:
                tg.send_message(chat_id=i[0], text='Payment recived.')
                users_db.EditPayStatus(i[0],2)
        print('BALANCECHECK')
        time.sleep(15)

def PayChecker():
    while True:
        users_db = SQL('users.db')
        paylist = users_db.SelectPayUsers()
        for i in paylist:
            cht_id = i[0]
            if (float(i[3])*10**-8) >= (float(i[6].split('_')[3])):
                try:
                    paidout_value = str(round(float(i[6].split('_')[3])*10**8)-10)
                    print(paidout_value)
                    url = 'https://bitaps.com/api/use/redeemcode'
                    parameters = {'redeemcode': str(i[2]),
                    'address': btc_adress,
                    'amount': 'All available',
                    'custom_fee': '50'}
                    response = requests.post(url, data=json.dumps(parameters))
                    print(response.text)

                    tg.send_message(chat_id=i[0], text='Payment received. Your adress: ')
                    temp = i[6].split('_')
                    f = open('text.txt', 'r+')
                    sold = open('sold.txt', 'a')
                    count = len(f.readlines())
                    f.seek(0)
                    for j in range(count):
                        line = f.readline()
                        if line.split('|')[:3] == temp[:3]:
                            f.seek(int(f.tell())-len(line)-1)
                            f.write(' '*(len(line)-1))
                            f.write('\n')
                            sold.write(line[:-1]+'* -'+time.ctime()+'\n')
                            sold.close()
                            tg.send_message(chat_id=cht_id, text=str(line))
                            f.close()
                            users_db.EditPayStatus(cht_id, 5)
                            break
                except Exception as e:
                    tg.send_message(chat_id=i[0], text = e)

        print('PAYCHECK')
        time.sleep(10)

t1 = threading.Thread(target=BalanceUpdater, args=()).start()
t2 = threading.Thread(target=PayChecker, args=()).start()


@tg.message_handler(content_types=['audio', 'document', 'photo', 'sticker','voice'])
def Ignore(message):
    print(message.from_user.id)
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text='<b>Ты е</b>блан)')

@tg.message_handler(commands=['start'])
def Start(message):
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text=lang.us.start_message, reply_markup=keyboard.main_menu())
    try:
        print(message.chat.id)
        users_db.GetUser(message.from_user.id)
    except Exception:
        users_db.AddUser(message.from_user.id)

@tg.message_handler(func=lambda message: '🍃' == message.text[:1], content_types=['text'])
def Stock(message):
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text=lang.us.category_message,reply_markup=keyboard.category_menu_inline())

@tg.message_handler(func=lambda message: '💳' == message.text[:1], content_types=['text'])
def BtcBalance(message):
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text=lang.us.bitcoin_wallet(message.from_user.id))

@tg.message_handler(func=lambda message: '💬' == message.text[:1], content_types=['text'])
def BtcBalance(message):
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text=lang.us.support_message)

@tg.message_handler(func=lambda message: '⏳' == message.text[:1], content_types=['text'])
def BtcBalance(message):
    tg.send_message(chat_id=message.chat.id, parse_mode='HTML',text=lang.us.status(message.chat.id))

@tg.callback_query_handler(func=lambda call: True and call.data == 'order_backto')
def CallbackOrderBack(call):
    tg.edit_message_text(chat_id=call.message.chat.id, parse_mode='HTML', message_id=call.message.message_id, text=lang.us.create_payment(str(users_db.GetUser(call.message.chat.id)[6])), reply_markup=keyboard.create_payment_inline(call.message.chat.id))

@tg.callback_query_handler(func=lambda call: True and call.data == 'cancel_acception')
def CallbackOrderCancelAcception(call):
    tg.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text ='Are you sure about THAT?',reply_markup=keyboard.cancel_acception())

@tg.callback_query_handler(func=lambda call: True and call.data == 'order_cancel')
def CallbackOrderCancel(call):
    users_db.EditOrdStatus(call.from_user.id,'')
    users_db.EditPayStatus(call.from_user.id,'0')
    tg.edit_message_text(chat_id=call.message.chat.id, parse_mode='HTML',message_id=call.message.message_id,reply_markup=keyboard.category_menu_inline(), text =lang.us.category_message)

@tg.callback_query_handler(func=lambda call: True and call.data[:12] == 'order_wallet')
def CallbackWalletMessage(call):
    tg.send_message(chat_id=call.message.chat.id, parse_mode='HTML',text='<b>'+users_db.GetUser(call.message.chat.id)[1]+'</b>')

@tg.callback_query_handler(func=lambda call: True and call.data[:11] == 'order_price')
def CallbackPriceMessage(call):
    tg.send_message(chat_id=call.message.chat.id, parse_mode='HTML',text='<b>'+call.data[12:]+'</b>')

@tg.callback_query_handler(func=lambda call: True and call.data[:12] == 'categorylist')
def CallbackCategoryList(call):
    tg.edit_message_text(chat_id=call.message.chat.id, parse_mode='HTML',message_id=call.message.message_id,reply_markup=keyboard.category_menu_inline(), text =lang.us.category_message)

@tg.callback_query_handler(func=lambda call: True and call.data[:12] == 'productlist_')
def CallbackProductList(call):
    tg.edit_message_text(chat_id=call.message.chat.id, parse_mode='HTML',message_id=call.message.message_id, text = lang.us.stock_message, reply_markup=keyboard.products_menu_inline(call.data[12:]))

@tg.callback_query_handler(func=lambda call: True and call.data[:13] == 'productcount_')
def CallbackPoductCount(call):
    tg.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =lang.us.product_count, reply_markup=keyboard.products_count_inline(call.data[13:]))

@tg.callback_query_handler(func=lambda call: True and call.data[:11] == 'newpayment_')
def CallbackPayment(call):
    users_db.EditOrdStatus(call.from_user.id,call.data[11:])
    users_db.EditPayStatus(call.from_user.id,'1')
    tg.edit_message_text(chat_id=call.message.chat.id, parse_mode='HTML', message_id=call.message.message_id, text=lang.us.create_payment(call.data[11:]), reply_markup=keyboard.create_payment_inline(call.message.chat.id))

if __name__=="__main__":
    tg.polling()
