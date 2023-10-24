import time
import random
import requests
import json
from tabulate import tabulate

# Constants
SCORE_FILE = "scores.txt"

def main():
    total_score = 0
    duration = 60
    start_time = time.time()  # Record the start time
    lang = get_language()
    words = get_words(lang)

    while time.time() - start_time <= duration:
        word = generate_word(words)
        print(word)
        user_input = input("Enter the word: ")

        if user_input == word:
            total_score += 1

    print(f"Time's up! Your typing speed is {total_score} wpm")
    save_score(name, total_score)
    create_and_display_table_of_scores()

def get_language():
    lang = input("Enter the language (English/Spanish/Arabic): ")
    return lang

def get_words(lang):
    words = []
    if lang.lower() == "english":
        url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/common.json"
    elif lang.lower() == "spanish":
        url = "https://www.wordfrequency.info/span/samples/span_40k_lemmas.txt"
    elif lang.lower() == "arabic":
        url = "https://raw.githubusercontent.com/mohataher/arabic-stop-words/master/list.txt"
    else:
        print("Language not supported.")
        exit(1)

    try:
        response = requests.get(url)
        response.raise_for_status()

        if lang.lower() == "english":
            common_words = json.loads(response.text)
            words = common_words["commonWords"]
        elif lang.lower() == "spanish":
            spanish_words = response.text.split()
            spanish_words = [word for word in spanish_words if word.isalpha() and len(word) > 1]
            words = spanish_words[39:]
        elif lang.lower() == "arabic":
            arabic_words = response.text.split('\n')
            arabic_words = [word.strip() for word in arabic_words if word.strip()]
            words = arabic_words

    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)

    return words

def generate_word(words):
    return random.choice(words)

def save_score(name, score):
    try:
        with open(SCORE_FILE, "a") as file:
            file.write(f"{name}: {score}\n")
    except Exception as e:
        print("Error saving score:", e)

def create_and_display_table_of_scores():
    try:
        with open(SCORE_FILE, "r") as file:
            scores = file.readlines()

        if not scores:
            print("No scores found.")
        else:
            name_score_pairs = [line.strip().split(": ") for line in scores]
            table = []
            for i, (name, score) in enumerate(name_score_pairs, start=1):
                table.append([i, name, score])

            headers = ["Rank", "Name", "Score"]
            print(tabulate(table, headers=headers, tablefmt="pretty"))
    except FileNotFoundError:
        print("No scores found.")
    except Exception as e:
        print("Error reading scores:", e)

if __name__ == "__main__":
    print("Typing speed test")
    name = input("Enter your name: ")
    main()
