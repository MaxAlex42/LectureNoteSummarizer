from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv('API_KEY')


client = genai.Client(api_key= API_key)

system_prompt="""
Du bist ein professioneller Lerncoach und darauf spezialisiert, aus Lerntexten effektive Karteikarten zu erstellen. 
Deine Aufgabe ist es, aus dem folgenden Fachtext mehrere Lernkarten im Frage-Antwort-Format zu erzeugen. Achte dabei auf folgende Kriterien:

- Verwende **nur ein Kernthema pro Karte** (z. B. eine Definition, eine Formel, ein Konzept).
- **Formuliere die Inhalte neu** in einfachen, klaren Worten. **Kein direktes Abschreiben**.
- Nutze **einfache, eindeutige Sprache**, sodass Frage und Antwort auch **nach Wochen noch verständlich** und erinnerbar sind.
- Vermeide Mehrdeutigkeiten oder komplexe Satzkonstruktionen.
- Die **Frage auf der Vorderseite** muss als klarer Trigger funktionieren: Sie sollte helfen, eine spezifische Erinnerung zu aktivieren.
- Die **Antwort soll so kurz wie möglich** sein – ein Satz, ein Begriff, eine Formel, aber inhaltlich korrekt und vollständig.
- Wende das **Mindestprinzip** an: Besser viele kleine Karten mit klaren Einzelinformationen als wenige überladene Karten.

- die Lernkarten dienen als Simulation zur Prüfung. Gib deshalb auch spezifische Aufgaben, die ähnlich bei einer Prüfung abgefragt werden könnten.


"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt),
    contents="""
Zusammenfassung: 06 Arrays

1. Grundlagen von Arrays
------------------------
Definition:
Ein Array ist eine Datenstruktur, die eine feste Anzahl von Werten desselben Datentyps in einer geordneten Folge speichert.

Zweck:
Wird benötigt, wenn man nicht nur einen einzelnen Wert, sondern eine ganze Sequenz von Werten verarbeiten muss (z.B. eine Liste von Messwerten, eine Sammlung von Namen).

Dimensionen:
- Eindimensional: Eine einfache Liste von Werten.
- Mehrdimensional: Eine Tabelle (2D) oder ein Würfel (3D), bei denen die Elemente selbst wieder Arrays sind.

2. Eindimensionale Arrays (1D)
-----------------------------
Deklaration:
int[] a;

Erzeugung (Instanziierung):
a = new int[10]; // Erzeugt ein Array für 10 Integer.

Zugriff auf Elemente (Indizierung):
- Zugriff über Index in eckigen Klammern: a[0] = 11;
- Index beginnt bei 0, gültige Indizes: 0 bis N-1 bei Länge N

Eigenschaft length:
for (int i=0; i < a.length; i++) { ... }

Initialisierung bei Deklaration:
int[] fivePrimes = {2, 3, 5, 7, 11};

Wichtige Regeln & Fehlerquellen:
- Typkonsistenz: z.B. kein double in int[]: a[2] = 33.33; // Fehler
- Array-Grenzen: a[10] bei Länge 10 → IndexOutOfBoundsException

3. Arrays, Referenzen und Speicherverwaltung
-------------------------------------------
Arrays als Referenztypen:
Array-Variable speichert die Adresse des Speicherbereichs, nicht die Daten selbst.

Zuweisung:
int[] b = a; // b zeigt auf dasselbe Array wie a

Folge:
Änderungen über b wirken sich auch auf a aus.

Garbage Collection:
- a = null;
- a = new int[20]; // alte Referenz wird verworfen

4. Zweidimensionale Arrays (2D)
-------------------------------
Konzept:
Ein 2D-Array ist ein Array von Arrays (z.B. eine Tabelle).

Deklaration & Erzeugung:
int[][] a = new int[3][4];

Zugriff:
a[1][1] = 6; // zweite Zeile, zweite Spalte

length-Eigenschaften:
- a.length: Anzahl der Zeilen
- a[0].length: Anzahl der Spalten (erste Zeile)

Initialisierung:
int[][] a = { {1,2,3}, {4,5,6}, {7,8,9} };

Fortgeschritten:
- Jagged Arrays (unregelmäßige Zeilenlängen möglich, aber unüblich)
- Mehrdimensionale Arrays (z.B. float[][][])

5. Iteration über Arrays
------------------------
Klassische for-Schleife:
for (int i=0; i < a.length; i++) { System.out.println(a[i]); }

Enhanced for-Loop (Iterator-Form):
1D:
for (int val : a) { System.out.println(val); }

2D (verschachtelt):
for (int[] row : a) {
    for (int cell : row) {
        System.out.print(cell + "\t");
    }
    System.out.println();
}
"""
)

print(response.text)


