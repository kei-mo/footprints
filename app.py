#次やること

#app.py
from flask import Flask, request, render_template
import urllib
import numpy as np
import json

import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs

import matplotlib.pyplot as plt
from matplotlib.dates import date2num

from io import BytesIO

import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

fig, ax = plt.subplots(1,1)


@app.route("/")
def index():
    return render_template("index.html")

'''
初期化
jsonをつくる
空の世界地図をプロットする
'''
@app.route("/init")
def init():

    data = {} # 辞書
    with open('experience.json', 'w') as outfile:
        json.dump(data, outfile)
    
    # plot
    fig = plt.figure(figsize=(4,4),dpi=200)
    ax = fig.add_subplot(1,1,1)
    
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND,facecolor=(.8, .8, .8), alpha=.6)
    ax.add_feature(cartopy.feature.OCEAN,facecolor=(0.99, .99, .99))
    ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.5)
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5,linewidth=0.1)
    # ax.add_feature(cartopy.feature.LAKES, alpha=0.95)
    #ax.add_feature(cartopy.feature.RIVERS)
    # ax.set_extent([-150, 60, -25, 60])

    
    png_out = BytesIO()
    plt.savefig(png_out, format="png", bbox_inches="tight")
    img_data = urllib.parse.quote(png_out.getvalue())

    return "data:image/png:base64," + img_data



'''
更新
jsonを読み込み更新
世界地図を更新
'''
@app.route("/plot/country")
def plot_country():

    # Obtain query parameters

    exp = request.args.get("experience",default=-1,type=int) # 経験
    update_country = request.args.get("country", default="", type=str) # 国の記号 英字2文字
    
    update_country =  update_country.upper() # HTMLは小文字表記のため大文字に変換する
    
    print(update_country)

    # 辞書(json)読み込み
    with open("experience.json","r") as f:
        data = json.load(f)
    
    for k, v in data.items():
        if v == -1:
            data[k] = 0
            
    # 辞書に追加
    data[update_country] = exp
    
    # 辞書(json)書き込み    
    with open('experience.json', 'w') as outfile:
        json.dump(data, outfile)

        
    
    # 色を塗る国のリストを抽出
    plotCountList = data.keys()

    
    
    # plot
    fig = plt.figure(figsize=(4,4),dpi=200)
    ax = fig.add_subplot(1,1,1)
    
    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.LAND,facecolor=(.8, .8, .8), alpha=.6)
    ax.add_feature(cartopy.feature.OCEAN,facecolor=(0.99, .99, .99))
    ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.5)
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.5,linewidth=0.1)
    # ax.add_feature(cartopy.feature.LAKES, alpha=0.95)
    #ax.add_feature(cartopy.feature.RIVERS)
    # ax.set_extent([-150, 60, -25, 60])

    
    # 国名読み込み
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records() # ジェネレーター

    # 色塗り
    # ISO_A2は国名の2文字表記
    print('point'+str(exp))
    
    num = 0
    for country in countries:
        cntName = country.attributes['ISO_A2']
        
        # # debug用
        # if country.attributes['NAME'] == 'France':
        #     print('France' + country.attributes['ISO_A2'])
        
        # # debug用
        # if country.attributes['NAME'] == 'Norway':
        #     print('Norway' + country.attributes['ISO_A2'])
        

        if cntName == '-99':
            if country.attributes['NAME'] == 'France':
                cntName = 'FR'
            elif country.attributes['NAME'] == 'Norway':
                cntName = 'NO'

        if cntName in plotCountList:
            if data[cntName] == -1:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(0, 1, 1),
                                  label=cntName)
            elif data[cntName] == 0:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(.9, .9, .9),
                                  label=cntName)
            elif data[cntName] == 1:
                num += 1
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(1, 0.5, 0),
                                  alpha=0.5,
                                  label=cntName)
            elif data[cntName] == 2:
                num += 1
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(1, 0.5, 0),
                                  alpha=0.5,
                                  label=cntName)
            elif data[cntName] == 3:
                num += 1
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(1, 0.5, 0),
                                  label=cntName)
            elif data[cntName] == 4:
                num += 1
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                                  facecolor=(1, 0.5, 0),
                                  label=cntName)
        

    png_out = BytesIO()
    plt.savefig(png_out, format="png", bbox_inches="tight")
    img_data = urllib.parse.quote(png_out.getvalue())

    return "data:image/png:base64," + img_data

'''
画像データをダウンロードする関数
サーバー内にに保存する
'''
@app.route("/save/fig")
def save_fig(img_data):

    img_data.savefig('footprint.png', format="png", bbox_inches="tight")
    img_data.savefig('footprint.svg', format="svg", bbox_inches="tight")



'''
result 1(訪問国数)を計算する関数
'''
@app.route("/show/result1")
def show_result1():
    
    
    # 辞書(json)読み込み
    with open("experience.json","r") as f:
        data = json.load(f)
    num = 0
    for k,v in data.items():
        if v >= 1:
            num+=1
    
    return str(num)



'''
result 2(経験値)を計算する関数
'''
@app.route("/show/result2")
def show_result2():
    
    
    # 辞書(json)読み込み
    with open("experience.json","r") as f:
        data = json.load(f)
    num = 0
    for k,v in data.items():
        if v >= 1:
            num+=v
    
    return str(num)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
