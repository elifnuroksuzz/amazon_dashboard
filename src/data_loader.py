# src/data_loader.py

import pandas as pd
import streamlit as st
# NLTK kütüphanesini ve VADER modelini içeri aktarıyoruz.
from nltk.sentiment.vader import SentimentIntensityAnalyzer

DATA_URL = "data/Reviews.csv"

# Bu fonksiyon, VADER'in ürettiği skoru alıp etiket döndürecek.
def classify_sentiment(compound_score):
    """VADER'in compound skorunu Pozitif, Negatif veya Nötr olarak sınıflandırır."""
    if compound_score >= 0.05:
        return 'Pozitif'
    elif compound_score <= -0.05:
        return 'Negatif'
    else:
        return 'Nötr'

@st.cache_data
def load_data(nrows):
    """
    Amazon yorum veri setini yükler ve her yorum için duygu analizi yapar.
    """
    try:
        data = pd.read_csv(DATA_URL, nrows=nrows)
        data.columns = data.columns.str.lower()
        data['time'] = pd.to_datetime(data['time'], unit='s')

        # --- YENİ EKLENEN DUYGU ANALİZİ BÖLÜMÜ ---
        
        # VADER analizcisini başlatıyoruz.
        sia = SentimentIntensityAnalyzer()
        
        # 'text' sütunundaki her yorum için VADER'in polarity skorlarını hesaplıyoruz.
        # .apply() metodu ve bir lambda fonksiyonu ile bu işlemi tüm satırlara verimli bir şekilde uyguluyoruz.
        # Önce metnin str olduğundan emin oluyoruz.
        data['sentiment_scores'] = data['text'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])
        
        # Hesapladığımız 'compound' skorunu etiketlere dönüştürüyoruz.
        data['sentiment'] = data['sentiment_scores'].apply(classify_sentiment)
        
        # Artık skor sütununa ihtiyacımız kalmadı, silebiliriz.
        data.drop(columns=['sentiment_scores'], inplace=True)
        
        return data
    except FileNotFoundError:
        st.error(f"HATA: '{DATA_URL}' adresinde veri dosyası bulunamadı.")
        return None
    except Exception as e:
        st.error(f"Veri işlenirken bir hata oluştu: {e}")
        return None