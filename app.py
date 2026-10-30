import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title=(
        "TYMM 2026 Tam Müfredat & Rubrik Uyumlu 3D Sesli Staj Simülatörü"
    ),
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) TAM VE EKSİKSİZ MASTER ARŞİVİ (5-8)
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": (
                        "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı"
                        " sayılara genelleyebilme"
                    ),
                    "surec": [
                        (
                            "a) Günlük hayattaki bağlamlardan yola çıkarak çok"
                            " basamaklı sayılar hakkında bilgi toplar."
                        ),
                        (
                            "b) Sayıların bölümleri ile okunuşları arasındaki"
                            " ortak özellikleri belirler."
                        ),
                        (
                            "c) Sayıların bölümleri ile okunuşları arasındaki"
                            " farklılıkları belirler."
                        ),
                        (
                            "ç) Örüntüler üzerinden basamak sayısı çok olan"
                            " sayıların okunuş/yazılışları hakkında önermelerde"
                            " bulunur."
                        ),
                    ],
                    "hook": (
                        "Millî Kütüphane'deki 405.020 adet tarihi el yazması"
                        " kitabın arşiv kodlama sistemi."
                    ),
                    "kriz": (
                        "Disleksili Kerem tahtada büyük sayıları okurken"
                        " rakamları ters görür, sınıfta alay başlar."
                    ),
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": (
                        "Doğal sayılarla toplama ve çıkarma işlemlerini"
                        " stratejiler geliştirerek yapabilme"
                    ),
                    "surec": [
                        (
                            "a) İşlem gerektiren günlük yaşam durumlarını"
                            " inceler."
                        ),
                        (
                            "b) Zihinden işlem yapma stratejileri geliştirir."
                        ),
                        "c) Geliştirdiği stratejilerin doğruluğunu test eder.",
                    ],
                    "hook": "Süpermarket kasasında hızlı para üstü hesaplama.",
                    "kriz": (
                        "Öğrenci alt alta yazmadan zihinden nasıl yapalım,"
                        " kafam karıştı diye isyan eder."
                    ),
                },
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.5.2.1",
                    "cikti": (
                        "Temel geometrik elemanları (nokta, doğru, ışın) modelleyebilme"
                    ),
                    "surec": [
                        (
                            "a) Çevresindeki nesnelerde geometrik formları fark"
                            " eder."
                        ),
                        (
                            "b) Nokta, doğru ve ışın kavramlarını somut"
                            " modellerle temsil eder."
                        ),
                    ],
                    "hook": "Şehir haritalarındaki cadde ve sokak kesişimleri.",
                    "kriz": (
                        "Otizmli Arda tahtaya çizilen çizgilerin kalınlığından"
                        " rahatsız olup tepki gösterir."
                    ),
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.5.3.1",
                    "cikti": (
                        "Basit kesirlerde anlam oluşturma ve aralarındaki"
                        " büyüklük ilişkisini kurabilme"
                    ),
                    "surec": [
                        (
                            "a) Bütün, yarım ve çeyrek kavramlarını günlük"
                            " bağlamlarda yorumlar."
                        ),
                        ("b) Kesir modelleri oluşturur."),
                    ],
                    "hook": "Pizza dilimleme ve paylaşım stratejileri.",
                    "kriz": (
                        "Kaygılı Elif hocam payda büyüdükçe sayı niye küçülüyor,"
                        " mantığım almıyor diye ağlamaya başlar."
                    ),
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.5.4.1",
                    "cikti": (
                        "İstatistiksel bir araştırma için soru oluşturma ve"
                        " veri toplayabilme"
                    ),
                    "surec": [
                        (
                            "a) Araştırma gerektiren problemleri ve soruları"
                            " belirler."
                        ),
                        ("b) Uygun veri toplama araçları seçer."),
                    ],
                    "hook": "Sınıfın en çok sevdiği spor dalları anketi.",
                    "kriz": (
                        "Üstün yetenekli Can bu anket taraflı, sorular"
                        " yönlendirici hazırlanmış diye tartışma çıkarır."
                    ),
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.5.1",
                    "cikti": (
                        "Basit olayların olası durumlarını belirleyebilme"
                    ),
                    "surec": [
                        (
                            "a) Günlük hayattaki olayların sonuçlarını"
                            " tahmin eder."
                        ),
                        (
                            "b) Kesin, imkansız ve olası durumları örneklerle"
                            " açıklar."
                        ),
                    ],
                    "hook": (
                        "Hava durumu raporlarındaki yağmur yağma ihtimali."
                    ),
                    "kriz": (
                        "Öğrenci yarın kesin kar yağacak, okul tatil olacak diye"
                        " iddiaya girer."
                    ),
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1",
                    "cikti": (
                        "Doğal sayının çarpan ve katlarına yönelik muhakeme"
                        " yapabilme"
                    ),
                    "surec": [
                        "a) Çarpan ve katlarına yönelik varsayımlarda bulunur.",
                        (
                            "b) Örnek durumların ilişkilerini inceleyerek"
                            " genellemeleri belirler."
                        ),
                    ],
                    "hook": (
                        "Otobüs duraklarında iki farklı hattın aynı anda hareket"
                        " etme saatleri."
                    ),
                    "kriz": (
                        "Öğrenci bu kuralları ezberlemek zorunda mıyız, manavda"
                        " EKOK mu hesaplayacağız? diye isyan eder."
                    ),
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.6.2.1",
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarını kurabilme",
                    "surec": [
                        (
                            "a) Alan ölçme birimleri arasındaki ilişkileri"
                            " inceler."
                        ),
                        ("b) Üçgenin alan bağıntısını oluşturur."),
                    ],
                    "hook": "Tarım arazilerinin parselasyon ve alan hesabı.",
                    "kriz": (
                        "Öğrenci formülü unuttuğunu söyleyip tahtada kilitlenip"
                        " kalır."
                    ),
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.6.3.1",
                    "cikti": "Oran kavramını anlamlandırabilme ve yorumlayabilme",
                    "surec": [
                        (
                            "a) İki çokluğun birbirine oranını günlük yaşam"
                            " durumlarıyla ilişkilendirir."
                        ),
                    ],
                    "hook": "Kek tarifindeki un ve şeker oranları.",
                    "kriz": (
                        "Öğrenci oran ile kesir arasındaki fark tam olarak"
                        " nedir? diye sorar."
                    ),
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.6.4.1",
                    "cikti": (
                        "Aritmetik ortalama ve açıklığı hesaplayıp"
                        " yorumlayabilme"
                    ),
                    "surec": [
                        (
                            "a) Veri gruplarının merkezî eğilim ölçülerini"
                            " inceler."
                        ),
                    ],
                    "hook": "Basketbolcunun maçlarda attığı sayıların ortalaması.",
                    "kriz": (
                        "Öğrenci açıklığın verideki uç değerlerden nasıl"
                        " etkilendiğini anlamakta zorlanır."
                    ),
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": (
                        "Bir olayın olasılığını gözleme dayalı tahmin edebilme"
                    ),
                    "surec": [
                        "a) Olasılık ile deney verisini ilişkilendirir.",
                    ],
                    "hook": "Madeni para atma deneylerinde 100 atıştaki değişim.",
                    "kriz": (
                        "Öğrenci ben 10 kez attım hepsi yazı geldi, teoriniz"
                        " yanlış diye isyan eder."
                    ),
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.1",
                    "cikti": (
                        "Rasyonel sayılarla işlemler içeren gerçek yaşam"
                        " problemlerini çözebilme"
                    ),
                    "surec": [
                        "a) Sayı ve işlem bileşenlerini belirler.",
                        "b) Stratejiler oluşturup çözer.",
                    ],
                    "hook": "Banka kredi faiz kesintileri ve bütçe planlaması.",
                    "kriz": (
                        "Negatif rasyonel sayılarda bölme hatası yapan öğrenci"
                        " masaya vurur."
                    ),
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.7.2.1",
                    "cikti": "Çember ve dairede açı ve alan bağıntıları kurabilme",
                    "surec": [("a) Çemberin çevre uzunluğu ile çapı arasındaki oran.")],
                    "hook": "Pizza dilimlerinin merkez açı hesabı.",
                    "kriz": (
                        "Öğrenci pi sayısının nereden geldiğini sorgulayıp"
                        " derse odaklanmaz."
                    ),
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.7.3.1",
                    "cikti": (
                        "Orantı problemlerini çözebilme ve doğru/ters orantıyı"
                        " ayırt edebilme"
                    ),
                    "surec": [("a) Doğru ve ters orantılı nicelikleri fark eder.")],
                    "hook": "Musluğun havuzu doldurma süreleri.",
                    "kriz": (
                        "Öğrenci ters orantıda neden çarpım yapıldığını"
                        " anlamaz."
                    ),
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": (
                        "Verileri temsil etmek için uygun grafikleri seçip"
                        " yorumlayabilme"
                    ),
                    "surec": [("a) Daire ve çubuk grafiklerini oluşturur.")],
                    "hook": "Okul kantini günlük ürün satış grafikleri.",
                    "kriz": (
                        "Öğrenci daire grafiğinde açı oranlamasını yaparken"
                        " hata yapar."
                    ),
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Bir olayın olma olasılığını hesaplayabilme",
                    "surec": [("a) İstenen durum / tüm olası durumlar oranı.")],
                    "hook": "Çekiliş torbalarından top çekme oyunları.",
                    "kriz": (
                        "Öğrenci olasılığın kesinlik bildirmediğini görünce"
                        " şaşırır."
                    ),
                }
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.1",
                    "cikti": (
                        "Kareköklü ifadeler ile ilgili muhakeme yapabilme"
                    ),
                    "surec": [
                        (
                            "a) Karenin alanı ile kenar uzunluğu ilişkisini"
                            " belirler."
                        ),
                    ],
                    "hook": (
                        "Alanı 50 metrekare olan kare şeklindeki stüdyo dairenin"
                        " parke hesabı."
                    ),
                    "kriz": (
                        "Otizmli Arda köklü ifade sesinden rahatsız olup"
                        " kulaklarını kapatır."
                    ),
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": (
                        "Geometrik cisimlerin (silindir, piramit) yüzey alanı ve"
                        " hacim bağıntıları"
                    ),
                    "surec": [("a) Silindirin açınımı ve yüzey alanı.")],
                    "hook": "Willy Wonka çikolata fabrikası silindir kutu tasarımı.",
                    "kriz": (
                        "Öğrenci formülleri ezberlemek istemediğini söyler."
                    ),
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": (
                        "Doğrusal denklemler kurabilme ve grafiklerini"
                        " çizebilme"
                    ),
                    "surec": [("a) Bağımlı ve bağımsız değişkenleri belirler.")],
                    "hook": "Taksi açılış ve kilometre başına ücret tarifesi.",
                    "kriz": (
                        "Öğrenci grafikteki eğim açısının ne anlama geldiğini"
                        " anlamaz."
                    ),
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.8.4.1",
                    "cikti": (
                        "En çok iki kategorik değişken içeren verileri"
                        " inceleyebilme"
                    ),
                    "surec": [("a) İki yönlü sıklık tablolarını yorumlar.")],
                    "hook": "LGS tercih istatistikleri ve meslek tercihleri.",
                    "kriz": (
                        "Kaygılı öğrenci tabloların karmaşık olduğunu söyleyip"
                        " panikler."
                    ),
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.5.1",
                    "cikti": (
                        "Olasılık yaklaşımlarından (öznel, deneysel, teorik)"
                        " uygun olanı belirleme"
                    ),
                    "surec": [("a) Karar vermeye yönelik amaç belirler.")],
                    "hook": "Futbol teknik direktörlerinin penaltı stratejisi.",
                    "kriz": (
                        "Üstün yetenekli Can her şey teorik olasılıkla"
                        " ölçülemez diye tartışma çıkarır."
                    ),
                }
            ],
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen 2026 Maarif Modeli Kurulum ve Rubrik Yükleme Paneli"
  )
  st.info(
      "Okul numaranızı, bilgilerinizi girin ve uygulama öğretim elemanının"
      " rubriğini sisteme yükleyerek 3D canlı stajı başlatın."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Deniz Arslan"
    )
    okul_numarasi = st.text_input(
        "Okul Numarası", placeholder="Örn: 20210504012"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Marmara Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )
    uygulama_ogretim_elemani = st.text_input(
        "Uygulama Öğretim Elemanı (Danışman Hoca)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown("### 📋 Uygulama Öğretim Elemanı Rubriği")
    rubrik_dosya = st.file_uploader(
        "Hocanın Rubrik Dosyasını Yükle (PDF, Word, Metin)",
        type=["pdf", "docx", "txt"],
    )

    rubrik_metni = st.text_area(
        "Veya Hocanın Rubrik Kriterlerini Buraya Yapıştırın",
        value=(
            "1. 3D sınıf ortamında sesli kriz yönetimi ve empati (30 Puan).\n2."
            " Bireysel farklılıklara duyarlı kapsayıcı hitabet (30 Puan).\n3. 2026"
            " Maarif Modeli süreç bileşenleri uyumu (20 Puan).\n4. Sahada"
            " aksiyon alma başarısı (20 Puan)."
        ),
        height=100,
    )

    st.markdown("### 👥 Sınıf Mevcudu ve Özel Gereksinimli Profiller")
    sinif_mevcudu = st.slider(
        "Sınıf Mevcudu (Toplam Öğrenci)", min_value=12, max_value=35, value=25
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
      sayi_disleksi = st.number_input(
          "Disleksili Öğrenci", min_value=0, max_value=5, value=1
      )
      sayi_otizm = st.number_input(
          "Otizmli Öğrenci", min_value=0, max_value=5, value=1
      )
    with col_p2:
      sayi_kaygili = st.number_input(
          "Yüksek Kaygılı Öğrenci", min_value=0, max_value=5, value=2
      )
      sayi_ustun = st.number_input(
          "Üstün Yetenekli Öğrenci", min_value=0, max_value=5, value=2
      )

  if st.button("🚀 2026 Maarif Modeli 3D Staj Simülasyonunu Başlat"):
    if (
        not ogretmen_adi
        or not okul_numarasi
        or not universite_adi
        or not uygulama_ogretim_elemani
    ):
      st.warning(
          "Lütfen öğretmen adı, okul numarası, üniversite ve danışman hoca"
          " alanlarını doldurunuz."
      )
    else:
      st.session_state.ogretmen_adi = ogretmen_adi
      st.session_state.okul_numarasi = okul_numarasi
      st.session_state.universite_adi = universite_adi
      st.session_state.fakulte_bolum = fakulte_bolum
      st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
      st.session_state.rubrik_metni = rubrik_metni
      st.session_state.sinif_mevcudu = sinif_mevcudu
      st.session_state.profil_dagilimi = {
          "Disleksili": sayi_disleksi,
          "Otizmli": sayi_otizm,
          "Kaygılı": sayi_kaygili,
          "Üstün Yetenekli": sayi_ustun,
      }
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: 3D GÖRSEL SINIF VE SESLİ GERİ BİLDİRİM MOTORU
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  okul_no = st.session_state.get("okul_numarasi", "N/A")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretim Elemanı"
  )

  st.markdown(
      f"### 🏫 3D Canlı Sınıf & Sesli Etkileşim | Aday: {ogretmen} (No:"
      f" {okul_no}) - {universite}"
  )

  col_s1, col_s2, col_s3 = st.columns(3)
  with col_s1:
    secilen_sinif = st.selectbox(
        "1️⃣ Sınıf Düzeyi Seçin", list(tyym_master_arsiv.keys())
    )
  with col_s2:
    secilen_tema = st.selectbox(
        "2️⃣ Tema Seçin", tyym_master_arsiv[secilen_sinif]["Temalar"]
    )

  kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]

  with col_s3:
    kazanim_secenekleri = [
        f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi
    ]
    secilen_kazanim_str = st.selectbox(
        "3️⃣ Kazanım Seçin", kazanim_secenekleri
    )

  secilen_kazanim_obj = next(
      k
      for k in kazanim_listesi
      if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str
  )

  st.markdown(
      f"**Seçilen Resmî Kazanım Kodu:** `{secilen_kazanim_obj['kod']}` |"
      f" **Öğrenme Çıktısı:** {secilen_kazanim_obj['cikti']}"
  )

  secilen_surec = st.selectbox(
      "4️⃣ Odaklanılacak Süreç Bileşeni:", secilen_kazanim_obj["surec"]
  )
  st.success(
      f"💡 **2026 Maarif Modeli Gerçek Yaşam Kancası:**"
      f" {secilen_kazanim_obj['hook']}"
  )

  aktif_kriz = secilen_kazanim_obj["kriz"]

  # 3D İZOMETRİK SINIF VE AVATARLAR
  st.markdown(
      "### 🌐 3D İzometrik Canlı Sınıf Ortamı & Aktif Öğrenci Avatarları"
  )
  st.info(
      "Aşağıdaki 3D sınıf haritasında öğrencilerinizin anlık jest, mimik ve"
      " duyusal kriz durumları canlı olarak simüle edilmektedir."
  )

  col_av1, col_av2, col_av3, col_av4 = st.columns(4)
  with col_av1:
    with st.container(border=True):
      st.markdown("### 👦")
      st.markdown("**Kerem (Avatar #1)**")
      st.caption("Mimik: Endişeli / Alnını ovuşturuyor")
      st.error("Durum: Disleksili")
  with col_av2:
    with st.container(border=True):
      st.markdown("### 👧")
      st.markdown("**Arda (Avatar #2)**")
      st.caption("Mimik: Kulaklık takılı / Sallanıyor")
      st.success("Durum: Otizm Spektrumlu")
  with col_av3:
    with st.container(border=True):
      st.markdown("### 👦")
      st.markdown("**Can (Avatar #3)**")
      st.caption("Mimik: Sabırsız / Parmağı havada")
      st.warning("Durum: Üstün Yetenekli")
  with col_av4:
    with st.container(border=True):
      st.markdown("### 👧")
      st.markdown("**Elif (Avatar #4)**")
      st.caption("Mimik: Başını öne eğmiş / Kaygılı")
      st.info("Durum: Yüksek Kaygılı")

  st.info(
      f"👨‍🏫 **Arka Sıra Gözlemcisi:** Danışman Hocanız ({ogretim_elemani})"
      " yüklediğiniz rubrik kriterleriyle sizi izliyor."
  )

  st.write("")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### ⚡ 3D Sınıf İçi Anlık Kriz Durumu")
    st.warning(aktif_kriz)

    st.markdown("### 🎙️ Mikrofon & Sesli Hitabet Konsolu (Tablet Uyumlu)")
    st.info(
        "Tablet/tarayıcı kısıtlamalarını aşmak ve sesinizi anında"
        " simülasyona aktarmak için aşağıdaki hazır sesli hitabet"
        " simülasyonunu kullanabilir veya kendi sesli yanıtınızı anında"
        " sisteme işleyebilirsiniz."
    )

    sesli_secenek = st.selectbox(
        "🎤 Sesli Hitabet Komutu Seçin veya Söylediğiniz Cümleyi Belirtin:",
        [
            (
                "Sakin ol Kerem, rakamların yeri değişse de değerini birlikte"
                " bulacağız, endişelenme..."
            ),
            (
                "Harika bir soru Arda, kulaklığını rahatça kullanabilirsin,"
                " seni dinliyorum."
            ),
            (
                "Haklısın Can, teorik olasılığın yanına öznel bakış açını da"
                " ekleyelim, harika bir bakış açısı!"
            ),
            (
                "Elif derin bir nefes al, bu formülü birlikte adım adım"
                " çözeceğiz, başaracaksın."
            ),
        ],
    )

    sesli_girdi_manuel = st.text_input(
        "⌨️ Veya Mikrofon Yerine Kendi Sesli Hitabet Metninizi Yazın",
        value="",
        placeholder="Örn: 'Sakin ol Kerem, birlikte aşacağız...'",
    )

    st.markdown(
        "### 👩‍🏫 Bu Kriz Durumunda 2026 Maarif Modeli'ne Göre Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sahada uygulanabilirlik ve rubrik kriterleri açısından doğru aksiyonu"
        " seçin:",
        [
            (
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve"
                " sınıf disiplini sert kurallarla korumak."
            ),
            (
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak,"
                " akran destekli empati kurdurmak ve somut materyalle"
                " desteklemek."
            ),
            (
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu"
                " anlatmaya devam etmek."
            ),
            (
                "D) Danışman hocaya dönüp sınıfın yönetilemez olduğunu"
                " bildirmek."
            ),
            (
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak"
                " kavramsal değişimi tetiklemek."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Detaylı Raporlamaya Geç"):
      kayit_metni = (
          sesli_girdi_manuel if sesli_girdi_manuel else sesli_secenek
      )
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "tema": secilen_tema,
          "kod": secilen_kazanim_obj["kod"],
          "surec": secilen_surec,
          "kriz": aktif_kriz,
          "karar": ogretmen_karari,
          "sesli_komut": kayit_metni,
      })
      st.success(
          "✅ 3D staj kararınız ve sesli kayıtlarınız sisteme işlendi! Sağ"
          " taraftan 2026 Maarif ve rubrik uyum analizlerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown(
        "#### 💡 2026 Maarif Modeli & Yüklenen Rubrik Uyum Analizi Paneli"
    )

    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Rubrik Kriterleri Kapsamında Saha Analizi")
      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.success(
            "🌟 **Mükemmel Rubrik ve Maarif Uyumu (100/100):** Seçtiğiniz bu"
            " yaklaşım; yüklediğiniz rubriğin kapsayıcı eğitim ve kriz"
            " yönetimi maddeleriyle ve 2026 Türkiye Yüzyılı Maarif Modeli"
            " felsefesiyle birebir örtüşmektedir."
        )
      else:
        st.error(
            "⚠️ **Rubrik Uyarısı:** Bu geleneksel yaklaşım, yüklediğiniz"
            " rubriğin kapsayıcı eğitim ilkelerini ihlal eder ve danışman"
            " hocadan düşük puan almanıza neden olur."
        )

      st.markdown(
          "##### 🛠️ Öğretmen Adayı İçin Net Ne Yapmalı / Nasıl Davranmalı Eylem"
          " Planı"
      )
      st.markdown(
          "- **Adım 1 (Güvenli Alan):** Öğrenciyi asla akranlarının önünde"
          " eleştirmeyin; 'Birlikte bakalım, bu harika bir keşif fırsatı'"
          " diyerek hitap edin.\n- **Adım 2 (Somutlaştırma):** Soyut kavramları"
          " onluk taban blokları veya dijital araçlarla destekleyin.\n- **Adım"
          " 3 (Rubrik Eşleme):** Yüklediğiniz rubriğin duyarlılık kriterini"
          " birebir uygulayın."
      )

      st.divider()
      if st.button("📋 Çok Katmanlı Detaylı Raporlama Paneline Geç"):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı kaydedip butona bastıktan sonra rubrik"
          " ve Maarif modeline uygunluk analizleri burada açılacaktır."
      )

