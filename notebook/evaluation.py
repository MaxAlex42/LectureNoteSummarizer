import nltk
from nltk import word_tokenize, pos_tag, wordpunct_tokenize
from nltk.corpus import stopwords as _stopwords
import textstat
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util

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
    Lower  ⇒ easier to read (we are aiming for at least 8).
    """
    return textstat.flesch_kincaid_grade(answer)

# evaluation.py
from collections import defaultdict

def find_exact_and_question_duplicates(df):
    """
    Returns two lists of indices:
      - exact duplicates (same question & same answer)
      - same-question-with-different-answer duplicates
    """
    seen_exact = set()
    seen_q = defaultdict(list)
    exact_dups = []
    question_dups = []

    for idx, row in df[["question", "answer"]].iterrows():
        q = row["question"].strip().lower()
        a = row["answer"].strip().lower()
        key = (q, a)

        if key in seen_exact:
            exact_dups.append(idx)
        else:
            seen_exact.add(key)

        seen_q[q].append((idx, a))

    for q, items in seen_q.items():
        answers = {a for _, a in items}
        if len(answers) > 1:
            question_dups.extend(idx for idx, _ in items)

    return exact_dups, question_dups

def find_semantic_question_duplicates(df, model_name="all-MiniLM-L6-v2", threshold=0.90):
    """
    Uses sentence-transformers to find pairs of questions whose
    cosine-similarity ≥ threshold. Returns list of (idx_i, idx_j, score).
    """
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer(model_name)
    qs = df["question"].tolist()
    embeds = model.encode(qs, convert_to_tensor=True)
    cos_mat = util.cos_sim(embeds, embeds)

    sem_dups = []
    n = len(qs)
    indices = list(df.index)
    for i in range(n):
        for j in range(i+1, n):
            score = cos_mat[i, j].item()
            if score >= threshold:
                sem_dups.append((indices[i], indices[j], score))

    return sem_dups

def compute_max_semantic_similarity(df, model_name="all-MiniLM-L6-v2"):
    """
    For each question in df, compute the max cosine-similarity
    to any *other* question, and return a dict {index: max_score}.
    """
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer(model_name)
    questions = df["question"].tolist()
    embeds = model.encode(questions, convert_to_tensor=True)

    cos_mat = util.cos_sim(embeds, embeds)

    idxs = list(df.index)
    max_scores = {}
    for i, idx in enumerate(idxs):
        row = cos_mat[i].clone().cpu()
        row[i] = -1.0
        max_scores[idx] = float(row.max().item())
    return max_scores
