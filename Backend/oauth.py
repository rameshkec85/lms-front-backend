import requests
from flask import *
import traceback
app=Flask(__name__)

@app.route('/oauth/redirect')
def generateCode():
    return {'token':request.args.get('code')}
    


if __name__ =='__main__':
    app.run(debug=True)
    
