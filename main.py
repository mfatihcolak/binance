import talib.stream
from talib import MA_Type
from StratejikFonksiyonlar import *
from Telegram import *
from Veri import Altcoin, fiyat

apiKey = input("Binance Api Key = ")
secretKey = input("Binance Secret Key = ")
coin = input("İşlem Yapılacak coin adını giriniz: ( BTCUSDT ) = ")
adet = float(input("Kaç adet alınacak = "))
dakika = input("Kaç dakikalık grafikler ( 1m, 3m, 15m, 1h, 4h, 1d ) = ")
limit = 0
telegramId = input("Telegram Id'nizi girin = ")
price = fiyat(coin, dakika)["close"][len(fiyat(coin, dakika)["close"]) - 1]
print(coin, "fiyatı = ", price)
secim = input("Kar al ve Stoplu bir stratejimi olsun ? ( y/n ) = ")

if secim == "y":
    tslYuzde = float(input("İz Süren Stop Yüzdesi Gir = "))
    stop = float(input("Kaç dolar zararda stop olmak istiyorsun = "))
    kar = float(input("Kaç dolar karda işlemi kapatmak istiyorsun = "))
    tezdAktif = float(input("Takip eden zarar durdur PNL kaç olduktan sonra çalışsın"))
else:
    tslYuzde = 0
kaldirac = input("Kaç x kaldıraç = ")
marginType = "ISOLATED"

telegramBotSendText(f"BOT Verileri girildi : \n{coin}\n Adet = {adet}\n Periyot = {dakika} \n Kaldıraç = {kaldirac}",
                    telegramId)

coin1 = Altcoin(adet, coin, dakika, limit, tslYuzde, secretKey, apiKey, kaldirac, marginType)
bekle(1)
coin1.marginTipi()
bekle(1)
coin1.marginKaldirac()
bekle(1)


