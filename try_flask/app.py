# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', \
		title = 'ココフォリアへの出力(クトゥルフ)', \
        style = 'display:none', \
		message = 'URLを入力して下さい。')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
	name = request.form['name']
	return render_template('index.html', \
		title = 'ココフォリアへの出力(クトゥルフ)', \
        result = make_chara(name))

def make_charadata_dict(json_dict):
  charadata_dict = {}
  ginou_list = []
  ginouchi_list = []
  ginou_category_list = ["TBA", "TFA", "TAA", "TCA", "TKA"]
  ginou_category_dict = {
      "TBA": [
              "回避", "キック", "組み付き", "こぶし", "頭突き", "投擲", "マーシャルアーツ", "拳銃", 
              "サブマシンガン", "ショットガン", "マシンガン", "ライフル"
      ], 
      "TFA": [
              "応急手当", "鍵開け", "隠す", "隠れる", "聞き耳", "忍び歩き", "写真術", "精神分析", 
              "追跡", "登攀", "図書館", "目星"
      ], 
      "TAA": [
              f'運転({json_dict["unten_bunya"]})', "機械修理", "重機械操作", "乗馬", "水泳", 
              f'製作({json_dict["seisaku_bunya"]})', f'操縦({json_dict["main_souju_norimono"]})', 
              "跳躍", "電気修理", "ナビゲート", "変装"
      ], 
      "TCA": [
              "言いくるめ", "信用", "説得", "値切り", f'母国語({json_dict["mylang_name"]})'
      ], 
      "TKA": [
              "医学", "オカルト", "化学", "クトゥルフ神話", f'芸術({json_dict["geijutu_bunya"]})', 
              "経理", "考古学", "コンピュータ", "心理学", "人類学", "生物学", "地質学", "電子工学", 
              "天文学", "博物学", "物理学", "法律", "薬学", "歴史"
      ]
  }
  for category in ginou_category_list:
    ginou_list += ginou_category_dict[category]
    ginouchi_list += json_dict[f'{category}P']
    if f'{category}Name' in json_dict:
      ginou_list += json_dict[f'{category}Name']
  chat_palette = """CCB<=
CCB<={SAN} SANチェック
RESB({STR}-対抗値) STR対抗
RESB({CON}-対抗値) CON対抗
RESB({POW}-対抗値) POW対抗
RESB({DEX}-対抗値) DEX対抗
RESB({APP}-対抗値) APP対抗
RESB({SIZ}-対抗値) SIZ対抗
RESB({INT}-対抗値) INT対抗
RESB({EDU}-対抗値) EDU対抗
CCB<=({STR}*5) STR倍数
CCB<=({CON}*5) CON倍数
CCB<=({POW}*5) POW倍数
CCB<=({DEX}*5) DEX倍数
CCB<=({APP}*5) APP倍数
CCB<=({SIZ}*5) SIZ倍数
CCB<=({INT}*5) INT倍数
CCB<=({EDU}*5) EDU倍数
CCB<=({INT}*5) アイデア
CCB<=({POW}*5) 幸運
CCB<=({EDU}*5) 知識"""
  for i in range(len(ginou_list)):
    chat_palette += f"\nCCB<={ginouchi_list[i]} {ginou_list[i]}"
  chat_palette += f"""\n1D3 こぶしダメージ
CBRB({ginouchi_list[3]},{ginouchi_list[6]}) MAこぶし
2D3 MAこぶしダメージ
1D4 頭突きダメージ
CBRB({ginouchi_list[4]},{ginouchi_list[6]}) MA頭突き
2D4 MA頭突きダメージ
1D6 キックダメージ
CBRB({ginouchi_list[1]},{ginouchi_list[6]}) MAキック
2D6 MAキックダメージ
1D3 応急手当回復
2D2 医学回復
2D2 正気度回復(不定狂気時・初回のみ)
"""
  return chat_palette

def make_chara(url):
  url_js = url + ".js"
  req = urllib.request.Request(url_js)
  with urllib.request.urlopen(req) as res:
      body = res.read()
  charadata_dict = json.loads(body.decode('unicode-escape'), strict=False)
  if charadata_dict["SAN_Left"]=="":
    charadata_dict["SAN_Left"]="100"
  data = {
      "kind": "character", 
      "data": {
          "name": charadata_dict["pc_name"],
          "initiative": int(charadata_dict["NP4"]),
          "externalUrl": url,
          "status": [
              {"label": "HP", "value": int(charadata_dict["NP9"]), "max": int(charadata_dict["NP9"])},
              {"label": "MP", "value": int(charadata_dict["NP10"]), "max": int(charadata_dict["NP10"])},
              
              {"label": "SAN", "value": int(charadata_dict["SAN_Left"]), "max": int(charadata_dict["SAN_Left"])},
              {"label": "クリチケ", "value": 0, "max": 0}
          ],
          "params": [
              {"label": "STR", "value": charadata_dict["NP1"]},
              {"label": "CON", "value": charadata_dict["NP2"]},
              {"label": "POW", "value": charadata_dict["NP3"]},
              {"label": "DEX", "value": charadata_dict["NP4"]},
              {"label": "APP", "value": charadata_dict["NP5"]},
              {"label": "SIZ", "value": charadata_dict["NP6"]},
              {"label": "INT", "value": charadata_dict["NP7"]},
              {"label": "EDU", "value": charadata_dict["NP8"]}
          ],
          "commands": make_charadata_dict(charadata_dict)
      }
  }
  return json.dumps(data, ensure_ascii=False, indent=2)

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port="8000")