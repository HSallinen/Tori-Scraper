import requests
from bs4 import BeautifulSoup
import datetime
import json
from sanakirja import sanakirja
def toriScraper(productName, priceMin, priceMax, etäisyys, kaupunki):
    runWait=30

    today=datetime.date.today()
    #tämä joskus featureksi siten, että käyttäjä voi itse inputaa kuinka vanhoja tuloksia maksimissaan haluaa
    latest="3 päivää sitten"
    if latest and "päivä" in latest:
        if latest.split(" ")[0] == "päivä":
            daysToAdd=1
        else:
            daysToAdd=float(latest.split(" ")[0])
        latest=today - datetime.timedelta(days=daysToAdd)

    productNameFixed=str(productName).lower().split(" ")
    product=""
    plus=len(productNameFixed)
    no_plus=1
    for word in productNameFixed:
        no_plus+=1
        product+=word.strip()
        if plus>=no_plus:
            product+="+"

    #Tänä osa on sitä varten, jos joskus halutaan, että ohjelma hakee VAIN läheltä torista. ilman tätä käy koko suomen läpi
    #givenLocation=str(input()).lower() 
    #givenLocation=""

    #locationsDict={
    #    "ahvenanmaa":"0.100015",
    #    "etelä-karjala":"0.100014",
    #    "etelä-pohjanmaa":"0.100006",
    #    "etelä-savo":"0.100013",
    #    "kainuu":"0.100003",
    #    "keski-pohjanmaa":"0.100004",
    #    "keski-suomi":"0.100007",
    #    "kymenlaakso":"0.100020",
    #    "lappi":"0.100001",
    #    "pirkanmaa":"0.100011",
    #    "pohjanmaa":"0.100005",
    #    "pohjois-karjala":"0.100009",
    #    "pohjois-pohjanmaa":"0.100002",
    #    "pohjois-savo":"0.100008",
    #    "päijät-häme":"0.100012",
    #    "satakunta":"0.100010",
    #    "uusimaa":"0.100018",
    #    "varsinais-suomi":"0.100016"
    #}
    #if givenLocation:
    #    location=locationsDict[givenLocation]
    #    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?location={location}&q={product}&sort=PUBLISHED_DESC")
    #    print(f"https://www.tori.fi/recommerce/forsale/search?location={location}&q={product}&sort=PUBLISHED_DESC")
    #else:
    #    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")
    #    print(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")

    allCities=sanakirja[kaupunki]
    allowedCities=[]
    for city in allCities:
        if city[1]<=etäisyys:
            allowedCities.append(city[0].lower())
    print(allowedCities)

    foundListings=[]

    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")
    print(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")

    if page.status_code==200:
        page=page.content
        parsedPage=BeautifulSoup(page, 'html.parser')
        announcements=parsedPage.find('div', attrs={'class':'grid grid-cols-2 md:grid-cols-3 grid-flow-row-dense gap-16 items-start sf-result-list mt-16'})
        sales=announcements.find_all('article')

        for sale in sales:
            link=str(sale.find('a', attrs={'class':'sf-search-ad-link s-text! hover:no-underline'})).split("href")[1].split(">")[0].replace("href","").replace('"','').split("=")[1].replace(" id","")
            if "paalupaikka" in str(sale.find('span', attrs={'class':'absolute top-0 left-0 pointer-events-none badge--positionTL badge--info'})).lower():
                continue
            name=str(sale.find('a')).split("</span>")[-1].replace("</a>","")
            if "ostetaan" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                continue
            elif "annetaan" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                price=0
            elif "myydään" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                continue
            else:
                price=int(str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("\xa0","").replace("</span>","").replace("</div>","").replace("€","").strip())
            when=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[0].replace("<span>","").replace('<div class="text-s s-text-subtle mx-16 mt-8">','')
            place=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[2].replace("<span>","").split(",")[0].lower()
            if place not in allowedCities:
                continue
            if latest:
                if "päivä" in when:
                    if when.split(" ")[0] == "päivä":
                        when=today-datetime.timedelta(days=1)
                    else:
                        daysToAdd=float(when.split(" ")[0])
                        when=today-datetime.timedelta(days=daysToAdd)
                    if latest>when:
                        return foundListings
            else:
                if "minuutti" in when:
                    if "minuutti" in when.split(" ")[0]:
                        time=1
                    else:
                        time=int(when.split(" ")[0])
                    if time>runWait*2:
                        return foundListings
                else:
                    return foundListings
            if price<=priceMax and price >= priceMin:
                print(name)
                print(price)
                print(place)
                print(when)
                dataOfProduct=f"nimi: {name}, hinta: {price}, paikka: {place}, milloin: {when}, linkki: {link}"
                foundListings.append(dataOfProduct)
        pages=parsedPage.find('nav', attrs={'class':'flex items-center justify-center p-8 mt-24'})
        pages=pages.find('div',attrs={'class':'hidden md:block s-text-link'})
        pages=str(pages).count("Sivu")
        if pages:
            for whichPage in range (2,51):

                #if givenLocation:
                #    location=locationsDict[givenLocation]
                #    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?location={location}&page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                #    print(f"https://www.tori.fi/recommerce/forsale/search?location={location}&page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                #else:
                #    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                #    print(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")

                page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                print(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")

                if page.status_code==200:
                    page=page.content
                    parsedPage=BeautifulSoup(page, 'html.parser')

                    announcements=parsedPage.find('div', attrs={'class':'grid grid-cols-2 md:grid-cols-3 grid-flow-row-dense gap-16 items-start sf-result-list mt-16'})
                    sales=announcements.find_all('article')
                    for sale in sales:
                        link=str(sale.find('a', attrs={'class':'sf-search-ad-link s-text! hover:no-underline'})).split("href")[1].split(">")[0].replace("href","").replace('"','').split("=")[1].replace(" id","")
                        if "paalupaikka" in str(sale.find('span', attrs={'class':'absolute top-0 left-0 pointer-events-none badge--positionTL badge--info'})).lower():
                            continue
                        name=str(sale.find('a')).split("</span>")[-1].replace("</a>","")
                        if "ostetaan" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                            continue
                        elif "annetaan" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                            price=0
                        elif "myydään" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                            continue
                        else:
                            price=int(str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("\xa0","").replace("</span>","").replace("</div>","").replace("€","").strip())
                        when=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[0].replace("<span>","").replace('<div class="text-s s-text-subtle mx-16 mt-8">','')
                        place=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[2].replace("<span>","").split(",")[0].lower()
                        if not place in allowedCities:
                            continue
                        if latest:
                            if "päivä" in when:
                                if when.split(" ")[0] == "päivä":
                                    when=today-datetime.timedelta(days=1)
                                else:
                                    daysToAdd=float(when.split(" ")[0])
                                    when=today-datetime.timedelta(days=daysToAdd)
                                if latest>when:
                                    print(foundListings)
                                    return foundListings
                        else:
                            if "minuutti" in when:
                                if "minuutti" in when.split(" ")[0]:
                                    time=1
                                time=int(when.split(" ")[0])
                                if time>runWait*2:
                                    return foundListings
                            else:
                                return foundListings
                        if  price<=priceMax and price >= priceMin:
                            print(name)
                            print(price)
                            print(place)
                            print(when)
                            dataOfProduct=f"nimi: {name}, hinta: {price}, paikka: {place}, milloin: {when}, linkki: {link}"
                            foundListings.append([name, price, place, when, link])
                    pages=parsedPage.find('nav', attrs={'class':'flex items-center justify-center p-8 mt-24'})
                    pages=pages.find('div',attrs={'class':'hidden md:block s-text-link'})
                    if not f"Sivu {whichPage+1}" in str(pages):
                        print(foundListings)
                        return foundListings
