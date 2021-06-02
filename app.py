from flask import Flask, request, render_template
import wikipedia
import requests
import random

app = Flask(__name__)

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
        summary = wikipedia.summary(text)
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
def postKeyword():
    request_data = request.json

    return scrape_single_keyword(request_data['message'])


if __name__ == '__main__':
    app.run()
