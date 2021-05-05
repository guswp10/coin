import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume) 로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-doge", count=30) # COUNT = ? 일동안 
#df = pyupbit.get_ohlcv("KRW-CHZ", count=14) 

# 변동성 돌파 기준 범위 계산, (고가 - 저가) *  k값
df['range'] = (df['high'] - df['low']) * 0.1

# range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# fee = 0.0032
#df['ror'] = np.where(df['high'] > df['target'],
#                     df['close'] / df['target'] - fee,
#                     1)

# np.where(조건문, 참일때 값, 거짓일때 값) ror은 수익률
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

# 누적 곱 계산(cumprod) => 누적 수익률  hpr
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100) 하락폭계산
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD (MAX Draw Down)
print("MDD(%): ", df['dd'].max())
print("HPR(%): ", df['hpr'].max())
df.to_excel("dd.xlsx")

#open : 시가, high : 고가, low : 저가, close : 종가, vloume : 거래량
#range : 변동폭*k, target : 매수가, ror : 수익률, hpr : 누적수익률, dd:낙폭
