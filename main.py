# TriggerBot Overlay & Website: Version immer synchron halten!
# Kostenloses Hosting-Tipp: Siehe unten für Anleitung zu GitHub Pages.
# ...existing code...

import pyautogui
import keyboard
from PIL import ImageGrab
import threading
import time
import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import colorchooser
import tkinter.ttk as ttk
import requests  # already imported
import tkinter.messagebox
import random
import tkinter.simpledialog

# === VERIFICATION CODE CONFIG ===
CODE_URL = "https://ljashub.github.io/triggerbot-gui/"  # <-- Set your real URL here!
CODE_REFRESH_INTERVAL = 30  # seconds

# === CONFIGURATION ===
CURRENT_VERSION = "v0.6"  # Version erhöht

# === HOTKEY DEFAULTS ===
HOTKEY_STARTSTOP = "f5"
HOTKEY_PANIC = "ctrl+f4"

# === THEMES ===
THEMES = {
    'dark': {'bg': '#23272e', 'fg': '#00ff99', 'console': '#181818', 'button': '#00ff99', 'label': '#bbbbbb'},
    'light': {'bg': '#ececec', 'fg': '#1a7f5a', 'console': '#f5f5f5', 'button': '#1a7f5a', 'label': '#444'}
}
current_theme = 'light'

FONT_SIZES = [9, 10, 11, 12, 14, 16]
current_font_size = 10

ICONS = ["🎯", "🟢", "⭐", "🔵", "🟡", "🟣"]
current_icon = 0

# === LANGUAGE ===
LANGUAGES = {
    'en': {
        'status': 'Status:',
        'inactive': 'INACTIVE',
        'active': 'ACTIVE',
        'color_trigger': 'Set Color Trigger',
        'pick_color': 'Pick Color',
        'start_stop': '▶ Start / Stop (F5)',
        'panic': '🛑 PANIC (CTRL+F4)',
        'overlay_info': 'Overlay: Selectable corner | Hotkeys: F5, CTRL+F4',
        'made_by': '🌹 made by ljas | youtube.com/ljas_vu',
        'started': '[PythonBot] Version {version} started!\n',
        'overlay_positions': ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right'],
        'language': 'Language',
    }
}
current_lang = 'en'

# Overlay position: 0=TopLeft, 1=TopRight, 2=BottomLeft, 3=BottomRight
overlay_position = 1

# === COLOR TRIGGER DEFAULTS ===
color_r = 134
color_g = 94
color_b = 83