def emaKesisim():
    emaKisa = input("Kısa EMA girin = ")
    emaUzun = input("Uzun EMA girin = ")
    izAktif = False
    telegramBotSendText("EMA kesişim Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        close = coin1.bilgiSelf()["close"]  # istenilen coinin kapanış değerlerini getirir
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        emaK = talib.EMA(close, float(emaKisa))
        emaU = talib.EMA(close, float(emaUzun))

        kontrol = islem["entryPrice"][0]
        bekle(1)

        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if yukariKesme(emaK, emaU) is True:  # EMA KISA EMA UZUNU YUKARI KESTİYSE
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif asagiKesme(emaK, emaU) is True:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if asagiKesme(emaK, emaU) is True:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if yukariKesme(emaK, emaU) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True


def smaKesisim():
    smaKisa = input("Kısa SMA girin = ")
    smaUzun = input("Uzun SMA girin = ")
    izAktif = False
    telegramBotSendText("SMA kesişim Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        close = coin1.bilgiSelf()["close"]  # istenilen coinin kapanış değerlerini getirir
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        smaK = talib.SMA(close, float(smaKisa))
        smaU = talib.SMA(close, float(smaUzun))

        kontrol = islem["entryPrice"][0]
        bekle(1)

        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if yukariKesme(smaK, smaU) is True:  # EMA KISA EMA UZUNU YUKARI KESTİYSE
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif asagiKesme(smaK, smaU) is True:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if asagiKesme(smaK, smaU) is True:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if yukariKesme(smaK, smaU) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True


def bollinger():
    izAktif = False
    telegramBotSendText("Bollinger Bandı Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        close = coin1.bilgiSelf()["close"]  # istenilen coinin kapanış değerlerini getirir
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=MA_Type.T3)
        kontrol = islem["entryPrice"][0]
        bekle(1)

        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if upLowFinder(upper,lower,close) is False:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif upLowFinder(upper,lower,close) is True:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if upLowFinder(upper,lower,close) is True:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if upLowFinder(upper,lower,close) is False:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True


def superTrend():
    izAktif = False
    telegramBotSendText("SuperTrend Stratejisi Seçildi", telegramId)

    islemTipi = ""
    while True:
        close = coin1.bilgiSelf()["close"]
        high = coin1.bilgiSelf()["high"]
        low = coin1.bilgiSelf()["low"]
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)

        superTrendHesaplama = generateSupertrend(close, high, low, 14, 2.8)
        kontrol = islem["entryPrice"][0]
        bekle(1)

        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if superTrendMi(superTrendHesaplama, close) is True:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif superTrendMi(superTrendHesaplama, close) is False:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if superTrendMi(superTrendHesaplama, close) is False:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                    telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
            elif secim == "y":
                if pnl > kar:
                    coin1.kapat(islemTipi)
                    islemTipi = ""
                    telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                    print(f"{kar} dolar kar alındı")
                elif pnl < -stop:
                    coin1.kapat(islemTipi)
                    islemTipi = ""
                    telegramBotSendText("Stop olundu ", telegramId)
                    print("Stop olundu")
                elif pnl > tezdAktif and izAktif is False:
                    coin1.tStopLoss(islemTipi)
                    telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                    print("İz süren stop aktifleşti")
                    izAktif = True
            elif islemTipi == "short":
                if superTrendMi(superTrendHesaplama, close) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True

def rsiVeMacd():
    izAktif = False
    telegramBotSendText("Macd Kesişimi ve RSI stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        close = coin1.bilgiSelf()["close"]
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        macd, macdSignal, macdHist = ta.MACD(close,fastperiod=12, slowperiod=26, signalperiod=9)
        rsi = ta.RSI(close,timeperiod=14)
        kontrol = islem["entryPrice"][0]
        bekle(1)

        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if rsiAndMacd(rsi,macd,macdSignal) is True:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif rsiAndMacd(rsi,macd,macdSignal) is False:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if rsiAndMacd(rsi,macd,macdSignal) is False:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if rsiAndMacd(rsi,macd,macdSignal) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText(f"{kar} dolar kar alındı", telegramId)
                        print(f"{kar} dolar kar alındı")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True

def tillson():
    izAktif = False
    telegramBotSendText("Tillson T3 Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        bekle(10)
        close = coin1.bilgiSelf()["close"]
        high = coin1.bilgiSelf()["high"]
        low = coin1.bilgiSelf()["low"]
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        volume_factor = 0.7
        t3length = 8
        tillsont3 = T3TillsonIndicatorHesaplama(close,high,low,volume_factor,t3length)
        kontrol = islem["entryPrice"][0]
        bekle(1)
        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if T3TillsonSinyal(tillsont3) is True:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif T3TillsonSinyal(tillsont3) is False:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if T3TillsonSinyal(tillsont3) is False:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(1)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if T3TillsonSinyal(tillsont3) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(1)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True

def macdCrossOverStrategy():
    izAktif = False
    telegramBotSendText("Macd Crossover Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        bekle(5)
        close = coin1.bilgiSelf()["close"]
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        kontrol = islem["entryPrice"][0]
        bekle(1)
        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if macdCrossover(close) is True:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif macdCrossover(close) is False:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if macdCrossover(close) is False:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(2)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if macdCrossover(close) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(1)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True

def AlphaTrend():
    izAktif = False
    telegramBotSendText("Alpha Trend Stratejisi Seçildi", telegramId)

    islemTipi = ""

    while True:
        bekle(5)
        close = coin1.bilgiSelf()["close"]
        low = coin1.bilgiSelf()["low"]
        high = coin1.bilgiSelf()["high"]
        volume = coin1.bilgiSelf()["volume"]
        bekle(1)
        islem = coin1.islem()
        profit = islem["unRealizedProfit"][0]
        bekle(1)
        pnl = float(profit)
        kontrol = islem["entryPrice"][0]
        bekle(1)
        if float(kontrol) <= 0:
            coin1.emirIptal()
            bekle(1)
            izAktif = False
            bekle(1)
            if alphaTrend(close,low,high,volume) is True:
                coin1.longAc()
                islemTipi = "long"
                bekle(1)
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından LONG işlem açıldı")
            elif alphaTrend(close,low,high,volume) is False:
                coin1.shortAc()
                islemTipi = "short"
                giris = coin1.islem()["entryPrice"][0]
                bekle(1)
                telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı", telegramId)
                print(f"{coin1.coin} {giris} fiyatından SHORT işlem açıldı")
        elif float(kontrol) > 0:
            if islemTipi == "long":
                if alphaTrend(close,low,high,volume) is False:
                    coin1.kapat(islemTipi)
                    islemTipi = "short"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından LONG işlem kapatılıp SHORT işlem açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(2)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True
            elif islemTipi == "short":
                if alphaTrend(close,low,high,volume) is True:
                    coin1.kapat(islemTipi)
                    coin1.longAc()
                    islemTipi = "long"
                    bekle(1)
                    giris = coin1.islem()["entryPrice"][0]
                    bekle(1)
                    telegramBotSendText(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı",
                                        telegramId)
                    print(f"{coin1.coin} {giris} fiyatından SHORT işlem kapatılıp LONG açıldı")
                elif secim == "y":
                    if pnl > kar:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        bekle(1)
                        guncelbakiye = coin1.balance()["availableBalance"][6]
                        telegramBotSendText(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}", telegramId)
                        print(f"{kar} dolar kar alındı /// Güncel USDT Bakiyeniz = {guncelbakiye}")
                    elif pnl < -stop:
                        coin1.kapat(islemTipi)
                        islemTipi = ""
                        telegramBotSendText("Stop olundu ", telegramId)
                        print("Stop olundu")
                    elif pnl > tezdAktif and izAktif is False:
                        coin1.tStopLoss(islemTipi)
                        telegramBotSendText("İz Süren stop aktifleşti", telegramId)
                        print("İz süren stop aktifleşti")
                        izAktif = True

stratejiSecim = input(
    "Strateji Seç : \n 1-) EMA kesişimlerine göre işlem açar \n "
    "2-) SMA Kesişimlerine göre işlem açar \n "
    "3-) Bollinger bandı stratejisine göre işlem açar \n "
    "4-) SuperTrend Stratejisine Göre İşlem Açar \n "
    "5-) Macd Kesişimi ve RSI stratejisine göre işlem açar \n "
    "6-) Tillson T3 stratejisine göre işlem açar \n "
    "7-) Macd Crossover stratejisine göre işlem açar \n "
    "8-) AlphaTrend stratejisine göre işlem açar \n ")

if stratejiSecim == "1":
    emaKesisim()
elif stratejiSecim == "2":
    smaKesisim()
elif stratejiSecim == "3":
    bollinger()
elif stratejiSecim == "4":
    superTrend()
elif stratejiSecim == "5":
    rsiVeMacd()
elif stratejiSecim == "6":
    tillson()
elif stratejiSecim == "7":
    macdCrossOverStrategy()
elif stratejiSecim == "8":
    AlphaTrend()
else:
    print("Strateji Seçmediniz")
