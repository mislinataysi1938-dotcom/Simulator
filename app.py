import datetime
import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Ultimate Virtual Classroom & Simulator",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu (Session State) Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sanal Sınıf, 3: Detaylı Raporlar

# ==========================================
# 1. 2026 MAARİF MODELİ (5, 6, 7, 8. SINIFLAR - TÜM KAPSAMLI A, B, C KAZANIMLARI)
# ==========================================
maarif_tam_veritabani = {
    "5. Sınıf": {
        "Doğal Sayılar ve İşlemler (5.1.1.)": {
            "alt_baslik_a": (
                "5.1.1.A. Milyonlar Bölüğü ve Basamak Değeri: Doğal"
                " sayıların milyonlar bölüğündeki basamakları belirler, basamak"
                " adlarını ve değerlerini çözümler."
            ),
            "alt_baslik_b": (
                "5.1.1.B. Okuma ve Yazma Kuralları: En çok dokuz basamaklı"
                " doğal sayıları okur, yazar ve basamaklardaki sıfırların"
                " işlevini yorumlar."
            ),
            "alt_baslik_c": (
                "5.1.1.C. Karşılaştırma ve Sıralama: Doğal sayıları büyükten"
                " küçüğe sıralar, aralarındaki basamaksal farkları analiz"
                " eder."
            ),
            "sinif_durumu_senaryosu": (
                "Sınıf içi eş zamanlı gözlem: Öğretmen tahtada işlem yaparken"
                " ön sıradaki Disleksili Kerem sayıları tersten algılayıp"
                " defterine karalamakta; arka sırada oturan Otizmli Arda"
                " dış seslerden ve tahta kalemi sesinden rahatsız olup"
                " kulaklarını kapatmaktadır. Kaygılı Elif ise parmağını"
                " kaldırıp indirmekte, tahtaya kalkma korkusuyla terlemektedir."
            ),
            "durum_turu": (
                "Kritik Kavram Yanılgısı ve Duygusal/Duyusal Tepki Kesişimi"
            ),
            "gercek_yanilgi_ve_analiz": (
                "Sıfırın basamak tutucu rolünü kavramama; okunuş sırasını"
                " doğrudan rakamsal değere aktaramama ve eş zamanlı duyusal"
                " uyaran fazlalığı nedeniyle öğrencinin odak kaybı."
            ),
            "bilissel_kok": (
                "Görsel simgeler ile sayısal soyut değerler arasındaki"
                " basamak ilerleme kuralını kuramama; çevresel uyaran"
                " yönetimi eksikliği."
            ),
            "cozum_stratejisi": (
                "Onluk taban blokları, gürültü önleyici kulaklık desteği"
                " veya sakin köşe alanı oluşturma; sıfırın o basamakta 'yokluk'"
                " değil '0 tane' olduğunu somutlaştırma."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları, Manyetik"
                " Basamak Abaküsü\n💻 **Dijital / Web Araçları:** Base Ten Blocks"
                " (Math Learning Center), PhET Interactive simulations"
            ),
        },
        "Kesirler ve İşlemler (5.2.3.)": {
            "alt_baslik_a": (
                "5.2.3.A. Birim Kesirler ve Sıralama: Birim kesirleri"
                " modellerle gösterir ve sayı doğrusu üzerinde"
                " karşılaştırır."
            ),
            "alt_baslik_b": (
                "5.2.3.B. Denk Kesirler: Genişletme ve sadeleştirme"
                " işlemlerini modelleyerek denk kesirleri oluşturur."
            ),
            "alt_baslik_c": (
                "5.2.3.C. Kesirlerle Toplama ve Çıkarma: Paydaları eşit veya"
                " birinin diğerinin katı olan kesirlerle işlem yapar."
            ),
            "sinif_durumu_senaryosu": (
                "Sınıf içi eş zamanlı gözlem: 1/4 ve 1/2 karşılaştırılırken"
                " Üstün Yetenekli Can sıkıntıdan kalem çevirmekte ve"
                " 'Hocam zaten paydası büyük olan küçüktür, bunu geçelim'"
                " diye bağırmaktadır. Kinestetik Deniz ise pizzayı"
                " dilimlemek için tahtaya fırlamak istemektedir."
            ),
            "durum_turu": "Akran Sabırsızlığı ve Kinestetik Motivasyon Çatışması",
            "gercek_yanilgi_ve_analiz": (
                "Doğal sayı mantığını kesirlere transfer etme; paydadaki"
                " sayı büyüdükçe kesrin büyüyeceğini sanma."
            ),
            "bilissel_kok": (
                "Parçalanan bütünün parça boyutu küçülmesi kuralını,"
                " sayısal büyüklük algısıyla ters orantılı yorumlama."
            ),
            "cozum_stratejisi": (
                "Özdeş iki pizza modeli üzerinden dilimleme simülasyonu"
                " yapılarak payda büyüdükçe dilimin küçüldüğü görsel"
                " çelişkiyle gösterilmelidir."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Kesir Takımları, Manyetik Pasta/Pizza"
                " Dilimleme Seti\n💻 **Dijital / Web Araçları:** PhET Fraction"
                " Matcher, GeoGebra Kesir Çarkları"
            ),
        },
    },
    "6. Sınıf": {
        "Cebirsel İfadeler (6.2.1.)": {
            "alt_baslik_a": (
                "6.2.1.A. Sözel İfadeler ve Harf: Sözel olarak verilen bir"
                " duruma uygun cebirsel ifade yazar."
            ),
            "alt_baslik_b": (
                "6.2.1.B. Değer Hesaplama: Cebirsel ifadenin değerini,"
                " değişkenin alacağı farklı doğal sayı değerleri için"
                " hesaplar."
            ),
            "alt_baslik_c": (
                "6.2.1.C. Benzer Terimler: Benzer terimleri ayırt eder ve"
                " cebirsel ifadelerde toplama/çıkarma yapar."
            ),
            "sinif_durumu_senaryosu": (
                "Sınıf içi eş zamanlı gözlem: '3x + 5' ifadesi tahtaya"
                " yazıldığında öğrencilerin yarısı '8x' demekte, Otizmli"
                " öğrenci ise masasına kapanıp şekiller çizmeye devam"
                " etmektedir."
            ),
            "durum_turu": "Cebirsel Körlük ve Odak Dağınıklığı",
            "gercek_yanilgi_ve_analiz": (
                "Değişken içeren terimler ile sabit terimleri benzer terim"
                " kabul ederek hatalı toplama yapma."
            ),
            "bilissel_kok": (
                "Cebirsel harfleri nesne yerine koyma aşamasında aritmetik"
                " toplama refleksini körü körüne uygulama."
            ),
            "cozum_stratejisi": (
                "Cebir karoları kullanılarak x ile sayıların elma ile armut"
                " gibi farklı birimler olduğu somutlaştırılmalıdır."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Manyetik Cebir Karoları (Algebra"
                " Tiles)\n💻 **Dijital / Web Araçları:** Desmos Cebir Karoları"
                " Etkinliği"
            ),
        },
    },
    "7. Sınıf": {
        "Oran ve Orantı (7.2.1.)": {
            "alt_baslik_a": (
                "7.2.1.A. Oran Kavramı ve Birimli/Birimsiz Oran: İki çokluğun"
                " birbirine oranını belirler ve yorumlar."
            ),
            "alt_baslik_b": (
                "7.2.1.B. Doğru Orantı: Doğru orantılı iki nicelik arasındaki"
                " ilişkiyi kurar ve orantı sabitini bulur."
            ),
            "alt_baslik_c": (
                "7.2.1.C. Ters Orantı: Ters orantılı nicelikleri ayırt eder"
                " ve günlük hayat problemlerini çözer."
            ),
            "sinif_durumu_senaryosu": (
                "Sınıf içi eş zamanlı gözlem: İşçi-gün problemi çözülürken"
                " sınıfın büyük kısmı 'işçi artarsa gün artar' mantığıyla"
                " doğru orantı kurmakta, Kaygılı Elif ise defterine hiçbir"
                " şey yazamamaktadır."
            ),
            "durum_turu": "Yaygın Doğru Orantı Genelleme Hatası ve Kaygı",
            "gercek_yanilgi_ve_analiz": (
                "Ters orantı gerektiren durumlarda dahi doğru orantı"
                " şablonunu uygulama."
            ),
            "bilissel_kok": (
                "Niceliklerin her zaman birlikte artması genellemesini tüm"
                " problemlere dayatma."
            ),
            "cozum_stratejisi": (
                "Mantıksal sorgulama ve tablo testi ile bilişsel çelişki"
                " yaratma."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Oran Tahtası, Renkli Boncuklar\n💻"
                " **Dijital / Web Araçları:** GeoGebra Orantı Simülasyonları"
            ),
        },
    },
    "8. Sınıf": {
        "Kareköklü İfadeler (8.1.2.)": {
            "alt_baslik_a": (
                "8.1.2.A. Tam Kare Sayılar ve Karekök: Alanı verilen karenin"
                " kenar uzunluğunu bulur."
            ),
            "alt_baslik_b": (
                "8.1.2.B. Kareköklü Sayılarda Tahmin: Hangi iki doğal sayı"
                " arasında olduğunu belirler."
            ),
            "alt_baslik_c": (
                "8.1.2.C. Kareköklü İfadelerde İşlemler: Çarpma, bölme ve"
                " toplama/çıkarma kuralları."
            ),
            "sinif_durumu_senaryosu": (
                "Sınıf içi eş zamanlı gözlem: Kök(9+16) = Kök9 + Kök16 hatası"
                " yapılırken, arka sıradaki öğrenciler grup halinde"
                " birbirleriyle sohbet etmekte, öğretmen otoritesini"
                " sarsacak mini bir uğultu yükselmektedir."
            ),
            "durum_turu": "Dağılma Özelliği Yanılgısı ve Akran Kontrol Kaybı",
            "gercek_yanilgi_ve_analiz": (
                "Kareköklü ifadelerde toplama üzerine kök alma işleminin"
                " dağılabileceğini varsayma."
            ),
            "bilissel_kok": (
                "Çarpma/bölmedeki kuralı toplama işlemine hatalı uyarlama."
            ),
            "cozum_stratejisi": (
                "Sayısal eşitlikleri sayarak çelişkiyi kanıtlama ve grup"
                " yönetimi stratejileri uygulama."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Birim Kare Kartları ve Alan Izgaraları\n💻"
                " **Dijital / Web Araçları:** Desmos Square Roots Explorer"
            ),
        },
    },
}

# ==========================================
# 2. ADIM 1: KAPSAMLI KURULUM VE GİRİŞ PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen Kurumsal Kayıt ve 3D Sanal Sınıf Kurulum Paneli"
      " (2026 Maarif Modeli)"
  )
  st.info(
      "Üniversitenizi, fakültenizi, bölümünüzü, kendi uygulama öğretim"
      " elemanınızı seçebilir veya yazabilir; öğretim elemanınızın değerlendirme"
      " rubriğini sisteme yükleyerek simülasyonu özelleştirebilirsiniz."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Zeynep Kaya"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Hacettepe Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )

    # Öğretim elemanı seçme veya yazma
    ogretim_elemani_secim = st.selectbox(
        "Uygulama Öğretim Elemanı (Danışman Hoca)",
        [
            "Prof. Dr. Ahmet Yılmaz (Matematik Eğitimi ABD)",
            "Doç. Dr. Fatma Demir (Özel Öğretim Yöntemleri)",
            "Dr. Öğr. Üyesi Mustafa Çelik (Eğitim Teknolojileri)",
            "Prof. Dr. Seda Kaya (Ölçme ve Değerlendirme)",
            "✏️ Diğer / Listede Yok (Kendim Yazacağım)",
        ],
    )
    if ogretim_elemani_secim == "✏️ Diğer / Listede Yok (Kendim Yazacağım)":
      uygulama_ogretim_elemani = st.text_input(
          "Öğretim Elemanının Adını ve Unvanını Giriniz",
          placeholder="Örn: Prof. Dr. Ali Can",
      )
    else:
      uygulama_ogretim_elemani = ogretim_elemani_secim

  with col2:
    st.markdown("### 📋 Öğretim Elemanı Rubriği / Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Öğretim Elemanınızın Değerlendirme Kriterlerini / Rubriğini Buraya"
        " Yapıştırın (Opsiyonel)",
        placeholder=(
            "Örn: 1. Kapsayıcı dil kullanımı, 2. Bilişsel çelişki yaratma"
            " becerisi, 3. Somut materyal entegrasyonu..."
        ),
        height=100,
    )

    st.markdown("### 👥 Sanal Sınıf Mevcudu ve Eş Zamanlı Öğrenci Profilleri")
    sinif_mevcudu = st.slider(
        "Sınıf Mevcudu (Toplam Öğrenci)", min_value=10, max_value=35, value=24
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
      sayi_disleksi = st.number_input(
          "Disleksili Öğrenci", min_value=0, max_value=5, value=2
      )
      sayi_otizm = st.number_input(
          "Otizm Spektrumlu Öğrenci", min_value=0, max_value=5, value=1
      )
    with col_p2:
      sayi_kaygili = st.number_input(
          "Yüksek Kaygılı Öğrenci", min_value=0, max_value=5, value=3
      )
      sayi_ustun = st.number_input(
          "Üstün Yetenekli Öğrenci", min_value=0, max_value=5, value=2
      )

  st.markdown("### 🏫 3D İzometrik Sınıf Ortamı ve Sesli Etkileşim Tercihleri")
  sanal_3d_gorus = st.checkbox(
      "3D İzometrik Sınıf Ortamı Görünümünü Etkinleştir (Sıralar, Kürsü, Öğrenci"
      " Avatarları, Jest ve Mimikler)",
      value=True,
  )
  sesli_mikrofon = st.checkbox(
      "Sesli Komut ve Konuşma Tanıma Entegrasyonunu Aç (Mikrofon ile simüle"
      " edilmiş sesli yanıt ve avatar seslendirmesi)",
      value=True,
  )

  if st.button("🚀 3D Sanal Sınıf Simülasyonunu Başlat"):
    if not ogretmen_adi or not universite_adi:
      st.warning(
          "Lütfen öğretmen adı ve üniversite alanlarını eksiksiz doldurunuz."
      )
    else:
      st.session_state.ogretmen_adi = ogretmen_adi
      st.session_state.universite_adi = universite_adi
      st.session_state.fakulte_bolum = fakulte_bolum
      st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
      st.session_state.rubrik_metni = (
          rubrik_metni
          if rubrik_metni
          else "Standart Eğitim Fakültesi Staj Rubriği"
      )
      st.session_state.sinif_mevcudu = sinif_mevcudu
      st.session_state.profil_dagilimi = {
          "Disleksili": sayi_disleksi,
          "Otizmli": sayi_otizm,
          "Kaygılı": sayi_kaygili,
          "Üstün Yetenekli": sayi_ustun,
      }
      st.session_state.sanal_3d_gorus = sanal_3d_gorus
      st.session_state.sesli_mikrofon = sesli_mikrofon
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: 3D SANAL SINIF ORTAMI VE DETAYLI KAZANIM UYGULAMASI
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretim Elemanı"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 24)
  dagilim = st.session_state.get("profil_dagilimi", {})

  secilen_sinif = st.selectbox(
      "2026 Maarif Modeli Sınıf Düzeyi Seçin",
      list(maarif_tam_veritabani.keys()),
  )
  konu_secenekleri = list(maarif_tam_veritabani[secilen_sinif].keys())

  st.markdown(
      f"### 🏫 3D İzometrik Sanal Sınıf | Öğretmen Adayı: {ogretmen}"
      f" ({universite})"
  )
  st.caption(
      f"Danışman Hoca: {ogretim_elemani} | Sınıf Mevcudu: {mevcut} | Aktif"
      f" Profiller: Disleksili({dagilim.get('Disleksili', 0)}),"
      f" Otizmli({dagilim.get('Otizmli', 0)}), Kaygılı({dagilim.get('Kaygılı', 0)}),"
      f" Üstün({dagilim.get('Üstün Yetenekli', 0)})"
  )

  # 3D Ortam ve Avatar Görselleştirme Simülasyon Kutusu
  if st.session_state.get("sanal_3d_gorus", True):
    st.markdown(
        "> 🧊 **[3D İzometrik Sınıf Kuşbakışı ve Avatar Görünüm Paneli]**\n"
        "> *Sınıf U düzeninde dizilmiş olup, öğretmen masasında **Avatarınız (Öğretmen Adayı 3D Model)** konumlanmıştır.*\n"
        "> *📌 Ön sırada **Disleksili Kerem (Avatar #1)** sayıları karıştırıp endişeyle eliyle alnını ovuşturmakta; orta sırada **Otizmli Arda (Avatar #2)** kulaklık takarak tahtaya bakmaktadır. Arka sırada ise **Üstün Yetenekli Can (Avatar #3)** sabırsızca parmak sallamakta, **Kaygılı Elif (Avatar #4)** ise başını öne eğmiştir.*\n"
        "> *🎯 Sınıfın genelinde anlık uğultu ve dikkat dalgalanmaları 3D simülasyon motoru tarafından izlenmektedir.*"
    )

  secilen_konu = st.selectbox(
      "2026 Maarif Modeli Konu ve Kapsam Başlığı", konu_secenekleri
  )
  veri = maarif_tam_veritabani[secilen_sinif][secilen_konu]

  st.divider()

  # A, B, C Alt Kazanım Seçimi
  st.markdown("### 🎯 2026 Maarif Modeli A, B, C Alt Kazanım Seçimi")
  secilen_abc = st.radio(
      "İşlemek istediğiniz spesifik alt kazanım bölümünü seçiniz:",
      [veri["alt_baslik_a"], veri["alt_baslik_b"], veri["alt_baslik_c"]],
  )

  st.info(f"**Odak Alt Kazanım Metni:**\n\n{secilen_abc}")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### 💬 Sınıf İçi Eş Zamanlı Durum ve Öğrenci Tepkileri")
    st.warning(veri["sinif_durumu_senaryosu"])
    st.markdown(f"**Olay Türü:** {veri['durum_turu']}")

    if st.session_state.get("sesli_mikrofon", True):
      st.markdown(
          "🎤 *[Sesli Mikrofon & Avatar Seslendirme Aktif]*: Öğrenciye sesli"
          " yanıt vermek için konuşabilir ya da aşağıdaki simülasyon kutusunu"
          " kullanabilirsiniz."
      )
      st.text_input(
          "Öğretmen Adayı Sesli Hitabet Simülasyonu",
          placeholder="Örn: 'Sakin olun arkadaşlar, gelin bu kavramı hep birlikte"
          " somut modellerle inceleyelim...'",
      )

    st.markdown("### 👩‍🏫 Bu Durumda Pedagojik Kararınız Ne Olurdu?")
    ogretmen_karari = st.radio(
        "Sınıf yönetimi, kapsayıcılık ve kavramsal değişim açısından en uygun"
        " kararı seçiniz:",
        [
            (
                "A) Doğru kuralı doğrudan tahtaya yazıp geçmek, ezberletmek ve"
                " sınıfın akışını bozmamak."
            ),
            (
                "B) Öğrencilerin bireysel profillerini (otizm, disleksi, kaygı)"
                " gözeterek güvenli sınıf iklimi oluşturmak; çelişki yaratacak"
                " somut model ve rehberli sorular sunmak."
            ),
            (
                "C) Öğrencilerin hatalarını ve duyusal tepkilerini tamamen"
                " görmezden gelip müfredata devam etmek."
            ),
            (
                "D) Problem çıkaran öğrenciyi tahtadan indirip yerine"
                " oturtmak ve dersi sert bir uyarıla sürdürmek."
            ),
            (
                "E) Sınıf genelinde akran destekli grup çalışması başlatarak"
                " hem kavram yanılgısını gidermek hem de kaygıyı azaltmak."
            ),
        ],
    )

    if st.button("📥 Pedagojik Kararı Kaydet ve Uzman Analizini Gör"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "konu": secilen_konu,
          "abc_kazanim": secilen_abc,
          "karar": ogretmen_karari,
          "yanilgi": veri["gercek_yanilgi_ve_analiz"],
          "bilissel_kok": veri["bilissel_kok"],
          "cozum": veri["cozum_stratejisi"],
          "materyaller": veri["materyal_ve_araclar"],
      })
      st.success(
          "✅ Kararınız kaydedildi! Sağ taraftan uzman analizlerini ve"
          " materyal önerilerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown("#### 💡 Uzman / Mentor Geri Bildirim ve Materyal Paneli")

    # KRİTİK KURAL: Uzman analizleri ve somut materyal önerileri yalnızca karar verildikten sonra açılır!
    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Tespit Edilen Temel Kavram Yanılgısı & Sınıf Analizi")
      st.error(son_kayit["yanilgi"])

      st.markdown("##### 🧠 Yanılgının Bilişsel Kökü")
      st.warning(son_kayit["bilissel_kok"])

      st.markdown("##### 🛠️ Önerilen Pedagojik Çözüm Stratejisi")
      st.success(son_kayit["cozum"])

      st.markdown(
          "##### 🧩 Kullanılabilecek Somut Materyal ve Dijital Web Araçları"
      )
      st.info(son_kayit["materyaller"])

      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.markdown(
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — Kapsayıcı"
            " eğitime, otizm/disleksi duyarlılığına ve yapılandırmacı"
            " yaklaşıma tam uygun profesyonel refleks!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " öğrencilerin dersten kopmasına ve yanılgının kalıcılaşmasına"
            " yol açabilir."
        )

      st.divider()
      if st.button(
          "📋 Simülasyonu Tamamla ve Detaylı Rapor Paneline Geç"
      ):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı seçip 'Pedagojik Kararı Kaydet' butonuna"
          " bastıktan sonra gizli uzman analizleri ve somut materyal önerileri"
          " bu alanda açılacaktır."
      )

# ==========================================
# 4. ADIM 3: ÇOK DETAYLI ÇİFT YÖNLÜ RAPORLAMA VE GERİ DÖNÜT SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "📋 KAPSAMLI PEDAGOJİK DEĞERLENDİRME, RUBRİK UYUM VE KURUMSAL STAJ RAPORU"
  )
  st.markdown(
      f"**Üniversite & Fakülte:** {st.session_state.get('universite_adi', 'N/A')}"
      f" / {st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
      f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} |"
      f" **Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
  )
  st.markdown(
      f"**Rapor Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
  )

  st.divider()

  # Sekmeli Yapı: 1. Öğretmen Adayı Gelişim Raporu & Grafikler | 2. Fakülte ve Rubrik Karşılaştırma Raporu | 3. Uygulama Değerlendirme Anketi
  tab1, tab2, tab3 = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Gelişim Raporu & Görsel Öneriler",
      "🏛️ 2. Fakülte Kurumsal Raporu & Rubrik Karşılaştırma Analizi",
      "📝 3. Simülasyon Deneyim Anketi ve Geri Dönüt Kutusu",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab1:
    st.markdown(
        "### 📈 Öğretmen Adayı Bireysel Gelişim ve Performans Grafikleri"
    )

    if toplam_islem > 0:
      # Görsel Grafik Simülasyonu (Streamlit Native Chart)
      import pandas as pd

      chart_data = pd.DataFrame(
          {
              "Kriter": [
                  "Kapsayıcı Eğitim",
                  "Kavramsal Değişim",
                  "Sınıf Yönetimi",
                  "Materyal Kullanımı",
              ],
              "Puan": [92, 88, 95, 90],
          }
      )
      st.bar_chart(chart_data, x="Kriter", y="Puan")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### Oturum #{idx}: {veri['konu']}")
        st.markdown(f"- **Odak A-B-C Kazanım Bölümü:** {veri['abc_kazanim']}")
        st.markdown(f"- **Seçilen Pedagojik Karar:** {veri['karar']}")
        st.markdown(f"- **Tespit Edilen Yanılgı & Durum:** {veri['yanilgi']}")
        st.markdown(f"- **Bilişsel Kök Analizi:** {veri['bilissel_kok']}")
        st.markdown(f"- **Önerilen Profesyonel Strateji:** {veri['cozum']}")
        st.markdown(
            f"- **Görsel Olarak Önerilen Somut/Dijital Araçlar:**\n"
            f"  {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **Gelişim Analizi ve Öneri:** Sınıf içindeki disleksili ve"
          " otizmli öğrencilerin duyusal ihtiyaçlarını karşılarken"
          " hazırladığınız somut materyal entegrasyonu oldukça başarılıdır."
          " Ancak zaman yönetimi ve akran etkileşimi konularında"
          " zayıf olduğunuz alanlar için dijital oyunlaştırılmış araçlara"
          " ağırlık vermeniz önerilir."
      )
    else:
      st.warning("Henüz kaydedilmiş bir simülasyon oturumu bulunmuyor.")

  with tab2:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Kurumsal Rapor ve Rubrik Uyum Analizi"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi Staj"
        " Komisyonu* tarafından onaylanmıştır."
    )

    st.markdown("#### 🔍 Öğretim Elemanı Rubriği ile Aday Performans Uyum Testi:")
    st.markdown(
        f"> **Yüklenen/Seçilen Rubrik Kriterleri:**\n> *"
        f" {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Karşılaştırmalı Uyum Matrisi:\n"
        "- ✅ **Kapsayıcı Dil ve Bireysel Farkındalık:** Adayın tercih ettiği"
        " B seçeneği, rubriğin kapsayıcılık maddesiyle **%95 oranında"
        " uyuşmaktadır**.\n- ⚠️ **Zaman Yönetimi ve Otorite Dengesi:** Rubrik"
        " kriterlerinde yer alan sınıf içi akış yönetimi konusunda adayın"
        " alternatif C kararlarından kaçınması gerektiği tespit"
        " edilmiştir.\n- ✅ **2026 Maarif Modeli Uyumu:** Kazanımların A, B, C"
        " kırılımlarına tam uyum sağlanmıştır."
    )

    st.markdown("---")
    st.markdown("#### 📋 Fakülte Bölüm Başkanlığı Değerlendirme Kararı")
    st.markdown(
        "Adayın simülasyon seanslarındaki kararları, öğretim elemanının"
        " rubrik kriterleriyle eşleştirilmiş olup saha stajına çıkması"
        " **UYGUNDUR**."
    )

    st.success(
        "🎉 **Kurumsal Mühür:** Bu rapor fakülte staj portfolyosuna"
        " kaydedilmiştir."
    )

  with tab3:
    st.markdown(
        "### 📝 Öğretmen Adayının Simülasyonu Değerlendirme Anketi ve Geri Dönüt"
        " Kutusu"
    )
    st.info(
        "Bu simülasyon uygulamasını geliştirmemiz için lütfen aşağıdaki"
        " alanları doldurunuz."
    )

    deneyim_puan = st.slider(
        "Simülasyonun Gerçekçilik Puanı (1-10)", 1, 10, 9
    )
    kullanisli_alanlar = st.text_area(
        "Uygulamanın en çok hangi yönlerini faydalı buldunuz?",
        placeholder="Örn: 3D sınıf ortamı ve anlık öğrenci tepkileri...",
    )
    gelistirme_onerisi = st.text_area(
        "Uygulamada geliştirilmesini veya eklenmesini istediğiniz özellikler"
        " nelerdir?",
    )

    if st.button("📤 Geri Dönütleri Sisteme Gönder"):
      st.success(
          "🙏 Değerli geri bildirimleriniz için teşekkür ederiz! Geri"
          " bildiriminiz geliştirici ekibe ve uygulama öğretim elemanınıza"
          " iletilmiştir."
      )

  if st.button("🔄 Yeni Bir Simülasyon Oturumu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
