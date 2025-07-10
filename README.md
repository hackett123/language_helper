# Mandarin CLI Flashcard & Vocabulary Tool

A terminal-based flashcard and word lookup system for learning Mandarin, designed to work with HelloChinese-style vocab exports.

## Features

- 🔄 `load`: Merge new vocabulary from a JSON file into your saved vocab.
- 🔍 `search`: Look up words by **pinyin substring** (tone-insensitive).
- 🧠 `study`: Flashcard quiz mode (randomized, shows either English or Chinese first).
- ➕ `add`: Add new words manually from the command line.

---

## Getting Started

### 1. Install

Clone this repo and run with Python 3:

```bash
python3 mandarin.py [mode] [args...]
```
### 2. Load Vocabulary

You can load a HelloChinese-style JSON file (like hellochinese.json):

```bash
python3 mandarin.py load hellochinese.json
```

This will merge the new words into vocab.json.

## Modes

### ✅ Load

```bash
python3 mandarin.py load hellochinese.json
```

Merges words from a new file into your existing vocabulary.

### ✅ Search

```bash
python3 mandarin.py search guo
```

Matches any words where the pinyin contains the substring (tone-insensitive):

```bash
苹果 (píngguǒ): apple
芒果 (mángguǒ): mango
中国 (Zhōngguó): China
```

### ✅ Study

```bash
python3 mandarin.py study
```

Flashcard quiz — shows either:

    English → you guess Chinese

    Chinese → you guess English


### ✅ Add

```bash
python3 mandarin.py add "mother" "mā" "妈"
```

Adds a new word to your vocabulary (avoids duplicates).

### Format of vocab.json

```json
[
  {
    "simplified": "妈",
    "pinyin": "mā",
    "english": "mother"
  },
  ...
]
```