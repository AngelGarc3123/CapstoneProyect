from datetime import datetime
import re
import unicodedata
import unittest

def normalize_input(data):
    if isinstance(data, str):
        # Normalizar el texto a la forma canónica
        data = unicodedata.normalize('NFKD', data)
        # Convertir a minúsculas y eliminar espacios en blanco
        data = data.strip().lower()
    return data

# Valida el email para cualquier dominio válido
def validate_email(email):
    email = normalize_input(email)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Valida la edad (al menos 18 años)
def validate_dob(dob):
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age >= 18

# Valida el usuario con formato "nombre.apellido"
def validate_user(user):
    patron = r'^[a-zA-Z]+\.[a-zA-Z]+$'
    return bool(re.fullmatch(patron, user))

# Valida el DNI: exactamente 10 dígitos
def validate_dni(dni):
    patron = r'^\d{10}$'
    return bool(re.fullmatch(patron, dni))

# Valida la contraseña: entre 8 y 35 caracteres, con al menos una minúscula, una mayúscula, un dígito y un carácter especial
def validate_pswd(pswd):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#*@\$%&\-!+=?])[A-Za-z\d#*@\$%&\-!+=?]{8,35}$'
    return bool(re.fullmatch(pattern, pswd))

# Valida que el nombre contenga solo letras (sin espacios ni números)
def validate_name(name):
    return bool(re.fullmatch(r'^[a-zA-Z]+$', name))

# Valida todos los campos del registro
def validate_signup(nombre, apellidos, dni, dob, telefono, email, password, tipo):
    errores = []
    
    if not validate_name(nombre):
        errores.append("Nombre inválido. Solo se permiten letras sin espacios.")
    if not validate_name(apellidos):
        errores.append("Apellidos inválidos. Solo se permiten letras sin espacios.")
    if not validate_dni(dni):
        errores.append("DNI inválido. Debe tener 10 dígitos.")
    if not validate_dob(dob):
        errores.append("Fecha de nacimiento inválida. Debes tener al menos 18 años.")
    if not validate_email(email):
        errores.append("Correo electrónico inválido.")
    if not validate_pswd(password):
        errores.append("Contraseña inválida. Debe tener entre 8 y 35 caracteres, incluyendo mayúsculas, minúsculas, un dígito y un carácter especial.")
    if tipo not in ["medico", "usuario"]:
        errores.append("Tipo de usuario inválido. Selecciona 'medico' o 'usuario'.")
    
    if errores:
        return " ".join(errores)
    return None

# Pruebas unitarias
class TestValidationFunctions(unittest.TestCase):
    
    def test_validate_email(self):
        self.assertTrue(validate_email("usuario@urosario.edu.co"))
        self.assertTrue(validate_email("usuario@gmail.com"))
        self.assertTrue(validate_email("usuario@domain.com"))
        self.assertFalse(validate_email("usuario@domain"))
        self.assertFalse(validate_email("usuario@.com"))
        self.assertFalse(validate_email("usuario.com"))
    
    def test_validate_dob(self):
        self.assertTrue(validate_dob("2000-01-01"))  # Mayor de 18
        self.assertFalse(validate_dob("2010-01-01")) # Menor de 18
    
    def test_validate_user(self):
        self.assertTrue(validate_user("sara.palacios"))
        self.assertFalse(validate_user("sara_palacios"))
        self.assertFalse(validate_user("sarapalacios"))
        self.assertFalse(validate_user("sara.palacios1"))
        self.assertFalse(validate_user("sara.palacios!"))
    
    def test_validate_dni(self):
        self.assertTrue(validate_dni("1000000001"))
        self.assertFalse(validate_dni("10000000001"))
        self.assertFalse(validate_dni("abcdefg123"))
    
    def test_validate_name(self):
        self.assertTrue(validate_name("Sara"))
        self.assertTrue(validate_name("Palacios"))
        self.assertFalse(validate_name("Sara123"))
        self.assertFalse(validate_name("Sara_Palacios"))
        self.assertFalse(validate_name("Sara!"))
        self.assertFalse(validate_name("Sara Palacios"))
    
    def test_validate_password(self):
        self.assertTrue(validate_pswd("Passw0rd!"))
        self.assertFalse(validate_pswd("password"))
        self.assertFalse(validate_pswd("PASSWORD1"))
        self.assertFalse(validate_pswd("Passw0rd"))
        self.assertFalse(validate_pswd("Pw1!"))
        self.assertFalse(validate_pswd("A" * 36 + "1!"))
    
    def test_validate_signup(self):
        # Ejemplo de registro válido
        error = validate_signup("Sara", "Palacios", "1234567890", "2000-01-01", "3001234567", "sara@example.com", "Passw0rd!", "usuario")
        self.assertIsNone(error)
        
        # Ejemplo con errores en nombre y email
        error = validate_signup("Sara123", "Palacios", "1234567890", "2000-01-01", "3001234567", "saraexample.com", "Passw0rd!", "usuario")
        self.assertIsNotNone(error)
        
if __name__ == "__main__":
    unittest.main()
