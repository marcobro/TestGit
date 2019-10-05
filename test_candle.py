import matplotlib
from matplotlib import style
import stockreader
import matplotlib.dates as mdates
import matplotlib.ticker as mtikcer
from matplotlib.finance import candlestick_ohlc

style.use('seaborn-talk')

fig = plt.figure()
ax1 = plt.subplot2grid((2,2), (0,0))
ax2 = plt.subplot2grid((2,2), (0,1))
ax3 = plt.subplot2grid((2,2), (1,0), colspan=2)

def drawStockTrend(compcode):
    global ax1, ax2
    
    ref_price = 1250000
    date, closep, high, low, openp, volume = stockreader.getStockData(compcode, '1y')
    
    ax1.plot([],[], linewidth = 5, label = '이익', color = 'r', alpha = 0.5)
    ax1.plot([],[], linewidth = 5, label = '손해', color = 'b', alpha = 0.5)
    ax1.fill_between(date, closep, ref_price, where = (closep > ref_price),
                                                         facecolr = 'r', alpha = 0.5)
    ax1.fill_between(date, closep, ref_price, where = (closep < ref_price),
                                                         facecolor = 'b', alpha = 0.5)
    ax1.spines['left'].set_color('c')
    ax1.spines['left'].set_linewidth(5)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_vsible(False)
    ax1.plot_date(date, closep, '-', color = 'b')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1.tick_params(axis = 'x', colors = 'r')
    ax1.tick_params(axis = 'y', colors = '#225588')
    ax1.grid(True)
    
    ohlc = []
    for i in range(len(date)):
        stock_data = date[i], openp[i], high[i], low[i], closep[i], volume[i]
        ohlc.append(stock_data)
        
    candlestick_ohlc(ax2, ohlc, width=0.5, colorup='r', colordown='b')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(10))
    
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax2.grid(True)
    
compcode = '005930'
drawStockTrend(compcode)
plt.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.9, wspace=0.5, hspace=0.5)
plt.show()
        