import webbrowser
import re
import sys
import os
import  tkinter as tk
import tkinter.messagebox as tk1
import tkinter.filedialog
from pathlib import Path

# Add tkdesigner to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tkdesigner.designer import Designer
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add tkdesigner to the PATH.")


# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Required in order to add data files to Windows executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""


def btn_clicked():
    token = token_entry.get()
    URL = URL_entry.get()
    output_path = path_entry.get()
    output_path = output_path.strip()

    if not token:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter Token.")
        return
    if not URL:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter URL.")
        return
    if not output_path:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Enter a valid output path.")
        return

    match = re.search(
        r'https://www.figma.com/file/([0-9A-Za-z]+)', URL.strip())
    if match is None:
        tk.messagebox.showerror(
            "Invalid URL!", "Please enter a valid file URL.")
        return

    file_key = match[1].strip()
    token = token.strip()
    output = Path(f"{output_path}/build").expanduser().resolve()

    if output.exists() and not output.is_dir():
        tk1.showerror(
            "Exists!",
            f"{output} already exists and is not a directory.\n"
            "Enter a valid output directory.")
    elif output.exists() and output.is_dir() and tuple(output.glob('*')):
        response = tk1.askyesno(
            "Continue?",
            f"Directory {output} is not empty.\n"
            "Do you want to continue and overwrite?")
        if not response:
            return

    designer = Designer(token, file_key, output)
    designer.design()

    tk.messagebox.showinfo(
        "Success!", f"គម្រោងបង្កើតដោយជោគជ័យនៅ {output}.")


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)


def know_more_clicked(event):
    instructions = (
        "https://link.payway.com.kh/aba?id=DDCDBF42E545&code=292017&acc=007265828&dynamic=true"
        "blob/master/docs/instructions.md")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


window = tk.Tk()
logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
window.call('wm', 'iconphoto', window._w, logo)
window.title("Tkinter Designer")

window.geometry("862x519")
window.configure(bg="#7ff63a")
canvas = tk.Canvas(
    window, bg="#7ff63a", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")

text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)

token_entry = tk.Entry(bd=0, bg="#F6F7F9",fg="#000716",  highlightthickness=0)
token_entry.place(x=490.0, y=137+25, width=321.0, height=35)
token_entry.focus()

URL_entry = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716",  highlightthickness=0)
URL_entry.place(x=490.0, y=218+25, width=321.0, height=35)

path_entry = tk.Entry(bd=0, bg="#F6F7F9", fg="#000716", highlightthickness=0)
path_entry.place(x=490.0, y=299+25, width=321.0, height=35)

path_picker_img = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    image = path_picker_img,
    text = '',
    compound = 'center',
    fg = 'white',
    borderwidth = 0,
    highlightthickness = 0,
    command = select_path,
    relief = 'flat')

path_picker_button.place(
    x = 783, y = 319,
    width = 24,
    height = 22)

canvas.create_text(
    490.0, 156.0, text="Token ID", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 234.5, text="File URL", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 315.5, text="Output Path",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    573.5, 88.0, text="Enter the details.",
    fill="#515486", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="សូមស្វាគមន៍មកកាន់ Tkinter \n Designer", bg="#7ff63a",
    fg="white",justify="left", font=("Arial-BoldMT", int(20.0)))
title.place(x=20.0, y=120.0)
canvas.create_rectangle(25, 160, 33 + 60, 160 + 5, fill="#7ff63a", outline="")

info_text = tk.Label(
    text="Tkinter Designer ប្រើ Figma API\n"
     "ដើម្បីវិភាគឯកសាររចនា បន្ទាប់មកបង្កើត\n"
     "លេខកូដ និងឯកសារនីមួយៗដែលត្រូវការ\n"
     "សម្រាប់ GUI របស់អ្នក។\n\n"

     "សូម្បីតែ GUI នេះត្រូវបានបង្កើត\n"
     "ប្រើ Tkinter Designer ។",
    bg="#7ff63a", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=20.0, y=200.0)

know_more = tk.Label(
    text="................ This My ABA Qr For pay me the Coffe Thank You",
    bg="#f6d03a", fg="white",justify="left", cursor="hand2", font=("Arial-BoldMT", int(12.0)))
know_more.place(x=20, y=400)
know_more.bind('<Button-1>', know_more_clicked,)

know_more1 = tk.Label(
    text="Click here",
    bg="#f6b13a", fg="white",justify="left", cursor="hand2", font=("Arial-BoldMT", int(12.0)))
know_more1.place(x=20, y=400)
know_more1.bind('<Button-1>', know_more_clicked,)



generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)

window.resizable(False, False)
window.mainloop()
