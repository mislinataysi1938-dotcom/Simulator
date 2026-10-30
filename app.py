import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Class Simulator", page_icon="📚", layout="centered"
)

st.title("🎓 Smart Pedagogy Class: Sınıf ve Öğretim Simülatörü")
st.markdown(
    "Ortaokul matematik öğretmenliği adayları için senaryo tabanlı sınıf"
    " yönetimi ve pedagojik karar simülasyonu."
)

# Yan Menü - Simülasyon Ayarları
st.sidebar.header("⚙️ Simülasyon Ayarları")
ogretmen_adi = st.sidebar.text_input("Öğretmen Adayı Adı", "Öğretmen Adayı")
sinif_duzeyi = st.sidebar.selectbox(
    "Sınıf Düzeyi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"]
)
matematik_konusu = st.sidebar.selectbox(
    "Matematik Konusu",
    [
        "Oran ve Orantı (Oran Tahtası)",
        "3D Hacim ve Cisimler (Willy Wonka Senaryosu)",
        "Kesirlerde İşlemler ve Kavram Yanılgıları",
    ],
)

st.divider()

# Senaryo Alanı
st.subheader(f"📖 Senaryo: {matematik_konusu} ({sinif_duzeyi})")

if "Oran ve Orantı" in matematik_konusu:
  st.info(
      "**Durum:** Derste oran tahtası ve renkli boncuklar kullanıyorsunuz. 7."
      " sınıf öğrencisi Mert parmak kaldırıp şöyle diyor: *'Öğretmenim, iki"
      " katı kadar boncuk alırsak fiyat da iki katına çıkıyor ama ben toptan"
      " alımda indirim beklerdim, neden hep doğru orantı kurmak zorundayız?'*"
  )

  secim = st.radio(
      "Bu durumda pedagojik olarak nasıl bir yaklaşım sergilersiniz?",
      [
          (
              "A) 'Matematiksel modeller günlük hayatın her detayını birebir"
              " yansıtmaz, bu yüzden kurala uymalıyız' de."
          ),
          (
              "B) Öğrencinin eleştirel düşüncesini takdir edip, gerçek hayattaki"
              " indirim/kampanya durumlarını sınıfta tartışmaya aç."
          ),
          (
              "C) Soruyu görmezden gelip müfredattaki standart oran-orantı"
              " problemlerine devam et."
          ),
      ],
  )

  if st.button("Değerlendir ve Geri Bildirim Al"):
    if "B)" in secim:
      st.success(
          "🌟 **Harika Yaklaşım! (Yapılandırmacı ve Süreç Odaklı Yaklaşım)**"
          " Öğrencinin kavramsal sorgulamasını avantaja çevirdiniz. Gerçek"
          " yaşam bağlamı kurarak matematik okuryazarlığını desteklediniz."
      )
    else:
      st.warning(
          "⚠️ **Geliştirilebilir:** Öğrencinin bilişsel merakını ve günlük"
          " hayat bağlantısını göz ardı etmek motivasyonu düşürebilir."
      )

elif "3D Hacim" in matematik_konusu:
  st.info(
      "**Durum:** Willy Wonka'nın çikolata fabrikası temalı hacim ölçme"
      " dersindesiniz. Öğrenciler birim küplerle farklı kutu tasarımları"
      " yapıyor. Bir grup, taban alanı aynı kalıp yüksekliği iki katına çıkan"
      " kutunun hacminin de iki katına çıkacağını fark ediyor."
  )

  ogrenci_notu = st.text_area(
      "Bu keşfi pekiştirmek için tahtaya veya dijital simülasyona ne yazar ya"
      " da sorarsınız?"
  )
  if st.button("Öneriyi Kaydet"):
    if ogrenci_notu:
      st.success(
          "✅ Pedagojik öneriniz kaydedildi! Somut nesnelerden dijital araçlara"
          " geçiş için harika bir köprü kurdunuz."
      )
    else:
      st.error("Lütfen pedagojik stratejinizi ifade eden bir not girin.")

else:
  st.info(
      "**Durum:** Öğrenciler kesirlerde bölme işleminde 'ters çevir çarp'"
      " kuralını ezberlemiş ancak nedenini açıklayamıyorlar."
  )
  st.markdown(
      "💡 **Öneri:** Somut bir malzeme (örneğin pizza dilimleri veya ölçü"
      " kapları) kullanarak sezgisel bir açıklama yapmanız önerilir."
  )

st.divider()
st.caption("Smart Pedagogy Class v1.0 • Öğretmen Adayı Gelişim Modülü")
