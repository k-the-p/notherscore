import sys
import cshogi
import cshogi.KIF
from cshogi.usi import Engine
import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
board = cshogi.Board() #使わないけど何かの際に

def listoutput():
    #エンジン読み込み、設定変更はここ
    engine = Engine(config.get("DEFAULT", "Enginepath") , debug=False)
    engine.setoption("NodesLimit", config.get("DEFAULT", "Nodeslimit"))

    #以下は触らない
    engine.setoption("MultiPV", "2")
    engine.isready()

    #棋譜読み込み
    path = 'kifu.kif'
    with open(path, encoding="UTF-8", mode="r") as f:
        kif = cshogi.KIF.Parser.parse_str(f.read())[0]
    kiflist = kif['moves']
    #kiflist = ['7g7f', '3c3d', '7i6h', '2b6f'] #テスト用

    #out.txt初期化
    with open("out.txt", 'w') as f:
        f.truncate(0)


    #棋譜に従って手を進める
    j = []
    for i in kiflist:
        j.append(i)
        engine.position(j)
        # #ここから下はなんとかしたかったけど不明
        sys.stdout = open('out.txt', 'a')
        engine.go(listener=print)
        sys.stdout = sys.__stdout__ # 元に戻す
    return kif['moves']

def sente():
    path = 'kifu.kif'
    with open(path, encoding="UTF-8", mode="r") as f:
        kif = cshogi.KIF.Parser.parse_str(f.read())[0] 
    return("先手 " + str(kif['names'][cshogi.BLACK]).replace("None", ""))
def gote():
    path = 'kifu.kif'
    with open(path, encoding="UTF-8", mode="r") as f:
        kif = cshogi.KIF.Parser.parse_str(f.read())[0] 
    return("後手 " + str(kif['names'][cshogi.WHITE]).replace("None", ""))