# === GUI ===
last_tab = "settings"
def create_gui():
    global debug_console, main_window, color_r, color_g, color_b, current_lang, overlay_position, current_theme, current_font_size, current_icon, last_tab
    lang = LANGUAGES[current_lang]
    theme = {
        'bg': '#181c23',
        'panel': '#232837',
        'accent': '#00bfff',
        'fg': '#e6eaf3',
        'button': '#232837',
        'button_active': '#00bfff',
        'button_fg': '#e6eaf3',
        'label': '#7a8597',
        'console': '#151822',
        'border': '#00bfff',
        'tab_bg': '#232837',
        'tab_active': '#181c23',
    }
    main_window = tk.Tk()
    main_window.title(f"PythonBot | {CURRENT_VERSION}")
    try:
        main_window.iconbitmap('icon.ico')
    except Exception as e:
        print(f'[Icon] Fehler beim Setzen des Icons: {e}')
    main_window.configure(bg=theme['bg'])
    main_window.geometry("520x520+100+100")
    main_window.resizable(False, False)
    main_window.overrideredirect(True)  # Custom Dragbar, kein Windows-Rahmen
    main_window.update_idletasks()
    # Runde Ecken für das Hauptfenster (optisch, per Layer)
    try:
        main_window.wm_attributes('-transparentcolor', '#123456')
    except:
        pass
    # Custom Drag Bar (runder, Glow)
    dragbar = tk.Frame(main_window, bg=theme['accent'], height=38, relief=tk.FLAT, bd=0, highlightthickness=0)
    dragbar.pack(fill=tk.X, side=tk.TOP)
    dragbar.config(cursor="fleur")
    dragbar_radius = tk.Frame(main_window, bg=theme['accent'], height=2, relief=tk.FLAT, bd=0, highlightthickness=0)
    dragbar_radius.pack(fill=tk.X, side=tk.TOP)
    dragbar.configure(highlightbackground=theme['accent'], highlightcolor=theme['accent'], highlightthickness=2)
    # Glow-Effekt für Dragbar
    dragbar.after(10, lambda: dragbar.config(bg=theme['accent']))
    # Drag-Events
    def start_move(event):
        main_window.x = event.x
        main_window.y = event.y
    def stop_move(event):
        main_window.x = None
        main_window.y = None
    def do_move(event):
        x = main_window.winfo_pointerx() - main_window.x
        y = main_window.winfo_pointery() - main_window.y
        main_window.geometry(f"+{x}+{y}")
    dragbar.bind('<Button-1>', start_move)
    dragbar.bind('<ButtonRelease-1>', stop_move)
    dragbar.bind('<B1-Motion>', do_move)
    # Close-Button
    close_btn = tk.Button(dragbar, text="✕", command=lambda: fade_out(main_window) or main_window.destroy(), bg=theme['accent'], fg=theme['bg'], bd=0, relief=tk.FLAT, font=("Segoe UI", 13, "bold"), activebackground=theme['button_active'], activeforeground=theme['bg'], highlightthickness=0, padx=8, pady=0, cursor="hand2")
    close_btn.pack(side=tk.RIGHT, padx=8, pady=0)
    close_btn.configure(borderwidth=0, highlightbackground=theme['accent'], highlightcolor=theme['accent'])
    close_btn.bind('<Enter>', lambda e: close_btn.config(bg='#0090c0'))
    close_btn.bind('<Leave>', lambda e: close_btn.config(bg=theme['accent']))

    # Runde Ecken für das Hauptfenster (optisch, per Canvas)
    try:
        main_window.wm_attributes('-transparentcolor', '#123456')
    except:
        pass

    # Subheader
    subheader = tk.Label(main_window, text=f"{ICONS[current_icon]} PythonBot", font=("Segoe UI", 13, "bold"), fg=theme['fg'], bg=theme['bg'])
    subheader.pack(pady=(10, 12))

    # Tabs (Settings, Overlay, Info) nur Icons, vertikal links, runder, Glow
    tab_frame = tk.Frame(main_window, bg=theme['bg'])
    tab_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
    tab_selected = tk.StringVar(value=last_tab)
    def switch_tab(tab):
        global last_tab
        last_tab = tab
        tab_selected.set(tab)
        # Sanfte Animation
        for f in [settings_tab, overlay_tab, info_tab]:
            f.place_forget()
        main_window.after(60, lambda: show_tab(tab))
    tab_icons = {"settings": "🎯", "overlay": "🖼️", "info": "ℹ️"}
    for tab in ["settings", "overlay", "info"]:
        btn = tk.Button(tab_frame, text=tab_icons[tab], command=lambda t=tab: switch_tab(t),
                        bg=theme['tab_active'] if tab_selected.get()==tab else theme['tab_bg'],
                        fg=theme['accent'] if tab_selected.get()==tab else theme['label'],
                        font=("Segoe UI", 18, "bold"), bd=0, relief=tk.FLAT, padx=12, pady=16, activebackground=theme['tab_active'], activeforeground=theme['accent'], anchor='center', justify='center', width=3, height=1)
        btn.pack(pady=10)
        btn.configure(borderwidth=0, highlightbackground=theme['accent'], highlightcolor=theme['accent'])
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#232f47'))
        btn.bind('<Leave>', lambda e, b=btn, t=tab: b.config(bg=theme['tab_active'] if tab_selected.get()==t else theme['tab_bg']))

    # Panel-Container (rechts neben Tabs), jetzt ohne Canvas/Kreis
    panel_frame = create_rounded_panel(main_window, 400, 440, theme['panel'], theme['border'])
    panel_frame.pack(padx=(0,18), pady=16, fill=tk.BOTH, expand=False, side=tk.LEFT)
    # Tab Content Frames werden direkt auf dem Frame platziert
    settings_tab = tk.Frame(panel_frame, bg=theme['panel'])
    overlay_tab = tk.Frame(panel_frame, bg=theme['panel'])
    info_tab = tk.Frame(panel_frame, bg=theme['panel'])
    tab_frames = {"settings": settings_tab, "overlay": overlay_tab, "info": info_tab}
    for f in tab_frames.values():
        f.place(relx=0, rely=0, relwidth=1, relheight=1)
    def show_tab(tab):
        for t, f in tab_frames.items():
            f.place_forget()
        tab_frames[tab].place(relx=0, rely=0, relwidth=1, relheight=1)
    show_tab(tab_selected.get())

    # SETTINGS TAB (rundere Entry, Buttons)
    tk.Label(settings_tab, text="General", font=("Segoe UI", 13, "bold"), fg=theme['accent'], bg=theme['panel']).pack(anchor='w', pady=(8,2), padx=12)
    # Theme
    tk.Label(settings_tab, text="Theme:", font=("Segoe UI", 10, "bold"), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(6,0))
    theme_frame = tk.Frame(settings_tab, bg=theme['panel'])
    theme_frame.pack(anchor='w', padx=18, pady=(0,4))
    for t, label in [("light", "Light"), ("dark", "Dark")]:
        tk.Button(theme_frame, text=label, command=lambda th=t: set_theme(th), bg=theme['tab_bg'], fg=theme['accent'] if current_theme==t else theme['label'], font=("Segoe UI", 10, "bold"), bd=0, relief=tk.FLAT, padx=10, pady=2, activebackground=theme['tab_active'], activeforeground=theme['accent']).pack(side=tk.LEFT, padx=2)
    # Schriftgröße
    tk.Label(settings_tab, text="Font size:", font=("Segoe UI", 10, "bold"), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(6,0))
    font_frame = tk.Frame(settings_tab, bg=theme['panel'])
    font_frame.pack(anchor='w', padx=18, pady=(0,4))
    for fs in FONT_SIZES:
        b = tk.Button(font_frame, text=str(fs), command=lambda s=fs: set_font_size(s), bg=theme['tab_bg'], fg=theme['accent'] if current_font_size==fs else theme['label'], font=("Segoe UI", 10, "bold"), bd=0, relief=tk.FLAT, padx=12, pady=8, activebackground=theme['tab_active'], activeforeground=theme['accent'])
        b.pack(side=tk.LEFT, padx=4)
        b.configure(borderwidth=0, highlightbackground=theme['accent'], highlightcolor=theme['accent'])
        b.bind('<Enter>', lambda e, b=b: b.config(bg='#232f47'))
        b.bind('<Leave>', lambda e, b=b: b.config(bg=theme['tab_bg']))
    # Icon
    tk.Label(settings_tab, text="Overlay Icon:", font=("Segoe UI", 10, "bold"), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(6,0))
    icon_frame = tk.Frame(settings_tab, bg=theme['panel'])
    icon_frame.pack(anchor='w', padx=18, pady=(0,4))
    for i, ic in enumerate(ICONS):
        tk.Button(icon_frame, text=ic, command=lambda idx=i: set_icon(idx), bg=theme['tab_bg'], fg=theme['accent'] if current_icon==i else theme['label'], font=("Segoe UI", 13), bd=0, relief=tk.FLAT, padx=6, pady=2, activebackground=theme['tab_active'], activeforeground=theme['accent']).pack(side=tk.LEFT, padx=1)
    # Hotkeys
    tk.Label(settings_tab, text="Hotkeys:", font=("Segoe UI", 10, "bold"), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(6,0))
    hotkey_frame = tk.Frame(settings_tab, bg=theme['panel'])
    hotkey_frame.pack(anchor='w', padx=18, pady=(0,4))
    tk.Label(hotkey_frame, text="Start/Stop:", font=("Segoe UI", 10), fg=theme['label'], bg=theme['panel']).pack(side=tk.LEFT)
    hotkey_var = tk.StringVar(value=HOTKEY_STARTSTOP)
    tk.Entry(hotkey_frame, textvariable=hotkey_var, width=10, font=("Segoe UI", 10), bg=theme['tab_bg'], fg=theme['fg'], bd=0, insertbackground=theme['accent']).pack(side=tk.LEFT, padx=4)
    tk.Label(hotkey_frame, text="Panic:", font=("Segoe UI", 10), fg=theme['label'], bg=theme['panel']).pack(side=tk.LEFT, padx=(10,0))
    panic_var = tk.StringVar(value=HOTKEY_PANIC)
    tk.Entry(hotkey_frame, textvariable=panic_var, width=10, font=("Segoe UI", 10), bg=theme['tab_bg'], fg=theme['fg'], bd=0, insertbackground=theme['accent']).pack(side=tk.LEFT, padx=4)
    # Schriftgröße, Icon, Theme, Sprache werden wie gehabt umgesetzt

    # OVERLAY TAB
    tk.Label(overlay_tab, text="Overlay Settings", font=("Segoe UI", 13, "bold"), fg=theme['accent'], bg=theme['panel']).pack(anchor='w', pady=(8,2), padx=12)
    # Overlay-Transparenz
    transparency_frame = tk.Frame(overlay_tab, bg=theme['panel'])
    transparency_frame.pack(anchor='w', padx=18, pady=(0,4))
    tk.Label(transparency_frame, text="Transparenz:", font=("Segoe UI", 10), fg=theme['label'], bg=theme['panel']).pack(side=tk.LEFT)
    transparency_var = tk.DoubleVar(value=0.9)
    def set_transparency(val):
        try:
            overlay_window.attributes("-alpha", float(val))
        except:
            pass
    tk.Scale(transparency_frame, from_=0.4, to=1.0, resolution=0.05, orient=tk.HORIZONTAL, variable=transparency_var, command=set_transparency, length=120, bg=theme['tab_bg'], fg=theme['accent'], highlightthickness=0, troughcolor=theme['panel']).pack(side=tk.LEFT, padx=8)
    # Overlay-Position
    tk.Label(overlay_tab, text="Position:", font=("Segoe UI", 10), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(6,0))
    overlay_var = tk.IntVar(value=overlay_position)
    def change_overlay_pos(*_):
        global overlay_position
        overlay_position = overlay_var.get()
        update_overlay()
    overlay_menu = tk.OptionMenu(overlay_tab, overlay_var, *list(range(4)), command=lambda _: change_overlay_pos())
    for i, pos in enumerate(lang['overlay_positions']):
        overlay_menu['menu'].entryconfig(i, label=pos)
    overlay_menu.config(bg=theme['tab_bg'], fg=theme['accent'], font=("Segoe UI", 10), bd=0, highlightthickness=0, activebackground=theme['tab_active'])
    overlay_menu.pack(anchor='w', padx=18, pady=(0,4))
    # Color Picker (rund)
    color_frame = tk.LabelFrame(overlay_tab, text=lang['color_trigger'], bg=theme['tab_bg'], fg=theme['accent'], font=("Segoe UI", 11, "bold"), bd=2, relief=tk.GROOVE, labelanchor='n')
    color_frame.pack(padx=18, pady=(0, 10), fill=tk.X)
    color_preview = tk.Label(color_frame, width=4, height=2, bg=f'#{color_r:02x}{color_g:02x}{color_b:02x}', relief=tk.SUNKEN, bd=2)
    color_preview.grid(row=0, column=0, padx=10, pady=8)
    color_label = tk.Label(color_frame, text=f"R>{color_r}  G<{color_g}  B<{color_b}", bg=theme['tab_bg'], fg=theme['fg'], font=("Consolas", 10, "bold"))
    color_label.grid(row=0, column=1, padx=10)
    def pick_color():
        global color_r, color_g, color_b
        rgb, hexcode = colorchooser.askcolor(title="Pick Color", initialcolor=(color_r, color_g, color_b))
        if rgb:
            color_r, color_g, color_b = int(rgb[0]), int(rgb[1]), int(rgb[2])
            color_preview.config(bg=f'#{color_r:02x}{color_g:02x}{color_b:02x}')
            color_label.config(text=f"R>{color_r}  G<{color_g}  B<{color_b}")
    pick_btn = tk.Button(color_frame, text=lang['pick_color'], command=pick_color, bg=theme['button'], fg=theme['fg'], font=("Segoe UI", 10, "bold"), relief=tk.RAISED, bd=2, activebackground=theme['button_active'], activeforeground=theme['fg'])
    pick_btn.grid(row=0, column=2, padx=10)

    # INFO TAB
    tk.Label(info_tab, text="Information", font=("Segoe UI", 13, "bold"), fg=theme['accent'], bg=theme['panel']).pack(anchor='w', pady=(8,2), padx=12)
    # FiveM Hinweis
    tk.Label(info_tab, text="Developer recommendation: Use with FiveM for best experience!", font=("Consolas", 10, "bold"), fg="#00bfff", bg=theme['panel']).pack(anchor='w', padx=18, pady=(0,4))
    tk.Label(info_tab, text=f"{lang['made_by']} | {CURRENT_VERSION}", font=("Consolas", 10, "italic"), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(0,4))
    tk.Label(info_tab, text=lang['overlay_info'], font=("Consolas", 10), fg=theme['label'], bg=theme['panel']).pack(anchor='w', padx=18, pady=(0,4))

    # Debug Console
    debug_console = scrolledtext.ScrolledText(info_tab, height=7, bg=theme['console'], fg=theme['fg'], font=("Consolas", current_font_size), insertbackground=theme['fg'], borderwidth=2, relief=tk.GROOVE, highlightthickness=1, highlightbackground=theme['accent'])
    debug_console.pack(padx=18, pady=8, fill=tk.BOTH, expand=True)
    debug_console.insert(tk.END, lang['started'].format(version=CURRENT_VERSION))
    debug_console.config(state=tk.DISABLED)
    def safe_insert(msg):
        debug_console.config(state=tk.NORMAL)
        debug_console.insert(tk.END, msg)
        debug_console.see(tk.END)
        debug_console.config(state=tk.DISABLED)
    global safe_insert_to_console
    safe_insert_to_console = safe_insert

    try:
        create_overlay()
    except Exception as e:
        print(f"[ERROR] create_overlay: {e}")
        safe_insert(f"[ERROR] Overlay: {e}\n")
    fade_in(main_window, speed=0.01)

