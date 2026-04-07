# views.py
from typing import List
from models import Quiz, GameRecord

def display_main_menu() -> str:
    print("\n" + "="*30)
    print("💡 나만의 퀴즈 게임 (Ultimate MVC Ver.) 💡")
    print("="*30)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 삭제")
    print("4. 퀴즈 목록")
    print("5. 최고 점수 확인")
    print("6. 전체 기록 보기")
    print("7. 종료")
    print("="*30)
    return input("원하시는 메뉴의 번호를 입력하세요: ").strip()

def display_message(message: str):
    """일반 메시지나 에러를 출력할 때 사용합니다."""
    print(message)

def get_input(prompt: str) -> str:
    """단순 입력을 받을 때 사용합니다."""
    return input(prompt).strip()

def display_quiz_list(quizzes: List[Quiz]):
    print("\n--- 등록된 퀴즈 목록 ---")
    if not quizzes:
        print("현재 등록된 퀴즈가 없습니다.")
        return
    for i, quiz in enumerate(quizzes, 1):
        q_summary = quiz.question[:30] + "..." if len(quiz.question) > 30 else quiz.question
        print(f"{i}. {q_summary}")
    print("------------------------")

def display_best_score(best_score: int):
    print("\n--- 🏆 최고 점수 확인 🏆 ---")
    if best_score > 0:
        print(f"현재 최고 점수는 {best_score}점 입니다!")
    else:
        print("아직 기록된 점수가 없습니다.")
    print("----------------------------")

def display_history(history: List[GameRecord]):
    print("\n--- 📜 전체 게임 기록 히스토리 📜 ---")
    if not history:
        print("아직 저장된 기록이 없습니다.")
        return
    print(f"{'일시':<20} | {'문항수':<5} | {'정답수':<5} | {'점수':<5}")
    print("-" * 50)
    for entry in history:
        print(f"{entry.date:<20} | {entry.total_questions:<8} | {entry.correct_count:<8} | {entry.score}점")
    print("-" * 50)

def display_question(index: int, quiz: Quiz):
    print(f"\n[문제 {index}] {quiz.question}")
    for j, choice in enumerate(quiz.choices, 1):
        print(f"  {j}. {choice}")
    if quiz.hint:
        print("  (힌트를 보려면 'h' 입력)")

def display_game_result(correct_count: int, total_count: int, hint_count: int, final_score: int):
    print("\n" + "="*30)
    print("       📊 퀴즈 결과 발표 📊")
    print("="*30)
    print(f"▶ 맞힌 문항 수: {correct_count} / {total_count} 문제")
    print(f"▶ 사용한 힌트: {hint_count}회")
    print(f"▶ 최종 획득 점수: {final_score}점")
    print("="*30)