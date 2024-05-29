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
        self.resize(512, 512)
        self.model = tf.keras.models.load_model("trained_model.h5")
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(["Hijau", "Hitam", "Oolong"])
        self.initUI()
        self.serial_reader = SerialReader(port='COM3')  # Ganti 'COM3' dengan port serial Anda
        self.serial_reader.data_received.connect(self.handle_serial_data)
        self.serial_reader.start()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Judul
        layout_judul = QHBoxLayout()
        judul = QLabel("Klasifikasi Jenis Teh")
        judul_font = QFont("Arial", 20)
        judul.setFont(judul_font)
        layout_judul.addWidget(judul)
        layout_judul.setAlignment(Qt.AlignCenter)

        # Indikator hasil
        self.indikator = QLabel("Menunggu data...")
        self.indikator.setFont(judul_font)
        layout_indikator = QVBoxLayout()
        layout_indikator.addWidget(self.indikator)
        layout_indikator.setAlignment(Qt.AlignCenter)

        main_layout.addLayout(layout_judul)
        main_layout.addLayout(layout_indikator)
        self.setLayout(main_layout)

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
        except Exception as e:
            self.indikator.setText(f"Error: {e}")

    def closeEvent(self, event):
        self.serial_reader.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
