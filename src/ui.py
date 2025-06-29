import os
import sys
from typing import List, Optional
from logic import WordManager
from word import Word, Definition

class EnglishUI:
    def __init__(self, word_manager: WordManager):
        self.word_manager = word_manager

    def _get_enter(self) -> None:
        input("回车以继续...")
        os.system('cls')

    def greet_user(self) -> None:
        print("===== 欢迎使用英语单词管理系统 =====")

    def display_menu(self) -> str:
        self._get_enter()
        print("===== 英语单词管理系统 ======")
        print("1. 添加新单词")
        print("2. 查询单词")
        print("3. 列出所有单词")
        print("4. 退出程序")
        print("===========================")
        return input("请选择功能 (1-4): ").strip()

    def _show_word_details(self, word: Word) -> None:
        print(f"===== {word.spelling} 详情 =====")
        print("释义列表:")
        if word.definitions:
            for idx, definition in enumerate(word.definitions, 1):  # type: int, Definition
                print(f"{idx}. [{definition.pos}] {definition.meaning}")
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
            print(f"{i}. {word.spelling}")
            if word.definitions:
                for j, definition in enumerate(word.definitions, 1):  # type: int, Definition
                    print(f"   {j}. [{definition.pos}] {definition.meaning}")
            else:
                print("   暂无释义")
            print("-------------------------")

    def option_search_words(self) -> None:
        keyword: str = input("请输入查询关键词: ").strip()
        if not keyword:
            print("关键词不能为空!")
            return

        results: List[Word] = self.word_manager.search_words(keyword)
        
        if not results:
            print(f"未找到包含 '{keyword}' 的单词")
            return

        page_size: int = 10
        current_page: int = 1
        total_pages: int = max(1, (len(results) + page_size - 1) // page_size)

        while True:
            self._get_enter()
            print(f"===== 单词查询结果 =====")
            print(f"关键词: '{keyword}' | 结果: {len(results)} 个 | 页码: {current_page}/{total_pages}")
            print("--------------------------")

            start: int = (current_page - 1) * page_size
            end: int = start + page_size
            page_results: List[Word] = results[start:end]
            for i, word in enumerate(page_results, start=1):  # type: int, Word
                print(f"{i}. {word.spelling}")

            print("--------------------------")
            print("操作: [数字]选择单词 | 'N'下一页 | 'P'上一页 | 'Q'返回")
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

        while True:
            self._get_enter()
            print(f"===== 编辑 {chosen_word.spelling}: ======")
            print("--------------------------")
            print("1. 添加释义")
            print("2. 修改释义")
            print("3. 删除释义")
            print("4. 删除单词")
            print("5. 退出编辑")
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
        choice: str = input("请输入操作: ").strip().lower()

        if choice.isdigit():
            idx: int = int(choice) - 1
        elif choice == 'q':
            return
        else:
            print("无效操作!")
        
        if 0 <= idx < len(word.definitions):
            definition: Definition = word.definitions[idx]
            pos: str = input("请输入新的词性: ").strip()
            meaning: str = input("请输入新的释义: ").strip()
            if pos and meaning:
                definition.pos = pos
                definition.meaning = meaning
                print("修改成功!")
            else:
                print("错误: 词性和释义都不能为空!")
        else:
            print("无效的编号选择!")

    def _del_definition(self, word: Word) -> None:
        if not word.definitions:
            print("错误: 该单词没有释义!")
            return
        
        self._show_word_details(word)
        print("操作: [数字]选择释义 | 'Q'返回")
        choice: str = input("请输入操作: ").strip().lower()

        if choice.isdigit():
            idx: int = int(choice) - 1
        elif choice == 'q':
            return
        else:
            print("无效操作!")

        if 0 <= idx < len(word.definitions):
            definition: Definition = word.definitions[idx]
            word.del_definition(definition)
            print("删除成功!")
        else:
            print("无效的编号选择!")
