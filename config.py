from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'D1wakanda0!B'
app.config['MYSQL_DATABASE_DB'] = 'sandboxdb'
app.config['MYSQL_DATABASE_HOST'] = '54.171.7.205'
mysql.init_app(app)