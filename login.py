from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from main import Face_Recognition_System, new_print


class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#031F3C")  # Toàn bộ nền màu xanh

        # ============= Biến lưu trữ thông tin đăng nhập ============
        self.var_email = StringVar()
        self.var_password = StringVar()

        # ============ Frame chứa phần đăng nhập ============
        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        login_frame.place(x=400, y=150, width=550, height=400)

        title = Label(login_frame, text="Đăng nhập", font=("times new roman", 25, "bold"), bg="white", fg="#031F3C")
        title.place(x=180, y=30)

        # ============ Email ============
        email_lbl = Label(login_frame, text="Email", font=("times new roman", 16, "bold"), bg="white", fg="gray")
        email_lbl.place(x=50, y=100)
        self.txtuser = ttk.Entry(login_frame, textvariable=self.var_email, font=("times new roman", 14))
        self.txtuser.place(x=50, y=130, width=450, height=35)

        # ============ Mật khẩu ============
        pass_lbl = Label(login_frame, text="Mật khẩu", font=("times new roman", 16, "bold"), bg="white", fg="gray")
        pass_lbl.place(x=50, y=180)
        self.txtpass = ttk.Entry(login_frame, textvariable=self.var_password, font=("times new roman", 14), show="*")
        self.txtpass.place(x=50, y=210, width=450, height=35)

        # ============ Checkbutton Admin ============
        self.varcheck = IntVar()
        checkbtn = Checkbutton(login_frame, variable=self.varcheck, text="Đăng nhập bằng Admin",
                               font=("times new roman", 12), bg="white")
        checkbtn.place(x=50, y=260)

        # ============ Nút Đăng nhập ============
        btn_login = Button(login_frame, text="Đăng nhập", command=self.login, font=("times new roman", 16, "bold"),
                           fg="white", bg="#B00857", cursor="hand2")
        btn_login.place(x=150, y=320, width=250, height=40)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()

        if self.varcheck.get() == 1:
            my_cursor.execute("SELECT * FROM admin WHERE Account=%s AND Password=%s",
                              (self.var_email.get(), self.var_password.get()))
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")
            else:
                new_print(str(0))
                messagebox.showinfo("Thông báo", "Đăng nhập Admin thành công")
                self.new_window = Toplevel(self.root)
                self.app = Face_Recognition_System(self.new_window)
        else:
            my_cursor.execute("SELECT Teacher_id FROM teacher WHERE Email=%s AND Password=%s",
                              (self.var_email.get(), self.var_password.get()))
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")
            else:
                new_print(str(row[0]))
                self.new_window = Toplevel(self.root)
                self.app = Face_Recognition_System(self.new_window)

        conn.commit()
        conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = Login_Window(root)
    root.mainloop()