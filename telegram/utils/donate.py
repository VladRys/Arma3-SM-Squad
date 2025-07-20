from telebot import types as t
from core.config import TEST_CRYPTOBOT_TOKEN
import requests
class Donate:
    def __init__(self, bot):
        self.bot = bot
        self.token = TEST_CRYPTOBOT_TOKEN
    
    def authorize(self):
        url = "https://pay.crypt.bot/api/getMe"
        headers = {
            "Crypto-Pay-API-Token": self.token
        }

        response = requests.get(url, headers=headers)
        print(response.json())

    def create_invoice(self, amount, currency='USDT'):
        
        url = "https://pay.crypt.bot/api/createInvoice"
        headers = {"Crypto-Pay-API-Token": self.token}
        data = {
            "amount": amount,
            "asset": currency,
            "description": "Донат на хост и разработку бота ❤️‍🔥",
        }
        response = requests.post(url, json=data, headers=headers)
        print(response.json())
        return response.json()


    def send_invoice_message(self, message):
        invoice = self.create_invoice(1)
        markup = t.InlineKeyboardMarkup(row_width=1)
        markup.add(t.InlineKeyboardButton(text='Ссылка', url=invoice['result']['bot_invoice_url']))
        self.bot.send_message(message.chat.id, 'Донат на хост и разработку бота ❤️‍🔥', parse_mode='Markdown', reply_markup = markup)        
