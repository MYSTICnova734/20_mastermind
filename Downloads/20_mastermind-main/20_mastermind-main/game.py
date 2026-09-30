import random
from logic import feedback


class Mastermind:
    def __init__(self):
        self.code = [str(random.randint(1, 6)) for _ in range(4)]
        self.history = []
        self.max_turns = 10
        self.turns = self.max_turns
        self.status = "playing"  # "playing", "won", "lost" or "quit"

    def is_over(self):
        return self.status != "playing"

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

    def run(self):
        print("Mastermind — enter four digits from 1 to 6.")
        while not self.is_over():
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self.quit()
                return
            if len(raw) != 4 or any(ch not in "123456" for ch in raw):
                print("Enter exactly four digits from 1 to 6.")
                continue
            exact, partial = self.submit(raw)
            print("Exact:", exact, " Partial:", partial)
        if self.status == "won":
            print("Cracked the code!")
        else:
            print("Out of turns. The code was", "".join(self.code))