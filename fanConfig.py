import tkinter as tk
from pathlib import Path

root = tk.Tk()
root.title("PiBreeze")
root.geometry("580x720")
root.configure(bg="#0D1117")
root.resizable(False, False)

# --------------------------------------------------
# Colors
# --------------------------------------------------
BG = "#0D1117"
CARD = "#161B22"
METRIC_BG = "#21262D"
ACCENT = "#3FB950"
ACCENT_DIM = "#238636"
WARNING = "#D29922"
DANGER = "#F85149"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
BORDER = "#30363D"
BUTTON_SECONDARY = "#30363D"

# --------------------------------------------------
# Hardware paths
# --------------------------------------------------
FAN_PATH = Path("/sys/class/hwmon/hwmon2")
PWM_PATH = FAN_PATH / "pwm1"
MODE_PATH = FAN_PATH / "pwm1_enable"
RPM_PATH = FAN_PATH / "fan1_input"
TEMP_PATH = Path("/sys/class/thermal/thermal_zone0/temp")
CLOCK_PATH = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")

current_mode = None

# --------------------------------------------------
# Hardware helpers
# --------------------------------------------------
def read_sensor(path):
    try:
        return int(path.read_text().strip())
    except (OSError, ValueError):
        return None


def write_sensor(path, value):
    path.write_text(str(value))


def get_cpu_clock():
    value = read_sensor(CLOCK_PATH)
    return value / 1000 if value is not None else None


def get_cpu_temperature():
    value = read_sensor(TEMP_PATH)
    return value / 1000 if value is not None else None


def get_fan_rpm():
    return read_sensor(RPM_PATH)


def get_pwm():
    return read_sensor(PWM_PATH)


def get_fan_mode():
    return read_sensor(MODE_PATH)


# --------------------------------------------------
# Fan control
# --------------------------------------------------
def set_auto_mode():
    global current_mode
    try:
        write_sensor(MODE_PATH, 2)
        current_mode = "AUTO"
        slider.configure(state="disabled")
        apply_button.configure(state="disabled")
        control_mode_label.config(text="● AUTO", fg=ACCENT)
        speed_label.config(text="Automatic")
        auto_button.configure(bg=ACCENT, fg=BG)
        manual_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
    except OSError as error:
        show_error(error)


def set_manual_mode():
    global current_mode
    try:
        write_sensor(MODE_PATH, 1)
        current_mode = "MANUAL"
        slider.configure(state="normal")
        apply_button.configure(state="normal")
        control_mode_label.config(text="● MANUAL", fg=WARNING)
        auto_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
        manual_button.configure(bg=ACCENT, fg=BG)
    except OSError as error:
        show_error(error)


def update_speed(value):
    speed = int(float(value))
    speed_label.config(text=f"{speed}%")


def apply_speed():
    if current_mode != "MANUAL":
        return
    try:
        selected_speed = slider.get()
        pwm_value = round(selected_speed * 255 / 100)
        write_sensor(PWM_PATH, pwm_value)
        speed_label.config(text=f"{selected_speed}%")
    except OSError as error:
        show_error(error)


def show_error(error):
    fan_status_label.config(text=f"● ERROR: {error}", fg=DANGER)


# --------------------------------------------------
# Menu
# --------------------------------------------------
menu = tk.Menu(root, bg=CARD, fg=TEXT, activebackground=ACCENT,
               activeforeground=BG, borderwidth=0, font=("Segoe UI", 10))
root.config(menu=menu)

filemenu = tk.Menu(menu, tearoff=0, bg=CARD, fg=TEXT,
                   activebackground=ACCENT, activeforeground=BG)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Refresh", command=lambda: refresh_metrics())
filemenu.add_separator()
filemenu.add_command(label="Exit", command=lambda: on_close())

# --------------------------------------------------
# Layout
# --------------------------------------------------
main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=22, pady=18)

# Header
header = tk.Frame(main, bg=BG)
header.pack(fill="x", pady=(0, 16))

tk.Label(header, text="PiBreeze", font=("Segoe UI", 22, "bold"),
         bg=BG, fg=TEXT).pack(side="left")

tk.Label(header, text="Raspberry Pi 5 Cooling", font=("Segoe UI", 10),
         bg=BG, fg=MUTED).pack(side="left", padx=(10, 0), pady=(8, 0))

