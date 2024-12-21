import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 1. Önceden Tanımlı Kelime Puanları
word_scores = {
    "ağır": 10,
    "iç kanama": 10,
    "bilinci kapalı": 9,
    "şok": 9,
    "hayati tehlike": 10,
    "kritik": 9,
    "durumu stabil değil": 9,
    "nabız yok": 10,
    "kan kaybı": 10,
    "solunum durması": 10,
    "orta kırık": 6,
    "travmatik": 6,
    "yanık": 5,
    "kanama": 6,
    "kafa travması": 7,
    "omurga zedelenmesi": 7,
    "ciddi yaralanma": 6,
    "tansiyon düşmesi": 5,
    "bilinç kaybı": 6,
    "nefes darlığı": 6,
    "hafif": 2,
    "çizik": 1,
    "çatlak": 2,
    "kırık": 3,
    "morluk": 1,
    "şişlik": 1,
    "burkulma": 2,
    "sarsıntı": 2,
    "hafif yaralanma": 3,
    "doku zedelenmesi": 2
}

# 2. Eğitim Verisi
data = {
    "message": [
        "15 ağır yaralı, 10 orta düzey yaralı, 28 hafif yaralı.",
        "İç kanamalı hasta, bilinci kapalı.",
        "Hafif çizik ve kırık, 2 kişi hayati tehlike taşımıyor.",
        "Kritik durumda 5 kişi, bir kişinin nabzı yok."
    ],
    "importance_score": [9, 10, 4, 10]
}
df = pd.DataFrame(data)

# 3. TF-IDF Özellik Çıkartma
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df["message"])

# 4. Model Eğitimi (Random Forest Regressor)
y = df["importance_score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 5. Gelen Mesajı İşleme Fonksiyonu
def analyze_message(message):
    # Kelime bazlı puanlama
    words = message.lower().split()
    manual_score = 0
    for word in words:
        if word in word_scores:
            manual_score += word_scores[word]
    
    # Makine öğrenmesi tahmini
    tfidf_vector = tfidf.transform([message])
    ml_score = model.predict(tfidf_vector)[0]
    
    return manual_score, ml_score

# 6. İki Vaka İçin Karşılaştırma
vaka_1 = "10 ağır yaralı, 5 kritik durumda, bilinci kapalı 3 kişi."
vaka_2 = "7 orta kırık, 2 ciddi yaralanma, 15 hafif yaralı."

manual_score_1, ml_score_1 = analyze_message(vaka_1)
manual_score_2, ml_score_2 = analyze_message(vaka_2)

# 7. Karşılaştırma ve Yönlendirme
print("Vaka 1:")
print(f"Mesaj: {vaka_1}")
print(f"Kelime bazlı toplam önem puanı: {manual_score_1}")
print(f"Makine öğrenmesi tahmini önem puanı: {ml_score_1:.2f}\n")

print("Vaka 2:")
print(f"Mesaj: {vaka_2}")
print(f"Kelime bazlı toplam önem puanı: {manual_score_2}")
print(f"Makine öğrenmesi tahmini önem puanı: {ml_score_2:.2f}\n")

if manual_score_1 > manual_score_2:
    print("Kelime bazlı değerlendirmeye göre: Vaka 1 daha acil!")
else:
    print("Kelime bazlı değerlendirmeye göre: Vaka 2 daha acil!")

if ml_score_1 > ml_score_2:
    print("Makine öğrenmesi tahminine göre: Vaka 1 daha acil!")
else:
    print("Makine öğrenmesi tahminine göre: Vaka 2 daha acil!")
