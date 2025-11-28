from flask import Blueprint, request, jsonify
from app.models import db, Vote, Voter, Candidate
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import os

bp = Blueprint('votes', __name__)

@bp.route('/votes', methods=['POST'])
def create_vote():
    try:
        data = request.get_json()
        
        #validaciones
        if not data or not data.get('voter_id') or not data.get('candidate_id'):
            return jsonify({'error': 'voter_id and candidate_id are required'}), 400
        
        voter_id = data['voter_id']
        candidate_id = data['candidate_id']
        
        # Verificar que el votante existe
        voter = Voter.query.get(voter_id)
        if not voter:
            return jsonify({'error': 'Voter not found'}), 404
        
        # Verificar que el candidato existe
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Verificar que el votante no sea candidato
        voter_as_candidate = Candidate.query.filter_by(name=voter.email).first()
        if voter_as_candidate:
            return jsonify({'error': 'A voter cannot be a candidate and vice versa'}), 400
        
        
        if voter.has_voted:
            return jsonify({'error': 'Voter has already voted'}), 400
        
        # Crear el voto
        vote = Vote(
            voter_id=voter_id,
            candidate_id=candidate_id
        )
        
      
        voter.has_voted = True
        
        # Incrementar el conteo de votos del candidato
        candidate.votes += 1
        
        db.session.add(vote)
        db.session.commit()
        
        return jsonify({
            'id': vote.id,
            'voter_id': vote.voter_id,
            'candidate_id': vote.candidate_id,
            'message': 'Vote recorded successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/votes', methods=['GET'])
def get_votes():
    try:
        votes = Vote.query.all()
        votes_data = [vote.to_dict() for vote in votes]
        return jsonify(votes_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/voters', methods=['GET'])
def get_voters():
    try:
        voters = Voter.query.all()
        return jsonify([voter.to_dict() for voter in voters]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/votes/statistics', methods=['GET'])
def get_statistics():
    try:
        
        candidates = Candidate.query.all()
        
        
        total_votes = sum(candidate.votes for candidate in candidates)
        
        
        voted_voters = Voter.query.filter_by(has_voted=True).count()
        
        # Estadísticas por candidato
        statistics = []
        for candidate in candidates:
            percentage = (candidate.votes / total_votes * 100) if total_votes > 0 else 0
            statistics.append({
                'candidate_id': candidate.id,
                'candidate_name': candidate.name,
                'party': candidate.party,
                'votes': candidate.votes,
                'percentage': round(percentage, 2)
            })
        
        # Generar gráfica con pandas
        generate_votes_chart(statistics)
        
        return jsonify({
            'statistics': statistics,
            'total_votes': total_votes,
            'voted_voters': voted_voters,
            'chart_generated': True,
            'chart_path': '/static/votes_chart.png'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_votes_chart(statistics):
    """Genera gráfica de votos usando pandas y matplotlib"""
    if not statistics:
        return
    
   
    df = pd.DataFrame(statistics)
    
    
    plt.figure(figsize=(12, 8))
    
    
    bars = plt.bar(df['candidate_name'], df['votes'], color='skyblue', edgecolor='black')
    
    
    plt.xlabel('Candidatos', fontsize=12, fontweight='bold')
    plt.ylabel('Votos', fontsize=12, fontweight='bold')
    plt.title('Resultados de la Votación - Distribución de Votos por Candidato', 
              fontsize=14, fontweight='bold', pad=20)
    
    
    plt.xticks(rotation=45, ha='right')
    
   
    for bar, votes, percentage in zip(bars, df['votes'], df['percentage']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{votes} votos\n({percentage}%)', 
                ha='center', va='bottom', fontsize=9)
    
    
    plt.tight_layout()
    
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
   
    plt.savefig('static/votes_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
