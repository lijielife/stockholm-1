import dao
import re

from decimal import Decimal

risk_factor = 100

def find(account_value, filter):
  print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
  print "Symbol\tDate\tClose\tStop\tTarget\tShares\tPosition\tChart"
  print "-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
  for quote in dao.Quote.get_latest_quotes():
    if not re.search(filter, quote.symbol):
      continue
    if quote.is_above_20_day_high():
      
      if(quote.is_above_sma20() and quote.is_above_sma50()):
        #print "Above sma20 and sma50"
        chart = "http://finance.yahoo.com/echarts?s=%s" % quote.symbol
        #print "https://www.avanza.se/aza/sok/standard.jsp?word=%s" % (
        #    quote.symbol.replace('.ST', '').replace('-A', '').replace('-B', ''))

        stop = quote.get_indicator().calculate_stop(quote.close) #TODO add transaction cost
        risk = quote.close - stop
        target = risk * 6 + quote.close
        shares = dao.Position.get_shares(quote, account_value/risk_factor)
        position = long(shares * quote.close)
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (quote.symbol, quote.date, quote.close, stop, target, shares, position, chart)
        #chart = chart + "+" + quote.symbol
    else:
      #print "Leave %s " % quote.symbol
      pass
  print

print "AVANZA pension"
find(Decimal('48000'), '\.ST')

print "STOCKS"
find(Decimal('390000') / dao.Currency.get_rate('GBPSEK'), '\.ST')