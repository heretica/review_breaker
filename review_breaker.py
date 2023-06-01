#!/usr/bin/env python
# coding: utf-8

# In[25]:


import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from collections import Counter
import markdown
from bs4 import BeautifulSoup


# In[26]:


# Fonction pour calculer le nombre de mots dans un texte
def word_count(text):
    tokens = word_tokenize(text)
    word_count = len(tokens)
    return word_count

# Fonction pour calculer la structure des articles
def article_structure(article):
    section_count = article.count("Section:")
    subsection_count = article.count("Subsection:")
    return section_count, subsection_count

# Fonction pour analyser le style d'écriture
def analyze_writing_style(article):
    # Calcul de la longueur moyenne des phrases
    sentences = nltk.sent_tokenize(article)
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
    average_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

    # Analyse de la densité d'informations
    word_tokens = word_tokenize(article)
    word_tokens = [token.lower() for token in word_tokens if token.isalpha()]
    word_tokens = [token for token in word_tokens if token not in stopwords.words('french')]
    word_count = len(word_tokens)
    unique_words = set(word_tokens)
    vocabulary_size = len(unique_words)
    lexical_density = vocabulary_size / word_count

    return average_sentence_length, lexical_density

# Fonction pour étudier le vocabulaire et la terminologie
def analyze_vocabulary(article):
    word_tokens = word_tokenize(article)
    word_tokens = [token.lower() for token in word_tokens if token.isalpha()]
    word_tokens = [token for token in word_tokens if token not in stopwords.words('french')]

    # Calcul de la fréquence des mots
    fdist = FreqDist(word_tokens)
    most_common_words = fdist.most_common(10)

    # Calcul des bigrammes les plus fréquents
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(word_tokens)
    most_common_bigrams = finder.nbest(bigram_measures.pmi, 10)

    return most_common_words, most_common_bigrams

# Fonction pour évaluer la cohérence argumentative
def evaluate_argument_coherence(article):
    # Exemple de logique pour évaluer la cohérence argumentative
    # Ici, nous supposons que l'article est constitué de plusieurs paragraphes
    # Nous vérifions si chaque paragraphe commence par une phrase d'introduction et se termine par une phrase de conclusion

    paragraphs = article.split("\n\n")  # Supposons que les paragraphes sont séparés par des lignes vides

    coherence_score = 0
    num_paragraphs = len(paragraphs)
    for paragraph in paragraphs:
        sentences = nltk.sent_tokenize(paragraph)
        if len(sentences) > 2:
            # Vérification de la cohérence argumentative
            if sentences[0].endswith(":") and sentences[-1].endswith("."):
                coherence_score += 1

    coherence_score /= num_paragraphs  # Normalisation du score

    return coherence_score

# Fonction pour évaluer la qualité de la rédaction
def evaluate_writing_quality(article):
    from language_tool_python import LanguageTool

    tool = LanguageTool('fr')
    errors = tool.check(article)
    num_errors = len(errors)

    quality_score = 1 - (num_errors / word_count(article))

    return quality_score






# In[27]:


with open('premiere_review.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text)


with open('premiere_review.html', 'w') as f:
    f.write(html)

with open('premiere_review.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')
    article1 = soup.get_text()
    #print(text1)


# In[28]:


with open('seconde_review.md', 'r') as f:
    text = f.read()
    html = markdown.markdown(text)


with open('seconde_review.html', 'w') as f:
    f.write(html)

with open('seconde_review.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')
    article2 = soup.get_text()
    #print(text2)


# In[29]:


# Analyse de l'article 1
word_count_article1 = word_count(article1)
section_count_article1, subsection_count_article1 = article_structure(article1)
average_sentence_length_article1, lexical_density_article1 = analyze_writing_style(article1)
most_common_words_article1, most_common_bigrams_article1 = analyze_vocabulary(article1)
coherence_score_article1 = evaluate_argument_coherence(article1)
quality_score_article1 = evaluate_writing_quality(article1)

# Analyse de l'article 2
word_count_article2 = word_count(article2)
section_count_article2, subsection_count_article2 = article_structure(article2)
average_sentence_length_article2, lexical_density_article2 = analyze_writing_style(article2)
most_common_words_article2, most_common_bigrams_article2 = analyze_vocabulary(article2)
coherence_score_article2 = evaluate_argument_coherence(article2)
quality_score_article2 = evaluate_writing_quality(article2)

# Affichage des résultats
print("Analyse de l'article en cours d'évaluation:")
print("Nombre de mots:", word_count_article1)
print("Longueur moyenne des phrases:", average_sentence_length_article1)
print("Densité lexicale:", lexical_density_article1)
print("Bigrammes les plus fréquents:", most_common_bigrams_article1)
print("Score de qualité de rédaction:", quality_score_article1)

print("\nAnalyse de l'article publié:")
print("Nombre de mots:", word_count_article2)
print("Longueur moyenne des phrases:", average_sentence_length_article2)
print("Densité lexicale:", lexical_density_article2)
print("Bigrammes les plus fréquents:", most_common_bigrams_article2)
print("Score de qualité de rédaction:", quality_score_article2)

