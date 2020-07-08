import tkinter as tk
from tkinter import ttk
import sqlite3


# Вызов дочернего окна
def open_dialog():
    Child()


# Вызов окна для редактирования данных
def open_update_dialog():
    Update()


# Вызов окна для поиска данных
def open_search_dialog():
    Search()


class Main(tk.Frame):
    def __init__(self, window):
        super().__init__(window)
        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings')
        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        self.search_img = tk.PhotoImage(file='search.gif')
        self.delete_img = tk.PhotoImage(file='delete.gif')
        self.update_img = tk.PhotoImage(file='update.gif')
        self.add_img = tk.PhotoImage(file='add.gif')
        self.init_main()
        self.db = db
        self.view_records()

    # Для хранения и инициализации всех объектов графического интерфейса
    def init_main(self):
        # Для хранения и инициализации всех объектов графического интерфейса
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # Создание кнопки создания
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)
        # Создание кнопки редактирования
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', command=open_update_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT)
        # Создание кнопки удаления
        btn_delete_dialog = tk.Button(toolbar, text='Удалить', command=self.delete_records, bg='#d7d8e0', bd=0,
                                      compound=tk.TOP, image=self.delete_img)
        btn_delete_dialog.pack(side=tk.LEFT)
        btn_search = tk.Button(toolbar, text='Поиск', command=open_search_dialog, bg='#d7d8e0', bd=0,
                               compound=tk.TOP, image=self.search_img)
        btn_search.pack(side=tk.LEFT)
        btn_refresh = tk.Button(toolbar, text='Обновить', command=self.view_records, bg='#d7d8e0', bd=0,
                                compound=tk.TOP, image=self.refresh_img)
        btn_refresh.pack(side=tk.LEFT)
        # Создание необходимых полей
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=345, anchor=tk.CENTER)
        self.tree.column('costs', width=170, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')
        self.tree.pack()

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        # Для автоматизации отображения данных
        self.view_records()

    # Для редактирование/обновление записи в БД
    def update_record(self, description, costs, total):
        self.db.c.execute("UPDATE finance SET description=?, costs=?, total=? WHERE ID=?",
                          (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Для отображения информации из БД в виджете Treeview главного окна
    def view_records(self):
        self.db.c.execute("SELECT * FROM finance")
        # Очистка содержимого виджета во изберание повторений в нем
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Для отображения данных из БД
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute("DELETE FROM finance WHERE id=?", (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Поиск данных
    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute("SELECT * FROM finance WHERE description LIKE ?", description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


# Создание дочернего окна, наследуясь от Toplevel
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_add = ttk.Button(self, text='Добавить')
        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.entry_money = ttk.Entry(self)
        self.entry_description = ttk.Entry(self)
        self.init_child()
        self.view = app

    # Для хранения и инициализации всех объектов графического интерфейса
    def init_child(self):
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)
        # Подписать поля ввода
        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=40, y=50)
        label_select = tk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=40, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=40, y=110)
        # Добавить элемент для ввода данных
        self.entry_description.place(x=200, y=50)
        self.entry_money.place(x=200, y=110)
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)
        # Кнопка закрытия окна
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)
        # Кнопка добавления данных
        self.btn_add.place(x=200, y=170)
        # Добавить функционал кнопки
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(
            self.entry_description.get(), self.combobox.get(), self.entry_money.get()))
        # Перехват всех событий происходящие в приложении и удержание фокуса до закрытия
        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.extract_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=200, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.entry_description.get(), self.combobox.get(), self.entry_money.get()))
        self.btn_add.destroy()

    # Извлекает из БД выделенную запись
    def extract_data(self):
        self.db.c.execute("SELECT * FROM finance WHERE id=?", (self.view.tree.set(
            self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_money.insert(0, row[3])


# Класс для поиска данных
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.entry_search = ttk.Entry(self)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        self.entry_search.place(x=105, y=20, width=150)
        # Добавить кнопку закрыть
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)
        # Добавить кнопку поиска
        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


# Класс для работы с базой данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')  # Подключить БД
        # Для взаимодействия с БД и выполнения в ней операций
        self.c = self.conn.cursor()
        # Для создания таблицы БД
        self.c.execute("CREATE TABLE IF NOT EXISTS finance ("
                       "id integer primary key, description text, costs text, total real)")
        # Для сохранения изменений внесенных в БД
        self.conn.commit()

    # Для получения на вход значений из данных дочернего окна
    def insert_data(self, description, costs, total):
        self.c.execute("INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)",
                       (description, costs, total))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
