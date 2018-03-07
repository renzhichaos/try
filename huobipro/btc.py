import huobipro.huobi as mm
import time
import itchat

itchat.auto_login(hotReload=True, enableCmdQR=True)
author = itchat.search_chatrooms(name='三人行')[0]
tradef = mm.get_kline("btcusdt", "1min", 1)
dataf = tradef["data"]

author.send('btc:' + str(dataf[0]["close"]) + "$=🙏")
price = dataf[0]["close"]
print(price)
print("成交日期时间", "\t\t\t\t", "对比价", "\t\t", "开盘价", "\t\t", "收盘价", "\t\t", "最低价", "\t\t", "最高价", "\t\t", "成交笔数", "\t", "成交额")
for x in iter(dataf):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x["id"])), "\t", price, "\t", x["open"], "\t", x["close"], "\t",x["low"], "\t", x["high"], "\t", x["count"], "\t", x["vol"])
time.sleep(60)
i = 1
j = 1
while True:
    trade = mm.get_kline("btcusdt", "1min", 1)
    data = trade["data"]

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data[0]["id"])), "\t", price, "\t", data[0]["open"], "\t", data[0]["close"], "\t", data[0]["low"], "\t", data[0]["high"], "\t", data[0]["count"], "\t", data[0]["vol"])
    if data[0]["close"] > price + i*10:
        author.send('btc:' + str(data[0]["close"]) + "$↑👆")
        i = i + 1
    elif data[0]["close"] < price - j*10:
        author.send('btc:' + str(data[0]["close"]) + "$↓👇")
        j = j + 1
    elif price - j*10 <= data[0]["close"] <= price + i*10:
        i = i
        j = j

    time.sleep(60)
