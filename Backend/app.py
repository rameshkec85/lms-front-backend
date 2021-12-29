import requests
from flask import *
import traceback
app=Flask(__name__)
import library
import json
INVALID_INPUT=402
RESPONSE_SUCCESS=200

@app.route('/')
def home():
    return "Welcome to library management system"

#1. LOGIN/SIGNUP
#2. Add books
#3. View Books
#4. View Users(Students)
#5. Issue Book
#6. Request a Book
#http://localhost:5001/signup?name=Anusha&email=anu@gmai.com&password=123456
@app.route('/signup')
def signup():
    #name,email,password, role=Student
    name=request.args.get('name')
    email=request.args.get('email')
    password=request.args.get('password')
    role='student'
    library.addUser(name=name,email=email,password=password,role=role)
    return  {'code':RESPONSE_SUCCESS,'message': "User created successfully"}

#localhost:5001/login?email=&password=
@app.route('/login')
def login():
    email=request.args.get('email')
    password=request.args.get('password')
    row=library.loginUser(email=email,password=password)
    if row is None:
        return {'code':INVALID_INPUT, 'message':"Invalid Credentials"}
    # print(row.keys())
    obj={}
    obj['code']=RESPONSE_SUCCESS
    obj['message']='Logged-in successfully'
    for key in row.keys():
        if key!='password':
            obj[key]=row[key]
    return obj

@app.route('/users')
def users():
    rows=library.getUsers()
    list=[]
    for row in rows:
        print(row['name'])
        list.append({'id':row[0], 'name':row[1],'role':row[2]})
    return json.dumps(list)



#BOOKS
@app.route('/addbook')
def addBook():
    # title,author,isbn,description
    title=request.args.get('title')
    author=request.args.get('author')
    isbn=request.args.get('isbn')
    description=request.args.get('description')
    if title is None or author is None:
        return  {'code':INVALID_INPUT,'message': "Book title or author is missing."}
    
    print(title)
    library.addBook(title=title,author=author,isbn=isbn,description=description)
    return  {'code':RESPONSE_SUCCESS,'message': "Book Added successfully"}

@app.route('/books')
def getBooks():
    rows=library.getBooks()
    list=[]
    for row in rows:
        print(row['title'])
        list.append({'id':row['id'], 'title':row['title'],'description':row['description'],'isbn':row['isbn'],'author':row['author']})
    return json.dumps(list)

#/books/search?key=text
@app.route('/books/search')
def getBooksSearch():
    key=request.args.get('key')
    if key is None:
        return {'code':INVALID_INPUT,'message': "Parameter [key] is missing"}

    rows=library.getBooksSearch(key)
    list=[]
    for row in rows:
        # print(row['title'])
        list.append({'id':row['id'], 'title':row['title'],'description':row['description'],'isbn':row['isbn'],'author':row['author']})
    return json.dumps(list)    

#REQUESTS
@app.route('/addrequest')
def addRequest():
   
    book_id=request.args.get('book_id')
    user_id=request.args.get('user_id')

    if book_id is None or user_id is None:
        return  {'code':INVALID_INPUT,'message': "Book Id or User id is missing."}
    
    library.addRequest(bookid=book_id,userid=user_id)
    return  {'code':RESPONSE_SUCCESS,'message': "Request Raised successfully"}

@app.route('/requests')
def getAllRequests():
    rows=library.getAllRequests()
    list=[]
    for row in rows:
        # print(row.keys())
        obj={}
        for key in row.keys(): #Iterate through keys and store values into object. 'request_id':row['request_id']
            obj[key]=row[key]
        print(obj)    
        list.append(obj)    
    return json.dumps(list)

@app.route('/requests_bystatus')
def getRequestsFilter():
    status=request.args.get('status')
    user_id=request.args.get('user_id')

    if status is None or user_id is None:
        return  {'code':INVALID_INPUT,'message': "Status or User id is missing."}
    
    rows=library.getRequestsByStatus(status=status,users_id=user_id)
    list=[]
    for row in rows:
        # print(row.keys())
        obj={}
        for key in row.keys(): #Iterate through keys and store values into object. 'request_id':row['request_id']
            obj[key]=row[key]
        print(obj)    
        list.append(obj)    
    return json.dumps(list)

@app.route('/issueBook')
def issueBook():
    request_id=request.args.get('request_id')
    
    if request_id is None:
        return  {'code':INVALID_INPUT,'message': "request_id key missing."}
    
    user_id=request.args.get('user_id')
    row=library.getRole(user_id=user_id)
    role=row['role']
    print(role)
    if role is None or role=='student' :
        return {'code':INVALID_INPUT,'message': "You do not have sufficient permissions."}

    library.issueBook(req_id=request_id)
    return  {'code':RESPONSE_SUCCESS,'message': "Book Issued successfully"}

@app.route('/returnBook')
def returnBook():
    request_id=request.args.get('request_id')
    if request_id is None:
        return  {'code':INVALID_INPUT,'message': "request_id key missing."}
    
    user_id=request.args.get('user_id')
    row=library.getRole(user_id=user_id)
    role=row['role']
    print(role)
    if role is None or role=='student' :
        return {'code':INVALID_INPUT,'message': "You do not have sufficient permissions."}

    
    library.returnBook(req_id=request_id)
    return  {'code':RESPONSE_SUCCESS,'message': "Book Issued successfully"}


if __name__ =='__main__':
    # app.run(debug=True)
    app.run(debug=True,host='localhost', port=5001)

