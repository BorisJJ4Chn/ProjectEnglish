from typing import Optional, Callable, Dict
from ui import EnglishUI
from logic import WordManager
from word import Word, Definition, Example

class EnglishCLI:
    def __init__(self) -> None:
        self.word_manager: WordManager = WordManager()
        self.ui: EnglishUI = EnglishUI(self.word_manager)
        self.commands: Dict[str, Callable[[], None]] = {
            '1': self.ui.option_add_word,
            '2': self.ui.option_search_words,
            '3': self.ui.option_list_words,
            '4': self.ui.option_save_words,
            '5': self.ui.option_exit_program
        }

    def run(self) -> None:
        self.ui.greet_user()
        while True:
            choice: str = self.ui.display_menu()
            self.ui.run_option(choice)

if __name__ == "__main__":
    cli = EnglishCLI()
    cli.run()