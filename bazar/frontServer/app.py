import requests
from flask import Flask

app = Flask(__name__)

order_counter=1
catalog_counter=1


# return the books information(ID,title) with the given topic
# this req send to the catalog ser
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
    global catalog_counter
    if catalog_counter == 1:
        r = requests.get("http://192.168.1.30:3000/search/" + topic)
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 2:
        r = requests.get("http://192.168.1.30:4000/search/" + topic)
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 3:
        r = requests.get("http://192.168.1.30:5000/search/" + topic)
        catalog_counter = 1
    return (r.content)

# return all information about all books
# this req send to catalog server 
@app.route('/information/all', methods=['Get'])
def information_all():
  global catalog_counter
  if catalog_counter == 1:
    r = requests.get("http://192.168.1.30:3000/information/all")
    catalog_counter = catalog_counter + 1
  elif catalog_counter == 2:
    r = requests.get("http://192.168.1.30:4000/information/all")
    catalog_counter = catalog_counter + 1
  elif catalog_counter == 3:
    r = requests.get("http://192.168.1.30:5000/information/all")
    catalog_counter = 1
  return (r.content)


# return all information about specific book according to given ID
# this req send to catalog server 
@app.route('/information/<int:id>', methods=['Get'])
def information_id(id):
      global catalog_counter
  if catalog_counter == 1:
    r = requests.get("http://192.168.1.30:3000/information/")
    catalog_counter = catalog_counter + 1
  elif catalog_counter == 2:
    r = requests.get("http://192.168.1.30:4000/information/")
    catalog_counter = catalog_counter + 1
  elif catalog_counter == 3:
    r = requests.get("http://192.168.1.30:5000/information/")
    catalog_counter = 1
  return (r.content)


# this req will be used from the internal system by the admin in order to
#update price of specific book - it will send to catalog server
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
    price = request.json['price']
    global catalog_counter
    if catalog_counter == 1:
        r = requests.put("http://192.168.1.30:3000/update_price/" + str(id), {'price': price})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 2:
        r = requests.put("http://192.168.1.30:4000/update_price/" + str(id), {'price': price})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 3:
        r = requests.put("http://192.168.1.30:5000/update_price/" + str(id), {'price': price})
        catalog_counter = 1
    return (r.content)


# this req will be used from the internal system by the admin in order to
#increase the amount of specific book in the store
@app.route('/increase/<int:id>', methods=['Put'])
def increase(id):
    amount = request.json['amount']
    global catalog_counter
    if catalog_counter == 1:
        r = requests.put("http://192.168.1.30:3000/increase/" + str(id), {'amount': amount})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 2:
        r = requests.put("http://192.168.1.30:4000/increase/" + str(id), {'amount': amount})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 3:
        r = requests.put("http://192.168.1.30:5000/increase/" + str(id), {'amount': amount})
        catalog_counter = 1
    return (r.content)

# this req will be used from the internal system by the admin in order to
#decrese the amount of specific book in the store
@app.route('/decrease/<int:id>', methods=['Put'])
def decrease(id):
    amount = request.json['amount']
    global catalog_counter
    if catalog_counter == 1:
        r = requests.put("http://192.168.1.30:3000/decrease/" + str(id), {'amount': amount})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 2:
        r = requests.put("http://192.168.1.30:4000/decrease/" + str(id), {'amount': amount})
        catalog_counter = catalog_counter + 1
    elif catalog_counter == 3:
        r = requests.put("http://192.168.1.30:5000/decrease/" + str(id), {'amount': amount})
        catalog_counter = 1
    return (r.content)

#this req will be sent to order server in order to purchase a number of specific
# book
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
        amount = request.json['amount']
    global order_counter
    if order_counter == 1:
        r = requests.post("http://192.168.1.20:3000/purchase/" + str(id), {'amount': amount})
        order_counter = order_counter + 1
    elif order_counter == 2:
        r = requests.post("http://192.168.1.20:4000/purchase/" + str(id), {'amount': amount})
        order_counter = order_counter + 1
    elif order_counter == 3:
        r = requests.post("http://192.168.1.20:5000/purchase/" + str(id), {'amount': amount})
        order_counter = 1
    return (r.content)

if __name__ == '__main__':
    app.run(debug=True, port=3500)
