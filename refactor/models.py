# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Quiz:
    """개별 퀴즈 데이터를 정의하는 모델"""
    question: str
    choices: List[str]
    answer: int
    hint: str = ""  # 힌트는 필수가 아니므로 기본값 빈 문자열 부여

@dataclass
class GameRecord:
    """게임 플레이 결과(히스토리)를 정의하는 모델"""
    date: str
    total_questions: int
    correct_count: int
    score: int