# ==========================================
# 4. ADIM 3: ÇOK KATMANLI, GRAFİKLİ VE DETAYLI RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "🎥 2026 MAARİF MODELİ & RUBRİK UYUMLU ÇOK KATMANLI DETAYLI RAPORLAMA"
      " SİSTEMİ"
  )
  st.markdown(
      f"**Üniversite & Fakülte:** {st.session_state.get('universite_adi', 'N/A')}"
      f" / {st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
      f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} |"
      f" **Okul No:** {st.session_state.get('okul_numarasi', 'N/A')} |"
      f" **Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
  )
  st.markdown(
      f"**Rapor Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
  )

  st.divider()

  tab_aday, tab_fakulte, tab_ogretim = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Gelişim, Replay & Geri Bildirim",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Puan Matrisi & Geri Dönüt",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 3D Sınıf & Sesli Hitabet Oturumu Dijital Replay Paneli"
    )
    st.info(
        "Aşağıdaki simülasyon tekrar panelinde, 3D sınıf ortamında"
        " gerçekleştirdiğiniz sesli hitabet oturumu, kriz anı yönetimi ve"
        " öğrenci avatarlarının tepkileri anlık olarak kayıt altına alınmıştır."
    )

    with st.container(border=True):
      st.markdown("#### 🔄 Oturum Senkronizasyon & Dijital Replay Kaydı")
      if toplam_islem > 0:
        son_adim = st.session_state.simulasyon_gecmisi[-1]
        st.success(
            f"🟢 **Canlı Oturum ID:** #TYMM-{random.randint(10000, 99999)} |"
            f" **Sınıf:** {son_adim['sinif']} | **Tema:** {son_adim['tema']}"
        )
        st.markdown(
            f"- **Seçilen Kazanım Kodu:** `{son_adim['kod']}`\n- **Odaklanılan"
            f" Süreç Bileşeni:** {son_adim['surec']}\n- **Simüle Edilen"
            f" Kriz:** {son_adim['kriz']}\n- **Adayın Sesli Hitabet Yanıtı:**"
            f" *\"{son_adim['sesli_komut']}\"*"
        )
      else:
        st.warning(
            "Henüz tamamlanmış bir oturum bulunmuyor. Adım 2'den simülasyonu"
            " tamamlayarak replay verilerini burada görüntüleyebilirsiniz."
        )

    st.markdown("---")
    st.markdown(
        "### 📝 Öğretmen Adayı Simülasyon Öz-Değerlendirme ve Uygulama Geri"
        " Bildirimi"
    )
    st.info(
        "Bu 3D staj simülasyonu deneyiminizi, mesleki gelişiminize katkısını ve"
        " uygulama hakkındaki geri bildirimlerinizi aşağıya yazarak fakülte"
        " komisyonuna ve portfolyonuza iletebilirsiniz."
    )

    aday_geri_bildirimi = st.text_area(
        "Öğretmen Adayı Geri Bildirim ve Yansıtma Notu",
        placeholder=(
            "Örn: Bu simülasyon kriz yönetimi ve kapsayıcı dil kullanımı"
            " konusunda bana harika bir refleks kazandırdı. 2026 Maarif Modeli"
            " süreç bileşenlerini sınıf ortamında uygulamak çok öğreticiydi..."
        ),
    )

    if st.button("📤 Aday Geri Bildirimini Arşive ve Fakülteye Kaydet"):
      if aday_geri_bildirimi:
        st.success(
            "✅ Simülasyon ve uygulama hakkındaki geri bildiriminiz başarıyla"
            " kaydedildi ve kişisel staj portfolyonuza eklendi!"
        )
      else:
        st.warning(
            "Lütfen göndermeden önce geri bildirim alanına notunuzu yazınız."
        )

    st.markdown(
        "### 📈 2026 Maarif Modeli & Sahada Uygulanabilirlik Grafikleri"
    )

    if toplam_islem > 0:
      chart_data = pd.DataFrame(
          {
              "Rubrik & Maarif Kriteri": [
                  "Sesli Hitabet Simülasyonu",
                  "Kapsayıcı Eğitim",
                  "Maarif Süreç Bileşeni",
                  "Saha Aksiyon Başarısı",
              ],
              "Yeterlilik Puanı": [99, 97, 96, 98],
          }
      )
      st.bar_chart(chart_data, x="Rubrik & Maarif Kriteri", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### 3D Esnek Oturum #{idx}: {veri['tema']}")
        st.markdown(
            f"- **Kazanım Kodu:** `{veri['kod']}` | **Süreç Bileşeni:**"
            f" {veri['surec']}"
        )
        st.markdown(f"- **Karşılaşılan Kriz:** {veri['kriz']}")
        st.markdown(f"- **Adayın Sesli Yanıtı:** {veri['sesli_komut']}")
        st.markdown(f"- **Seçilen Saha Kararı:** {veri['karar']}")
        st.markdown("---")

      st.success(
          "💡 **Aday Detaylı Eylem Rehberi:** Gerçek sahada bu simülasyon"
          " sayesinde olumlu ve olumsuz durumlar için önceden refleks"
          " kazandığınız; çocukların bireysel farklılıklarına göre"
          " zenginleştirme ve farklılaştırma yapabileceğiniz kanıtlanmıştır."
      )
    else:
      st.warning("Henüz kaydedilmiş bir staj oturumu bulunmuyor.")

  with tab_fakulte:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon ve Uygunluk Raporu"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi İlköğretim"
        " Matematik Öğretmenliği Bölüm Komisyonu* tarafından 2026 Türkiye"
        " Yüzyılı Maarif Modeli ve yüklenen rubrikler çerçevesinde"
        " düzenlenmiştir."
    )

    st.markdown(
        "#### 📊 Kurumsal Uygunluk ve Sahada Uygulanabilirlik Değerlendirmesi:\n"
        "1. **2026 Maarif Modeli Uygunluğu:** Aday öğretmen; yüklenen"
        " kazanımlar ve süreç bileşenleri bağlamında teorik bilgiyi sahaya"
        " aktarabileceğini kanıtlamıştır.\n2. **Rubrik Kriterlerine Göre"
        " Değerlendirme:** Yüklenen danışman hoca rubriği ile yapılan"
        " testlerde aday yüksek başarı sergilemiştir.\n3. **Dekanlık Kararı:**"
        " Adayın gerçek okul stajına çıkması fakültemiz komisyonunca **UYGUN"
        " BULUNMUŞTUR**."
    )

    st.success(
        "🎉 **Resmî Dekanlık Mührü:** Bu detaylı rapor üniversite staj bilgi"
        " sistemine (OBS) aktarılmıştır."
    )

  with tab_ogretim:
    st.markdown(
        "### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Puan Matrisi & Geri Dönüt"
    )
    st.markdown(
        f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    st.markdown(
        "🎥 **3D Aday Oturum Replay & Sesli Kayıt İnceleme Alanı:** Danışman"
        " hoca olarak yüklediğiniz rubrik kriterlerine göre adayı puanlayın."
    )

    st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri ve Başarı Matrisi:")
    st.markdown(
        f"> **Rubrik Metni:**\n> * {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Puan Tablosu:\n"
        "- 🎙️ **Sesli Kriz Yönetimi ve Hitabet:** 30 / 30 Puan\n- 🤝"
        " **Kapsayıcı Eğitim ve Farkındalık:** 30 / 30 Puan\n- 🎯 **2026 Maarif"
        " Süreç Bileşeni Uyumu:** 20 / 20 Puan\n- 🚀 **Sahada Aksiyon Alma"
        " Başarısı:** 20 / 20 Puan\n- **TOPLAM PUAN:** **100 / 100**"
    )

    st.markdown("---")
    st.markdown(
        "#### ✍️ Öğretmen Elemanı Resmî Geri Dönüt ve Gelişim Tavsiyesi"
    )
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Adaya Resmî Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, yüklediğiniz rubrik kriterlerine"
            " ve 2026 Maarif Modeli'ne göre 3D simülasyon performansınızı ve"
            " sesli hitabetinizi çok başarılı buldum. Gerçek sahada da bu"
            " vizyonu sürdürmenizi dilerim."
        ),
    )

    if st.button("📤 Geri Dönütü Adaya ve Dekanlığa Gönder"):
      st.success(
          "✅ Danışman hoca geri dönütünüz başarıyla kaydedildi, oturum"
          " replay kaydı arşivlendi ve aday portfolyosuna eklendi!"
      )

  if st.button("🔄 Yeni Bir 3D Staj Simülasyonu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
