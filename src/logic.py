import sys
import os
import json
from typing import List, Optional, Dict
from word import Word, Definition, Example
from algo import ratio, partial_ratio
from settings import WORDS_PATH, SEARCH_SIMILARITY

class WordManager:
    def __init__(self) -> None:
        self.words: List[Word] = []
        self.load_words(WORDS_PATH)
        
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
        keyword_lower: str = keyword.lower()
        results: List[Word] = [word for word in self.words if\
            keyword_lower in word.spelling.lower() or\
            ratio(keyword, word.spelling) > SEARCH_SIMILARITY]
        results.sort(key=lambda x: (
            ratio(keyword, x.spelling),
            len(x.spelling)
        ))
        return results
        
    def clear_all(self) -> None:
        self.words = []

    def modify_definition(self, definition: Definition, pos: str, meaning: str) -> bool:
        # 业务规则校验：存在且不重复
        if isinstance(definition, Definition) and pos and meaning:
            # 检查释义是否已存在
            if all(ori_definition != definition for ori_definition in definition.parentWord.definitions):
                definition.pos = pos
                definition.meaning = meaning
                return True
        return False

    def add_example_to_definition(self, definition: Definition, original_sentence: str, translated_meaning: str) -> bool:
        example = Example(definition.parentWord, original_sentence, translated_meaning)
        # 业务规则校验：存在且不重复
        if isinstance(definition, Definition) and example:
            # 检查例句是否已存在
            if all(ori_example != example for ori_example in definition.examples):
                definition.add_example(example)
                return True
        return False

    def del_example_from_definition(self, definition: Definition, example: Example) -> bool:
        # 业务规则校验：存在
        if isinstance(definition, Definition) and isinstance(example, Example):
            # 检查例句是否存在
            if example in definition.examples:
                definition.del_example(example)
                return True
        return False
    
    def save_words(self) -> bool:
        """
        将当前单词列表保存到JSON文件
        返回: 保存成功返回True，失败返回False
        """
        try:
            # 构建保存路径
            file_path = os.path.join(os.path.dirname(__file__), 'words.json')
            
            # 转换单词数据为JSON可序列化格式
            words_data = []
            for word in self.words:
                definitions = []
                for definition in word.definitions:
                    examples = [{
                        'original_sentence': example.original_sentence,
                        'translated_meaning': example.translated_meaning
                    } for example in definition.examples]
                    
                    definitions.append({
                        'pos': definition.pos,
                        'meaning': definition.meaning,
                        'examples': examples
                    })
                
                words_data.append({
                    'spelling': word.spelling,
                    'definitions': definitions
                })
            
            # 写入JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(words_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存单词失败: {str(e)}", file=sys.stderr)
            return False

    def load_words(self, file_path: str) -> bool:
        """
        从指定路径加载单词数据
        参数:
            file_path (str): 单词数据文件路径
        返回:
            bool: 加载成功返回True，失败返回False
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                words_data = json.load(f)
                
            # 清空当前单词列表
            self.words = []
            
            # 解析并添加单词
            for word_data in words_data:
                spelling = word_data['spelling']
                definitions: List[Dict[str, str]] = word_data['definitions']
                
                # 创建单词实例
                word = Word(spelling)
                
                # 添加释义
                for def_data in definitions:
                    pos = def_data['pos']
                    meaning = def_data['meaning']
                    definition = Definition(parent_word=word, pos=pos, meaning=meaning)
                    
                    # 添加例句
                    for example_data in def_data.get('examples', []):
                        original_sentence = example_data['original_sentence']
                        translated_meaning = example_data['translated_meaning']
                        example = Example(definition.parentWord, original_sentence, translated_meaning)
                        definition.add_example(example)
                    
                    # 添加释义到单词
                    word.add_definition(definition)
                
                self.words.append(word)
                    
            return True
        except Exception as e:
            print(f"加载单词失败: {str(e)}", file=sys.stderr)
            return False
            