import yfinance as yf  # anything i use from yf is from this documentation https://yfinance-python.org



def get_stock_price(stock_symbol): 
    '''returns most current stock price'''
    stock =  yf.Ticker(stock_symbol)
    data = stock.history(period="1d")
    if not data.empty: 
        price = float(data['Close'].iloc[-1])
        price = round(price, 2)
        return price
    return None

def get_market_cap(stock_symbol):
    '''returns market cap from yfinance api'''
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    market_cap = info.get('marketCap')
    if market_cap:
        mc = float(market_cap) / 1_000_000_000
        mc = round(mc, 2)
    return None

def get_percent_change(stock_symbol):
    '''returns the percent change of stock price from today and yesterday's closing prices'''
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="2d")
    if len(data) >=2:
        yesterday = data['Close'].iloc[-2]
        today = data['Close'].iloc[-1]
        percent_change = ((today - yesterday) / yesterday) * 100
        percent_change = round(percent_change, 2)
        return percent_change

def format_price_change(percentage):
    '''adds an up arrow or down arrow based on positive/negative percent change'''
    if percentage is None: 
        return "N/A"
    
    if percentage > 0: 
        return f"↑ {percentage}%"
    elif percentage < 0: 
        return f"↓ {percentage}%"
    else:
        return f"0.00%"