import time

import talib
import talib as ta
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

    atr = ta.ATR(high_array, low_array, close_array, atr_period)


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

    e1 = ta.EMA(ema_first_input, t3Length)

    e2 = ta.EMA(e1, t3Length)

    e3 = ta.EMA(e2, t3Length)

    e4 = ta.EMA(e3, t3Length)

    e5 = ta.EMA(e4, t3Length)

    e6 = ta.EMA(e5, t3Length)

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
    fastMA = talib.EMA(close, fastLength)
    slowMA = talib.EMA(close, slowLength)
    macd = fastMA - slowMA
    signal = talib.SMA(macd, signalLength)
    if signal[len(signal) - 2] >= macd[len(macd) - 2]:
        if signal[len(signal)-1] < macd[len(macd)-1] - 0.0004:
            return True
    elif signal[len(signal)-2] <= macd[len(macd)-2]:
        if signal[len(signal)-1] > macd[len(macd)-1] + 0.0004:
            return False




