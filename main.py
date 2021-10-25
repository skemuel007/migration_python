import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/activity_logs', defaults={'page':1})
@app.route('/activity_logs/<int:page>')
def activity_logs(page):
	per_page = 100
	# page = request.args.get(get_page_parameter(), type=int, default=1)
	offset = (page - 1) * per_page
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT * FROM activity_logs")
		total = cursor.fetchall()

		cursor.execute("SELECT * FROM activity_logs order by id asc LIMIT %s OFFSET %s", (per_page, offset))
		activityRows = cursor.fetchall()

		response = jsonify({
			"paginate" : {
				"page" : page,
				"per_page": per_page,
				"offset": offset,
				"total": len(total)
			},
			"data" : activityRows
		})
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/mtn_dumps', defaults={'page':1})
@app.route('/mtn_dumps/<int:page>')
def mtn_dumps(page):
	per_page = 100
	# page = request.args.get(get_page_parameter(), type=int, default=1)
	offset = (page - 1) * per_page
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT * FROM mtndumps")
		total = cursor.fetchall()

		cursor.execute("SELECT * FROM mtndumps order by id asc LIMIT %s OFFSET %s", (per_page, offset))
		mtnDumpsRows = cursor.fetchall()

		response = jsonify({
			"paginate": {
				"page": page,
				"per_page": per_page,
				"offset": offset,
				"total": len(total)
			},
			"data": mtnDumpsRows
		})

		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/data_dumps', defaults={'page':1})
@app.route('/data_dumps/<int:page>')
def data_dumps(page):
	per_page = 100
	# page = request.args.get(get_page_parameter(), type=int, default=1)
	offset = (page - 1) * per_page
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT * FROM data_dumps")
		total = cursor.fetchall()

		cursor.execute("SELECT * FROM data_dumps order by id asc LIMIT %s OFFSET %s", (per_page, offset))
		dataDumpsRows = cursor.fetchall()

		response = jsonify({
			"paginate": {
				"page": page,
				"per_page": per_page,
				"offset": offset,
				"total": len(total)
			},
			"data": dataDumpsRows
		})

		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/precustomers')
def precustomers():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("select id as precustomer_id, bvn_dump, id_dump from pre_customers where bvn_dump is not null and id_dump is not null")
		precustomers = cursor.fetchall()
		respone = jsonify(precustomers)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Record not found: ' + request.url,
	}
	respone = jsonify(message)
	respone.status_code = 404
	return respone


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5032, debug=True)