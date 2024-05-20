from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder

def eventHandler():
    mq3 = mq3_input.text()
    mq4 = mq4_input.text()
    mq5 = mq5_input.text()
    mq135 = mq135_input.text()
    try:
        manual_data = np.array([[int(mq3),int(mq4),int(mq5),int(mq135)]])
        # Load the saved model
        model = tf.keras.models.load_model('trained_model.h5')
        classes = ['Hijau', 'Hitam', 'Oolong']
        # Use the model to make predictions or further evaluation
        predictions = model.predict(manual_data)
        predicted_classes = np.argmax(predictions, axis=1)

        # Inisialisasi LabelEncoder
        label_encoder = LabelEncoder()
        label_encoder.fit(classes)

        # Konversi kelas yang diprediksi menjadi nama kelas yang sesuai
        predicted_classes_names = label_encoder.inverse_transform(predicted_classes)
        indikator.setText(predicted_classes_names[0])
    except:
        indikator.setText("Ada kesalahan")
        

app = QApplication([])
window = QWidget()
window.setWindowTitle("Klasifikasi Teh")
window.resize(512, 512)
main_layout = QVBoxLayout()

#judul
layout_judul = QHBoxLayout()
judul = QLabel("Klasifikasi Jenis Teh")
judul_font = QFont("Arial", 20)  # Set font family and size
judul.setFont(judul_font)
layout_judul.addWidget(judul)
layout_judul.setAlignment(Qt.AlignCenter)  # Align center horizontally

#masukkan inputan
mq3_input = QLineEdit()
mq3_input_label = QLabel("MQ3:")
mq4_input = QLineEdit()
mq4_input_label = QLabel("MQ4:")
mq5_input = QLineEdit()
mq5_input_label = QLabel("MQ5:")
mq135_input = QLineEdit()
mq135_input_label = QLabel("MQ135:")

#layou each input

layout_mq3 = QHBoxLayout()
layout_mq4 = QHBoxLayout()
layout_mq5 = QHBoxLayout()
layout_mq135 = QHBoxLayout()
layout_mq3.addWidget(mq3_input_label)
layout_mq3.addWidget(mq3_input)
layout_mq4.addWidget(mq4_input_label)
layout_mq4.addWidget(mq4_input)
layout_mq5.addWidget(mq5_input_label)
layout_mq5.addWidget(mq5_input)
layout_mq135.addWidget(mq135_input_label)
layout_mq135.addWidget(mq135_input)

layout_input = QVBoxLayout()
#set all of width of input in 700

#add all input into layput input
layout_input.addLayout(layout_mq3)
layout_input.addLayout(layout_mq4)
layout_input.addLayout(layout_mq5)
layout_input.addLayout(layout_mq135)
layout_input.setAlignment(Qt.AlignCenter)  # Align center horizontally

#add button
button = QPushButton("Prediksi")
button_layout = QHBoxLayout()
button_layout.addWidget(button)
button_layout.setAlignment(Qt.AlignCenter)
button.clicked.connect(eventHandler)

#indikator hasil
indikator = QLabel()
layout_indikator = QVBoxLayout()
layout_indikator.addWidget(indikator)
indikator.setFont(judul_font)
layout_indikator.setAlignment(Qt.AlignCenter)

#add layout to windoq
main_layout.addLayout(layout_judul)
main_layout.addLayout(layout_input)
main_layout.addLayout(button_layout)
main_layout.addLayout(layout_indikator)
window.setLayout(main_layout)
window.show()
app.exec_()