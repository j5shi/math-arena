import datetime
import json
import os
import random
import tkinter as tk
from enum import Enum
from tkinter import messagebox

# 用户数据文件
USER_DATA_FILE = "./user_data.json"


# 加载用户数据
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                return json.loads(content)
            else:
                return {}
    return {}


# 保存用户数据
def save_user_data(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# 生成随机题目
def generate_question(question_type):
    if question_type == QuestionType.ADDITION_LEVEL_1.value:
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        return f"{num1} + {num2}", num1 + num2

    elif question_type == QuestionType.ADDITION_LEVEL_2.value:
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        return f"{num1} + {num2}", num1 + num2

    elif question_type == QuestionType.SUBTRACTION_LEVEL_1.value:
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 9)
        return f"{num1} - {num2}", num1 - num2

    elif question_type == QuestionType.SUBTRACTION_LEVEL_2.value:
        while True:
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
            if num1 > num2:
                return f"{num1} - {num2}", num1 - num2

    elif question_type == QuestionType.DIVISION_LEVEL_1.value:
        while True:
            divisor = random.randint(1, 9)
            dividend = random.randint(2, 99)
            if dividend % divisor == 0:
                return f"{dividend} ÷ {divisor}", dividend // divisor

    elif question_type == QuestionType.DIVISION_LEVEL_2.value:
        while True:
            divisor = random.randint(1, 9)
            dividend = random.randint(2, 99)
            if dividend % divisor != 0:
                return f"{dividend} ÷ {divisor}", dividend // divisor

    elif question_type == QuestionType.MULTIPLICATION_LEVEL_1.value:
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 9)
        return f"{num1} × {num2}", num1 * num2

    elif question_type == QuestionType.MULTIPLICATION_LEVEL_2.value:
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        return f"{num1} × {num2}", num1 * num2

    else:
        raise ValueError(f"Invalid question type: {question_type}")


# 更新用户信息
def update_user_info(username, user_data, test_type, score, questions, corrects, errors):
    if username not in user_data:
        user_data[username] = {
            "tests": []
        }

    # 记录本次测验信息
    user_data[username]["tests"].append({
        "type": test_type,
        "score": score,
        "questions": questions,
        "corrects": corrects,
        "errors": errors,
        "timestamp": str(datetime.datetime.now())
    })

    # 只保留最近3次测验记录
    user_data[username]["tests"] = user_data[username]["tests"][-3:]

    save_user_data(user_data)


class QuestionType(Enum):
    ADDITION_LEVEL_1 = "两位数加法"
    ADDITION_LEVEL_2 = "三位数加法"
    SUBTRACTION_LEVEL_1 = "两位数减一位数"
    SUBTRACTION_LEVEL_2 = "两位数减两位数"
    DIVISION_LEVEL_1 = "两位数除一位数的整除法"
    DIVISION_LEVEL_2 = "两位数除一位数的非整除法"
    MULTIPLICATION_LEVEL_1 = "两位数乘一位数"
    MULTIPLICATION_LEVEL_2 = "两位数乘两位数"


