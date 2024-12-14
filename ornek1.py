import json
import pandas as pd

# Bina türüne göre önem puanları
BUILDING_PRIORITY = {
    "hospital": 100,  # Hastaneler en yüksek önceliğe sahip
    "school": 80,     # Okullar
    "police_station": 90,  # Polis merkezleri
    "shopping_mall": 50,   # Alışveriş merkezleri
    "residential": 30,     # Konutlar
    "other": 10            # Diğer binalar
}

# Örnek bina verileri (JSON formatında bir dosyadan okunabilir)
building_data = [
    {"name": "Hospital A", "type": "hospital", "coordinates": [40.7128, -74.0060]},
    {"name": "School B", "type": "school", "coordinates": [40.7139, -74.0070]},
    {"name": "Police Station C", "type": "police_station", "coordinates": [40.7148, -74.0080]},
    {"name": "Mall D", "type": "shopping_mall", "coordinates": [40.7157, -74.0090]},
    {"name": "Residential E", "type": "residential", "coordinates": [40.7166, -74.0100]},
    {"name": "Other F", "type": "other", "coordinates": [40.7175, -74.0110]}
]

# Bina öncelik puanlarını hesapla
def calculate_priority(building_data):
    for building in building_data:
        building_type = building["type"]
        priority_score = BUILDING_PRIORITY.get(building_type, 0)
        building["priority"] = priority_score
    return building_data

# Öncelik sırasına göre sıralama
def prioritize_buildings(building_data):
    sorted_data = sorted(building_data, key=lambda x: x["priority"], reverse=True)
    return sorted_data

# Çıktıyı görselleştir
def display_priorities(building_data):
    df = pd.DataFrame(building_data)
    print("Bina Öncelik Listesi:")
    print(df[["name", "type", "priority"]])

# Ana akış
def main():
    print("Veriler işleniyor...")
    processed_data = calculate_priority(building_data)
    prioritized_data = prioritize_buildings(processed_data)
    display_priorities(prioritized_data)

# Kodu çalıştır
if __name__ == "__main__":
    main()