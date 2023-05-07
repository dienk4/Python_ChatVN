from tkinter import *
from tkinter import messagebox
import socket
from PIL import ImageTk, Image
from PIL import Image as PILImage
import sqlite3
import json
import datetime
from tkinter import ttk
from tkinter import filedialog
import io
import threading
import speech_recognition as sr
import cv2
import PIL.ImageTk, PIL.Image
import webbrowser
import openai
import pyperclip
import base64
import pygame
import time
import os
from gtts import gTTS

class Login:
    def __init__(self, window):
        self.window = window

        self.name = None  # chưa có giá trị ban đầu
        self.image_path = None

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=50)

        # ========================================================
        self.txt = "Welcome to ChatVN"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=7,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=45)

        # ============ Left Side Image ===========================================
        self.side_image = Image.open('images\\vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ============ Image =============================================
        self.images = [('icon_user\\1.jpg', '\1'), ('icon_user\\2.jpg', '\2'), ('icon_user\\3.jpg', '\3'),
                       ('icon_user\\4.jpg', '\4'), ('icon_user\\5.jpg', '\5'), ('icon_user\\15.jpg', '\15'),
                       ('icon_user\\6.jpg', '\6'), ('icon_user\\7.jpg', '\7'), ('icon_user\\13.jpg', '\13'),
                       ('icon_user\\14.jpg', '\14'), ('icon_user\\10.jpg', '\10'), ('icon_user\\12.jpg', '\12'),
                       ('icon_user\\11.jpg', '\11'), ('icon_user\\16.jpg', '\16')
                       ]
        self.current_index = 0
        self.create_widgets()

        # ============ Sign In label =============================================
        self.sign_in_label = Label(self.lgn_frame, text="Đăng nhập", bg="#040405", fg="white",
                                   font=("yu gothic ui", 19, "bold"))
        self.sign_in_label.place(x=630, y=80)

        # ===================== Choose avatar =======================================
        self.username_label = Label(self.lgn_frame, text="Chọn ảnh đại diện", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=140)

        # ============================ Username ==============================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground='#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)
        self.username_entry.focus_set()

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images\\username_icon.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ============================ password ==================================================
        self.password_label = Label(self.lgn_frame, text="Mật khẩu", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)

        self.password_icon = Image.open('images\\password_icon.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=414)
        # ========= show/hide password =============
        self.img1 = Image.open('images\\eye_open.jpg')
        self.img1.thumbnail((25, 25), Image.LANCZOS)
        self.show_image = ImageTk.PhotoImage(self.img1)

        self.img2 = Image.open('images\\eye_close.jpg')
        self.img2.thumbnail((25, 25), Image.LANCZOS)
        self.hide_image = ImageTk.PhotoImage(self.img2)

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_image.image = self.hide_image
        self.show_button.place(x=860, y=420)

        # ============================login button================================
        self.lgn_button = Image.open('images\\btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.login)
        self.login.place(x=20, y=10)
        # ============================Forgot password=============================
        self.forgot_button = Button(self.lgn_frame, text="Quên mật khẩu ?",
                                    font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                                    activebackground="#040405"
                                    , borderwidth=0, background="#040405", cursor="hand2"
                                    , command=self.go_to_forget)
        self.forgot_button.place(x=630, y=510)
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='Bạn chưa có tài khoản ?', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=570, y=560)

        self.signup_img = ImageTk.PhotoImage(file='images\\register.png')
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#040405", activebackground="#040405",
                                          command=self.go_to_signup)
        self.signup_button_label.place(x=740, y=555, width=111, height=35)

    def create_widgets(self):
        self.icon_user = Label(self.lgn_frame)
        self.icon_user.place(x=645, y=190)
        self.previous_button = Button(self.lgn_frame, text="←", command=self.show_previous_image,
                                      font=("yu gothic ui", 17, "bold"),
                                      cursor="hand2", borderwidth=0, bg='black', fg='white')
        self.previous_button.place(x=605, y=220)

        self.next_button = Button(self.lgn_frame, text="→", command=self.show_next_image,
                                  font=("yu gothic ui", 17, "bold"),
                                  cursor="hand2", borderwidth=0, bg='black', fg='white')
        self.next_button.place(x=755, y=220)

        self.image_path, emoji_code = self.images[self.current_index]
        image = Image.open(f"{self.image_path}")
        image.thumbnail((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.icon_user.config(image=self.photo)
        self.icon_user.image = self.photo

    def show_previous_image(self):
        self.current_index = (self.current_index - 1) % len(self.images)
        self.image_path, emoji_code = self.images[self.current_index]
        image = Image.open(f"{self.image_path}")
        image.thumbnail((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.icon_user.config(image=self.photo)
        self.icon_user.image = self.photo

    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)

        self.image_path, emoji_code = self.images[self.current_index]
        image = Image.open(f"{self.image_path}")
        image.thumbnail((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.icon_user.config(image=self.photo)
        self.icon_user.image = self.photo

    def show_next_image(self):
        self.current_index = (self.current_index + 1) % len(self.images)

        self.image_path, emoji_code = self.images[self.current_index]
        image = Image.open(f"{self.image_path}")
        image.thumbnail((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        self.icon_user.config(image=self.photo)
        self.icon_user.image = self.photo

    def login(self):
        username_entry = self.username_entry.get()
        password_entry = self.password_entry.get()

        if password_entry == '' or username_entry == '':
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập đầy đủ thông tin')
        else:
            conn = sqlite3.connect('Data\\dangky.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dangky WHERE user = ? and pass = ?", (username_entry, password_entry))
            row = cursor.fetchall()
            if row:
                messagebox.showinfo('Thông báo - ChatVN', 'Đăng nhập thành công')
                self.name = username_entry
                conn.close()

                self.lgn_frame.destroy()
                self.bg_panel.destroy()
                Chat(self.window, self.name, self.image_path)
            else:
                messagebox.showerror('Lỗi - ChatVN', 'Thông tin vừa nhập chưa đúng')

    def go_to_signup(self):
        Signup(self.window)

    def go_to_forget(self):
        Forget(self.window)

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.hide_image, command=self.hide, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.show_image, command=self.show, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')
class Signup:
    def __init__(self, window):
        self.window = window

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images\\background1.png')
        photo1 = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo1)
        self.bg_panel.image = photo1
        self.bg_panel.pack(fill='both')
        # ====== Login Frame =========================
        self.sig_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.sig_frame.place(x=200, y=50)

        # ========================================================
        self.txt = "Welcome to ChatVN"
        self.heading = Label(self.sig_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=7,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=45)

        # ========================================================================
        # ============ Left Side Image ===========================================
        # ========================================================================
        self.side_image = Image.open('images\\vector1.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.sig_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ======================= Sign up ==========================================
        # ========================================================================
        self.signup = Label(self.sig_frame, text="Đăng ký", bg="#040405", fg="white",
                            font=("yu gothic ui", 20, "bold"))
        self.signup.place(x=650, y=40)

        # ======================= Name ==========================================
        self.name1 = Label(self.sig_frame, text="Họ và tên", bg="#040405", fg="#4f4e4d",
                           font=("yu gothic ui", 13, "bold"))
        self.name1.place(x=550, y=100)

        self.name1_icon = Image.open('images\\username_icon.png')
        photo2 = ImageTk.PhotoImage(self.name1_icon)
        self.name1_icon_label = Label(self.sig_frame, image=photo2, bg='#040405')
        self.name1_icon_label.image = photo2
        self.name1_icon_label.place(x=550, y=127)

        self.name1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                 font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
        self.name1_entry.place(x=580, y=127, width=244)

        self.name1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.name1_line.place(x=550, y=155)

        # ======================= Username ==========================================
        self.user1 = Label(self.sig_frame, text="Username", bg="#040405", fg="#4f4e4d",
                           font=("yu gothic ui", 13, "bold"))
        self.user1.place(x=550, y=160)

        self.user1_icon = Image.open('images\\username_icon.png')
        photo3 = ImageTk.PhotoImage(self.user1_icon)
        self.user1_icon_label = Label(self.sig_frame, image=photo3, bg='#040405')
        self.user1_icon_label.image = photo3
        self.user1_icon_label.place(x=550, y=187)

        self.user1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                 font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
        self.user1_entry.place(x=580, y=187, width=244)

        self.user1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.user1_line.place(x=550, y=215)

        # ======================= SDT ==========================================
        self.SDT1 = Label(self.sig_frame, text="Số điện thoại", bg="#040405", fg="#4f4e4d",
                          font=("yu gothic ui", 13, "bold"))
        self.SDT1.place(x=550, y=220)

        self.SDT1_icon = Image.open('images\\rsz_2sdt_icon.png')
        photo4 = ImageTk.PhotoImage(self.SDT1_icon)
        self.SDT1_icon_label = Label(self.sig_frame, image=photo4, bg='#040405')
        self.SDT1_icon_label.image = photo4
        self.SDT1_icon_label.place(x=550, y=247)

        self.SDT1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
        self.SDT1_entry.place(x=580, y=247, width=244)

        self.SDT1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.SDT1_line.place(x=550, y=275)

        # ======================= Email ==========================================
        self.email1 = Label(self.sig_frame, text="Email", bg="#040405", fg="#4f4e4d",
                            font=("yu gothic ui", 13, "bold"))
        self.email1.place(x=550, y=280)

        self.email1_icon = Image.open('images\\mail.png')
        self.email1_icon.thumbnail((25, 25), Image.LANCZOS)
        photo5 = ImageTk.PhotoImage(self.email1_icon)
        self.email1_icon_label = Label(self.sig_frame, image=photo5, bg='#040405')
        self.email1_icon_label.image = photo5
        self.email1_icon_label.place(x=550, y=307)

        self.email1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                  font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
        self.email1_entry.place(x=580, y=307, width=244)

        self.email1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.email1_line.place(x=550, y=337)

        # ======================= Password ==========================================
        self.password1 = Label(self.sig_frame, text="Mật khẩu", bg="#040405", fg="#4f4e4d",
                               font=("yu gothic ui", 13, "bold"))
        self.password1.place(x=550, y=340)

        self.password1_icon = Image.open('images\\password_icon.png')
        photo6 = ImageTk.PhotoImage(self.password1_icon)
        self.password1_icon_label = Label(self.sig_frame, image=photo6, bg='#040405')
        self.password1_icon_label.image = photo6
        self.password1_icon_label.place(x=550, y=367)

        self.password1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                     font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.password1_entry.place(x=580, y=367, width=244)

        self.password1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password1_line.place(x=550, y=395)

        # ========= show/hide password =============
        self.img1 = Image.open('images\\eye_open.jpg')
        self.img1.thumbnail((25, 25), Image.LANCZOS)
        self.show_image = ImageTk.PhotoImage(self.img1)

        self.img2 = Image.open('images\\eye_close.jpg')
        self.img2.thumbnail((25, 25), Image.LANCZOS)
        self.hide_image = ImageTk.PhotoImage(self.img2)

        self.show_button = Button(self.sig_frame, image=self.show_image, command=self.show_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_image.image = self.hide_image
        self.show_button.place(x=860, y=375)

        # ======================= Re-password ==========================================
        self.repassword1 = Label(self.sig_frame, text="Xác nhận mật khẩu", bg="#040405", fg="#4f4e4d",
                                 font=("yu gothic ui", 13, "bold"))
        self.repassword1.place(x=550, y=400)

        self.repassword1_icon = Image.open('images\\password_icon.png')
        photo7 = ImageTk.PhotoImage(self.password1_icon)
        self.repassword1_icon_label = Label(self.sig_frame, image=photo7, bg='#040405')
        self.repassword1_icon_label.image = photo7
        self.repassword1_icon_label.place(x=550, y=427)

        self.repassword1_entry = Entry(self.sig_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                       font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.repassword1_entry.place(x=580, y=427, width=244)

        self.repassword1_line = Canvas(self.sig_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.repassword1_line.place(x=550, y=455)

        # ============================= Clear ========================================
        self.clear_button = Button(self.sig_frame, text='Xoá', font=("yu gothic ui", 13, "bold underline"),
                                   fg="#0099FF", relief=FLAT,
                                   activebackground="#040405"
                                   , borderwidth=0, background="#040405", cursor="hand2", command=self.clear)
        self.clear_button.place(x=800, y=460)

        # ============================ Sign up button================================
        self.lgn_button = Image.open('images\\btn1.png')
        photo8 = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.sig_frame, image=photo8, bg='#040405')
        self.lgn_button_label.image = photo8
        self.lgn_button_label.place(x=550, y=490)
        self.login = Button(self.lgn_button_label, text='SIGNUP', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.sig)
        self.login.place(x=20, y=10)

        # ======================= Login ==========================================
        self.login = Label(self.sig_frame, text='Bạn đã có tài khoản ? ', font=("yu gothic ui", 11, "bold"),
                           relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.login.place(x=560, y=560)

        # ======================= Login icon ========================================
        self.signup_img = ImageTk.PhotoImage(file='images\\login_icon.png')
        self.signup_button_label = Button(self.sig_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#040405", activebackground="#040405",
                                          command=self.go_to_login)
        self.signup_button_label.place(x=716, y=550, width=120, height=35)

    def go_to_login(self):
        Login(self.window)

    def clear(self):
        self.email1_entry.delete(0, END)
        self.SDT1_entry.delete(0, END)
        self.name1_entry.delete(0, END)
        self.password1_entry.delete(0, END)
        self.user1_entry.delete(0, END)
        self.repassword1_entry.delete(0, END)

    def sig(self):
        self.email = self.email1_entry.get()
        self.SDT = self.SDT1_entry.get()
        self.name = self.name1_entry.get()
        self.password = self.password1_entry.get()
        self.user = self.user1_entry.get()

        if (
                self.email == '' or self.SDT == '' or self.name == '' or self.user == '' or self.password == '' or self.repassword1_entry.get() == ''):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập đầy đủ thông tin')
        elif (len(self.name) < 4):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập nhập tên từ 4 ký tự trở lên')
            self.name1_entry.delete(0, END)
        elif (len(self.user) < 4):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập nhập tên user từ 4 ký tự trở lên')
            self.user1_entry.delete(0, END)
        elif (len(self.SDT) != 10):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập số điện thoại gồm 10 chữ số')
            self.SDT1_entry.delete(0, END)
        elif (len(self.password) < 4):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập nhập mật khẩu từ 4 ký tự trở lên')
            self.password1_entry.delete(0, END)
        elif '@gmail.com' not in self.email1_entry.get():
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập email có đuôi @gmail.com')
        elif (self.password != self.repassword1_entry.get()):
            messagebox.showerror('Lỗi - ChatVN', 'Thông tin mật khẩu chưa khớp')
        else:
            conn = sqlite3.connect('Data\\dangky.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dangky WHERE user = ?', (
                self.user,))  # dấu phẩy sau đối số thứ hai để nó trở thành một tuple chứ không phải một chuỗi.

            result = cursor.fetchone()
            if result:
                messagebox.showerror('Lỗi - ChatVN', 'Tên user đã được sử dụng\nVui lòng đổi đổi tên user')
            else:
                conn1 = sqlite3.connect('Data\\dangky.db')
                cursor1 = conn1.cursor()
                cursor1.execute("INSERT INTO dangky VALUES (?, ?, ?, ?, ?)",
                                (self.name, self.user, self.SDT, self.email, self.password))
                conn1.commit()
                messagebox.showinfo('Thông báo - ChatVN', 'Đăng ký thành công')
                cursor.close()

                # Delete entry
                self.name1_entry.delete(0, 'end')
                self.user1_entry.delete(0, 'end')
                self.repassword1_entry.delete(0, 'end')
                self.SDT1_entry.delete(0, 'end')
                self.email1_entry.delete(0, 'end')
                self.password1_entry.delete(0, 'end')
                Login(self.window)

    def show_pass(self):
        self.hide_button = Button(self.sig_frame, image=self.hide_image, command=self.hide_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.hide_button.place(x=860, y=373)
        self.password1_entry.config(show='')
        self.repassword1_entry.config(show='')

    def hide_pass(self):
        self.show_button = Button(self.sig_frame, image=self.show_image, command=self.show_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_button.place(x=860, y=373)
        self.password1_entry.config(show='*')
        self.repassword1_entry.config(show='*')
class Forget:
    def __init__(self, window):
        self.window = window

        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = PILImage.open('images\\background1.png')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.window, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both')
        # ====== Login Frame =========================
        self.log_frame = Frame(self.window, bg='#040405', width=950, height=600)
        self.log_frame.place(x=200, y=50)

        # ========================================================
        self.txt = "Welcome to ChatVN"
        self.heading = Label(self.log_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=7,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=45)

        # ========================================================================
        # ============ Left Side Image ===========================================
        # ========================================================================
        self.side_image = PILImage.open('images\\vector2-removebg-preview.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.log_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ============ Image =============================================
        self.sign_in_image = PILImage.open('images\\hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.log_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=630, y=60)
        # ========================================================================
        # ======================= Sign up ==========================================
        # ========================================================================
        self.signup = Label(self.log_frame, text="Cập nhật mật khẩu", bg="#040405", fg="white",
                            font=("yu gothic ui", 17, "bold"))
        self.signup.place(x=600, y=170)

        # ======================= Username ==========================================
        self.user1 = Label(self.log_frame, text="Username", bg="#040405", fg="#4f4e4d",
                           font=("yu gothic ui", 13, "bold"))
        self.user1.place(x=550, y=230)

        self.user1_icon = PILImage.open('images\\username_icon.png')
        photo3 = ImageTk.PhotoImage(self.user1_icon)
        self.user1_icon_label = Label(self.log_frame, image=photo3, bg='#040405')
        self.user1_icon_label.image = photo3
        self.user1_icon_label.place(x=550, y=257)

        self.user1_entry = Entry(self.log_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                 font=("yu gothic ui", 12, "bold"), insertbackground='#6b6a69')
        self.user1_entry.place(x=580, y=257, width=244)

        self.user1_line = Canvas(self.log_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.user1_line.place(x=550, y=285)

        # ======================= Password ==========================================
        self.password1 = Label(self.log_frame, text="Mật khẩu mới", bg="#040405", fg="#4f4e4d",
                               font=("yu gothic ui", 13, "bold"))
        self.password1.place(x=550, y=290)

        self.password1_icon = PILImage.open('images\\password_icon.png')
        photo6 = ImageTk.PhotoImage(self.password1_icon)
        self.password1_icon_label = Label(self.log_frame, image=photo6, bg='#040405')
        self.password1_icon_label.image = photo6
        self.password1_icon_label.place(x=550, y=317)

        self.password1_entry = Entry(self.log_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                     font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.password1_entry.place(x=580, y=317, width=244)

        self.password1_line = Canvas(self.log_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password1_line.place(x=550, y=345)

        # ========= show/hide password =============
        self.img1 = PILImage.open('images\\eye_open.jpg')
        self.img1.thumbnail((25, 25))
        self.show_image = ImageTk.PhotoImage(self.img1)

        self.img2 = PILImage.open('images\\eye_close.jpg')
        self.img2.thumbnail((25, 25))
        self.hide_image = ImageTk.PhotoImage(self.img2)

        self.show_button = Button(self.log_frame, image=self.show_image, command=self.show_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_button.image = self.hide_image
        self.show_button.place(x=860, y=323)

        # ======================= Re-password ==========================================
        self.repassword1 = Label(self.log_frame, text="Xác nhận mật khẩu mới", bg="#040405", fg="#4f4e4d",
                                 font=("yu gothic ui", 13, "bold"))
        self.repassword1.place(x=550, y=350)

        self.repassword1_icon = PILImage.open('images\\password_icon.png')
        photo7 = ImageTk.PhotoImage(self.password1_icon)
        self.repassword1_icon_label = Label(self.log_frame, image=photo7, bg='#040405')
        self.repassword1_icon_label.image = photo7
        self.repassword1_icon_label.place(x=550, y=377)

        self.repassword1_entry = Entry(self.log_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#DDDDDD",
                                       font=("yu gothic ui", 12, "bold"), show="*", insertbackground='#6b6a69')
        self.repassword1_entry.place(x=580, y=377, width=244)

        self.repassword1_line = Canvas(self.log_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.repassword1_line.place(x=550, y=405)

        # ============================ Sign up button================================
        self.lgn_button = PILImage.open('images\\btn1.png')
        photo8 = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.log_frame, image=photo8, bg='#040405')
        self.lgn_button_label.image = photo8
        self.lgn_button_label.place(x=550, y=440)
        self.login = Button(self.lgn_button_label, text='UPDATE', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white', command=self.request)
        self.login.place(x=20, y=10)

        # ========================= return ============================
        self.return1 = Button(self.log_frame, text='Trở về', font=("yu gothic ui", 13, "bold"), fg="#00CC33",
                              relief=FLAT,
                              activebackground="#040405"
                              , borderwidth=0, background="#040405", cursor="hand2", command=self.go_to_login)
        self.return1.place(x=560, y=510)

    def go_to_login(self):
        Login(self.window)

    def request(self):
        self.user1 = self.user1_entry.get()
        self.pass_new = self.password1_entry.get()
        if (self.user1 == '' or self.pass_new == '' or self.repassword1_entry.get() == ''):
            messagebox.showerror('Lỗi - ChatVN', 'Vui Lòng nhập đầy đủ thông tin')
        elif (len(self.user1) < 4):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập nhập tên user từ 4 ký tự trở lên')
            self.user1_entry.delete(0, END)
        elif (len(self.pass_new) < 4):
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập nhập mật khẩu từ 4 ký tự trở lên')
            self.password1_entry.delete(0, END)
        elif (self.pass_new != self.repassword1_entry.get()):
            messagebox.showerror('Lỗi - ChatVN', 'Thông tin mật khẩu chưa khớp')
        else:
            conn = sqlite3.connect('Data/dangky.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dangky WHERE user=?", (self.user1,))
            result = cursor.fetchone()
            if result:
                cursor.execute('UPDATE dangky SET pass=? WHERE user=?', (self.pass_new, self.user1))
                conn.commit()  # save information
                messagebox.showinfo('Thông báo - ChatVN', 'Cập nhật thành công')
                Login(self.window)


            else:
                messagebox.showerror('Lỗi - ChatVN', 'Thông tin user or số điện thoại không tồn tại')
            cursor.close()

        self.user1_entry.delete(0, 'end')
        self.password1_entry.delete(0, 'end')
        self.repassword1_entry.delete(0, 'end')

    def show_pass(self):
        self.hide_button = Button(self.log_frame, image=self.hide_image, command=self.hide_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.hide_button.place(x=860, y=323)
        self.password1_entry.config(show='')
        self.repassword1_entry.config(show='')

    def hide_pass(self):
        self.show_button = Button(self.log_frame, image=self.show_image, command=self.show_pass, relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_button.place(x=860, y=323)
        self.password1_entry.config(show='*')
        self.repassword1_entry.config(show='*')
class Chat:
    def __init__(self, home, name, image_path):
        self.home = home
        self.name = name
        self.home.title(f"login3 - {name}")

        self.host = 'localhost'
        self.port = 5000

        self.is_open_icon = False
# tkinter
        # Khung chứa chức năng bên trái
        self.f1 = Frame(self.home, width=70, height=700,bg='#3333FF')
        self.f1.place(x=0,y=0)

        self.img_photo_user = Image.open(f'{image_path}')
        self.img_photo_user.thumbnail((40, 40), Image.LANCZOS)
        photo_user = ImageTk.PhotoImage(self.img_photo_user)
        photo_user_label = Label(self.f1, image=photo_user)
        photo_user_label.image = photo_user
        photo_user_label.place(relx=0.2, rely=0.05)

        self.menu = Menu(self.f1, tearoff=0)
        self.menu.add_command(label='Giới thiệu',command=self.information)
        self.menu.add_command(label='Đăng xuất',command=self.logout)
        self.menu.add_separator()
        self.menu.add_command(label='Thoát',command=self.exit)
        self.img = Image.open('images\\setting.jpg')
        self.img.thumbnail((40, 40), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.img)
        self.setting_label = Label(self.f1,image=photo, font=('Arial', 20),fg='white', borderwidth=0,bg='#3333FF',cursor='hand2')
        self.setting_label.place(relx=0.23,rely=0.9)
        self.setting_label.image = photo
        self.setting_label.bind('<Button-1>',self.showMenu)

        # Khung hiển thị danh sách người dùng
        self.f2 = Frame(self.home,width=330,height=530,bg='white')
        self.f2.place(x=70,y=170)
        self.text_scroll_x_f2 = Scrollbar(self.f2, orient=VERTICAL)
        self.text_scroll_x_f2.place(relx=0.95, rely=0, height=600)
        self.text_show_f2 = Text(self.f2, xscrollcommand=self.text_scroll_x_f2.set, wrap=WORD,
                             borderwidth=0)
        self.text_show_f2.place(relx=0, rely=0, height=600, width=315)
        self.text_show_f2.tag_configure('right', justify='right')
        self.text_scroll_x_f2.config(command=self.text_show_f2.yview)

        # khung chứa Chatbot
        self.fr_chatbot = Frame(self.home, width=330, height=69, bg='#B9D3EE')
        self.fr_chatbot.place(x=70, y=100)
        self.img_chatbot = Image.open('images\\chatbot.png')
        self.img_chatbot.thumbnail((90,80), Image.LANCZOS)
        photo_chatbot = ImageTk.PhotoImage(self.img_chatbot)
        self.chatbot_label = Label(self.fr_chatbot, image=photo_chatbot, bg='#B9D3EE')
        self.chatbot_label.image = photo_chatbot
        self.chatbot_label.place(relx=0.03,rely=0)
        self.name_chatbot = Label(self.fr_chatbot, text='ChatbotVN', font=('Arial', 18,'bold'), fg='white', bg='#B9D3EE')
        self.name_chatbot.place(relx=0.3,rely=0.27)

        def change_chatbot(event):
            Chatbot(self.home,self.f5,self.f6,self.f7,self.f8)

        self.fr_chatbot.bind('<Button-1>',change_chatbot)
        self.chatbot_label.bind('<Button-1>', change_chatbot)
        self.name_chatbot.bind('<Button-1>', change_chatbot)


        # Khung chứa chức năng tìm kiếm
        self.f3 = Frame(self.home, width=329, height=69,bg='white')
        self.f3.place(x=70, y=30)
        self.search_entry = Entry(self.f3, font=('Arial', 15),width=23, relief=FLAT, highlightthickness=0,fg='grey')
        self.search_entry.place(relx=0.05,rely=0.32)
        self.search_entry.insert(0,'Tìm kiếm người bạn kết nối')
        self.search_entry.bind("<FocusIn>",self.on_search_entry_click)
        self.search_entry.bind("<FocusOut>", self.on_search_entry_focus_out)
        self.search_entry.bind("<Return>", self.check_connect)
        self.search_entry.config(insertwidth=0,insertontime=0)
        self.search_entry_line = Canvas(self.f3, width=270, height=1, bg="#888888", highlightthickness=0)
        self.search_entry_line.place(relx=0.05,rely=0.72)
        self.img = Image.open('images\\search.jpg')
        self.img.thumbnail((28, 28), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.img)
        self.search_bn = Button(self.f3, image=photo,font=('Arial', 17),cursor='hand2',borderwidth=0,bg='white',command=self.check_connect)
        self.search_bn.image = photo
        self.search_bn.place(relx=0.88,rely=0.3)

        # Khung chứa chức năng khác
        self.f4 = Frame(self.home, width=1300, height=30,bg='#6699FF')
        self.f4.place(x=70, y=0)

        # Khung chứa chức năng tên người dùng và gọi điện
        self.f5 = Frame(self.home, width=970, height=59,bg='white')
        self.f5.place(x=400, y=30)
        self.img = Image.open('images\\call.jpg')
        self.img.thumbnail((30, 30), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.img)
        self.bn_call = Button(self.f5, image=photo, font=('Arial', 23), background='white',borderwidth=0,cursor='hand2')
        self.bn_call.image = photo
        self.bn_call.place(relx=0.85, rely=0.28)

        self.img = Image.open('images\\1159798.png')
        self.img.thumbnail((70, 35), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.img)

        self.bn_video = Button(self.f5, image=photo, bg='white', borderwidth=0,command=self.camera)
        self.bn_video.image = photo
        self.bn_video.place(relx=0.92, rely=0.241)

        # Khung  hiện thị nội dung
        self.f6 = Frame(self.home, width=970, height=499,bg='white')
        self.f6.place(x=400, y=90)
        self.text_scroll_x_f6 = Scrollbar(self.f6, orient=VERTICAL)
        self.text_scroll_x_f6.place(relx=0.98,rely=0,height=500)
        self.text_mes_f6 = Text(self.f6, xscrollcommand=self.text_scroll_x_f6.set, wrap=WORD,borderwidth=0, font=('Arial', 11),background='#E6E6FA')
        self.text_mes_f6.place(relx=0, rely=0,height=500,width=950)
        self.text_mes_f6.tag_configure('right', justify='right')
        self.text_scroll_x_f6.config(command=self.text_mes_f6.yview)

        # Khung chứa chức năng về tin nhắn
        self.f7 = Frame(self.home, width=970, height=49,bg='white')
        self.f7.place(x=400, y=590)
        self.img1 = Image.open('images\\mic.png')
        self.img1.thumbnail((30, 30), Image.LANCZOS)
        photo1 = ImageTk.PhotoImage(self.img1)
        self.bn_mic = Button(self.f7, image=photo1, bg='white', borderwidth=0, command=self.mic,cursor='hand2')
        self.bn_mic.image = photo1
        self.bn_mic.place(relx=0.03, rely=0.15)

        self.img4 = Image.open('images\\anh.png')
        self.img4.thumbnail((40, 40), Image.LANCZOS)
        photo4 = ImageTk.PhotoImage(self.img4)
        self.bn_picture = Button(self.f7, image=photo4, bg='white', borderwidth=0, command=self.send_picture, cursor='hand2')
        self.bn_picture.image = photo4
        self.bn_picture.place(relx=0.11, rely=0.06)

        self.img5 = Image.open('images\\gir.png')
        self.img5.thumbnail((50, 50), Image.LANCZOS)
        photo5 = ImageTk.PhotoImage(self.img5)
        self.bn_gir = Button(self.f7, image=photo5, bg='white', borderwidth=0, command=self.gir, cursor='hand2')
        self.bn_gir.image = photo5
        self.bn_gir.place(relx=0.19, rely=0.17)

        self.img8 = Image.open('images\\listen.jpg')
        self.img8.thumbnail((35,35),Image.LANCZOS)
        photo8 = ImageTk.PhotoImage(self.img8)
        self.bn_listen = Button (self.f7,image = photo8, bg='white', borderwidth=0, command=self.listen_music, cursor='hand2')
        self.bn_listen.image = photo8
        self.bn_listen.place(relx=0.28, rely=0.15)

        # Khung soạn tin nhắn
        self.f8 = Frame(self.home, width=970, height=60, bg='white')
        self.f8.place(x=400, y=640)
        self.mes_entry = Text(self.f8, font=('Arial', 15),width=67,height=2 ,relief=FLAT, highlightthickness=0,fg='grey')
        self.mes_entry.place(relx=0.03, rely=0.20)
        self.mes_entry.insert('1.0', 'Nhập @, tin nhắn tới ...')
        self.mes_entry.config(insertwidth=0, insertontime=0)

        self.mes_entry.bind('<FocusIn>', self.on_mes_entry_click)
        self.mes_entry.bind('<FocusOut>', self.on_mes_entry_focus_out)
        self.mes_entry.bind('<Shift-Return>', self.shift_enter)
        self.mes_entry.bind('<Return>', self.send_message)

        self.img2 = Image.open('images\\send1.png')
        self.img2.thumbnail((40,40),Image.LANCZOS)
        photo2 = ImageTk.PhotoImage(self.img2)
        self.mes_bn = Button(self.f8, image = photo2,bg='white',  borderwidth=0,command=self.send_message,cursor='hand2')
        self.mes_bn.image = photo2
        self.mes_bn.place(relx=0.9, rely=0.15)

        self.img_icon = Image.open('images\\icon.png')
        self.img_icon.thumbnail((35,35),Image.LANCZOS)
        photo_icon = ImageTk.PhotoImage(self.img_icon)
        self.icon_btn = Button(self.f8,image=photo_icon,bg='white',  borderwidth=0,command=self.iconForm,cursor='hand2')
        self.icon_btn.image = photo_icon
        self.icon_btn.place(relx=0.82, rely=0.2)

        # socket nhắn tin
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.host, self.port)
        self.client_socket.connect(self.server_address)
        print('Đã kết nối tới Server:', self.server_address)

        threading.Thread(target=self.receive_message).start()

        # Đóng gói thông tin tên của client vào JSON message
        message = {"type": "login", "user": self.name}
        message_json = json.dumps(message)

        # Gửi message đến server
        self.client_socket.sendall(message_json.encode('utf-8'))
    def check_connect(self,event = None):
        search_entry = self.search_entry.get()
        if search_entry == '' or search_entry == 'Tìm kiếm người bạn kết nối':
            messagebox.showerror('Lỗi - ChatVN', 'Vui lòng nhập đầy đủ thông tin')
        else:
            conn = sqlite3.connect('Data\\dangky.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dangky WHERE user = ?", (search_entry,))
            row = cursor.fetchall()
            conn.close()
            if row:
                yes = messagebox.askyesno('Thông báo - ChatVN', 'Đã tìm thấy người dùng\nBạn có muốn kết nối với họ không')
                if yes:
                    mes = {'connect': search_entry}
                    mes_json = json.dumps(mes)
                    self.client_socket.sendall(mes_json.encode('utf-8'))

                    self.listFrame_f2 = Frame(self.text_show_f2, bg="#66CCFF", relief=FLAT, padx=10, pady=5,
                                              highlightbackground='#E6E6FA',
                                              highlightthickness=1, cursor='hand2')
                    self.listFrame_f2.pack(side=RIGHT, fill=X, expand=True)
                    self.list_f2 = Label(self.listFrame_f2, text=f'{search_entry}                                                            ', bg="#66CCFF", font=("Arial", 13),
                                         anchor='w', cursor='hand2')
                    self.list_f2.pack(side=LEFT, fill=X, expand=True)
                    self.text_show_f2.window_create(END, window=self.listFrame_f2)
                    self.text_show_f2.insert(END, '\n')
                    self.text_show_f2.see(END)

                    self.user_label = Label(self.f5, text=search_entry, bg="white", anchor='w', font=("Arial", 14))
                    self.user_label.place(relx=0.2, rely=0.3)

                    # with open(self.image_path, 'rb') as f:
                    #     a = f.read()
                    # self.client_socket.sendall(a)
                    # print(len(a))
            else:
                messagebox.showerror('Lỗi - ChatVN', 'Không tìm thấy tên trong hệ thống\nCó thể họ chưa hoạt động hoặc chưa kết nối app')
    def receive_message(self):

        while True:
            data = self.client_socket.recv(102400000)
            try:
                message_str = data.decode('utf-8')
            except UnicodeDecodeError:
                message_str = None
            if message_str:
                data = data.decode('utf-8')
                sender_name, message = data.rsplit(":", 1) # tách chuỗi str
                message_frame = Frame(self.text_mes_f6, bg="#E0FFFF", relief=FLAT, padx=10, pady=5,
                                      highlightbackground='#E6E6FA', highlightthickness=1)
                message_frame.pack(side=RIGHT)

                message_label = Label(message_frame, text=f"{message}", bg="#E0FFFF",anchor='w', font=("Arial", 13), wraplength=350)
                message_label.pack(side=LEFT)

                time = datetime.datetime.now()
                time_present = time.strftime("%H:%M")
                time_label = Label(message_frame, text=f"{time_present}", bg="#E0FFFF", font=("Arial", 8))
                time_label.pack(side=BOTTOM)
                self.text_mes_f6.window_create(END, window=message_frame)
                self.text_mes_f6.insert(END, '\n')
                self.text_mes_f6.see(END)
            else:
                img = b''
                a = 0
                while True:
                    print(len(data))
                    if not data:
                        break
                    a += len(data)
                    img += data
                    if len(img) == a:
                        break
                print('Nhận',len(img))
                img_receive = Image.open(io.BytesIO(img))

                img_receive.thumbnail((int(img_receive.size[0] / 4), int(img_receive.size[1] / 4)), Image.LANCZOS)
                photo_receive = ImageTk.PhotoImage(img_receive)

                img_frame_receive = Frame(self.text_mes_f6, bg="#E0FFFF", relief=FLAT, padx=10, pady=5,
                                          highlightbackground='#E6E6FA',
                                          highlightthickness=1)

                img_label_receive = Label(img_frame_receive, image=photo_receive, bg="#E0FFFF", font=("Arial", 10),
                                          wraplength=350)
                img_label_receive.image = photo_receive
                img_label_receive.pack(side=LEFT)

                def show_Menu_3_cham_receive(e):
                    menu_3_cham_receive.post(e.x_root, e.y_root)

                def save_receive():
                    data1 = base64.b64encode(data)
                    self.save_image_photo(data1)

                menu_3_cham_receive = Menu(img_frame_receive, tearoff=0)
                menu_3_cham_receive.add_command(label='Lưu', command=save_receive)
                menu_3_cham_receive.add_command(label='Xoá', command=img_frame_receive.destroy)

                ba_cham_label_receive = Label(img_frame_receive, text="...", bg="#E0FFFF", font=("Arial", 14),cursor='hand2')
                ba_cham_label_receive.pack(side=TOP)
                ba_cham_label_receive.bind('<Button-1>', show_Menu_3_cham_receive)

                time_receive = datetime.datetime.now()
                time_present_receive = time_receive.strftime("%H:%M")
                time_label_receive = Label(img_frame_receive, text=f"{time_present_receive}", bg="#E0FFFF",
                                           font=("Arial", 8))
                time_label_receive.pack(side=BOTTOM)

                self.text_mes_f6.window_create(END, window=img_frame_receive)
                self.text_mes_f6.insert(END, '\n')
    def send_picture(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg')])
        if self.search_entry.get() == '' or self.search_entry.get() == 'Tìm kiếm người bạn kết nối':
            messagebox.showerror('Lỗi', 'Vui lòng nhập người bạn muốn kết nối trước khi gửi')
        elif os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as f:
                img_data = f.read()

                img = Image.open(io.BytesIO(img_data))

                img.thumbnail((int(img.size[0] / 4), int(img.size[1] / 4)), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                message_frame = Frame(self.text_mes_f6,bg="white", relief=FLAT, padx=10, pady=5, highlightbackground='#E6E6FA',
                                      highlightthickness=1)

                message_label = Label(message_frame, image=photo, bg="white", font=("Arial", 10), wraplength=350,cursor='hand2')
                message_label.image = photo
                message_label.pack(side=LEFT)

                def show_Menu_3_cham(e):
                    menu_3_cham.post(e.x_root, e.y_root)

                def save():
                    self.save_image(self.file_path)

                menu_3_cham = Menu(message_frame, tearoff=0)
                menu_3_cham.add_command(label='Lưu', command=save)
                menu_3_cham.add_command(label='Xoá', command=message_frame.destroy)

                ba_cham_label = Label(message_frame, text="...", bg="white", font=("Arial", 14),cursor='hand2')
                ba_cham_label.pack(side=TOP)
                ba_cham_label.bind('<Button-1>', show_Menu_3_cham)

                time = datetime.datetime.now()
                time_present = time.strftime("%H:%M")
                time_label = Label(message_frame, text=f"{time_present}", bg="white", font=("Arial", 8))
                time_label.pack(side=BOTTOM)

                if len(img_data) <= 8192:
                    self.client_socket.sendall(img_data)
                    print('Gửi ', len(img_data))

                    self.text_mes_f6.window_create(END, window=message_frame)
                    self.text_mes_f6.insert(END, '\n')
                else:
                    messagebox.showerror('Lỗi', 'Kích thước quá tải\nVui lòng giảm kích thước xuống hợp lệ')
    def send_message(self,event = None):
        message = self.mes_entry.get("1.0", "end-1c")
        if message == '' or  message == 'Nhập @, tin nhắn tới ...':
            messagebox.showerror('Lỗi', 'Vui lòng nhập thông tin trước khi gửi')
        elif self.search_entry.get() == '' or self.search_entry.get() == 'Tìm kiếm người bạn kết nối':
            messagebox.showerror('Lỗi', 'Vui lòng nhập người bạn muốn kết nối trước khi gửi')
        else:
            message_frame = Frame(self.text_mes_f6, bg="white", relief=FLAT, padx=10, pady=5,highlightbackground='#E6E6FA',highlightthickness=1)
            message_frame.pack(side=RIGHT)

            message_label = Label(message_frame, text=message, bg="white", font=("Arial", 13),wraplength=350,anchor='w')
            message_label.pack(side=LEFT)

            time = datetime.datetime.now()
            time_present = time.strftime("%H:%M")
            time_label = Label(message_frame, text=f"{time_present}", bg="white", font=("Arial", 8))
            time_label.pack(side=BOTTOM)
            self.client_socket.send(message.encode('utf-8'))
            self.text_mes_f6.window_create(END, window=message_frame)
            self.text_mes_f6.insert(END, '\n')
            # self.text_mes_f6.config(state='disabled')
            self.text_mes_f6.see(END)
            self.mes_entry.delete('1.0', END)
    def iconForm(self):
        global table_icon
        if self.is_open_icon:
            table_icon.destroy()
            self.is_open_icon = False
        else:
            table_icon = Toplevel(self.f8,bg='white')
            table_icon.title('Icon - ChatVN')
            table_icon.geometry('150x150+1100+500')
            table_icon.resizable(False,False)
            table_icon.lift()
            emoji_data = [('emojis\\u0001f44a.png', '\U0001F44A'), ('emojis\\u0001f44c.png', '\U0001F44C'),
                          ('emojis\\u0001f44d.png', '\U0001F44D'),
                          ('emojis\\u0001f495.png', '\U0001F495'), ('emojis\\u0001f496.png', '\U0001F496'),
                          ('emojis\\u0001f4a6.png', '\U0001F4A6'),
                          ('emojis\\u0001f4a9.png', '\U0001F4A9'), ('emojis\\u0001f4af.png', '\U0001F4AF'),
                          ('emojis\\u0001f595.png', '\U0001F595'),
                          ('emojis\\u0001f600.png', '\U0001F600'), ('emojis\\u0001f602.png', '\U0001F602'),
                          ('emojis\\u0001f603.png', '\U0001F603'),
                          ('emojis\\u0001f605.png', '\U0001F605'), ('emojis\\u0001f606.png', '\U0001F606'),
                          ('emojis\\u0001f608.png', '\U0001F608'),
                          ('emojis\\u0001f60d.png', '\U0001F60D'), ('emojis\\u0001f60e.png', '\U0001F60E'),
                          ('emojis\\u0001f60f.png', '\U0001F60F'),
                          ('emojis\\u0001f610.png', '\U0001F610'), ('emojis\\u0001f618.png', '\U0001F618'),
                          ('emojis\\u0001f61b.png', '\U0001F61B'),
                          ('emojis\\u0001f61d.png', '\U0001F61D'), ('emojis\\u0001f621.png', '\U0001F621'),
                          ('emojis\\u0001f624.png', '\U0001F621'),
                          ('emojis\\u0001f631.png', '\U0001F631'), ('emojis\\u0001f632.png', '\U0001F632'),
                          ('emojis\\u0001f634.png', '\U0001F634'),
                          ('emojis\\u0001f637.png', '\U0001F637'), ('emojis\\u0001f642.png', '\U0001F642'),
                          ('emojis\\u0001f64f.png', '\U0001F64F'),
                          ('emojis\\u0001f920.png', '\U0001F920'), ('emojis\\u0001f923.png', '\U0001F923'),
                          ('emojis\\u0001f928.png', '\U0001F928')]

            emoji_x_pos = 0
            emoji_y_pos = 0
            for Emoji in emoji_data:
                global emojis
                emojis = Image.open(Emoji[0])
                emojis.thumbnail((20,20),Image.LANCZOS)
                emojis = ImageTk.PhotoImage(emojis)

                emoji_unicode = Emoji[1]
                emoji_label = Label(table_icon, image = emojis, text = emoji_unicode, bg = "white", cursor = "hand2")
                emoji_label.image = emojis
                emoji_label.place(x=emoji_x_pos, y=emoji_y_pos)
                emoji_label.bind('<Button-1>', lambda x: self.insert_emoji(x))

                emoji_x_pos += 25
                cur_index = emoji_data.index(Emoji)
                if (cur_index + 1) % 6 == 0:
                    emoji_y_pos += 25
                    emoji_x_pos = 0
            self.is_open_icon = True
    def insert_emoji(self, x):
        if self.mes_entry.get('1.0', "end-1c") == 'Nhập @, tin nhắn tới ...':
            self.mes_entry.delete('1.0','end')
            self.mes_entry.config(fg='black')
            self.mes_entry.insert("end-1c", x.widget['text'])
        else:
            self.mes_entry.insert("end-1c", x.widget['text'])
    def listen_music(self):
        self.topl_music = Toplevel(self.home)
        self.topl_music.title('Youtube Music - ChatVN')
        self.topl_music.resizable(False, False)
        self.topl_music.geometry('220x50+600+300')
        self.topl_music.lift()

        self.name_music = Label(self.topl_music, text='Nhập bài hát yêu thích', font=('Arial', 12), background='#99CCFF')
        self.name_music.pack(fill=X)

        self.entry_music = Entry(self.topl_music, font=('Arial', 12))
        self.entry_music.pack(side=LEFT)

        def search_music():
            if self.entry_music.get() == '':
                messagebox.showerror('Lỗi', 'Vui lòng nhập thông tin cần tìm kiếm')
                self.topl_music.lift()
            else:
                webbrowser.open(f'https://www.youtube.com/results?search_query= {self.entry_music.get()}')
                self.topl_music.destroy()

        self.img = Image.open('images\\search.jpg')
        self.img.thumbnail((20, 20), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.img)
        self.bn_music = Button(self.topl_music,image=photo, font=('Arial', 12), borderwidth=0, cursor='hand2',command=search_music)
        self.bn_music.image = photo
        self.bn_music.pack(side=RIGHT)
    def information(self):
        self.toplv = Toplevel(self.home,bg='white')
        self.toplv.resizable(False, False)
        self.toplv.title('Giới thiệu - ChatVN')
        self.toplv.geometry('330x400+500+200')

        self.ig = Image.open('images\\chatvn.png')
        self.ig.thumbnail((100,100),Image.LANCZOS)
        photo6 = ImageTk.PhotoImage(self.ig)
        self.label = Label(self.toplv,image=photo6,background='white')
        self.label.image = photo6
        self.label.place(x=10,y=10)
        self.label1 = Label(self.toplv,text='ChatVN', font=('Goudy Stout', 17),fg='#3366FF',background='white')
        self.label1.place(x=130,y=50)
        self.label2 = Label(self.toplv,text='Thông tin:', font=('Arial', 13),fg='#444444',background='white')
        self.label2.place(x=20,y=125)
        self.label3 = Label(self.toplv, text='App mới tạo nên còn nhiều hạn chế\n Mong mọi người có thể góp ý giúp mình', font=('Arial', 10), fg='black', background='white')
        self.label3.place(x=20, y=150)
        self.label4 = Label(self.toplv, text='-----------------------------------------', font=('Arial', 10), fg='#999999', background='white')
        self.label4.place(x=20, y=190)
        self.label5 = Label(self.toplv, text='Liên hệ và đóng góp:', font=('Arial', 13), fg='#444444', background='white')
        self.label5.place(x=20, y=230)
        self.label6 = Label(self.toplv,
                            text='Email:          xuandienk4@gmail.com',
                            font=('Arial', 10), fg='black', background='white')
        self.label6.place(x=20, y=265)
        self.label7 = Label(self.toplv,text='Zalo:',font=('Arial', 10), fg='black', background='white')
        self.label7.place(x=20, y=288)

        self.ig1 = Image.open('images\\maQR.jpg')
        self.ig1.thumbnail((100, 100), Image.LANCZOS)
        photo7 = ImageTk.PhotoImage(self.ig1)
        self.label8 = Label(self.toplv, image=photo7, background='white')
        self.label8.image = photo7
        self.label8.place(x=100, y=290)
    def logout(self):
        answer = messagebox.askyesno("Thông báo - ChatVN", "Bạn đã chắc chắn đăng xuất chưa ?")
        if answer:
            Login(self.home)
    def exit(self):
        answer = messagebox.askyesno('Thông báo - ChatVN','Bạn muốn thoát ChatVN ?')
        if answer:
            self.home.destroy()
    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)
    def save_image_photo(self,file_path):
        if not file_path:
            return

        # Extract tên file và tạo file mới
        file_name = os.path.basename(file_path)

        # Hòi người dùng muốn dùng tên file gì
        save_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile=file_name,
                                                 filetypes=[('JPEG files', '*.jpg'), ('PNG files', '*.png')])

        # Nếu không có file thì return
        if not save_path:
            return

        # load file lên và save
        with open(file_path, 'rb') as file:
            img = Image.open(file)
            img.save(save_path)
    def save_image(self,file_path):
        if not file_path:
            return

        # Extract tên file và tạo file mới
        file_name = os.path.basename(file_path)
        file_name_parts = file_name.split('.')
        new_file_name = '.'.join(file_name_parts[:-1]) + '_ChatVN.' + file_name_parts[-1]

        # Hòi người dùng muốn dùng tên file gì
        save_path = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile=new_file_name,
                                                 filetypes=[('JPEG files', '*.jpg'), ('PNG files', '*.png')])

        # Nếu không có file thì return
        if not save_path:
            return

        # load file lên và save
        with open(file_path, 'rb') as file:
            img = Image.open(file)
            img.save(save_path)
    def gir(self):
        pass
    def shift_enter(self, event=None):
        self.mes_entry.insert(END, '')
    def on_search_entry_click(self,event):
        if self.search_entry.get() == 'Tìm kiếm người bạn kết nối':
            self.search_entry.delete(0, 'end')
            self.search_entry.config(fg='black')
    def on_search_entry_focus_out(self,event):
        if self.search_entry.get() == '':
            self.search_entry.insert(0, 'Tìm kiếm người bạn kết nối')
            self.search_entry.config(fg='grey')
    def on_mes_entry_click(self,event):
        if self.mes_entry.get("1.0", "end-1c") == 'Nhập @, tin nhắn tới ...':
            self.mes_entry.delete("1.0", 'end')
            self.mes_entry.config(fg='black')
    def on_mes_entry_focus_out(self,event):
        if self.mes_entry.get("1.0", "end-1c") == '':
            self.mes_entry.insert("1.0", 'Nhập @, tin nhắn tới ...')
            self.mes_entry.config(fg='grey')
    def mic(self):
        threading.Thread(target=self.listen).start()
    def listen(self):
        self.mes_entry.delete("1.0", END)
        self.mes_entry.config(fg='black')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            try:
                audio = r.listen(source, timeout=5.0)
                text = r.recognize_google(audio, language='vi')
                print("You said: {}".format(text))
                self.mes_entry.insert(END, text)
            except sr.WaitTimeoutError:
                messagebox.showerror('Lỗi', 'Không nhận dạng được giọng nói quá 3 giây')
            except sr.UnknownValueError:
                messagebox.showerror('Lỗi', 'Không thể nhận được giọng nói của bạn')
    def camera(self):
        self.top = Toplevel(self.home)
        self.top.lift()
        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open camera: {str(e)}")
            return

        self.canvas = Canvas(self.top, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                             height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.img10 = Image.open('images\\close_call.jpg')
        self.img10.thumbnail((30, 30), Image.LANCZOS)
        photo10 = ImageTk.PhotoImage(self.img10)
        self.bn_cam = Button(self.top, image=photo10, bg='white', borderwidth=0, command=self.close_camera)
        self.bn_cam.image = photo10
        self.bn_cam.place(x=303, y=450)

        self.delay = 15
        self.update()

        self.top.protocol("WM_DELETE_WINDOW", self.close_camera)
    def close_camera(self):
        self.cap.release()
        self.top.destroy()
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

            self.home.after(self.delay, self.update)
class Chatbot:
    def __init__(self, home, f5, f6, f7, f8):
        self.home = home
        self.f5 = f5
        self.f6 = f6
        self.f7 = f7
        self.f8 = f8

        self.f5.place_forget()
        self.f6.place_forget()
        self.f7.place_forget()
        self.f8.place_forget()
        # =======================================================================================
        self.f5_chatbot = Frame(self.home, width=970, height=59, bg='white')
        self.f5_chatbot.place(x=400, y=30)

        self.return_chatbot = Button(self.f5_chatbot, text="←", command=self.return_frame_chat,
                                     font=("yu gothic ui", 16, "bold"),
                                     cursor="hand2", borderwidth=0, bg='white', fg='black')
        self.return_chatbot.place(relx=0.01, rely=0.15)

        self.img_f5_chatbot = Image.open('images\\chatbot.png')
        self.img_f5_chatbot.thumbnail((60, 50), Image.LANCZOS)
        photo_f5_chatbot = ImageTk.PhotoImage(self.img_f5_chatbot)
        self.chatbot_f5_label = Label(self.f5_chatbot, image=photo_f5_chatbot, bg='white')
        self.chatbot_f5_label.image = photo_f5_chatbot
        self.chatbot_f5_label.place(relx=0.05, rely=0.13)
        self.name_f5_chatbot = Label(self.f5_chatbot, text='ChatbotVN', font=('Arial', 12), fg='black',
                                     bg='white')
        self.name_f5_chatbot.place(relx=0.12, rely=0.32)
        # =======================================================================================
        self.f6_chatbot = Frame(self.home, width=970, height=499, bg='white')
        self.f6_chatbot.place(x=400, y=90)
        self.text_scroll_x_f6_chatbot = Scrollbar(self.f6_chatbot, orient=VERTICAL)
        self.text_scroll_x_f6_chatbot.place(relx=0.98, rely=0, height=500)
        self.text_mes_f6_chatbot = Text(self.f6_chatbot, xscrollcommand=self.text_scroll_x_f6_chatbot.set, wrap=WORD,
                                        borderwidth=0,
                                        font=('Arial', 11), background='#E6E6FA')
        self.text_mes_f6_chatbot.place(relx=0, rely=0, height=500, width=950)
        self.text_mes_f6_chatbot.tag_configure('right', justify='right')
        self.text_scroll_x_f6_chatbot.config(command=self.text_mes_f6_chatbot.yview)
        # =======================================================================================
        self.f7_chatbot = Frame(self.home, width=970, height=49, bg='white')
        self.f7_chatbot.place(x=400, y=590)
        self.loa = Button(self.f7_chatbot, text='📣', font=('Arial', 22),bg='white', foreground='black', borderwidth=0)
        self.loa.place(relx=0.02, rely=0)

        # =======================================================================================
        self.f8_chatbot = Frame(self.home, width=970, height=60, bg='white')
        self.f8_chatbot.place(x=400, y=640)
        self.mes_entry_chatbot = Text(self.f8_chatbot, font=('Arial', 15), width=67, height=2, relief=FLAT,
                                      highlightthickness=0,
                                      fg='grey')
        self.mes_entry_chatbot.place(relx=0.03, rely=0.20)
        self.mes_entry_chatbot.insert('1.0', 'Nhập @, tin nhắn tới ...')
        self.mes_entry_chatbot.config(insertwidth=0, insertontime=0)

        self.mes_entry_chatbot.bind('<FocusIn>', self.on_mes_entry_click_chatbot)
        self.mes_entry_chatbot.bind('<FocusOut>', self.on_mes_entry_focus_out_chatbot)
        self.mes_entry_chatbot.bind('<Shift-Return>', self.shift_enter)
        self.mes_entry_chatbot.bind('<Return>', self.send_question)

        self.img2_chatbot = Image.open('images\\send1.png')
        self.img2_chatbot.thumbnail((40, 40), Image.LANCZOS)
        photo2_chatbot = ImageTk.PhotoImage(self.img2_chatbot)
        self.mes_bn_chatbot = Button(self.f8_chatbot, image=photo2_chatbot, bg='white', borderwidth=0,
                                     command=self.threading_chatbot,

                                     cursor='hand2')
        self.mes_bn_chatbot.image = photo2_chatbot
        self.mes_bn_chatbot.place(relx=0.9, rely=0.15)
    def speak(self,audio):
        pygame.init()
        tts = gTTS(text=audio, lang='vi')
        tts.save('voice.mp3')
        sound = pygame.mixer.Sound('voice.mp3')
        sound.play()
        time.sleep(sound.get_length())
        os.remove('voice.mp3')
    def shift_enter(self,event = None):
            self.mes_entry_chatbot.insert(END,'')
    def on_mes_entry_click_chatbot(self, event):
        if self.mes_entry_chatbot.get("1.0", "end-1c") == 'Nhập @, tin nhắn tới ...':
            self.mes_entry_chatbot.delete("1.0", 'end')
            self.mes_entry_chatbot.config(fg='black')
    def on_mes_entry_focus_out_chatbot(self, event):
        if self.mes_entry_chatbot.get("1.0", "end-1c") == '':
            self.mes_entry_chatbot.insert("1.0", 'Nhập @, tin nhắn tới ...')
            self.mes_entry_chatbot.config(fg='grey')
    def return_frame_chat(self):
        self.f5_chatbot.place_forget()
        self.f6_chatbot.place_forget()
        self.f7_chatbot.place_forget()
        self.f8_chatbot.place_forget()

        self.f5.place(x=400, y=30)
        self.f6.place(x=400, y=90)
        self.f7.place(x=400, y=590)
        self.f8.place(x=400, y=640)
    def chatgpt(self, user_question):
        # Cài đặt thông tin model và API key
        openai.api_key = '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'
        model = 'text-davinci-003'
        response = openai.Completion.create(
            engine=model,
            prompt=user_question,
            max_tokens=1024,
            n=1,  # trả lời số lượng một câu
            temperature=0.5
        )
        # lấy câu trả lời đầu tiên
        if 'bạn là ai' in user_question:
            response_text = '\n\nTôi là ChatbotVN. Tôi rất vui khi được nói chuyện với bạn.'
        elif 'bạn đến từ đâu' in user_question:
            response_text = '\n\nTôi đến từ trong tim bạn. Ở đâu có bạn ở đó có tôi'
        elif 'người tạo ra bạn' in user_question:
            response_text = '\n\nTôi được tạo ra bởi ChatVN nơi có tôi và bạn.'
        elif ('ChatVN' or 'chatvn') in user_question:
            response_text = '\n\nChatVN là ứng dụng nhắn tin mới thành lập từ 2023. Ứng dụng cũng có nhiều chức năng nhưng còn hạn chế. Mặc dù vậy nhưng ChatVN sẽ không ngừng cải thiện và tạo ra những đột phá mới và tạo hứng thú cho người dùng. Tuy nhiên mọi đóng góp của bạn là niềm vui của chúng tôi.'
        elif 'xuân diện' in user_question:
            response_text = '\n\nXuân Diện là người tạo ra ChatVN.'
        else:
            response_text = response.choices[0].text
        return response_text
    def threading_chatbot(self):
        threading.Thread(target=self.send_question).start()
    def send_question(self,event = None):
        message = self.mes_entry_chatbot.get("1.0", "end-1c")
        if message == '' or message == 'Nhập @, tin nhắn tới ...':
            messagebox.showerror('Lỗi', 'Vui lòng nhập thông tin trước khi gửi')
        else:
            message_frame = Frame(self.text_mes_f6_chatbot, bg="white", relief=FLAT, padx=10, pady=5,
                                  highlightbackground='#E6E6FA', highlightthickness=1)
            message_frame.pack(side=RIGHT, anchor="ne")

            message_label = Label(message_frame, text=message, bg="white", font=("Arial", 10), wraplength=600,
                                  justify="left", anchor="w")
            message_label.pack(side=LEFT)

            time = datetime.datetime.now()
            time_present = time.strftime("%H:%M")
            time_label = Label(message_frame, text=f"{time_present}", bg="white", font=("Arial", 8))
            time_label.pack(side=BOTTOM)

            self.text_mes_f6_chatbot.window_create(END, window=message_frame)
            self.text_mes_f6_chatbot.insert(END, '\n')
            self.text_mes_f6_chatbot.see(END)
            self.mes_entry_chatbot.delete('1.0', END)
            self.home.after(1000, self.get_answer, message)
    def get_answer(self, message):
        response_text = self.chatgpt(message)
        message1_frame = Frame(self.text_mes_f6_chatbot, bg="#E0FFFF", relief=FLAT, padx=10, pady=5,
                               highlightbackground='#E6E6FA', highlightthickness=1)
        message1_frame.pack(side=LEFT)

        message_label = Label(message1_frame, text=f"{response_text}", bg="#E0FFFF", font=("Arial", 10), justify="left",
                              anchor="w",
                              wraplength=600)
        message_label.pack(side=LEFT, anchor="n")
        self.loa.config(command=lambda:self.speak(response_text))
        self.text_mes_f6_chatbot.see(END)

        def copy_message(event):
            self.home.clipboard_clear()  # Xóa nội dung clipboard hiện có
            self.home.clipboard_append(message_label['text'])  # Thêm nội dung mới vào clipboard
            self.home.focus_set()  # Thiết lập focus cho cửa sổ để xác định nơi để paste
            pyperclip.copy(self.home.clipboard_get())  # Lưu nội dung vào ctrl + c
            message_box = Toplevel(self.home)
            message_box.title('Thông báo')
            message_box_label = Label(message_box, text='Đã copy thành công', font=("Arial", 10))
            message_box_label.pack(side=BOTTOM)
            message_box.after(2000, lambda: message_box.destroy())

        menu_label = Label(message1_frame, text="Copy", bg="#E0FFFF", font=("Arial", 7), cursor='hand2', fg='#339966')
        menu_label.pack(side=TOP)
        menu_label.bind('<Button-1>', copy_message)

        time = datetime.datetime.now()
        time_present = time.strftime("%H:%M")
        time_label = Label(message1_frame, text=f"{time_present}", bg="#E0FFFF", font=("Arial", 8))
        time_label.pack(side=BOTTOM)
        self.text_mes_f6_chatbot.window_create(END, window=message1_frame)
        self.text_mes_f6_chatbot.insert(END, '\n')
        self.text_mes_f6_chatbot.see(END)

if __name__ == '__main__':
    window = Tk()
    window.geometry('1370x700+-10+0')
    window.resizable(False, False)
    window.title('login3')
    window.config(background='#003399')
    icon = ImageTk.PhotoImage(Image.open("images\\chatvn.png"))
    Login(window)
    window.iconphoto(True, icon)
    window.mainloop()