def create_rounded_panel(parent, width, height, bg, border_color, radius=32, border=3, glow=True):
    # Panel-Container ohne Kreis und Glow
    frame = tk.Frame(parent, width=width, height=height, bg=bg, bd=0, highlightthickness=0)
    return frame

# === ANIMATION ===
def fade_in(window, speed=0.02):
    for i in range(0, 11):
        window.attributes("-alpha", i / 10)
        window.update()
        time.sleep(speed)

def fade_out(window, speed=0.02):
    for i in range(10, -1, -1):
        window.attributes("-alpha", i / 10)
        window.update()
        time.sleep(speed)

# === CORE FEATURES ===
def toggle_script():
    global toggle
    toggle = not toggle
    main_window.after(0, update_overlay)
    if 'safe_insert_to_console' in globals():
        safe_insert_to_console(f"[TOGGLE] TriggerBot ist jetzt {'AKTIV' if toggle else 'INAKTIV'}\n")
    else:
        debug_console.insert(tk.END, f"[TOGGLE] TriggerBot ist jetzt {'AKTIV' if toggle else 'INAKTIV'}\n")
        debug_console.see(tk.END)

def panic():
    os._exit(0)

def triggerbot_loop():
    global color_r, color_g, color_b
    while True:
        if toggle:
            x, y = pyautogui.size()
            cx, cy = x // 2, y // 2
            holding = False
            while toggle:
                img = ImageGrab.grab(bbox=(cx - 3, cy - 3, cx + 4, cy + 4))
                found = False
                for px in range(3):
                    for py in range(3):
                        r, g, b = img.getpixel((px, py))
                        if r > color_r and g < color_g and b < color_b:
                            found = True
                            break
                    if found:
                        break
                if found:
                    if not holding:
                        pyautogui.mouseDown()
                        holding = True
                else:
                    if holding:
                        pyautogui.mouseUp()
                        holding = False
                time.sleep(0.001)
            if holding:
                pyautogui.mouseUp()
        time.sleep(0.01)

