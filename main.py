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

def solve_quiz(quiz_list):
    """
    저장된 퀴즈를 출제하고, 정답 수 기반으로 계산된 최종 점수를 반환하는 함수
    """
    if not quiz_list:
        print("\n[!] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
        return 0

    correct_count = 0
    points_per_question = 10  # 문제당 점수
    
    print(f"\n--- 퀴즈를 시작합니다! (총 {len(quiz_list)}문제, 문제당 {points_per_question}점) ---")

    try:
        for i, quiz in enumerate(quiz_list, 1):
            while True:
                quiz.display(i)
                user_input = input("정답 번호를 입력하세요 (1~4): ").strip()

                # 1. 빈 입력 처리
                if not user_input:
                    print("[!] 입력이 비어 있습니다. 다시 입력해주세요.")
                    continue

                # 2. 숫자 변환 및 범위 확인
                try:
                    choice = int(user_input)
                    if not (1 <= choice <= 4):
                        print("[!] 1에서 4 사이의 숫자만 입력 가능합니다.")
                        continue
                except ValueError:
                    print("[!] 숫자로만 입력해주세요 (예: 1).")
                    continue

                # 정답 확인
                if quiz.is_correct(choice):
                    print("=> 정답입니다! ✨")
                    correct_count += 1
                else:
                    print(f"=> 오답입니다. (정답: {quiz.answer}) 😢")
                break

        # 최종 점수 계산 및 출력
        score = correct_count * points_per_question
        print(f"\n--- 결과 발표 ---")
        print(f"총 {len(quiz_list)}문제 중 {correct_count}문제를 맞히셨습니다!")
        print(f"최종 획득 점수: {score}점")
        return score

    except (KeyboardInterrupt, EOFError):
        # 비정상 종료 시에도 현재까지의 점수 계산 후 안전하게 반환
        score = correct_count * points_per_question
        print("\n\n[!] 퀴즈 진행이 중단되었습니다. 메뉴로 돌아갑니다.")
        print(f"중단 전까지 맞힌 문제: {correct_count}개 / 획득 점수: {score}점")
        return score

# 실행 예시 (테스트용)
current_score = solve_quiz(initial_quizzes)