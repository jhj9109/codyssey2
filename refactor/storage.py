# storage.py
import json
import os
from typing import Dict, Any, List
from dataclasses import asdict
from models import Quiz, GameRecord

# 파일 손상 시 시스템을 구출할 최후의 보루 (기본 데이터)
DEFAULT_QUIZZES = [
    Quiz("(여자)아이들의 데뷔곡은 무엇인가요?", ["LATATA", "한(HANN)", "Senorita", "덤디덤디"], 1, "L로 시작하는 강렬한 곡입니다."),
    Quiz("(여자)아이들의 리더는 누구인가요?", ["미연", "민니", "소연", "우기"], 3, "천재 프로듀서로 불리는 멤버입니다."),
    Quiz("다음 중 멤버 미연의 생일은 언제인가요?", ["1월 21일", "1월 31일", "2월 14일", "3월 9일"], 2, "1월의 마지막 날입니다."),
    Quiz("앨범 '2'의 타이틀 곡은 무엇인가요?", ["Queencard", "TOMBOY", "Nxde", "Super Lady"], 4, "웅장한 에너지가 느껴지는 곡 제목입니다."),
    Quiz("(여자)아이들의 공식 팬클럽 명칭은?", ["네버랜드", "원스", "마이", "다이브"], 1, "피터팬이 사는 그곳의 이름입니다.")
]

def load_game_state(file_path: str) -> Dict[str, Any]:
    """
    [인프라 함수] 파일에서 데이터를 안전하게 불러와 도메인 모델 객체로 역직렬화(Deserialize) 합니다.
    파일 부재, JSON 파싱 에러 등 모든 예외 상황을 조용히 처리하고 기본값을 반환합니다.
    """
    if not os.path.exists(file_path):
        return {"quizzes": DEFAULT_QUIZZES[:], "best_score": 0, "history": []}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1. JSON 딕셔너리 리스트 -> Quiz 객체 리스트로 복원
        loaded_quizzes = [
            Quiz(
                question=q["question"],
                choices=q["choices"],
                answer=q["answer"],
                hint=q.get("hint", "")
            ) for q in data.get("quizzes", [])
        ]

        # 2. JSON 딕셔너리 리스트 -> GameRecord 객체 리스트로 복원
        loaded_history = [
            GameRecord(
                date=h["date"],
                total_questions=h["total_questions"],
                correct_count=h["correct_count"],
                score=h["score"]
            ) for h in data.get("history", [])
        ]

        # 불러온 퀴즈가 비어있다면 기본 데이터 사용
        final_quizzes = loaded_quizzes if loaded_quizzes else DEFAULT_QUIZZES[:]

        return {
            "quizzes": final_quizzes,
            "best_score": data.get("best_score", 0),
            "history": loaded_history
        }

    except (json.JSONDecodeError, Exception):
        # 실무 시스템이라면 여기서 logger.error("데이터 훼손 감지")를 호출하여 모니터링 팀에 알립니다.
        return {"quizzes": DEFAULT_QUIZZES[:], "best_score": 0, "history": []}

def save_game_state(file_path: str, quizzes: List[Quiz], best_score: int, history: List[GameRecord]) -> bool:
    """
    [인프라 함수] 현재 시스템의 객체 상태를 JSON 포맷으로 직렬화(Serialize)하여 영구 저장합니다.
    저장 성공 여부를 boolean으로 반환하여, 호출부(UI)가 사용자에게 올바른 피드백을 줄 수 있게 합니다.
    """
    # 데이터클래스들을 JSON이 이해할 수 있는 기본 자료형(dict)으로 패키징
    state = {
        "quizzes": [asdict(q) for q in quizzes],
        "best_score": best_score,
        "history": [asdict(h) for h in history]
    }

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
        return True # 정상 저장 완료
    except Exception:
        # 파일 시스템 권한 문제, 디스크 용량 부족 등의 에러
        return False # 저장 실패