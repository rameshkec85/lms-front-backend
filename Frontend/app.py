import requests
from flask import *
import traceback
app=Flask(__name__)
import json
# localhost:5001/login?email=&password=
BASE_URL='http://localhost:5001'

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login')
def doLogin():
    email = request.args.get('email')
    pwd = request.args.get('pwd')
    #Backend apis 
    url=BASE_URL+'/login'
    #http://localhost:5001/login?email=anu@gmai.com&password=123456
    res=requests.get(url,params={'email':email,'password':pwd})
    print(res.status_code)
    print(res.text)    
    resJson=json.loads(res.text) # Convert String to JSON
    print(resJson)
    if resJson['code']!=200:
            return render_template('login-error.html')
    return render_template('home.html',name=resJson['name'])

   

if __name__ =='__main__':
    # app.run(debug=True)
    app.run(debug=True,host='localhost', port=5000)

