import sqlite3
DATABASE_NAME='library.db'
def createUsersTable():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute('create table if not exists users(id integer primary key autoincrement,name text,role text,email text,password text)')
    con.commit()

def getUsers():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    cur.execute('select * from users')
    rows=cur.fetchall() #POSTGRESQL
    return rows

def addUser(name,email,password,role):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute('insert into users(name,email,password,role) values(?,?,?,?)',(name,email,password,role))
    con.commit()   

def loginUser(email,password):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    cur.execute('select * from users where email=? and password=?',(email,password))
    rows=cur.fetchone()
    print(rows)
    return rows  

def getRole(user_id):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    cur.execute('select role from users where id=?', (user_id,))
    rows=cur.fetchone() #POSTGRESQL
    return rows
#======BOOK MODULE=========
def createBooksTable():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute('create table if not exists books(id integer primary key autoincrement,title text,author text,isbn text,description text)')
    con.commit()

def addBook(title,author,isbn,description):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute('insert into books(title,author,isbn,description) values(?,?,?,?)',(title,author,isbn,description))
    con.commit() 

def getBooks():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    cur.execute('select * from books')
    rows=cur.fetchall() 
    return rows


def getBooksSearch(key):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    key='%'+key+'%'
    cur.execute('select * from books where title like ? or author like ? or description like ?',(key,key,key))
    rows=cur.fetchall()
    return rows    


#Request==========
def createRequestTable():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute('create table if not exists requests(id integer primary key autoincrement,book_id integer,user_id integer,status text,req_date text,issue_date text, return_date text)')
    con.commit()

def addRequest(userid,bookid):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute("insert into requests(book_id,user_id,status,req_date) values(?,?,?,datetime('now', 'localtime'))",(userid,bookid,'Requested'))
    con.commit() 
    

#Admin
def getAllRequests():
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    cur.execute('select rq.*, books.title,users.name,users.id as user_id,books.id as book_id  from requests as rq inner join books on rq.book_id==books.id inner join users on rq.user_id==users.id')
    rows=cur.fetchall() 
    print(rows)
    return rows

#To return individual user requests 
def getRequestsByStatus(users_id,status):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    con.row_factory = sqlite3.Row #Add this: To get data by column name
    cur=con.cursor()
    status=str(status).lower()
    if status=='all':
        cur.execute('select rq.*, books.title,users.name,users.id as user_id,books.id as book_id  from requests as rq inner join books on rq.book_id==books.id inner join users on rq.user_id==users.id where rq.user_id=?',(users_id,))
    else:
        cur.execute('select rq.*, books.title,users.name,users.id as user_id,books.id as book_id  from requests as rq inner join books on rq.book_id==books.id inner join users on rq.user_id==users.id where rq.user_id=? and rq.status=?',(users_id,status))
    rows=cur.fetchall()
    return rows    
# Issue 
def issueBook(req_id):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute("update requests set status=?, issue_date=datetime('now', 'localtime') where id=?",('Issued',req_id))
    #TODO:Update books table as it was issued.
    con.commit()   
# Return admin
def returnBook(req_id):
    con=sqlite3.connect(DATABASE_NAME,check_same_thread=False)
    cur=con.cursor()
    cur.execute("update requests set status=?, return_date=datetime('now', 'localtime') where id=?",('Returned',req_id))
    #TODO:Update books table as it was issued.
    con.commit()      

createUsersTable()
createBooksTable()
createRequestTable()


