from html import entities
import json
import requests
import bs4
import csv
import re

"""
TODO:
1. Deal with wrong course numbers
2.
"""
class Lesson:
    def __init__(self,proffesor,type,groupId,semester,days,hours,location) -> None:
        self._proffesor=proffesor
        self._type=type
        self._groupId=groupId
        self._semester=semester
        self._days=days
        self._hours=hours
        self._location=location
    
    def __str__(self) -> str:
        return f"Teacher : {self._proffesor}\n \
                Lesson type : {self._type}\n \
                Group Id : {self._groupId}\n \
                Semester : {self._semester}\n \
                Days : {self._days}\n \
                Hours : {self._hours}\n \
                Location : {self._location}\n"

    def toRow(self):
        return [self._proffesor,self._type,self._groupId,self._semester,self._days,self._hours,self._location]

def getCourseInfo(course_num):
    url='https://shnaton.huji.ac.il/index.php'
    headers={"Host": "shnaton.huji.ac.il",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": "&quot;Chromium&quot;;v=&quot;104&quot;, &quot; Not A;Brand&quot;;v=&quot;99&quot;, &quot;Microsoft Edge&quot;;v=&quot;104&quot;",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "&quot;Windows&quot;",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://shnaton.huji.ac.il",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://shnaton.huji.ac.il/index.php",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "he,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "Cookie": "PHPSESSID=60lt4gpmj2i092deu7tpaqlu87; TS012d2d50=01b025178ede9f7fc5ff302b002c3411cbf1b60aaa5407d01093dde96592ccf827d607fcfba525815b3f26f663265cd8b92195777b6cdab363d4e9bdb1c1d8fac756460ced; TS6368d62d027=082149a1b4ab2000ff08a509ca26f22bc4e74aa4569c73abeb74dacd9aae0d74ba0fdb18c16da14c0864a628fe1130005ffb9c5aae17d3edcf4ef4f515f7c7335f6fffb90d90b1b9773851c98d0ecfea64db061d00022ca6f6f1e977a6499b02"}
    req = "peula=Simple&maslul=0&shana=0&year=2023&course="
    response = requests.post(url=url,headers=headers,data=req + course_num)
    if response.status_code == 200:
        print(course_num)
    elif response.status_code == 404:
        # print('Not Found.')
        raise Exception("Not Found")
    return response.text

def parseData(html_text):
    soup = bs4.BeautifulSoup(html_text,'html.parser')
    main_table=soup.find('table',{'style':'margin-top:15px;','width':'850'})
    for i,table in enumerate(main_table.find_all('table')):
        if(i!=4):
            continue
        all_lessons=[]
        #comment section
        comments=table.find_all('tr')[-2:]

        #classes section last two rows in table are the comments
        for elem_tr in table.find_all('tr')[-3::-1]:

            row=elem_tr.find_all('td')
            regex=re.compile('\W^-+')

            if len(row)!=8:
                continue
            try:
                location=[item.text.replace(',','') for item in row[0].children]
            except IndexError:
                location=row[0].text.replace(',','')
            location=regex.sub('',str(location))

            try:
                location_type=[item.text.replace(',','') for item in row[1].children]
            except IndexError:
                location_type=row[1].text.replace(',','')
            location_type=regex.sub('',str(location_type))

            try:
                hours=[item.text.replace(',','') for item in row[2].children]
            except IndexError:
                hours=row[2].text.replace(',','')
            hours=regex.sub('',str(hours))


            try:
                day=[item.text.replace(',','') for item in row[3].children]
            except IndexError:
                day=row[3].text.replace(',','')
            day=regex.sub('',str(day))


            try:
                semester=[item.text.replace(',','') for item in row[4].children]
            except IndexError:
                semester=row[4].text.replace(',','')
            semester=regex.sub('',str(semester))

            
            group_id=row[5].text.replace(',','')
            group_id=regex.sub('',str(group_id))

            lesson_type=row[6].text.replace(',','')
            lesson_type=regex.sub('',str(lesson_type))

            proffeser=row[7].text.replace(',','')
            proffeser=regex.sub('',str(proffeser))

            lesson=Lesson(proffeser,lesson_type,group_id,semester,day,hours,location)
            print(lesson)
            
            all_lessons.append(lesson)
        # Finally write all rows
        print(all_lessons)
        with open(f'out{i}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([ls.toRow() for ls in all_lessons])


if __name__=="__main__":
    for course_num in range(80000,100000):
        html_text=getCourseInfo(str(course_num))
        parseData(html_text)





