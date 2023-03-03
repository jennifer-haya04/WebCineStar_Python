from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='cinestar'

mysql.init_app(app)

@app.route('/')
def index():
  conection = mysql.connect()
  print(conection)
  return render_template('index.html')

@app.route('/cines')
def cines():
  conection = mysql.connect()
  cursor = conection.cursor()
  cursor.execute("call sp_getCines()")
  cines = cursor.fetchall()
  conection.close()
  print(cines)
  return render_template('cines.html', cines = cines)

@app.route('/cine/<int:id>')
def cine(id):
  conection = mysql.connect()
  cursorCine = conection.cursor()
  cursorCine.execute("call sp_getCine(%s)", id)
  cine = cursorCine.fetchall()

  cursorTarifas = conection.cursor()
  cursorTarifas.execute("call sp_getCineTarifas(%s)", id)
  cineTarifa = cursorTarifas.fetchall()

  cursorPeli = conection.cursor()
  cursorPeli.execute("call sp_getCinePeliculas(%s)", id)
  cinePeli = cursorPeli.fetchall()

  conection.close()
      
  return render_template('cine.html', cine = cine, cineTarifa = cineTarifa, cinePeli = cinePeli)

@app.route('/peliculas/<string:tipo>')
def peliculas(tipo):
    conection = mysql.connect()
    cursor = conection.cursor()
    if(tipo == 'cartelera'):
      cursor.execute("call sp_getPeliculas(1)")      
    else:
      cursor.execute("call sp_getPeliculas(2)")
    
    peliculas = cursor.fetchall()
    conection.commit()
    print(peliculas)
    return render_template('peliculas.html', peliculas = peliculas)

@app.route('/pelicula/<int:id>')
def pelicula(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute("call sp_getPelicula(%s)", (id))   
    
    pelicula = cursor.fetchall()
    conection.commit()
    return render_template('pelicula.html', pelicula = pelicula)

if __name__ == '__main__':
    app.run(debug=True)