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