#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tkinter as tk
import cv2
import threading



# Global variable to keep track of whether the video is running
video_running = False

# Global variable for the virtual classroom
classrooms = {}

class Classroom:
    def __init__(self, name):
        self.name = name
        self.participants = []
        self.messages = []

    def add_participant(self, participant):
        self.participants.append(participant)

    def remove_participant(self, participant):
        self.participants.remove(participant)

    def send_message(self, sender, message):
        self.messages.append(f"{sender}: {message}")

    def get_messages(self):
        return self.messages

# Function to start video capture
def start_video():
    global video_running
    video_running = True

    def capture_video():
        cap = cv2.VideoCapture(0)

        while video_running:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    video_thread = threading.Thread(target=capture_video)
    video_thread.start()

# Function to stop video capture
def stop_video():
    global video_running
    video_running = False

# Function to handle chat messages
def send_message():
    message = entry.get()
    chat_text.insert(tk.END, "You: " + message + "\n")
    entry.delete(0, tk.END)

# Function to create a classroom
def create_classroom():
    name = classroom_name.get()
    if name not in classrooms:
        classrooms[name] = Classroom(name)
        chat_text.insert(tk.END, f"Classroom '{name}' created.\n")
    else:
        chat_text.insert(tk.END, f"Classroom '{name}' already exists.\n")

# Function to join a classroom
def join_classroom():
    name = classroom_to_join.get()
    participant = participant_name.get()
    if name in classrooms:
        classroom = classrooms[name]
        classroom.add_participant(participant)
        chat_text.insert(tk.END, f"{participant} joined '{name}' classroom.\n")
    else:
        chat_text.insert(tk.END, f"Classroom '{name}' does not exist.\n")

# Function to leave a classroom
def leave_classroom():
    participant = leave_participant_name.get()
    for classroom in classrooms.values():
        if participant in classroom.participants:
            classroom.remove_participant(participant)
            chat_text.insert(tk.END, f"{participant} left '{classroom.name}' classroom.\n")
            return
    chat_text.insert(tk.END, f"{participant} is not in any classroom.\n")

# Function for the login mechanism
def login():
    username = username_entry.get()
    password = password_entry.get()

    # You can add more users and passwords as needed
    users = {"user1": "password1", "user2": "password2"}

    if username in users and users[username] == password:
        login_window.destroy()
        print("Login successful. Welcome, " + username + "!")
    else:
        login_status.config(text="Invalid username or password. Please try again.")
login_window = tk.Tk()
login_window.title("Login")

username_label = tk.Label(login_window, text="Username:")
username_label.pack()

username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()

password_entry = tk.Entry(login_window, show="*")  # Mask the password
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

login_status = tk.Label(login_window, text="")
login_status.pack()

login_window.mainloop()

# Create the main window
root = tk.Tk()
root.title("Virtual Classroom")

# Create and configure the video frame
video_frame = tk.Frame(root)
video_frame.pack(side=tk.LEFT, padx=10, pady=10)
start_button = tk.Button(video_frame, text="Start Video", command=start_video)
start_button.pack()
stop_button = tk.Button(video_frame, text="Stop Video", command=stop_video)
stop_button.pack()

# Create and configure the chat frame
chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.RIGHT, padx=10, pady=10)
chat_text = tk.Text(chat_frame, height=20, width=30)
chat_text.pack()
entry = tk.Entry(chat_frame, width=30)
entry.pack()
send_button = tk.Button(chat_frame, text="Send", command=send_message)
send_button.pack()

# Create and configure the virtual classroom frame
classroom_frame = tk.Frame(root)
classroom_frame.pack(side=tk.RIGHT, padx=10, pady=10)
classroom_label = tk.Label(classroom_frame, text="Virtual Classroom")
classroom_label.pack()
classroom_name_label = tk.Label(classroom_frame, text="Classroom Name:")
classroom_name_label.pack()
classroom_name = tk.StringVar()
classroom_name_entry = tk.Entry(classroom_frame, textvariable=classroom_name)
classroom_name_entry.pack()
create_button = tk.Button(classroom_frame, text="Create Classroom", command=create_classroom)
create_button.pack()
join_label = tk.Label(classroom_frame, text="Join Classroom:")
join_label.pack()
classroom_to_join = tk.StringVar()
classroom_to_join_entry = tk.Entry(classroom_frame, textvariable=classroom_to_join)
classroom_to_join_entry.pack()
participant_name_label = tk.Label(classroom_frame, text="Participant Name:")
participant_name_label.pack()
participant_name = tk.StringVar()
participant_name_entry = tk.Entry(classroom_frame, textvariable=participant_name)
participant_name_entry.pack()
join_button = tk.Button(classroom_frame, text="Join Classroom", command=join_classroom)
join_button.pack()

# Create and configure the leave classroom frame
leave_frame = tk.Frame(root)
leave_frame.pack(side=tk.RIGHT, padx=10, pady=10)
leave_label = tk.Label(leave_frame, text="Leave Classroom")
leave_label.pack()
leave_participant_name_label = tk.Label(leave_frame, text="Participant Name:")
leave_participant_name_label.pack()
leave_participant_name = tk.StringVar()
leave_participant_name_entry = tk.Entry(leave_frame, textvariable=leave_participant_name)
leave_participant_name_entry.pack()
leave_button = tk.Button(leave_frame, text="Leave Classroom", command=leave_classroom)
leave_button.pack()


root.mainloop()

