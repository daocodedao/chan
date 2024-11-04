# import 路径修改
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.logger_settings import api_logger



# 策略运行前要加
    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")
    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpeRatio') # 夏普比率


# results = cerebro.run() 
def printResultTotal( results, initCash=1000000, endCash=0, endValue=0, resultDidct={}):
    strat = results[0]
    # https://zhuanlan.zhihu.com/p/98775974
    

    resultDidct['初始金额'] =  initCash
    resultDidct['期末现金'] =  endCash
    resultDidct['期末股票'] =  endValue - endCash
    resultDidct['期末总市值'] =  endValue


    if strat.analyzers.trades:
        trades = strat.analyzers.trades.get_analysis()
        if trades.total.total != 0 and "open" in trades.total.keys() and "closed" in trades.total.keys():
            total = trades.total.open + trades.total.closed
            winners = trades.won.total
            losers = trades.lost.total

            win_rate = (winners / total) * 100 if total != 0 else 0
            resultDidct['交易[总次数]'] = total
            resultDidct['交易[盈利次数]'] =  winners
            resultDidct['交易[亏损次数]'] =  losers
            resultDidct['交易[胜率]'] =  f"{win_rate:.2f}%"

            # net_total_pnl = trades['pnl']['net']['total']
            # net_average_pnl = trades['pnl']['net']['average']
            # resultDidct['总交易[盈利/亏损]'] =  f"{net_total_pnl:.2f}"
            # resultDidct['平均每笔交易[盈利/亏损]'] =  f"{net_average_pnl:.2f}"

            net_total_pnl = trades['pnl']['net']['total']
            gross_total_pnl = trades['pnl']['gross']['total']
            net_average_pnl = trades['pnl']['net']['average']
            gross_average_pnl = trades['pnl']['gross']['average']
            
            resultDidct['总交易[盈利/亏损]'] =  f"{net_total_pnl:.2f}"
            resultDidct['总交易[盈利/亏损]（未计手续费）'] =  f"{gross_total_pnl:.2f}"
            resultDidct['平均每笔交易[盈利/亏损]'] =  f"{net_average_pnl:.2f}"
            resultDidct['平均每笔交易[盈利/亏损]（未计手续费）'] =  f"{gross_average_pnl:.2f}"



    if strat.analyzers.drawdown:
        drawdown = strat.analyzers.drawdown.get_analysis()
        if  drawdown:
            max_drawdown = drawdown['max']['drawdown']
            resultDidct['最大回撤%'] =  f"{max_drawdown:.2f}%"
            resultDidct['最大回撤后金额'] =  f"{(1-max_drawdown/100)*initCash:.2f}"
            resultDidct['最大回撤金额'] =  f"{(max_drawdown/100)*initCash:.2f}"


    if strat.analyzers.sharpeRatio:
        sharpReturn = strat.analyzers.sharpeRatio.get_analysis()
        # api_logger.info(sharpReturn)
        if sharpReturn and sharpReturn['sharperatio']:
            resultDidct['夏普比率'] =  f"{sharpReturn['sharpeRatio']:.2f}"



    outResultStr = "\n----------------------------\n"
    for key, value in resultDidct.items():
        outResultStr = outResultStr + key + ": " + str(value) + "\n"


    api_logger.info(outResultStr)