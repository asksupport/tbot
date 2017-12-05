from sql import SQL
import math
import requests, json
users_db = SQL('users.db')


class us:
    global course
    course = (requests.get("https://blockchain.info/ru/ticker").json()['AUD']['15m'])
    start_message = "💆 Welcome to the Ask Alice drug shop! Here you can buy everything you want without dangerous offline meetings!"
    category_message = "💁 Choose category:"
    stock_message = "💁 Choose sort:"
    escape_btn = '↖️ Back'
    assortment_btn = '🍃 Assortment'
    order_status_btn = '⏳ Order status'
    bitcoin_wallet_btn = '💳 Bitcoin wallet'
    support_message_btn = '💬 Contact support'
    cancel_order = '🔕 Cancel order'
    bitcoin_as_message = '💳 Send BTC adress for copypast '
    price_as_message = '💵 Send order value'
    order_return = '🚶🏼‍♀️ Return'
    order_confirm = '💃🏻 Confirm'
    support_message = '😯 Sorry us for non-regular support, first time you can contact us here @askaliceforsupport every day from 8pm to midnight'
    payment_received = '<b>Payment received.</b> Your adress:'
    product_count = '🖐 Choose product count:'

    def choose_product(ProductName):
        return('You have choosen <b>'+str(ProductName)+'</b>.\nChoose sort from possitions based lower:')

    def create_payment(Product):
        Product = Product.split('_')
        product_name = Product[1]
        price_btc = Product[3]
        count = Product[2]
        disclaimer = '🕐 Processing <i>it can hold for a short time</i>. With lack of payment order will automatically cancel in 24 hours. Money you sent to wallet will be able to shop.\n🎯 <b>Payment status</b> and <b>order status</b> you can find in main menu.'
        return('📌 You have choosen: <b>'+product_name+' ('+count+' g.)</b>\n💵 Total: <b>'+str(price_btc)+'</b> BTC.'+'\n\n'+disclaimer)

    def product_price(ProductName, ProductCount, ProductPrice):
        return(str(int(ProductCount)*int(ProductPrice))+' AUD '+ProductCount+' oz')

    def status(TLID):
        status = users_db.GetUser(TLID)[8]
        if status == 0:
            return('🗑 Your cart is empty.')
        if status == 1:
            return('🕣 Payment awaiting.')
        if status == 2:
            return('🕣 Payment recived. Balance checking.')
        if status == 5:
            return('✔️ Payment recived. Adress sent.')


    def bitcoin_wallet(TLID):
        amount_btc = users_db.GetUser(TLID)[3]*(10**-8)
        amount_aud = round(amount_btc*course,2)
        payment_status = users_db.GetUser(TLID)[4]
        pending = users_db.GetUser(TLID)[4]
        if payment_status == 0:
            payment_status = 'no payment recieved.'
        else:
            payment_status = 'payment checking. Sorry, but it could take few hours.'
        return('💰 Your bitcoin wallet: <b>'+users_db.GetUser(TLID)[1]+'</b> \n🛒 You filled your wallet for: <b>'+str(amount_btc)+'</b> BTC [<i>'+str(amount_aud)+'$</i> ~'+str(round(pending/10**8*course,3))+']\n⚖️ rate BTC/$: <b>'+str(course)+'</b>\n🕒 Payment status: <b>'+payment_status+'</b>')
