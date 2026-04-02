# bonus/bonus_main.py
import json
import os
import random  # 보너스 1: random 모듈 추가

class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint  # [보너스 3] 힌트 속성 추가

    def display(self, index):
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")
        if self.hint:
            print("  (힌트를 보려면 'h' 또는 'hint'를 입력하세요.)")

    def is_correct(self, user_input):
        return str(self.answer) == str(user_input).strip()

# 기본 데이터에 힌트 추가
initial_quizzes = [
    Quiz("(여자)아이들의 데뷔곡은 무엇인가요?", ["LATATA", "한(HANN)", "Senorita", "덤디덤디"], 1, "L로 시작하는 강렬한 곡입니다."),
    Quiz("(여자)아이들의 리더는 누구인가요?", ["미연", "민니", "소연", "우기"], 3, "천재 프로듀서로 불리는 멤버입니다."),
    Quiz("다음 중 멤버 미연의 생일은 언제인가요?", ["1월 21일", "1월 31일", "2월 14일", "3월 9일"], 2, "1월의 마지막 날입니다."),
    Quiz("앨범 '2'의 타이틀 곡은 무엇인가요?", ["Queencard", "TOMBOY", "Nxde", "Super Lady"], 4, "웅장한 에너지가 느껴지는 곡 제목입니다."),
    Quiz("(여자)아이들의 공식 팬클럽 명칭은?", ["네버랜드", "원스", "마이", "다이브"], 1, "피터팬이 사는 그곳의 이름입니다.")
]
class QuizGame:
    def __init__(self):
        # 보너스 폴더 내에서 독립적으로 실행되도록 동일 경로의 state.json 사용
        self.file_path = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path):
            self.quizzes = initial_quizzes[:]
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                for q_data in data.get("quizzes", []):
                    self.quizzes.append(Quiz(q_data["question"], q_data["choices"], q_data["answer"], q_data.get("hint", "")))
        except Exception:
            self.quizzes = initial_quizzes[:]

    def save_data(self):
        quiz_data = [{
            "question": q.question, 
            "choices": q.choices, 
            "answer": q.answer,
            "hint": q.hint # 힌트 저장 추가
        } for q in self.quizzes]
        state = {"quizzes": quiz_data, "best_score": self.best_score}
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=4)
        except Exception as e:
            pass

    def play(self):
        if not self.quizzes:
            print("\n[!] 등록된 퀴즈가 없습니다.")
            return

        # [보너스 1] 랜덤 출제
        play_list = self.quizzes[:]
        random.shuffle(play_list)

        # [보너스 2] 문제 수 선택 로직 추가
        total_available = len(play_list)
        print(f"\n현재 총 {total_available}개의 문제가 준비되어 있습니다.")
        
        while True:
            count_input = input(f"몇 문제를 풀고 싶으신가요? (1~{total_available}): ").strip()
            if not count_input:
                print("[!] 숫자를 입력해주세요.")
                continue
            try:
                count = int(count_input)
                if 1 <= count <= total_available:
                    # 선택한 수만큼 리스트 슬라이싱
                    play_list = play_list[:count]
                    break
                else:
                    print(f"[!] 1에서 {total_available} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("[!] 숫자로만 입력해주세요.")
            except (KeyboardInterrupt, EOFError):
                print("\n[!] 문제 수 선택이 취소되었습니다.")
                return

        score = 0
        correct_count = 0
        base_points = 10     # 기본 점수
        hint_penalty = 3    # 힌트 사용 시 차감 점수
        
        print(f"\n--- 퀴즈 시작! (기본 {base_points}점 / 힌트 사용 시 {base_points - hint_penalty}점) ---")

        try:
            for i, quiz in enumerate(play_list, 1):
                used_hint = False
                while True:
                    quiz.display(i)
                    user_input = input("정답 번호를 입력하세요 (1~4): ").strip().lower()
                    
                    if not user_input: continue
                    
                    # 힌트 요청 처리
                    if user_input in ['h', 'hint']:
                        if quiz.hint:
                            print(f"\n💡 힌트: {quiz.hint}")
                            used_hint = True
                        else:
                            print("\n[!] 이 문제에는 힌트가 없습니다.")
                        continue

                    try:
                        choice = int(user_input)
                        if not (1 <= choice <= 4): continue
                    except ValueError:
                        print("[!] 숫자(1~4) 또는 힌트(h)를 입력해주세요.")
                        continue

                    if quiz.is_correct(choice):
                        print("=> 정답입니다! ✨")
                        correct_count += 1
                        # 힌트 사용 여부에 따라 점수 합산
                        score += (base_points - hint_penalty) if used_hint else base_points
                    else:
                        print(f"=> 오답입니다. (정답: {quiz.answer}) 😢")
                    break

            print(f"\n--- 결과 발표 ---")
            print(f"맞힌 개수: {correct_count} / {len(play_list)}")
            print(f"최종 획득 점수: {score}점")
            
            if score > self.best_score:
                print(f"🎉 최고 점수 경신! (새로운 최고 점수: {score}점) 🎉")
                self.best_score = score
                self.save_data()

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] 퀴즈가 중단되었습니다.")

    def add_quiz(self):
        """퀴즈 추가"""
        print("\n--- 새로운 퀴즈 추가 ---")
        try:
            while True:
                question = input("질문을 입력하세요: ").strip()
                if question: break
                print("[!] 질문은 비어있을 수 없습니다.")

            choices = []
            for i in range(1, 5):
                while True:
                    choice = input(f"선택지 {i}를 입력하세요: ").strip()
                    if choice:
                        choices.append(choice)
                        break
                    print("[!] 비어있을 수 없습니다.")

            while True:
                answer_input = input("정답 번호를 입력하세요 (1~4): ").strip()
                try:
                    answer = int(answer_input)
                    if 1 <= answer <= 4: break
                    print("[!] 1~4 사이의 숫자만 입력 가능합니다.")
                except ValueError:
                    print("[!] 숫자로만 입력해주세요.")

            self.quizzes.append(Quiz(question, choices, answer))
            self.save_data() # 추가 시 자동 저장
            print("\n=> 퀴즈가 성공적으로 추가되었습니다! ✅")

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] 추가가 중단되었습니다.")

    def delete_quiz(self):
        """등록된 퀴즈를 목록에서 선택하여 삭제합니다."""
        print("\n--- 퀴즈 삭제 ---")
        if not self.quizzes:
            print("[!] 삭제할 퀴즈가 없습니다.")
            return

        # 현재 목록을 먼저 보여줌
        self.show_list()
        
        try:
            while True:
                choice_input = input("삭제할 퀴즈의 번호를 입력하세요 (취소: 0): ").strip()
                if choice_input == '0':
                    print("삭제가 취소되었습니다.")
                    return
                
                try:
                    index = int(choice_input)
                    if 1 <= index <= len(self.quizzes):
                        # 삭제 확인 절차
                        removed_quiz = self.quizzes.pop(index - 1)
                        self.save_data() # 삭제 후 즉시 파일 저장
                        print(f"\n=> [질문: {removed_quiz.question[:20]}...] 항목이 성공적으로 삭제되었습니다. 🗑️")
                        break
                    else:
                        print(f"[!] 1에서 {len(self.quizzes)} 사이의 번호를 입력해주세요.")
                except ValueError:
                    print("[!] 숫자로만 입력해주세요.")
        
        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] 삭제 과정이 중단되었습니다.")

    def show_list(self):
        """퀴즈 목록 출력"""
        print("\n--- 등록된 퀴즈 목록 ---")
        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다.")
            return
        for i, quiz in enumerate(self.quizzes, 1):
            q_summary = quiz.question[:30] + "..." if len(quiz.question) > 30 else quiz.question
           # [Hotfix] 정답 노출 제거
            print(f"{i}. {q_summary}")
        print("------------------------")

    def show_score(self):
        """최고 점수 출력"""
        print("\n--- 🏆 최고 점수 확인 🏆 ---")
        if self.best_score > 0:
            print(f"현재 최고 점수는 {self.best_score}점 입니다!")
        else:
            print("아직 기록된 점수가 없습니다. 첫 퀴즈에 도전해 보세요!")
        print("----------------------------")

    # --- 메인 메뉴 실행 흐름 ---
    
    def run(self):
        """메뉴에 삭제 옵션(6번) 추가"""
        while True:
            print("\n" + "="*30)
            print("💡 나만의 퀴즈 게임 (Bonus) 💡")
            print("="*30)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수 확인")
            print("5. 퀴즈 삭제 (New!)") # 메뉴 추가
            print("6. 종료")
            print("="*30)
            
            try:
                choice = input("원하시는 메뉴의 번호를 입력하세요: ").strip()
                
                if choice == '1': self.play()
                elif choice == '2': self.add_quiz()
                elif choice == '3': self.show_list()
                elif choice == '4': self.show_score()
                elif choice == '5': self.delete_quiz() # 삭제 메서드 연결
                elif choice == '6':
                    print("\n게임을 종료합니다. 👋")
                    self.save_data()
                    break
                else:
                    print("[!] 올바른 메뉴 번호를 입력해주세요.")
            except (KeyboardInterrupt, EOFError):
                self.save_data()
                break

# 프로그램 실행 진입점
if __name__ == "__main__":
    game = QuizGame()
    game.run()