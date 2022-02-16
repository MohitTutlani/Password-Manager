#for storing password into database
import json
import mysql.connector
from tkinter import *
#import message box from tkinter
from tkinter import messagebox
#pyperclip helps to put our password into clipboard so we can easily paste it elsewhere
import pyperclip
#password generator file
from password_generator import password_generator

# ---------------------------- UI COLORS AND FONT ------------------------------- #
WINDOW_BG = "#000000"
FIELD_COLORS = "#dddddd"
FIELD_FONT_COLOR = "#000000"
LABEL_COLOR = "white"
LABEL_BACKGROUND = "black"
FONT = ("Comic Sans MS", 15, "normal")

# ---------------------------- UI SETUP ------------------------------- #
#Creating a tkinter window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=WINDOW_BG)

# ---------------------------- Databse Connection SETUP ------------------------------- #
#Database connection
myconn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "password_manager"
)

# ---------------------------- Genereate Password ------------------------------- #

def generate_password():
    #generate new password from password generator
    password = password_generator()
    #copying password to our clipboard
    pyperclip.copy(password)
    #clear password entry widget
    password_entry.delete(0,END)
    #entering password to password entry widget
    password_entry.insert(END,password)

# ---------------------------- Search Password ------------------------------- #
def search_password():
    # Getting user website entry
    website = website_entry.get()
    # Get password data
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website to search")
    else:
        # Try to see if password files exit ,is in JSON, and not blank
        try:
            # seeing if there is any old passwords data file
            with open("data.json", mode="r") as old_password_file:
                # reading old password data
                password_data = json.load(old_password_file)
        # If there is no password file, or is in incorrect JSON format or is blank
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showinfo(title="No passwords saved", message="Sorry, you have not saved any password before")
        else:
            
            # If the searched website is in password data
            if website in password_data:
                username = password_data[website]["username"]
                password = password_data[website]["password"]
                # Save to clipboard message box
                is_clipboard = messagebox.askokcancel(title=website, message=f"username: {username}\nPassword: {password}"
                                                                             f"\n\nSave to clipboard ?")
                # Save to clipboard
                if is_clipboard:
                    # saving password to clipboard
                    pyperclip.copy(password)
                    messagebox.showinfo(title="Saved to clipboard", message="Password has been saved to clipboard")
            # IF the searched website is not in the database
            else:
                messagebox.showinfo(title="Password not saved for this website", message=f"The password for {website}\n"
                                                                                         f"has not been saved")



# ---------------------------- Insert into database ------------------------------- #
def insert():
    
    if (len(website_entry.get()) != 0) or (len(email_entry.get()) != 0) or (len(password_entry.get()) != 0):
        cur = myconn.cursor()
        #getting values from Entrybox
        website=website_entry.get()
        username=email_entry.get()
        password=password_entry.get()
        try:
            #asking for confirmation of data inserted
            is_ok = messagebox.askokcancel(title="Confirm entries", message=f"These are the details you entered: \n Website: {website} \n Email: {username} \n Password: {password} \n Is it okay to save ?")

            #condition to check if the result is OK, If Yes then the if will execute
            if is_ok:
                web = "select * from user_details where website=%s and username<>%s and password<>%s"
                web_val = (website,username,password)
                cur.execute(web,web_val)
                result=cur.fetchall()
                if result:
                        print("insert data")
                        sql = "insert into user_details values(%s,%s,%s,%s)"
                        val=("",website,username,password)
                        cur.execute(sql,val)
                        myconn.commit()
                        messagebox.showinfo(title="Confirmed", message="Record Inserted")
                        file_generation(website,username,password)
                        myconn.close()
                else:
                    ok=messagebox.showerror(title="Insertion Error", message="The password is used before")
                    if ok:
                        window.destroy()


        except:
            myconn.rollback()
    else:
        ok=messagebox.showerror(title="Error",message="Please insert information")
        if ok:
            window.destroy()

# ---------------------------- file manager ------------------------------- #
def file_manager(new_entry):
    try:
        with open("data.json",mode="r") as old_password_file:
            password_data = json.load(old_password_file)
    except(FileNotFoundError,json.decoder.JSONDecodeError):
        with open("data.json",mode="w") as new_password_file:
            json.dump(new_entry,new_password_file,indent=4)
            messagebox.showinfo(title="Entry",message="File Created...!")
    else:
        password_data.update(new_entry)
        with open("data.json",mode="w") as old_password_file:
            json.dump(password_data, old_password_file, indent=4)
            messagebox.showinfo(title="Entry",message="File Created...!")
    finally:
        website_entry.delete(0,END)
        email_entry.delete(0,END)
        password_entry.delete(0,END)
    
# ---------------------------- file generation storage ------------------------------- #
def file_generation(website,username,password):
    
        pyperclip.copy(password)
        new_entry_in_json = {
                website:{
                    "username": username,
                    "password": password
                }
            }
        file_manager(new_entry_in_json)   


# ---------------------------- UI SETUP ------------------------------- #
#Canvas for image
PASS_IMG = PhotoImage(file="logo.png")
canvas = Canvas(width= 200, height= 200, bg=WINDOW_BG, highlightthickness=0)
canvas.config()
canvas.create_image(100,100,image=PASS_IMG)
canvas.grid(column=1, row=0)

#Labels
#labels for websites
website_label = Label(window,text="Website ",font=FONT,bg=LABEL_BACKGROUND , fg=LABEL_COLOR, padx=20).grid(column=0, row=1, sticky=W)

#Labels for Email/Username
user = Label(window,text="Email/Username", font=FONT, bg=LABEL_BACKGROUND, fg=LABEL_COLOR, padx=20).grid(column=0, row=2, sticky=W)

#Label for Password
password = Label(window,text="password", font=FONT,bg=LABEL_BACKGROUND, fg=LABEL_COLOR, padx=20).grid(column=0, row=3, sticky=W)
window.grid_columnconfigure(1, weight=1)

#Entry box for the above labels
#Website Entry Box
website_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
website_entry.insert(END, string="")
website_entry.grid(column= 1, row=1)

website_entry.focus()
#Email/username Entry Box
email_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
email_entry.insert(END, string="")
email_entry.grid(column= 1, row=2)
#Password Entry Box
password_entry = Entry(width=30, bg=FIELD_COLORS, fg=FIELD_FONT_COLOR, font=FONT)
password_entry.insert(END, string="")
password_entry.grid(column= 1, row=3)


#BUTTONS
#Search Password button
search_button = Button(text="Search", font=FONT, command=search_password).grid(column=3, row=1)

#Generate Password Button
generate_password = Button(window, text="Generate Password", font= FONT, command=generate_password).grid(column=3, row=3)

#Create a file for password button
insert_button = Button(window, text="Insert Record", padx=95, font=FONT,command= insert).grid(column=1, row=5 ,columnspan=2, sticky=W)

window.mainloop()