import os
import pandas as pd
import re
from collections import Counter
import nltk
from textblob import TextBlob
nltk.download('punkt', quiet=True)

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'articles')
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'results.xlsx')
INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assignemnt', 'Test_Assignment', 'Input.xlsx')

# Load input for URL_ID and URL
input_df = pd.read_excel(INPUT_PATH)

# Prepare output columns (from Output Data Structure.xlsx)
output_columns = list(input_df.columns) + [
    'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

# Placeholder for loading positive/negative words, stopwords, etc.
def load_dictionaries():
    # Load positive words
    pos_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assignemnt', 'Test_Assignment', 'MasterDictionary', 'positive-words.txt')
    with open(pos_path, 'r', encoding='ISO-8859-1') as f:
        pos_words = set([line.strip().lower() for line in f if line.strip() and not line.startswith(';')])
    # Load negative words
    neg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assignemnt', 'Test_Assignment', 'MasterDictionary', 'negative-words.txt')
    with open(neg_path, 'r', encoding='ISO-8859-1') as f:
        neg_words = set([line.strip().lower() for line in f if line.strip() and not line.startswith(';')])
    # Load all stopwords from StopWords_*.txt
    stopwords = set()
    stopwords_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'assignemnt', 'Test_Assignment', 'StopWords')
    for fname in os.listdir(stopwords_dir):
        if fname.endswith('.txt'):
            with open(os.path.join(stopwords_dir, fname), 'r', encoding='ISO-8859-1') as f:
                stopwords.update([line.strip().lower() for line in f if line.strip()])
    return pos_words, neg_words, stopwords

def count_syllables(word):
    word = word.lower()
    vowels = 'aeiouy'
    count = 0
    prev_char_was_vowel = False
    for char in word:
        if char in vowels:
            if not prev_char_was_vowel:
                count += 1
            prev_char_was_vowel = True
        else:
            prev_char_was_vowel = False
    if word.endswith('e'):
        count = max(1, count-1)
    return max(count, 1)

def is_complex(word):
    return count_syllables(word) > 2

def count_personal_pronouns(text):
    # Standard set for English
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    return len(re.findall(pronoun_pattern, text, re.I))

def analyze_text(text, pos_words, neg_words, stopwords):
    # Remove title (first line)
    lines = text.split('\n')
    if len(lines) > 1:
        text_body = '\n'.join(lines[1:])
    else:
        text_body = text
    blob = TextBlob(text_body)
    sentences = nltk.sent_tokenize(text_body)
    words = [w for w in nltk.word_tokenize(text_body) if w.isalpha()]
    words_lower = [w.lower() for w in words]
    # Remove stopwords for word count
    filtered_words = [w for w in words_lower if w not in stopwords]
    # Sentiment scores
    pos_score = sum(1 for w in filtered_words if w in pos_words)
    neg_score = sum(1 for w in filtered_words if w in neg_words)
    # Polarity and subjectivity (TextBlob)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    # Sentence and word stats
    num_sentences = len(sentences) if sentences else 1
    num_words = len(filtered_words)
    avg_sentence_length = num_words / num_sentences if num_sentences else 0
    # Complex words
    complex_words = [w for w in filtered_words if is_complex(w)]
    percent_complex = (len(complex_words) / num_words) if num_words else 0
    fog_index = 0.4 * (avg_sentence_length + (percent_complex * 100))
    avg_words_per_sentence = avg_sentence_length
    complex_word_count = len(complex_words)
    word_count = num_words
    syllable_per_word = (sum(count_syllables(w) for w in filtered_words) / num_words) if num_words else 0
    personal_pronouns = count_personal_pronouns(text_body)
    avg_word_length = (sum(len(w) for w in filtered_words) / num_words) if num_words else 0
    return {
        'POSITIVE SCORE': pos_score,
        'NEGATIVE SCORE': neg_score,
        'POLARITY SCORE': polarity,
        'SUBJECTIVITY SCORE': subjectivity,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percent_complex * 100,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

def main():
    # Get the exact output columns from Output Data Structure.xlsx
    ods_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'ods_columns.csv')
    with open(ods_csv, 'r', encoding='utf-8') as f:
        header = f.readline().strip().split(',')
    pos_words, neg_words, stopwords = load_dictionaries()
    results = []
    for idx, row in input_df.iterrows():
        url_id = row['URL_ID']
        article_path = os.path.join(ARTICLES_DIR, f"{url_id}.txt")
        if not os.path.exists(article_path):
            print(f"Missing article for {url_id}")
            continue
        with open(article_path, 'r', encoding='utf-8') as f:
            text = f.read()
        analysis = analyze_text(text, pos_words, neg_words, stopwords)
        # Build result row in the correct order
        result_row = {col: '' for col in header}
        for col in input_df.columns:
            result_row[col] = row[col]
        for col in analysis:
            result_row[col] = analysis[col]
        results.append(result_row)
    output_df = pd.DataFrame(results, columns=header)
    output_df.to_excel(OUTPUT_PATH, index=False)
    output_df.to_csv(os.path.join(os.path.dirname(OUTPUT_PATH), 'results.csv'), index=False)
    print(f"Analysis complete. Results saved to {OUTPUT_PATH} and results.csv")

if __name__ == '__main__':
    main() 