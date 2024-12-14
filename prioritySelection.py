import numpy as np
import random

# Mekanlar ve ödülleri
locations = ["Hastane", "Okul", "Cami", "Karakol"]
rewards = {"Hastane": 10, "Okul": 20, "Cami": 30, "Karakol": 40}

# Q-table oluşturma (4 mekan için 4 eylem)
q_table = np.zeros((len(locations), len(locations)))

# RL parametreleri
learning_rate = 0.1  # Öğrenme hızı
discount_factor = 0.9  # Gelecekteki ödüllerin indirgenme katsayısı
epsilon = 0.1  # Epsilon-greedy stratejisi için keşif oranı
episodes = 1000  # Eğitim döngü sayısı

# Drone'nun toplam ödülünü hesaplamak için ödül hedefi
reward_goal = 100

# Ortam simülasyonu
for episode in range(episodes):
    # Drone rastgele bir yerden başlar
    current_location = random.choice(range(len(locations)))
    total_reward = 0

    while total_reward < reward_goal:
        # Epsilon-greedy stratejisi ile eylem seçimi
        if random.uniform(0, 1) < epsilon:
            action = random.choice(range(len(locations)))  # Keşif
        else:
            action = np.argmax(q_table[current_location])  # Sömürü

        # Seçilen eyleme göre ödül al
        selected_location = locations[action]
        reward = rewards[selected_location]
        total_reward += reward

        # Q-Learning güncellemesi
        old_value = q_table[current_location, action]
        next_max = np.max(q_table[action])  # Sonraki durumdaki maksimum Q değeri
        new_value = old_value + learning_rate * (reward + discount_factor * next_max - old_value)
        q_table[current_location, action] = new_value

        # Drone'un bulunduğu konumu güncelle
        current_location = action

# Eğitim tamamlandıktan sonra sonuçları inceleyelim
print("Q-Table:")
print(q_table)

# Drone'un eğitilmiş stratejisini gösteren bir fonksiyon
def choose_action(state):
    return locations[np.argmax(q_table[state])]

# Test etme
start_location = 0  # "Hastane"den başlıyor
print("\nTest Stratejisi:")
total_reward = 0
current_location = start_location
visited_locations = []

while total_reward < reward_goal:
    action = np.argmax(q_table[current_location])
    next_location = locations[action]
    visited_locations.append(next_location)
    total_reward += rewards[next_location]
    current_location = action

print("Drone'un izlediği rota:", visited_locations)
print("Toplam kazanç:", total_reward)