def create_overlay():
    global overlay_window, overlay_label
    if overlay_window is not None:
        try:
            overlay_window.destroy()
        except:
            pass
    overlay_window = tk.Toplevel(main_window)
    overlay_window.overrideredirect(True)
    overlay_window.attributes("-topmost", True)
    overlay_window.attributes("-alpha", 0.9)
    overlay_window.configure(bg="black")
    # Overlay-Label ohne Rand
    overlay_label = tk.Label(overlay_window, text=f"{ICONS[current_icon]} [INACTIVE] | PythonBot | {CURRENT_VERSION}", bg="black", fg="red", font=("Consolas", 11, "bold"))
    overlay_label.pack(padx=12, pady=7)
    overlay_label.after(10, lambda: overlay_label.config(bg="black"))
    # Position wählbar
    screen_width = overlay_window.winfo_screenwidth()
    screen_height = overlay_window.winfo_screenheight()
    overlay_window.update_idletasks()
    width = overlay_label.winfo_reqwidth() + 20
    height = overlay_label.winfo_reqheight() + 10
    positions = [
        (10, 10),  # Top Left
        (screen_width - width - 10, 10),  # Top Right
        (10, screen_height - height - 40),  # Bottom Left
        (screen_width - width - 10, screen_height - height - 40)  # Bottom Right
    ]
    x, y = positions[overlay_position]
    overlay_window.geometry(f"{width}x{height}+{x}+{y}")
    update_overlay()

