import base64
import io
import matplotlib #これと
matplotlib.use("Agg") #これは警告よけのおまじない
import matplotlib.pyplot as plt
import numpy as np
import math
import value_output

def imageoutput():
    #生データの読み込み
    with open('out.txt', mode="r") as f:
        inpt = f.read()
    
    rawlist = []
    scorelist = []
    num = 0
    #生のデータをリスト化。もっとなんとかなった気はする
    rawlist = inpt.split("\n")
    for i in rawlist:
        if i == "go":
            num = num + 1
            scorelist.append([num])
        elif i in "bestmove":
            pass
        else:
            scorelist[num - 1].append(i)

    #リストを使いやすく
    pvlist = []
    import re
    for i in scorelist:
        if "mate" in str(i): #詰み絡み
            #ここのせいでfloatを使うはめに
            pvlist.append([float(np.nan), float(np.nan)])    
        elif "multipv" in str(i): #ちゃんとmultipv吐いてる場合
            count = (i[0])
            length = len(i)
            first = i[length - 3]
            second = i[length - 2]
            #後方参照の使い方がよくわからなかったので苦肉の策
            S = "(info depth \d+ seldepth \d+ score cp )"
            E = " multipv \d+ nodes \d+ nps \d+ time \d+ pv .*"
            score1_s = re.sub(S, "" , first)
            score2_s = re.sub(S, "" , second)
            score1_se = re.sub(E, "" , score1_s)
            score2_se = re.sub(E, "" , score2_s)
            pvlist.append([score1_se, score2_se])
        else: #主に王手などの対応でその一手の場合
            count = (i[0])
            length = len(i)
            last = i[length - 2]
            S = "info depth \d+ seldepth \d+ score cp "
            E = " nodes \d+ nps \d+ time \d+ pv .*"
            last_s = re.sub(S, "" , last)
            last_se = re.sub(E, "" , last_s)
            pvlist.append([last_se, last_se])

    na = np.array(pvlist , dtype="float")
    na_point = na[:, 0] #リスト分割 na_point=最終的に出力する評価値
    na_point[0::2] *= -1 #後手の評価値を正負逆転

    teban = "gote" #データは先手が指した後から始まる
    sen_val = np.array([])
    go_val = np.array([np.nan]) #後手を1手遅らせる

    for i in na: #先後で+-分けつつリストを2倍に引き延ばす
        if teban == "sente":
            diff = np.abs(i[1] - i[0])
            sen_val = np.append(sen_val, diff) 
            sen_val = np.append(sen_val, diff)
            teban = "gote"
        
        elif teban == "gote":
            diff = np.abs(i[1] - i[0])
            go_val = np.append(go_val, diff * -1)
            go_val = np.append(go_val, diff * -1)
            #sen_val = np.append(sen_val, float(np.nan))
            teban = "sente"

    #出力を+-2000に丸める
    clipval = 2000
    sen_val = sen_val.clip(clipval * -1 , clipval)
    go_val = go_val.clip(clipval * -1 , clipval)
    na_point = na_point.clip(clipval * -1 , clipval)

    #グラフの高解像度化 jupyterにおける
    #%matplotlib inline
    #%config InlineBackend.figure_formats = {'png', 'retina'}

    #あとはmatplotlibにお任せ
    plt.figure(dpi=150)
    plt.plot(na_point, lw = 0.7 , ls = "dotted" , color="black")
    plt.plot(sen_val , lw = 1)
    plt.plot(go_val , lw = 1)

    #対局者名を取得
    s = value_output.sente()
    g = value_output.gote()
    plt.text(2, 750, s ,fontname="MS Gothic", color="tab:blue")
    plt.text(2, -750, g , fontname="MS Gothic", color="tab:orange")
    plt.text(-2, 0, "評価値" , fontname="MS Gothic", color="black")

    #流石に0手目からグラフが始まるのは許せなかったために小賢しい努力
    plt.xticks([0, math.floor(len(na_point)/2), len(na_point)],
    [1,math.ceil(len(na_point)/2 + 0.5), len(na_point) + 1])

    #出力
    #plt.savefig("sin.png")
    #plt.show()
    s= io.BytesIO()
    plt.savefig(s, format='png', bbox_inches="tight")
    plt.close()
    s= base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return (s)