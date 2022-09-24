import requests
from datetime import date, timedelta
from twilio.rest import Client

account_sid = '__Your_account_SID__'
auth_token = '__Your_auth_token'

date = date.today()
before_yesterday = date - timedelta(days=3)
yesterday = date - timedelta(days=2)
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "Alphavantage API Key"
NEWS_APIKEY = '__newsapi.com API Key'

## Using https://www.alphavantage.co to get stock price
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News")
parametres_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
c = requests.get(url="https://www.alphavantage.co/query", params=parametres_stock)
stock_data = c.json()
close_price = float(stock_data['Time Series (Daily)'][f"{before_yesterday}"]["4. close"])
open_price = float(stock_data['Time Series (Daily)'][f"{yesterday}"]["1. open"])
if (close_price-open_price)>=0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

percent = abs((close_price - open_price) / close_price) * 100
rounded = round(percent,2)
## Using https://newsapi.org
# Instead of printing all news from ("Get News"), getting the first 3 news pieces for the COMPANY_NAME.
parametres_news = {
    "apiKey": NEWS_APIKEY,
    "q": "Tesla",
    "pageSize": "3"
}
n = requests.get(url="https://newsapi.org/v2/top-headlines", params=parametres_news)
news_data = n.json()
news_1 = news_data["articles"][0]["title"]
breif_1 = news_data["articles"][0]["description"]
news_2 = news_data["articles"][1]["title"]
breif_2 = news_data["articles"][1]["description"]
news_3 = news_data["articles"][2]["title"]
breif_3 = news_data["articles"][2]["description"]

##  Using https://www.twilio.com
# Sending a seperate message with the percentage change and each article's title and description to your phone number.
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
    body=f"TSLA : {up_down}{percent}\n"
         f"Headline: {news_1}\n"
         f"Brief:{breif_1}\n"
         f"Headline: {news_2}\n"
         f"Brief:{breif_2}\n"
         f"Headline: {news_3}\n"
         f"Brief:{breif_3}\n",
    to="+919160597001",
    from_="+16067141570"
)
print(message.status)

# This message is sent to our phone
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
