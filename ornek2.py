import numpy as np

# Ortam Parametreleri
BUILDINGS = ["hospital", "school", "police_station", "mall", "residential", "other"]
REWARDS = {
    "hospital": 5000,  # Hastane ödülü çok yüksek yapıldı
    "school": 80,
    "police_station": 90,
    "mall": 50,
    "residential": 30,
    "other": -10  # Gereksiz bina seçilirse ceza
}

# Q-Tablosu (Başlangıçta 0'larla dolu)
q_table = np.zeros((len(BUILDINGS), len(BUILDINGS)))

# Hyperparametreler
learning_rate = 0.05  # Öğrenme hızı daha düşük
discount_factor = 0.9  # Gelecek ödülleri indirimleme faktörü
epsilon = 0.1  # Keşif oranı (rastgele seçim yapma ihtimali)
episodes = 5000  # Eğitim döngü sayısı artırıldı

# Ajanın karar verdiği bina
def choose_action(state, epsilon):
    if np.random.rand() < epsilon:  # Keşif
        return np.random.choice(len(BUILDINGS))
    else:  # Sömürü (En iyi aksiyonu seç)
        return np.argmax(q_table[state])

# Pekiştirmeli öğrenme süreci
for episode in range(episodes):
    current_state = np.random.choice(len(BUILDINGS))  # Rastgele başlangıç durumu
    
    while True:
        action = choose_action(current_state, epsilon)
        reward = REWARDS[BUILDINGS[action]]
        
        # Eğer hastane hedefleniyorsa ek ödül ekle
        if BUILDINGS[action] == "hospital":
            reward += 1000  # Hastaneyi özel bir ödül ile teşvik et
        
        # Q-Değeri Güncellemesi
        best_next_action = np.argmax(q_table[action])
        q_table[current_state, action] = q_table[current_state, action] + learning_rate * (
            reward + discount_factor * q_table[action, best_next_action] - q_table[current_state, action]
        )
        
        # Durum Güncelleme
        current_state = action
        
        # Eğer ödül negatifse (örneğin gereksiz bina seçilirse), ceza ver ve çık
        if reward < 0:
            break
        
        # Hedef (örneğin hastane gibi) seçilirse dur
        if BUILDINGS[action] == "hospital":
            break

# Eğitim Sonuçları
print("Q-Tablosu (Öğrenme Sonrası):")
print(q_table)

# Öncelik sırasına göre binaları sıralama
def prioritize_buildings():
    priority = []
    for i, building in enumerate(BUILDINGS):
        total_score = max(q_table[i])
        priority.append((building, total_score))
    return sorted(priority, key=lambda x: x[1], reverse=True)

# Adam atama fonksiyonu
def assign_people_to_buildings(prioritized_buildings):
    people_assignment = {}
    importance_scores = [10, 8, 6, 4, 2, 1]  # Adam atama puanları
    for i, (building, score) in enumerate(prioritized_buildings):
        people_assignment[building] = importance_scores[i] if i < len(importance_scores) else 1
    return people_assignment

# Öncelik sırasını öğren
prioritized_buildings = prioritize_buildings()

# Hastane en öncelikli bina olacak şekilde sıralama
prioritized_buildings = sorted(prioritized_buildings, key=lambda x: (x[0] != "hospital", -x[1]))

# Adamları ata
people_assignment = assign_people_to_buildings(prioritized_buildings)

# Sonuçları yazdır
print("\nBinaların Öncelik Sırası ve Adam Atamaları:")
for building, score in prioritized_buildings:
    print(f"{building.capitalize()}: Öncelik Puanı = {score}, Atanan Adam Sayısı = {people_assignment[building]}")

# Drone'un öğrendiği rota (maksimum ödüller üzerinden)
def get_learned_path():
    state = 0  # Örnek başlangıç durumu
    path = []
    while True:
        action = np.argmax(q_table[state])
        path.append(BUILDINGS[action])
        if BUILDINGS[action] == "hospital" or REWARDS[BUILDINGS[action]] < 0:
            break
        state = action
    return path

print("\nDrone'un öğrendiği rota:")
print(" -> ".join(get_learned_path()))