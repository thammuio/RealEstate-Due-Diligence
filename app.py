from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os


app = Flask(__name__)
app.config['DEBUG'] = True

address = ''
zip_code = ''

app.route("/")
def hello():
    return "Welcome to Zinvest!!"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search_form.html')
    elif request.form['address'] or request.form['zip']:
        global address
        global zip_code
        address = request.form['address']
        zip_code = request.form['zip']
        data = address + " " + zip_code
        return redirect(url_for('search_address', data=data))
    else:
        return render_template('search_form.html')


@app.route('/search/<data>', methods=['GET', 'POST'])
def search_address(data):
    context = True
    return render_template('search_form.html', fulladdress=data, address=address, zip_code=zip_code, context=context)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('search'))


@app.route('/homefacts/', methods=['GET'])
def homefacts():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Connection': 'keep-alive',
               'Content-Length': '0',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'www.homefacts.com',
               'Referer': 'http://www.homefacts.com/',
               'Upgrade-Insecure-Requests': '1'}
    data = 'listing_type=&fulladdress=' + address+zip_code + '&category=default'
    req = requests.post('http://www.homefacts.com/hfreport.html', headers=headers, data=data)
    return redirect(req.url)


@app.route('/realtytrac/', methods=['GET'])
def realtytrac():
    req = requests.get('http://www.realtytrac.com/geo/location/HomeSearch?address=' + address+zip_code +
                       '&flow=foreclosures&bedsFrom=undefined&bathFrom=undefined&priceFrom=null'
                       '&priceTo=null&isDefaultText=false&callback=')
    url = str(req.text)
    url = json.loads(url)
    url = str(url['RedirectUrl'])
    return redirect('http://realtytrac.com' + url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)