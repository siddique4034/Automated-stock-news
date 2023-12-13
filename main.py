import requests
from datetime import datetime, timedelta
import smtplib


MY_EMAIL = "mdsiddiquerain@gmail.com"
PASSWORD = "dykytphasnylvqhx"
TO_EMAIL = "siddiquemd4034@gmail.com"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_KEY = "706e66e93c234d6aa47eac5d37e22df5"
news_list = []
STOCK_KEY= "Z25O8SZJIJ0N5BZV"
result = "increased 🔺"

today = datetime.now()
today_date = f"{today}".split()[0]
last_30_days = f"{today - timedelta(days=30)}".split()[0]
yesterday = f"{today - timedelta(days=1)}".split()[0]
last_yesterday = f"{today - timedelta(days=2)}".split()[0]

stock_response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={STOCK_KEY}")

data = stock_response.json()

yesterday_value = float(data["Time Series (Daily)"][yesterday]["4. close"])

last_yesterday_value = float(data["Time Series (Daily)"][last_yesterday]["4. close"])

change_in_value = (yesterday_value - last_yesterday_value) * 100 / last_yesterday_value


if change_in_value < 0: 
  result = "decreased 🔻"

if change_in_value >= 5 or change_in_value <= -5:
  news_response = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={today_date}&to={last_30_days}&sortBy=popularity&apiKey={NEWS_KEY}")

  news = news_response.json()
  for i in range(0, 3):
    news_list.append(news["articles"][i])


  with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=f"Subject: Tesla stock {result} by {change_in_value}%\n\n{STOCK} is {result} by {change_in_value}\n\nThese are the sources\n\n\nHEADLINE: {news_list[0]['title']}\nDESCRIPRION: {news_list[0]['description']}\nURL: {news_list[0]['url']}\n\nHEADLINE: {news_list[1]['title']}\nDESCRIPRION: {news_list[1]['description']}\nURL: {news_list[1]['url']}\n\nHEADLINE: {news_list[2]['title']}\nDESCRIPRION: {news_list[2]['description']}\nURL: {news_list[2]['url']}\n\n".encode('utf-8'))
    
    
