import nltk
from nltk import word_tokenize, pos_tag, wordpunct_tokenize
from nltk.corpus import stopwords as _stopwords
import textstat

RESOURCES = {
    "punkt":                       "tokenizers/punkt",
    "punkt_tab":                   "tokenizers/punkt_tab",
    "averaged_perceptron_tagger":  "taggers/averaged_perceptron_tagger_de",
    "stopwords":                   "corpora/stopwords",
}
for res, path in RESOURCES.items():
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(res, quiet=True)

STOPWORDS = set(_stopwords.words("german"))

def atomicity_score(question: str) -> float:
    tokens = wordpunct_tokenize(question)

    try:
        from nltk import pos_tag
        tags = pos_tag(tokens)  
    except LookupError:
        tags = [(tok, "") for tok in tokens]

    verbs = sum(tag.startswith("VB") for _, tag in tags)
    conjs = sum(tok.lower() in {"und", "oder"} for tok in tokens)

    score = 1.0 \
        - 0.4 * max(0, verbs - 1) \
        - 0.3 * conjs \
        - 0.2 * (len(tokens) > 20)
    return max(0.0, min(1.0, score))

def conciseness_score(answer: str) -> float:
    """
    Is the answer short enough to be rememberable?
    Current limits: 
        - 1.0 (<= 10 tokens)
        - 0.7 (11 - 20)
        - 0.4 (> 20)
    """
    n = len(word_tokenize(answer))
    return 1.0 if n <= 10 else 0.7 if n <= 20 else 0.4

def _content_words(text: str) -> set[str]:
    return {
        w.lower() for w in word_tokenize(text)
        if w.isalpha() and w.lower() not in STOPWORDS
    }

def leakage_score(question: str, answer: str) -> float:
    """
    Jaccard overlap/index - how much of the answers words appear in the question already.
    0 - 1, >= 0.6 is minimal overlap
    """
    q, a = _content_words(question), _content_words(answer)
    if not q or not a:
        return 1.0
    jacc = len(q & a) / len(q | a)
    return 1.0 - jacc


def fk_grade(answer: str) -> float:
    """
    Flesch-Kincaid **Grade Level** of the answer.
    Lower  ⇒ easier to read (we are aiming for 10 <= g <= 14).
    """
    return textstat.flesch_kincaid_grade(answer)