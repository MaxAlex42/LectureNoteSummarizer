# 06 Arrays

## 1. Grundlagen von Arrays
Definition:
Ein Array ist eine Datenstruktur, die eine feste Anzahl von Werten desselben Datentyps in einer geordneten Folge speichert.

Zweck:
Wird benötigt, wenn man nicht nur einen einzelnen Wert, sondern eine ganze Sequenz von Werten verarbeiten muss (z.B. eine Liste von Messwerten, eine Sammlung von Namen).

Dimensionen:
- Eindimensional: Eine einfache Liste von Werten.
- Mehrdimensional: Eine Tabelle (2D) oder ein Würfel (3D), bei denen die Elemente selbst wieder Arrays sind.

### 1. Eindimensionale Arrays (1D)
Deklaration:
```java
int[] a;
```

Erzeugung (Instanziierung):
```java
a = new int[10]; // Erzeugt ein Array für 10 Integer.
```

Zugriff auf Elemente (Indizierung):
- Zugriff über Index in eckigen Klammern:
    ```java
    a[0] = 11;
    ```
- Index beginnt bei 0, gültige Indizes: 0 bis N-1 bei Länge N

Eigenschaft length:
```java
for (int i = 0; i < a.length; i++) {
     ... 
}
```

Initialisierung bei Deklaration:
```java
int[] fivePrimes = {2, 3, 5, 7, 11};
```

Wichtige Regeln & Fehlerquellen:
- Typkonsistenz: z.B. kein double in int[]: 
    ```java
    a[2] = 33.33; // Fehler
    ```
- Array-Grenzen: a[10] bei Länge 10 → IndexOutOfBoundsException

### 4. Zweidimensionale Arrays (2D)
Konzept:
Ein 2D-Array ist ein Array von Arrays (z.B. eine Tabelle).

Deklaration & Erzeugung:
```java
int[][] a = new int[3][4];
```

Zugriff:
```java
a[1][1] = 6; // zweite Zeile, zweite Spalte
```

length-Eigenschaften:
- a.length: Anzahl der Zeilen
- a[0].length: Anzahl der Spalten (erste Zeile)

Initialisierung:
```java
int[][] a = { {1,2,3}, {4,5,6}, {7,8,9} };
```

Fortgeschritten:
- Jagged Arrays (unregelmäßige Zeilenlängen möglich, aber unüblich)
- Mehrdimensionale Arrays (z.B. float[][][])

## 3. Arrays, Referenzen und Speicherverwaltung
Arrays als Referenztypen:
Array-Variable speichert die Adresse des Speicherbereichs, nicht die Daten selbst.

Zuweisung:
```java
int[] b = a; // b zeigt auf dasselbe Array wie a
```

Folge:
Änderungen über b wirken sich auch auf a aus.

Garbage Collection:
```java
a = null;
a = new int[20]; // alte Referenz wird verworfen
```

## 5. Iteration über Arrays
Klassische for-Schleife:
```java
for (int i=0; i < a.length; i++) {
     System.out.println(a[i]); 
}
```

Enhanced for-Loop (Iterator-Form):
1D:
```java
for (int val : a) {
     System.out.println(val);
}
```


2D (verschachtelt):
```java
for (int[] row : a) {
    for (int cell : row) {
        System.out.print(cell + "\t");
    }
    System.out.println();
}
```

# 07 Klassen und Objekte  

## 1. Motivation & Grundbegriffe  
**Klassen** sind benutzerdefinierte Datentypen, die Daten (Attribute) und darauf operierende **Methoden** kapseln. Objekte sind Instanzen dieser Klassen und werden mit `new` erzeugt; sie kommunizieren, indem sie einander Nachrichten (Methodenaufrufe) schicken.  

### 1.1 Verdeckte Daten & sichtbare Operationen  
- **Instanzvariablen** beschreiben den Zustand einzelner Objekte und sind in der Regel `private`.  
- **Methoden** sind öffentlich (`public`), um den internen Zustand zu manipulieren oder auszulesen.  
- **Zugriffsattribute**: `private`, *package-private* (kein Schlüsselwort), `protected`, `public` – Geheimnisprinzip.  

## 2. Beispielklasse `Fraction`  
```java
class Fraction {
    private int num = 0; // Zähler
    private int den = 1; // Nenner

    public Fraction(int n, int d){ … }
    public int getNum(){ return num; }
    public int getDen(){ return den; }
    public Fraction add(Fraction f){ … }
    // mult(), sub(), div(), toString(), toDouble()
}
```  
- Objekte sind immer **in kanonischer Form** (gekürzt, Nenner positiv, `den ≠ 0`).  
- Invariante wird durch Konstruktoren und
  ```java
  public static int gcd(int a, int b){ … }
  ```
  sichergestellt.  

