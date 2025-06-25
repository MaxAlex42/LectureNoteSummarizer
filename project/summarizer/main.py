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
)

load_dotenv()

API_key = os.getenv('API_KEY')
client = genai.Client(api_key= API_key)

with open('summaries/arrays.md') as f:
    prompt = f.read()

with open('prompts.json', 'r') as f:
    data = json.load(f)

system_prompt = data['system_prompt_de']
system_prompt="""

**Rolle:** Du bist ein Experte für Didaktik und Wissensaufbereitung. Deine Spezialität ist die Erstellung von hochwirksamen Lernmaterialien, insbesondere von digitalen Lernkarten (Flashcards). 
    Du verstehst, dass der Lernerfolg am größten ist, wenn Informationen in kleinen, gut verdaulichen Einheiten präsentiert werden.

**Ziel:** Dein Ziel ist es, aus dem unten bereitgestellten Text eine Serie von Lernkarten zu generieren, die für maximalen Lernerfolg optimiert sind.

**Anweisungen & Regeln:**


1. **Klarheit und Prägnanz:** Die Informationen auf den Karten sollten klar und eindeutig formuliert sein. Vermeide lange Sätze und unnötige Füllwörter. 
2. **Fokus auf das Wesentliche:** Konzentriere dich auf die wichtigsten Informationen und vermeide es, die Karten mit zu vielen Details zu überladen. 
3. **Stichworte und Schlüsselwörter:** Nutze Stichwörter oder kurze Sätze, um wichtige Informationen zu erfassen und den Lernprozess zu unterstützen. 
4. **Atomarität:** ein Kernthema pro Karte - vermeide überladene Karten. Ausnahmen gibt es bei Themen, die ineinander greifen.
5. **Gewährung des Zusammenhangs:** Der Zusammenhang der Themen sollte nicht verloren gehen. Unverbundenes Detailwissen sollte vermieden werden.
6. **Wiedererkennungswert:** Die Frage muss als klarer Trigger funktionieren: Sie sollte helfen, eine spezifische Erinnerung zu aktivieren.
7.  **Format:** Gib jede Lernkarte im folgenden Format aus und trenne die Karten durch `---`.

    Frage: [Deine Frage hier]
    Antwort: [Deine Antwort hier]
    ---

**Ausführliche Beispiele:**

**Beispiel: Falsche Anwendung (zu viele Informationen pro Karte)**

*   **Input-Satz:** "Der photoelektrische Effekt, der 1905 von Albert Einstein entscheidend erklärt wurde, beschreibt die Freisetzung von Elektronen aus einem Material, wenn Licht darauf trifft."
*   **FALSCHE, NICHT-ATOMARE LERNKARTE (SO NICHT!):**

    Frage: Erkläre den photoelektrischen Effekt.
    Antwort: Der photoelektrische Effekt wurde 1905 von Albert Einstein erklärt und beschreibt die Freisetzung von Elektronen aus einem Material, wenn Licht darauf trifft.
    *(Grund für Fehler: Diese Antwort testet drei Fakten gleichzeitig: Was, Wer, Wann. Das widerspricht dem Mindestprinzip.)*
    ---

---
**Beispiel: Anwendung der kontextbewussten Flexibilität**

*   **Input-Satz:** "Bei der Osmose bewegt sich ein Lösungsmittel, typischerweise Wasser, durch eine semipermeable Membran von einem Bereich niedrigerer Konzentration gelöster Stoffe zu einem Bereich höherer Konzentration."
*   **KORREKTE, FLEXIBLE LERNKARTEN:**

    Frage: Was bewegt sich bei der Osmose durch eine semipermeable Membran?
    Antwort: Ein Lösungsmittel (typischerweise Wasser).
    ---
    Frage: In welche Richtung bewegt sich das Lösungsmittel bei der Osmose?
    Antwort: Von einem Bereich niedrigerer Konzentration gelöster Stoffe zu einem Bereich höherer Konzentration.
    

**Dein Auftrag:**
Analysiere nun den folgenden Text und erstelle eine Lernkarte pro Kernthema gemäß den oben genannten Prinzipien und Beispielen. 


"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json"),
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
    "frage":  "question",
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

print(
    df_cards[
        ["question", "answer", "atomicity_score", "conciseness_score", "leakage_score", "fk_grade"]
    ].head()
)
        system_instruction=system_prompt),
    contents="""
Christoph Kolumbus (italienisch Cristoforo Colombo, spanisch Cristóbal Colón, portugiesisch Cristóvão Colombo, latinisiert Christophorus Columbus; 
* um 1451 in der Republik Genua; † 20. Mai 1506 in Valladolid, Königreich Kastilien) war ein italienischer Seefahrer in kastilischen Diensten, der über den Atlantik einen westlichen 
Seeweg nach Indien finden wollte und im Oktober 1492 eine Insel der Bahamas erreichte, dann weitere Karibikinseln. Dies wird im Allgemeinen als die Entdeckung Amerikas 1492 angesehen. 
Es folgten weitere Eroberungsreisen, und er wurde der erste Vizekönig der las Indias genannten Gebiete.

Im Wettlauf mit Portugal um den Seeweg nach Indien im Rahmen des Indienhandels wollte Kolumbus den Weg im Westen erschließen. Das Ziel seiner ersten Entdeckungsreise war die Hafenstadt Quinsay 
in China, das im damaligen Sprachgebrauch zu Indien gezählt wurde.

Auf seinen vier Entdeckungsreisen zwischen 1492 und 1504 steuerte Kolumbus vor allem die Großen Antillen an, darunter bei allen vier Reisen Hispaniola (heute Haiti und Dominikanische Republik), 
wo er erste Kolonien gründete. Erst auf seiner vierten Reise betrat er im heutigen Honduras amerikanisches Festland. Kolumbus hat zeitlebens nicht erkannt, dass es sich um einen bis dahin 
unbekannten Kontinent handelte. Diese Auffassung vertrat erst Amerigo Vespucci, nach dem die Neue Welt schließlich Amerika benannt wurde.

Die ersten Entdecker Amerikas waren die Vorfahren der indigenen Bevölkerung Amerikas, die vor langer Zeit von Asien her in den zuvor menschenleeren Kontinent eindrangen 
(siehe Besiedlung Amerikas). Außerdem wurde Nordamerika schon rund 500 Jahre vor Kolumbus von Leif Eriksson und anderen Wikingern besucht, die zeitweilig auch dort siedelten. 
Wenn Kolumbus gleichwohl bis heute als maßgeblicher europäischer Entdecker Amerikas gilt, ist das darauf zurückzuführen, dass erst seine Reisen die dauerhafte Kolonisierung und 
Besiedlung des amerikanischen Doppelkontinents durch Europäer und Menschen aus anderen Kontinenten in geschichtlicher Zeit zur Folge hatten. 

"""
)

print(response.text)


