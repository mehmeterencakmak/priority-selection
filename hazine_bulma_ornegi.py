import numpy as np
import random

# Izgara boyutları
grid_size = 3

# Durumlar (hücreler) ve eylemler
states = [(i, j) for i in range(grid_size) for j in range(grid_size)]  # 3x3 ızgaradaki tüm hücreler
actions = ["up", "down", "left", "right"]

# Ödüller
reward_grid = np.zeros((grid_size, grid_size))
reward_grid[1, 3-1] = 100  # Hazine konumu (1, 2) → +100 ödül
reward_grid[1, 0] = -10    # Duvar konumu (1, 0) → -10 ödül

# Q-table başlangıç değerleri
q_table = np.zeros((len(states), len(actions)))

# Q-Learning parametreleri
learning_rate = 0.1       # Öğrenme oranı
discount_factor = 0.9     # Gelecekteki ödüller için indirgeme faktörü
epsilon = 0.1             # Epsilon-greedy keşif oranı
episodes = 1000           # Eğitim döngüsü

# Hareket mantığı: Eylemin etkisini belirler
def get_next_state(state, action):
    x, y = state
    if action == "up" and x > 0:         # Yukarı
        x -= 1
    elif action == "down" and x < grid_size - 1:  # Aşağı
        x += 1
    elif action == "left" and y > 0:    # Sola
        y -= 1
    elif action == "right" and y < grid_size - 1: # Sağa
        y += 1
    return (x, y)

# Eğitim döngüsü
for episode in range(episodes):
    current_state = (0, 0)  # Başlangıç durumu
    done = False

    while not done:
        # Epsilon-greedy stratejisi ile eylem seçimi
        if random.uniform(0, 1) < epsilon:
            action_index = random.choice(range(len(actions)))  # Rastgele bir eylem seç
        else:
            action_index = np.argmax(q_table[states.index(current_state)])  # Q-tablosundan en iyi eylemi seç

        action = actions[action_index]
        next_state = get_next_state(current_state, action)

        # Ödülü al
        reward = reward_grid[next_state]

        # Q-Table güncellemesi
        old_value = q_table[states.index(current_state), action_index]
        next_max = np.max(q_table[states.index(next_state)])
        new_value = old_value + learning_rate * (reward + discount_factor * next_max - old_value)
        q_table[states.index(current_state), action_index] = new_value

        # Eğer hazineye ulaşıldıysa durumu bitir
        if reward == 100:
            done = True

        # Durumu güncelle
        current_state = next_state

# Eğitim sonrası Q-tablosunu yazdır
print("Eğitim tamamlandı!")
print("Q-Table:")
print(q_table)

# Test aşaması: Robotun hareketini simüle edelim
current_state = (0, 0)  # Başlangıç
path = [current_state]

print("\nTest Aşaması:")
while current_state != (1, 2):  # Hazine konumu
    action_index = np.argmax(q_table[states.index(current_state)])
    action = actions[action_index]
    current_state = get_next_state(current_state, action)
    path.append(current_state)

print("İzlenen Rota:", path)
