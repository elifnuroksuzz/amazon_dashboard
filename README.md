# Amazon Fine Food Review Analyzer

Amazon Fine Food yorumlarını analiz eden Streamlit tabanlı Python uygulaması. VADER duygu analizi, interaktif grafikler, kelime bulutları ve anahtar kelime arama özellikleri içerir. Kullanıcı puanları ile metin duyguları arasındaki tutarsızlıkları tespit eder.


<img width="1920" height="861" alt="image" src="https://github.com/user-attachments/assets/be8fa634-cfca-4642-81b7-140ff21e8882" />
<img width="1920" height="591" alt="image" src="https://github.com/user-attachments/assets/656a8bfc-8ab8-4673-a70c-ab1d229a7c5d" />
<img width="1920" height="852" alt="image" src="https://github.com/user-attachments/assets/9fd70248-7efb-4e04-b150-cd3febcc5503" />
<img width="1920" height="679" alt="image" src="https://github.com/user-attachments/assets/f2d80560-7e26-4b31-87e8-2bf2472aa2cb" />


## 🍎 Özellikler

- **VADER Duygu Analizi**: Yorum metinlerinde otomatik duygu tespit
- **İnteraktif Dashboard**: Streamlit ile kullanıcı dostu arayüz
- **Görsel Analiz**: Plotly ile interaktif grafikler
- **Kelime Bulutları**: Pozitif ve negatif yorumlarda sık kullanılan kelimeler
- **Anahtar Kelime Arama**: Belirli konularda yorum analizi
- **Tutarsızlık Tespiti**: Puan ve metin duygusu uyumsuzluklarını bulma
- **Zaman Serisi Analizi**: Yorumların zamana göre dağılımı

## 🛠️ Teknolojiler

- **Python**: Ana programlama dili
- **Streamlit**: Web arayüzü ve dashboard
- **NLTK VADER**: Duygu analizi modeli
- **Plotly**: İnteraktif grafik görselleştirme
- **WordCloud**: Kelime bulutu oluşturma
- **Pandas**: Veri işleme ve analiz
- **Matplotlib**: Statik grafik görselleştirme

## 📊 Analiz Modülleri

### `data_loader.py`
- CSV veri yükleme ve ön işleme
- VADER duygu analizi entegrasyonu
- Zaman damgası dönüşümü
- Veri önbellekleme (`@st.cache_data`)

### `analyzer.py`
- Özet metrikleri hesaplama
- Puan dağılımı grafikleri
- Zaman serisi analizi
- Kelime bulutu oluşturma
- Anahtar kelime arama
- Duygu dağılımı analizi

### `app.py`
- Ana Streamlit uygulaması
- Dashboard layout ve etkileşim
- Kullanıcı arayüzü bileşenleri

## 🚀 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install streamlit pandas nltk plotly wordcloud matplotlib
```

2. NLTK VADER verisini indirin:
```python
import nltk
nltk.download('vader_lexicon')
```

3. Veri dosyasını yerleştirin:
   - `data/Reviews.csv` dosyasını proje dizinine ekleyin

4. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## 📱 Kullanım

### Dashboard Ana Sayfası
1. **Genel Bakış**: Toplam yorum, ürün ve kullanıcı sayıları
2. **Puan Dağılımı**: 1-5 yıldız puanlarının grafiksel analizi
3. **Zaman Analizi**: Günlük yorum sayısı trendleri

### Görsel Analiz
- **Kelime Bulutları**: Pozitif ve negatif yorumlarda en sık kullanılan kelimeler
- **İnteraktif Grafikler**: Plotly ile zoom, filter ve hover özellikleri

### Arama ve Filtreleme
- **Anahtar Kelime Arama**: Belirli konularda (coffee, shipping, quality) yorum analizi
- **Ham Veri Görüntüleme**: Kenar çubuğundan veri tablosunu inceleme

### Tutarsızlık Analizi
- **5 Yıldız + Negatif Metin**: Yüksek puan ama olumsuz yorumlar
- **1 Yıldız + Pozitif Metin**: Düşük puan ama olumlu yorumlar

## 📈 Duygu Sınıflandırması

VADER Compound Score sistemine göre:
- **Pozitif**: ≥ 0.05
- **Negatif**: ≤ -0.05  
- **Nötr**: -0.05 < score < 0.05

## 🔧 Veri Formatı

Beklenen CSV sütunları:
- `text`: Yorum metni
- `score`: Kullanıcı puanı (1-5)
- `summary`: Yorum özeti
- `time`: Unix timestamp
- `productid`: Ürün ID
- `userid`: Kullanıcı ID

## 📄 Lisans

Bu proje açık kaynak kodludur.

## 👨‍💻 Geliştirici

**Elif Nur Öksüz**
- 📧 Email: elifnuroksuz4@gmail.com
- 💼 LinkedIn: [linkedin.com/in/elifnuroksuz](https://www.linkedin.com/in/elifnuroksuz/)

---

*Bu proje, e-ticaret yorumlarında veri bilimi ve doğal dil işleme tekniklerinin pratik uygulamasını göstermektedir.*
