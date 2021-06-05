from flask import Flask, request, render_template
import wikipedia
import requests
import random
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERs'] = 'Content-Type'

def get_picture(wiki):
    url = "http://flip1.engr.oregonstate.edu:4075/?" + wiki
    r = requests.get(url).json()
    r = r[1:]
    r = r[:-1]
    r = json.loads(r)
    return r['url']

def scrape_multiple_keyword(wiki):
    summary = wikipedia.summary(wiki)
    count = 0
    res = ""
    for ele in summary:
        if ele == ' ':
            count = count + 1
            if res[-1] != ' ':
                res = res + " "
                
        else:
            if count % 6 == 0:
                res = res + ele

        if len(res) > 150:
            break
        
    res_list = res.split()
    return res_list

def scrape_single_keyword(wiki_page):
    summary = wikipedia.summary(wiki_page)
    count = 0
    res = ""
    for ele in summary:
        if ele == ' ':
            count = count + 1
            if res[-1] != ' ':
                res = res + " "
                
        else:
            if count % 6 == 0:
                res = res + ele

        if len(res) > 150:
            break
        
    res_list = res.split()
    return random.choice(res_list)


@app.route('/')
def search():
    return render_template("hello.html")

@app.route('/', methods=['POST'])
def search_result():
    if request.form['submit_button'] == 'Scrape':
        text = request.form['text']

        res_list = scrape_multiple_keyword(text)
        #picture = get_picture(text)

        return render_template("results.html", res_list = res_list)
    elif request.form['submit_button'] == 'Encrypt':
        url = 'https://quiet-wave-78817.herokuapp.com/encrypt'
        password = "yourpassword"
        message = request.form["encrypt_text"]

        myobj = {'password': password,
            'message' : message }

        x = requests.post(url, json = myobj)
        x = x.text

        return render_template("results_encrypt.html", x = x)

@app.route("/keyword", methods=['POST'])
@cross_origin()
def postKeyword():
    request_data = request.json

    return scrape_single_keyword(request_data['message'])


if __name__ == '__main__':
    app.run()
