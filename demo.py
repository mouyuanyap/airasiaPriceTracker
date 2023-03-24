import scrapy
import requests,re
import json,pprint,codecs
from datetime import datetime
import time,os
header = {'User-Agent':'Mozilla/5.0'}

try:
    os.mkdir('./result')
except:
    pass

##For KUL-PVG
# origin = r"KUL"
# destination = r"PVG"
# airline = r"D7"
# fnumber = r"330"
# flightNumber = r"{}-{}".format(airline,fnumber)
# # month = '03'
# # day = ['26','28','30']
# month = '04'
# day = ['02','04','06','09','11','13','16','18','20','23','25','27','30']

####################################

#For KUL-TPE
origin = r"KUL"
destination = r"TPE"
month = '04'
airline = r'D7'
fnumber = r'378'
flightNumber = r"{}-{}".format(airline,fnumber)
day = ['01','02','03','04','05','06','07','08','09','10']
for i in range(11,32):
    day.append(str(i))
####################################


for d in day:

    baseurl = 'https://www.airasia.com/flights/search/?origin={}&destination={}&departDate={}/{}/2023&tripType=O&adult=1&child=0&infant=0&locale=en-gb&currency=MYR&airlineProfile=all&type=paired&cabinClass=economy&upsellWidget=true&upsellPremiumFlatbedWidget=true&isOC=false&isDC=false&uce=false'.format(origin,destination,d,month)
    r = requests.get(baseurl, headers= header, timeout=10)
    r.raise_for_status()
    file = codecs.open("./webPageText_airasia_.txt", 'w',encoding= "UTF-8")
    file.write(r.text)
    # print(r'"tripId":(.*?)"sharedFlight":"'+origin+'-'+ destination + '-' + flightNumber +'",')
    results = re.findall(r'"tripId":(.*?)"sharedFlight":"(.*?)"',r.text)
    for res in results:
        if str(re.findall(r'"marketingFlightNumber":(.*?),',res[0])[0]) == fnumber and res[1] == "{}-{}-{}".format(origin,destination,flightNumber):
            result = res[0]
    
    fare = re.findall(r'"fare":{"adults":(.*?),',result)[0]
    seatAvailability = re.findall(r'"seatAvailability":{"seats":(.*?)},',result)[0]
    flightName = "{}-{}-{}".format(origin,destination,flightNumber)
    departureDate = re.findall(r'"departureTime":"(.*?)T.*?"',result)[0]


    print(flightName,departureDate,datetime.now(),fare, seatAvailability)
    try:
        file = codecs.open("./result/{}_{}.txt".format(flightName,departureDate), 'a',encoding= "UTF-8")

        file.write("{},{},{}\n".format(datetime.now(),fare, seatAvailability))
    except:
        pass

    time.sleep(1)