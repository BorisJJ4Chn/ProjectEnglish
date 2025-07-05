import json
import os
from typing import List

# 加载配置文件
try:
    with open(os.path.join(os.path.dirname(__file__), 'settings.json'), 'r', encoding='utf-8') as f:
        settings = json.load(f)
except FileNotFoundError:
    raise Exception("settings.json file not found in src directory")
except json.JSONDecodeError as e:
    raise Exception(f"Error parsing settings.json: {e}")

# 获取配置版本号，默认为1.0.0
config_version = settings.get('version', '1.0.0')

# 根据版本号解析配置
if config_version == '1.0.0':
    # 1.0.0版本的解析逻辑
    PAGE_SIZE: int = settings['pagination']['page_size']
    INITIAL_PAGE: int = settings['pagination']['initial_page']
    WORDS_PATH: str = settings['words_path']
    SEARCH_SIMILARITY: float = settings['search_similarity']
else:
    raise Exception(f"Unsupported configuration version: {config_version}")

# 数据格式版本号，用于文件兼容性检查
DATA_FORMAT_VERSION: str = "1.0.0"