# Main card
card = tk.Frame(main, bg=CARD, padx=18, pady=16,
                highlightthickness=1, highlightbackground=BORDER)
card.pack(fill="x")

# ---- System Monitor ----
tk.Label(card, text="SYSTEM STATUS", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 12))

# Status rows
status_frame = tk.Frame(card, bg=CARD)
status_frame.pack(fill="x", pady=(0, 14))

# Fan status
status_row = tk.Frame(status_frame, bg=CARD)
status_row.pack(fill="x", pady=(0, 6))
tk.Label(status_row, text="Fan", font=("Segoe UI", 10),
         bg=CARD, fg=TEXT).pack(side="left")
fan_status_label = tk.Label(status_row, text="● CHECKING",
                            font=("Segoe UI", 10, "bold"), bg=CARD, fg=MUTED)
fan_status_label.pack(side="right")

# Control mode
mode_row = tk.Frame(status_frame, bg=CARD)
mode_row.pack(fill="x")
tk.Label(mode_row, text="Mode", font=("Segoe UI", 10),
         bg=CARD, fg=TEXT).pack(side="left")
control_mode_label = tk.Label(mode_row, text="● CHECKING",
                              font=("Segoe UI", 10, "bold"), bg=CARD, fg=MUTED)
control_mode_label.pack(side="right")

# Metrics
metrics = tk.Frame(card, bg=CARD)
metrics.pack(fill="x", pady=(4, 16))


def create_metric(parent, title):
    frame = tk.Frame(parent, bg=METRIC_BG, padx=12, pady=12)
    frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

    tk.Label(frame, text=title, font=("Segoe UI", 8, "bold"),
             bg=METRIC_BG, fg=MUTED).pack(anchor="w")

    value_label = tk.Label(frame, text="--", font=("Segoe UI", 18, "bold"),
                           bg=METRIC_BG, fg=TEXT)
    value_label.pack(anchor="w", pady=(4, 0))

    unit_label = tk.Label(frame, text="", font=("Segoe UI", 9),
                          bg=METRIC_BG, fg=MUTED)
    unit_label.pack(anchor="w")

    return value_label, unit_label


temp_label, temp_unit = create_metric(metrics, "CPU TEMP")
temp_unit.config(text="°C")

clock_label, clock_unit = create_metric(metrics, "CPU CLOCK")
clock_unit.config(text="MHz")

fan_label, fan_unit = create_metric(metrics, "FAN SPEED")
fan_unit.config(text="RPM")

# Remove last metric's right padding
for child in metrics.winfo_children():
    child.pack_configure(padx=(0, 8))
metrics.winfo_children()[-1].pack_configure(padx=(0, 0))

# Divider
tk.Frame(card, bg=BORDER, height=1).pack(fill="x", pady=(2, 16))

# ---- Fan Control ----
tk.Label(card, text="FAN CONTROL", font=("Segoe UI", 9, "bold"),
         bg=CARD, fg=MUTED).pack(anchor="w")

# Speed display
speed_row = tk.Frame(card, bg=CARD)
speed_row.pack(fill="x", pady=(12, 4))

tk.Label(speed_row, text="Target Speed", font=("Segoe UI", 11),
         bg=CARD, fg=TEXT).pack(side="left")

speed_label = tk.Label(speed_row, text="--%", font=("Segoe UI", 18, "bold"),
                       bg=CARD, fg=ACCENT)
speed_label.pack(side="right")

# Slider
slider = tk.Scale(
    card, from_=0, to=100, orient="horizontal",
    command=update_speed, bg=CARD, fg=TEXT,
    troughcolor=BORDER, activebackground=ACCENT,
    highlightthickness=0, borderwidth=0, sliderrelief="flat",
    showvalue=False, length=300, state="disabled"
)
slider.set(50)
slider.pack(fill="x", pady=(4, 2))

# Scale labels
scale_labels = tk.Frame(card, bg=CARD)
scale_labels.pack(fill="x", pady=(0, 10))
tk.Label(scale_labels, text="0%  Off", font=("Segoe UI", 8),
         bg=CARD, fg=MUTED).pack(side="left")
tk.Label(scale_labels, text="100%  Max", font=("Segoe UI", 8),
         bg=CARD, fg=MUTED).pack(side="right")

