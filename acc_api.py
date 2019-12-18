from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import Flask, render_template, request, redirect,make_response
from flask_mysqldb import MySQL
app = Flask(__name__)
api = Api(app)
import os
# from werkzeug import secure_filename
app.config['MYSQL_HOST'] = '144.76.137.232'
app.config['MYSQL_USER'] = 'vkingsol_demo'
app.config['MYSQL_PASSWORD'] = 'gUj3z5?9'
app.config['MYSQL_DB'] = 'vkingsol_frennsdevelopment_aug'
# # app.config['SERVER_NAME'] = 'srv2.frenns.com'
# # app.root_path = os.path.dirname(os.path.abspath(__file__))
import json
import datetime
mysql = MySQL(app)

# import logging.config
# import config
# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# logging.config.fileConfig(logging_conf_path)
# logger = logging.getLogger(__name__)
# @app.route('/')
# def index():
#         return redirect('/upload_document_image', code=302)
@app.route('/index')
def index():
    return "<h1 style='color:blue'>Use cashflow_table or business_aging etc.!</h1>"

@app.route('/cashflow', methods=['POST']) 
def cashflow():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM cashflow WHERE cashflow.frenns_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # print(update)
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status



@app.route('/business_aging', methods=['POST']) 
def business_aging():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            name=req_data['name']
            cur.execute("SELECT * FROM business_aging WHERE business_aging.frenns_id='"+str(frenns_id)+"' and business_aging.name='"+str(name)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/cockpit_BOG', methods=['POST']) 
def cockpit_BOG():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            syncsupplier_id=req_data['syncsupplier_id']
            cur.execute("SELECT id, FRN_id, syncsupplier_id, variable_analysis, value, decision, path FROM cockpit_BOG WHERE cockpit_BOG.FRN_id='"+str(frenns_id)+"' and cockpit_BOG.syncsupplier_id='"+str(syncsupplier_id)+"'")
            update=cur.fetchall()
            cur.close()
            # from django.core.serializers.json import DjangoJSONEncoder
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status


@app.route('/cockpit_customer', methods=['POST']) 
def cockpit_customer():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT id, FRN_id, variable_analysis, value, decision, path FROM cockpit_customer WHERE cockpit_customer.FRN_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/cockpit_invoice', methods=['POST']) 
def cockpit_invoice():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            syncsupplier_id=req_data['syncsupplier_id']
            syncinvoice_id=req_data['syncinvoice_id']
            cur.execute("SELECT * FROM cockpit_invoice WHERE cockpit_invoice.FRN_id='"+str(frenns_id)+"' and cockpit_invoice.syncsupplier_id='"+str(syncsupplier_id)+"' and cockpit_invoice.syncinvoice_id='"+str(syncinvoice_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/fluctuation', methods=['POST']) 
def fluctuation():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            types=req_data['type']
            cur.execute("SELECT * FROM fluctuation WHERE fluctuation.frenns_id='"+str(frenns_id)+"' and fluctuation.type='"+str(types)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/forensic', methods=['POST']) 
def forensic():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM forensic WHERE forensic.frenns_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/invoice_analysis_syncid', methods=['POST']) 
def invoice_analysis_syncid():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            syncinvoice_id=req_data['syncinvoice_id']
            cur.execute("SELECT * FROM invoice_analysis WHERE invoice_analysis.syncinvoice_id='"+str(syncinvoice_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/invoice_analysis', methods=['POST']) 
def invoice_analysis():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM invoice_analysis WHERE invoice_analysis.frenns_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/py_aging', methods=['POST']) 
def py_aging():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM py_aging WHERE py_aging.customer_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/py_auction_analysis_data', methods=['POST']) 
def py_auction_analysis_data():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM py_auction_analysis_data WHERE py_auction_analysis_data.frn_number='"+str(frenns_id)+"'")
            update=cur.fetchall()
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update)
        except:
            status={"result":False} 
       
    return status

@app.route('/syncfraudanalysis', methods=['POST']) 
def syncfraudanalysis():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['customer_id']
            cur.execute("SELECT * FROM syncfraudanalysis WHERE syncfraudanalysis.frenns_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            # cur.execute("SELECT date_from, date_to FROM syncfraudanalysis WHERE syncfraudanalysis.frenns_id='"+str(frenns_id)+"'")
            # update1=cur.fetchall()
            def myconverter(o):
                if isinstance(o, datetime.date):
                    return o.__str__()
             
            # status2=json.dumps(update1, default = myconverter)
            # status1=json.dumps(update)
            cur.close()
            # update=json.dumps(update)
            status=json.dumps(update, default = myconverter)
        except:
            status={"result":False} 
       
    return status


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 400)
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid Request'}), 500)

#curl POST -d '{"frenns_id":"FRN00000647", "firstname": "mohammad","lastname":"yousuf","gender":"male","dob":"21/12/1994","passport_number":"L2514514"}' http://127.0.0.1:5000/details

if __name__ == '__main__':
	# app.run(host='144.76.137.232', port=2626)#
    # app.run(host='0.0.0.0')
    from waitress import serve
    serve(app,host='144.76.137.232', port=2626)#,host='144.76.137.232'

