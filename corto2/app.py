from flask import Flask,  render_template, request
import gramatica2 as gr
app = Flask(__name__)
tmp_val=""

@app.route("/", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        global tmp_val
        print("-------------SIENTRA------------------")
        tmp_val=gr.analisis(inpt)
        return render_template('index.html',input=inpt,outt=tmp_val) 
    else:
        f = open("./entrada.txt", "r")
        entrada = f.read()
        return render_template('index.html', input=entrada)

if __name__ == "__app__":
    app.run(debug=True)#para que se actualice al detectar cambios