import json
import pandas as pd
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from evaluation import (
    atomicity_score,
    conciseness_score,
    leakage_score,
    fk_grade,
    find_exact_and_question_duplicates,
    find_semantic_question_duplicates,
    compute_max_semantic_similarity
)

load_dotenv()

API_key = os.getenv('API_KEY')
client = genai.Client(api_key= API_key)

with open('summaries/esop.md', encoding='utf-8') as f:
    prompt = f.read()

with open('prompts.json', 'r') as f:
    data = json.load(f)

system_prompt = data['system_prompt_de']

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type= "application/json",),
    contents=prompt,
)

raw = response.text

cards = json.loads(raw)

df_cards = pd.DataFrame(cards)

rename_map = {
    "front": "question",
    "back":  "answer",
    "question": "question",
    "answer":   "answer",
    "frage": "question",
    "antwort": "answer",
}

df_cards.rename(columns={k: v for k, v in rename_map.items()
                         if k in df_cards.columns},
                inplace=True)

df_cards["atomicity_score"] = df_cards["question"].apply(atomicity_score)
df_cards["conciseness_score"] = df_cards["answer"].apply(conciseness_score)
df_cards["leakage_score"] = df_cards.apply(
    lambda row: leakage_score(row["question"], row["answer"]), axis=1
)
df_cards["fk_grade"]   = df_cards["answer"].apply(fk_grade)

exact_dups, question_dups = find_exact_and_question_duplicates(df_cards)
df_cards["is_exact_dup"]      = df_cards.index.isin(exact_dups)
max_sims = compute_max_semantic_similarity(df_cards, model_name="all-MiniLM-L6-v2")
df_cards["semantic_similarity"] = df_cards.index.map(max_sims)

threshold = 0.90
df_cards["is_semantic_dup"] = df_cards["semantic_similarity"] >= threshold    

print(df_cards[[
    "question", "answer",
    "atomicity_score", "conciseness_score",
    "leakage_score", "fk_grade",
    "semantic_similarity",
    "is_exact_dup"
]])