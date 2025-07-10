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

You can load a JSON file to quickly get started - I've included a starting vocab.json file already, but to add more:

```bash
python3 mandarin.py load my_mandarin_vocab.json
```

This will merge the new words into vocab.json.

## Modes

### Search

```bash
python3 mandarin.py search guo
```

Matches any words where the pinyin contains the substring (tone-insensitive):

```bash
苹果 (píngguǒ): apple
芒果 (mángguǒ): mango
中国 (Zhōngguó): China
```

### Study

```bash
python3 mandarin.py study
```

Flashcard quiz — shows either:

    English → you guess Chinese

    Chinese → you guess English

You hit enter to reveal the answer, and then y/n to say if you were right. When you're done, hit q and it will end the session, and save your stats to a `user_stats.json` file. By default this is in the gitignore so you don't get someone else's stats.

### ✅ Add

```bash
python3 mandarin.py add "mother" "māma" "妈妈"
```

Adds a new word to your vocabulary (avoids duplicates).

### Format of vocab.json

```json
[
  {
    "simplified": "妈妈",
    "pinyin": "māma",
    "english": "mother"
  },
  ...
]
```