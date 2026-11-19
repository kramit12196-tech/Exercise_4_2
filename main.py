
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from About import AboutWindow


#---------- Main Window ----------
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.temperatures = []
        self.profits = []
        self.selected_file_path = ""

        #---------- חלון אודות ----------
        self.about_window = AboutWindow()
        #-------------------------------

        self.initUI()


    #---------- User Interface ----------
    def initUI(self):
        self.setWindowTitle("Ice Cream Profits")
        self.resize(1000, 700)

        main_layout = QVBoxLayout()

        #---------- כפתורי פעולה ----------
        button_layout = QHBoxLayout()

        self.load_csv_button = QPushButton("Load CSV")
        self.load_csv_button.clicked.connect(self.load_csv_file)
        button_layout.addWidget(self.load_csv_button)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_window.show)
        button_layout.addWidget(self.about_button)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        #---------------------------------

        #---------- אזור גרף ----------
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        #------------------------------

        self.setLayout(main_layout)
        self.draw_plot()


    #---------- בחירת קובץ ----------
    def load_csv_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )

        if file_path:
            self.selected_file_path = file_path
            self.load_csv_data()
    #--------------------------------


    #---------- טעינת נתונים ----------
    def load_csv_data(self):
        self.temperatures = []
        self.profits = []

        with open(self.selected_file_path, 'r') as f:
            next(f)

            for line in f:
                temperature, profit = line.strip().split(',')
                self.temperatures.append(float(temperature))
                self.profits.append(int(profit))

        print("Rows loaded:", len(self.temperatures))
        print("Temperatures:", self.temperatures[:3])
        print("Profits:", self.profits[:3])

        self.draw_plot()
    #----------------------------------


    #---------- ציור גרף ----------
    def draw_plot(self):
        self.figure.clear()
        axis = self.figure.add_subplot(111)

        example_temperatures = [10, 15, 20, 25, 30]
        example_profits = [100, 180, 260, 320, 400]
        axis.plot(example_temperatures, example_profits)

        axis.set_xlabel("Temperature")
        axis.set_ylabel("Profit")
        axis.set_title("Ice Cream Profits")
        self.figure.tight_layout()
        self.canvas.draw()
    #-------------------------------


#---------- Run Application ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
