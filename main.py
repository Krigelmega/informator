
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from pybit.unified_trading import HTTP
import okx.Account as Account
import concurrent.futures
import logging
import pytz

api_key = 'UIVxrdbrHubkUoumq3'
api_secret = 'fCr4EFilGlH2EWwSq1L30fOQ4mlSXjcPgPcY'
api_key2 = 'xtyMkrnsXPEO5bqNUW'
api_secret2 = 'GkiyJTLXAy9yNt31JLdpEl5whsqqDtgV4H8k'

def main():
    logging.basicConfig(level=logging.INFO)
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret, recv_window=10000)
    session_sem = HTTP(testnet=False, api_key=api_key2, api_secret=api_secret2, recv_window=10000)
    api_key3 = "1a99a7d8-2a20-4b60-8fc4-23533c4c1944"
    secret_key3 = "394FEE3C7EACBE51680896451B139187"
    passphrase3 = "784512Zz."
    api_key4 = 'b73ea002-1fd2-4620-b2ab-1022b79e3777'
    secret_key4 = '1ACA55BD8DCD57D6437EE0249B5D2BC1'
    passphrase4 = '>y]3SrrE64xzd/=Eb/d8Wospk'
    flag = "0"  # live trading: 0, demo trading: 1
    
    accountAPI = Account.AccountAPI(api_key3, secret_key3, passphrase3, False, flag)
    accountAPI_sem = Account.AccountAPI(api_key4, secret_key4, passphrase4, False, flag)

    result = accountAPI.get_account_balance()
    result_sem = accountAPI_sem.get_account_balance()
    
    pos = accountAPI.get_positions()
    pos_sem = accountAPI_sem.get_positions()

    logging.log(logging.INFO, pos)
    logging.log(logging.INFO, result_sem)
    
    if pos['data'] == [] or pos_sem['data'] == []:
        return
    
    list_of_pos = list(pos['data'])
    pos_sem = list(pos_sem['data'])
    
    
    result_okx = result['data'][0]
    result_okx_sem = result_sem['data'][0]
    

    symbols_now_okx_vic = []
    order_volume_okx_vic = []
    buy_price_okx_vic = []
    market_price_now_okx_vic = []
    pnl_okx_vic = []
    open_time_okx_vic = []
    edit_time_okx_vic = []

    symbols_now_okx_sem = []
    order_volume_okx_sem = []
    buy_price_okx_sem = []
    market_price_now_okx_sem = []
    pnl_okx_sem = []
    open_time_okx_sem = []
    edit_time_okx_sem = []

    vladivostok_tz = pytz.timezone('Asia/Vladivostok')

    for market_position in list_of_pos:
        symbols_now_okx_vic.append(market_position['instId'].split('-')[0])
        order_volume_okx_vic.append(int(float(market_position['notionalUsd'])))
        buy_price_okx_vic.append(market_position['avgPx'][:10])
        market_price_now_okx_vic.append(market_position['markPx'][:10])
        pnl_okx_vic.append(market_position['uplLastPx'][:5])
        open_time_okx_vic.append(datetime.fromtimestamp(int(market_position['cTime']) if int(market_position['cTime']) <= 1e12 else (int(market_position['cTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))
        edit_time_okx_vic.append(datetime.fromtimestamp(int(market_position['uTime']) if int(market_position['uTime']) <= 1e12 else (int(market_position['uTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))

    for market_position in pos_sem:
        symbols_now_okx_sem.append(market_position['instId'].split('-')[0])
        order_volume_okx_sem.append(int(float(market_position['notionalUsd'])))
        buy_price_okx_sem.append(market_position['avgPx'][:10])
        market_price_now_okx_sem.append(market_position['markPx'][:10])
        pnl_okx_sem.append(market_position['uplLastPx'][:5])
        open_time_okx_sem.append(datetime.fromtimestamp(int(market_position['cTime']) if int(market_position['cTime']) <= 1e12 else (int(market_position['cTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))
        edit_time_okx_sem.append(datetime.fromtimestamp(int(market_position['uTime']) if int(market_position['uTime']) <= 1e12 else (int(market_position['uTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))

    posi_bb = session.get_positions(category='linear', settleCoin='USDT')
    posi_bb_sem = session_sem.get_positions(category='linear', settleCoin='USDT')
    
    if posi_bb['result']['list'] == [] or posi_bb_sem['result']['list'] == []:
        return

    posi_bb = posi_bb['result']['list']
    posi_bb_sem = posi_bb_sem['result']['list']

    symbols_now_bb_vic = []
    order_volume_bb_vic = []
    buy_price_bb_vic = []
    market_price_now_bb_vic = []
    pnl_bb_vic = []
    open_time_bb_vic = []
    edit_time_bb_vic = []

    symbols_now_bb_sem = []
    order_volume_bb_sem = []
    buy_price_bb_sem = []
    market_price_now_bb_sem = []
    pnl_bb_sem = []
    open_time_bb_sem = []
    edit_time_bb_sem = []
    
        for position in posi_bb:
        symbols_now_bb_vic.append(position['symbol'][:-4])
        order_volume_bb_vic.append(int(float(position['positionValue'])))
        buy_price_bb_vic.append(position['avgPrice'][:10])
        market_price_now_bb_vic.append(position['markPrice'][:10])
        pnl_bb_vic.append(position['unrealisedPnl'][:5])
        open_time_bb_vic.append(datetime.fromtimestamp(int(position['createdTime']) if int(position['createdTime']) <= 1e12 else (int(position['createdTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))
        edit_time_bb_vic.append(datetime.fromtimestamp(int(position['updatedTime']) if int(position['updatedTime']) <= 1e12 else (int(position['updatedTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))
        
    for position in posi_bb_sem:
        symbols_now_bb_sem.append(position['symbol'][:-4])
        order_volume_bb_sem.append(int(float(position['positionValue'])))
        buy_price_bb_sem.append(position['avgPrice'][:10])
        market_price_now_bb_sem.append(position['markPrice'][:10])
        pnl_bb_sem.append(position['unrealisedPnl'][:5])
        open_time_bb_sem.append(datetime.fromtimestamp(int(position['createdTime']) if int(position['createdTime']) <= 1e12 else (int(position['createdTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))
        edit_time_bb_sem.append(datetime.fromtimestamp(int(position['updatedTime']) if int(position['updatedTime']) <= 1e12 else (int(position['updatedTime']) / 1000), tz=vladivostok_tz).strftime("%Y.%m.%d %H:%M"))

    bb = []
    bb.append([symbols_now_bb_vic, order_volume_bb_vic, buy_price_bb_vic, market_price_now_bb_vic, pnl_bb_vic, open_time_bb_vic, edit_time_bb_vic])
    bb.append([symbols_now_bb_sem, order_volume_bb_sem, buy_price_bb_sem, market_price_now_bb_sem, pnl_bb_sem, open_time_bb_sem, edit_time_bb_sem])
    okx = []
    okx.append([symbols_now_okx_vic, order_volume_okx_vic, buy_price_okx_vic, market_price_now_okx_vic, pnl_okx_vic, open_time_okx_vic, edit_time_okx_vic])
    okx.append([symbols_now_okx_sem, order_volume_okx_sem, buy_price_okx_sem, market_price_now_okx_sem, pnl_okx_sem, open_time_okx_sem, edit_time_okx_sem])
    all = str([bb, okx])

    balance_info = session.get_wallet_balance(accountType='UNIFIED', recv_window=10000,timeout=30)  # Increased timeout to 30 seconds
    balance_info2 = session_sem.get_wallet_balance(accountType='UNIFIED', recv_window=10000,timeout=30)  # Increased timeout to 30 seconds

    mama = balance_info['result']['list'][0]
    mama2 = balance_info2['result']['list'][0]
    mama3 = result_okx['details'][0]
    mama4 = result_okx_sem['details'][0]

    # Process balances and other metrics
    total_usd_summ = round(float(mama['totalEquity']), 2)
    total_usd_summ2 = round(float(mama2['totalEquity']), 2)
    total_usd_summ3 = round(float(result_okx['totalEq'].replace(',', '').replace(' ', '').replace('\xa0', '')))
    total_usd_summ4 = round(float(result_okx_sem['totalEq'].replace(',', '').replace(' ', '').replace('\xa0', '')))

    pl = round(float(mama['totalPerpUPL']), 3)
    pl2 = round(float(mama2['totalPerpUPL']), 3)
    pl3 = round(float(mama3['upl']), 3)
    pl4 = round(float(mama4['upl']), 3)


    return f'{int(round(total_usd_summ + (abs(pl if pl < 0 else pl)), 2))};{int(round(total_usd_summ2 + (abs(pl2 if pl2 < 0 else pl2)), 2))};{int(round((total_usd_summ3 + (abs(pl3 if pl3 < 0 else 0))), 2))};{int(round((total_usd_summ4 + (abs(pl4 if pl4 < 0 else 0))), 2))};{all}'


app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return main()
    except Exception as e:
        print(e)
        return str(e)

app.run(host='0.0.0.0', port=8080)
