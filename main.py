import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        """
        퀴즈 초기화
        :param question: 문제 내용 (str)
        :param choices: 4개의 선택지 (list)
        :param answer: 정답 번호 1~4 (int)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index):
        """문제와 선택지를 화면에 출력"""
        print(f"\n[문제 {index}] {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_input):
        """사용자 입력값과 정답 비교 (공백 제거 후 비교)"""
        return str(self.answer) == str(user_input).strip()

# 기본 퀴즈 데이터 생성 (주제: (여자)아이들)
initial_quizzes = [
    Quiz("(여자)아이들의 데뷔곡은 무엇인가요?", ["LATATA", "한(HANN)", "Senorita", "덤디덤디"], 1),
    Quiz("(여자)아이들의 리더는 누구인가요?", ["미연", "민니", "소연", "우기"], 3),
    Quiz("다음 중 멤버 미연의 생일은 언제인가요?", ["1월 21일", "1월 31일", "2월 14일", "3월 9일"], 2),
    Quiz("앨범 '2'의 타이틀 곡은 무엇인가요?", ["Queencard", "TOMBOY", "Nxde", "Super Lady"], 4),
    Quiz("(여자)아이들의 공식 팬클럽 명칭은?", ["네버랜드", "원스", "마이", "다이브"], 1)
]


class QuizGame:
    def __init__(self):
        """게임 초기화: 데이터 파일을 불러오거나 기본값을 설정합니다."""
        self.file_path = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        """state.json 파일에서 데이터를 불러옵니다. 파일이 없거나 손상되었으면 기본값을 사용합니다."""
        if not os.path.exists(self.file_path):
            print("[안내] 저장된 데이터 파일이 없어 기본 퀴즈 데이터를 불러옵니다.")
            self.quizzes = initial_quizzes[:] # 앞서 만든 기본 데이터 복사
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                self.best_score = data.get("best_score", 0)
                
                # JSON 데이터의 딕셔너리를 다시 Quiz 객체로 변환
                for q_data in data.get("quizzes", []):
                    quiz = Quiz(q_data["question"], q_data["choices"], q_data["answer"])
                    self.quizzes.append(quiz)
                    
            print("[안내] 저장된 퀴즈 데이터를 성공적으로 불러왔습니다.")
            
        except json.JSONDecodeError:
            print("[오류] 데이터 파일이 손상되었습니다. 기본 퀴즈 데이터로 시작합니다.")
            self.quizzes = initial_quizzes[:]
        except Exception as e:
            print(f"[오류] 파일을 불러오는 중 문제가 발생했습니다: {e}")
            self.quizzes = initial_quizzes[:]

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 파일에 저장합니다."""
        quiz_data = [{"question": q.question, "choices": q.choices, "answer": q.answer} for q in self.quizzes]
        state = {"quizzes": quiz_data, "best_score": self.best_score}
        
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[!] 파일 저장 중 오류가 발생했습니다: {e}")

    # --- 기존 함수들을 메서드로 이식 ---
    
    def play(self):
        """퀴즈 풀기 및 점수 갱신"""
        # 이전에 만든 solve_quiz 로직 활용
        if not self.quizzes:
            print("\n[!] 등록된 퀴즈가 없습니다.")
            return

        correct_count = 0
        points_per_question = 10
        print(f"\n--- 퀴즈 시작! (총 {len(self.quizzes)}문제, 문제당 {points_per_question}점) ---")

        try:
            for i, quiz in enumerate(self.quizzes, 1):
                while True:
                    quiz.display(i)
                    user_input = input("정답 번호를 입력하세요 (1~4): ").strip()
                    
                    if not user_input:
                        print("[!] 입력이 비어 있습니다. 다시 입력해주세요.")
                        continue
                    try:
                        choice = int(user_input)
                        if not (1 <= choice <= 4):
                            print("[!] 1~4 사이의 숫자만 입력 가능합니다.")
                            continue
                    except ValueError:
                        print("[!] 숫자로만 입력해주세요 (예: 1).")
                        continue

                    if quiz.is_correct(choice):
                        print("=> 정답입니다! ✨")
                        correct_count += 1
                    else:
                        print(f"=> 오답입니다. (정답: {quiz.answer}) 😢")
                    break

            score = correct_count * points_per_question
            print(f"\n--- 결과 발표 ---")
            print(f"▶ 맞힌 문항 수: {correct_count} / {len(play_list)} 문제")
            print(f"▶ 최종 획득 점수: {score}점")
            
            # 최고 점수 갱신 로직
            if score > self.best_score:
                print(f"🎉 최고 점수 경신! (기존: {self.best_score}점 -> 새로운 최고 점수: {score}점) 🎉")
                self.best_score = score
                self.save_data() # 갱신 시 자동 저장

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] 퀴즈가 중단되었습니다. 메인 메뉴로 돌아갑니다.")

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
        """프로그램의 메인 루프를 실행합니다."""
        while True:
            print("\n" + "="*30)
            print("💡 나만의 퀴즈 게임 💡")
            print("="*30)
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수 확인")
            print("5. 종료")
            print("="*30)
            
            try:
                choice = input("원하시는 메뉴의 번호를 입력하세요: ").strip()
                
                if choice == '1':
                    self.play()
                elif choice == '2':
                    self.add_quiz()
                elif choice == '3':
                    self.show_list()
                elif choice == '4':
                    self.show_score()
                elif choice == '5':
                    print("\n게임을 종료합니다. 이용해 주셔서 감사합니다! 👋")
                    self.save_data() # 종료 전 안전하게 한 번 더 저장
                    break
                else:
                    print("[!] 1번부터 5번 사이의 숫자를 입력해주세요.")
            
            except (KeyboardInterrupt, EOFError):
                print("\n\n[!] 비정상 종료가 감지되었습니다. 데이터를 저장하고 안전하게 종료합니다.")
                self.save_data()
                break

# 프로그램 실행 진입점
if __name__ == "__main__":
    game = QuizGame()
    game.run()
# 실행 예시 (테스트용)
current_score = solve_quiz(initial_quizzes)