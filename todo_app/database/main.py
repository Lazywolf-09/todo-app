import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window

# Set the window icon
Window.icon = "icons/app_icon.png"

# Database Functions
def fetch_tasks():
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, due_date, reminder_set, reminder_time, status FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title, description, due_date, reminder_set, reminder_time):
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, due_date, reminder_set, reminder_time, status) VALUES (?, ?, ?, ?, ?, 'Pending')", 
                   (title, description, due_date, reminder_set, reminder_time))
    conn.commit()
    conn.close()

def add_note_to_db(title, content):
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, datetime('now'))", 
                   (title, content))
    conn.commit()
    conn.close()

# Task List UI
class TaskList(BoxLayout):
    def __init__(self, **kwargs):
        super(TaskList, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.update_task_list()

    def update_task_list(self):
        self.clear_widgets()
        tasks = fetch_tasks()
        for task in tasks:
            task_label = Label(text=f"{task[1]} - Due: {task[3]} - Status: {task[6]}")
            self.add_widget(task_label)

# Add Task Popup
class AddTaskPopup(Popup):
    def __init__(self, **kwargs):
        super(AddTaskPopup, self).__init__(**kwargs)
        self.title = "Add Task"
        self.size_hint = (0.8, 0.8)
        self.content = FloatLayout()

        self.title_input = TextInput(hint_text="Task Title", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "top": 0.9})
        self.description_input = TextInput(hint_text="Description", size_hint=(0.8, 0.2), pos_hint={"x": 0.1, "top": 0.75})
        self.due_date_input = TextInput(hint_text="Due Date (YYYY-MM-DD)", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "top": 0.5})
        self.reminder_input = TextInput(hint_text="Reminder Time (YYYY-MM-DD HH:MM:SS)", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "top": 0.35})

        save_button = Button(text="Save", size_hint=(0.4, 0.1), pos_hint={"x": 0.3, "top": 0.2})
        save_button.bind(on_release=self.save_task)

        self.content.add_widget(self.title_input)
        self.content.add_widget(self.description_input)
        self.content.add_widget(self.due_date_input)
        self.content.add_widget(self.reminder_input)
        self.content.add_widget(save_button)

    def save_task(self, instance):
        title = self.title_input.text
        description = self.description_input.text
        due_date = self.due_date_input.text
        reminder_time = self.reminder_input.text
        reminder_set = 1 if reminder_time else 0

        add_task(title, description, due_date, reminder_set, reminder_time)
        self.dismiss()

# Add Note Popup
class AddNotePopup(Popup):
    def __init__(self, **kwargs):
        super(AddNotePopup, self).__init__(**kwargs)
        self.title = "Add Note"
        self.size_hint = (0.8, 0.8)
        self.content = FloatLayout()

        self.title_input = TextInput(hint_text="Note Title", size_hint=(0.8, 0.1), pos_hint={"x": 0.1, "top": 0.9})
        self.content_input = TextInput(hint_text="Note Content", size_hint=(0.8, 0.5), pos_hint={"x": 0.1, "top": 0.75})

        save_button = Button(text="Save", size_hint=(0.4, 0.1), pos_hint={"x": 0.3, "top": 0.2})
        save_button.bind(on_release=self.save_note)

        self.content.add_widget(self.title_input)
        self.content.add_widget(self.content_input)
        self.content.add_widget(save_button)

    def save_note(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        add_note_to_db(title, content)
        self.dismiss()

# Main App
class MyApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        # App Icon at the top
        app_icon = Image(source='icons/app_icon.png', size_hint=(0.3, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.9})
        root.add_widget(app_icon)

        # Task List
        self.task_list = TaskList(size_hint=(1, 0.5))
        root.add_widget(self.task_list)

        # Add Task and Add Note Buttons
        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        add_task_button = Button(
            background_normal='icons/add_task_icon.png',
            size_hint=(None, None),
            size=(50, 50)
        )
        add_task_button.bind(on_release=self.open_add_task_popup)

        add_note_button = Button(
            background_normal='icons/add_note_icon.png',
            size_hint=(None, None),
            size=(50, 50)
        )
        add_note_button.bind(on_release=self.open_add_note_popup)

        buttons_layout.add_widget(add_task_button)
        buttons_layout.add_widget(add_note_button)

        root.add_widget(buttons_layout)

        return root

    def open_add_task_popup(self, instance):
        popup = AddTaskPopup()
        popup.open()

    def open_add_note_popup(self, instance):
        popup = AddNotePopup()
        popup.open()

if __name__ == "__main__":
    MyApp().run()