## 3. Konstruktoren & Überladen  
Mehrere Konstruktoren ermöglichen verschiedene Initialisierungen (`Fraction(int,int)`, `Fraction(int)`, `Fraction()`). Methoden dürfen überladen werden, solange sich die Signaturen unterscheiden.  

## 4. Instanz- vs. Klassenkomponenten  
- **Instanzmethoden** besitzen ein implizites `this`.  
- **Klassenmethoden/-variablen** (`static`) besitzen kein `this` und existieren einmal pro Klasse (z. B. ein Zähler `nFractions`).  

## 5. Parameterübergabe in Java  
- **Grundtypen** → Call-by-Value (Wert wird kopiert).  
- **Objektreferenzen** → Call-by-Value der *Referenz* → Änderungen betreffen das Objekt.

# 10 Generizität  

## 1. Problemstellung  
Ein nicht-generischer `Stack` speichert Elemente als `Object`; beim Entnehmen ist eine **Abwärtskonversion** nötig – fehleranfällig und nur zur Laufzeit überprüfbar.  

## 2. Generische Typen (parametrisierte Klassen)  
```java
interface IStack<E>{
    void push(E e);
    E pop();
    E top();
    boolean empty();
}

class DynStack<E> implements IStack<E>{
    private class ListElement{
        E value; ListElement next;
        ListElement(E v, ListElement n){ value = v; next = n; }
    }
    …
}
```  
- Der Typparameter `E` wird bei Gebrauch durch einen konkreten Typ ersetzt (`IStack<Fraction>`).  
- Der Compiler stellt Typkonsistenz sicher → **typsichere, homogene** Container.  

### 2.1 Vorteile  
- Keine expliziten Casts, dadurch lesbarer Code.  
- Laufzeitfehler (ClassCastException) werden zu Compile-Time-Fehlern.  
- Mehrere Typ­parameter möglich (`Map<K,V>`).  

---

# 14 Ein- und Ausgabe  

## 1. Stream-Abstraktion  
Ein **Stream** repräsentiert Quelle oder Senke von Daten; Programme bleiben unabhängig von Geräte-Details. Es gibt **InputStreams** (lesen) und **OutputStreams** (schreiben).  

## 2. Byte- vs. Character-Streams  

| Kategorie        | Basisklassen                    | Zweck                              | Typische Klassen             |
|------------------|---------------------------------|------------------------------------|------------------------------|
| Byte-Streams     | `InputStream` / `OutputStream`  | rohe 8-Bit-Daten                   | `FileInputStream`, `FileOutputStream` |
| Character-Streams| `Reader` / `Writer`            | Text, automatische Zeichensatz-Konversion | `FileReader`, `FileWriter`   |

### 2.1 Beispiel: Datei-Kopie (Byte-weise)  
```java
try(FileInputStream  in  = new FileInputStream("src.txt");
    FileOutputStream out = new FileOutputStream("dest.txt")){
    int c;
    while((c = in.read()) != -1) out.write(c);
}
```  

### 2.2 Beispiel: Datei-Kopie (Zeichen-weise)  
```java
try(BufferedReader in  = new BufferedReader(new FileReader("src.txt"));
    PrintWriter     out = new PrintWriter(new FileWriter("dest.txt"))){
    String line;
    while((line = in.readLine()) != null) out.println(line);
}
```  

## 3. Pufferung  
`BufferedInputStream`, `BufferedReader`, … reduzieren teure Gerätezugriffe; `flush()` leert Ausgabepuffer sofort.  

## 4. Hilfsklassen für Text-I/O  
- **`PrintWriter` / `PrintStream`**: `print()`, `println()`, `format()`; unterstützen plattformabhängige Zeilenenden (`%n`).  
- **`Scanner`**: zerlegt Eingabe in Token, bietet `nextInt()`, `hasNextDouble()` usw.  

## 5. Data-Streams (binäre Grundtyp-I/O)  
`DataOutputStream` & `DataInputStream` schreiben/lesen primitive Typen (`writeInt`, `readDouble`) im plattformunabhängigen Format; `EOFException` signalisiert Dateiende.  

## 6. Objekt-Streams  

### 6.1 Serialisierung  
`ObjectOutputStream.writeObject(obj)` speichert  
- Klassen-Info,  
- Signatur,  
- alle nicht-transienten Instanzvariablen.  

Erforderlich: Klasse implementiert **`Serializable`** (Marker-Interface).  

### 6.2 Deserialisierung  
```java
Shape s = (Shape) in.readObject();
```  
Erhält Objektidentität und behandelt zyklische Referenzen.  