# 主应用类
class MathQuizApp:

    def __init__(self, tkinter):
        self.root = tkinter

        # 用户数据
        self.user_data = load_user_data()
        self.current_username = None
        self.questions = []
        self.answers = []
        self.scores = []
        self.current_question_index = 0
        self.test_type = None

        # 默认使用第一个用户
        if len(self.user_data):
            self.current_username = list(self.user_data.keys())[0]

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        self.root.title("小学生数学强化练习工具")

        # 可以更改背景颜色
        self.background_color = None
        self.root.configure(bg=self.background_color)

        # 设置窗口大小为
        window_width = 600
        window_height = 450

        # 获取屏幕的宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算窗口左上角的坐标，使其居中
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # 设置窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建一个框架来放置用户名标签和输入框
        self.username_frame = tk.Frame(self.root)
        self.username_frame.pack(padx=5, pady=5)

        # 用户名标签
        self.username_label = tk.Label(self.username_frame, text="请输入姓名:")
        self.username_label.pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)

        # 用户名输入框
        self.username_entry = tk.Entry(self.username_frame)
        if self.current_username:
            self.username_entry.insert(0, self.current_username)
        self.username_entry.pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)

        self.save_username_button = tk.Button(self.username_frame,
                                              text="保存或修改姓名",
                                              command=self.save_username)
        self.save_username_button.pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)

        # 题目类型选择按钮宽度
        question_button_width = 20

        # 题目类型选择标签
        self.question_type_label = tk.Label(self.root, text="请选择题目类型:")
        self.question_type_label.pack(pady=5)

        # 创建一个框架来放置题目按钮
        self.questions_frame1 = tk.Frame(self.root)
        self.questions_frame1.pack(padx=5, pady=5)

        self.divisible_button = tk.Button(self.questions_frame1,
                                          text=QuestionType.ADDITION_LEVEL_1.value,
                                          command=lambda: self.start_quiz(QuestionType.ADDITION_LEVEL_1.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.LEFT, pady=5)

        self.divisible_button = tk.Button(self.questions_frame1,
                                          text=QuestionType.ADDITION_LEVEL_2.value,
                                          command=lambda: self.start_quiz(QuestionType.ADDITION_LEVEL_2.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.RIGHT, pady=5)

        # 创建一个框架来放置题目按钮
        self.questions_frame2 = tk.Frame(self.root)
        self.questions_frame2.pack(padx=5, pady=5)

        self.divisible_button = tk.Button(self.questions_frame2,
                                          text=QuestionType.SUBTRACTION_LEVEL_1.value,
                                          command=lambda: self.start_quiz(QuestionType.SUBTRACTION_LEVEL_1.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.LEFT, pady=5)

        self.divisible_button = tk.Button(self.questions_frame2,
                                          text=QuestionType.SUBTRACTION_LEVEL_2.value,
                                          command=lambda: self.start_quiz(QuestionType.SUBTRACTION_LEVEL_2.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.RIGHT, pady=5)

        # 创建一个框架来放置题目按钮
        self.questions_frame3 = tk.Frame(self.root)
        self.questions_frame3.pack(padx=5, pady=5)

        self.divisible_button = tk.Button(self.questions_frame3,
                                          text=QuestionType.DIVISION_LEVEL_1.value,
                                          command=lambda: self.start_quiz(QuestionType.DIVISION_LEVEL_1.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.LEFT, pady=5)

        self.divisible_button = tk.Button(self.questions_frame3,
                                          text=QuestionType.DIVISION_LEVEL_2.value,
                                          command=lambda: self.start_quiz(QuestionType.DIVISION_LEVEL_2.value),
                                          width=question_button_width)
        self.divisible_button.pack(side=tk.RIGHT, pady=5)

        # 创建一个框架来放置题目按钮
        self.questions_frame4 = tk.Frame(self.root)
        self.questions_frame4.pack(padx=5, pady=5)

        self.multiplication_button = tk.Button(self.questions_frame4,
                                               text=QuestionType.MULTIPLICATION_LEVEL_1.value,
                                               command=lambda: self.start_quiz(QuestionType.MULTIPLICATION_LEVEL_1.value),
                                               width=question_button_width)
        self.multiplication_button.pack(side=tk.LEFT, pady=5)

        self.multiplication_button = tk.Button(self.questions_frame4,
                                               text=QuestionType.MULTIPLICATION_LEVEL_2.value,
                                               command=lambda: self.start_quiz(QuestionType.MULTIPLICATION_LEVEL_2.value),
                                               width=question_button_width)
        self.multiplication_button.pack(side=tk.RIGHT, pady=5)

        # 答题区域
        self.answer_frame = tk.Frame(self.root)
        self.answer_frame.pack(padx=5, pady=25)

        self.question_label = tk.Label(self.answer_frame, text="请输入答案: ")
        self.question_label.pack(padx=5, side=tk.LEFT, expand=True, anchor=tk.CENTER)

        self.answer_entry = tk.Entry(self.answer_frame)
        self.answer_entry.pack(padx=5, side=tk.LEFT, expand=True, anchor=tk.CENTER)

        self.confirm_button = tk.Button(self.answer_frame,
                                        text="确认",
                                        command=self.check_answer)
        self.confirm_button.pack(padx=5, side=tk.RIGHT, expand=True, anchor=tk.CENTER)

        # 题目切换区域
        self.question_switch_frame = tk.Frame(self.root)
        self.question_switch_frame.pack(padx=5, pady=30)

        self.prev_button = tk.Button(self.question_switch_frame,
                                     text="上一题",
                                     command=self.prev_question,
                                     bg=self.background_color)
        self.prev_button.pack(side=tk.LEFT, padx=20, pady=5)

        self.next_button = tk.Button(self.question_switch_frame,
                                     text="下一题",
                                     command=self.next_question,
                                     bg=self.background_color)
        self.next_button.pack(side=tk.RIGHT, padx=20, pady=5)

        self.end_test_button = tk.Button(self.question_switch_frame,
                                         text="结束测验",
                                         command=self.end_test,
                                         bg=self.background_color)
        self.end_test_button.pack(side=tk.BOTTOM, padx=10, pady=5)

        # 测验结果显示
        self.result_label = tk.Label(self.root, text="", bg=self.background_color)
        self.result_label.pack(pady=10)

    def save_username(self):
        username = self.username_entry.get()
        if username.strip() == "":
            messagebox.showerror("错误", "姓名不能为空！")
            self.root.focus_force()
            return

        self.current_username = username
        if self.current_username not in self.user_data:
            self.user_data[self.current_username] = {"tests": []}
            save_user_data(self.user_data)

        messagebox.showinfo("成功", f"姓名已保存: {self.current_username}")
        self.root.focus_force()

    def start_quiz(self, test_type):
        if self.current_username is None:
            messagebox.showerror("错误", "请先输入并保存姓名！")
            self.root.focus_force()
            return

        self.test_type = test_type
        self.questions = [generate_question(test_type) for _ in range(10)]
        self.answers = [None] * len(self.questions)
        self.scores = [10] * len(self.questions)
        self.current_question_index = 0

        self.show_question()

    def show_question(self):
        self.root.focus_force()

        if self.current_question_index < len(self.questions):
            question_text, _ = self.questions[self.current_question_index]
            self.question_label.config(text=f"第 {self.current_question_index + 1} 题: {question_text} =")
            self.answer_entry.delete(0, tk.END)
        else:
            self.end_test()

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字答案！")
            self.root.focus_force()
            return

        _, correct_answer = self.questions[self.current_question_index]

        if user_answer == correct_answer:
            messagebox.showinfo("正确", "回答正确！")
            self.answers[self.current_question_index] = user_answer
            # 显示下一题
            self.next_question()
        else:
            self.scores[self.current_question_index] -= 4
            if self.scores[self.current_question_index] <= 0:
                self.scores[self.current_question_index] = 0
                messagebox.showinfo("错误", f"回答错误，正确答案是: {correct_answer}")
                self.answers[self.current_question_index] = ""  # "" 表示答错， None 表示没有回答
                self.next_question()

            else:
                messagebox.showinfo("错误", f"回答错误，请再试一次！本题分数: {self.scores[self.current_question_index]}")
                self.root.focus_force()

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()

    def end_test(self):
        if not self.test_type:
            messagebox.showerror("错误", "请先开始测验！")
            self.root.focus_force()
            return

        total_questions = len(self.questions)
        total_correct_answers = 0
        total_errors = 0
        total_not_answered = 0
        total_score = 0
        for index, answer in enumerate(self.answers):
            if answer is None:
                total_not_answered += 1
                continue
            if answer == "":
                total_errors += 1
                continue
            if answer is not None and answer != "":
                total_correct_answers += 1
                total_score += self.scores[index]
                continue

        if total_questions - total_not_answered:
            total_score_avg = total_score / (total_questions - total_not_answered)
        else:
            total_score_avg = 0

        messagebox.showinfo(
            "测验结束",
            f"""本次测验结束！
                    总题数: {total_questions}
                    答对题数: {total_correct_answers}
                    答错题数: {total_errors}
                    未答题数: {total_not_answered}
                    总得分: {total_score}
                    平均分: {total_score_avg:.2f}"""
        )
        self.root.focus_force()

        # 更新用户数据
        update_user_info(self.current_username,
                         self.user_data,
                         self.test_type,
                         total_score,
                         total_questions,
                         total_correct_answers,
                         total_errors)

        # 清空答题状态
        self.questions = []
        self.answers = []
        self.scores = []
        self.current_question_index = 0
        self.question_label.config(text="")
        self.result_label.config(text="")
        self.answer_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
