import json
import os

class Color:
    # 텍스트 색상
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # 색상 초기화 (필수!)

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
        print(f"\n{Color.BOLD}[문제 {index}] {self.question}{Color.END}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {Color.BLUE}{i}.{Color.END} {choice}")

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

    def set_default_data(self):
        """기본 퀴즈 데이터를 설정하고 최고 점수를 초기화합니다. (파일이 없거나 손상되었을 때 사용)"""
        self.quizzes = initial_quizzes[:]
        self.best_score = 0

    def load_data(self):
        """state.json 파일에서 데이터를 불러옵니다. 파일이 없거나 손상되었으면 기본값을 사용합니다."""
        if not os.path.exists(self.file_path):
            print(f"{Color.YELLOW}[안내] 저장된 데이터 파일이 없어 기본 퀴즈 데이터를 불러옵니다.{Color.END}")
            self.set_default_data()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                self.best_score = data["best_score"]
                self.quizzes = [
                Quiz(q_data["question"], q_data["choices"], q_data["answer"]) 
                    for q_data in data["quizzes"]
                ]
                    
            print(f"{Color.CYAN}[성공] 저장된 퀴즈 데이터를 성공적으로 불러왔습니다.{Color.END}")
            
        except json.JSONDecodeError:
            print(f"{Color.RED}[오류] 데이터 파일이 손상되었습니다. 기본 퀴즈 데이터로 시작합니다.{Color.END}")
            self.set_default_data()
        except KeyError as e:
            print(f"{Color.RED}[오류] 데이터 파일에 필수 항목({e})이 누락되었습니다. 기본 데이터로 시작합니다.{Color.END}")
            self.set_default_data()
        except ValueError as ve:
            print(f"{Color.RED}[오류] 데이터 구조 문제: {ve} 기본 데이터로 시작합니다.{Color.END}")
            self.set_default_data()
        except Exception as e:
            print(f"{Color.RED}[오류] 파일을 불러오는 중 문제가 발생했습니다: {e}{Color.END}")
            self.set_default_data()

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 파일에 저장합니다."""
        quiz_data = [{"question": q.question, "choices": q.choices, "answer": q.answer} for q in self.quizzes]
        best_score = self.best_score
        state = {"quizzes": quiz_data, "best_score": best_score}
        
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"{Color.RED}[!] 파일 저장 중 오류가 발생했습니다: {e}{Color.END}")

    # --- 기존 함수들을 메서드로 이식 ---
    
    def play(self):
        """퀴즈 풀기 및 점수 갱신"""
        # 이전에 만든 solve_quiz 로직 활용
        if not self.quizzes:
            print(f"\n{Color.RED}[!] 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요!{Color.END}")
            return

        correct_count = 0
        points_per_question = 10
        print(f"\n{Color.BOLD}{Color.BLUE}--- 🎮 퀴즈 시작! (총 {len(self.quizzes)}문제, 문제당 {points_per_question}점) ---{Color.END}")

        try:
            for i, quiz in enumerate(self.quizzes, 1):
                while True:
                    quiz.display(i)
                    user_input = input(f"{Color.YELLOW}👉 정답 번호를 입력하세요 (1~4): {Color.END}").strip()
                    
                    if not user_input:
                        print(f"{Color.RED}[!] 입력이 비어 있습니다. 다시 입력해주세요.{Color.END}")
                        continue
                    try:
                        choice = int(user_input)
                        if not (1 <= choice <= 4):
                            print(f"{Color.RED}[!] 1~4 사이의 숫자만 입력 가능합니다.{Color.END}")
                            continue
                    except ValueError:
                        print(f"{Color.RED}[!] 숫자로만 입력해주세요 (예: 1).{Color.END}")
                        continue

                    if quiz.is_correct(choice):
                        print(f"{Color.BOLD}{Color.GREEN}✅ 정답입니다! 아주 멋져요! ✨{Color.END}")
                        correct_count += 1
                    else:
                        print(f"{Color.BOLD}{Color.RED}❌ 오답입니다. (정답은 {quiz.answer}번이었습니다) 😢{Color.END}")
                    break

            score = correct_count * points_per_question
            print(f"\n{Color.BOLD}{Color.BLUE}--- 📊 결과 발표 ---{Color.END}")
            print(f"▶ 맞힌 문항 수: {Color.CYAN}{correct_count} / {len(self.quizzes)}{Color.END} 문제")
            print(f"▶ 최종 획득 점수: {Color.BOLD}{Color.CYAN}{score}점{Color.END}")
            
            # 최고 점수 갱신 로직
            if score > self.best_score:
                print(f"\n{Color.BOLD}{Color.PURPLE}🎊 축하합니다! 최고 점수 경신! 🎊{Color.END}")
                print(f"{Color.YELLOW}(기존: {self.best_score}점 {Color.END} -> {Color.BOLD}{Color.GREEN}새로운 최고 점수: {score}점!){Color.END}")
                self.best_score = score
                self.save_data()

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Color.RED}[!] 퀴즈가 중단되었습니다. 메인 메뉴로 돌아갑니다.{Color.END}")

    def add_quiz(self):
        """퀴즈 추가"""
        print(f"\n{Color.BOLD}{Color.BLUE}--- ✨ 새로운 퀴즈 데이터 등록 ---{Color.END}")
        try:
            while True:
                question = input(f"{Color.YELLOW}질문을 입력하세요: {Color.END}").strip()
                if question: break
                print(f"{Color.RED}[!] 질문은 비어있을 수 없습니다.{Color.END}")

            choices = []
            for i in range(1, 5):
                while True:
                    choice = input(f"선택지 {i}를 입력하세요: ").strip()
                    if choice:
                        choices.append(choice)
                        break
                    print(f"{Color.RED}[!] 비어있을 수 없습니다.{Color.END}")

            while True:
                # 정답 번호 유도
                answer_input = input(f"{Color.BOLD}정답 번호를 입력하세요 (1~4): {Color.END}").strip()
                try:
                    answer = int(answer_input)
                    if 1 <= answer <= 4: break
                    print(f"{Color.RED}[!] 1~4 사이의 숫자만 입력 가능합니다.{Color.END}")
                except ValueError:
                    print(f"{Color.RED}[!] 숫자로만 입력해주세요.{Color.END}")

            self.quizzes.append(Quiz(question, choices, answer))
            
            # 성공 메시지: 확실한 초록색(GREEN)으로 완료 표시
            print(f"\n{Color.BOLD}{Color.GREEN}✅ 퀴즈가 성공적으로 추가되었습니다!{Color.END}")
            print(f"{Color.BLUE}----------------------------{Color.END}")
            
            self.save_data() # 추가 시 자동 저장

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] 추가가 중단되었습니다.")

    def show_list(self):
        """퀴즈 목록 출력"""
        print(f"\n{Color.BOLD}{Color.PURPLE}------------------- 📚 등록된 퀴즈 목록 -------------------{Color.END}")
        if not self.quizzes:
            print(f"{Color.YELLOW}현재 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해 주세요!{Color.END}")
            return
        for i, quiz in enumerate(self.quizzes, 1):
            q_summary = quiz.question[:30] + "..." if len(quiz.question) > 30 else quiz.question
           # [Hotfix] 정답 노출 제거
            print(f"{Color.CYAN}{i:2d}.{Color.END} {q_summary}")
        print(f"{Color.PURPLE}-----------------------------------------------------------{Color.END}")

    def show_score(self):
        """최고 점수 출력"""
        # 제목: 굵은 노란색으로 황금빛 트로피 느낌 강조
        print(f"\n{Color.BOLD}{Color.BLUE}-------- 🏆 최고 점수 확인 🏆 --------{Color.END}")
        
        if self.best_score > 0:
            # 점수 부분만 하늘색(Cyan)으로 강조하여 눈에 띄게 함
            print(f"현재 최고 점수는 {Color.BOLD}{Color.CYAN}{self.best_score}점{Color.END} 입니다!")
            print(f"{Color.CYAN}대단해요! 기록을 더 경신해 보세요! 🔥{Color.END}")
        else:
            # 기록이 없을 때는 부드러운 흰색(기본) 혹은 안내 느낌의 노란색
            print(f"{Color.BLUE}아직 기록된 점수가 없습니다.{Color.END}")
            print("첫 퀴즈에 도전해서 1등이 되어보세요! 🏃‍♂️")
            
        print(f"{Color.BLUE}--------------------------------------{Color.END}")

    # --- 메인 메뉴 실행 흐름 ---
    
    def run(self):
        """프로그램의 메인 루프를 실행합니다."""
        while True:
            print(f"\n{Color.BOLD}{Color.YELLOW}" + "="*30)
            print("💡 나만의 퀴즈 게임 💡")
            print("="*30 + f"{Color.END}")
            
            print(f"{Color.CYAN}1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 최고 점수 확인")
            print(f"{Color.RED}5. 종료{Color.END}")
            print(f"{Color.YELLOW}" + "="*30 + f"{Color.END}")
            
            try:
                choice = input(f"{Color.BOLD}원하시는 메뉴의 번호를 입력하세요: {Color.END}").strip()
                
                if choice == '1':
                    self.play()
                elif choice == '2':
                    self.add_quiz()
                elif choice == '3':
                    self.show_list()
                elif choice == '4':
                    self.show_score()
                elif choice == '5':
                    print(f"\n{Color.GREEN}게임을 종료합니다. 이용해 주셔서 감사합니다! 👋{Color.END}")
                    break
                else:
                    print(f"{Color.RED}[!] 1번부터 5번 사이의 숫자를 입력해주세요.{Color.END}")
            
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{Color.RED}[!] 비정상 종료가 감지되었습니다. 데이터를 저장하고 안전하게 종료합니다.{Color.END}")
                break

# 프로그램 실행 진입점
if __name__ == "__main__":
    game = QuizGame()
    game.run()