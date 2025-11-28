from flask import Blueprint, request, jsonify
from app.models import db, Candidate, Voter

bp = Blueprint('candidates', __name__)

@bp.route('/candidates', methods=['POST'])
def create_candidate():
    try:
        data = request.get_json()
        
        # Validaciones requeridas
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Verificar que el nombre no esté registrado como candidato
        existing_candidate = Candidate.query.filter_by(name=data['name']).first()
        if existing_candidate:
            return jsonify({'error': 'Name already registered as candidate'}), 400
        
        # Verificar que el nombre no esté registrado como votante
        existing_voter = Voter.query.filter_by(email=data['name']).first()
        if existing_voter:
            return jsonify({'error': 'Name already registered as voter'}), 400
        
        # Crear nuevo candidato
        candidate = Candidate(
            name=data['name'],
            party=data.get('party')
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify(candidate.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = Candidate.query.all()
        return jsonify([candidate.to_dict() for candidate in candidates]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/candidates/<int:id>', methods=['DELETE'])
def delete_candidate(id):
    try:
        candidate = Candidate.query.get(id)
        
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Validar que el candidato no tenga votos asociados
        # (Agregaremos esta validación cuando tengamos el modelo de votos)
        
        db.session.delete(candidate)
        db.session.commit()
        
        return jsonify({'message': 'Candidato eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500