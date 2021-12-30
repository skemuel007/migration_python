import json

import pymysql
import requests
from requests.exceptions import HTTPError

from app import app
from config import mysql
from flask import jsonify
from flask import flash, request


@app.route('/activity_logs', defaults={'page': 1})
@app.route('/activity_logs/<int:page>')
def activity_logs(page):
    per_page = 100
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT count(id) as count FROM activity_logs_01")
        total = cursor.fetchall()

        count = total[0]['count']

        iterations = (count // per_page) + 2

        f = open("logs.txt", "w")
        f.close()

        for i in range(1, iterations):
            page = i
            offset = (page - 1) * per_page
            cursor.execute("SELECT * FROM activity_logs_01 order by id asc LIMIT %s OFFSET %s", (per_page, offset))
            activity_rows = cursor.fetchall()
            payload = json.dumps(activity_rows, indent=4, sort_keys=True, default=str)

            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            try:
                res = requests.post('http://prodapps.intelligra.io:86/api/v1/activity/batch', data=payload, headers=headers)
                # res.json()
                # f = open("logs.txt", "a")
                # f.write("Record - {} to {} written \n".format(activity_rows[0]['id'], activity_rows[len(activity_rows) - 1]['id']))
                # f.close()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            else:
                print('Success!')

        response = jsonify({
            "paginate": {
                "page": page,
                "per_page": per_page,
                "offset": offset,
                "total": len(total)
            },
            "data": activity_rows
        })
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/data_dump', defaults={'page': 1})
@app.route('/data_dump/<int:page>')
def precustomers(page):
    per_page = 100
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT count(id) as count FROM data_dumps")
        total = cursor.fetchall()

        count = total[0]['count']

        iterations = (count // per_page) + 2

        f = open("logs.txt", "w")
        f.close()

        for i in range(1, iterations):
            page = i
            offset = (page - 1) * per_page
            cursor.execute("SELECT * FROM data_dumps order by id asc LIMIT %s OFFSET %s", (per_page, offset))
            activity_rows = cursor.fetchall()
            payload = json.dumps(activity_rows, indent=4, sort_keys=True, default=str)

            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }
            try:
                res = requests.post('http://prodapps.intelligra.io:86/api/v1/data/batch', data=payload, headers=headers)
                # res.json()
                # f = open("logs.txt", "a")
                # f.write("Record - {} to {} written \n".format(activity_rows[0]['id'], activity_rows[len(activity_rows) - 1]['id']))
                # f.close()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')  # Python 3.6
            except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
            else:
                print('Success!')

        response = jsonify({
            "paginate": {
                "page": page,
                "per_page": per_page,
                "offset": offset,
                "total": len(total)
            },
            "data": activity_rows
        })
        response.status_code = 200
        return response
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
    app.run(host='0.0.0.0', port=5032, debug=True)
