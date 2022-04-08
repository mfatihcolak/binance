import time
import pandas_ta as ta
import numpy
import numpy as np
import pandas as pd
#import talib
#import talib as ta
import math

def bekle(sn):
    time.sleep(sn)

def yukariKesme(a,b):
    oncekiKisa = a[len(a)-3]
    kisa= a[len(a)-2]
    simdikiKisa = a[len(a)-1]

    oncekiUzun = b[len(b)-3]
    uzun = b[len(b)-2]
    simdikiUzun = b[len(b)-1]

    if oncekiKisa < oncekiUzun and kisa > uzun and simdikiKisa > simdikiUzun:
        return True
    else:
        return False

def asagiKesme(a,b):
    oncekiKisa = a[len(a) - 3]
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    oncekiUzun = b[len(b) - 3]
    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if oncekiKisa > oncekiUzun and kisa < uzun and simdikiKisa < simdikiUzun:
        return True
    else:
        return False

def dipMi(a):
    ikiOnce = a[len(a)-3]
    birOnce = a[len(a)-2]
    once = a[len(a)-1]

    if ikiOnce > birOnce and once > birOnce:
        return True
    else:
        return False

def tepeMi(a):
    ikiOnce = a[len(a)-3]
    birOnce = a[len(a)-2]
    once = a[len(a)-1]

    if ikiOnce < birOnce and once < birOnce:
        return True
    else:
        return False
def enYuksek(a,barSayisi):
    return max(a.tail(barSayisi))

def enDusuk(a,barSayisi):
    return min(a.tail(barSayisi))

def mesafe(l, eleman):
    for i in l.index:
        if l[i] == eleman:
            return len(l) -i -1
    return None


def generateSupertrend(close_array, high_array, low_array, atr_period, atr_multiplier):

    atr = ta.atr(high_array, low_array, close_array, atr_period)


    previous_final_upperband = 0
    previous_final_lowerband = 0
    final_upperband = 0
    final_lowerband = 0
    previous_close = 0
    previous_supertrend = 0
    supertrend = []
    supertrendc = 0

    for i in range(0, len(close_array)):
            highc = high_array[i]
            lowc = low_array[i]
            atrc = atr[i]
            closec = close_array[i]

            if math.isnan(atrc):
                atrc = 0

            basic_upperband = (highc + lowc) / 2 + atr_multiplier * atrc
            basic_lowerband = (highc + lowc) / 2 - atr_multiplier * atrc

            if basic_upperband < previous_final_upperband or previous_close > previous_final_upperband:
                final_upperband = basic_upperband
            else:
                final_upperband = previous_final_upperband

            if basic_lowerband > previous_final_lowerband or previous_close < previous_final_lowerband:
                final_lowerband = basic_lowerband
            else:
                final_lowerband = previous_final_lowerband

            if previous_supertrend == previous_final_upperband and closec <= final_upperband:
                supertrendc = final_upperband
            else:
                if previous_supertrend == previous_final_upperband and closec >= final_upperband:
                    supertrendc = final_lowerband
                else:
                    if previous_supertrend == previous_final_lowerband and closec >= final_lowerband:
                        supertrendc = final_lowerband
                    elif previous_supertrend == previous_final_lowerband and closec <= final_lowerband:
                        supertrendc = final_upperband

            supertrend.append(supertrendc)

            previous_close = closec

            previous_final_upperband = final_upperband

            previous_final_lowerband = final_lowerband

            previous_supertrend = supertrendc

    return supertrend

def superTrendMi(superTrend,close):
    son_kapanis = close[len(close)-1]
    onceki_kapanis = close[len(close)-2]

    son_supertrend_deger = superTrend[len(superTrend)-1]
    onceki_supertrend_deger = superTrend[len(superTrend)-2]

    if son_kapanis > son_supertrend_deger and onceki_kapanis < onceki_supertrend_deger:
        return True

    if son_kapanis < son_supertrend_deger and onceki_kapanis > onceki_supertrend_deger:
        return False

def upLowFinder(up,low,close):
    if close[len(close)-1] > up[len(up)-1]:
        return True
    if close[len(close)-1] < low[len(low)-1]:
        return False
def rsiAndMacd(rsi,macd,macdSignal):
    closeMacd = macd[len(macd) - 1]
    closeMacdSignal = macdSignal[len(macdSignal) - 1]

    prevCloseMacd = macd[len(macd) - 2]
    prevCloseMacdSignal = macdSignal[len(macdSignal) - 2]

    closeRsi = rsi[len(rsi) - 1]

    if closeMacd > closeMacdSignal and prevCloseMacd < prevCloseMacdSignal and closeRsi > 50:
        return True
    if closeMacd < closeMacdSignal and prevCloseMacd > prevCloseMacdSignal and closeRsi <50:
        return False

def T3TillsonIndicatorHesaplama(close_array, high_array, low_array, volume_factor, t3Length):
    ema_first_input = (high_array + low_array + 2 * close_array) / 4

    e1 = ta.ema(ema_first_input, t3Length)

    e2 = ta.ema(e1, t3Length)

    e3 = ta.ema(e2, t3Length)

    e4 = ta.ema(e3, t3Length)

    e5 = ta.ema(e4, t3Length)

    e6 = ta.ema(e5, t3Length)

    c1 = -1 * volume_factor * volume_factor * volume_factor

    c2 = 3 * volume_factor * volume_factor + 3 * volume_factor * volume_factor * volume_factor

    c3 = -6 * volume_factor * volume_factor - 3 * volume_factor - 3 * volume_factor * volume_factor * volume_factor

    c4 = 1 + 3 * volume_factor + volume_factor * volume_factor * volume_factor + 3 * volume_factor * volume_factor

    T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

    return T3


