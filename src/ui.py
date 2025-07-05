import os
import sys
from typing import List, Optional
from logic import WordManager
from word import Word, Definition
from settings import PAGE_SIZE, INITIAL_PAGE

class EnglishUI:
    # UI菜单选项常量
    MENU_OPTIONS_MAIN = [
        "添加新单词",
        "查询单词",
        "列出所有单词",
        "保存单词",
        "退出程序"
    ]
    MENU_OPTIONS_EDIT = [
        "添加释义",
        "修改释义",
        "删除释义",
        "删除单词",
        "退出编辑"
    ]
    MENU_OPTION_EDIT_DEFINITION = [
        "修改词性及释义",
        "增加例句",
        "删除例句",
        "退出编辑"
    ]

    def __init__(self, word_manager: WordManager) -> None:
        self.word_manager = word_manager
        self.commands: Dict[str, Callable[[], None]] = {
            '1': self.option_add_word,
            '2': self.option_search_words,
            '3': self.option_list_words,
            '4': self.option_save_words,
            '5': self.option_exit_program
        }

    def _get_enter(self) -> None:
        input("回车以继续...")
        os.system('cls')

    def greet_user(self) -> None:
        print("===== 欢迎使用英语单词管理系统 =====")

    def display_menu(self) -> str:
        self._get_enter()
        print("===== 英语单词管理系统 ======")
        for i, option in enumerate(self.MENU_OPTIONS_MAIN, 1):
            print(f"{i}. {option}")
        print("===========================")
        return input(f"请选择功能 (1-{len(self.MENU_OPTIONS_MAIN)}): ").strip()

    def run_option(self, choice: str) -> None:
        command: Optional[Callable[[], None]] = self.commands.get(choice)
        if command:
            command()
        else:
            print("无效的选择，请重试!")

    def _show_word_details(self, word: Word) -> None:
        print(f"===== {word.spelling} 详情 =====")
        print("释义列表:")
        if word.definitions:
            for idx, definition in enumerate(word.definitions, 1):  # type: int, Definition
                print(f"{idx}. [{definition.pos}] {definition.meaning}")
                if definition.examples:
                    for jdx, example in enumerate(definition.examples, 1):  # type: int, Example
                        print(f"   {jdx}) {example.original_sentence}")
                        print(f"      {example.translated_meaning}")
        else:
            print("  暂无释义")
        print("===========================")

    def option_add_word(self) -> None:
        spelling: str = input("请输入单词拼写: ").strip()
        if not self.word_manager.is_valid_spelling(spelling):
            print("错误: 单词拼写不能为空!")
            return
        
        # 检查单词是否已存在
        if self.word_manager.is_word_exists(spelling):
            print(f"警告: 单词 '{spelling}' 已存在!")
            return
        
        self.word_manager.add_word(spelling)
        print(f"单词 '{spelling}' 添加成功!")

    def option_list_words(self) -> None:
        words: List[Word] = self.word_manager.get_all_words()
        if not words:
            print("没有单词记录!")
            return

        print("\n===== 单词列表 ======")
        for i, word in enumerate(words, 1):  # type: int, Word
            print(f"{i}.", end='')
            self._show_word_details(word)

    def option_search_words(self) -> None:
        keyword: str = input("请输入查询关键词: ").strip()
        if not keyword:
            print("关键词不能为空!")
            return

        results: List[Word] = self.word_manager.search_words(keyword)
        
        if not results:
            print(f"未找到包含 '{keyword}' 的单词")
            return

        page_size: int = PAGE_SIZE
        current_page: int = INITIAL_PAGE
        total_pages: int = max(1, (len(results) + page_size - 1) // page_size)

        while True:
            self._get_enter()
            print(f"===== 单词查询结果 =====")
            print(f"关键词: '{keyword}' | 结果: {len(results)} 个"
                    + (" | 页码: {current_page}/{total_pages}" if total_pages > 1 else ""))
            print("--------------------------")

            start: int = (current_page - 1) * page_size
            end: int = start + page_size
            page_results: List[Word] = results[start:end]
            for i, word in enumerate(page_results, start=1):  # type: int, Word
                print(f"{i}. {word.spelling}")

            print("--------------------------")
            _prompt = "操作: [数字]选择单词" +\
                (" | 'N'下一页" if current_page < total_pages else "") +\
                (" | 'P'上一页" if current_page > 1 else "") + " | 'Q'返回"
            print(_prompt)
            choice: str = input("请输入操作: ").strip().lower()

            if choice.isdigit():
                idx: int = int(choice) - 1
                if 0 <= idx < len(page_results):
                    chosen_word: Word = page_results[idx]
                    break
                else:
                    print("无效的数字选择!")
            elif choice == 'n' and current_page < total_pages:
                current_page += 1
            elif choice == 'p' and current_page > 1:
                current_page -= 1
            elif choice == 'q':
                return
            else:
                print("无效操作!")
        
        self._show_word_details(chosen_word)

        edit: str = input("是否编辑单词? (Y/N): ").strip().lower()
        if edit != 'y':
            return

        self._modify_word(chosen_word)

    def option_save_words(self) -> None:
        self.word_manager.save_words()

    def _modify_word(self, chosen_word: Word) -> None:
        while True:
            self._get_enter()
            self._show_word_details(chosen_word)
            print(f"===== 编辑 {chosen_word.spelling}: ======")
            for i, option in enumerate(self.MENU_OPTIONS_EDIT, 1):
                print(f"{i}. {option}")
            print("===========================")
            choice: str = input("请选择操作 (1-5): ").strip()
            if choice.isdigit():
                idx: int = int(choice)
                if idx == 1:
                    self._add_definition(chosen_word)
                elif idx == 2:
                    self._modify_definition(chosen_word)
                elif idx == 3:
                    self._del_definition(chosen_word)
                elif idx == 4:
                    self.word_manager.del_word(chosen_word)
                    print(f"单词 '{chosen_word.spelling}' 删除成功!")
                    return
                elif idx == 5:
                    return
                else:
                    print("无效的数字选择!")
            else:
                print("无效操作!")

    def option_exit_program(self) -> None:
        print("感谢使用，再见!")
        sys.exit(0)

    def _add_definition(self, word: Word) -> None:
        pos: str = input("请输入词性: ").strip()
        meaning: str = input("请输入释义: ").strip()
        
        if not pos or not meaning:
            print("错误: 词性和释义都不能为空!")
            return
        
        definition = Definition(parent_word=word, pos=pos, meaning=meaning)
        if self.word_manager.add_definition_to_word(word, definition):
            print(f"释义添加成功!\n单词: {word.spelling}\n词性: {pos}\n释义: {meaning}")
        else:
            print("添加失败: 已存在相同的释义!")

    def _modify_definition(self, word: Word) -> None:
        if not word.definitions:
            print("错误: 该单词没有释义!")
            return
        
        self._show_word_details(word)
        print("操作: [数字]选择释义 | 'Q'返回")
        choice: str = input("请输入编号: ").strip().lower()

        if choice.isdigit():
            idx: int = int(choice) - 1
        elif choice == 'q':
            return
        else:
            print("无效操作!")
            return
        
        if 0 <= idx < len(word.definitions):
            definition: Definition = word.definitions[idx]
        else:
            print("无效的编号选择!")

        print("--------------------------")
        for i, option in enumerate(self.MENU_OPTION_EDIT_DEFINITION, 1):
            print(f"{i}. {option}")
        print("--------------------------")
        choice = input("请输入操作: ").strip().lower()

        if choice.isdigit():
            editions = {
                '1': self._modify_meaning,
                '2': self._add_example,
                '3': self._del_example,
            }
            editions[choice](definition)
        else:
            print("无效操作!")
            return

    def _modify_meaning(self, definition: Definition) -> None:
        pos: str = input("请输入新的词性: ").strip()
        meaning: str = input("请输入新的释义: ").strip()
        if self.word_manager.modify_definition(definition, pos, meaning):
            print("修改成功!")
        else:
            print("错误: 词性和释义都不能为空!")

    def _add_example(self, definition: Definition) -> None:
        original_sentence: str = input("请输入例句: ").strip()
        translated_meaning: str = input("请输入例句翻译: ").strip()
        if self.word_manager.add_example_to_definition(definition, original_sentence, translated_meaning):
            print("添加成功!")
        else:
            print("错误: 例句不能为空!")

    def _del_example(self, definition: Definition) -> None:
        if not definition.examples:
            print("错误: 该释义没有例句!")
            return
        print("操作: [数字]选择例句 | 'Q'返回")
        choice: str = input("请输入编号: ").strip().lower()
        if choice.isdigit():
            idx: int = int(choice) - 1
            if 0 <= idx < len(definition.examples) and\
                    self.word_manager.del_example_from_definition(definition, definition.examples[idx]):
                print("删除成功!")
            else:
                print("无效的编号选择!")
        elif choice == 'q':
            return
        else:
            print("无效操作!")

    def _del_definition(self, word: Word) -> None:
        if not word.definitions:
            print("错误: 该单词没有释义!")
            return
        
        self._show_word_details(word)
        print("操作: [数字]选择释义 | 'Q'返回")
        choice: str = input("请输入编号: ").strip().lower()

        if choice.isdigit():
            idx: int = int(choice) - 1
        elif choice == 'q':
            return
        else:
            print("无效操作!")
            return

        if 0 <= idx < len(word.definitions):
            definition: Definition = word.definitions[idx]
            word.del_definition(definition)
            print("删除成功!")
        else:
            print("无效的编号选择!")
