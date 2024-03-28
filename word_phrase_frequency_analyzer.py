import itertools
from collections import defaultdict

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


class WordAnalyzer:
    def __init__(self):
        self.four_word_sets = defaultdict(int)
        self.three_word_sets = defaultdict(int)
        self.two_word_sets = defaultdict(int)
        self.single_word_counts = defaultdict(int)
        self.excluded_words = set()
        self.lemmatizer = WordNetLemmatizer()
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")

    def load_exclusions(self, filename):
        with open(filename, "r") as file:
            for line in file:
                self.excluded_words.add(line.strip())

    def process_text(self, text):
        word_units = self.generate_word_units(text)
        cleaned_words = self.clean_words(word_units)
        cleaned_words = [word.lower() for word in cleaned_words]
        lemmatized_words = [
            self.lemmatize_word(word) for word in cleaned_words
        ]

        # Analyze four-word sets
        for i in range(len(lemmatized_words) - 3):
            four_word_set = lemmatized_words[i : i + 4]
            if not any(word in self.excluded_words for word in four_word_set):
                three_word_combinations = itertools.combinations(
                    four_word_set, 3
                )
                two_word_combinations = itertools.combinations(
                    four_word_set, 2
                )
                for word in four_word_set:
                    self.single_word_counts[word] += 1
                for combo in three_word_combinations:
                    self.three_word_sets[combo] += 1
                for combo in two_word_combinations:
                    self.two_word_sets[combo] += 1
                self.four_word_sets[tuple(four_word_set)] += 1

    def generate_word_units(self, text):
        word_units = []
        word = ""
        apostrophes = ["'", "’"]
        dashes = ["-", "—", "–"]
        for i, char in enumerate(text):
            if char.isalnum():
                word += char
            elif char in dashes or char in apostrophes:
                if word and word[-1].isalnum():
                    if char in apostrophes:
                        word += char
                    elif i < len(text) - 1 and text[i + 1] in dashes:
                        word_units.append(word)
                        word = ""
                    else:
                        word += char
            elif word:
                word_units.append(word.strip())
                word = ""
        if word:
            word_units.append(word.strip())
        return word_units

    def clean_words(self, word_units):
        cleaned_words = []
        for unit in word_units:
            if unit[-1] in [",", ".", "!", "?"]:
                unit = unit[:-1]
            cleaned_words.append(unit)
        return cleaned_words

    def lemmatize_word(self, word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }
        return self.lemmatizer.lemmatize(word, tag_dict.get(tag, wordnet.NOUN))

    def should_exclude(self, word):
        return word.lower() in self.excluded_words

    def print_output(self):
        # Print headers for each section
        print("Four-word sets:")
        print("Set\tFrequency")
        # Print each set with corresponding frequency, sorted by frequency
        for four_word_set, frequency in sorted(
            self.four_word_sets.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{' '.join(four_word_set)}\t{frequency}")

        print("\nThree-word sets:")
        print("Set\tFrequency")
        for three_word_set, frequency in sorted(
            self.three_word_sets.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{' '.join(three_word_set)}\t{frequency}")

        print("\nTwo-word sets:")
        print("Set\tFrequency")
        for two_word_set, frequency in sorted(
            self.two_word_sets.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{' '.join(two_word_set)}\t{frequency}")

        print("\nSingle words:")
        print("Word\tFrequency")
        for word, frequency in sorted(
            self.single_word_counts.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"{word}\t{frequency}")

    def save_output(self, filename):
        with open(filename, "w") as file:
            # Write headers for each section
            file.write("Four-word sets:\n")
            file.write("Set\tFrequency\n")
            # Write each set with corresponding frequency, sorted by frequency
            for four_word_set, frequency in sorted(
                self.four_word_sets.items(), key=lambda x: x[1], reverse=True
            ):
                file.write(f"{' '.join(four_word_set)}\t{frequency}\n")

            file.write("\nThree-word sets:\n")
            file.write("Set\tFrequency\n")
            for three_word_set, frequency in sorted(
                self.three_word_sets.items(), key=lambda x: x[1], reverse=True
            ):
                file.write(f"{' '.join(three_word_set)}\t{frequency}\n")

            file.write("\nTwo-word sets:\n")
            file.write("Set\tFrequency\n")
            for two_word_set, frequency in sorted(
                self.two_word_sets.items(), key=lambda x: x[1], reverse=True
            ):
                file.write(f"{' '.join(two_word_set)}\t{frequency}\n")

            file.write("\nSingle words:\n")
            file.write("Word\tFrequency\n")
            for word, frequency in sorted(
                self.single_word_counts.items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                file.write(f"{word}\t{frequency}\n")


def main():
    # Read input text from a file
    os.chdir("/app/input")
    for in_file in os.listdir("."):
        if in_file == "exclusions.txt":
            continue
        with open(in_file, "r") as file:
            text = file.read()
        print(f"Processing {in_file}.")
        # Initialize the analyzer
        analyzer = WordAnalyzer()

        # Load excluded words from file
        analyzer.load_exclusions("/app/input/exclusions.txt")

        # Process the text
        analyzer.process_text(text)

        # Print the output
        # analyzer.print_output()
        orig_file = os.path.splitext(in_file)[0]
        # Save the output to a file
        analyzer.save_output(
            f"/app/output/word_frequency_analysis_{orig_file}.txt"
        )
        print(
            f"Finished processing {in_file} and saved to word_frequency_analysis_{orig_file}.txt in output location."
        )


if __name__ == "__main__":
    main()
