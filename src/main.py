from typing import Optional, Callable
from ui import EnglishUI
from logic import WordManager
from word import Word, Definition, Example

class EnglishCLI:
    def __init__(self):
        self.word_manager = WordManager()
        self.ui = EnglishUI(self.word_manager)
        self.commands = {
            '1': self.ui.option_add_word,
            '2': self.ui.option_search_words,
            '3': self.ui.option_list_words,
            '4': self.ui.option_exit_program
        }

    def run(self) -> None:
        self.ui.greet_user()
        while True:
            choice: str = self.ui.display_menu()
            command: Optional[Callable[[], None]] = self.commands.get(choice)
            if command:
                command()
            else:
                print("无效的选择，请重试!")

if __name__ == "__main__":
    cli = EnglishCLI()
    cli.run()