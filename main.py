import time
import random
import requests
import json
from tabulate import tabulate


def main():
    total_score = 0
    duration = 60
    lang = language()
    words = get_words(lang)

    while time.time() - start_time <= duration:
        word = generate_word(words)
        print(word)
        user_input = input("Enter the word: ")

        if user_input == word:
            total_score += 1

    print(f"Time's up! your typing speed is {total_score} wpm")
    save_score(name, total_score)
    create_and_display_table_of_scores()


def language():
    lang = input("Enter the language (English/Spanish/Arabic): ")
    return lang


def get_words(lang):
    global words
    if lang.lower() == "english":
        url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/common.json"

        try:
            response = requests.get(url)
            response.raise_for_status()

            common_words = json.loads(response.text)
            words = common_words["commonWords"]

        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)

    elif lang.lower() == "spanish":
        url = "https://www.wordfrequency.info/span/samples/span_40k_lemmas.txt"

        try:
            response = requests.get(url)
            response.raise_for_status()
            spanish_words = response.text.split()
            spanish_words = [word for word in spanish_words if word.isalpha() and len(word) > 1]
            words = spanish_words[39:]
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)

    elif lang.lower() == "arabic":

        url = "https://raw.githubusercontent.com/mohataher/arabic-stop-words/master/list.txt"

        response = requests.get(url)
        if response.status_code == 200:
            arabic_words = response.text.split('\n')
            arabic_words = [word.strip() for word in arabic_words if word.strip()]
            words = arabic_words

        else:
            print("Failed to retrieve data from the URL. Status code:", response.status_code)

    return words


def generate_word(words):
    a = random.choice(words)
    return a


def save_score(name, score):
    try:
        with open(score_file, "a") as file:
            # Format the data as "Name: Score" and save it to the file
            file.write(f"{name}: {score}\n")
    except Exception as e:
        print("Error saving score:", e)


def create_and_display_table_of_scores():
    try:
        with open(score_file, "r") as file:
            scores = file.readlines()

        # Parse the name-score pairs from the lines
        name_score_pairs = [line.strip().split(": ") for line in scores]

        # Create a table with names and scores
        table = []
        for i, (name, score) in enumerate(name_score_pairs, start=1):
            table.append([i, name, score])

        # Display the table using tabulate
        headers = ["Name", "Score"]
        print(tabulate(table, headers=headers, tablefmt="rounded_outline"))
    except FileNotFoundError:
        print("No scores found.")
    except Exception as e:
        print("Error reading scores:", e)


if __name__ == "__main__":
    print("Typing speed test")
    name = input("Enter your name: ")
    score_file = "scores.txt"
    start_time = time.time()  # Record the start time
    main()

