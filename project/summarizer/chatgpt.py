import json
import os
import pandas as pd
from evaluation import (
    atomicity_score,
    conciseness_score,
    leakage_score,
    fk_grade,
)

# 1. JSON-Datei mit Lernkarten laden
with open('cardsgpt/esop-gpt.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# 2. In DataFrame umwandeln
df_cards = pd.DataFrame(cards)

# 3. Optional: Spaltennamen anpassen (für Kompatibilität mit anderen Formaten)
rename_map = {
    "front": "question",
    "back": "answer",
    "frage": "question",
    "antwort": "answer"
}

df_cards.rename(columns={k: v for k, v in rename_map.items()
                         if k in df_cards.columns},
                inplace=True)

# 4. Evaluation durchführen
df_cards["atomicity_score"] = df_cards["question"].apply(atomicity_score)
df_cards["conciseness_score"] = df_cards["answer"].apply(conciseness_score)
df_cards["leakage_score"] = df_cards.apply(
    lambda row: leakage_score(row["question"], row["answer"]), axis=1
)
df_cards["fk_grade"] = df_cards["answer"].apply(fk_grade)

# 5. Ergebnisse anzeigen
print(
    df_cards[
        ["question", "answer", "atomicity_score", "conciseness_score", "leakage_score", "fk_grade"]
    ]
)
