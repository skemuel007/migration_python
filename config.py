from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'intlgrdbmn'
app.config['MYSQL_DATABASE_PASSWORD'] = 'D1wakanda0!B'
app.config['MYSQL_DATABASE_DB'] = 'intllgr_dbms'
app.config['MYSQL_DATABASE_HOST'] = '54.82.41.46'
mysql.init_app(app)