import json
import requests
from flask import Flask, request, jsonify, make_response

# from flask import Flask
# from flask_ngrok import run_with_ngrok
app = Flask(__name__)

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def create_todo():
  session=requests.Session()
  
  
  #cme officially forbids scraping
  #so a header must be used to disguise as a browser
  #technically speaking, the website should be able to detect that too
  #those tech guys just turn a blind eye, thx fellas
  session.headers.update(
          {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})

  url = session.get("https://www.espncricinfo.com/series/ipl-2021-1249214/points-table-standings").text;
  bs1 = BeautifulSoup(url,'html.parser').find('table').findAll('tr')
  cols = []
  cols = [index.text for index in bs1[0].findAll('th')]
  output = []
  print(len(bs1))
  for l in range(1, len(bs1)-1):
    row = {}
    idx = 0;
    data_cols = [content.text for content in bs1[l].findAll('td')];
    for col in cols:
      row[col] = data_cols[idx]
      idx+=1
    output.append(row)
  print(output)
  return make_response(jsonify({"result": output}), 200)

if __name__ == '__main__':
    app.run(port=5000)