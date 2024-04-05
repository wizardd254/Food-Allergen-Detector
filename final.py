from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import ast
import sqlite3
import tkinter as tk
import cv2
import pytesseract

conn = sqlite3.connect('user_allergies.db')  
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (Username TEXT,allergies TEXT)''')
conn.commit()

root=tk.Tk()
root.title("Login")
root.geometry("1450x750+0+0")

root.configure(bg='#cfe2f3')

background_image = tk.PhotoImage(file="logo3.png")

canvas = tk.Canvas(root)
canvas.pack(fill=BOTH, expand=YES)

canvas.create_image(0, 0, image=background_image, anchor=NW)

frame=tk.Frame(root,width=350,height=350,bg="#9CEEF1")
frame.place(x=880,y=200)
heading=tk.Label(frame,text='Sign In',fg='#1D1F61',bg='#9CEEF1', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

def signin():
    username=user.get()
    password=code.get()

    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)

    if username in r.keys() and password == r[username]:
        cursor.execute("SELECT allergies FROM users WHERE Username=?", (username,))
        user_allergies = cursor.fetchone()

        if user_allergies:
            allergies = user_allergies[0]
            show_allergies(username, allergies)
        else:
            add_allergies(username)

    else:
        messagebox.showerror('Invalid', 'Invalid username or password') 

def show_allergies(username, allergies):
    def edit_allergies():
        edit_allergies_window = tk.Toplevel(root)
        edit_allergies_window.title("Edit Allergies")
        edit_allergies_window.geometry('400x300')

        background_image2= PhotoImage(file="background.png")

        canvas2 = Canvas(edit_allergies_window)
        canvas2.pack(fill=BOTH, expand=YES)

        canvas2.create_image(0, 0, image=background_image2, anchor=NW)

        swelling_var = tk.IntVar()
        digestion_var = tk.IntVar()
        rash_var = tk.IntVar()
        asthma_var = tk.IntVar()
        itchy_var = tk.IntVar()
        sneezing_var = tk.IntVar()

        def save_allergies():
            selected_allergies = []
            if swelling_var.get() == 1:
                selected_allergies.append("Swelling")
            if digestion_var.get() == 1:
                selected_allergies.append("Digestion Issues")
            if rash_var.get() == 1:
                selected_allergies.append("Rash")
            if asthma_var.get() == 1:
                selected_allergies.append("Asthma")
            if itchy_var.get() == 1:
                selected_allergies.append("Itchy Nose")
            if sneezing_var.get() == 1:
                selected_allergies.append("Sneezing")

            allergies_text = ",".join(selected_allergies)

            cursor.execute('UPDATE users SET allergies=? WHERE Username=?', (allergies_text, username))
            conn.commit()
            edit_allergies_window.destroy()
            show_allergies(username, allergies_text)  

        swelling = tk.Checkbutton(edit_allergies_window, text="Swelling", variable=swelling_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        swelling.place(x=40, y=40)

        digestion = tk.Checkbutton(edit_allergies_window, text="Digestion Issues", variable=digestion_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        digestion.place(x=240, y=40)

        rash = tk.Checkbutton(edit_allergies_window, text="Rash", variable=rash_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        rash.place(x=40, y=80)

        asthma = tk.Checkbutton(edit_allergies_window, text="Asthma", variable=asthma_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        asthma.place(x=240, y=80)

        itchy = tk.Checkbutton(edit_allergies_window, text="Itchy Nose", variable=itchy_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        itchy.place(x=40, y=120)

        sneezing = tk.Checkbutton(edit_allergies_window, text="Sneezing", variable=sneezing_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
        sneezing.place(x=240, y=120)

        save_button = tk.Button(edit_allergies_window, text="Save Allergies", command=save_allergies, bg='#61EDDF', font=(12))
        save_button.place(x=120, y=180)

        edit_allergies_window.mainloop()

    def scan_allergies():

        conn1 = sqlite3.connect('allergy_database.db')
        cursor1 = conn1.cursor()

        def browse_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
            if file_path:
                image = cv2.imread(file_path)
                extracted_text = extract_text_from_image(image)
                extracted_text_label.config(text="Extracted Text: " + extracted_text, fg="black", font=("Helvetica", 12))

                analyze_button.config(state=tk.NORMAL)
                global extracted_text_data
                extracted_text_data = extracted_text

        def analyze_image():
            matched_allergens = match_allergens(extracted_text_data)

        def extract_text_from_image(image):
            text = pytesseract.image_to_string(image)
            return text

        def match_allergens(extracted_text):
            words = extracted_text.split()
            matched_allergens = set()

            cursor.execute("SELECT allergies FROM users WHERE Username=?", (username,))
            user_allergies = cursor.fetchone()
            if user_allergies:
                allergies = user_allergies[0]
                cursor1.execute('SELECT allergen_list FROM allergies WHERE allergy_name IN ({seq})'.format(
            seq=','.join(['?'] * len(allergies.split(',')))), allergies.split(','))
                allergen_list = cursor1.fetchall()
                
                for word in words:
                    c='IN'
                    for allergen in allergen_list:
                        if (word.lower() in allergen[0].lower() and word.lower()!=c.lower()):
                            matched_allergens.add(word)

                if matched_allergens:
                    messagebox.showwarning("Warning", f"The product contains allergens: {', '.join(matched_allergens)}")
                else:
                    messagebox.showinfo("Safe", "The product seems safe to eat!")
            else:
                messagebox.showerror("Error", "User allergies not found. Please add allergies.")   
            app.destroy()         

        app = Toplevel(root)
        app.title("Allergy Allergen Detector")
                
        background_image1 = tk.PhotoImage(file="background2.png")

        canvas1 = tk.Canvas(app,width=651,height=600)
        canvas1.pack(fill=BOTH, expand=YES)

        canvas1.create_image(0, 0, image=background_image1, anchor=NW)

        label_style = {'font': ('Helvetica', 14), 'bg': '#61EDDF'}
        file_path_label = tk.Label(app, text="Select an image:", **label_style)
        file_path_label.place(x=245,y=25)

        button_style = {'font': ('Helvetica', 12), 'bg': '#61EDDF', 'fg': 'black'}
        browse_button = tk.Button(app, text="Browse", command=browse_image, **button_style,bd=5)
        browse_button.place(x=275,y=350)

        analyze_button = tk.Button(app, text="Analyze", command=analyze_image, font=('Helvectica',12),bg='#61EDDF',fg='black',bd=5)
        analyze_button.place(x=275,y=425)
        analyze_button.config(state=tk.DISABLED)  

        extracted_text_label = tk.Label(app, text="", fg='white',bg='#61EDDF')
        extracted_text_label.place(x=100,y=60)

        app.mainloop()

    allergy_window = tk.Toplevel(root)
    allergy_window.title("User Allergies")
    allergy_window.geometry('600x300')

    background_image1 = tk.PhotoImage(file="background3.png")

    canvas1 = tk.Canvas(allergy_window)
    canvas1.pack(fill=BOTH, expand=YES)

    canvas1.create_image(0, 0, image=background_image1, anchor=NW)

    allergy_label = tk.Label(allergy_window, text=f"User Allergies", font=('Arial', 12), bg='#61EDDF')
    allergy_label.place(x=258, y=50)

    allergy_label1 = tk.Label(allergy_window, text=f"{allergies}", font=('Arial', 12), bg='#61EDDF', fg='black',width=50,anchor=W)
    allergy_label1.place(x=80, y=90)

    edit_button = tk.Button(allergy_window, text="Edit Allergies", command=edit_allergies,bg='#61EDDF',bd=5)
    edit_button.place(x=260,y=140)

    scan_button = tk.Button(allergy_window, text="SCAN THE LABEL", command=scan_allergies,bg='#61EDDF',bd=5)
    scan_button.place(x=250,y=190)

    allergy_window.mainloop()        

def add_allergies(username):

    add_allergywindow=tk.Toplevel(root)
    add_allergywindow.geometry("400x300")
    add_allergywindow.title("Add allergies")
    background_image2= PhotoImage(file="background.png")

    canvas2 = Canvas(add_allergywindow)
    canvas2.pack(fill=BOTH, expand=YES)

    canvas2.create_image(0, 0, image=background_image2, anchor=NW)
    

    swelling_var=tk.IntVar()
    rash_var=tk.IntVar()
    asthma_var=tk.IntVar()
    digestion_var=tk.IntVar()
    itchy_var=tk.IntVar()
    sneezing_var=tk.IntVar()

    def save_allergies():
       selected=[]

       if swelling_var.get()==1:
        selected.append("Swelling")
       if rash_var.get()==1:
        selected.append("Rash")
       if itchy_var.get()==1:
        selected.append("Itchy Nose")
       if asthma_var.get()==1:
        selected.append("Asthma")
       if sneezing_var.get()==1:
        selected.append("Sneezing")
       if digestion_var.get()==1:
        selected.append("Digestion Issues")
      
       
       allergytext=','.join(selected)
       cursor.execute("INSERT INTO users (allergies,Username) VALUES(?,?)",(allergytext,username))
       conn.commit()
       show_allergies(username,allergytext)

    swelling = tk.Checkbutton(add_allergywindow, text="Swelling", variable=swelling_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    swelling.place(x=40, y=40)

    rash = tk.Checkbutton(add_allergywindow, text="Rash", variable=rash_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    rash.place(x=40, y=80)
    digestion = tk.Checkbutton(add_allergywindow, text="Digestion Issues", variable=digestion_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    digestion.place(x=40, y=120)

    asthma = tk.Checkbutton(add_allergywindow, text="Asthma", variable=asthma_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    asthma.place(x=40, y=160)

    itchynose = tk.Checkbutton(add_allergywindow, text="Itchy Nose", variable=itchy_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    itchynose.place(x=40, y=200)

    sneezing = tk.Checkbutton(add_allergywindow, text="Sneezing", variable=sneezing_var, bg='#1A1D53', fg='white', font=(12), selectcolor='black')
    sneezing.place(x=40, y=240)

    tk.Button(add_allergywindow,text="Save",bg='lightblue',fg='black',font=('Arial',12,'bold'),command=save_allergies).place(x=80,y=240)

    add_allergywindow.mainloop()


    

def signup_command():
  window=tk.Toplevel(root)

  window.title("SignUp")
  window.geometry('1450x750+0+0')
  window.configure(bg='#1D1F61')

  background_image1 = tk.PhotoImage(file="background1.png")

  canvas1 = tk.Canvas(window)
  canvas1.pack(fill=BOTH, expand=YES)

  canvas1.create_image(0, 0, image=background_image1, anchor=NW)

  def signup():
    username = user.get()
    password = code.get()
    conform_password = conform_code.get()

    if len(password) < 8:
        messagebox.showerror('Invalid', 'Password should be at least 8 characters long')
        return
    
 
    if password != conform_password:
        messagebox.showerror('Invalid', 'Both passwords should match')
        return

  
    cursor.execute("SELECT Username FROM users WHERE Username=?", (username,))
    existing_username = cursor.fetchone()
    if existing_username:
        messagebox.showerror('Invalid', 'Username already exists')
        return

  
    try:
        file = open('Datasheet.txt', 'r+')
        d = file.read()
        r = ast.literal_eval(d)

        dict2 = {username: password}
        r.update(dict2)

        file.truncate(0)
        file.close()

        file = open('Datasheet.txt', 'w')
        w = file.write(str(r))
        window.destroy()
        messagebox.showinfo('Signup', 'Successfully signed up')
    except Exception as e:
        messagebox.showerror('Error', f'Error during signup: {str(e)}')
    
  def sign():
     window.destroy()
        
  img = PhotoImage(file='login.png')

  tk.Label(window,image=img, border=0, bg='#1A1D53').place(x=250, y=190)

  frame=tk.Frame(window,width=350,height=390,bg="#9CEEF1")
  frame.place(x=950,y=190)

  tk.Label(frame,text='Sign up',fg='#1D1F61', bg="#9CEEF1", font=('Microsoft Yahei UI Light', 23, 'bold')).place(x=100,y=5)
 
  def on_enter(e):
    if user.get() == 'Username':
     user.delete(0,'end')
  def on_leave(e):
     if user.get() == '':
       user.insert(0, 'Username' )

  user = tk.Entry(frame,width=25,fg='black',border=0,font=('Microsoft Yahei UI Light',11,'bold'),bg="#9CEEF1")
  user.place(x=30,y=80)
  user.insert(0, 'Username')
  user.bind("<FocusIn>", on_enter)
  user.bind("<FocusOut>", on_leave)

  tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

  def on_enter(e):
   if code.get() == 'Password':
    code.delete(0,'end')
  def on_leave(e):
    if code.get() == '':
      code.insert(0, 'Password')

  code = tk.Entry(frame,width=25,fg='black',border=0,font=('Microsoft Yahei UI Light',11,'bold'),bg="#9CEEF1")
  code.place(x=30,y=150)
  code.insert(0, 'Password')
  code.bind("<FocusIn>", on_enter)
  code.bind("<FocusOut>", on_leave)

  tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

  def on_enter(e):
    if conform_code.get() == 'Conform Password': 
        conform_code.delete(0, 'end') 
    conform_code.config(show='*')
  def on_leave(e):
    if conform_code.get() == '':
     conform_code.insert(0,'Conform Password')

  conform_code = tk.Entry(frame,width=25,fg='black',border=0,bg="#9CEEF1", font=('Microsoft Yahei UI Light', 11,'bold'))
  conform_code.place(x=30,y=220)
  conform_code.insert(0, 'Conform Password')
  conform_code.bind("<FocusIn>",on_enter)
  conform_code.bind("<FocusOut>", on_leave)

  tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)

  tk.Button(frame, width=39, pady=7, text='Sign up',bg='#1D1F61', fg='white', border=0,command=signup).place(x=35,y=280)
  label=tk.Label(frame, text='I have an account', fg='black', bg="#9CEEF1", font=('Microsoft YaHei UI Light',11,'bold'))
  label.place(x=70,y=340)

  signin=tk.Button(frame, width=6, text='Sign in', border=0,bg="#9CEEF1",font=('Microsoft YaHei UI Light',11,'bold'), cursor='hand2', fg='#1D1F61',command=sign)
  signin.place(x=215,y=338)

  window.mainloop()

def on_enter(e):
   if user.get() == 'Username': 
    user.delete(0, 'end')
def on_leave(e):
    name=user.get()
    if name == '':
        user.insert(0,'Username')

user = tk.Entry(frame,width=25, fg='black',border=0, font=('Microsoft YaHei UI Light',11,'bold'),bg='#9CEEF1')
user.place(x=30,y=80)
user.insert(0, 'Username')
tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)


def on_enter_password(e):
    if code.get() == 'Password': 
        code.delete(0, 'end') 
    code.config(show='*') 

def on_leave_password(e):
    if code.get()=='': 
        code.insert(0,'Password')


code = tk.Entry(frame, width=25, fg='black', border=0, font=('Microsoft YaHei UI Light', 11, 'bold'), bg='#9CEEF1')
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_password)  
code.bind('<FocusOut>', on_leave_password)

tk.Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

tk.Button(frame,width=39,pady=7,text='Sign in',bg='#1D1F61',fg='white',border=0,command=signin,relief='groove').place(x=35,y=204)
label=tk.Label(frame,text="Don't have an account?",fg='black',bg='#9CEEF1',font=('Microsoft YaHei UI Light',11,'bold'))
label.place(x=50,y=270)

sign_up= tk.Button(frame, width=6, text='Sign up',border=0,bg='#9CEEF1', cursor='hand2', fg='#1D1F61',command=signup_command,font=('Microsoft YaHei UI Light',11,'bold'))
sign_up.place(x=235,y=268)

root.mainloop()