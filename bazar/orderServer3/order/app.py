from flask import Flask , request
import requests

app = Flask(__name__)
catalog_counter =1

#redirect the purchase requset to decrese requsest
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
   
    amount = request.form.get('amount')
    global catalog_counter
    if catalog_counter==1:
      response  = requests.put("http://192.168.1.30:3000/decrease/"+ str(id), {'amount':amount})
      catalog_counter = catalog_counter +1
    elif catalog_counter == 2:
       response  = requests.put("http://192.168.1.30:4000/decrease/"+ str(id), {'amount':amount})
       catalog_counter = catalog_counter + 1
    elif catalog_counter == 3:
       response  = requests.put("http://192.168.1.30:5000/decrease/"+ str(id), {'amount':amount})
       catalog_counter = 1
    
    x = response.json()

    if x['response'][0]['status'] =="decreased quantity sucsesfully":
        return "the order is placed"

    return x['response'][0]['status']


   

if __name__ == '__main__':
    app.run(debug = True),
