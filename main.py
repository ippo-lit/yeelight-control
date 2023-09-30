import tkinter as tk
from tkinter import Spinbox, colorchooser
from yeelight import Bulb
import json

def toggle_light():
    try:
        ampul = Bulb(ip_entry.get(), int(port_entry.get()))
        ampul.toggle()
        status_label.config(text="Ampul Durumu: " + ampul.get_properties()["power"])
    except Exception as e:
        status_label.config(text="Hata: " + str(e))

def set_brightness():
    try:
        brightness = int(brightness_spinbox.get())
        ampul = Bulb(ip_entry.get(), int(port_entry.get()))
        ampul.set_brightness(brightness)
    except Exception as e:
        status_label.config(text="Hata: " + str(e))

def set_color_temperature():
    try:
        temperature = int(temperature_spinbox.get())
        ampul = Bulb(ip_entry.get(), int(port_entry.get()))
        ampul.set_color_temp(temperature)
    except Exception as e:
        status_label.config(text="Hata: " + str(e))

def choose_color():
    color = colorchooser.askcolor(title="Renk Seçin")
    if color[1] is not None:
        try:
            r, g, b = [int(c) for c in color[0]]
            ampul = Bulb(ip_entry.get(), int(port_entry.get()))
            ampul.set_rgb(r, g, b)
            last_selected_color = (r, g, b)
        except Exception as e:
            status_label.config(text="Hata: " + str(e))

def set_default_settings():
    try:
        ampul = Bulb(ip_entry.get(), int(port_entry.get()))
        ampul.set_rgb(255, 255, 255)
        ampul.set_brightness(100)
        ampul.set_color_temp(4700)
    except Exception as e:
        status_label.config(text="Hata: " + str(e))

def save_settings():
    settings = {
        "ip": ip_entry.get(),
        "port": port_entry.get(),
        "brightness": brightness_spinbox.get(),
        "temperature": temperature_spinbox.get()
    }
    with open("settings.json", "w") as file:
        json.dump(settings, file)

def load_settings():
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
            ip_entry.delete(0, tk.END)
            ip_entry.insert(0, settings.get("ip", ""))
            port_entry.delete(0, tk.END)
            port_entry.insert(0, settings.get("port", ""))
            brightness_spinbox.delete(0, tk.END)
            brightness_spinbox.insert(0, settings.get("brightness", 50))
            temperature_spinbox.delete(0, tk.END)
            temperature_spinbox.insert(0, settings.get("temperature", 2700))
    except FileNotFoundError:
        pass

def on_exit():
    save_settings()
    root.destroy()

root = tk.Tk()
root.title("Yeelight Kontrol")

root.geometry("400x300")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 200
window_height = 400

x_position = screen_width - window_width - 20
y_position = screen_height - window_height - 100

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

ip_label = tk.Label(root, text="Ampul IP Adresi:")
ip_label.pack()

ip_entry = tk.Entry(root)
ip_entry.pack()

port_label = tk.Label(root, text="Ampul Port: (55443)")
port_label.pack()

port_entry = tk.Entry(root)
port_entry.pack()

toggle_button = tk.Button(root, text="Ampulu Aç/Kapat", command=toggle_light)
toggle_button.pack()

brightness_label = tk.Label(root, text="Parlaklık:")
brightness_label.pack()

brightness_spinbox = Spinbox(root, from_=1, to=100)
brightness_spinbox.pack()

temperature_label = tk.Label(root, text="Renk Sıcaklığı (1700-6500K):")
temperature_label.pack()

temperature_spinbox = Spinbox(root, from_=1700, to=6500)
temperature_spinbox.pack()

set_brightness_button = tk.Button(root, text="Parlaklığı Ayarla", command=set_brightness)
set_brightness_button.pack()

set_temperature_button = tk.Button(root, text="Renk Sıcaklığını Ayarla", command=set_color_temperature)
set_temperature_button.pack()

color_button = tk.Button(root, text="Renk Seç", command=choose_color)
color_button.pack()

default_settings_button = tk.Button(root, text="Varsayılana Ayarla", command=set_default_settings)
default_settings_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

load_settings()

root.protocol("WM_DELETE_WINDOW", on_exit)

root.mainloop()