# Apply button
apply_button = tk.Button(
    card, text="Apply Speed", font=("Segoe UI", 10, "bold"),
    bg=ACCENT, fg=BG, activebackground=ACCENT_DIM, activeforeground=BG,
    relief="flat", cursor="hand2", pady=9, state="disabled",
    command=apply_speed
)
apply_button.pack(fill="x", pady=(4, 12))

# Mode buttons
button_row = tk.Frame(card, bg=CARD)
button_row.pack(fill="x")

auto_button = tk.Button(
    button_row, text="AUTO MODE", font=("Segoe UI", 10, "bold"),
    bg=ACCENT, fg=BG, activebackground=ACCENT_DIM, relief="flat",
    cursor="hand2", pady=9, command=set_auto_mode
)
auto_button.pack(side="left", expand=True, fill="x", padx=(0, 6))

manual_button = tk.Button(
    button_row, text="MANUAL MODE", font=("Segoe UI", 10, "bold"),
    bg=BUTTON_SECONDARY, fg=TEXT, activebackground="#484F58",
    relief="flat", cursor="hand2", pady=9, command=set_manual_mode
)
manual_button.pack(side="left", expand=True, fill="x", padx=(6, 0))

# --------------------------------------------------
# Monitoring loop
# --------------------------------------------------
def refresh_metrics():
    temperature = get_cpu_temperature()
    clock = get_cpu_clock()
    rpm = get_fan_rpm()
    mode = get_fan_mode()
    pwm = get_pwm()

    # Temperature with color coding
    if temperature is not None:
        temp_label.config(text=f"{temperature:.1f}")
        if temperature >= 75:
            temp_label.config(fg=DANGER)
        elif temperature >= 60:
            temp_label.config(fg=WARNING)
        else:
            temp_label.config(fg=ACCENT)
    else:
        temp_label.config(text="--", fg=TEXT)

    # Clock
    clock_label.config(
        text=f"{clock:.0f}" if clock is not None else "--"
    )

    # Fan RPM
    fan_label.config(
        text=f"{rpm:,}" if rpm is not None else "--"
    )

    # Fan status
    if rpm is None:
        fan_status_label.config(text="● UNAVAILABLE", fg=MUTED)
    elif rpm > 0:
        fan_status_label.config(text="● RUNNING", fg=ACCENT)
    else:
        fan_status_label.config(text="● STOPPED", fg=WARNING)

    # Hardware mode sync
    if mode == 2:
        control_mode_label.config(text="● AUTO", fg=ACCENT)
        slider.configure(state="disabled")
        apply_button.configure(state="disabled")
        auto_button.configure(bg=ACCENT, fg=BG)
        manual_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
        if current_mode != "MANUAL":
            speed_label.config(text="Automatic")
    elif mode == 1:
        control_mode_label.config(text="● MANUAL", fg=WARNING)
        slider.configure(state="normal")
        apply_button.configure(state="normal")
        auto_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
        manual_button.configure(bg=ACCENT, fg=BG)
        if pwm is not None:
            speed_label.config(text=f"{round(pwm * 100 / 255)}%")
    else:
        control_mode_label.config(text="● DISABLED", fg=DANGER)
        slider.configure(state="disabled")
        apply_button.configure(state="disabled")

    root.after(1000, refresh_metrics)


# --------------------------------------------------
# Exit handling
# --------------------------------------------------
def on_close():
    try:
        write_sensor(MODE_PATH, 2)
        print("Automatic fan control restored.")
    except OSError as error:
        print("Could not restore automatic mode:", error)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

# --------------------------------------------------
# Startup
# --------------------------------------------------
def initialize_fan():
    global current_mode
    mode = get_fan_mode()
    pwm = get_pwm()

    if mode == 2:
        current_mode = "AUTO"
        slider.configure(state="disabled")
        apply_button.configure(state="disabled")
        speed_label.config(text="Automatic")
        auto_button.configure(bg=ACCENT, fg=BG)
        manual_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
    elif mode == 1:
        current_mode = "MANUAL"
        slider.configure(state="normal")
        apply_button.configure(state="normal")
        auto_button.configure(bg=BUTTON_SECONDARY, fg=TEXT)
        manual_button.configure(bg=ACCENT, fg=BG)
        if pwm is not None:
            slider.set(round(pwm * 100 / 255))
    else:
        current_mode = "UNKNOWN"
        slider.configure(state="disabled")
        apply_button.configure(state="disabled")


initialize_fan()
refresh_metrics()
root.mainloop()
