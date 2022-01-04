import requests
from flask import *
import traceback
app=Flask(__name__)
import json
# localhost:5001/login?email=&password=
BASE_URL='http://localhost:5001'
app.static_folder = 'static'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html',page='home')


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
    # return render_template('sidemenu.html',name=resJson['name'])
    return redirect('/home')

   
@app.route('/sidemenu')
def sideMenu():
    return render_template('sidemenu.html')   


@app.route('/test')
def test():
    return render_template('sidemenu.html',content='About')   

@app.route('/add-book')
def addBook():
    return render_template('add-book.html',page='add-book')   

@app.route('/view-books')
def viewBooks():
    url=BASE_URL+'/books'
    try:
        res=requests.get(url)
        print(res.status_code)
        print(res.text)    
        resJson=json.loads(res.text) # Convert String to JSON
        print(resJson)
        return render_template('view-books.html',books=resJson,page='view-books')   
    except:
        return render_template('view-books.html',books=[],page='view-books')   

@app.route('/student-requests')
def studentRequests():
    url=BASE_URL+'/requests'
    try:
        res=requests.get(url)
        print(res.status_code)
        print(res.text)    
        resJson=json.loads(res.text) # Convert String to JSON
        print(resJson)
        return render_template('student-requests.html',book_req=resJson)   
    except:
        return render_template('student-requests.html',book_req=[])   

@app.route('/saveBook',methods=['POST'])
def saveBook():
    title = request.form.get('title')
    description = request.form.get('description')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    #Backend apis 
    url=BASE_URL+'/addbook'
    res=requests.get(url,params={'title':title,'description':description,'author':author,'isbn':isbn})
    print(res.status_code)
    print(res.text)    
    resJson=json.loads(res.text) # Convert String to JSON
    print(resJson)
    if resJson['code']!=200:
            return render_template('login-error.html')
    return redirect('/add-book')

#student-requests
if __name__ =='__main__':
    # app.run(debug=True)
    app.run(debug=True,host='localhost', port=5000)

