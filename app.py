# app.py

# Gerekli kütüphaneleri ve oluşturduğumuz modülleri içeri aktarıyoruz.
import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.analyzer import (
    calculate_summary_metrics, 
    plot_score_distribution, 
    plot_reviews_over_time,
    create_wordcloud,
    analyze_keyword # YENİ EKLENDİ
)

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="Amazon Yorum Analiz Paneli",
    page_icon="📊",
    layout="wide"
)

# --- Ana Başlık ve Veri Yükleme ---
# (Bu kısımlar aynı kalıyor, değişiklik yapmıyoruz)
st.title("📊 Amazon Fine Food Analiz Paneli")
st.markdown("Bu panel, Fine Food yorumlarını analiz etmek ve görselleştirmek için oluşturulmuştur.")
data = load_data(100000)
if data is not None:
    
    # --- Kenar Çubuğu (Sidebar) ---
    # (Bu kısım aynı kalıyor)
    st.sidebar.header("Filtreler ve Ayarlar")
    if st.sidebar.checkbox("Ham Veriyi Göster"):
        st.subheader("Ham Veri Seti")
        rows_to_show = st.sidebar.slider("Görüntülenecek Satır Sayısı", 5, 50, 10)
        st.write(data.head(rows_to_show))

    # --- Dashboard Ana Sayfası ---
    
    st.subheader("Genel Bakış")
    total_reviews, total_products, total_users = calculate_summary_metrics(data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Yorum", f"{total_reviews:,}")
    col2.metric("Toplam Ürün", f"{total_products:,}")
    col3.metric("Toplam Kullanıcı", f"{total_users:,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Yorum Puanlarının Dağılımı")
        fig_score = plot_score_distribution(data)
        st.plotly_chart(fig_score, use_container_width=True)
    with col2:
        st.subheader("Zaman İçinde Yorum Sayısı")
        fig_time = plot_reviews_over_time(data)
        st.plotly_chart(fig_time, use_container_width=True)

    # --- YENİ EKLENEN KISIM: Kelime Bulutları ---
    
    st.markdown("---")
    st.subheader("Yorum İçerik Analizi: Kelime Bulutları")

    # Kelime bulutları hesaplama gerektirdiği için kullanıcıya bir bekleme mesajı göstermek iyi bir pratiktir.
    with st.spinner('Kelime bulutları oluşturuluyor, bu işlem biraz zaman alabilir...'):
        col1, col2 = st.columns(2)
        
        with col1:
            # analyzer modülümüzdeki fonksiyonu 'Pozitif' parametresi ile çağırıyoruz.
            fig_positive_wc = create_wordcloud(data, 'Pozitif')
            # st.pyplot ile matplotlib figürünü Streamlit'e gömüyoruz.
            st.pyplot(fig_positive_wc)

        with col2:
            # analyzer modülümüzdeki fonksiyonu 'Negatif' parametresi ile çağırıyoruz.
            fig_negative_wc = create_wordcloud(data, 'Negatif')
            st.pyplot(fig_negative_wc)
 # --- YENİ EKLENEN KISIM: İnteraktif Anahtar Kelime Arama ---
    
    st.markdown("---")
    st.subheader("🔍 Belirli Bir Kelimeyi Analiz Edin")

    # st.text_input ile kullanıcıdan metin girişi alıyoruz.
    user_input = st.text_input(
        "Yorumlarda aramak istediğiniz bir kelime veya konu girin (örn: coffee, dog, tea, shipping):",
        "" # Başlangıç değeri boş
    )

    # Kullanıcı bir kelime girip Enter'a bastığında bu blok çalışır.
    if user_input:
        with st.spinner(f"'{user_input}' kelimesi içeren yorumlar analiz ediliyor..."):
            # Analiz fonksiyonumuzu çağırıyoruz.
            filtered_df, match_count, average_score = analyze_keyword(data, user_input)

            if match_count > 0:
                st.success(f"**{match_count:,}** adet yorum bulundu.")
                
                col1, col2 = st.columns([1, 2]) # Sütun genişlik oranlarını ayarlıyoruz.
                
                with col1:
                    # Bulunan sonuçlar için özet metrikleri gösteriyoruz.
                    st.metric(
                        label=f"'{user_input}' İçeren Yorumların Ortalama Puanı",
                        value=f"{average_score:.2f} ★" # Sonucu 2 ondalık basamakla formatlıyoruz
                    )
                    
                with col2:
                    # Sadece filtrelenmiş veriye ait puan dağılımını çizdiriyoruz.
                    # Mevcut plot_score_distribution fonksiyonumuzu yeniden kullanıyoruz!
                    fig_keyword_dist = plot_score_distribution(filtered_df)
                    fig_keyword_dist.update_layout(title=f"'{user_input}' İçeren Yorumların Puan Dağılımı")
                    st.plotly_chart(fig_keyword_dist, use_container_width=True)

                # Eşleşen yorumlardan birkaçını örnek olarak gösteriyoruz.
                st.subheader("Eşleşen Yorumlardan Örnekler")
                # Sadece en ilgili sütunları seçerek gösteriyoruz.
                st.dataframe(filtered_df[['summary', 'text', 'score']].head())

            else:
                st.warning(f"'{user_input}' kelimesini içeren hiçbir yorum bulunamadı. Lütfen başka bir kelime deneyin.")

  # --- YENİ EKLENEN KISIM: PUAN-YORUM TUTARSIZLIKLARI ---
    st.markdown("---")
    st.subheader("🕵️‍♀️ Puan ve Yorum Tutarsızlıkları Analizi")
    st.info("Burada, kullanıcının verdiği yıldız puanı ile yapay zeka modelinin metinden anladığı duygunun farklı olduğu ilginç yorumları bulabilirsiniz.")
    
    # Checkbox'lar ile kullanıcıya seçenek sunuyoruz.
    if st.checkbox("5 Yıldızlı Ama Metni 'Negatif' Olan Yorumları Göster"):
        inconsistent_reviews = data[(data['score'] == 5) & (data['sentiment'] == 'Negatif')]
        st.write(f"Toplam {len(inconsistent_reviews)} adet tutarsız yorum bulundu.")
        if not inconsistent_reviews.empty:
            st.dataframe(inconsistent_reviews[['summary', 'text', 'score', 'sentiment']].head())

    if st.checkbox("1 Yıldızlı Ama Metni 'Pozitif' Olan Yorumları Göster"):
        inconsistent_reviews = data[(data['score'] == 1) & (data['sentiment'] == 'Pozitif')]
        st.write(f"Toplam {len(inconsistent_reviews)} adet tutarsız yorum bulundu.")
        if not inconsistent_reviews.empty:
            st.dataframe(inconsistent_reviews[['summary', 'text', 'score', 'sentiment']].head())

