import pip
pip.main(['install', 'beautifulsoup4'])
pip.main(['install', 'requests'])
pip.main(['install', 'lxml'])
import bs4
import requests
import easygui as eg

#ALL RESULTS COMING FROM WORLDOMETERS.INFO/coronavirus

def gt(a): # Get total cases and deaths
    stats=[]

    soup=bs4.BeautifulSoup(a.text, "lxml") #into bs4 for parsing
    for i in soup.find_all('div',class_='maincounter-number'): #find title tag in HTML
        number= i.span.text
        stats.append(number)
    cases=stats[0]
    deaths=stats[1]
    recovered=stats[2]

    activecase=soup.find('div',class_="number-table-main")
    active=activecase.text
    return cases,deaths,recovered,active

#Country info (might take a while)
def getcountry(a):
    soup=bs4.BeautifulSoup(a.text,'lxml')
    i=soup.find('table')
    n=0


    trows=i.find_all('tr') #all table rows
    trep=[]
    for tr in trows:
        td=tr.find_all('td') #all table data values
        row=[i.text for i in td] #list of all td in one table row
        try:
            if row[0]!="":
                trep.append(row)
        except:print("",end="")
    n=0
    countries=[] #countries with all stats
    country=[] #single country
    for i in trep:
        count=[]
        count.append(trep[n][1])
        country.append(trep[n][1])
        if trep[n][2]=="":
            count.append("Total Cases: N/A")
        else:
            count.append("Total Cases: "+trep[n][2])

        if trep[n][3]=="":
            count.append("New Cases Today: N/A")
        else:
            count.append("New Cases Today: "+trep[n][3])

        if trep[n][4]=="":
            count.append("Total Deaths: N/A")
        else:
            count.append("Total Deaths: "+trep[n][4])

        if trep[n][6]=="":
            count.append("Total Recovered: N/A")
        else:
            count.append("Total Recovered: "+trep[n][6])

        countries.append(count)
        n+=1
    return countries,country

res = requests.get("https://www.worldometers.info/coronavirus/")

c,d,r,a=gt(res)
Countrystats,country=getcountry(res)
country=sorted(country)
Countrystats=sorted(Countrystats)
space=c.find(" ")
c=c[:space]

Cases="Cases: "+ c
Deaths="Deaths: "+ d
Recovered="Recovered: "+r
Active="Active Cases: "+a

a=0
while a==0:
    c,d,r,a=gt(res)
    Countrystats,country=getcountry(res)
    country=sorted(country)
    Countrystats=sorted(Countrystats)
    space=c.find(" ")
    c=c[:space]

    Cases="Cases: "+ c
    Deaths="Deaths: "+ d
    Recovered="Recovered: "+r
    Active="Active Cases: "+a
    b=0
    while b==0:
        choice=eg.buttonbox("COVID-19 STATS (provided by worldometers)", "COVID STATS",["Quit","Start"])
        while choice==None or choice=="Quit":
            quit()
            break
        while choice=="Start":
            yo=eg.choicebox("Worldwide COVID-19 stats:"+"\n"+Cases+"\n"+Deaths+"\n"+Recovered+"\n"+Active+"\n","COVID STATS",country)
            if yo not in country:
                choice==""
                break
            if yo in country:
                yo=country.index(yo)
                con=eg.choicebox(str(country[yo]),"COVID STATS",Countrystats[yo])
                if con==None:
                    yo=""
