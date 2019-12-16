import os
from flask import Flask, request, redirect,jsonify
from werkzeug.utils import secure_filename
from try_retrain import predict_image_class
from bs4 import BeautifulSoup
import requests

UPLOAD_FOLDER = 'D:/'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/alzheimer')
def alzheimer():
    # URL = "https://www.google.com/search?tbm=nws&q=alzheimer"
    URL = "https://news.google.com/search?q=alzheimer"
    r = requests.get(URL)
    # return r.content
    soup = BeautifulSoup(r.content, 'html5lib')
    # return str(len(soup.findAll('a',{'class': 'lLrAF'})))
    # return r.content
    newsList = []  # a list to store quotes
    all_news = soup.findAll('article')
    print(len(all_news))
    # soup.findNextSiblings
    all_news = all_news[:10]
    for news in all_news:
        newsData = {}
        newsData['url'] = news.contents[1].a['href']
        newsData['title'] = news.contents[1].a.text
        newsData['source'] = news.contents[3].div.a.text
        newsData['time'] = news.contents[3].div.time.text
        newsList.append(newsData)
    return jsonify(newsList)

@app.route('/cancer')
def cancer():
    # URL = "https://www.google.com/search?tbm=nws&q=alzheimer"
    URL = "https://news.google.com/search?q=cancer"
    r = requests.get(URL)
    # return r.content
    soup = BeautifulSoup(r.content, 'html5lib')
    # return str(len(soup.findAll('a',{'class': 'lLrAF'})))
    # return r.content
    newsList = []  # a list to store quotes
    all_news = soup.findAll('article')
    print(len(all_news))
    # soup.findNextSiblings
    all_news = all_news[:10]
    for news in all_news:
        newsData = {}
        newsData['url'] = news.contents[1].a['href']
        newsData['title'] = news.contents[1].a.text
        newsData['source'] = news.contents[3].div.a.text
        newsData['time'] = news.contents[3].div.time.text
        newsList.append(newsData)
    return jsonify(newsList)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print("START")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            testres = predict_image_class(UPLOAD_FOLDER+filename)
            print(testres)
            return jsonify(testres)

if __name__ == '__main__':
   app.run(debug = True,host='0.0.0.0')
