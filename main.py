import os
import random
DEFAULT_QUESTIONS_PATH = "./interviews"

class Question:
    def __init__(self, category, que, ans):
        self.category = category
        self.que = que
        self.ans = ans

    def __repr__(self):
        return "{} ===========\n {}\n".format(self.que, self.ans)

class QuestionPool:
    def __init__(self, path):
        self.path = path
        self.questions = []
        self._read_questions(path)
        self.index = 0

    def _read_questions(self, path):
        # print("path",path)
        if os.path.isdir(path):
            childPaths = os.listdir(path)
            for p in childPaths:
                self._read_questions(os.path.join(path,p))
        if os.path.isfile(path):
            q = Question(None, None, None)
            with open(path, 'r') as f:
                for x in f:
                    if x.startswith('##'):
                        if q.que != None:
                            q.ans.strip('\n')
                            q.que.strip('\n')
                            self.questions.append(q)
                        q = Question(None, None, None)
                        q.category = path
                        q.que = x
                        q.ans = ""
                    else:
                        if x != "\n":
                            q.ans += x
                if q != None:
                    self.questions.append(q)
    def next_question(self):
        self.index = self.index + random.randint(1,3)
        if self.index >= len(self.questions):
            self.index = 0
        return self.questions[self.index]

class Answer:
    def __init__(self, question, score, remark):
        self.question = question
        self.score = score
        self.remark = remark

    def __repr__(self):
        return "{} \t得分：{} \n\t备注：{}\n".format(self.question.que, self.score, self.remark)

class Interview:
    def __init__(self, qp):
        self.qp = qp  # question pool
        self.ans = []
    
    def go(self):
        question = self.qp.next_question()
        print(question)
        score = self.ask_score()
        remark = input("请输入一些备注信息，按回车结束： ")
        self.ans.append(Answer(question, int(score), remark))
        self.next_step_guide()

    def ask_score(self):
        score = input("请输入候选人在此题上的得分，输入其他键跳过此题 (1-5)： ")
        if not score.isdigit():
            # 有堆栈溢出风险
            self.go()
        score = int(score)
        if score > 5 or score < 1:
            score = self.ask_score()
        return score

    def finish(self):
        num_ans = len(self.ans)
        sum_score = sum([a.score for a in self.ans])
        avg_score = sum_score / num_ans
        print("==================详细信息====================")
        print("候选人共回答 {} 题，总得分 {}，平均得分 {}".format(num_ans, sum_score, avg_score))
        for a in self.ans:
            print(a)

    def next_step_guide(self):
        next_step = input("回车继续，或输入 exit 退出")
        if next_step == '':
            self.go()
        elif next_step == "exit":
            self.finish()
        else:
            self.next_step_guide()
            
def main():
    qp = QuestionPool(DEFAULT_QUESTIONS_PATH)
    interview = Interview(qp)
    interview.go()

if __name__ == "__main__":
    main()
