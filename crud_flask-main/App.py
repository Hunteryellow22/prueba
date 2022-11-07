from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Products')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        unidad = request.form['Unidad_medida']
        precio = request.form['Precio']
        stock = request.form['Stock']
        total= int(precio)* int(stock) 
        print(stock)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO  Products(nombre, unidad_medida, precio, stock,total) VALUES (%s,%s,%s,%s,%s)", 
        (nombre, unidad, precio, stock, total))
        mysql.connection.commit()
        flash('Product Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Products WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        unidad = request.form['Unidad_medida']
        precio = request.form['Precio']
        stock = request.form['Stock']
        total= int(precio)* int(stock) 
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Products SET nombre = %s,unidad_medida = %s,precio = %s,stock = %s,total =%s WHERE id = %s
        """, (nombre, unidad, precio, stock, total, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT stock FROM Products WHERE id={0}'.format(id))
        data = cur.fetchall()
        Contact = data[0]
        if Contact[0] > 0:
            print('Can´t Removed Product')
        else:
            cur.execute('DELETE FROM Products WHERE id = {0}'.format(id))
            mysql.connection.commit()
            flash('Contact Removed Successfully')
        return redirect(url_for('Index'))

@app.route('/search', methods = ['POST','GET'])
def search():
    if request.method == 'POST':
        nombre =request.form['Nombre']
        nombre_formato='"'+nombre+'"'
        print(nombre_formato)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Products WHERE nombre= {0}'.format(nombre_formato))
        data = cur.fetchall()
        cur.close()
        print(data)
        return render_template('search.html', contact = data[0]) 
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
