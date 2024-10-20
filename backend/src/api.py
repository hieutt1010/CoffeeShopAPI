import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
@app.after_request

def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH, OPTIONS')
    return response
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        
        format_drinks = [drink.short() for drink in drinks]
        return jsonify ({
            'success': True,
            'drinks': format_drinks    
        })
    except:
        abort(404)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        if payload is None:
            abort(401)
            
        drinks = Drink.query.all()
        
        format_drinks = [drink.long() for drink in drinks]
        return jsonify ({
            'success': True,
            'drinks': format_drinks    
        })
    except:
        abort(401)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
# {
# "title": "Water3",
# "recipe": {
# "name": "Water",
# "color": "blue",
# "parts": 1
# }
# }
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    if payload is None: 
        abort(401)
    if payload in [400,403]: 
        abort(payload)
    body = request.get_json()
    reqest_title = body.get('title')
    # reqest_recipe = body.get('recipe')
    request_recipe = json.dumps(body['recipe'])
    new_drink = Drink(title = reqest_title, recipe = f'[{request_recipe}]')
    new_drink.insert()
    drink = new_drink.long()
    
    return jsonify({
        'success': True,
        'drinks': drink
    })

# {
#     "title": "Water5"
# }
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload,id):
    if payload is None: 
        abort(401)
    if payload in [400,403]: 
        abort(payload)
    modify_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if modify_drink is None:
        abort(404)
    else:
        body = request.get_json()
        title = body['title']
        modify_drink.title = title
        modify_drink.update()
        
        drink = modify_drink.long()
    return jsonify({
        "success": True, 
        "drinks": [drink]
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload,id):
    if payload is None: 
        abort(401)
    if payload in [400,403]: 
        abort(payload)
        
    delete_drink = Drink.query.filter(Drink.id == id).one_or_none()
    if delete_drink is None:
        abort(404)
        
    delete_drink.delete()
    return jsonify({"success": True, "delete": id})

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
            jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
