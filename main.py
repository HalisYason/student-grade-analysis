import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class StudentAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Öğrenci Not Analiz Uygulaması")
        self.setGeometry(200, 200, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.label = QLabel("Veri Analizi Yapmak İçin Bir CSV Dosyası Seçin:")
        layout.addWidget(self.label)

        self.select_button = QPushButton("Dosya Seç")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)

        self.analysis_button = QPushButton("Analiz Yap")
        self.analysis_button.setEnabled(False)
        self.analysis_button.clicked.connect(self.analyze_data)
        layout.addWidget(self.analysis_button)

        self.analysis_options = ["Ders Notu", "Ödev Notu", "Proje Notu"]
        self.analysis_label = QLabel("Analiz Seçin:")
        layout.addWidget(self.analysis_label)

        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems(self.analysis_options)
        layout.addWidget(self.analysis_combo)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.graph_label = QLabel()
        layout.addWidget(self.graph_label)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "CSV Dosyası Seç", "", "CSV Dosyaları (*.csv);;All Files (*)", options=options)
        if file_name:
            self.file_name = file_name
            self.load_data()
            self.label.setText(f"Seçilen Dosya: {file_name}")
            self.analysis_button.setEnabled(True)

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_name)
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hata oluştu: {e}")

    def analyze_data(self):
        try:
            analysis_type = self.analysis_combo.currentText()
            result = self.df[analysis_type].describe().to_string()
            self.result_label.setText(result)

            plt.figure(figsize=(8, 6))
            self.df.plot(x='Öğrenci Adı', y=analysis_type, kind='bar', legend=False)
            plt.title(f"{analysis_type} Analizi")
            plt.xlabel("Öğrenci Adı")
            plt.ylabel(analysis_type)
            plt.tight_layout()
            plt.savefig('graph.png')
            plt.close()

            pixmap = QPixmap('graph.png')
            self.graph_label.setPixmap(pixmap)

        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hata oluştu: {e}")

    def closeEvent(self, event):
        self.remove_temp_files()
        event.accept()

    def remove_temp_files(self):
        try:
            os.remove('graph.png')
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentAnalysisApp()
    window.show()
    sys.exit(app.exec_())