def set_font_size(size):
    global current_font_size
    current_font_size = size
    main_window.destroy(); create_gui()

def set_icon(idx):
    global current_icon
    current_icon = idx
    main_window.destroy(); create_gui()

def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    main_window.destroy()
    create_gui()

def animate_overlay():
    if overlay_label:
        orig = overlay_label.cget('fg')
        overlay_label.config(fg='yellow')
        overlay_label.after(120, lambda: overlay_label.config(fg=orig))

def update_overlay():
    global overlay_label, overlay_window
    if overlay_label is None or overlay_window is None:
        print("[DEBUG] overlay_label or overlay_window is None in update_overlay")
        return
    status = "[ACTIVE]" if toggle else "[INACTIVE]"
    overlay_label.config(text=f"{ICONS[current_icon]} {status} | PythonBot | {CURRENT_VERSION}", fg="lime" if toggle else "red")
    animate_overlay()
    # Overlay-Position neu setzen
    overlay_window.update_idletasks()
    width = overlay_label.winfo_reqwidth() + 20
    height = overlay_label.winfo_reqheight() + 10
    screen_width = overlay_window.winfo_screenwidth()
    screen_height = overlay_window.winfo_screenheight()
    positions = [
        (10, 10),  # Top Left
        (screen_width - width - 10, 10),  # Top Right
        (10, screen_height - height - 40),  # Bottom Left
        (screen_width - width - 10, screen_height - height - 40)  # Bottom Right
    ]
    x, y = positions[overlay_position]
    overlay_window.geometry(f"{width}x{height}+{x}+{y}")

