from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Replace the following values with your PostgreSQL connection details
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_NAME = 'sat'
DB_USER = 'fabio'
DB_PASSWORD = '123456'

# Function to connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Route to display all materials
@app.route('/')
def index():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT m.id, m.name, m.quantity, m.price, p.id, p.nome FROM material m, pessoal p WHERE m.pessoal_id = p.id ORDER BY m.id")
    materials = cur.fetchall()
    conn.close()
    return render_template('index.html', materials=materials)

# Route to display all pessoals
@app.route('/pessoal')
def pessoal():
    materialAcaut = request.args.get('materialAcaut')
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pessoal where id != '0' ORDER BY nome")
    pessoals = cur.fetchall()
    conn.close()
    return render_template('pessoal.html', pessoals=pessoals, material=materialAcaut)

# Route to add a new material
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO material (name, quantity, price, pessoal_id) VALUES (%s, %s, %s, 0)", (name, quantity, price))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to add a new material
@app.route('/addPessoal', methods=['POST'])
def addPessoal():
    id = request.form['id']
    nome = request.form['nome']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO pessoal (id, nome) VALUES (%s, %s)", (id, nome))
    conn.commit()
    conn.close()

    return redirect(url_for('pessoal'))

# Route to update a material
@app.route('/update/<int:material_id>', methods=['POST'])
def update(material_id):
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE material SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, material_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to update a pessoal
@app.route('/updatePessoal/<int:pessoal_id>', methods=['POST'])
def updatePessoal(pessoal_id):
    nome = request.form['nome']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE pessoal SET nome=%s WHERE id=%s", (nome, pessoal_id))
    conn.commit()
    conn.close()

    return redirect(url_for('pessoal'))

# Route to delete a material
@app.route('/delete/<int:material_id>')
def delete(material_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM material WHERE id=%s", (material_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to delete a pessoal
@app.route('/deletePessoal/<int:pessoal_id>')
def deletePessoal(pessoal_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM pessoal WHERE id=%s", (pessoal_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('pessoal'))

# Route to entrega material
@app.route('/entrega/<int:material_id>')
def entrega(material_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE material SET pessoal_id=0 WHERE id=%s", (material_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to acaut
@app.route('/acautelar/<int:pessoalId>', methods=['POST'])
def acaut(pessoalId):
    materialId = request.form['materialId']

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE material SET pessoal_id=%s WHERE id=%s", (pessoalId, materialId))
    conn.commit()
    conn.close()

    return redirect(url_for('pessoal'))

if __name__ == '__main__':
    app.run(debug=True)
