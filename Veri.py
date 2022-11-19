import hashlib
import hmac
from urllib.parse import urljoin, urlencode
import pandas as pd
import requests
import TimeStamp

BASE_URL = "https://fapi.binance.com"


def fiyat(symbol, minute):
    url = f"/fapi/v2/positionRisk?symbol={symbol}&interval={minute}&limit=200"
    payload = {}
    headers = {
        "Content-Type": "application/json"
    }
    obje = requests.request("GET", url, headers=headers, data=payload).json()
    toplu = pd.DataFrame(obje, columns=["open_time", "open", "high", "low", "close", "volume", "close_time",
                                        "queast_asset_volume", "number_of_trades", "tbbav", "tbqav", "ignore"],
                         dtype=float)
    return toplu


class Altcoin:
    def __init__(self, adet, coin, dakika, limit, tStopLossYuzde, secretKey, apiKey, leverage, marginType):
        self.adet = adet
        self.coin = coin
        self.dakika = dakika
        self.limit = limit
        self.tStopLossYuzde = tStopLossYuzde
        self.secretKey = secretKey
        self.apiKey = apiKey
        self.leverage = leverage
        self.marginType = marginType

    def marginKaldirac(self):
        params = {
            "symbol": self.coin, "leverage": self.leverage, "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/leverage")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        response = requests.post(url, headers=headers, params=params).json()
        return response

    def marginTipi(self):
        params = {
            "symbol": self.coin, "marginType": self.marginType, "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/marginType")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        response = requests.post(url, headers=headers, params=params).json()
        return response

    def bilgiSelf(self):
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={self.coin}&interval={self.dakika}&limit=200"
        payload = {}
        headers = {
            "Content-Type": "application/json"
        }
        obje = requests.request("GET", url, headers=headers, data=payload).json()
        toplu = pd.DataFrame(obje, columns=["open_time", "open", "high", "low", "close", "volume", "close_time",
                                            "queast_asset_volume", "number_of_trades", "tbbav", "tbqav", "ignore"],
                             dtype=float)
        return toplu

    def islem(self):
        params = {
            "symbol": self.coin, "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v2/positionRisk")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        response = requests.get(url, headers=headers, params=params).json()
        veri = pd.DataFrame(response)
        return veri

    def balance(self):
        params = {
            "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v2/balance")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        response = requests.get(url, headers=headers, params=params).json()
        veri = pd.DataFrame(response)
        return veri

    def islemdeMi(self):
        bilgi = self.islem()["entryPrice"][0]
        if bilgi > 0:
            return True
        elif bilgi <= 0:
            return False

    def emirGonder(self, pozisyon, tip):
        params = {
            "symbol": self.coin, "positionSide": "BOTH", "type": tip, "workingType": "CONTRACT_PRICE",
            "side": pozisyon, "quantity": self.adet, "callBackRate": self.tStopLossYuzde,
            "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/order")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey
        }
        response = requests.post(url, headers=headers, params=params).json()
        return response

    def kapat(self, pozisyon):
        if pozisyon == "long":
            self.emirGonder("SELL", "MARKET")
        elif pozisyon == "short":
            self.emirGonder("BUY", "MARKET")

    def longAc(self):
        self.emirGonder("BUY", "MARKET")

    def shortAc(self):
        self.emirGonder("SELL", "MARKET")

    def gecmis(self):
        params = {
            "symbol": self.coin, "incomeType": "REALIZED_PNL", "limit": "10", "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/income")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey,
            self.apiKey: self.secretKey
        }
        response = requests.post(url, headers=headers, params=params).json()
        veri = pd.DataFrame(response, dtype=float)
        return veri

    def karHesapla(self):
        kar = 0
        for sayac in range(0, 5):
            kar += self.gecmis()["income"][sayac]
        return f"Son 5 işlemde toplam kar : {kar}"

    def tStopLoss(self, pozisyon):
        if pozisyon == "long":
            self.emirGonder("SELL", "TRAILING_STOP_MARKET")
        elif pozisyon == "short":
            self.emirGonder("BUY", "TRAILING_STOP_MARKET")

    def emirIptal(self):
        params = {
            "symbol": self.coin, "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v1/allOpenOrders")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey,
            self.apiKey: self.secretKey
        }
        response = requests.post(url, headers=headers, params=params)
        return response

    def acikEmirler(self):
        params = {
            "symbol": self.coin, "timestamp": TimeStamp.timeStamp()
        }
        queryString = urlencode(params)
        params["signature"] = hmac.new(self.secretKey.encode("utf-8"), queryString.encode("utf-8"),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, "/fapi/v2/openOrders")
        payload = {}
        headers = {
            "Content-Type": "application/json",
            "X-MBX-APIKEY": self.apiKey,
            self.apiKey: self.secretKey
        }
        response = requests.post(url, headers=headers, params=params).json()
        veri = pd.DataFrame(response, dtype=float)
        return veri

