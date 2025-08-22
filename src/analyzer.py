# src/analyzer.py
# Gerekli kütüphaneleri içeri aktarıyoruz.
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def calculate_summary_metrics(df):
    """
    Veri setinin genel özet metriklerini hesaplar.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.

    Returns:
        tuple: Toplam yorum, toplam ürün ve toplam kullanıcı sayılarını içeren bir tuple.
    """
    total_reviews = len(df)
    total_products = df['productid'].nunique()
    total_users = df['userid'].nunique()
    return total_reviews, total_products, total_users

def plot_score_distribution(df):
    """
    Yorum puanlarının (score) dağılımını gösteren bir bar grafiği oluşturur.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.

    Returns:
        plotly.Figure: Oluşturulan bar grafiği.
    """
    # 'score' sütunundaki her bir değerin kaç kez tekrarlandığını sayıyoruz.
    score_counts = df['score'].value_counts().sort_index()
    
    # Plotly Express ile interaktif bir bar grafiği oluşturuyoruz.
    fig = px.bar(
        score_counts,
        x=score_counts.index,
        y=score_counts.values,
        title="Yorum Puanlarının Dağılımı",
        labels={'x': 'Puan (Yıldız)', 'y': 'Yorum Sayısı'},
        text=score_counts.values,  # Barların üzerine sayıları yazdırır.
        color=score_counts.index, # Barları puan değerine göre renklendirir.
        color_continuous_scale=px.colors.sequential.Viridis # Renk skalasını belirler.
    )
    # Grafiğin daha okunaklı olması için metin pozisyonunu ayarlıyoruz.
    fig.update_traces(textposition='outside')
    return fig

def plot_reviews_over_time(df):
    """
    Zaman içinde günlük yorum sayısını gösteren bir çizgi grafiği oluşturur.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.

    Returns:
        plotly.Figure: Oluşturulan çizgi grafiği.
    """
    # 'time' sütununu index olarak ayarlıyoruz. Bu, zaman serisi analizlerini kolaylaştırır.
    df_time = df.set_index('time')
    
    # Veriyi günlük olarak yeniden örnekliyoruz (resample) ve her günkü yorum sayısını
    # sayıyoruz (count). Bu, günlük yorum trendini görmemizi sağlar.
    daily_reviews = df_time['score'].resample('D').count()
    
    # Plotly Express ile interaktif bir çizgi grafiği oluşturuyoruz.
    fig = px.line(
        daily_reviews,
        x=daily_reviews.index,
        y=daily_reviews.values,
        title="Zaman İçinde Günlük Yorum Sayısı",
        labels={'x': 'Tarih', 'y': 'Yorum Sayısı'}
    )
    return fig

def create_wordcloud(df, sentiment):
    """
    Belirtilen duyguya sahip yorumlardan bir kelime bulutu oluşturur.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.
        sentiment (str): 'Pozitif' veya 'Negatif'.

    Returns:
        matplotlib.figure.Figure: Oluşturulan kelime bulutunu içeren figür.
    """
    # Duyguya göre veri setini filtreliyoruz.
    # 4 ve 5 yıldızlı yorumları 'Pozitif', 1 ve 2 yıldızlıları 'Negatif' olarak kabul ediyoruz.
    # 3 yıldızlı yorumlar nötr olduğu için bu analizde şimdilik dışarıda bırakıyoruz.
    if sentiment == 'Pozitif':
        subset_df = df[df['score'] >= 4]
        title = "Olumlu Yorumlarda En Sık Geçen Kelimeler"
    elif sentiment == 'Negatif':
        subset_df = df[df['score'] <= 2]
        title = "Olumsuz Yorumlarda En Sık Geçen Kelimeler"
    else:
        return None

    # Yorumların 'text' sütunundaki tüm metinleri tek bir büyük metin bloğu olarak birleştiriyoruz.
    # ' ' (boşluk) ile birleştirerek kelimelerin ayrık kalmasını sağlıyoruz.
    text = " ".join(review for review in subset_df.text)
    
    # Kelime bulutu nesnesini oluşturuyoruz.
    # stopwords='english', 'the', 'a', 'in' gibi anlamsız kelimeleri otomatik olarak çıkarır.
    # max_words, bulutta gösterilecek maksimum kelime sayısını sınırlar.
    # background_color, arka plan rengini belirler.
    wordcloud = WordCloud(
        stopwords='english',
        max_words=100,
        background_color="white",
        width=800,
        height=400
    ).generate(text)

    # Matplotlib kullanarak görseli çizdiriyoruz.
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_title(title, fontsize=20)
    # Eksenleri (x, y koordinatlarını) gizleyerek daha temiz bir görünüm elde ediyoruz.
    ax.axis("off")
    
    return fig

# src/analyzer.py dosyasının en altına ekleyin:

def analyze_keyword(df, keyword):
    """
    Veri setinde belirli bir anahtar kelimeyi içeren yorumları analiz eder.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.
        keyword (str): Aranacak anahtar kelime.

    Returns:
        tuple: Filtrelenmiş DataFrame, bulunan yorum sayısı ve bu yorumların ortalama puanını içeren bir tuple.
    """
    # 'text' sütununda arama yaparken büyük/küçük harf duyarlılığını ortadan kaldırmak için
    # case=False kullanıyoruz. na=False, olası boş (NaN) yorum metinlerinde hata almayı önler.
    filtered_df = df[df['text'].str.contains(keyword, case=False, na=False)]
    
    match_count = len(filtered_df)
    
    # Eğer eşleşen yorum bulunduysa ortalama puanı hesapla, bulunmadıysa 0 olarak ata.
    if match_count > 0:
        average_score = filtered_df['score'].mean()
    else:
        average_score = 0
        
    return filtered_df, match_count, average_score

def plot_sentiment_distribution(df):
    """
    Model tarafından belirlenen duygu (sentiment) etiketlerinin dağılımını
    gösteren bir pasta grafiği (pie chart) oluşturur.

    Args:
        df (pd.DataFrame): Analiz edilecek DataFrame.

    Returns:
        plotly.Figure: Oluşturulan pasta grafiği.
    """
    sentiment_counts = df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Modelin Belirlediği Duygu Dağılımı (VADER)",
        color=sentiment_counts.index,
        color_discrete_map={'Pozitif':'green', 'Negatif':'red', 'Nötr':'royalblue'}
    )
    return fig