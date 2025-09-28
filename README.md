# Brainrot Lang

**Brainrot Lang** is a programming language aimed at using only/mostly brainrot terms!

```brainrot
LOCK IN
FANUMTAX gyatt FR "wsg"
FANUMTAX goon FR "WORLD!"
FANUMTAX sigma FR gyatt 💀 goon
SAY sigma
ITS OVER
```

---

## Program Structure
Programs must start with `LOCK IN` and end with `ITS OVER`.

```brainrot
LOCK IN
🖕 ...code
ITS OVER
```

---

## Comments
Rather than the typical `#`, comments are written with `🖕`.

```brainrot
🖕 this is a comment! this code sucks
```

---

## Math
Mathematical symbols are replaced with emojis/terms:  

- `💀 = +`  
- `😭 = -`  
- `😏 = ×`  
- `🚡 = ÷`  
- `FR = =`  

Notes:
- `💀` also concatenates strings: `"hi" 💀 " there"` → `hi there`
- String repeat with `😏`: `"ha" 😏 3` → `hahaha`
- Division returns a number; avoid dividing by zero (runtime error)

---

## Braincells
Data can be stored in any of the **7 braincells**:

- `aura`  
- `peak`  
- `goon`  
- `mog`  
- `npc`  
- `sigma`  
- `gyatt`  

Example:  

```brainrot
FANUMTAX peak FR 2
```

---

## I/O
`SAY` will print values.  

```brainrot
LOCK IN
FANUMTAX goon FR 69
SAY goon
ITS OVER
```
Output:
```
69
```

---

## Data and Copy
- `FANUMTAX` declares/assigns a value to a braincell.  
- `DIDDLE` copies the value from one braincell to another.

```brainrot
LOCK IN
FANUMTAX aura FR "hello"
DIDDLE peak FR aura
SAY peak
ITS OVER
```
Output:
```
hello
```

---

## Control Flow

### If / Else
Use `ONGOD` for the if, optional `NO CAP` for else, and close with `DEADASS`.

```brainrot
LOCK IN
FANUMTAX sigma FR 0
ONGOD sigma
  SAY "nonzero"
NO CAP
  SAY "zero"
DEADASS
ITS OVER
```
Output:
```
zero
```

### While Loop
Use `SKIBIDI` to start a loop and `RIZZUP` to end it.

```brainrot
LOCK IN
FANUMTAX gyatt FR 3
SKIBIDI gyatt
  SAY gyatt
  FANUMTAX gyatt FR gyatt 😭 1
RIZZUP
ITS OVER
```
Output:
```
3
2
1
```

### Truthiness
- Numbers: `0` is false; any other number is true.  
- Strings: empty is false; non-empty is true.

---

## Expressions
- Literals: integers (e.g., `123`), strings in double quotes (supports escapes like `\"` and `\n`).  
- Operands can be braincells or literals.  
- Operator precedence: `😏` and `🚡` before `💀` and `😭`.  
- Parentheses are **not** supported (keep expressions simple or split across assigns).

Examples:
```brainrot
FANUMTAX mog FR 10 😏 2 💀 5      🖕 (10*2)+5 = 25
FANUMTAX npc FR "hi" 💀 "!"       🖕 "hi!"
FANUMTAX sigma FR "ha" 😏 4       🖕 "hahaha"
```

---

## Errors (runtime vibes)
- Unknown braincell name → error  
- Copy from an unset braincell → error  
- Division by zero → error  
- Bad syntax (missing `FR`, mismatched blocks, etc.) → error

---

## Mini Cheatsheet
- **Assign:** `FANUMTAX <cell> FR <expr>`  
- **Copy:** `DIDDLE <dest> FR <source>`  
- **Print:** `SAY <expr>`  
- **If:** `ONGOD <expr> … NO CAP … DEADASS` (else optional)  
- **While:** `SKIBIDI <expr> … RIZZUP`  
- **Ops:** `💀 +`, `😭 -`, `😏 *`, `🚡 /`
