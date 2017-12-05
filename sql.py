#PaymentStatus 0 = вы ничего не заказали
#PaymentStatus 1 = Ожидание оплаты
#PaymentStatus 2 = Подтверждение перевода
#PaymentStatus 5 = Деньги получены. Оплата произведена.

import sqlite3, telebot, traceback, requests, urllib, json

class SQL:

    def SelectAllCategories(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM categories').fetchall()

    def SelectAllUsers(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def EditOrdStatus(self, TLID, OrdStatus):
        with self.connection:
            return self.cursor.execute('UPDATE users SET ORDSTATUS= ? WHERE TLID= ?', (OrdStatus, TLID))

    def EditPayStatus(self, TLID, PayStatus):
        with self.connection:
            return self.cursor.execute('UPDATE users SET PAYSTATUS= ? WHERE TLID= ?', (PayStatus, TLID))

    def SelectPayUsers(self):
        """ Получаем все строки """
        biglist = []
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE PAYSTATUS = 1').fetchall()

    def SelectAllProducts(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM products').fetchall()

    def GetData(self, ProductName):
        """ Получаем одну строку с номером tl_id """
        with self.connection:
            return self.cursor.execute('SELECT * FROM products WHERE ProductName = ?', [ProductName]).fetchall()[0]

    def GetUser(self, TLID):
        """ Получаем одну строку с номером tl_id """
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE TLID = ?', [TLID]).fetchall()[0]

    def AddUser(self, TLID):
        with self.connection:
            redeem_code = requests.get("https://bitaps.com/api/create/redeemcode").json()['redeem_code']
            url = 'https://bitaps.com/api/get/redeemcode/info'
            parameters = {'redeemcode': redeem_code}
            response = requests.post(url, data=json.dumps(parameters)).json()
            return self.cursor.execute('INSERT INTO users (TLID, ADDRESS, REDEEMCODE, BALANCE, PBALANCE, PAIDOUT, SYSSTATUS) VALUES (?,?,?,?,?,?,?)', (TLID,response['address'],redeem_code,response['balance'],response['pending_balance'],response['paid_out'],0))


    def UpdateBalance(self, TLID, RedeemCode):
        with self.connection:
            url = 'https://bitaps.com/api/get/redeemcode/info'
            parameters = {'redeemcode': RedeemCode}
            response = requests.post(url, data=json.dumps(parameters)).json()
            return self.cursor.execute('UPDATE users SET BALANCE=?,PBALANCE=?,PAIDOUT=? WHERE TLID= ?', (response['balance'],response['pending_balance'],response['paid_out'], TLID))

    def SelectAllFromCategory(self, ProductCategory):
        with self.connection:
            return self.cursor.execute('SELECT * FROM products WHERE ProductCategory = ?', [ProductCategory]).fetchall()

    def EditProduct(self, ProductName, ProductPrice):
        with self.connection:
            return self.cursor.execute('UPDATE products SET ProductPrice= ? WHERE ProductName= ?', (ProductPrice, ProductName))

    def close(self):
        self.connection.close()
