import requests
from bs4 import BeautifulSoup
import os
import hashlib
import datetime
import time
import smtplib
from email.message import EmailMessage


# loops indefinetly (uses timestop)
urls = {'Matan Aman': 'https://www.mitgaisim.idf.il/%D7%AA%D7%A4%D7%A7%D7%99%D7%93%D7%99%D7%9D/%D7%9E%D7%AA%D7%9F-%D7%90%D7%9E%D7%9F/',
        'Maslul Matan': 'https://www.mitgaisim.idf.il/%D7%AA%D7%A4%D7%A7%D7%99%D7%93%D7%99%D7%9D/%D7%9E%D7%A1%D7%9C%D7%95%D7%9C-%D7%9E%D7%AA%D7%9F/'}


while True:
    for key, value in urls.items():

        # uses HTTP to get webpage data
        r = requests.get(value)
        html = r.text
        new_soup = BeautifulSoup(html, 'html.parser')
        hash = hashlib.sha224(html.encode('utf-8')).hexdigest()

        # if folders doesn't exist, create it and put html data
        if not os.path.exists("{}\\{}".format(os.path.abspath(os.getcwd()), key)):
            os.mkdir("{}\\{}".format(os.path.abspath(os.getcwd()), key))
            f = open(key + '/' + key + '.txt', 'w', encoding="utf-8")
            f.write(html)
            f.close()

            print("{} file created".format(key))

        else:  # if folder exists, open it and compare to data
            f = open(key + '/' + key + '.txt', "r", encoding="utf-8")
            file_data = f.read()
            old_soup = BeautifulSoup(file_data, 'html.parser')

            old_text = "".join(
                [i.text.replace("\r\n", "\n\n") for i in old_soup.main.find_all(['p', 'h1'])])
            new_text = "".join(
                [i.text.replace("\r\n", "\n\n") for i in new_soup.main.find_all(['p', 'h1'])])

            if old_text != new_text:
                # writes doc with old text
                print(old_text)
                print(new_text)

                n = open(key + '/' + key + ' {}'.format(str(datetime.datetime.today()).replace(':', '-')) +
                         '.txt', 'w', encoding="utf-8")
                n.write(" ".join(old_text))
                n.close()

                # updates html doc
                f = open(key + '/' + key +
                         '.txt', 'w', encoding="utf-8")
                f.write(html)
                f.close()

                # send email
                print('change')
                print(value)
            else:
                print("{} hasn't changed at {}".format(
                    key, datetime.datetime.today()))
    time.sleep(60)
