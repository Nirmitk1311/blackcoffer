# Blackcoffer Text Analysis Solution

## Approach

This solution was designed to strictly follow the assignment objectives and ensure clarity, modularity, and originality. The approach is divided into two main phases: data extraction and data analysis.

### 1. Data Extraction
- **Read Input:** The script reads all URLs and their corresponding URL_IDs from `Input.xlsx`.
- **Web Scraping:** For each URL, the script fetches the web page and extracts only the article title and main text, avoiding headers, footers, and ads. This is done using BeautifulSoup (with a placeholder for Selenium if needed for dynamic content).
- **Save Articles:** Each article is saved as a text file named `{URL_ID}.txt` in the `solution/output/articles/` directory. This ensures traceability and easy access for further analysis.

### 2. Data Analysis
- **Dictionary Loading:** The script loads positive and negative word lists from the provided MasterDictionary, and aggregates all stopwords from the StopWords directory.
- **Text Processing:** For each article, the script computes all required variables as defined in the assignment (e.g., POSITIVE SCORE, NEGATIVE SCORE, POLARITY SCORE, FOG INDEX, etc.). Standard NLP libraries (NLTK, TextBlob) are used for tokenization and sentiment analysis, and custom logic is used for metrics like syllable count and complex word detection.
- **Output Structure:** The results for all articles are compiled into a DataFrame with columns matching exactly the structure and order of `Output Data Structure.xlsx`.
- **Export:** The final results are saved in both Excel (`results.xlsx`) and CSV (`results.csv`) formats in the `solution/output/` directory, ensuring compatibility with the required output format.

### 3. Modularity & Documentation
- The code is modular, with clear separation between extraction and analysis.
- All dependencies are listed in `requirements.txt`.
- This README provides instructions and a summary of the approach, ensuring the solution is easy to understand and reproduce.

## How to Run

1. Install dependencies:
   ```
   pip install -r solution/requirements.txt
   ```
2. Extract articles:
   ```
   python solution/extract_articles.py
   ```
3. Analyze articles and generate output:
   ```
   python solution/analyze_texts.py
   ```
4. Find the results in `solution/output/results.csv` and `results.xlsx`.

## Dependencies

See `solution/requirements.txt` for all required Python packages. 