
#   Date :  Fri June 24 2022 18:44:38 GMT+0530 (India Standard Time)
#   Author : Suman Gurung
#   Description : server created using flask that scrape (webscrape) data from a website (ecampus) that requires login


from flask import jsonify,Flask,render_template,url_for,request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def hello():
    return "Flask"


@app.route('/login',methods=['GET','POST'])
def login():

    output = request.get_json()

    student = {}

    user = output['registration']
    pwd = output['password']

    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

    login = {"__LASTFOCUS":"", 
    "__EVENTTARGET":"",
    "__EVENTARGUMENT":"",
    "__VIEWSTATE":"/wEPDwULLTE5OTQxMDI0NjAPZBYCAgMPZBYEAgcPDxYCHgdWaXNpYmxlaGRkAg8PDxYGHgRUZXh0BQZTaWduaW4eBVdpZHRoGwAAAAAAAFlAAQAAAB4EXyFTQgKAAmRkZDKOds53WytBv8xci5XgxKGRNp3PIEQTISB4q7VSEjb3",
    "__VIEWSTATEGENERATOR":"29EDAEC7",
    "__EVENTVALIDATION":"/wEdAAYgaLyRoW+/TSI/G20zAv3IEHX99fbNOkB7jDZxhdx2HMKuxa9nriHe9jO7RhlVlprZLo06Fl6DYP/kYTXPzdB2op4oRunf14dz2Zt2+QKDEHXoT2A5OSqQSW0XQ3USDjET3Hu0lvxHjsiQVlwXXRZbAkDo9JWYcKHqeAUdl5pPMg==",
    "TxtUserName": user,
    "TxtPassword": pwd,
    "btnLogin": "Sign in"
    }

    with requests.Session() as s:
    	url ="https://ecm.smtech.in/ecm/"
    	page = s.post(url,data=login ,headers=headers)
    
    print(page)
    
    content = page.content

    # print(content)
    soup = BeautifulSoup(content,"html.parser")

    # print(soup)
    info = soup.find(class_="panel panel-default")

    detail = []

    if info!=None:
        for text in info.find_all('span'):
            detail.append(text.get_text())

        while("" in detail) :
            detail.remove("")

        student["name"]=detail[0]
        student["course"]=detail[1]
        student["sem"]=detail[2]
        student["section"]=detail[3]
        student["tg"]=detail[4]
        student["tgphno"]=detail[5]
        student["status"]=1

        record = []

        subject = soup.find(id="ctl00_ContentPlaceHolder1_gvRecord")

        if subject!=None:
            for sub in subject.find_all('td'):
                record.append(sub.get_text())

        attendance = []

        for i in range(len(record)):
            if i>14:    #to remove table head
                record[i] = record[i].replace(u'\xa0', u'')   #to remove \xa0
                attendance.append(record[i])

        attendance_record = {}

        no_of_subject = int(len(attendance)/13);

        for i in range(no_of_subject):
            attendance_record[attendance[(i*13)+0]] = {
                "totalclass":attendance[(i*13)+1],
                "present":attendance[(i*13)+2],
                "percentage":attendance[(i*13)+3],
                "quiz1":attendance[(i*13)+4],
                "sessional1":attendance[(i*13)+6],
                "quiz2":attendance[(i*13)+7],
                "sessional2":attendance[(i*13)+9],
                "assignment":attendance[(i*13)+10],
                "att_mark":attendance[(i*13)+11],
            }

        student["att_detail"] = attendance_record 

        student = json.dumps(student)

        return student
    else:
        return {"status":0,"message":"Invalid Login Input"}



if __name__ == "__main__":
    app.run(debug=True)
