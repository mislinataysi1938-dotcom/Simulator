import streamlit as st
import random
import pandas as pd

# ==============================================================================
# 1. UYGULAMA VE SAYFA YAPILANDIRMASI
# ==============================================================================
st.set_page_config(
    page_title="TYMM 2026 Tam Müfredat & Rubrik Uyumlu Staj Simülatörü",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. OTURUM DURUMU (SESSION STATE) YÖNETİMİ
# ==============================================================================
# Sayfa yenilendiğinde veya kullanıcı etkileşiminde verilerin sıfırlanmaması için
# Streamlit'in session_state mekanizması kullanılır.

if 'simulasyon_asamasi' not in st.session_state:
    st.session_state.simulasyon_asamasi = 1

if 'secilen_sinif' not in st.session_state:
    st.session_state.secilen_sinif = 7

if 'secilen_tema' not in st.session_state:
    st.session_state.secilen_tema = "MAT.7.1. Sayılar ve Nicelikler (Oran-Orantı)"

if 'puan' not in st.session_state:
    st.session_state.puan = 50  # Nötr başlangıç puanı

if 'mesajlar' not in st.session_state:
    # İlk varsayılan öğrenci sorusu (Oran Tahtası ve somut materyal kullanımı bağlamı)
    st.session_state.mesajlar = [
        {
            "role": "student", 
            "content": "Öğretmenim, oran tahtasındaki boncuk sayısını artırdığımda mesafe de artıyor ama doğru mu yapıyorum emin olamadım..."
        }
    ]

# ==============================================================================
# 3. YAN MENÜ (SIDEBAR): MÜFREDAT VE ÖĞRENCİ PROFİLİ
# ==============================================================================
st.sidebar.header("🎯 Simülasyon Parametreleri")

# Sınıf Seviyesi Seçimi
secilen_sinif = st.sidebar.selectbox(
    "Sınıf Düzeyi Seçin", 
    [5, 6, 7, 8], 
    index=2  # Varsayılan: 7. Sınıf
)

# Türkiye Yüzyılı Maarif Modeli 5-8. Sınıf Müfredat Temaları
tema_haritasi = {
    5: [
        "MAT.5.1. Sayılar ve Nicelikler", 
        "MAT.5.2. İşlemlerle Cebirsel Düşünme", 
        "MAT.5.3. Geometrik Şekiller",
        "MAT.5.4. Geometrik Nicelikler",
        "MAT.5.5. İstatistiksel Araştırma Süreci"
    ],
    6: [
        "MAT.6.1. Sayılar ve Nicelikler", 
        "MAT.6.2. Cebirsel Düşünme ve Değişimler", 
        "MAT.6.3. Geometrik Şekiller",
        "MAT.6.4. Geometrik Nicelikler",
        "MAT.6.5. İstatistiksel Araştırma Süreci"
    ],
    7: [
        "MAT.7.1. Sayılar ve Nicelikler (Oran-Orantı)", 
        "MAT.7.2. Cebirsel Düşünme ve Değişimler", 
        "MAT.7.3. Dönüşüm",
        "MAT.7.4. Geometrik Nicelikler",
        "MAT.7.5. Geometrik Şekiller"
    ],
    8: [
        "MAT.8.1. Sayılar ve Nicelikler (Üslü/Kareköklü)", 
        "MAT.8.2. Cebirsel Düşünme (Doğrusal Fonksiyonlar)", 
        "MAT.8.3. Geometrik Şekiller (Pisagor/Benzerlik)",
        "MAT.8.4. Geometrik Nicelikler (Hacim/Yüzey Alanı)",
        "MAT.8.5. Dönüşüm Geometrisi"
    ]
}

secilen_tema = st.sidebar.selectbox(
    "Tema Seçin (TYMM 2026)", 
    tema_haritasi.get(secilen_sinif, ["MAT.7.1. Sayılar ve Nicelikler"])
)

# Öğrenci Profil Kartı (Rehberlik ve Vaka Analizi Verileri)
st.sidebar.markdown("---")
st.sidebar.subheader("👤 Vaka Öğrenci Profili (STU-1309)")
st.sidebar.info(
    "**Yaş / Sınıf:** 13 Yaş | 7. Sınıf\n\n"
    "**Sosyal / Hobi:** Görsel Sanatlar Kulübü, Kitap Yazma, Polis Olma Hedefi\n\n"
    "**Pedagojik Profil:** Somut materyallerle (Oran Tahtası, Birim Küpler) ve keşfederek öğrenmeyi tercih eder. "
    "Doğrudan kural veya ezber formül verilmesine karşı direnç gösterir."
)

# ==============================================================================
# 4. ANA EKRAN VE CANLI CANLI DİYALOG AKIŞI
# ==============================================================================
st.title("📐 TYMM 2026 Sanal Sınıf Staj Simülatörü")
st.caption("Senior Öğretmen Adayı Sınıf Yönetimi ve Yapılandırmacı Pedagoji Pratik Alanı")
st.markdown("---")

st.subheader(f"💬 Canlı Etkileşim Alanı ({secilen_sinif}. Sınıf | {secilen_tema})")

# Geçmiş konuşma balonlarının ekrana çizdirilmesi
for mesaj in st.session_state.mesajlar:
    if mesaj["role"] == "student":
        with st.chat_message("student", avatar="🧑‍🎓"):
            st.write(f"**Öğrenci (13 yaş):** {mesaj['content']}")
    else:
        with st.chat_message("teacher", avatar="👩‍🏫"):
            st.write(f"**Öğretmen Adayı:** {mesaj['content']}")

# Öğretmen Adayı Metin Girdi Kutusu
ogretmen_girdisi = st.chat_input("Öğrenciye rehberlik edecek sorunuzu veya yönlendirmenizi buraya yazın...")

# ==============================================================================
# 5. PEDAGOJİK DEĞERLENDİRME VE ÖĞRENCİ TEPKİ MOTORU
# ==============================================================================
if ogretmen_girdisi:
    # 1. Öğretmenin yanıtını diyaloğa kaydet
    st.session_state.mesajlar.append({"role": "teacher", "content": ogretmen_girdisi})
    
    # 2. Metin Analizi (Anahtar Kelime ve Pedagoji Denetimi)
    girdi_kucuk = ogretmen_girdisi.lower()
    
    # Olumsuz Pedagojik Örüntü: Doğrudan Formül / Kural / Ezber Aktarımı
    dogrudan_formul = any(k in girdi_kucuk for k in ["formül", "ezberle", "çarp geç", "kural şu", "topla geç", "direk yap"])
    
    # Olumlu Pedagojik Örüntü: Yönlendirici Soru / Somut Temsil Kullanımı
    rehberlik_sorusu = any(k in girdi_kucuk for k in ["ne fark ettin", "nasıl değişti", "inceleyelim", "boncuk", "ilişki", "neden", "tahta"])
    
    # Olumlu Bilişsel Bağlam: Öğrencinin Kişisel İlgilerini Bağlama Katma
    ilgi_entegrasyonu = any(k in girdi_kucuk for k in ["görsel", "sanat", "polis", "kitap", "çizim"])

    # 3. Pedagojik Puanlama ve Öğrenci Yanıt Mantığı
    if dogrudan_formul:
        st.session_state.puan -= 15
        ogrenci_tepkisi = "Öğretmenim, ezberlemek yerine tahtadaki boncukları hareket ettirerek anlamak istiyordum..."
        st.warning("⚠️ **Pedagojik Uyarı (Maarif Modeli):** Doğrudan kural/formül aktarımı yapılandırmacı yaklaşım ile çelişmektedir. Öğrencinin kavramı kendisinin keşfetmesini sağlayın.")
        
    elif rehberlik_sorusu:
        st.session_state.puan += 20
        ogrenci_tepkisi = "Anladım öğretmenim! Boncuk sayısı 2 katına çıkınca aradaki mesafe de 2 katına çıkıyor, yani kat oranı sabit kalıyor!"
        st.success("✨ **Harika Rehberlik!** Somut temsil ve yönlendirici açık uçlu sorularla kavramsal derinleşme sağlandı.")
        
    else:
        ogrenci_tepkisi = "Anlamaya çalışıyorum öğretmenim, biraz daha açık ifade edebilir misiniz?"
        st.info("💡 **İpucu:** Öğrencinin Oran Tahtası üzerindeki değişimi kendi kelimeleriyle keşfetmesini sağlayacak yönlendirici sorular sorun.")

    # İlgilerin derse entegrasyonu bonusu
    if ilgi_entegrasyonu:
        st.session_state.puan += 10
        ogrenci_tepkisi += " (Ayrıca bunu çizimlerimde oran kurmaya benzetmek çok hoşuma gitti!)"

    # Puanı 0 ile 100 arasında sınırla
    st.session_state.puan = max(0, min(100, st.session_state.puan))

    # 4. Öğrencinin cevabını diyaloğa kaydet ve arayüzü güncelle
    st.session_state.mesajlar.append({"role": "student", "content": ogrenci_tepkisi})
    st.rerun()

# ==============================================================================
# 6. SÜREÇ ODAKLI CANLI EVALUATION RUBRİĞİ (SIDEBAR ALT KISIM)
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Canlı Performans Rubriği")

# Puan Göstergesi
st.sidebar.metric(
    label="Pedagojik Yetkinlik Puanı", 
    value=f"{st.session_state.puan} / 100"
)
st.sidebar.progress(st.session_state.puan / 100)

# Sıfırlama Butonu
if st.sidebar.button("🔄 Simülasyonu Sıfırla", use_container_width=True):
    st.session_state.puan = 50
    st.session_state.mesajlar = [
        {
            "role": "student", 
            "content": "Öğretmenim, oran tahtasındaki boncuk sayısını artırdığımda mesafe de artıyor ama doğru mu yapıyorum emin olamadım..."
        }
    ]
    st.rerun()
