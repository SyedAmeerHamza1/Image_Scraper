from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import os
from urllib.request import urlopen as ureq
import requests
import logging
logging.basicConfig(filename="Scraper.log", level=logging.INFO, format='%(levelname)s %(asctime)s %(name)s %(message)s')

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/review", methods=["POST"])
def review():
    if request.method == 'POST':
        try:
            query= request.form['content'].replace(" ", "")


            save_d="images_scr/"

            if not os.path.exists(save_d):
                os.makedirs(save_d)

            # fake user agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M")

            response_bs=BeautifulSoup(response.content, "html.parser")

            image_tags=response_bs.find_all("img")

            del image_tags[0]

            for i in image_tags:
                image_url=i["src"]
                image_data=requests.get(image_url).content
                with open(os.path.join(save_d, f"{query}_{image_tags.index(i)}.jpg"), "wb") as f:
                    f.write(image_data)

            return "Images has been saved"
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:
        return render_template("index.html")
    

if __name__=="__main__":
    app.run(debug=True)

