import datetime
import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# 初始化用户数据文件
USER_DATA_FILE = "user_data.json"

# 加载用户数据
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# 保存用户数据
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 生成随机题目
def generate_question(question_type):
    if question_type == "division":
        divisor = random.randint(1, 9)
        dividend = random.randint(10, 99)
        return f"{dividend} ÷ {divisor}", dividend // divisor
    elif question_type == "multiplication":
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        return f"{num1} × {num2}", num1 * num2

# 更新用户信息
def update_user_info(username, test_type, score, questions, errors):
    user_data = load_user_data()
    if username not in user_data:
        user_data[username] = {
            "tests": []
        }

    # 记录本次测验信息
    user_data[username]["tests"].append({
        "type": test_type,
        "score": score,
        "questions": questions,
        "errors": errors,
        "timestamp": str(datetime.datetime.now())
    })

    # 只保留最近3次测验记录
    user_data[username]["tests"] = user_data[username]["tests"][-3:]

    save_user_data(user_data)

# 主应用类
class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("小学生数学练习工具")

        # 用户数据
        self.user_data = load_user_data()
        self.current_username = None
        self.questions = []
        self.answers = []
        self.scores = []
        self.current_question_index = 0
        self.test_type = None

        # 创建界面
        self.create_widgets()

    def create_widgets(self):
        # 用户名输入框
        self.username_label = tk.Label(self.root, text="请输入用户名:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.save_username_button = tk.Button(self.root, text="保存用户名", command=self.save_username)
        self.save_username_button.pack(pady=5)

        # 题目类型选择
        self.question_type_label = tk.Label(self.root, text="请选择题目类型:")
        self.question_type_label.pack(pady=5)

        self.division_button = tk.Button(self.root, text="除数是一位数的除法", command=lambda: self.start_quiz("division"))
        self.division_button.pack(pady=5)

        self.multiplication_button = tk.Button(self.root, text="两位数乘两位数", command=lambda: self.start_quiz("multiplication"))
        self.multiplication_button.pack(pady=5)

        # 答题区域
        self.question_label = tk.Label(self.root, text="")
        self.question_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.root)
        self.answer_entry.pack(pady=5)

        self.confirm_button = tk.Button(self.root, text="确认", command=self.check_answer)
        self.confirm_button.pack(pady=5)

        self.prev_button = tk.Button(self.root, text="上一题", command=self.prev_question)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="下一题", command=self.next_question)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.end_test_button = tk.Button(self.root, text="结束测验", command=self.end_test)
        self.end_test_button.pack(pady=10)

        # 测验结果显示
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

    def save_username(self):
        username = self.username_entry.get()
        if username.strip() == "":
            messagebox.showerror("错误", "用户名不能为空！")
            return

        self.current_username = username
        if self.current_username not in self.user_data:
            self.user_data[self.current_username] = {"tests": []}
            save_user_data(self.user_data)

        messagebox.showinfo("成功", f"用户名已保存为: {self.current_username}")

    def start_quiz(self, test_type):
        if self.current_username is None:
            messagebox.showerror("错误", "请先输入并保存用户名！")
            return

        self.test_type = test_type
        self.questions = [generate_question(test_type) for _ in range(10)]
        self.answers = [None] * len(self.questions)
        self.scores = [10] * len(self.questions)
        self.current_question_index = 0

        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            question_text, _ = self.questions[self.current_question_index]
            self.question_label.config(text=f"第 {self.current_question_index + 1} 题: {question_text}")
            self.answer_entry.delete(0, tk.END)
        else:
            self.end_test()

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字答案！")
            return

        _, correct_answer = self.questions[self.current_question_index]

        if user_answer == correct_answer:
            messagebox.showinfo("正确", "回答正确！")
            self.answers[self.current_question_index] = user_answer
            self.show_question()
        else:
            self.scores[self.current_question_index] -= 2
            if self.scores[self.current_question_index] <= 0:
                self.scores[self.current_question_index] = 0
                messagebox.showinfo("错误", f"回答错误，正确答案是: {correct_answer}")
                self.answers[self.current_question_index] = None
                self.show_question()
            else:
                messagebox.showinfo("错误", f"回答错误，请再试一次！当前分数: {self.scores[self.current_question_index]}")

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()

    def end_test(self):
        total_score = sum(score for score in self.scores if score > 0)
        total_questions = len(self.questions)
        total_errors = sum(1 for answer in self.answers if answer is None)

        messagebox.showinfo("测验结束", f"本次测验结束！\n答对题数: {total_questions - total_errors}\n答错题数: {total_errors}\n总得分: {total_score}\n平均分: {total_score / total_questions:.2f}")

        # 更新用户数据
        update_user_info(self.current_username, self.test_type, total_score, total_questions, total_errors)

        # 清空答题状态
        self.questions = []
        self.answers = []
        self.scores = []
        self.current_question_index = 0
        self.question_label.config(text="")
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()
