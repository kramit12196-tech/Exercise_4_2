
import sys
import os
import numpy as np
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
)
from PySide6.QtWidgets import QStyle
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

        self.load_style_sheet()

        #---------- חלון אודות ----------
        self.about_window = AboutWindow()
        #-------------------------------

        self.initUI()

    #---------- טעינת עיצוב ----------
    def load_style_sheet(self):
        style_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")

        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as style_file:
                self.setStyleSheet(style_file.read())
    #---------------------------------

    #---------- User Interface ----------
    def initUI(self):
        self.setWindowTitle("Ice Cream Profits")
        self.resize(1000, 700)
        self.setMinimumSize(700, 500)
        self.setObjectName("mainWindow")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        #---------- כפתורי פעולה ----------
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.load_csv_button = QPushButton("Load CSV")
        self.load_csv_button.setObjectName("loadCsvButton")
        self.load_csv_button.clicked.connect(self.load_csv_file)
        button_layout.addWidget(self.load_csv_button)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.clicked.connect(self.about_window.show)
        button_layout.addWidget(self.about_button)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        #---------------------------------

        #---------- אזור גרף ----------
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setObjectName("graphToolbar")
        self.toolbar.setMovable(False)
        self.toolbar.format_coord = lambda x, y: ""
        reset_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)

        for action in self.toolbar.actions():
            if action.text() == "Home":
                action.setIcon(reset_icon)
                action.setToolTip("Reset Graph View")
                action.setStatusTip("Reset Graph View")
                break

        self.canvas.setObjectName("graphCanvas")

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.canvas)
        #------------------------------

        self.setLayout(main_layout)
        self.draw_plot()

    #---------- תיבת קואורדינטות ----------
    def setup_coordinate_tooltip(self):
        if not hasattr(self, "_coordinate_event_cid"):
            self._coordinate_event_cid = self.canvas.mpl_connect(
                "motion_notify_event",
                self.update_mouse_coordinates,
            )

        axis = self.figure.axes[0]
        annotation_is_on_axis = (
            hasattr(self, "coordinate_annotation")
            and self.coordinate_annotation in axis.texts
        )

        if not annotation_is_on_axis:
            self.coordinate_annotation = axis.annotate(
                "",
                xy=(0, 0),
                xytext=(12, 12),
                textcoords="offset points",
                bbox={
                    "boxstyle": "round,pad=0.35",
                    "facecolor": "#FFFFFF",
                    "edgecolor": "#C7D5DB",
                    "linewidth": 0.8,
                },
                fontsize=9,
                color="#263238",
                visible=False,
            )

    def update_mouse_coordinates(self, event):
        if event.inaxes is None or event.xdata is None or event.ydata is None:
            if hasattr(self, "coordinate_annotation"):
                if self.coordinate_annotation.get_visible():
                    self.coordinate_annotation.set_visible(False)
                    self.canvas.draw_idle()
            return

        if hasattr(self, "coordinate_annotation"):
            self.coordinate_annotation.set_text(
                f"X: {event.xdata:.2f} | Y: {event.ydata:.2f}"
            )
            self.coordinate_annotation.xy = (event.xdata, event.ydata)
            self.coordinate_annotation.set_visible(True)
            self.canvas.draw_idle()
    #--------------------------------------

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
        self.figure.set_facecolor("#F7F9FA")
        axis = self.figure.add_subplot(111)
        axis.set_facecolor("#FFFFFF")

    #---------- גרף פיזור ----------
        axis.scatter(
            self.temperatures,
            self.profits,
            s=1,
            color="#2A9D8F",
            alpha=0.75,
        )

#---------- קו מגמה ----------
        if len(self.temperatures) > 1:
            m, b = np.polyfit(self.temperatures, self.profits, 1)

            x1 = min(self.temperatures)
            x2 = max(self.temperatures)

            y1 = m * x1 + b
            y2 = m * x2 + b

            axis.plot(
                [x1, x2],
                [y1, y2],
                color="#2878A8",
                linewidth=2,
                label=f"y = {m:.2f}x {b:+.2f}",
            )

            axis.legend(
                frameon=True,
                facecolor="#FFFFFF",
                edgecolor="#D8E1E5",
                loc="best",
            )

    #---------- כותרות הגרף ----------
        axis.set_xlabel("Temperature")
        axis.set_ylabel("Revenue")
        axis.set_title("Ice Cream Revenue vs Temperature")
        axis.title.set_fontsize(15)
        axis.title.set_fontweight("bold")
        axis.title.set_color("#263238")
        axis.xaxis.label.set_fontsize(12)
        axis.yaxis.label.set_fontsize(12)
        axis.xaxis.label.set_color("#455A64")
        axis.yaxis.label.set_color("#455A64")
        axis.tick_params(axis="both", colors="#607D8B", labelsize=10)
        axis.grid(True, color="#E6ECEF", linewidth=0.8, alpha=0.9)

    #---------- הסרת מסגרות ----------
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color("#B0BEC5")
        axis.spines["bottom"].set_color("#B0BEC5")

    #---------- עדכון הגרף ----------
        self.figure.tight_layout()
        self.canvas.draw()
        if hasattr(self, "toolbar"):
            self.toolbar.push_current()
        self.setup_coordinate_tooltip()
    #-------------------------------

#---------- Run Application ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
