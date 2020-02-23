import json

from bson.json_util import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://new:new@cluster0-7dxzv.azure.mongodb.net/tangkilik?retryWrites=true&w=majority"
app.secret_key = "BLUEHACKS2020"

mongo = PyMongo(app)
cors = CORS(app)
# PRODUCT SELLER
# CREATE NEW PRODUCT
@app.route('/CREATE', methods=['POST'])
def create_PRODUCT():
    json = request.json
    productlocation = json['ProductLocation']
    productname = json['ProductName']
    productprice = json['ProductPrice']
    productdescription = json['ProductDescription']
    productseller = json['productseller']
    productquantity = json['ProductQuantity']
    productIMGURL = json['ProductIMGURL']

    if productlocation and productquantity and productname and productseller and productprice and productdescription and productIMGURL and request.method == 'POST':
        id = mongo.db.products.insert_one({'ProductName': productname, 'ProductLocation': productlocation,
                                           'ProductPrice': productprice, 'ProductDescription': productdescription, 'productseller': productseller,
                                           'ProductQuantity': productquantity,
                                           'ProductIMGURL': productIMGURL})
        resp = jsonify("ADDING  SUCCESSFUL")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/', methods=['GET'])
@app.route('/READALL', methods=['GET'])
def getall_PRODUCT():
    products = mongo.db.products.find()
    return dumps(products)


@app.route('/READONE/<id>', methods=['GET'])
def get_PRODUCT(id):
    product = mongo.db.products.find_one({'_id': ObjectId(id)})
    return dumps(product)


@app.route('/UPDATE/<id>', methods=['POST'])
def update_user(id):
    _id = id
    json = request.json
    productlocation = json['ProductLocation']
    productname = json['ProductName']
    productprice = json['ProductPrice']
    productdescription = json['ProductDescription']
    productseller = json['productseller']
    productIMGURL = json['ProductIMGURL']
    productquantity = json['ProductQuantity']

    if productlocation and productquantity and productname and productseller and productprice and productdescription and productIMGURL and request.method == 'POST':
        id = mongo.db.products.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'ProductName': productname,
                                                                                                                        'ProductLocation': productlocation, 'ProductPrice': productprice, 'ProductQuantity': productquantity,
                                                                                                                        'ProductDescription': productdescription, 'productseller': productseller,
                                                                                                                        'ProductIMGURL': productIMGURL}})
        resp = jsonify("UPDATING  SUCCESSFUL")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/UPDATE_QUANTITY/<id>', methods=['POST'])
def update_quantity(id):
    _id = id
    json = request.json
    productquantity = json['ProductQuantity']

    if productquantity and request.method == 'POST':
        id = mongo.db.products.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {
                                          '$set': {'ProductQuantity': productquantity}})
        resp = jsonify("UPDATING  SUCCESSFUL")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/DELETE/<id>', methods=['POST'])
def delete_user(id):
    product = mongo.db.products.delete_one({'_id': ObjectId(id)})
    resp = jsonify("DELETED SUCESSFULLY")
    resp.status_code = 200
    return resp

# CONSUMER
# TO GET SPECIFIC ITEM TO DISPLAY IN CART
@app.route('/CART/<id>', methods=['POST'])
def store_item(id):
    product = mongo.db.products.find({'_id': {'$eq':ObjectId(id)}})
    return dumps(product)

# TO GET TRANSACTIONS THAT WILL BE SHOWN IN THE TRANSACTION HISTORY TAB
@app.route('/TRANSACTION', methods=['POST'])
def transaction_history():
    json = request.json
    transactionConsumerID = json['TransactionConsumerID']
    transactionSellerID = json['TransactionSellerID']
    transactionDate = json['TransactionDate']
    transactionProduct = json['TransactionProduct']
    transactionProductPrice = json['TransactionProductPrice']
    transactionProductQuantity = json['TransactionProductQuantity']
    transactionTotalPrice = json['TransactionTotalPrice']

    if transactionConsumerID and transactionSellerID and transactionDate and transactionProduct and transactionProductPrice and transactionProductQuantity and transactionTotalPrice and request.method == 'POST':
        id = mongo.db.transaction.insert_one({
            'TransactionConsumerID': transactionConsumerID,
            'TransactionSellerID': transactionSellerID,
            'TransactionDate': transactionDate,
            'TransactionProduct': transactionProduct,
            'TransactionProductPrice': transactionProductPrice,
            'TransactionProductQuantity': transactionProductQuantity,
            'TransactionTotalPrice': transactionTotalPrice
        })
        resp = jsonify("ADDING  SUCCESSFUL")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# DISPLAY ALL TRANSACTION BASE ON USERS ID
@app.route('/TRANSACTION/<id>', methods=['GET'])
def transaction_perse(id):
    product = mongo.db.transaction.find({'TransactionConsumerID': {'$eq': id}})
    return dumps(product)


# ERROR HANDLER
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Operation Failed ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
