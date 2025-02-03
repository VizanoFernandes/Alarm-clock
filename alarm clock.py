from tkinter import *
from tkinter import messagebox
import datetime
import time
import threading

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("400x450")
        
        self.alarms = []  # List to store alarm times and their statuses

        # Add Alarm Section
        Label(root, text="Set Alarm (12-hour format):", font=("Arial", 12)).pack(pady=10)
        self.hour = StringVar()
        self.minute = StringVar()
        self.second = StringVar()
        self.period = StringVar(value="AM")
        
        frame = Frame(root)
        frame.pack(pady=5)
        Entry(frame, textvariable=self.hour, width=5).pack(side=LEFT, padx=5)
        Label(frame, text=":").pack(side=LEFT)
        Entry(frame, textvariable=self.minute, width=5).pack(side=LEFT, padx=5)
        Label(frame, text=":").pack(side=LEFT)
        Entry(frame, textvariable=self.second, width=5).pack(side=LEFT, padx=5)
        
        OptionMenu(frame, self.period, "AM", "PM").pack(side=LEFT, padx=5)
        
        Button(root, text="Add Alarm", command=self.add_alarm).pack(pady=10)

        # Alarms List Section
        Label(root, text="Set Alarms:", font=("Arial", 12)).pack(pady=10)
        self.alarms_frame = Frame(root)
        self.alarms_frame.pack()

        self.update_alarm_list()

    def add_alarm(self):
        hour = self.hour.get()
        minute = self.minute.get()
        second = self.second.get()
        period = self.period.get()

        if not (hour.isdigit() and minute.isdigit() and second.isdigit()):
            messagebox.showerror("Invalid Input", "Please enter valid numbers for the time.")
            return

        hour = int(hour)
        if hour < 1 or hour > 12:
            messagebox.showerror("Invalid Input", "Hour must be between 1 and 12.")
            return

        time_string = f"{str(hour).zfill(2)}:{minute.zfill(2)}:{second.zfill(2)} {period}"
        self.alarms.append({"time": time_string, "enabled": True})
        self.update_alarm_list()

        # Start the alarm thread
        threading.Thread(target=self.check_alarm, daemon=True).start()

    def update_alarm_list(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()

        for i, alarm in enumerate(self.alarms):
            frame = Frame(self.alarms_frame)
            frame.pack(fill=X, pady=2)

            Label(frame, text=alarm["time"], font=("Arial", 10)).pack(side=LEFT, padx=10)
            
            toggle_button = Button(frame, text="On" if alarm["enabled"] else "Off", width=5,
                                   command=lambda i=i: self.toggle_alarm(i))
            toggle_button.pack(side=LEFT, padx=10)
            
            Button(frame, text="Delete", command=lambda i=i: self.delete_alarm(i)).pack(side=LEFT, padx=10)

    def toggle_alarm(self, index):
        self.alarms[index]["enabled"] = not self.alarms[index]["enabled"]
        self.update_alarm_list()

    def delete_alarm(self, index):
        del self.alarms[index]
        self.update_alarm_list()

    def check_alarm(self):
        while True:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            for alarm in self.alarms:
                if alarm["time"] == current_time and alarm["enabled"]:
                    messagebox.showinfo("Alarm", f"Time to wake up! ({alarm['time']})")
                    alarm["enabled"] = False  # Disable the alarm after it rings
                    self.update_alarm_list()
            time.sleep(1)

if __name__ == "__main__":
    root = Tk()
    app = AlarmClockApp(root)
    root.mainloop()
