import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash
import validation  # Asegúrate de que validation.py esté en la misma carpeta o en el PYTHONPATH

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para usar flash messages

DB_FILE = 'db.txt'

def load_db():
    """Carga la base de datos desde el archivo db.txt."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Retorna lista vacía si el archivo está corrupto
    return []

def save_db(data):
    """Guarda la base de datos en el archivo db.txt en formato JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Aquí implementarás la lógica de login
    return render_template('login.html')  # Página de inicio de sesión

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Recoge los datos del formulario, incluyendo el nuevo campo "tipo"
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        dni = request.form.get('dni')
        dob = request.form.get('dob')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        password = request.form.get('password')
        tipo = request.form.get('tipo')  # "medico" o "usuario"
        
        # Validación de los datos usando tu función en validation.py
        errores = validation.validate_signup(nombre, apellidos, dni, dob, telefono, email, password, tipo)
        if errores:
            flash(errores, 'danger')
            return render_template('signup.html')
        
        # Si la validación es exitosa, crear el objeto usuario
        usuario = {
            "nombre": nombre,
            "apellidos": apellidos,
            "dni": dni,
            "dob": dob,
            "telefono": telefono,
            "email": email,
            "password": password,  # Nota: recuerda hashear la contraseña en producción
            "tipo": tipo
        }
        
        # Cargar la base de datos, agregar el usuario y guardar
        db = load_db()
        db.append(usuario)
        save_db(db)
        
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))
    
    # Si es GET, simplemente renderiza el formulario
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
