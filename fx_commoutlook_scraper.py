# Name   : fx_commoutlook_scraper.py
# Author : Steve Armstrong  (github.com/sacbnc) 
# Date   : Sep 2016
# Columns: symbol, short_value, short_volume, long_value, long_volume, 
#          average_short, average_long, interest
 
import sys
import lxml.html
import requests
from BeautifulSoup import BeautifulSoup

min_lots = 100

def scrape(min_lots):
	url  = 'http://www.myfxbook.com/community/outlook'
	doc  = requests.get(url)#, proxies=proxies)
	soup = BeautifulSoup(doc.text)
	root = lxml.html.fromstring(doc.text)
	
	# get list of all input ids
	all_id_inputs = root.xpath("//input[starts-with(@id,'outlookTip')]/@id")
	
	for id in all_id_inputs:
		# populate string with current id
		xpath_value = '//*[@id="{}"]/@value'.format(id)
		table_value = root.xpath(xpath_value)
		root_table  = lxml.html.fromstring(table_value[0])
		
		# reference 0th of element of all derived xpath variables
		# as a single element list is returned
		symbol = root_table.xpath("//table/tr[1]/td[1]/text()")[0]
		
		short_value =  root_table.xpath("//table/tr[2]/td[2]/text()")[0]
		short_volume = root_table.xpath("//table/tr[2]/td[3]/text()")[0].split(' ')[0]
		
		long_value =  root_table.xpath("//table/tr[3]/td[2]/text()")[0]
		long_volume = root_table.xpath("//table/tr[3]/td[3]/text()")[0].split(' ')[0]
		
		if float(short_volume) < min_lots and float(long_volume) < min_lots: continue
		
		interest = root_table.xpath("//div/text()")[1].split(' ')[0]
		average_short = soup.find(id="shortPriceCell" + symbol).string
		average_long  = soup.find(id="longPriceCell" + symbol).string

		print symbol       + "," + short_value   + "," + \
			  short_volume + "," + long_value    + "," + \
			  long_volume  + "," + average_short + "," + \
			  average_long + "," + interest

# If not inputs from user (arv length is 1 by default) then use default min_lots
if len(sys.argv) == 1:
    scrape(min_lots)
# If parameter received then parse as integer and use it as min_lots
elif len(sys.argv) == 2:
    scrape(int(sys.argv[1]))
    
    

    


