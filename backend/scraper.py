import requests
from bs4 import BeautifulSoup

def multiple(m, n):
    return True if m % n == 0 else False

def toriScraper():
    #productName=str(input()).lower().split(" ")
    product="matto"
    #priceMax=str(input()).lower()
    #priceMin=str(input()).lower()
    #givenLocation=str(input()).lower()
    givenLocation=""

    locationsDict={
        "ahvenanmaa":"0.100015",
        "etelä-karjala":"0.100014",
        "etelä-pohjanmaa":"0.100006",
        "etelä-savo":"0.100013",
        "kainuu":"0.100003",
        "keski-pohjanmaa":"0.100004",
        "keski-suomi":"0.100007",
        "kymenlaakso":"0.100020",
        "lappi":"0.100001",
        "pirkanmaa":"0.100011",
        "pohjanmaa":"0.100005",
        "pohjois-karjala":"0.100009",
        "pohjois-pohjanmaa":"0.100002",
        "pohjois-savo":"0.100008",
        "päijät-häme":"0.100012",
        "satakunta":"0.100010",
        "uusimaa":"0.100018",
        "varsinais-suomi":"0.100016"
    }
    if givenLocation:
        location=locationsDict[givenLocation]
        page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?location={location}&q={product}&sort=PUBLISHED_DESC")
        print(f"https://www.tori.fi/recommerce/forsale/search?location={location}&q={product}&sort=PUBLISHED_DESC")
    else:
        page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")
        print(f"https://www.tori.fi/recommerce/forsale/search?q={product}&sort=PUBLISHED_DESC")
    if page.status_code==200:
        page=page.content
        parsedPage=BeautifulSoup(page, 'html.parser')
        announcements=parsedPage.find('div', attrs={'class':'grid grid-cols-2 md:grid-cols-3 grid-flow-row-dense gap-16 items-start sf-result-list mt-16'})
        sales=announcements.find_all('article')

        for sale in sales:
            name=str(sale.find('a')).split("</span>")[-1].replace("</a>","")
            price=str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","")
            print(name)
            print(price)

        pages=parsedPage.find('nav', attrs={'class':'flex items-center justify-center p-8 mt-24'})
        pages=pages.find('div',attrs={'class':'hidden md:block s-text-link'})
        pages=str(pages).count("Sivu")
        if pages:
            for whichPage in range (2,900):

                if givenLocation:
                    location=locationsDict[givenLocation]
                    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?location={location}&page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                    print(f"https://www.tori.fi/recommerce/forsale/search?location={location}&page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                else:
                    page=requests.get(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                    print(f"https://www.tori.fi/recommerce/forsale/search?page={whichPage}&q={product}&sort=PUBLISHED_DESC")
                if page.status_code==200:
                    page=page.content
                    parsedPage=BeautifulSoup(page, 'html.parser')

                    announcements=parsedPage.find('div', attrs={'class':'grid grid-cols-2 md:grid-cols-3 grid-flow-row-dense gap-16 items-start sf-result-list mt-16'})
                    sales=announcements.find_all('article')
                    for sale in sales:
                        name=str(sale.find('a')).split("</span>")[-1].replace("</a>","")
                        price=str(sale.find('div', attrs={'class':'mt-16 flex justify-between sm:mt-8 space-x-12 font-bold whitespace-nowrap'})).split("<span>")[-1].replace("</span>","").replace("</div>","")
                        print(name)
                        print(price)
                    pages=parsedPage.find('nav', attrs={'class':'flex items-center justify-center p-8 mt-24'})
                    pages=pages.find('div',attrs={'class':'hidden md:block s-text-link'})
                    if not f"Sivu {whichPage+1}" in str(pages):
                        break
                        
            
toriScraper()