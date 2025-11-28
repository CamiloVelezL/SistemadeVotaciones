from flask import Flask, jsonify, render_template
from config import Config
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar base de datos
    init_db(app)
    
        # Imprimir la ruta de las plantillas
    print("Templates path:", app.template_folder)
    
    # Ruta Frontend
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Ruta de salud de la API
    @app.route('/api/health')
    def health():
        return jsonify({"status": "OK"})
    
    #  API
    @app.route('/api/info')
    def api_info():
        return jsonify({
            "message": "Sistema de Votaciones API",
            "endpoints": {
                "candidates": "/api/candidates",
                "voters": "/api/voters",
                "votes": "/api/votes"
            }
        })
    
    # blueprints
    from app.routes.voters import bp as voters_bp
    from app.routes.candidates import bp as candidates_bp
    from app.routes.votes import bp as votes_bp
    
    app.register_blueprint(voters_bp, url_prefix='/api')
    app.register_blueprint(candidates_bp, url_prefix='/api')
    app.register_blueprint(votes_bp, url_prefix='/api')
    
    return app