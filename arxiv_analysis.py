import requests
import re
from bs4 import BeautifulSoup
import json
import ollama
import pandas as pd
from datetime import datetime
import os
import time
import glob
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data if not already available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def fetch_arxiv_papers(url="https://arxiv.org/list/stat.ML/recent", num_papers=20):
    """Fetch recent papers from arXiv's stat.ML category"""
    print(f"Fetching papers from {url}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all paper entries (dlpage is the class for the listings page)
    papers = []
    
    # Find all dt elements (contain paper IDs)
    dt_elements = soup.find_all('dt')
    
    for i, dt in enumerate(dt_elements):
        if i >= num_papers:
            break
            
        # Get the next dd element which contains paper details
        dd = dt.find_next_sibling('dd')
        
        if not dd:
            continue
            
        # Extract paper ID
        arxiv_id_match = re.search(r'arXiv:(\d+\.\d+)', dt.text)
        if not arxiv_id_match:
            continue
        arxiv_id = arxiv_id_match.group(1)
        
        # Extract title
        title_element = dd.find('div', class_='list-title')
        title = title_element.text.replace('Title:', '').strip() if title_element else "No title found"
        
        # Extract authors
        authors_element = dd.find('div', class_='list-authors')
        authors = authors_element.text.replace('Authors:', '').strip() if authors_element else "No authors found"
        
        # Extract abstract (shown in the comments section)
        abstract_element = dd.find('p', class_='mathjax')
        abstract = abstract_element.text.strip() if abstract_element else "No abstract found"
        
        # Create PDF link
        pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        
        # Generate a short description (either from abstract or using Ollama if available)
        description = "No description available"
        if abstract and abstract != "No abstract found":
            # Use first 2 sentences or 200 chars of abstract as description
            sentences = abstract.split('. ')
            if len(sentences) > 1:
                description = '. '.join(sentences[:2]) + '.'
            else:
                description = abstract[:200] + ('...' if len(abstract) > 200 else '')
        
        # Add category and publication date for better UI display
        categories = dd.find('div', class_='list-subjects')
        category = categories.text.replace('Subjects:', '').strip() if categories else "stat.ML"
        
        # Get submission date if available
        date_element = dd.find('div', class_='list-date')
        pub_date = date_element.text.replace('Submitted:', '').strip() if date_element else datetime.now().strftime("%d %b %Y")
        
        papers.append({
            'id': arxiv_id,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'description': description,
            'pdf_link': pdf_link,
            'category': category,
            'pub_date': pub_date,
            'arxiv_link': f"https://arxiv.org/abs/{arxiv_id}"
        })
    
    print(f"Fetched {len(papers)} papers")
    return papers

def analyze_with_ollama(papers, model="gemma3"):
    """Use Ollama to analyze paper titles and identify trends"""
    if not papers:
        return "No papers to analyze"
    
    titles = [paper['title'] for paper in papers]
    titles_text = "\n".join(titles)
    
    # Get current date for the prompt
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Extract keywords from titles for better context
    keywords = extract_keywords_from_titles(titles)
    top_keywords = ", ".join([k for k, _ in keywords[:10]])
    
    prompt = f"""
    You are a research analyst specializing in machine learning. 
    Analyze the following {len(titles)} recent paper titles from arXiv's stat.ML category:
    
    {titles_text}
    
    Today's date is {current_date}.
    
    The top keywords extracted from these papers are: {top_keywords}
    
    Provide a concise analysis (around 400 words) covering:
    1. Main research themes and trends
    2. Most common topics/methods/algorithms
    3. Emerging research directions
    4. Any notable shifts from previous trends in ML research
    
    Format your response as a proper analysis report with sections.
    Include the current date ({current_date}) in your heading.
    """
    
    print("Analyzing papers with Ollama...")
    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        return response['message']['content']
    except Exception as e:
        print(f"Error using Ollama: {e}")
        return f"Error in analysis: {str(e)}"

def extract_keywords_from_titles(titles):
    """Extract and rank keywords from paper titles"""
    # Join all titles
    all_text = ' '.join(titles).lower()
    
    # Tokenize
    tokens = word_tokenize(all_text)
    
    # Remove stopwords and non-alphanumeric tokens
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [
        word for word in tokens 
        if word.isalnum() and 
        word not in stop_words and 
        len(word) > 2
    ]
    
    # Count frequencies
    word_freq = Counter(filtered_tokens)
    
    # Return most common keywords
    return word_freq.most_common(20)

def compare_with_previous_analysis(current_papers, current_analysis):
    """Compare current papers and analysis with previous ones"""
    # Load all previous JSON files
    json_files = glob.glob('arxiv_analysis_*.json')
    
    if not json_files:
        return {
            "status": "No previous analyses found for comparison",
            "trend_change": None,
            "keywords_comparison": None
        }
    
    # Sort by date (newest first, but not including the current one)
    json_files.sort(reverse=True)
    
    # Load the most recent previous analysis
    try:
        with open(json_files[0], 'r') as f:
            previous_papers = json.load(f)
    except Exception as e:
        return {
            "status": f"Error loading previous analysis: {str(e)}",
            "trend_change": None,
            "keywords_comparison": None
        }
    
    # Extract keywords from both sets
    current_titles = [paper['title'] for paper in current_papers]
    previous_titles = [paper['title'] for paper in previous_papers]
    
    current_keywords = extract_keywords_from_titles(current_titles)
    previous_keywords = extract_keywords_from_titles(previous_titles)
    
    # Create sets of current and previous top keywords (top 15)
    current_top_keywords = set([k for k, _ in current_keywords[:15]])
    previous_top_keywords = set([k for k, _ in previous_keywords[:15]])
    
    # Find new and disappeared keywords
    new_keywords = current_top_keywords - previous_top_keywords
    disappeared_keywords = previous_top_keywords - current_top_keywords
    
    # Calculate keyword ranking changes
    previous_keyword_dict = {k: (15-i) for i, (k, _) in enumerate(previous_keywords[:15])}
    current_keyword_dict = {k: (15-i) for i, (k, _) in enumerate(current_keywords[:15])}
    
    trending_up = []
    trending_down = []
    
    for keyword, current_rank_value in current_keyword_dict.items():
        if keyword in previous_keyword_dict:
            previous_rank_value = previous_keyword_dict[keyword]
            change = current_rank_value - previous_rank_value
            if change > 3:  # Significantly trending up
                trending_up.append(keyword)
            elif change < -3:  # Significantly trending down
                trending_down.append(keyword)
    
    # Generate comparison insights with Ollama
    try:
        # First, check if we have a previous analysis text file
        txt_filename = json_files[0].replace('.json', '.txt')
        previous_analysis_text = ""
        if os.path.exists(txt_filename):
            with open(txt_filename, 'r') as f:
                content = f.read()
                # Extract just the analysis part
                if "ANALYSIS:" in content:
                    previous_analysis_text = content.split("ANALYSIS:")[1].strip()
        
        if previous_analysis_text:
            # Generate insights comparing both analyses
            prompt = f"""
            Compare these two research trend analyses for arXiv ML papers:

            PREVIOUS ANALYSIS:
            {previous_analysis_text}

            CURRENT ANALYSIS:
            {current_analysis}

            What are the main differences in research trends? Keep your response under 200 words.
            Focus on:
            1. New emerging topics
            2. Topics that are no longer trending
            3. Shifts in research focus
            """
            
            response = ollama.chat(model="gemma3", messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ])
            
            trend_comparison = response['message']['content']
        else:
            trend_comparison = "No previous analysis text found for comparison"
    except Exception as e:
        trend_comparison = f"Error generating comparison: {str(e)}"
    
    # Return comparison data
    return {
        "status": "success",
        "previous_date": json_files[0].split('_')[1][:8],  # Extract date from filename
        "new_keywords": list(new_keywords),
        "disappeared_keywords": list(disappeared_keywords),
        "trending_up": trending_up,
        "trending_down": trending_down,
        "trend_comparison": trend_comparison
    }

