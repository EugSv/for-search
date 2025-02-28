from tkinter import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Настройка базы данных
engine = create_engine("postgresql://postgres:###", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Модель данных
class Data(Base):
    __tablename__ = 'database'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)

Base.metadata.create_all(engine)

# Функция для сохранения данных
def save_data():
    name = entry_name.get()
    surname = entry_surname.get()
    age = entry_age.get()

    if name and surname and age:
        new_data = Data(name=name, surname=surname, age=int(age))
        session.add(new_data)
        session.commit()
        entry_name.delete(0, END)
        entry_surname.delete(0, END)
        entry_age.delete(0, END)

# Функция для чтения данных
def read_data():
    text_zona.delete('1.0', END)
    records = session.query(Data).all()
    for record in records:
        text_zona.insert(END, f"ID: {record.id}, Имя: {record.name}, Фамилия: {record.surname}, Возраст: {record.age}\n")

# Функция для удаления данных
def delete_data():
    record_id = entry_id.get()
    if record_id:
        record = session.query(Data).filter_by(id=int(record_id)).first()
        if record:
            session.delete(record)
            session.commit()
            text_zona.insert(END, f"Запись с ID {record_id} удалена.\n")
        else:
            text_zona.insert(END, f"Запись с ID {record_id} не найдена.\n")
        entry_id.delete(0, END)

# Интерфейс приложения
root = Tk()
root.title("База данных")
root.geometry("485x500")

Label(text="Поле для ввода Имени:").grid(row=0, column=0)
entry_name = Entry()
entry_name.grid(row=0, column=1, sticky="nsew")

Label(text="Поле для ввода Фамилии:").grid(row=1, column=0)
entry_surname = Entry()
entry_surname.grid(row=1, column=1, sticky="nsew")

Label(text="Поле для ввода Возраста:").grid(row=2, column=0)
entry_age = Entry()
entry_age.grid(row=2, column=1, sticky="nsew")

Button(text="Записать", command=save_data).grid(row=3, column=0, pady=10, columnspan=2, ipadx=50)

Label(text="Поле для ввода ID для удаления:").grid(row=4, column=0)
entry_id = Entry()
entry_id.grid(row=4, column=1, sticky="nsew")

Button(text="Удалить", command=delete_data).grid(row=5, column=0, pady=10, columnspan=2, ipadx=50)

text_zona = Text(height=15, width=60)
text_zona.grid(row=6, column=0, columnspan=2, pady=10)

Button(text="Прочитать", command=read_data).grid(row=7, column=0, columnspan=2, ipadx=50)

root.mainloop()
