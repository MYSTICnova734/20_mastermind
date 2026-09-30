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
        # No state changes are allowed once the game has ended.
        if self.is_over():
            return None
        guess = list(raw)
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

    def choose_difficulty(self):
        names = "/".join(DIFFICULTIES)
        while True:
            raw = input(f"Choose difficulty ({names}) > ").strip().lower()
            if raw == "q":
                return None
            if raw in DIFFICULTIES:
                return raw
            print(f"Enter one of: {names}.")

    def run(self):
        choice = self.choose_difficulty()
        if choice is None:
            self.quit()
            return
        # Rebuild the game with the chosen difficulty.
        self.__init__(choice)
        print(f"Mastermind — enter {self.length} digits from "
              f"{self.symbols[0]} to {self.symbols[-1]}.")
        while not self.is_over():
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self.quit()
                return
            if not self.is_valid(raw):
                print(f"Enter exactly {self.length} digits from "
                      f"{self.symbols[0]} to {self.symbols[-1]}.")
                continue
            exact, partial = self.submit(raw)
            print("Exact:", exact, " Partial:", partial)
        if self.status == "won":
            print("Cracked the code!")
        else:
            print("Out of turns. The code was", "".join(self.code))