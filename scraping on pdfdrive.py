import requests
from bs4 import BeautifulSoup

#the books name
sersh= input("enter the field or a key for the book : ")
print("---------------------------------------")
sersh = sersh.replace(' ', '+')
#initialisation on page and limits of pages
p_num = 1
limits = 30
#creation csv file with the head column
file = open(f"{sersh}_books_datasets.csv", 'w',encoding="utf-8")
header = "title,pages,year,size,downloads,languge,infos\n"
file.write(header)
#the attempt for faild connection
attmp = 0
while True:
    #get code source from url
    try :
        URL = f"https://www.pdfdrive.com/search?q={sersh}&pagecount=&pubyear=&searchin=&em=&page={p_num}"
        page = requests.get(URL)
    except :
        if attmp>10:
            break
        attmp+=1
        print("Connection faild !")
        pass
    #all books in page
    soup = BeautifulSoup(page.content, 'lxml')
    book = soup.find_all('div',{"class":"row"})
    #limits of pages
    pg = soup.find("div",{'class':'pagination'})
    
    try:
        limits = int(pg.find_all("li")[-2].text)
    except :
        pass
    
    if p_num>limits :
        break
    
    #extract title, pages, year, size, downloads, languge and infos.
    for i in range(len(book)):
        #title
        try:
            title = book[i].find("h2").text.strip().replace(",",".")
        except AttributeError:
            title = None
        
        try :
            info = book[i].find("div",{"class":"file-info"})
        except:
            pass
        #pages
        try :
            pages = info.find("span",{"class":"fi-pagecount"}).text.strip().replace(",","")
        except AttributeError:
            pages = None
        #year
        try :
            year = info.find("span", {"class":"fi-year"}).text.strip()
        except AttributeError:
            year = None
        #size
        try :
            size =  info.find("span", {"class":"fi-size hidemobile"}).text.strip().replace(",",".")
        except AttributeError:
            size = None
        #downloads
        try:
            downloads = info.find("span", {"class":"fi-hit"}).text.strip().replace(",","")
        except AttributeError:
            downloads = None
        #languge
        try:
            languge = info.find("span", {'class':"fi-lang"}).text.strip()
        except AttributeError:
            languge = None
            
        #the infos (exception)
        text_elements =book[i].find_all(text=True)
        text = [t.strip() for t in text_elements if t.parent.name not in ['style', 'script']]
        text = text[-3:-8:-1]
        infos=""
        for n in range(len(text)-1,-1,-1):
            infos = infos + text[n].replace('\n',' ') + " "
        infos = infos.strip().replace(",",".")

        #line data and saving in csv
        result = str(title)+','+str(pages)+','+str(year)+','+str(size)+','+str(downloads)+','+str(languge)+','+str(infos)+'\n'
        try :
            file.write(result)
        except:
            pass
    
    #next page
    print("next page",p_num,"/",limits)
    p_num+=1
    
#close the file
file.close()