# === NEUE FEATURES ===
def show_about():
    lang = LANGUAGES[current_lang]
    theme = THEMES[current_theme]
    about = tk.Toplevel(main_window)
    about.title("About")
    about.geometry("350x220+180+180")
    about.configure(bg=theme['bg'])
    about.resizable(False, False)
    tk.Label(about, text=f"PythonBot {CURRENT_VERSION}", font=("Arial", 14, "bold"), fg=theme['fg'], bg=theme['bg']).pack(pady=8)
    tk.Label(about, text="Open Source Overlay for comfort & accessibility\nGitHub: ljas-vu/triggerbot-gui", fg=theme['fg'], bg=theme['bg'], font=("Arial", 10)).pack(pady=2)
    tk.Label(about, text="Features:\n- Overlay transparency\n- Custom hotkeys\n- Themes & font size\n- Overlay icon\n- Overlay animation\n- Changelog dialog", fg=theme['label'], bg=theme['bg'], font=("Arial", 10)).pack(pady=4)
    tk.Button(about, text="OK", command=about.destroy, bg=theme['button'], fg=theme['bg'], font=("Arial", 11, "bold"), relief="flat").pack(pady=10)

# === AUTO-UPDATER ===
import sys
import requests
import shutil
import tempfile
import tkinter.messagebox

