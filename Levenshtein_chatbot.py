# 레벤슈타인 거리 구하기를 이용한 챗봇
import pandas as pd

def calc_distance(a, b):
    ''' 레벤슈타인 거리 계산하기 '''
    if a == b: return 0 # 같으면 0을 반환
    a_len = len(a) # a 길이
    b_len = len(b) # b 길이
    if a == "": return b_len
    if b == "": return a_len
    # 2차원 표 (a_len+1, b_len+1) 준비하기 --- (※1)
    # matrix 초기화의 예 : [[0, 1, 2, 3], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0]]
    # [0, 1, 2, 3]
    # [1, 0, 0, 0]
    # [2, 0, 0, 0]
    # [3, 0, 0, 0] 
    matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
    for i in range(a_len+1): # 0으로 초기화
        matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
    # 0일 때 초깃값을 설정
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    # 표 채우기 --- (※2)
    # print(matrix,'----------')
    for i in range(1, a_len+1):
        ac = a[i-1]
        # print(ac,'=============')
        for j in range(1, b_len+1):
            bc = b[j-1] 
            # print(bc)
            cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
            matrix[i][j] = min([
                matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
            ])
            # print(matrix)
        # print(matrix,'----------끝')
    return matrix[a_len][b_len]
    
class LevenshteinChatBot:    
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        best_point = 100        # 초기값이 높게 셋팅한다.(낫을수록 정확도가 높다)
        best_point_index = 0    # 가장 점수가 낮은 index를 0으로 초기화 한다.
        index = 0               # 초기값 
        
        for ques in self.questions:  # 질문열의 수 만큼 반복
            point = calc_distance(input_sentence, ques)  # 입력값과 질문의 레벤슈타인 거리를 계산한다.
            #print('best_point : ', best_point, ', point : ', point, 'index : ', index,'[', ques, ']', input_sentence)
            if point == 0: # 점수가 0 이면 현재 index의 답변을 선택하고 중단한다.
                best_point_index = index
                break
            elif point < best_point: # 기존 가장 좋은 점수와 비교하여 더 좋으면 값을 변경한다.
                best_point = point
                best_point_index = index
                
            index += 1 # 현재 index를 증가한다.
        
        #print('best_point_index : ', best_point_index)
        return self.answers[best_point_index]

# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = LevenshteinChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
