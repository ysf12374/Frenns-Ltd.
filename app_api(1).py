from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
api = Api(app)
import os
from werkzeug import secure_filename
app.config['MYSQL_HOST'] = '144.76.137.232'
app.config['MYSQL_USER'] = 'vkingsol_demo'
app.config['MYSQL_PASSWORD'] = 'gUj3z5?9'
app.config['MYSQL_DB'] = 'vkingsol_frennsdevelopment'
# app.config['SERVER_NAME'] = 'srv2.frenns.com'
# app.root_path = os.path.dirname(os.path.abspath(__file__))
import json
mysql = MySQL(app)

# import logging.config
# import config
# logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
# logging.config.fileConfig(logging_conf_path)
# logger = logging.getLogger(__name__)

@app.route('/')
def index():
        return redirect('/upload_document_image', code=302)

# @app.route("/")
# def hello():
#     return "<h1 style='color:blue'>Use details document_photos selfie_photos instead!</h1>"

@app.route('/details', methods=['POST']) 
def details():
    status={"result":False} 
    if request.method == 'POST':
        try:
            req_data = request.get_json(force=True)
            cur = mysql.connection.cursor()
            frenns_id=req_data['frenns_id']
            firstname=req_data['firstname']
            lastname=req_data['lastname']
            gender=req_data['gender']
            dob=req_data['dob']
            passport_number=req_data['passport_number']
            cur.execute("SELECT frenns_id FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frenns_id)+"'")
            update=cur.fetchall()
            if not update:
            	sql="INSERT INTO frenns_app_api (frenns_id, firstname, lastname, gender, dob, passport_number) values ('"+str(frenns_id)+"','"+firstname+"','"+lastname+"','"+gender+"','"+str(dob)+"','"+passport_number+"') " 
            	cur.execute(sql)
            	mysql.connection.commit()
            	cur.close()
            else:
            	sql_update_query = "UPDATE frenns_app_api set firstname = '"+firstname+"',lastname='"+lastname+"',gender='"+gender+"',dob='"+str(dob)+"',passport_number='"+passport_number+"' where frenns_id = '"+str(frenns_id)+"' LIMIT 1"
            	cur.execute(sql_update_query)
            	mysql.connection.commit()
            	cur.close()
            cur.close()
            status={"result":True}
        except:
            status={"result":False} 
       
    return status
    
@app.route('/upload_document_image')
def upload_document_image():
    return render_template('upload_document.html')
@app.route('/upload_selfie_image')
def upload_selfie_image():
    return render_template('upload_selfie.html')
   
@app.route('/document_photos', methods=['POST']) 
def document_photos():
    status={"result":False}
    if request.method == 'POST':
        try:
         file=request.files['file']
         frn_id = request.form['name'] 
         filename=secure_filename(file.filename)
         document_filename=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/document_images",filename)#+"/document_images"
         file.save(os.path.join(os.path.dirname(os.path.abspath(__file__))+"/document_images",filename))#+"/document_images"
         cur = mysql.connection.cursor()
         cur.execute("SELECT passport_photo FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frn_id)+"'")
         update=cur.fetchall()
         if not update:
            sql="INSERT INTO frenns_app_api (passport_photo) values ('"+str(document_filename)+"') " 
            cur.execute(sql)
            mysql.connection.commit()
            cur.close()
         else:
            sql_update_query = "UPDATE frenns_app_api set passport_photo = '"+document_filename+"' where frenns_id = '"+str(frn_id)+"' LIMIT 1"
            cur.execute(sql_update_query)
            mysql.connection.commit()
            cur.close()
            status={"result":True}
         # return status
        except:
            status={"result":False}
    return status


@app.route('/selfie_photos', methods=['POST']) 
def selfie_photos():
    status={"result":False} 
    if request.method == 'POST':
        try:
         file=request.files['file']
         frn_id = request.form['name'] 
         filename=secure_filename(file.filename)
         selfie_filename=os.path.join(os.path.dirname(os.path.abspath(__file__))+"/selfie_images",filename)#
         file.save(os.path.join(os.path.dirname(os.path.abspath(__file__))+"/selfie_images",filename))#+"/selfie_images"
         cur = mysql.connection.cursor()
         cur.execute("SELECT capture_photo FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frn_id)+"'")
         update=cur.fetchall()
         if not update:
            sql="INSERT INTO frenns_app_api (capture_photo) values ('"+str(selfie_filename)+"') " 
            cur.execute(sql)
            mysql.connection.commit()
            cur.close()
         else:
            sql_update_query = "UPDATE frenns_app_api set capture_photo = '"+selfie_filename+"' where frenns_id = '"+str(frn_id)+"' LIMIT 1"
            cur.execute(sql_update_query)
            mysql.connection.commit()
            cur.close()
            status={"result":True}
         # return status
        except:
            status={"result":False}
    return status

@app.route('/result/<frn_id>', methods=['GET']) 
def result(frn_id):
    status={"result":False,"message":"not executed"}
    if request.method == 'GET':
        try:
            import face_detect
            cur = mysql.connection.cursor()
            cur.execute("SELECT passport_photo FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frn_id)+"'")
            passport_image=cur.fetchone()
            cur.execute("SELECT capture_photo FROM frenns_app_api WHERE frenns_app_api.frenns_id='"+str(frn_id)+"'")
            capture_image=cur.fetchone()
            passport_image=str(passport_image)
            passport_image=passport_image[2:-3]
            capture_image=str(capture_image)
            capture_image=capture_image[2:-3]
            # passport_image=passport_image.split('/')[-1]
            print("  ",passport_image)
            final_result=face_detect.comparison(passport_image,capture_image)
            status=final_result
            sql_update_query = "UPDATE frenns_app_api set result = '"+final_result+"' where frenns_id = '"+str(frn_id)+"' LIMIT 1"
            cur.execute(sql_update_query)
            mysql.connection.commit()
            cur.close()
            status={"result":status}
            # return status
        except:
            status={"result":False,"message":"not executed"}
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
	# app.run(host='144.76.137.232', port=3996)#
    # app.run(host='0.0.0.0')
    from waitress import serve
    serve(app,host='144.76.137.232', port=3787)#,host='144.76.137.232'

