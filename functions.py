import spacy
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
# import contractions
from contractions import CONTRACTION_MAP
import unicodedata

# nlp = spacy.load('en_core_web_sm', parse=True, tag=True, entity=True)
nlp = spacy.load('en_core_web_sm')

from nltk.tokenize.toktok import ToktokTokenizer

tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')


# stopword_list.remove('no')
# stopword_list.remove('not')

def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def normalize_corpus(corpus, html_stripping=False, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True):
    normalized_corpus = []
    # normalize each document in the corpus
    for doc in corpus:
        doc = doc.replace("in'", "ing")
        doc = doc.replace("gonna", "going to")
        doc = doc.replace("wanna", "want to")
        doc = doc.replace("tryna", "trying to")
        # strip HTML
        if html_stripping:
            doc = strip_html_tags(doc)
        # remove accented characters
        if accented_char_removal:
            try:
                doc = remove_accented_chars(doc)
            except:
                doc = doc
        # expand contractions
        if contraction_expansion:
            try:
                doc = expand_contractions(doc)
            except:
                doc = doc
                # lowercase the text
        if text_lower_case:
            try:
                doc = doc.lower()
            except:
                doc = doc
        # remove extra newlines
        try:
            doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
        except:
            doc = doc
        # lemmatize text
        if text_lemmatization:
            try:
                doc = lemmatize_text(doc)
            except:
                doc = doc
        # remove special characters and\or digits
        if special_char_removal:
            try:
                # insert spaces between special characters to isolate them
                special_char_pattern = re.compile(r'([{.(-)!}])')
                doc = special_char_pattern.sub(" \\1 ", doc)
                doc = remove_special_characters(doc, remove_digits=remove_digits)
            except:
                doc = doc
        # remove extra whitespace
        try:
            doc = re.sub(' +', ' ', doc)
        except:
            doc = doc
        # remove stopwords
        if stopword_removal:
            try:
                doc = remove_stopwords(doc, is_lower_case=text_lower_case)
            except:
                doc = doc

        normalized_corpus.append(doc)

    return normalized_corpus