from flask import Blueprint, request, jsonify
from app.models import db, Voter, Candidate

bp = Blueprint('voters', __name__)

@bp.route('/voters', methods=['POST'])
def create_voter():
    try:
        data = request.get_json()
        
        # Validaciones requeridas
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Verificar que el email no esté registrado como votante
        existing_voter = Voter.query.filter_by(email=data['email']).first()
        if existing_voter:
            return jsonify({'error': 'Email already registered as voter'}), 400
        
        # Verificar que el email no esté registrado como candidato
        existing_candidate = Candidate.query.filter_by(name=data['email']).first()
        if existing_candidate:
            return jsonify({'error': 'Email already registered as candidate'}), 400
        
        # Crear nuevo votante
        voter = Voter(
            name=data['name'],
            email=data['email']
        )
        
        db.session.add(voter)
        db.session.commit()
        
        return jsonify(voter.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/voters/<int:id>', methods=['DELETE'])
def delete_voter(id):
    try:
        voter = Voter.query.get(id)
        
        if not voter:
            return jsonify({'error': 'Voter not found'}), 404
        
        # Validar que el votante no haya votado
        if voter.has_voted:
            return jsonify({'error': 'Cannot delete voter who has already voted'}), 400
        
        db.session.delete(voter)
        db.session.commit()
        
        return jsonify({'message': 'Voter deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500