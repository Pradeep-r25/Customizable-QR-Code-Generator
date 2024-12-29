import pyqrcode
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
import io
import webcolors  
import os

def get_serial_number():
    if os.path.exists("serial_number.txt"):
        with open("serial_number.txt", "r") as f:
            return int(f.read().strip())
    return 1  

def update_serial_number(sno):
    with open("serial_number.txt", "w") as f:
        f.write(str(sno))

def gen_qr():
    global img_tk 
    content = con.get()
    color_fg = color_fg_var.get()
    color_bg = color_bg_var.get()

    try:
        color_fg_hex = webcolors.name_to_hex(color_fg)
        color_bg_hex = webcolors.name_to_hex(color_bg)
    except ValueError:
        print(f"Invalid color name. Please use valid color names (e.g., 'red', 'blue', 'black').")
        return

    qr = pyqrcode.create(content)
    
    qr_image = io.BytesIO()
    qr.png(qr_image, scale=10, module_color=color_fg_hex, background=color_bg_hex)
    qr_image.seek(0) 

   
    img = Image.open(qr_image) 
    
    img = img.convert("RGB")
    img.thumbnail((200, 200))  
    
    img_tk = ImageTk.PhotoImage(img)
    
    l4.config(image=img_tk)
    l4.image = img_tk  

    print(f"QR Code generated with colors: {color_fg}/{color_bg}")

def save():
    content = con.get()
    
    if not content:  
        print("Content is empty!")
        return

    sno = get_serial_number()

    file_name = f"qr_{sno:03d}"  

    color_fg = color_fg_var.get()
    color_bg = color_bg_var.get()
    file_format = format_var.get()

    try:
        color_fg_hex = webcolors.name_to_hex(color_fg)
        color_bg_hex = webcolors.name_to_hex(color_bg)
    except ValueError:
        print(f"Invalid color name. Please use valid color names (e.g., 'red', 'blue', 'black').")
        return

    qr = pyqrcode.create(content)

    if file_format == 'PNG':
        qr.png(f"{file_name}.png", scale=10, module_color=color_fg_hex, background=color_bg_hex)
        print(f"QR code saved as {file_name}.png")
    elif file_format == 'SVG':
        qr.svg(f"{file_name}.svg", scale=10, module_color=color_fg_hex, background=color_bg_hex)
        print(f"QR code saved as {file_name}.svg")
    elif file_format == 'PDF':
        pdf_filename = f"{file_name}.pdf"
        c = canvas.Canvas(pdf_filename)
        
        qr.png("temp_qr.png", scale=10, module_color=color_fg_hex, background=color_bg_hex)
        c.drawImage("temp_qr.png", 100, 500, width=300, height=300)
        c.save()
        
        print(f"QR code saved as {pdf_filename}")
    else:
        print("Invalid format selected!")

   
    sno += 1
    update_serial_number(sno)

    con.set('') 

wind = Tk()
wind.title('QR Code Generator')
wind.geometry('500x550')
wind.resizable(0, 0)
wind.config(bg='#f4f4f7')

con = StringVar()
color_fg_var = StringVar(value="black")  
color_bg_var = StringVar(value="white")  
format_var = StringVar(value="PNG")  

f1 = Frame(wind, width=500, height=100, bg='#f4f4f7')
f1.grid(row=0, column=0, columnspan=3, padx=20, pady=15)

f2 = Frame(wind, width=500, height=50, bg='#f4f4f7')
f2.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

f3 = Frame(wind, width=500, height=250, bg='#f4f4f7')
f3.grid(row=2, column=0, columnspan=3, padx=20, pady=20)

l1 = Label(f1, text='QR Code Generator', font=('Helvetica', 18, 'bold'), bg='#f4f4f7', fg='#333')
l1.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

l3 = Label(f2, text='Enter the content', font=('Arial', 12), bg='#f4f4f7', fg='#333')
l3.grid(row=0, column=0, padx=10)

e1 = Entry(f2, textvariable=con, width=40, font=('Arial', 12), relief="solid", borderwidth=1)
e1.grid(row=0, column=1, padx=5)

l3_fg = Label(f2, text="Foreground Color", font=('Arial', 10), bg='#f4f4f7', fg='#333')
l3_fg.grid(row=1, column=0, padx=5)

e3_fg = Entry(f2, textvariable=color_fg_var, width=15, font=('Arial', 12), relief="solid", borderwidth=1)
e3_fg.grid(row=1, column=1, padx=5)

l3_bg = Label(f2, text="Background Color", font=('Arial', 10), bg='#f4f4f7', fg='#333')
l3_bg.grid(row=2, column=0, padx=5)

e3_bg = Entry(f2, textvariable=color_bg_var, width=15, font=('Arial', 12), relief="solid", borderwidth=1)
e3_bg.grid(row=2, column=1, padx=5)

l_format = Label(f2, text="Select Format", font=('Arial', 10), bg='#f4f4f7', fg='#333')
l_format.grid(row=3, column=0, padx=5)

formats = ['PNG', 'SVG', 'PDF']  
format_menu = ttk.Combobox(f2, textvariable=format_var, values=formats, state="readonly", width=12)
format_menu.grid(row=3, column=1, padx=5)
format_menu.current(0)  

l4 = Label(f3, pady=10, bg='#f4f4f7')
l4.grid(row=0, column=0, columnspan=2)

b1 = Button(f2, text='Generate', command=gen_qr, font=('Arial', 12), width=15, relief="solid", borderwidth=1)
b1.grid(row=4, column=0, pady=15)

b2 = Button(f2, text='Save', command=save, font=('Arial', 12), width=15, relief="solid", borderwidth=1)
b2.grid(row=4, column=1, pady=15)

wind.mainloop()
