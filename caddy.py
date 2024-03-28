import cmd
import random
import re
import pathlib

WORDS_FILE = "target_words.txt"
no_repeat_chars_regex = (
    r"^(?:([a-z])(?!.*\1))*$"  # Ensure unique characters in suggestions
)
OPENER = "crane"
INTRO = "Welcome to Wordle Caddy: a Wordle word filterer.\nType help for a list of commands."


class WordleCaddy(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.words = (
            (pathlib.Path(__file__).parent / WORDS_FILE).read_text().splitlines()
        )
        self.last_search = self.words
        self.intro = INTRO
        self.prompt = "(wordle ) "
        self.not_contains = set()
        self.contains = set()
        self.matches = set()
        self.recommended = OPENER

    def do_ipick(self, arg):
        """Intelligently picks a word based on textual representation of clues."""
        try:
            guess, score = re.split(r"\s|:", arg)
        except ValueError:
            score = arg
            guess = self.recommended

        if len(guess) != len(score):
            print("Error: guess and score must be the same length")
            return

        not_in_word = []
        exact_positions = ["."] * len(guess)
        in_word = []
        not_in_positions = ["."] * len(guess)

        for i, (g, s) in enumerate(zip(guess, score)):
            if s in "-_.g":
                not_in_word.append(g)
            elif s in "o?y":
                in_word.append(g)
                not_in_positions[i] = g
                self.contains.add(g)
            elif s in "x+g":
                exact_positions[i] = g
                self.matches.add(g)

        self.process_filters(not_in_word, exact_positions, not_in_positions, in_word)

    def process_filters(self, not_in_word, exact_positions, not_in_positions, in_word):
        """Applies filters based on the clues provided."""
        if not_in_word_filtered := [
            char
            for char in not_in_word
            if char not in self.contains.union(self.matches)
        ]:
            self.do_not("".join(not_in_word_filtered))
        self.do_sub("".join(exact_positions))
        self.do_sub("".join([f"[^{c}]" if c != "." else "." for c in not_in_positions]))
        if in_word:
            self.do_contains("".join(in_word))
        self.do_suggest("")

    def do_find(self, arg, sub_search=False, show=True, save=True):
        """Finds arg in the word list using regex syntax."""
        regex = re.compile(arg)
        words = self.last_search if sub_search else self.words
        last_search = [word for word in words if regex.match(word)]
        if show:
            print(last_search, len(last_search))
        if save:
            self.last_search = last_search
        else:
            return last_search  # TODO: so cludgy!

    def do_sub(self, arg):
        """Executes a find within the last results."""
        self.do_find(arg, True)

    def do_contains(self, arg):
        """Finds words containing specified characters."""
        if not arg:
            self.contains = set()
            return
        self.contains.update(arg)
        query = "".join(f"(?=.*{c})" for c in self.contains)
        self.do_sub(query)

    def do_suggest(self, arg, auto_suggest=True):
        """Suggests a word based on current filters."""
        if not self.last_search:
            print("No suggestions available.")
            return
        self.display_suggestions(auto_suggest)

    def display_suggestions(self, auto_suggest):
        """Displays word suggestions."""
        suggestion = self.recommended if auto_suggest else None
        if auto_suggest:
            last_search = self.do_find(
                no_repeat_chars_regex, sub_search=True, show=False, save=False
            )
            if last_search and len(last_search) > 10:
                suggestion = random.choice(last_search)
            else:
                suggestion = (
                    random.choice(self.last_search)
                    if self.last_search
                    else self.recommended
                )

        if suggestion and self.recommended != suggestion:
            self.recommended = suggestion
            print("Suggested:", suggestion)
        else:
            print("No new suggestion.")

    def do_not(self, arg):
        """Finds words not containing specified characters."""
        if not arg:
            self.not_contains = set()
            return
        self.not_contains.update(arg)
        self.do_sub(r"[^" + "".join(self.not_contains) + "]{5}")

    def do_reset(self, arg):
        """Resets the search to the full word list."""
        self.last_search = self.words
        self.not_contains.clear()
        self.contains.clear()
        self.matches.clear()
        self.recommended = OPENER
        print("Search reset.")

    def do_quit(self, arg):
        """Quits the program."""
        print("Bye!")
        return True


def main():
    w = WordleCaddy()
    w.cmdloop()


if __name__ == "__main__":
    main()
