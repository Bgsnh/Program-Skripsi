import pandas as pd #digunakan untuk import pandas, pandas membaca data
import numpy as np #digunakan untuk import numpy, numpy mengolah data berkaitan dengan statistika dan matematika
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

sc = StandardScaler() #melakukan proses transformasi menjadi normalisasi dengan rumus deviasi
data=pd.read_csv("TEH1.csv")
print(data)
df=pd.DataFrame(data)
X=df.iloc[:,1:5].values # Fitur
y=df.iloc[:,0].values # Target
le = LabelEncoder()
y=le.fit_transform(y)
print(y)
print(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
data.info()
X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.fit_transform(X_test)
print(X_train_scaled)
print(X_test_scaled)

# Sesuaikan dan ubah label target
y_train_encoded = le.fit_transform(y_train)
y_test_encoded = le.transform(y_test)

# Ubah label menjadi pengkodean one-hot
y_train_one_hot = tf.keras.utils.to_categorical(y_train_encoded, num_classes=3)
y_test_one_hot = tf.keras.utils.to_categorical(y_test_encoded, num_classes=3)

# Tentukan arsitektur model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(units=8, activation='relu', input_shape=(X_train.shape[1],))) #hidden layer 1 
#model.add(tf.keras.layers.Dense(units=4, activation='relu'))
model.add(tf.keras.layers.Dense(units=3, activation='softmax')) # Output layer

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train_one_hot, epochs=100, batch_size=128)

model.save('trained_model.h5')

# Evaluate the model
evaluation_results = model.evaluate(X_test, y_test_one_hot, batch_size=128)

# Print out accuracy and all metrics
print("Evaluation results:")
for metric_name, metric_value in zip(model.metrics_names, evaluation_results):
    print(f"{metric_name}: {metric_value}")

manual_data = np.array([[786,883,1757,732]])

classes = ['Hijau', 'Hitam', 'Oolong']

# Lakukan prediksi dengan model
predictions = model.predict(manual_data)

# Dapatkan indeks kelas dengan probabilitas tertinggi untuk setiap prediksi
predicted_classes = np.argmax(predictions, axis=1)

# Inisialisasi LabelEncoder
label_encoder = LabelEncoder()
label_encoder.fit(classes)

# Konversi kelas yang diprediksi menjadi nama kelas yang sesuai
predicted_classes_names = label_encoder.inverse_transform(predicted_classes)

# Print hasil prediksi
print("Hasil prediksi untuk angka manual:", predicted_classes_names)