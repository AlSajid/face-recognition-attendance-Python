from tkinter import Tk
from tkinter import ttk
import mysql.connector
import face_detector
from tkinter import messagebox


class Attendance:

    def __init__(self, master):

        # Window Management
        master.title('DIU Smart Attendance Application')
        master.state('zoomed')
        master.resizable(False, False)

        # Frame Management
        header_frame = ttk.Frame(master)
        header_frame.pack()

        body_frame = ttk.Frame(master)
        body_frame.pack()

        self.attendance_list = ttk.Frame(body_frame)
        self.attendance_list.grid(column=0, columnspan=2, row=0, pady=20)

        # Widgets Management
        header = ttk.Label(
            header_frame, text="DIU Smart Attendance Application")
        header.grid(row=0, column=0, pady=3)
        header.config(background='#09509e', foreground="#e7e6e6",
                      width=1920, font=('Constantia', 24, 'bold'))

        self.camera = ttk.Label(body_frame, text="Open Camera to Start", font = "Calibri 14 bold")
        self.camera.grid(row=2, column=0, columnspan=3, pady=30)

        self.camera_button = ttk.Button(
            body_frame, text='Open Camera', width=25, command=self.detect_face)
        self.camera_button.grid(row=3, column=0, pady=25)

        self.add_attendance_button = ttk.Button(
            body_frame, text='Add attendance', width=25, command=self.add_attendance)
        self.add_attendance_button.grid(row=3, column=1)
        self.add_attendance_button.state(['disabled'])

        self.attendance_dashboard()

    def detect_face(self):
        global name
        name = face_detector.detect_face()
        self.camera.config(text=name)
        self.add_attendance_button.state(['!disabled'])

    def add_attendance(self):
        database = mysql.connector.connect(
            host="localhost", user="root", password="", database="diu_sap")
        cursor = database.cursor()

        sql = "SELECT `Roll` FROM `students` WHERE `Name` = %s"
        value = (name,)
        cursor.execute(sql, value)
        roll = cursor.fetchone()

        sql = "INSERT INTO `attendance` (`ID`, `Name`) VALUES (%s, %s)"
        value = (roll[0], name)
        cursor.execute(sql, value)
        database.commit()

        messagebox.showinfo(title="Confirmation",
                            message='Attendance has been recorded')
        self.add_attendance_button.state(['disabled'])
        self.camera_button.state(['!disabled'])
        self.camera.config(text="")
        self.attendance_dashboard()

    def attendance_dashboard(self):
        ttk.Label(self.attendance_list, text="Roll",
                  font="Calibri 16 bold").grid(row=0, column=0)
        ttk.Label(self.attendance_list, text="Name",
                  font="Calibri 16 bold").grid(row=0, column=1)
        ttk.Label(self.attendance_list, text="Date Time",
                  font="Calibri 16 bold").grid(row=0, column=2)

        database = mysql.connector.connect(
            host="localhost", user="root", password="", database="diu_sap")
        cursor = database.cursor()

        sql = "SELECT * FROM `attendance` ORDER BY `DateTime` DESC LIMIT 15"
        cursor.execute(sql)
        result = cursor.fetchall()

        for i in range(len(result)):
            for j in range(3):
                self.td = ttk.Entry(self.attendance_list, font="Calibri 14")
                self.td.grid(row=i+1, column=j)
                self.td.insert(0, result[i][j+1])
                self.td.state(['readonly'])


def main():
    master = Tk()
    Attendance(master)
    master.mainloop()


if __name__ == "__main__":
    main()
