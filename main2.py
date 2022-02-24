##Creating Rest Api with Crud operation
from email import message
import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

	
@app.route('/cicosy')
def cicosy():
		try:
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM cicosy")
			rows = cursor.fetchall()
			res= jsonify(rows)
			res.status_code = 200
 
			return res
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close() 

# @app.route('/cicosy/<int:CustomerID>')
# def cicosy(CustomerID):
# 	try:	               
# 		conn = mysql.connect()
# 		cursor = conn.cursor(pymysql.cursors.DictCursor)
# 		cursor.execute("SELECT CustomerID, Category, Region, Revenue FROM cicosy WHERE CustomerID =%s" ,CustomerID)
# 		cicosyRow = cursor.fetchone()
# 		res = jsonify(cicosyRow)
# 		res.status_code = 200

# 		return res
# 	except Exception as e:
# 		print(e)
# 	finally:
# 		cursor.close()
# 		conn.close()

@app.errorhandler(404)
def not_found(error=None):
	message={
		'status': 404,
        'message': 'Record not found: ' + request.url,
	}
	respone=jsonify(message)
	respone.status_code=404
	return respone



if __name__ == "__main__":
	    app.run()	

	