def auto_update():
    try:
        url = "https://raw.githubusercontent.com/ljas-vu/triggerbot-gui/main/version.txt"
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            latest = r.text.strip()
            if latest != CURRENT_VERSION:
                answer = tkinter.messagebox.askyesno("Update verfügbar", f"Neue Version: {latest}\nJetzt automatisch herunterladen und neustarten?")
                if answer:
                    py_url = "https://raw.githubusercontent.com/ljas-vu/triggerbot-gui/main/main.py"
                    py_r = requests.get(py_url, timeout=5)
                    if py_r.status_code == 200:
                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
                        tmp.write(py_r.content)
                        tmp.close()
                        shutil.copy(tmp.name, sys.argv[0])
                        tkinter.messagebox.showinfo("Update", "Update abgeschlossen! Das Programm wird neu gestartet.")
                        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"[Updater] Fehler: {e}")

def sync_website_version():
    # Synchronize version with website
    try:
        html_path = r'c:\Users\LVerm\Desktop\multiplayer\triggerbot_gui.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        # Version ersetzen
        import re
        html = re.sub(r'(Version:?\s*v?)[0-9]+\.[0-9]+', f'\\1{CURRENT_VERSION}', html)
        # Sprache entfernen (nur Englisch)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
    except Exception as e:
        print(f'[Website Sync] Fehler: {e}')

def verify_code():
    """
    Generiert den aktuellen Verification-Code wie auf der Website und fordert den Benutzer auf,
    diesen einzugeben, bevor die GUI startet.
    """
    import tkinter.simpledialog
    import tkinter.messagebox
    import tkinter as tk
    import math
    import time

    def generate_verification_code():
        now = int(time.time())
        interval = 30
        seed = now // interval
        x = math.sin(seed) * 10000
        code = int((x - math.floor(x)) * 10000)
        return str(code).zfill(4)

    while True:
        code = generate_verification_code()
        root = tk.Tk()
        root.withdraw()
        user_code = tkinter.simpledialog.askstring(
            "Verification",
            f"Enter the 4-digit verification code from the website:\n{CODE_URL}",
            parent=root
        )
        root.destroy()
        if user_code is None:
            exit()
        if user_code.strip() == code:
            print("[Verification] Code korrekt.")
            break
        else:
            tk.Tk().withdraw()
            tkinter.messagebox.showerror("Verification", "Incorrect code. Please try again.")

# === START ===
toggle = False
overlay_window = None
overlay_label = None

if __name__ == "__main__":
    verify_code()  # Benutzer muss Code eingeben, bevor GUI startet
    auto_update()  # Auto-Updater beim Start
    create_gui()
    # Hotkeys jetzt über main_window.bind, damit im Main-Thread:
    main_window.bind('<F5>', lambda event: toggle_script())
    main_window.bind('<Control-F4>', lambda event: panic())
    threading.Thread(target=triggerbot_loop, daemon=True).start()

    main_window.mainloop()

# === HINWEIS FÜR EXE-ERSTELLUNG ===
# Um eine EXE zu erstellen, führe im Terminal (im Projektordner) aus:
# pyinstaller --onefile --noconsole --icon=icon.ico main.py
# Die fertige EXE liegt dann im dist/ Ordner.
