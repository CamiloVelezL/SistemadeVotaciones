# Sistema de Votaciones - Flask

Sistema web completo para la gestión de procesos electorales desarrollado con Flask y MySQL.

## Estructura del Proyecto

Sistema-de-Votaciones/
├── app/ # Aplicación Flask
│ ├── routes/ # Controladores de rutas
│ │ ├── init.py
│ │ ├── candidates.py
│ │ ├── voters.py
│ │ └── votes.py
│ ├── models.py # Modelos de datos
│ ├── database.py # Configuración de base de datos
│ └── init.py # Inicialización de la app
├── static/ # Archivos estáticos
│ ├── style.css # Estilos CSS
│ └── script.js # JavaScript del frontend
├── templates/ # Plantillas HTML
│ └── index.html # Página principal
├── .venv/ # Entorno virtual 
├── config.py # Configuración de la aplicación
├── run.py # Punto de entrada
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo


## Características

### Gestión Completa
- **Candidatos**: Registrar, listar y eliminar candidatos
- **Votantes**: Registrar, listar y eliminar votantes
- **Estadísticas**: Conteo en tiempo real de registros

### Validaciones
- Nombres únicos para candidatos
- Emails únicos para votantes
- Prevención de duplicados
- Confirmación antes de eliminaciones

### Interfaz Moderna
- Diseño responsive con CSS Grid/Flexbox
- Colores profesionales con tema verde
- Iconografía Font Awesome
- Mensajes de confirmación y error


# Backend
- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **PyMySQL** - Conector MySQL
- **MySQL** - Base de datos

# Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos y animaciones
- **JavaScript ES6+** - Interactividad
- **Font Awesome** - Iconos

# . Prerrequisitos
- Python 3.8 o superior
- MySQL 5.7 o superior
- Git (opcional)

#. Configuración del Proyecto

```bash
# Crear directorio del proyecto
mkdir Sistema-de-Votaciones
cd Sistema-de-Votaciones

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

Instalar Dependencias

pip install flask flask-sqlalchemy pymysql
O crear archivo requirements.txt:

Flask==2.3.3
Flask-SQLAlchemy==3.0.5
PyMySQL==1.1.0
SQLAlchemy==2.0.20

Y luego ejecutar:
pip install -r requirements.txt

Configurar Base de Datos
CREATE DATABASE voting_system;

Configurar conexión en config.py:
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:password@localhost/voting_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave-secreta-para-desarrollo'

Estructura de Archivos
run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

app/__init__.py
from flask import Flask, jsonify
from config import Config
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_db(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        return jsonify({"status": "OK"})
    
    from app.routes.voters import bp as voters_bp
    from app.routes.candidates import bp as candidates_bp
    
    app.register_blueprint(voters_bp, url_prefix='/api')
    app.register_blueprint(candidates_bp, url_prefix='/api')
    
    return app

app/database.py
from app.models import db

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'party': self.party
        }

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'has_voted': self.has_voted
        }

Inicializar Base de Datos
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"




Ejecución
python run.py
La aplicación estará disponible en: http://127.0.0.1:5000

API Endpoints
Candidatos
GET /api/candidates - Listar candidatos
POST /api/candidates - Crear candidato
DELETE /api/candidates/<id> - Eliminar candidato

Votantes
GET /api/voters - Listar votantes
POST /api/voters - Registrar votante
DELETE /api/voters/<id> - Eliminar votante

Uso del Sistema

Gestión de Candidatos
Acceder a la aplicación en el navegador
En "Gestión de Candidatos", completar nombre y partido
Hacer clic en "Agregar Candidato"
Usar "Actualizar Lista" para ver todos los candidatos
Hacer clic en "Eliminar" para remover candidatos
Gestión de Votantes
En "Gestión de Votantes", completar nombre y email
Hacer clic en "Registrar Votante"
Usar "Actualizar Lista" para ver todos los votantes
Hacer clic en "Eliminar" para votantes que no han votado

Estadísticas
La sección "Estadísticas del Sistema" muestra conteos en tiempo real
Se actualiza automáticamente al agregar o eliminar registros

Validaciones
Candidatos
Nombre obligatorio
Nombre único en el sistema
No puede coincidir con email de votante existente

Votantes
Nombre y email obligatorios
Email único en el sistema
No puede coincidir con nombre de candidato existente
Solo se pueden eliminar votantes que no han votado

Desarrollo
Estructura de Blueprints
La aplicación utiliza blueprints de Flask para organizar las rutas:

app/routes/candidates.py - Rutas de candidatos
app/routes/voters.py - Rutas de votantes

Base de Datos
MySQL como motor principal
SQLAlchemy para ORM y migraciones
Modelos separados en app/models.py

Frontend
Templates Jinja2 para renderizado
CSS personalizado con variables CSS
JavaScript vanilla para interactividad
Diseño mobile-first responsive

Para consultas técnicas o soporte sobre el sistema de votaciones.

## **Archivos Adicionales Necesarios**
### **requirements.txt**
```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
PyMySQL==1.1.0
SQLAlchemy==2.0.20