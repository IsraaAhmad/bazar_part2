from flask import Flask , request
import requests

app = Flask(__name__)

#redirect the purchase requset to decrese requsest
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
   
    amount = request.form.get('amount')
    response  = requests.put("http://192.168.1.30:5000/decrease/"+ str(id), {'amount':amount})
    
    x = response.json()

    if x['response'][0]['status'] =="decreased quantity sucsesfully":
        return "the order is placed"

    return x['response'][0]['status']


   

if __name__ == '__main__':
    app.run(debug = True,port=3500),
