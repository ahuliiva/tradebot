# tradebot

Telegram bot for notifying changes of trading instruments on Binance


#### /price
    enter Binance instrument symbol (i.e. BTCUSDT) to get it's price
    
    example:
    /price
    BTCUSDT

#### /watch
    enter {SYMBOL} {< or >} {price level}
    
    example:
    /watch
    BTCUSDT > 18000

    * watch stops after ~ 10 seconds, as far as it is not async yet
    * after stopping it is still available in /show_watches

#### /stop_watch
    enter instrument symbol to stop watching it

#### /show_watches
    shows all instruments you are watching


