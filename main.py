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

def add_quiz(quiz_list):
    """
    사용자로부터 입력을 받아 새로운 퀴즈를 목록에 추가하고 파일에 저장하는 함수
    """
    print("\n--- 새로운 퀴즈 추가 ---")
    
    try:
        # 1. 문제 입력 (이전 코드 동일)
        while True:
            question = input("질문을 입력하세요: ").strip()
            if not question:
                print("[!] 질문은 비어있을 수 없습니다.")
                continue
            break

        # 2. 선택지 입력 (4개)
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}를 입력하세요: ").strip()
                if not choice:
                    print(f"[!] 선택지 {i}은(는) 비어있을 수 없습니다.")
                    continue
                choices.append(choice)
                break

        # 3. 정답 번호 입력
        while True:
            answer_input = input("정답 번호를 입력하세요 (1~4): ").strip()
            if not answer_input:
                print("[!] 정답 번호를 입력해야 합니다.")
                continue
            
            try:
                answer = int(answer_input)
                if not (1 <= answer <= 4):
                    print("[!] 1에서 4 사이의 숫자만 입력 가능합니다.")
                    continue
            except ValueError:
                print("[!] 숫자로만 입력해주세요 (예: 1).")
                continue
            break

        # 4. Quiz 객체 생성 및 목록 추가
        new_quiz = Quiz(question, choices, answer)
        quiz_list.append(new_quiz)
        
        # 5. [Hotfix] 파일에 즉시 저장
        # 현재는 best_score 로직 전이므로 기본값 0 전달
        save_to_file(quiz_list)
        
        print("\n=> 퀴즈가 성공적으로 추가되었으며 state.json에 저장되었습니다! ✅")
        return quiz_list

    except (KeyboardInterrupt, EOFError):
        print("\n\n[!] 퀴즈 추가가 중단되었습니다. 메뉴로 돌아갑니다.")
        return quiz_list


def show_quizzes(quiz_list):
    """
    현재 등록된 모든 퀴즈의 목록을 출력하는 함수
    """
    print("\n--- 등록된 퀴즈 목록 ---")
    
    if not quiz_list:
        print("[!] 현재 등록된 퀴즈가 없습니다. 새로운 퀴즈를 추가해보세요!")
        return

    print(f"총 {len(quiz_list)}개의 퀴즈가 있습니다.\n")
    
    for i, quiz in enumerate(quiz_list, 1):
        print(f"{i}. 질문: {question_summary(quiz.question)}")
        # 선택지도 간략하게 보여주고 싶다면 아래 주석을 해제하세요.
        # for j, choice in enumerate(quiz.choices, 1):
        #     print(f"   ({j}) {choice}")
        print(f"   (정답: {quiz.answer}번)")
    
    print("\n------------------------")

def question_summary(question, length=30):
    """질문이 너무 길 경우 말줄임표 처리 (가독성용)"""
    if len(question) > length:
        return question[:length] + "..."
    return question


def save_to_file(quiz_list, best_score=0):
    """
    퀴즈 목록과 최고 점수를 state.json 파일에 저장하는 함수
    """
    file_path = "state.json"
    
    # Quiz 객체들을 저장 가능한 딕셔너리 리스트로 변환
    quiz_data = []
    for q in quiz_list:
        quiz_data.append({
            "question": q.question,
            "choices": q.choices,
            "answer": q.answer
        })
    
    # 전체 데이터 구조 생성
    state = {
        "quizzes": quiz_data,
        "best_score": best_score
    }
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[!] 파일 저장 중 오류가 발생했습니다: {e}")

def show_best_score(best_score):
    """
    현재까지의 최고 점수를 출력하는 함수
    """
    print("\n--- 🏆 최고 점수 확인 🏆 ---")
    if best_score > 0:
        print(f"현재 최고 점수는 {best_score}점 입니다!")
        print("계속해서 기록을 경신해 보세요!")
    else:
        print("아직 기록된 점수가 없습니다. 첫 퀴즈에 도전해 보세요!")
    print("----------------------------")

def check_and_update_best_score(current_score, best_score, quiz_list):
    """
    방금 획득한 점수가 최고 점수인지 확인하고, 
    최고 점수라면 갱신 후 파일에 저장하는 함수
    """
    if current_score > best_score:
        print(f"\n🎉 축하합니다! 최고 점수를 경신했습니다! (기존: {best_score}점 -> 새로운 최고 점수: {current_score}점) 🎉")
        new_best_score = current_score
        
        # 앞서 만든 save_to_file 함수를 재사용하여 파일 업데이트
        save_to_file(quiz_list, new_best_score)
        return new_best_score
    
    return best_score

# 실행 예시 (테스트용)
current_score = solve_quiz(initial_quizzes)