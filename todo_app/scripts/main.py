import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

import sqlite3

kivy.require('2.3.0')

# Database functions
def fetch_tasks():
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task_to_db(task_name, task_due_date):
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, task_due_date) VALUES (?, ?)", (task_name, task_due_date))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def update_task_in_db(task_id, new_task_name, new_task_due_date, new_status):
    conn = sqlite3.connect('C:/Users/gugul/Desktop/todo_app/database/todo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET task_name=?, task_due_date=?, status=? WHERE id=?", (new_task_name, new_task_due_date, new_status, task_id))
    conn.commit()
    conn.close()

class TaskItem(BoxLayout):
    def __init__(self, task_id, task_name, task_due_date, task_status, update_task_list_callback, **kwargs):
        super(TaskItem, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.task_id = task_id
        self.update_task_list_callback = update_task_list_callback

        self.add_widget(Label(text=task_name, size_hint_x=0.6))
        self.add_widget(Label(text=task_due_date, size_hint_x=0.2))
        self.add_widget(Label(text=task_status, size_hint_x=0.2))

        edit_button = Button(text="Edit", size_hint_x=None, width=70)
        edit_button.bind(on_release=self.open_edit_popup)
        self.add_widget(edit_button)

        delete_button = Button(text="Delete", size_hint_x=None, width=70)
        delete_button.bind(on_release=self.delete_task)
        self.add_widget(delete_button)

    def open_edit_popup(self, instance):
        layout = BoxLayout(orientation='vertical')
        self.edit_task_name = TextInput(text=self.label.text.split(' - ')[0])
        layout.add_widget(self.edit_task_name)
        self.edit_task_due_date = TextInput(text=self.label.text.split(' - ')[1].replace("Due: ", ""))
        layout.add_widget(self.edit_task_due_date)
        self.edit_task_status = TextInput(text=self.label.text.split(' - ')[2].replace("Status: ", ""))
        layout.add_widget(self.edit_task_status)
        save_button = Button(text="Save")
        save_button.bind(on_release=self.save_task)
        layout.add_widget(save_button)

        self.popup = Popup(title='Edit Task', content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def save_task(self, instance):
        new_task_name = self.edit_task_name.text
        new_task_due_date = self.edit_task_due_date.text
        new_task_status = self.edit_task_status.text
        update_task_in_db(self.task_id, new_task_name, new_task_due_date, new_task_status)
        self.update_task_list_callback()
        self.popup.dismiss()

    def delete_task(self, instance):
        delete_task_from_db(self.task_id)
        self.update_task_list_callback()

class TaskList(BoxLayout):
    def __init__(self, **kwargs):
        super(TaskList, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.update_task_list()

    def update_task_list(self):
        self.clear_widgets()
        tasks = fetch_tasks()
        if tasks:
            for task in tasks:
                task_item = TaskItem(task_id=task[0], task_name=task[1], task_due_date=task[2], task_status=task[3], update_task_list_callback=self.update_task_list)
                self.add_widget(task_item)
        else:
            self.add_widget(Label(text="No tasks available"))

class AddTaskPopup(Popup):
    def __init__(self, update_task_list_callback, **kwargs):
        super(AddTaskPopup, self).__init__(**kwargs)
        self.title = 'Add New Task'
        self.size_hint = (0.8, 0.8)
        self.update_task_list_callback = update_task_list_callback

        layout = BoxLayout(orientation='vertical')
        self.task_name_input = TextInput(hint_text='Task Name')
        layout.add_widget(self.task_name_input)
        self.task_due_date_input = TextInput(hint_text='Due Date (YYYY-MM-DD)')
        layout.add_widget(self.task_due_date_input)

        add_button = Button(text='Add Task')
        add_button.bind(on_release=self.add_task)
        layout.add_widget(add_button)

        self.content = layout

    def add_task(self, instance):
        task_name = self.task_name_input.text
        task_due_date = self.task_due_date_input.text
        add_task_to_db(task_name, task_due_date)
        self.update_task_list_callback()
        self.dismiss()

class MyApp(App):
    def build(self):
        # Set window size
        Window.size = (400, 600)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # App Icon
        icon_layout = BoxLayout(size_hint=(1, 0.2))
        icon = Image(source='icons/app_icon.png', size_hint=(None, None), size=(150, 150))
        icon_layout.add_widget(icon)
        layout.add_widget(icon_layout)

        # Task List
        self.task_list = TaskList(size_hint=(1, 0.6))
        scroll_view = ScrollView(size_hint=(1, 0.6))
        scroll_view.add_widget(self.task_list)
        layout.add_widget(scroll_view)

        # Buttons
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=20)
        add_task_button = Button(text='Add Task', size_hint=(0.5, 1))
        add_task_button.bind(on_release=self.open_add_task_popup)
        button_layout.add_widget(add_task_button)

        add_note_button = Button(text='Add Note', size_hint=(0.5, 1))
        add_note_button.bind(on_release=self.open_add_note_popup)
        button_layout.add_widget(add_note_button)

        layout.add_widget(button_layout)

        return layout

    def open_add_task_popup(self, instance):
        popup = AddTaskPopup(update_task_list_callback=self.task_list.update_task_list)
        popup.open()

    def open_add_note_popup(self, instance):
        popup = Popup(title='Add Note', content=Label(text='Add Note Functionality Coming Soon!'), size_hint=(0.8, 0.8))
        popup.open()

if __name__ == '__main__':
    MyApp().run()
