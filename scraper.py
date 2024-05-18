import requests
from bs4 import BeautifulSoup
import datetime
import json
from sanakirja import sanakirja
def toriScraper(productName, priceMin, priceMax, etäisyys, kaupunki, timeSinceLastCheck):
    # TimeSinceLastCheck=0 means that this is a request made by frontend 
    # TimeSinceLastCheck should be in minutes and less than 60

    if timeSinceLastCheck==0:
        latest=3
        # This is a placeholder value
    else:
        # Set latest = 1 to only search for results from today
        latest=1
        
    # Make product name readable by tori search algorithm
    product=str(productName).lower().replace(" ", "+")

    # Check what cities products can be from
    allCities=sanakirja[kaupunki]
    allowedCities=[]
    for city in allCities:
        if city[1]<=etäisyys:
            allowedCities.append(city[0].lower())
    allowedCities.append(kaupunki)

    # Add to the end of link to include giving away type posts when 0€ is a valid price
    if priceMin<=0:
        freeIncludedLink="&trade_type=2"
    else:
        freeIncludedLink=""

    foundListings=[]

    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?price_from={priceMin}&price_to={priceMax}&published={latest}&q={product}&sort=PUBLISHED_DESC&trade_type=1{freeIncludedLink}")
    print(f"https://www.tori.fi/recommerce/forsale/search?price_from={priceMin}&published={latest}&price_to={priceMax}&q={product}&sort=PUBLISHED_DESC&trade_type=1{freeIncludedLink}")

    if page.status_code==200:
        page=page.content
        parsedPage=BeautifulSoup(page, 'html.parser')
        # Calculate how many pages are there
        pages=parsedPage.find('nav', attrs={'class':'flex items-center justify-center p-8 mt-24'})
        pages=pages.find('div',attrs={'class':'hidden md:block s-text-link'})
        pages=str(pages).count("Sivu")
        if pages:
            for whichPage in range (1,pages+1):
                # The first page is already loaded so we do not need to load it again
                if(whichPage!=1):
                    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?price_from={priceMin}&price_to={priceMax}&published={latest}&q={product}&sort=PUBLISHED_DESC&trade_type=1{freeIncludedLink}")
                    print(f"https://www.tori.fi/recommerce/forsale/search?price_from={priceMin}&price_to={priceMax}&published={latest}&q={product}&sort=PUBLISHED_DESC&trade_type=1{freeIncludedLink}")
                    if page.status_code==200:
                        page=page.content
                        parsedPage=BeautifulSoup(page, 'html.parser')
    
                announcements=parsedPage.find('div', attrs={'class':'grid grid-cols-2 md:grid-cols-3 grid-flow-row-dense gap-16 items-start sf-result-list mt-16'})
                sales=announcements.find_all('article')
                for sale in sales:
                    link=str(sale.find('a', attrs={'class':'sf-search-ad-link s-text! hover:no-underline'})).split("href")[1].split(">")[0].replace("href","").replace('"','').split("=")[1].replace(" id","")
                    # Don't include sales tagged paalupaikka. Later change this to include them only once
                    if "paalupaikka" in str(sale.find('span', attrs={'class':'absolute top-0 left-0 pointer-events-none badge--positionTL badge--info'})).lower():
                        continue
                    name=str(sale.find('a')).split("</span>")[-1].replace("</a>","")
                    # Set price of items that are being given away as free
                    if "annetaan" in str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","").replace("€","").strip().lower():
                        price=0
                    else:
                        price=int(str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("\xa0","").replace("</span>","").replace("</div>","").replace("€","").strip())
                    when=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[0].replace("<span>","").replace('<div class="text-s s-text-subtle mx-16 mt-8">','')
                    place=str(sale.find('div', attrs={'class':'text-s s-text-subtle mx-16 mt-8'})).split("</span>")[2].replace("<span>","").split(",")[0].lower()
                    
                    if not place in allowedCities:
                        continue

                    if timeSinceLastCheck!=0:
                        #check if post has been made since the last check
                        if "minuutti" in when:
                            if "minuutti" in when.split(" ")[0]:
                                time=1
                            else:
                                time=int(when.split(" ")[0])
                            if time>timeSinceLastCheck:
                                return foundListings
                        else:
                            return foundListings
                    foundListings.append([name, price, place, when, link])
            return foundListings
    return [["no pages found"]]
