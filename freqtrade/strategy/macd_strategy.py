import talib.abstract as ta
from pandas import DataFrame
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy


class_name = 'MACDStrategy'


class MACDStrategy(IStrategy):
    """
        MACD strategy
        author@: Marcin Zbijowski
        """

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "60": 0.01,
        "30": 0.03,
        "20": 0.04,
        "0": 0.05
    }

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.3

    # Optimal ticker interval for the strategy
    ticker_interval = 5

    def populate_indicators(self, dataframe: DataFrame):
        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # EMA - Exponential Moving Average
        # dataframe['ema3'] = ta.EMA(dataframe, timeperiod=3)
        # dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        # dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        # dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)

        print(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame):
        # print('BUY', dataframe['macdhist'] > 0, dataframe['macd'] > dataframe['macdsignal'])
        dataframe.loc[
            (
                (dataframe['macdhist'] > 0) &
                (dataframe['macd'] > dataframe['macdsignal'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame):
        dataframe.loc[
            (
                (dataframe['macdhist'] < 0) &
                (dataframe['macd'] < dataframe['macdsignal'])
            ),
            'sell'] = 1
        return dataframe