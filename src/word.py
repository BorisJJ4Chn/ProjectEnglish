from typing import List

class Example:
    def __init__(self, parent_word: 'Word', original_sentence: str, translated_meaning: str) -> None:
        # 所属单词（Word对象）
        self.parentWord = parent_word
        
        # 原句（字符串类型）
        self.original_sentence = original_sentence.strip() if isinstance(original_sentence, str) else ""
        # 译句（字符串类型）
        self.translated_meaning = translated_meaning.strip() if isinstance(translated_meaning, str) else ""
    
    def __str__(self):
        """字符串表示，便于打印和显示"""
        return f"{self.original_sentence} -> {self.translated_meaning}"
    
    def __repr__(self):
        """官方字符串表示，便于调试"""
        return f"Example(parentWord={repr(self.parentWord)}, original_sentence='{self.original_sentence}', translated_meaning='{self.translated_meaning}')"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Example):
            return self.original_sentence == value.original_sentence and self.translated_meaning == value.translated_meaning
        return False


class Definition:
    def __init__(self, parent_word: 'Word', pos: str = "", meaning: str = "") -> None:
        # 所属单词（Word对象）
        self.parentWord = parent_word
        
        # 词性（字符串类型）
        self.pos = pos.strip() if isinstance(pos, str) else ""
        
        # 释义内容
        self.meaning = meaning.strip() if isinstance(meaning, str) else ""
        
        # 例句列表
        self.examples: List[Example] = []
        
    def add_example(self, example: Example) -> None:
        """添加例句到列表"""
        if isinstance(example, Example) and example not in self.examples:
            self.examples.append(example)

    def del_example(self, example: Example) -> None:
        """删除例句"""
        if isinstance(example, Example) and example in self.examples:
            self.examples.remove(example)
            
    def __str__(self):
        """字符串表示，便于打印和显示"""
        pos_str: str = f"({self.pos}) " if self.pos else ""
        meaning_str: str = self.meaning if self.meaning else "无释义"
        examples_str: str = "; ".join(str(e) for e in self.examples) if self.examples else "无例句"
        return f"{pos_str}{meaning_str} [{examples_str}]"
        
    def __repr__(self):
        """官方字符串表示，便于调试"""
        return f"Definition(parentWord={repr(self.parentWord)}, pos='{self.pos}', meaning='{self.meaning}', examples={self.examples})"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Definition):
            return self.pos == value.pos and self.meaning == value.meaning
        return False


class Word:
    def __init__(self, spelling: str):
        # 单词拼写（字符串类型）
        self.spelling = spelling.strip()
        
        # 单词释义列表（默认为空列表）
        self.definitions: List[Definition] = []
    
    def add_definition(self, definition: Definition) -> None:
        """添加Definition对象到列表"""
        if isinstance(definition, Definition) and definition not in self.definitions:
            self.definitions.append(definition)

    def del_definition(self, definition: Definition) -> None:
        """删除Definition对象"""
        if isinstance(definition, Definition) and definition in self.definitions:
            self.definitions.remove(definition)
            definition.parentWord = None
    
    def __str__(self):
        """字符串表示，便于打印和显示"""
        return f"{self.spelling}: {'; '.join(str(d) for d in self.definitions) if self.definitions else '无释义'}"
    
    def __repr__(self):
        """官方字符串表示，便于调试"""
        return f"Word(spelling='{self.spelling}', definitions={[repr(d) for d in self.definitions]})"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, Word):
            return self.spelling == value.spelling
        return False