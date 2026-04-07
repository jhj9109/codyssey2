# domain.py
import random
from typing import Optional, List
from models import Quiz

def validate_user_input(user_input: str, min_range: int, max_range: int) -> Optional[int]:
    """
    [순수 함수] 사용자 입력을 검증하여 유효한 숫자면 정수 반환, 아니면 None 반환.
    print()나 무한루프 없이 오직 '검증' 결과만 반환합니다.
    """
    stripped_input = user_input.strip()
    if not stripped_input:
        return None
        
    try:
        choice = int(stripped_input)
        if min_range <= choice <= max_range:
            return choice
        return None
    except ValueError:
        return None

def check_answer(expected_answer: int, user_input: int) -> bool:
    """
    [순수 함수] 입력한 값이 정답인지 판정합니다.
    """
    return expected_answer == user_input

def calculate_final_score(correct_count: int, points_per_question: int = 10, hint_usage_count: int = 0) -> int:
    """
    [순수 함수] 맞힌 개수와 힌트 사용 횟수를 바탕으로 최종 점수를 계산합니다.
    방어 로직: 힌트를 너무 많이 써도 점수가 0점 아래로 내려가지 않도록 차단합니다.
    """
    base_score = correct_count * points_per_question
    penalty = hint_usage_count * 3
    return max(0, base_score - penalty)

def evaluate_best_score(current_best: int, new_score: int) -> int:
    """
    [순수 함수] 기존 최고 점수와 비교하여 새로운 최고 점수를 반환합니다.
    """
    return max(current_best, new_score)

def prepare_quizzes(quiz_list: List[Quiz], count: int, randomize: bool = True) -> List[Quiz]:
    """
    [순수 함수] 원본 리스트를 훼손(Mutate)하지 않고, 출제 조건에 맞춘 새로운 리스트를 생성합니다.
    """
    # 얕은 복사(Shallow Copy)를 통해 원본 배열은 그대로 보호합니다.
    prepared_list = quiz_list[:] 
    
    if randomize:
        random.shuffle(prepared_list)
        
    # 요구한 개수(count)만큼만 잘라서 반환합니다.
    return prepared_list[:count]
