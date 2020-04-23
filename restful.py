from flask import Flask, jsonify, request
app = Flask(__name__)

languages = [{'name':'JS'},{'name':'C++'},{'name':'Ruby'}]
@app.route('/', methods = ['GET'])
def test():
	return jsonify({'message':'It works!'})

@app.route('/lang',methods = ['GET'])
def returnAll():
    return jsonify({'langs':languages})

@app.route('/lang/<string:name>', methods = ['GET'])
def return1(name):
    langs1 = [lang for lang in languages if lang['name']==name]
    return jsonify({ 'lang2' : langs1[0]})
    
@app.route('/lang',methods = ['POST'])
def addone():
    lang2 = {'name':request.json['name']}
    languages.append(lang2)
    return jsonify({'languages':languages})
	
if __name__=='__main__':
	app.run(debug = True, port = 8080)