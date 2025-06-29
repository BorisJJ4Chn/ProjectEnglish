from typing import List, Optional
from word import Word, Definition, Example

class WordManager:
    def __init__(self) -> None:
        self.words = []
        self.load_words()
        
    def load_words(self) -> None:
        # 实际应用中可从文件或数据库加载
        self.words = [Word("apple"), Word("banana"), Word("cherry"), Word("date")]
        
    def add_word(self, spelling: str) -> bool:
        # 业务规则校验：非空且不重复
        if spelling and isinstance(spelling, str):
            spelling = spelling.strip()
            # 检查单词是否已存在（通过拼写）
            if not any(word.spelling == spelling for word in self.words):
                self.words.append(Word(spelling))
                return True
        return False

    def del_word(self, word: Word) -> bool:
        # 业务规则校验：存在
        if isinstance(word, Word) and word in self.words:
            self.words.remove(word)
            return True
        return False

    def add_definition_to_word(self, word: Word, definition: Definition) -> bool:
        # 业务规则校验：不重复
        if isinstance(word, Word) and isinstance(definition, Definition):
            # 检查释义是否已存在
            if all(ori_definition != definition for ori_definition in word.definitions):
                word.definitions.append(definition)
                return True
        return False

    def del_definition_from_word(self, word: Word, definition: Definition) -> bool:
        # 业务规则校验：存在
        if isinstance(word, Word) and isinstance(definition, Definition):
            # 检查释义是否存在
            if definition in word.definitions:
                word.del_definition(definition)
                return True
        return False
        
    def get_all_words(self) -> List[Word]:
        # 返回按拼写排序后的单词列表
        return sorted(self.words, key=lambda word: word.spelling)

    def is_valid_spelling(self, spelling: str) -> bool:
        # 检查拼写是否有效（非空字符串）
        return spelling and isinstance(spelling, str)

    def is_word_exists(self, spelling: str) -> bool:
        # 检查单词是否存在（通过拼写）
        return any(word.spelling == spelling for word in self.words)

    def search_words(self, keyword: str) -> List[Word]:
        # 按拼写搜索并排序
        if not keyword:
            return []
        keyword_lower = keyword.lower()
        results: List[Word] = [
            word for word in self.words
            if keyword_lower in word.spelling.lower()
        ]
        # 按匹配位置和长度排序
        results.sort(key=lambda x: (
            x.spelling.lower().index(keyword_lower),
            len(x.spelling)
        ))
        return results
        
    def clear_all(self) -> None:
        self.words = []
        self.load_words()  # 重置为初始数据