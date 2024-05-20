import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder

manual_data = np.array([[794,899,1755,748]])
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
# Setelah pelatihan, dapatkan nilai bobot dari model
weights = model.get_weights()

# Tampilkan nilai bobot
for i, layer_weights in enumerate(weights):
    print(f'Layer {i + 1} weights:')
    print(layer_weights)
    
# Print hasil prediksi
print("Hasil prediksi untuk angka manual:", predicted_classes_names)