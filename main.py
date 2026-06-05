import json
import threading
import requests
import pyperclip

from io import BytesIO
from PIL import Image

import customtkinter as ctk


ctk.set_appearance_mode("dark")

app = ctk.CTk()
# app.iconbitmap("icon.ico")
app.title("Paper Extractor")
app.geometry("700x500")


def log(message):
    textbox.configure(state="normal")  # enable editing internally
    textbox.insert("end", message + "\n")
    textbox.see("end")
    textbox.configure(state="disabled")  # lock again (read-only)
    app.update()


def generate_pdf():

    try:
        clipboard_text = pyperclip.paste()
        urls = json.loads(clipboard_text)

    except Exception:
        log("ERROR: Clipboard does not contain valid URL data.")
        return

    log(f"Found {len(urls)} pages.")
    log("")

    images = []

    for i, url in enumerate(urls, start=1):

        log(f"Downloading page {i}/{len(urls)}")

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content))

        if img.mode != "RGB":
            img = img.convert("RGB")

        images.append(img)

    log("")
    log("Creating PDF...")

    images[0].save(
        "answer_sheet.pdf",
        save_all=True,
        append_images=images[1:]
    )

    log("")
    log("Done!")
    log("Saved as answer_sheet.pdf")


def start():
    threading.Thread(target=generate_pdf, daemon=True).start()


title = ctk.CTkLabel(
    app,
    text="Paper Extractor",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=20)


button = ctk.CTkButton(
    app,
    text="Generate PDF",
    command=start,
    width=200,
    height=40
)
button.pack(pady=10)


textbox = ctk.CTkTextbox(
    app,
    width=650,
    height=350
)
textbox.pack(pady=20)


# make textbox read-only from start
textbox.configure(state="normal")
textbox.insert("end", "Waiting for URLs from clipboard...\n")
textbox.configure(state="disabled")


app.mainloop()