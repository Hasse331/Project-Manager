
import datetime
import PyQt5

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication as Qapp, QTextEdit, QFileDialog, QMessageBox, QStyle, QDateEdit, QHeaderView, QAbstractItemView, QTableWidget, QTableWidgetItem, QVBoxLayout, QCheckBox, QDialog, QMainWindow as Qmain, QLineEdit as Qline, QLabel as Qlab, QPushButton as Qbtn
from PyQt5.QtCore import pyqtSignal, QTimer, QDate




class RemainingTimer():
   def update(self, input_variable):

        if input_variable == "-":
            formatted_time = "-"

        elif input_variable == "Ready":
            formatted_time = "Ready"

        else:

            current_date = datetime.now().strftime("%d.%m.%y")
            deadline_date = input_variable

            now_date_obj = datetime.strptime(current_date,"%d.%m.%y")
            input_date_obj = datetime.strptime(deadline_date,"%d.%m.%y")

            remaining = input_date_obj - now_date_obj
            #remaining = str(remaining.days)

            current_time = datetime.now()

            days = remaining.days
            hours = 24
            minutes = 60
            seconds = 60

            current_hours = current_time.hour
            current_minutes = current_time.minute
            current_seconds = current_time.second

            formatted_time = f"{days}d {hours - current_hours}h {minutes - current_minutes}m {seconds - current_seconds}s"

        return formatted_time