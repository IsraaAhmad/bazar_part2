import requests
from flask import Flask, request , jsonify
import sqlite3

app = Flask(__name__)
order_counter = 1
catalog_counter = 1
counters = [2, 2, 3]



def DB_for_information(setetment):
    sqlcon = sqlite3.connect('cache.DB')
    cursor = sqlcon.cursor()
    count = cursor.execute(setetment)
    rows = cursor.fetchall()
    sqlcon.commit()
    cursor.close()
    sqlcon.close()
    return rows


# return the books information(ID,title) with the given topic
# this req send to the catalog ser
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
 sq_qa = 'select * from catalog where topic="'+topic+'"'
    rows = DB_for_information(sq_qa)
    print(len(rows))
    print("**************")
    if(topic == "Distributed systems" and len(rows) == counters[0]) or (topic == "Undergraduate School" and len(rows) == counters[1]) or (topic == "new catalog" and len(rows) == counters[2]):
        response = []
        for i in rows:
            dic = dict(ID=i[0], title=i[1], price=i[2], quantity=i[3], topic=i[4])
            response.append(dic)
        return jsonify({'response':response})
    else:
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
        result = r.json()
        sq_qa = 'delete from catalog where topic="' + topic + '"'
        DB_for_information(sq_qa)
        sq_qa = 'select * from catalog where 1'
        rows = DB_for_information(sq_qa)
        x =-1
        if topic == "Distributed systems":
            x = counters[0]
        if topic == "Undergraduate School":
            x = counters[1]
        if topic == "new catalog":
            x = counters[2]
        if( len(rows) + x > 5):
            diff = 5- len(rows) + x
            for i in range(0,diff):
                max = -1
                print("&&&&&&&&&&&")
                print(rows)
                for i in rows:
                    print(i[1])
                    if (int(i[1]) > max):
                        max = int(i[1])
                qur_sql = 'delete from catalog where ID ="' + str(max) + '"'
                DB_for_information(qur_sql)

        for i in range(0,x):
            print(result['response'][i]['price'])
            print("^^^^^^^^^^^^^^^^^^^")
            sql_qery = 'INSERT INTO catalog (ID,title ,price,quantity,topic) VALUES("' + str(result['response'][i]['ID']) + '","' + result['response'][i]['title'] + '","' + str(result['response'][i]['price']) + '","' + str(result['response'][i]['quantity']) + '","' + result['response'][i]['topic'] + '")'
            print(sql_qery)
            print("***********")

            DB_for_information(sql_qery)
        return r.content

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
sq_qa = 'select * from catalog where 1'
  rows = DB_for_information(sq_qa)
  cache_size = len(rows)
  print(cache_size)
  sql_query = 'select * from catalog where ID ='+str(id)
  rows = DB_for_information(sql_query)
  if len(rows) == 0:
      global catalog_counter
      if catalog_counter == 1:
          r = requests.get("http://192.168.1.30:3000/information/" + str(id))
          catalog_counter = catalog_counter + 1
      elif catalog_counter == 2:
          r = requests.get("http://192.168.1.30:4000/information/" + str(id))
          catalog_counter = catalog_counter + 1
      elif catalog_counter == 3:
          r = requests.get("http://192.168.1.30:5000/information/" + str(id))
          catalog_counter = 1
      result = r.json()
      if cache_size < 5:
          print("**************")
          print(result)
          sql_qery = 'INSERT INTO catalog (ID,title ,price,quantity,topic) VALUES("'+str(result['response'][0]['ID'])+'","'+result['response'][0]['title']+'","'+str(result['response'][0]['price'])+'","'+str(result['response'][0]['quantity'])+'","'+result['response'][0]['topic']+'")'
          print(sql_qery)
          DB_for_information(sql_qery)
      else:
          sql_q = 'SELECT * from catalog where 1'
          rows = DB_for_information(sql_q)
          max = -1
          print("&&&&&&&&&&&")
          print(rows)
          for i in rows:
              print(i[1])
              if(int(i[1]) > max):
                  max = int(i[1])
          qur_sql = 'delete from catalog where ID ="'+str(max)+'"'
          DB_for_information(qur_sql)
          sql_qery = 'INSERT INTO catalog (ID,title ,price,quantity,topic) VALUES("' + str(result['response'][0]['ID']) + '","' + result['response'][0]['title'] + '","' + str(result['response'][0]['price']) + '","' + str(result['response'][0]['quantity']) + '","' + result['response'][0]['topic'] + '")'
          DB_for_information(sql_qery)



      return (r.content)
  else:
      response = []
      for i in rows:
          dic = dict(ID=i[1], title=i[0], price=i[2], quantity=i[3], topic=i[4])
          response.append(dic)

      return jsonify({'response': response})



# this req will be used from the internal system by the admin in order to
#update price of specific book - it will send to catalog server
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
       price = request.json['price']
    sql_q = 'update catalog set price = '+str(price)+' where ID ='+str(id)
    rows = DB_for_information(sql_q)

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
