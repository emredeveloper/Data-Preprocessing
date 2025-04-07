import os
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from arxiv_analysis import fetch_arxiv_papers, analyze_with_ollama, get_papers_for_app, compare_with_previous_analysis

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/api/papers')
def get_papers():
    """API endpoint to get papers"""
    papers = get_papers_for_app()
    return jsonify(papers)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze papers"""
    data = request.get_json()
    papers = data.get('papers', [])
    model = data.get('model', 'gemma3')
    compare = data.get('compare', False)
    
    try:
        analysis = analyze_with_ollama(papers, model)
        
        # Get comparison with previous analyses if requested
        comparison_data = None
        if compare:
            comparison_data = compare_with_previous_analysis(papers, analysis)
            
        return jsonify({
            'success': True, 
            'analysis': analysis,
            'comparison': comparison_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/papers')
def papers_page():
    """Render the papers page"""
    return render_template('papers.html', current_year=datetime.now().year)

@app.route('/analysis')
def analysis_page():
    """Render the analysis page"""
    return render_template('analysis.html', current_year=datetime.now().year)

@app.route('/paper/<paper_id>')
def paper_details(paper_id):
    """Render individual paper details"""
    papers = get_papers_for_app()
    paper = next((p for p in papers if p['id'] == paper_id), None)
    if paper:
        return render_template('paper_details.html', paper=paper, current_year=datetime.now().year)
    return render_template('404.html', current_year=datetime.now().year), 404

if __name__ == '__main__':
    app.run(debug=True)
