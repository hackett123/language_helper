import json
import sys
import os
import random
import unicodedata

VOCAB_FILE = 'vocab.json'
USER_STATS_FILE = 'user_stats.json'

def normalize_pinyin(pinyin):
    """Remove tones to match input like 'ma' to 'mā', 'má', etc."""
    normalized = ''.join(c for c in unicodedata.normalize('NFD', pinyin) if unicodedata.category(c) != 'Mn')
    return normalized.lower()

def add(english, pinyin, simplified):
    new_entry = {
        "simplified": simplified,
        "pinyin": pinyin,
        "english": english
    }

    vocab = []
    if os.path.exists(VOCAB_FILE):
        with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
            vocab = json.load(f)

    if any(word['simplified'] == simplified for word in vocab):
        print(f"'{simplified}' already exists in your vocabulary.")
        return

    vocab.append(new_entry)

    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    print(f"Added: {simplified} ({pinyin}) → {english}")


def load(new_vocab_file):
    if os.path.exists(VOCAB_FILE):
        with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
            known_vocab = json.load(f)
    else:
        known_vocab = []

    with open(new_vocab_file, 'r', encoding='utf-8') as f:
        new_vocab = json.load(f)

    # Avoid duplicates (by simplified character)
    simplified_set = {word['simplified'] for word in known_vocab}
    merged_vocab = known_vocab + [w for w in new_vocab if w['simplified'] not in simplified_set]

    with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
        json.dump(merged_vocab, f, ensure_ascii=False, indent=2)
    print(f"Loaded {len(new_vocab)} new words. Total: {len(merged_vocab)}")

def search(query):
    if not os.path.exists(VOCAB_FILE):
        print("No vocab file found. Please run `load` first.")
        return

    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    results = [w for w in vocab if query.lower() in normalize_pinyin(w['pinyin'])]
    for word in results:
        print(f"{word['simplified']} ({word['pinyin']}): {word['english']}")

def load_stats():
    if os.path.exists(USER_STATS_FILE):
        with open(USER_STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def save_stats(stats):
    with open(USER_STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def study():
    if not os.path.exists(VOCAB_FILE):
        print("No vocab file found. Please run `load` first.")
        return

    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        vocab = json.load(f)

    stats = load_stats()
    random.shuffle(vocab)

    print("Starting study session. Press 'q' at any prompt to quit.\n")

    for word in vocab:
        show_chinese = random.choice([True, False])
        key = f"{word['simplified']}|{word['english']}"
        if key not in stats:
            stats[key] = {
                "guess_chinese": {"right": 0, "wrong": 0},
                "guess_english": {"right": 0, "wrong": 0}
            }

        if show_chinese:
            ans = input(f"What does '{word['simplified']}' ({word['pinyin']}) mean? Press Enter to reveal or 'q' to quit: ").strip().lower()
            if ans == 'q':
                break
            print(f"→ {word['english']}\n")
            while True:
                correct = input("Were you correct? (y/n, q to quit): ").strip().lower()
                if correct == 'q':
                    break
                if correct in ('y', 'n'):
                    if correct == 'y':
                        stats[key]["guess_english"]["right"] += 1
                    else:
                        stats[key]["guess_english"]["wrong"] += 1
                    break
            if correct == 'q':
                break
        else:
            ans = input(f"What is the Chinese for '{word['english']}'? Press Enter to reveal or 'q' to quit: ").strip().lower()
            if ans == 'q':
                break
            print(f"→ {word['simplified']} ({word['pinyin']})\n")
            while True:
                correct = input("Were you correct? (y/n, q to quit): ").strip().lower()
                if correct == 'q':
                    break
                if correct in ('y', 'n'):
                    if correct == 'y':
                        stats[key]["guess_chinese"]["right"] += 1
                    else:
                        stats[key]["guess_chinese"]["wrong"] += 1
                    break
            if correct == 'q':
                break

    save_stats(stats)
    print("Session ended. Stats saved to user_stats.json.")


# Command-line interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 mandarin.py [load/search/study] [args]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == 'load' and len(sys.argv) == 3:
        load(sys.argv[2])
    elif mode == 'search' and len(sys.argv) == 3:
        search(sys.argv[2])
    elif mode == 'study':
        study()
    elif mode == 'add' and len(sys.argv) == 5:
        _, _, english, pinyin, simplified = sys.argv
        add(english, pinyin, simplified)
    else:
        print("Invalid usage.")