def save_to_file(papers, analysis, filename=None):
    """Save the papers and analysis to a file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arxiv_analysis_{timestamp}"
    
    # Save papers as JSON
    with open(f"{filename}.json", "w") as f:
        json.dump(papers, f, indent=2)
    
    # Save analysis as text
    with open(f"{filename}.txt", "w") as f:
        f.write("ARXIV STAT.ML PAPERS ANALYSIS\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Number of papers analyzed: {len(papers)}\n\n")
        f.write("PAPER TITLES:\n")
        f.write("-" * 40 + "\n")
        for i, paper in enumerate(papers, 1):
            f.write(f"{i}. {paper['title']}\n")
        
        f.write("\n\n")
        f.write("ANALYSIS:\n")
        f.write("-" * 40 + "\n")
        f.write(analysis)
    
    print(f"Results saved to {filename}.json and {filename}.txt")

# Add a function to get papers for the Flask app
def get_papers_for_app():
    """Get papers for the Flask app or load from a cache file"""
    cache_file = 'paper_cache.json'
    
    # Check if cache exists and is less than 1 hour old
    try:
        if os.path.exists(cache_file):
            file_time = os.path.getmtime(cache_file)
            if (time.time() - file_time) < 3600:  # 1 hour in seconds
                with open(cache_file, 'r') as f:
                    return json.load(f)
    except Exception as e:
        print(f"Error reading cache: {e}")
    
    # Fetch new data
    papers = fetch_arxiv_papers(num_papers=20)
    
    # Save to cache
    try:
        with open(cache_file, 'w') as f:
            json.dump(papers, f, indent=2)
    except Exception as e:
        print(f"Error writing cache: {e}")
        
    return papers

def main():
    print("Starting arXiv stat.ML papers analysis...")
    
    # Fetch papers
    papers = fetch_arxiv_papers(num_papers=20)
    
    if not papers:
        print("Failed to fetch papers. Exiting.")
        return
    
    # Display the fetched paper titles
    print("\nFetched Paper Titles:")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}")
    
    # Analyze with Ollama
    try:
        analysis = analyze_with_ollama(papers)
        print("\nAnalysis Results:")
        print(analysis)
        
        # Save to file
        save_to_file(papers, analysis)
        
        # Compare with previous analysis
        comparison = compare_with_previous_analysis(papers, analysis)
        print("\nComparison with Previous Analysis:")
        print(comparison)
        
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
