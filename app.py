from flask import Flask, request, render_template
app = Flask(__name__)
import wrapper


@app.route("/")
def show():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    path = 'kifu.kif'
    kifutxt = request.form["kifutxt"]
    file = open(path, encoding="UTF-8", mode="w", newline="\n") #ここで改行コードを指定しないと改行が2重になる。動作に影響はないのだが。
    file.write(kifutxt)
    file.close()
    img = wrapper.result()
    imgtag = '<img src="data:image/png;base64,' + img + '" />'
    return render_template("index.html", kifutxt = kifutxt, img = imgtag)