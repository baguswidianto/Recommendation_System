from wsgiref import headers
import pandas as pd
import os.path
import numpy as np
from flask import Flask, request, make_response, render_template, redirect, url_for
from flask.helpers import url_for

app = Flask(__name__)

def recomendation_review(product):
    #data = pd.read_csv("data/Data Revisi.csv", encoding="ISO-8859-1",on_bad_lines='skip')
    data = pd.read_excel('data/Data Revisi.xlsx')
    cosine_sim = pd.read_csv("data/cosine_data.csv", encoding="ISO-8859-1",on_bad_lines='skip')
    indexprod = int(data.loc[data['Nama Produk'] == product].index.values[0])
    similar_review = list(enumerate(cosine_sim.iloc[indexprod]))
    sorted_similar_review = sorted(similar_review, key=lambda x:x[1], reverse=True)
    aa = []
    for i in range(1,6) :
        aa.append(sorted_similar_review[i][0])
    return data.iloc[aa,:5]




@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/result", methods=["POST"])
def recommendation():
    if request.method == "POST":
        product_name = str(request.form["product_name"])
        df = recomendation_review(product_name)
        headers = list(enumerate(df.columns, 1))
        rows = []
        print(headers)
        for _, row in df.iterrows():
            rows.append(list(enumerate(row, 1)))

        return render_template("result.html", headers=headers, rows=rows)


if __name__ == '__main__':
    app.run(debug=True)

