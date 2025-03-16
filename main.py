import os
import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk, messagebox
import PIL.Image
from time import strftime
import mysql.connector

from attendance import Attendance
from face_recognition import Face_Recognition
from lesson import Lesson
from report_attendance import Report
from student_upd import Student
from subject import Subject
from teacher import Teacher

value_from_p1 = None


def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value_from_p1)


class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống điểm danh bằng nhận diện khuôn mặt")
        today = strftime("%d-%m-%Y")

        # Background
        img3 = PIL.Image.open(
            r"C:\Users\PHAM HAO\PycharmProjects\PythonProject6\ImageFaceDetect\Trường Đại Học Mỏ Địa Chất.png")
        img3 = img3.resize((1530, 790), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1530, height=790)

        # Lấy thông tin tài khoản
        self.account = "Admin" if value_from_p1 == "0" or value_from_p1 is None else self.get_teacher_email(
            value_from_p1)

        # Tiêu đề
        self.txt = "Điểm danh bằng nhận diện khuôn mặt"
        self.heading = Label(self.root, text=self.txt, font=("yu gothic ui", 26, "bold"), bg="white", fg="black", bd=5,
                             relief=FLAT)
        self.heading.place(x=280, y=22, width=650)

        # Hiển thị email
        self.lblemail = Label(self.root, text=self.account, font=("yu gothic ui", 12, "bold"), bg="white", fg="green")
        self.lblemail.place(x=1000, y=48, width=150, height=22)

        # Đăng xuất
        b1 = Button(self.root, text="Đăng xuất", cursor="hand2", command=self.exit,
                    font=("times new roman", 13, "bold"), bg="white", fg="black", borderwidth=0)
        b1.place(x=1380, y=48, width=100, height=27)

        # Nếu là giáo viên thì hiển thị nút đổi mật khẩu
        if value_from_p1 != "0" and value_from_p1 is not None:
            change_pass = Button(self.root, text="Đổi mật khẩu", cursor="hand2", command=self.change_pass,
                                 font=("times new roman", 13, "bold"), bg="white", fg="black", borderwidth=0)
            change_pass.place(x=1220, y=48, width=100, height=27)

        # Các nút chức năng
        self.create_buttons()

    def get_teacher_email(self, teacher_id):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT Email FROM teacher WHERE Teacher_id=%s", (teacher_id,))
        row = my_cursor.fetchone()
        conn.close()
        return row[0] if row else "Unknown"

    def create_buttons(self):
        if value_from_p1 == "0" or value_from_p1 is None:
            buttons = [
                ("Sinh viên", "student.png", self.student_details),
                ("Giáo viên", "teacher.png", self.teacher_data),
                ("Thống kê", "report.png", self.report_data),
                ("Nhận diện", "nhandien.png", self.face_recognition),
                ("Điểm danh", "ghichu.png", self.attendance_data),
                ("Môn học", "book.png", self.subject_data),
                ("Buổi học", "lesson.png", self.lesson_data),
                ("Xem ảnh", "picture.png", self.open_img)
            ]
            columns = 4
        else:
            buttons = [
                ("Thống kê", "report.png", self.report_data),
                ("Nhận diện", "nhandien.png", self.face_recognition),
                ("Điểm danh", "ghichu.png", self.attendance_data),
                ("Môn học", "book.png", self.subject_data),
                ("Buổi học", "lesson.png", self.lesson_data),
                ("Xem ảnh", "picture.png", self.open_img)
            ]
            columns = 3

        x_positions = [300, 600, 900, 1200][:columns]
        y_positions = [200, 450]

        for i, (text, img, command) in enumerate(buttons):
            img_btn = PIL.Image.open(f"ImageFaceDetect/{img}")
            img_btn = img_btn.resize((80, 113), PIL.Image.ANTIALIAS)
            photo_btn = ImageTk.PhotoImage(img_btn)
            button = Button(self.root, text=text, font=("yu gothic ui", 16, "bold"), image=photo_btn, command=command,
                            cursor="hand2", activebackground="white", bg="white", borderwidth=0, compound="top")
            button.image = photo_btn  # Giữ tham chiếu tránh lỗi
            button.place(x=x_positions[i % columns], y=y_positions[i // columns], width=180, height=180)

    def exit(self):
        Exit = messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", parent=self.root)
        if Exit:
            self.root.destroy()

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def report_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Report(self.new_window)

    def face_recognition(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def subject_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Subject(self.new_window)

    def teacher_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Teacher(self.new_window)

    def lesson_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Lesson(self.new_window)

    def open_img(self):
        os.startfile("data")

    def change_pass(self):
        messagebox.showinfo("Thông báo", "Chức năng đổi mật khẩu đang phát triển", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()