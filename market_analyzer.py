import pandas as pd
import yfinance as yf
from config import logger

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates the Relative Strength Index (RSI) using standard pandas rolling windows."""
    delta = series.diff()
    
    # Isolate positive and negative gains
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    
    # Calculate exponential moving averages
    avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_and_analyze_ticker(ticker_name: str) -> dict:
    """Downloads historical data from yfinance and calculates technical indicator summaries."""
    logger.info(f"Downloading historical ticker data for: '{ticker_name}'...")
    try:
        ticker = yf.Ticker(ticker_name)
        # Fetch 30 days of daily intervals
        df = ticker.history(period="1mo", interval="1d")
        
        if df.empty or len(df) < 20:
            logger.warning(f"Insufficient pricing historical points returned for ticker '{ticker_name}'")
            return {}
            
        close_prices = df["Close"]
        current_price = float(close_prices.iloc[-1])
        yesterday_price = float(close_prices.iloc[-2])
        
        # 1. Price Changes
        price_change = current_price - yesterday_price
        pct_change = (price_change / yesterday_price) * 100
        
        # 2. Simple Moving Average (SMA-20)
        sma_20_series = close_prices.rolling(window=20).mean()
        current_sma_20 = float(sma_20_series.iloc[-1])
        
        # 3. Relative Strength Index (RSI-14)
        rsi_series = calculate_rsi(close_prices, period=14)
        current_rsi = float(rsi_series.iloc[-1])
        
        logger.info(f"Successfully calculated indicators for {ticker_name} (Price: ${current_price:.2f} | RSI: {current_rsi:.1f})")
        
        return {
            "ticker": ticker_name,
            "current_price": round(current_price, 2),
            "pct_change": round(pct_change, 2),
            "sma_20": round(current_sma_20, 2),
            "rsi_14": round(current_rsi, 1),
            "high_24h": round(float(df["High"].iloc[-1]), 2),
            "low_24h": round(float(df["Low"].iloc[-1]), 2)
        }
    except Exception as e:
        logger.error(f"Critical error fetching technical analysis parameters for {ticker_name}: {str(e)}")
        return {}
