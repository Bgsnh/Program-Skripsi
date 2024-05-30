import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import serial
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder

class SerialReader(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port, baudrate=115200, parent=None):
        super(SerialReader, self).__init__(parent)
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.running = False

    def run(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            while self.running:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.data_received.emit(data)
        except serial.SerialException as e:
            print(f"Error: {e}")
        finally:
            if self.ser:
                self.ser.close()

    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Klasifikasi Teh")
        self.resize(600, 400)
        self.model = tf.keras.models.load_model("trained_model.h5")
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(["Hijau", "Hitam", "Oolong"])
        self.history_data = []
        self.init_ui()
        self.serial_reader = SerialReader(port='COM3')  # Ganti 'COM3' dengan port serial Anda
        self.serial_reader.data_received.connect(self.handle_serial_data)
        self.serial_reader.start()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        
        # Add tab widget
        self.tabs = QTabWidget()
        self.tab_classification = QWidget()
        self.tab_history = QWidget()
        
        self.tabs.addTab(self.tab_classification, "Klasifikasi")
        self.tabs.addTab(self.tab_history, "Riwayat")
        
        # Set layout for classification tab
        self.classification_layout = QVBoxLayout()
        self.tab_classification.setLayout(self.classification_layout)
        
        # Judul
        judul = QLabel("Klasifikasi Jenis Teh")
        judul_font = QFont("Arial", 24, QFont.Bold)
        judul.setFont(judul_font)
        judul.setAlignment(Qt.AlignCenter)
        
        # Indikator hasil
        self.indikator = QLabel("Menunggu data...")
        self.indikator.setFont(QFont("Arial", 18))
        self.indikator.setAlignment(Qt.AlignCenter)
        
        self.classification_layout.addWidget(judul)
        self.classification_layout.addWidget(self.indikator)
        
        # Set layout for history tab
        self.history_layout = QVBoxLayout()
        self.tab_history.setLayout(self.history_layout)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Timestamp", "Klasifikasi", "Suhu (°C)", "Kelembaban (%)"])
        self.history_layout.addWidget(self.history_table)
        
        self.layout.addWidget(self.tabs)

    def handle_serial_data(self, data):
        try:
            # Parsing data
            humi, temp, mq3, mq4, mq5, mq135 = map(float, data.split(","))
            manual_data = np.array([[mq3, mq4, mq5, mq135]])
            
            # Predict
            predictions = self.model.predict(manual_data)
            predicted_classes = np.argmax(predictions, axis=1)
            predicted_class_name = self.label_encoder.inverse_transform(predicted_classes)[0]
            
            # Update UI
            self.indikator.setText(f"Hasil Klasifikasi: {predicted_class_name}")
            
            # Add to history
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            self.history_data.append((timestamp, predicted_class_name, temp, humi))
            self.update_history_table()
        except Exception as e:
            self.indikator.setText(f"Error: {e}")

    def update_history_table(self):
        self.history_table.setRowCount(len(self.history_data))
        for row, (timestamp, classification, temp, humi) in enumerate(self.history_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.history_table.setItem(row, 1, QTableWidgetItem(classification))
            self.history_table.setItem(row, 2, QTableWidgetItem(f"{temp:.2f}"))
            self.history_table.setItem(row, 3, QTableWidgetItem(f"{humi:.2f}"))
    
    def closeEvent(self, event):
        self.serial_reader.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
