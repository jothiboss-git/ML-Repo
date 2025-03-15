from quixstreams import State
from config import settings
from loguru import logger
import numpy as np
from talib import stream
from typing import Dict , List


MAX_CANDLE_IN_STATE = settings.max_candle_in_state
#max_candle_in_state: Maximum number of candles can keep in the state
def same_window(new_candle: dict, last_candle: dict) -> bool:
    """
      Check if the new candle  the last candle are in the same window
      Args:
        new_candle: dict
        last_candle: dict

      Returns:
        True if the new candle is in the same window as the last candle, False otherwise
    """
    return (new_candle['windows_start'] == last_candle['windows_start'] and
            new_candle['windows_end'] == last_candle['windows_end'] and 
            new_candle['pair'] == last_candle['pair'])

def update_candle(
    
    candle: dict, 
    state: State,
    
)->dict:
        """"
          Update the list of candles we have in our state with lastest candle
          if the latest  candle corresponds to the new window and the total number of candles in the list is less than the number of candles in the state, we just append it to the list
          if the latest candle corresponds to the last window, we replace the oldest candle in the list with the new one

          Args:
            candle: latest candle
            state: State of our application
            

          Returns:
            None
          
        """
        #Get the list of candles from the state
        candles= state.get('candles', default=[])

        
        if len(candles) == 0:
            candles.append(candle)
        #If the latest candle corresponds to the new window, we just append it to the list
        elif same_window(candle, candles[-1]):
            candles.append(candle)
        else:
            #If the latest candle corresponds to the last window, we replace the oldest candle in the list with the new one
            candles[-1] = candle    

        #If the total number of candles in the list is greater than the number of candles in the state, we just remove the oldest candle
        if len(candles) > MAX_CANDLE_IN_STATE:
            candles.pop(0)

        #We should check the candle have no missing window
    #this can happen for low volume pairs and we could inpterpolate the missing windows

        #print the list of candles
        logger.debug(f"number of Candles in the state: {len(candles)}")
        #Update the state with the new list of candles
        state.set('candles', candles)

        return candle

def compute_technical_indicators(
    
     candle: dict, 
     state: State,
) -> dict:
    """
    Compute technical indicators from the given candle data.
    """
    # Ensure candle is a dictionary
   # if not isinstance(candle, dict):
    #    logger.error(f"Invalid candle format: expected dict, got {type(candle)}")
     #   return {"error": "Invalid candle format"}

    # Retrieve candles from state and ensure it's a list
     #Get the list of candles from the state
    candles= state.get('candles', default=[])  # If 'candles' is missing, default to an empty list
    
    #breakpoint()
    if not candles:  # Ensure we have data before computing indicators
        return {**candle, "error": "No candle data available"}

    # Ensure we're working with valid candle data
    try:
        # Extract OHLCV data and convert to numpy arrays
        lows = np.array([c['low'] for c in candles], dtype=float)
        highs = np.array([c['high'] for c in candles], dtype=float)
        opens = np.array([c['open'] for c in candles], dtype=float)
        closes = np.array([c['close'] for c in candles], dtype=float)
        volumes = np.array([c['volume'] for c in candles], dtype=float)
    except (KeyError, TypeError) as e:
        logger.error(f"Error processing candle data: {e}")
        return {**candle, "error": "Invalid candle data format"}

    # Ensure arrays are not empty before applying indicators
   # if len(closes) < 50:  # Some indicators require a minimum number of candles
    #    return {**candle, "error": "Insufficient data for indicators"}

    # Dictionary to store indicators
    indicators = {}

    # 1. RSI - Measures momentum and identifies overbought/oversold conditions
    indicators['rsi_9'] = stream.RSI(closes, timeperiod=9)
    indicators['rsi_14'] = stream.RSI(closes, timeperiod=14)
    indicators['rsi_21'] = stream.RSI(closes, timeperiod=21)

    # 2. MACD - Identifies trend direction and strength
    indicators['macd'], indicators['macd_signal'], indicators['macd_hist'] = stream.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    

    # 3. Bollinger Bands (BBANDS) - Measures price volatility
    indicators['upper_bb'], indicators['middle_bb'], indicators['lower_bb'] = stream.BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2)
    

    # 4. Exponential Moving Average (EMA) - A moving average that gives more weight to recent prices
    indicators['ema_9'] = stream.EMA(closes, timeperiod=9)

    # 5. Simple Moving Average (SMA) - A basic moving average for smoothing price data
    indicators['sma_5'] = stream.SMA(closes, timeperiod=5)
    indicators['sma_10'] = stream.SMA(closes, timeperiod=10)
    indicators['sma_20'] = stream.SMA(closes, timeperiod=20)
    indicators['sma_50'] = stream.SMA(closes, timeperiod=50)

    # 6. Commodity Channel Index (CCI) - Measures price deviation from its average
    indicators['cci_14'] = stream.CCI(highs, lows, closes, timeperiod=14)

    # 7. Average True Range (ATR) - Measures market volatility
    indicators['atr_14'] = stream.ATR(highs, lows, closes, timeperiod=14)

    # 8. Stochastic Oscillator (%K and %D) - Identifies overbought and oversold levels
    indicators['stoch_k'], indicators['stoch_d'] = stream.STOCH(highs, lows, closes, fastk_period=14, slowk_period=3, slowd_period=3)
    

    # 9. Rate of Change (ROC) - Measures momentum
    indicators['roc_12'] = stream.ROC(closes, timeperiod=12)

    # 10. Parabolic SAR (SAR) - Identifies potential trend reversals
    indicators['sar'] = stream.SAR(highs, lows, acceleration=0.02, maximum=0.2)

    #breakpoint()

    # Return the indicators along with the latest candle data
    return {**candle, **indicators}  # Merge the original candle dict with the indicators dict
   
    
    
        
