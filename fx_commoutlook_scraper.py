import sys
import lxml.html
import requests

min_lots = 100

def scrape(min_lots):
    url = 'http://www.myfxbook.com/community/outlook'
    doc = requests.get(url)#, proxies=proxies)
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
    
        print symbol + "," + short_value + "," + short_volume + "," + long_value + "," + long_volume + "," + interest

if len(sys.argv) == 1:
    scrape(min_lots)
elif len(sys.argv) == 2:
    scrape(int(sys.argv[1]))
    
    

    


