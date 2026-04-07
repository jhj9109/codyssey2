# main.py
import sys
from datetime import datetime
from models import Quiz, GameRecord
import domain
import storage
import views  # View 계층 추가
import signal # 운영체제 시그널 제어 모듈

FILE_PATH = "state.json"

# [핵심 추가] 외부 강제 종료 시그널(SIGTERM)을 위한 커스텀 예외 클래스
class TerminateSignal(Exception):
    pass

class QuizGameController:
    def __init__(self):
        state = storage.load_game_state(FILE_PATH)
        self.quizzes = state["quizzes"]
        self.best_score = state["best_score"]
        self.history = state["history"]

        # 2. SIGTERM 시그널 가로채기 설정 추가!
        # OS로부터 SIGTERM(15) 시그널이 오면, self._sigterm_handler 메서드를 실행하라는 뜻입니다.
        signal.signal(signal.SIGTERM, self._sigterm_handler)

    def _sigterm_handler(self, signum, frame):
        """SIGTERM 시그널을 받으면 강제로 KeyboardInterrupt를 발생시킵니다."""
        # 이렇게 하면 기존에 만들어둔 except (KeyboardInterrupt) 방어막으로 흐름이 넘어가서
        # 똑같이 안전한 저장 및 우아한 종료(Graceful Shutdown)를 수행하게 됩니다.
        raise TerminateSignal()

    def _save(self):
        if storage.save_game_state(FILE_PATH, self.quizzes, self.best_score, self.history):
            views.display_message("\n데이터 저장에 성공했습니다.")
            return True
        else:
            views.display_message("\n[경고] 데이터 저장에 실패했습니다.")
            return False

    def play_quiz(self):
        if not self.quizzes:
            views.display_message("\n[!] 등록된 퀴즈가 없습니다.")
            return

        views.display_message(f"\n현재 총 {len(self.quizzes)}개의 문제가 준비되어 있습니다.")
        
        # 1. 문제 수 입력 (View -> Domain)
        while True:
            count_input = views.get_input(f"몇 문제를 풀고 싶으신가요? (1~{len(self.quizzes)}): ")
            count = domain.validate_user_input(count_input, 1, len(self.quizzes))
            if count is not None: break
            views.display_message(f"[!] 1에서 {len(self.quizzes)} 사이의 올바른 숫자를 입력해주세요.")

        play_list = domain.prepare_quizzes(self.quizzes, count, randomize=True)
        correct_count, hint_usage_count = 0, 0

        views.display_message(f"\n--- 퀴즈 시작! (총 {len(play_list)}문제) ---")
        
        # 2. 퀴즈 진행 루프
        for i, quiz in enumerate(play_list, 1):
            used_hint = False
            while True:
                views.display_question(i, quiz)
                user_input = views.get_input("정답 번호: ").lower()
                if not user_input: continue

                if user_input == 'h':
                    if quiz.hint and not used_hint:
                        views.display_message(f"\n💡 힌트: {quiz.hint}")
                        used_hint, hint_usage_count = True, hint_usage_count + 1
                    elif not quiz.hint:
                        views.display_message("\n[!] 이 문제에는 힌트가 없습니다.")
                    continue

                choice_num = domain.validate_user_input(user_input, 1, 4)
                if choice_num is None:
                    views.display_message("[!] 1~4 사이의 숫자 또는 'h'를 입력해주세요.")
                    continue

                if domain.check_answer(quiz.answer, choice_num):
                    views.display_message("=> 정답입니다! ✨")
                    correct_count += 1
                else:
                    views.display_message(f"=> 오답입니다. (정답: {quiz.answer}) 😢")
                break

        # 3. 점수 계산 및 히스토리 갱신
        final_score = domain.calculate_final_score(correct_count, 10, hint_usage_count)
        self.best_score = domain.evaluate_best_score(self.best_score, final_score)
        
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(GameRecord(now_str, len(play_list), correct_count, final_score))
        views.display_game_result(correct_count, len(play_list), hint_usage_count, final_score)
        self._save()

    def add_quiz(self):
        views.display_message("\n--- 새로운 퀴즈 추가 ---")
        question = ""
        while not question: question = views.get_input("질문을 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = ""
            while not choice: choice = views.get_input(f"선택지 {i}를 입력하세요: ")
            choices.append(choice)

        answer = None
        while answer is None:
            ans_input = views.get_input("정답 번호를 입력하세요 (1~4): ")
            answer = domain.validate_user_input(ans_input, 1, 4)
            if answer is None: views.display_message("[!] 1~4 사이의 올바른 숫자를 입력해주세요.")

        hint = views.get_input("힌트를 입력하세요 (없으면 엔터): ")
        self.quizzes.append(Quiz(question, choices, answer, hint))
        views.display_message("\n=> 퀴즈가 성공적으로 추가되었습니다! ✅")
        self._save()
    
    def delete_quiz(self):
        """퀴즈 삭제 제어 로직"""
        # 1. 먼저 목록을 보여줍니다. (View 활용)

        views.display_quiz_list(self.quizzes)
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        index = None
        while index is None:
            idx_input = views.get_input("삭제할 퀴즈의 번호를 입력하세요 (취소: 0)")
            index = domain.validate_user_input(idx_input, 0, len(self.quizzes))
            if index is None:
                views.display_message("[!] 올바른 번호를 입력해주세요.")
                continue
            if index == 0:
                views.display_message("삭제가 취소되었습니다.")
                return
    
        # 4. 삭제 실행 (Domain 순수 함수 활용)
        self.quizzes.pop(index - 1)
        # 5. 상태 변경 후 저장
        views.display_message(f"=> {index}번 퀴즈가 성공적으로 삭제되었습니다! 🗑️")
        self._save()

    def run(self):
        try:
            while True:
                choice = views.display_main_menu()

                if choice == '1': self.play_quiz()
                elif choice == '2': self.add_quiz()
                elif choice == '3': self.delete_quiz()
                elif choice == '4': views.display_quiz_list(self.quizzes)
                elif choice == '5': views.display_best_score(self.best_score)
                elif choice == '6': views.display_history(self.history)
                elif choice == '7':
                    views.display_message("\n게임을 종료합니다. 👋")
                    # self._save() 삭제됨 (이미 동기화되어 있으므로 불필요)
                    break
                else:
                    views.display_message(f"[!] 올바른 메뉴 번호를 입력해주세요.{choice}")

        except (KeyboardInterrupt, EOFError):
            views.display_message(f"\n\n[!] 프로그램 중단 요청(Ctrl+C 또는 Ctrl+D)을 감지했습니다. 안전하게 종료합니다. 👋")
            # self._save() 삭제됨 (강제 종료 시점에도 데이터는 이미 안전함)
            sys.exit(0)

        except TerminateSignal:
            # 2. 시스템(OS)에 의한 강제 종료 시그널 (kill <PID>)
            views.display_message("\n\n[!] 시스템의 강제 종료 요청(SIGTERM) 감지.")
            views.display_message("프로세스를 정리하고 우아하게(Graceful) 종료합니다. 👋")
            sys.exit(0)

        except Exception as e:
            # 2. 우리가 예측하지 못한 시스템 내부의 치명적 버그 (비정상 상황)
            # 실무에서는 이 부분을 파일 로그(logger)로 남기거나 에러 수집 서버(Sentry 등)로 전송합니다.
            views.display_message("\n\n🔥 [치명적 시스템 오류 발생] 🔥")
            views.display_message(f"오류 상세 내용: {e}") 
            views.display_message("안전하게 프로그램을 종료합니다. 👋")
            # self._save() 삭제됨 (오염된 상태를 파일에 쓰지 않기 위해 제거!)
            sys.exit(1)  # 1: 비정상 종료를 의미하는 상태 코드


if __name__ == "__main__":
    app = QuizGameController()
    app.run()
