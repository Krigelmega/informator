
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from pybit.unified_trading import HTTP
import okx.Account as Account
import concurrent.futures
from threading import Thread


api_key = 'UIVxrdbrHubkUoumq3'
api_secret = 'fCr4EFilGlH2EWwSq1L30fOQ4mlSXjcPgPcY'
api_key2 = 'xtyMkrnsXPEO5bqNUW'
api_secret2 = 'GkiyJTLXAy9yNt31JLdpEl5whsqqDtgV4H8k'

def main():
    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret, recv_window=10000)
    session_sem = HTTP(testnet=False, api_key=api_key2, api_secret=api_secret2, recv_window=10000)
    api_key3 = "1a99a7d8-2a20-4b60-8fc4-23533c4c1944"
    secret_key3 = "394FEE3C7EACBE51680896451B139187"
    passphrase3 = "784512Zz."
    api_key4 = '227f1809-f195-430d-bfad-9d3cc4d1d20a'
    secret_key4 = 'D9D9AAD31266397B1CBA40CBDB521778'
    passphrase4 = '>y]3SrrE64xzd/=Eb/d8Wospk'
    flag = "0"  # live trading: 0, demo trading: 1
    accountAPI = Account.AccountAPI(api_key3, secret_key3, passphrase3, False, flag)
    accountAPI_sem = Account.AccountAPI(api_key4, secret_key4, passphrase4, False, flag)
    result = accountAPI.get_account_balance()
    print(result)
    result_sem = accountAPI_sem.get_account_balance()
    print(result_sem)
    result_okx = result['data'][0]
    #result_okx_sem = result_sem['data'][0]

    def get_balance(session):
        return session.get_wallet_balance(accountType='UNIFIED', recv_window=10000,
                                          timeout=30)  # Increased timeout to 30 seconds

    def fetch_balance_info():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Running both API calls concurrently
            futures = [executor.submit(get_balance, session), executor.submit(get_balance, session_sem)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results

    # Fetch balance info concurrently
    balance_info = fetch_balance_info()

    # Extracting the relevant data for each account
    all_info_balance = balance_info[1]
    all_info_balance2 = balance_info[0]

    mama = all_info_balance['result']['list'][0]
    mama2 = all_info_balance2['result']['list'][0]
    mama3 = result_okx['details'][0]
    #mama4 = result_okx_sem['details'][0]

    # Process balances and other metrics
    total_usd_summ = round(float(mama['totalEquity']), 2)
    total_usd_summ2 = round(float(mama2['totalEquity']), 2)
    total_usd_summ3 = round(float(result_okx['totalEq'].replace(',', '').replace(' ', '').replace('\xa0', '')))
    #total_usd_summ4 = round(float(result_okx_sem['totalEq'].replace(',', '').replace(' ', '').replace('\xa0', '')))

    pl = round(float(mama['totalPerpUPL']), 3)
    pl2 = round(float(mama2['totalPerpUPL']), 3)
    pl3 = round(float(mama3['upl']), 3)
    #pl4 = round(float(mama4['upl']), 3)


    return (round(total_usd_summ + (abs(pl if pl < 0 else 0)), 2),
            round(total_usd_summ2 + (abs(pl2 if pl2 < 0 else 0)), 2),
            round((total_usd_summ3 + (abs(pl3 if pl3 < 0 else 0))), 2),)
            #round((total_usd_summ4 + (abs(pl4 if pl4 < 0 else 0))), 2)


app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return main()
    except:
        return 'None'
def mainn():
    app.run(host='0.0.0.0', port=8080)
t = Thread (target=mainn)
t.start()
