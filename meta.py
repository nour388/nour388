from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QTextEdit, \
    QInputDialog , QTextBrowser
import sys
from PIL import Image
import imagehash
import requests
import webbrowser
from PyQt5.QtGui import QPixmap
import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from PIL.ExifTags import TAGS
import subprocess
import exifread
from geopy.geocoders import Nominatim
import geopy
import os




# ---------------------------------------------------------------------------------------------------------------#

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Image Recon"
        self.top = 300
        self.left = 600
        self.width = 500
        self.height = 400

        self.InitWindow()

    # ---------------------------------------------------------------------------------------------------------------#
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("A:\\face.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.vbox = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.vbox.addWidget(self.textEdit)
        self.textEdit.setHtml("<font color='red' size='8'><red>Image Recon By Nour !</font>")
        self.textEdit2 = QTextBrowser()
        self.vbox.addWidget(self.textEdit2)
        self.textEdit2.setStyleSheet("background-color: rgb(0, 0, 0);")





        self.label = QLabel("Your Image will Be displayed here")
        self.label.setStyleSheet('color: rgb(97, 173, 184)')
        self.vbox.addWidget(self.label)

        self.btn1 = QPushButton("Browse Image")
        self.btn1.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn1.clicked.connect(self.getImage)

        self.vbox.addWidget(self.btn1)



        self.btn2 = QPushButton("Check Hash ")
        self.btn2.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn2.clicked.connect(self.chkHash)

        self.vbox.addWidget(self.btn2)

        self.btn3 = QPushButton("Google Reverse")
        self.btn3.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn3.clicked.connect(self.showD)
        self.vbox.addWidget(self.btn3)

        self.btn4 = QPushButton("Google Query")
        self.btn4.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn4.clicked.connect(self.showQ)
        self.vbox.addWidget(self.btn4)

        self.btn5 = QPushButton("Get MetaData")
        self.btn5.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn5.clicked.connect(self.metaData)
        self.vbox.addWidget(self.btn5)

        self.btn6 = QPushButton("Find The Place on GeoLocation")
        self.btn6.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn6.clicked.connect(self.Address)
        self.vbox.addWidget(self.btn6)

        self.btn8 = QPushButton("Clear")
        self.btn8.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn8.clicked.connect(self.clearText)

        self.vbox.addWidget(self.btn8)

        self.btn7 = QPushButton("Restart")
        self.btn7.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn7.clicked.connect(self.restartLayout)
        self.vbox.addWidget(self.btn7)



        self.setLayout(self.vbox)

        self.show()

    # ---------------------------------------------------------------------------------------------------------------#
    def clearText(self):
        self.textEdit.clear()
        self.textEdit2.clear()

    # ---------------------------------------------------------------------------------------------------------------#
    def restartLayout(self):
       args = sys.argv[:]  # get shallow copy of running script args
       args.insert(0, sys.executable)  # give it the executable
       os.execv(sys.executable, args)

    # ---------------------------------------------------------------------------------------------------------------#

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'C:\\', "Image files (*.jpg *.jpeg *.png *.gif)")
        self.imagePath = fname[0]
        pixmap = QPixmap(self.imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())

    # ---------------------------------------------------------------------------------------------------------------#
    def chkHash(self):
        hash0 = imagehash.average_hash(Image.open(self.imagePath))
        hash1 = imagehash.average_hash(Image.open('C:\\test.jpg'))
        cutoff = 5  # maximum bits that could be different between the hashes.

        if hash0 - hash1 < cutoff:
            self.textEdit.setHtml("<font color='red' size='6'><red>Images Are Similar !</font>")
        else:

            self.textEdit.setHtml("<font color='red' size='6'><red>Images Are Not Similar !</font>")
    # ---------------------------------------------------------------------------------------------------------------#
    def showD(self):

        self.text, ok = QInputDialog.getText(self, 'Write A Keyword', 'Exapmle:"twitter.com"')

        if ok == True:
            self.google()

    # ---------------------------------------------------------------------------------------------------------------#
    def showQ(self):

        self.text1, ok1 = QInputDialog.getText(self, 'Write A Keyword', 'Your Search Keyword')

        if ok1 == True:
            self.googlequery()

    # ---------------------------------------------------------------------------------------------------------------#
    def google(self):
        filePath = self.imagePath
        domain = self.text
        searchUrl = 'http://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': '', 'q': f'site:{domain}'}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        self.fetchUrl = response.headers['Location']
        # webbrowser.open(self.fetchUrl) #if i want to open browser
        self.textEdit2.setTextColor(QColor(57, 255, 20))
        self.textEdit2.append("-------------------------------------------------------")
        self.textEdit2.setFontPointSize(12)
        self.textEdit2.setTextColor(QColor(255, 0, 0))
        self.textEdit2.append("Exact Image was Found Below Click to Go !")
        self.textEdit2.setTextColor(QColor(57, 255, 20))
        self.textEdit2.append("-------------------------------------------------------")
        self.getLinks()
        self.textEdit2.setTextColor(QColor(57, 255, 20))
        self.textEdit2.setFontPointSize(12)
        self.textEdit2.append("-------------------------------------------------------")
        self.textEdit2.setTextColor(QColor(255, 0, 0))
        self.textEdit2.append("Similar Image Url was Found Below Click to Go !")
        self.textEdit2.setTextColor(QColor(57, 255, 20))
        self.textEdit2.setFontPointSize(12)
        self.textEdit2.append("-------------------------------------------------------")
        self.ImageUrl()

    # ---------------------------------------------------------------------------------------------------------------#

    def getLinks(self):
        links = []  # Initiate empty list to capture final results

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        headers = {'User-Agent': user_agent}
        url = self.fetchUrl
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        result = response.read().decode('utf-8')
        soup = BeautifulSoup(result, 'html.parser')
        search = soup.find_all('div', class_="yuRUbf")
        for h in search:
            links.append(h.a.get('href'))

        for i in range(len(links)):
            # print(links[i])
            ur = '<a href=\"{urls}\">{urls}</a>'.format(urls=links[i])
            self.textEdit2.setTextColor(QColor(255, 0, 0))
            self.textEdit2.setFontPointSize(12)
            self.textEdit2.append(ur)
            self.textEdit2.setOpenExternalLinks(True)
            self.textEdit2.setTextColor(QColor(57, 255, 20))
            self.textEdit2.setFontPointSize(12)
            self.textEdit2.append("-------------------------------------------------------")


    # ---------------------------------------------------------------------------------------------------------------#
    def googlequery(self):
        query = self.text1
        search = query.replace(' ', '+')
        results = 30
        url = (f"https://www.google.com/search?q={search}&num={results}")

        requests_results = requests.get(url)
        soup_link = BeautifulSoup(requests_results.content, "html.parser")
        links = soup_link.find_all("a")

        for link in links:
            link_href = link.get('href')
            if "url?q=" in link_href and not "webcache" in link_href:
                title = link.find_all('h3')

                if len(title) > 0:
                    # print(link.get('href').split("?q=")[1].split("&sa=U")[0])
                    # print(title[0].getText())
                    a = link.get('href').split("?q=")[1].split("&sa=U")[0]
                    b = '<a href=\"{urls}\">{urls}</a>'.format(urls=a)
                    self.textEdit2.setTextColor(QColor(255, 0, 0))
                    self.textEdit2.setFontPointSize(12)
                    self.textEdit2.append(b)
                    self.textEdit2.setOpenExternalLinks(True)
                    self.textEdit2.setTextColor(QColor(57, 255, 20))
                    self.textEdit2.setFontPointSize(12)
                    self.textEdit2.append("-------------------------------------------------------")
                    self.textEdit2.setTextColor(QColor(57, 255, 20))
                    self.textEdit2.setFontPointSize(12)
                    self.textEdit2.append("-------------------------------------------------------")

    # ---------------------------------------------------------------------------------------------------------------#
    def ImageUrl(self):
        link1 = []  # Initiate empty list to capture final results

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        headers = {'User-Agent': user_agent}
        url = self.fetchUrl
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        result = response.read().decode('utf-8')
        soup = BeautifulSoup(result, 'html.parser')
        search = soup.find_all('div', class_='eA0Zlc PZPZlf qN5nNb ivg-i GMCzAd')
        for h in search:
            link1.append(h.get('data-lpage'))

        for i in range(len(link1)):
            # print(links[i])
            ur2 = '<a href=\"{urls}\">{urls}</a>'.format(urls=link1[i])
            self.textEdit2.setTextColor(QColor(255, 0, 0))
            self.textEdit2.setFontPointSize(12)
            self.textEdit2.append(ur2)
            self.textEdit2.setTextColor(QColor(57, 255, 20))
            self.textEdit2.setFontPointSize(12)
            self.textEdit2.append("-------------------------------------------------------")


    # ---------------------------------------------------------------------------------------------------------------#
    def metaData(self):
        # pip install hachoir

        input_file = self.imagePath
        exe = "hachoir-metadata"
        self.process = subprocess.Popen([exe, input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for output in self.process.stdout:
            a = str(output.strip())
            self.textEdit.append(a)
            self.textEdit.setTextColor(QColor(57,255,20))
            self.textEdit.setFontPointSize(12)



    # ---------------------------------------------------------------------------------------------------------------#
    def Address(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        geopy.geocoders.options.default_user_agent = user_agent
        path1 = self.imagePath
        with open(path1, 'rb') as f:
            exif_dict = exifread.process_file(f)

            # Longitude
            lon_ref = exif_dict["GPS GPSLongitudeRef"].printable
            lon = exif_dict["GPS GPSLongitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lon = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / float(lon[3]) / 3600
            if lon_ref != "E":
                lon = lon * (-1)

            # Latitude
            lat_ref = exif_dict["GPS GPSLatitudeRef"].printable
            lat = exif_dict["GPS GPSLatitude"].printable[1:-1].replace(" ", "").replace("/", ",").split(",")
            lat = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / float(lat[3]) / 3600
            if lat_ref != "N":
                lat = lat * (-1)
            # print('latitude and longitude of photo: ', (lat, lon))

            reverse_value = str(lat) + ', ' + str(lon)
            geolocator = Nominatim()
            location = geolocator.reverse(reverse_value)

            v = location.address

            self.textEdit.setTextColor(QColor(57,255,20))
            self.textEdit.setFontPointSize(12)
            self.textEdit.append("-------------------------------------------------------")
            self.textEdit.setTextColor(QColor(255, 0, 0))
            self.textEdit.append('latitude and longitude information of photo: ')
            self.textEdit.append(reverse_value)
            self.textEdit.setTextColor(QColor(57, 255, 20))
            self.textEdit.append("-------------------------------------------------------")
            self.textEdit.setTextColor(QColor(255, 0, 0))
            self.textEdit.append('photo address information: ')
            self.textEdit.append(v)







# ---------------------------------------------------------------------------------------------------------------#


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