def T3TillsonSinyal(tillsont3):
    t3_last = tillsont3[len(tillsont3)-1]
    t3_previous = tillsont3[len(tillsont3)-2]
    t3_prev_previous = tillsont3[len(tillsont3)-3]

    # kırmızıdan yeşile dönüyor
    if t3_last > t3_previous and t3_previous < t3_prev_previous:
        return True

    # yeşilden kırmızıya dönüyor
    elif t3_last < t3_previous and t3_previous > t3_prev_previous:
        return False

def macdCrossover(close):
    fastLength = 8
    slowLength = 16
    signalLength = 11
    fastMA = ta.ema(close, fastLength)
    slowMA = ta.ema(close, slowLength)
    macd = fastMA - slowMA
    signal = ta.sma(macd, signalLength)
    if (signal[len(signal) - 2] >= macd[len(macd) - 2] or signal[len(signal) - 2] >= macd[len(macd) - 2] - 0.01) and \
            (signal[len(signal)-1] < (macd[len(macd)-1] - 0.05)):
        return True
    elif (signal[len(signal)-2] <= macd[len(macd)-2] or signal[len(signal)-2] <= macd[len(macd)-2] + 0.01) and \
            (signal[len(signal)-1] > (macd[len(macd)-1] + 0.05)):
        return False



def alphaTrenddeneme(close,low,high):
    coeff = 1
    AP = 14
    #showsignalsk = True
    novolumedata = False
    TR = np.max(high[len(high) -1] - low[len(low) -1], numpy.abs(high[len(high)-1] - close[len(close) -1]), numpy.abs(low[len(low)-1] - close[len(close) - 1]))
    ATR = ta.sma(ta.true_range(high, low, close), AP)
    upT = low - ATR * coeff
    downT = high + ATR * coeff
    hlc3 = (high + low + close) / 3
    AlphaTrend = [0.0] #walrus operator
    if AlphaTrend := (novolumedata if ta.rsi(close, 14) >= 50 else ta.mfi(hlc3, 14) >= 50) if (upT < np.isnan(AlphaTrend[len(AlphaTrend) - 1]) if np.isnan(AlphaTrend[len(AlphaTrend) - 1]) else upT) else (downT > np.isnan(AlphaTrend[len(AlphaTrend) - 1]) if np.isnan(AlphaTrend[len(AlphaTrend) - 1]) else downT):
        return AlphaTrend
    if AlphaTrend[len(AlphaTrend) - 2] > AlphaTrend[len(AlphaTrend) - 2] and AlphaTrend[len(AlphaTrend) - 1] < AlphaTrend[len(AlphaTrend) - 1]:
        return True
    else:
        return False

def alphaTrend(close,low,high,volume):
    AP= 14
    ATR = ta.sma(ta.true_range(high, low, close), AP)
    noVolumeData = True
    coeff = 0.1
    rsi = ta.rsi(close, 14)
    upT = []
    downT = []
    AlphaTrend = [0.0]
    hlc3 = ta.hlc3(high, low, close)
    mfi = ta.mfi(high,low,close,volume, 14)
    k1 = []
    k2 = []
    for i in range(len(low)):
        if pd.isna(ATR[i]):
            upT.append(0)
        else:
            upT.append(low[i] - (ATR[i] * coeff))
    for i in range(len(high)):
        if pd.isna(ATR[i]):
            downT.append(0)
        else:
            downT.append(high[i] + (ATR[i] * coeff))
    for i in range(1, len(close)):
        if noVolumeData is True and rsi[i] >= 50:
            if upT[i] < AlphaTrend[i-1]:
                AlphaTrend.append(AlphaTrend[i-1])
            else:
                AlphaTrend.append(upT[i])
        elif noVolumeData is False and mfi[i] >=50:
            if upT[i] < AlphaTrend[i-1]:
                AlphaTrend.append(AlphaTrend[i-1])
            else:
                AlphaTrend.append(upT[i])
        else:
            if downT[i] > AlphaTrend[i-1]:
                AlphaTrend.append(AlphaTrend[i-1])
            else:
                AlphaTrend.append(downT[i])
    for i in range(len(AlphaTrend)):
        if i < 2:
            k2.append(0)
            k1.append(AlphaTrend[i])
        else:
            k2.append(AlphaTrend[i-2])
            k1.append(AlphaTrend[i])
    at = pd.DataFrame(data=k1, columns=["k1"])
    at["k2"] = k2
    if k1[len(k1)-2] <= k2[len(k2) -2] and k1[len(k1)-1] > k2[len(k2)-1]:
        return True
    elif k1[len(k1)-2] >= k2[len(k2) -2] and k1[len(k1)-1] < k2[len(k2)-1]:
        return False


def crossOver(a,b):
    kisa = a[len(a) - 2]
    simdikiKisa = a[len(a) - 1]

    uzun = b[len(b) - 2]
    simdikiUzun = b[len(b) - 1]

    if kisa > uzun and simdikiKisa < simdikiUzun:
        return True
    else:
        return False

