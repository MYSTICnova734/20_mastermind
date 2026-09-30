import random
from logic import feedback

# name: (code length, highest symbol, allowed guesses)
DIFFICULTIES = {
    "easy": (3, 4, 12),
    "normal": (4, 6, 10),
    "hard": (5, 8, 8),
}


class Mastermind:
    def __init__(self, difficulty="normal"):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        self.difficulty = difficulty
        self.length, top, self.max_turns = DIFFICULTIES[difficulty]
        self.symbols = [str(n) for n in range(1, top + 1)]
        self.code = [random.choice(self.symbols) for _ in range(self.length)]
        self.history = []
        self.turns = self.max_turns
        self.status = "playing"  # "playing", "won", "lost" or "quit"

    def is_over(self):
        return self.status != "playing"

    def is_valid(self, raw):
        return len(raw) == self.length and all(ch in self.symbols for ch in raw)

    def submit(self, raw):
        # No state changes once the game has ended, and malformed guesses
        # are rejected before they can use up a turn.
        if self.is_over() or not self.is_valid(raw):
            return None
        guess = list(raw)
        # Feedback is computed exactly once, for this accepted guess only.
        exact, partial = feedback(self.code, guess)
        self.history.append((raw, exact, partial))
        self.turns -= 1
        # A win on the final turn still counts as a win, so check it first.
        if exact == len(self.code):
            self.status = "won"
        elif self.turns == 0:
            self.status = "lost"
        return exact, partial

    def quit(self):
        if not self.is_over():
            self.status = "quit"

    def format_history(self):
        lines = ["  #  Guess  Exact  Partial"]
        for i, (raw, exact, partial) in enumerate(self.history, 1):
            lines.append(f"{i:>3}  {raw:<5}  {exact:>5}  {partial:>7}")
        return "\n".join(lines)

    @staticmethod
    def read(prompt):
        # Returns None if input is closed (Ctrl-D) or interrupted (Ctrl-C).
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

    def choose_difficulty(self):
        names = "/".join(DIFFICULTIES)
        while True:
            raw = self.read(f"Choose difficulty ({names}) > ")
            if raw is None or raw.lower() == "q":
                return None
            raw = raw.lower()
            if raw in DIFFICULTIES:
                return raw
            print(f"Enter one of: {names}.")

    def run(self):
        choice = self.choose_difficulty()
        if choice is None:
            self.quit()
            print("Quit. Thanks for playing.")
            return
        # Rebuild the game with the chosen difficulty.
        self.__init__(choice)
        print(f"Mastermind — enter {self.length} digits from "
              f"{self.symbols[0]} to {self.symbols[-1]}.")
        while not self.is_over():
            raw = self.read(f"{self.turns} turns left > ")
            if raw is None or raw.lower() == "q":
                self.quit()
                print("Quit. Thanks for playing.")
                return
            result = self.submit(raw)
            if result is None:
                print(f"Invalid guess (no turn used). Enter exactly "
                      f"{self.length} digits from "
                      f"{self.symbols[0]} to {self.symbols[-1]}.")
                continue
            print(self.format_history())
        if self.status == "won":
            print("Cracked the code!")
        else:
            print("Out of turns. The code was", "".join(self.code))