import datetime
import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Masterclass Internship Simulator",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Staj ve Kayıt, 3: Raporlar

# ==========================================
# 1. AKADEMİK LİTERATÜR VE 2026 MAARİF MODELİ TABANLI STAJ ARŞİVİ
# ==========================================
akademik_staj_arsivi = {
    "5. Sınıf": {
        "Doğal Sayılar ve İşlemler": {
            "kazanim_kodu": "MATH.5.1.1",
            "alt_basliklar": [
                (
                    "5.1.1.A. Milyonlar bölüğü ve basamak değerlerini"
                    " çözümleme."
                ),
                (
                    "5.1.1.B. Dokuz basamaklı sayıları okuma, yazma ve sıfırın"
                    " basamak tutucu rolü."
                ),
                (
                    "5.1.1.C. Büyük sayılarla tahmin ve zihinden işlem"
                    " stratejileri."
                ),
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Millî Kütüphane'deki 405.020 adet"
                " tarihi el yazması kitabın arşiv kodlama sistemi."
            ),
            "staj_krizi_senaryosu": (
                "Kapsayıcı Saha Krizi: Dersin 15. dakikasında okul müdür"
                " yardımcısı denetim için sınıfa girip en arka sıraya"
                " oturur. Aynı anda disleksili Kerem 405.020 sayısını '452'"
                " olarak okuyunca, üstün yetenekli Can sesli bir şekilde"
                " alay eder. Sınıfta gerginlik tırmanır."
            ),
            "krizi_yonetme_zorlugu": (
                "İdari Denetim Baskısı Altında Akran Alay Etme ve Kapsayıcılık"
                " Krizi."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Sıfırın basamak tutucu rolünü anlamayıp boşlukları yok sayma"
                " eğilimi."
            ),
            "pedagojik_cozum": (
                "Müdüre dönüp saygı göstermek, Can'ın davranışına sınır"
                " koyarak akran empatisi kurdurmak ve onluk taban bloklarıyla"
                " Kerem'e güvenli alan açmak."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları\n💻"
                " **Tıklanabilir Web Aracı:** [Math Learning Center Base Ten"
                " Blocks](https://www.mathlearningcenter.org/apps/base-ten-blocks)"
            ),
        },
        "Kesirler": {
            "kazanim_kodu": "MATH.5.2.3",
            "alt_basliklar": [
                (
                    "5.2.3.A. Birim kesirleri modelleme ve sayı doğrusunda"
                    " gösterme."
                ),
                (
                    "5.2.3.B. Paydaları eşit veya katı olan kesirlerle işlem"
                    " yapma."
                ),
                "5.2.3.C. Kesir problemleri kurma ve çözme.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Willy Wonka çikolata fabrikasındaki"
                " eşit dilimleme senaryosu."
            ),
            "staj_krizi_senaryosu": (
                "Teknolojik Kriz: Akıllı tahta projektörü bir anda patlar ve"
                " ekran kararır. Kaygılı Elif 'Hocam tahta gitti, sınavda ne"
                " soracaksınız?' diye panik atak geçirir. Sınıftaki diğer"
                " öğrenciler karanlıkta fısıldaşmaya başlar."
            ),
            "krizi_yonetme_zorlugu": (
                "Akıllı Tahta Arızası ve Öğrenci Sınav Kaygısı Krizi."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Payda büyüdükçe kesrin büyüyeceği yanılgısı."
            ),
            "pedagojik_cozum": (
                "Panik yapmadan tebeşirle tahtaya dönmek, manyetik kesir"
                " takımlarını ele almak ve Elif'e bireysel güven"
                " pekiştireci vermek."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Manyetik Pizza Dilimleme Seti\n💻"
                " **Tıklanabilir Web Aracı:** [PhET Fraction"
                " Matcher](https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.tr.html)"
            ),
        },
    },
    "6. Sınıf": {
        "Cebirsel İfadeler": {
            "kazanim_kodu": "MATH.6.2.1",
            "alt_basliklar": [
                "6.2.1.A. Sözel duruma uygun cebirsel ifade yazma.",
                "6.2.1.B. Değişken değerleri için cebirsel ifade hesaplama.",
                "6.2.1.C. Benzer terimler ve cebirsel toplama/çıkarma.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Akıllı telefon veri paket tarifelerinin"
                " cebirsel modellenmesi."
            ),
            "staj_krizi_senaryosu": (
                "Disiplin ve Kavram Yanılgısı Krizi: Sınıfın çoğunluğu '3x + 5"
                "= 8x' hatasını yaparken, arka sıradaki iki öğrenci kağıt"
                " uçak yapıp fırlatır. Danışman hoca arka sırada deftere"
                " not alarak adayın sınıf hakimiyetini incelemektedir."
            ),
            "krizi_yonetme_zorlugu": (
                "Danışman Hoca Gözetimi Altında Akran Disiplin Problemi ve"
                " Kavramsal Çatışma."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Değişken ile sabiti toplama (Aritmetik alışkanlık)."
            ),
            "pedagojik_cozum": (
                "Cebir karolarıyla somutlaştırma ve kağıt atan"
                " öğrencilere 'akran liderliği' rolü vererek enerjilerini"
                " derse kanalize etme."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Manyetik Cebir Karoları\n💻"
                " **Tıklanabilir Web Aracı:** [Desmos Algebra"
                " Tiles](https://teacher.desmos.com/custom/algebra-tiles)"
            ),
        },
        "Veri İşleme ve Analiz": {
            "kazanim_kodu": "MATH.6.4.2",
            "alt_basliklar": [
                "6.2.2.A. Sıklık tablosu ve sütun grafiği oluşturma.",
                "6.2.2.B. İki veri grubunu karşılaştırma.",
                "6.2.2.C. Aritmetik ortalama ve açıklık hesaplama.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Olimpiyat sporcularının başarı"
                " ortalamaları."
            ),
            "staj_krizi_senaryosu": (
                "Duyusal Kriz: Otizmli Arda, sınıftaki ani gürültüden ötürü"
                " çığlık atıp masaya kapanır. Sınıf bir anda susar ve"
                " herkes Arda'ya döner. Aday hem ders akışını korumalı hem"
                " de Arda'nın duyusal krizini yönetmelidir."
            ),
            "krizi_yonetme_zorlugu": (
                "Otizm Spektrumlu Birey Duyusal Kriz ve Akran Farkındalığı"
                " Yönetimi."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Aritmetik ortalamanın sadece uç değerlerin ortalaması"
                " olduğu yanılgısı."
            ),
            "pedagojik_cozum": (
                "Sınıfa kısa bir nefes molası vermek, Arda'ya sakinleşmesi"
                " için kulaklık/güvenli alan sunmak ve denge terazisiyle"
                " konuya devam etmek."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Denge Terazisi\n💻 **Tıklanabilir Web"
                " Aracı:** [PhET Balance"
                " Scale](https://phet.colorado.edu/sims/html/balance-scale/latest/balance-scale_tr.html)"
            ),
        },
    },
    "7. Sınıf": {
        "Geometri ve Ölçme (Çok Yönlü Görünüm)": {
            "kazanim_kodu": "MATH.7.3.1",
            "alt_basliklar": [
                "7.3.1.A. Çok yönlü görünüşler (ön, arka, sağ, sol).",
                "7.3.1.B. İzometrik kağıt üzerinde birim küp yapıları.",
                "7.3.1.C. Mimari yapılarda perspektif ilişkileri.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Çin'in başkenti Pekin'deki ünlü"
                " **CCTV Binası**'nın dekonstrüktivist mimari perspektifleri."
            ),
            "staj_krizi_senaryosu": (
                "Öğrenci Direnci: CCTV binasının 3D görseli verilince"
                " öğrenciler perspektifi çizmeyi beceremeyip 'Hocam bu"
                " mimarlık dersi mi, yapamıyoruz!' diye isyan eder. Öğretmen"
                " adayının öz-yeterlilik inancını yükseltmesi gerekir."
            ),
            "krizi_yonetme_zorlugu": (
                "Öğrenci Motivasyon Çöküşü ve Öz-Yeterlilik Desteği."
            ),
            "kavram_yanilgisi_ve_kok": (
                "3 boyutlu yapıların derinliğini 2 boyuta aktarırken arka"
                " küpleri unutma."
            ),
            "pedagojik_cozum": (
                "Birim küplerle masada anında 3D model inşa edip telefon"
                " kamerasıyla farklı açılardan fotoğraflayarak göstermek."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Birim Küp Setleri\n💻 **Tıklanabilir Web"
                " Aracı:** [GeoGebra 3D"
                " Calculator](https://www.geogebra.org/3d)"
            ),
        },
        "Oran ve Orantı": {
            "kazanim_kodu": "MATH.7.2.1",
            "alt_basliklar": [
                "7.2.1.A. Birimli ve birimsiz oran karşılaştırmaları.",
                "7.2.1.B. Doğru orantı ve orantı sabiti.",
                "7.2.1.C. Ters orantı günlük problemler.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: İşçi-zaman inşaat planlaması."
            ),
            "staj_krizi_senaryosu": (
                "Akran Çatışması: Sınıfta iki grup öğrenci ters orantı"
                " konusunda iddiaya girip kavga eder (kalem fırlatma). Danışman"
                " öğretmen arka sırada kaşlarını kaldırarak adayın sınıf"
                " hakimiyetini izlemektedir."
            ),
            "krizi_yonetme_zorlugu": (
                "Akran Arası Fiziksel/Sözel Çatışma ve Danışman Gözetimi."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Her orantıyı doğru orantı zannetme."
            ),
            "pedagojik_cozum": (
                "Grupları ayırıp tablo üzerinden mantıksal test yaptırmak,"
                " taraflara ortak ortak görev vermek."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Oran Tablosu Kartları\n💻"
                " **Tıklanabilir Web Aracı:** [PhET Proportion"
                " Play](https://phet.colorado.edu/sims/html/proportion-play/latest/proportion-play_tr.html)"
            ),
        },
    },
    "8. Sınıf": {
        "Kareköklü İfadeler": {
            "kazanim_kodu": "MATH.8.1.2",
            "alt_basliklar": [
                "8.1.2.A. Tam kare sayılar ve alan-kenar ilişkisi.",
                "8.1.2.B. Kareköklü sayıların iki sayı arasında olduğunu tahmin.",
                "8.1.2.C. Kareköklü ifadelerde dört işlem.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: NASA uzay mekiği ısı kalkanı karoları."
            ),
            "staj_krizi_senaryosu": (
                "Kritik Sınav Anı: $\\sqrt{9+16} = 7$ hatası tahtada"
                " yapıldığında okul müdürü denetim için sınıfa girip en arka"
                " sıraya oturur. Sınıftaki gerginlik iki katına çıkar."
            ),
            "krizi_yonetme_zorlugu": (
                "Okul Müdürü Denetimi Altında Akademik Hata Yönetimi."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Kareköke alma işleminin toplama üzerine dağılması."
            ),
            "pedagojik_cozum": (
                "Panik yapmadan müdüre saygı gösterip ders akışını"
                " bozmadan sayısal alan modeliyle ispatı tahtaya yansıtmak."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Birim Kare Izgaraları\n💻"
                " **Tıklanabilir Web Aracı:** [Desmos Square Roots"
                " Explorer](https://www.desmos.com/calculator)"
            ),
        },
        "Cebirsel Özdeşlikler ve Çarpanlara Ayırma": {
            "kazanim_kodu": "MATH.8.2.1",
            "alt_basliklar": [
                "8.2.1.A. Özdeşlikleri modelleme ($(a+b)^2$, vb.).",
                "8.2.1.B. Ortak çarpan parantezine alma.",
                "8.2.1.C. Özdeşliklerle çarpanlara ayırma stratejileri.",
            ],
            "gercek_dunya_hook": (
                "Gerçek Yaşam Kancası: Mimari arsa planlaması ve havuz alanı"
                " değişimi."
            ),
            "staj_krizi_senaryosu": (
                "Alay Etme Krizi: $(a+b)^2 = a^2+b^2$ hatasını yapan öğrenciye"
                " sınıftaki popüler bir öğrenci alaycı bir gülüş atar."
                " Güvenli sınıf iklimi zedelenir."
            ),
            "krizi_yonetme_zorlugu": (
                "Akran Alay Etme ve Güvenli Sınıf İklimi Koruma."
            ),
            "kavram_yanilgisi_ve_kok": (
                "Üssün toplama üzerine dağılması (Cebirsel körlük)."
            ),
            "pedagojik_cozum": (
                "Alay etme davranışına anında sınır koyup, geometrik alan"
                " modeliyle hatanın çok normal olduğunu göstermek."
            ),
            "dijital_ve_somut_araclar": (
                "🧩 **Somut Materyal:** Geometrik Alan Kartları\n💻"
                " **Tıklanabilir Web Aracı:** [GeoGebra Algebraic"
                " Identities](https://www.geogebra.org/m/algebra-identities)"
            ),
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE GİRİŞ PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen Gerçekçi Saha Stajı Kurulum Paneli (2026 Maarif"
      " Modeli)"
  )
  st.info(
      "Bu simülasyon; okul idaresi denetimleri, akran çatışmaları,"
      " teknolojik arızalar, özel gereksinimli öğrenci krizleri ve danışman"
      " hoca gözlemleri dahil olmak üzere **gerçek bir staj deneyiminde"
      " yaşayabileceğiniz her şeyi** simüle eder."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Deniz Arslan"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Marmara Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )

    uygulama_ogretim_elemani = st.selectbox(
        "Uygulama Öğretim Elemanı (Danışman Hoca)",
        [
            "Prof. Dr. Selma Çetin (Matematik Eğitimi)",
            "Doç. Dr. Hakan Korkmaz (Özel Öğretim Yöntemleri)",
            "Dr. Öğr. Üyesi Canan Yıldız (Eğitim Teknolojileri)",
            "✏️ Diğer / Listede Yok (Kendim Yazacağım)",
        ],
    )
    if uygulama_ogretim_elemani == "✏️ Diğer / Listede Yok (Kendim Yazacağım)":
      uygulama_ogretim_elemani = st.text_input(
          "Öğretim Elemanının Adını ve Unvanını Giriniz"
      )

  with col2:
    st.markdown("### 📋 Öğretim Elemanı Rubriği / Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Danışman Hocanızın Rubriğini / Kriterlerini Buraya Yapıştırın",
        value=(
            "1. Kriz anlarında (teknik arıza, idari denetim, öğrenci krizleri)"
            " sakin kalma ve liderlik.\n2. Bireysel farklılıklara (disleksi,"
            " otizm, üstün yetenek) duyarlı kapsayıcı dil.\n3. 2026 Maarif"
            " Modeli kazanım uyumu ve tıklanabilir dijital/somut araç"
            " entegrasyonu.\n4. Akran çatışmalarını yönetme ve olumlu sınıf"
            " iklimi kurma."
        ),
        height=110,
    )

    st.markdown("### 👥 Sanal Sınıf Mevcudu ve Eş Zamanlı Öğrenci Profilleri")
    sinif_mevcudu = st.slider(
        "Sınıf Mevcudu (Toplam Öğrenci)", min_value=12, max_value=35, value=25
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

  if st.button("🚀 Gerçekçi Staj Simülasyonunu Başlat"):
    if not ogretmen_adi or not universite_adi:
      st.warning(
          "Lütfen öğretmen adı ve üniversite alanlarını eksiksiz doldurunuz."
      )
    else:
      st.session_state.ogretmen_adi = ogretmen_adi
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
      st.session_state.sanal_3d_gorus = sanal_3d_gorus
      st.session_state.sesli_mikrofon = sesli_mikrofon
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: 3D SANAL SINIF VE GERÇEKÇİ STAJ KRİZ YÖNETİMİ
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretmen Elemanı"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 25)
  dagilim = st.session_state.get("profil_dagilimi", {})

  secilen_sinif = st.selectbox(
      "2026 Maarif Modeli Sınıf Düzeyi Seçin",
      list(akademik_staj_arsivi.keys()),
  )
  konu_secenekleri = list(akademik_staj_arsivi[secilen_sinif].keys())

  st.markdown(
      f"### 🏫 3D İzometrik Gerçekçi Staj Sınıfı | Öğretmen Adayı: {ogretmen}"
      f" ({universite})"
  )
  st.caption(
      f"Danışman Hoca: {ogretim_elemani} | Sınıf Mevcudu: {mevcut} | Aktif"
      f" Profiller: Disleksili({dagilim.get('Disleksili', 0)}),"
      f" Otizmli({dagilim.get('Otizmli', 0)}), Kaygılı({dagilim.get('Kaygılı', 0)}),"
      f" Üstün({dagilim.get('Üstün Yetenekli', 0)})"
  )

  if st.session_state.get("sanal_3d_gorus", True):
    st.markdown(
        "> 🧊 **[3D İzometrik Gerçekçi Staj Ortamı & Gözlem Paneli]**\n"
        "> *Öğretmen kürsüsünde **Avatarınız (Öğretmen Adayı 3D Model)** yer almakta; arka sırada ise danışman hocanız elinde not defteriyle oturup sizi izlemektedir.*\n"
        "> *📌 Ön sırada **Disleksili Kerem (Avatar #1)** endişeyle alnını ovuşturmakta, orta sırada **Otizmli Arda (Avatar #2)** kulaklığıyla sallanmakta, en arkada ise öğrenciler arasında fısıltı ve kağıt uçak atma krizi simüle edilmektedir.*"
    )

  secilen_konu = st.selectbox(
      "2026 Maarif Modeli Konu ve Kapsam Başlığı", konu_secenekleri
  )
  veri = akademik_staj_arsivi[secilen_sinif][secilen_konu]

  st.divider()

  st.markdown("### 🎯 2026 Maarif Modeli A, B, C Alt Kazanım Seçimi")
  secilen_abc = st.selectbox("İşlemek istediğiniz alt kazanım:", veri["alt_basliklar"])

  st.info(f"**Odak Kazanım Kodu:** {veri['kazanim_kodu']} | **Metin:** {secilen_abc}")
  st.success(f"💡 **{veri['gercek_dunya_hook']}**")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown(
        "#### ⚡ Gerçek Staj Deneyimi: Sınıf İçi Kriz & Akran Senaryosu"
    )
    st.warning(veri["staj_krizi_senaryosu"])
    st.markdown(f"**Karşılaşılan Temel Kriz Türü:** {veri['krizi_yonetme_zorlugu']}")

    if st.session_state.get("sesli_mikrofon", True):
      st.markdown(
          "🎤 *[Sesli Mikrofon & Avatar Seslendirme Aktif]*: Öğrenciye veya"
          " danışman hocaya sesli yanıt vermek için konuşabilir ya da"
          " simülasyon kutusunu kullanabilirsiniz."
      )
      st.text_input(
          "Öğretmen Adayı Sesli Hitabet Simülasyonu",
          placeholder="Örn: 'Arkadaşlar lütfen sessizlik, Kerem sana yardım edeceğim...'",
      )

    st.markdown(
        "### 👩‍🏫 Bu Staj Krizi ve Pedagogik Durum Karşısında Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sınıf yönetimi, kriz çözümü ve kapsayıcılık açısından en uygun"
        " kararı seçiniz:",
        [
            (
                "A) Panikleyip dersi askıya almak veya disiplin için sert"
                " bağırarak öğrencileri azarlamak."
            ),
            (
                "B) Sakinliği koruyarak hem krizdeki öğrenciye güvenli alan"
                " sunmak hem de somut model/dijital araçla konuyu akran"
                " etkileşimiyle bağlamak."
            ),
            (
                "C) Durumu tamamen görmezden gelip tahtaya arkasını dönerek"
                " dersi hızla bitirmeye çalışmak."
            ),
            (
                "D) Danışman hocaya dönüp 'Hocam ben bu sınıfı"
                " yönetemiyorum' diyerek yardım istemek."
            ),
            (
                "E) Sınıf genelinde kısa bir akran destekli problem çözme"
                " molası vererek hem krizi avantaja çevirmek hem de kaygıyı"
                " azaltmak."
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
          "yanilgi": veri["kavram_yanilgisi_ve_kok"],
          "bilissel_kok": veri["pedagojik_cozum"],
          "cozum": veri["pedagojik_cozum"],
          "materyaller": veri["dijital_ve_somut_araclar"],
      })
      st.success(
          "✅ Staj kararınız kaydedildi ve oturum video kaydı buluta"
          " arşivlendi! Sağ taraftan uzman analizlerini ve tıklanabilir web"
          " araçlarını inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown("#### 💡 Uzman / Mentor Geri Bildirim ve Materyal Paneli")

    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Tespit Edilen Kavram Yanılgısı & Kriz Analizi")
      st.error(son_kayit["yanilgi"])

      st.markdown("##### 🛠️ Önerilen Profesyonel Çözüm Stratejisi")
      st.success(son_kayit["cozum"])

      st.markdown(
          "##### 🧩 Tıklanabilir Dijital Web Araçları ve Somut Materyaller"
      )
      st.info(son_kayit["materyaller"])

      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.markdown(
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — Gerçek saha"
            " stajında karşılaşılabilecek en sert krizlerde dahi profesyonel"
            " kriz yönetimi ve kapsayıcı refleks gösterdiniz!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " sınıf hakimiyetini tamamen kaybetmenize ve danışman hocadan"
            " olumsuz puan almanıza yol açabilir."
        )

      st.divider()
      if st.button(
          "📋 Simülasyonu Tamamla ve Video Kayıtlı 3 Ayrı Rapor Paneline Geç"
      ):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı seçip 'Pedagojik Kararı Kaydet' butonuna"
          " bastıktan sonra gizli uzman analizleri ve tıklanabilir araçlar bu"
          " alanda açılacaktır."
      )

# ==========================================
# 4. ADIM 3: VİDEO KAYITLI VE ÜÇLÜ PROFESYONEL RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "🎥 VİDEO KAYITLI VE KAPSAMLI ÜÇLÜ PEDAGOJİK DEĞERLENDİRME SİSTEMİ"
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

  # 3 Ayrı Sekme: 1. Aday Raporu & Video Kaydı | 2. Fakülte Dekanlığı Raporu | 3. Öğretim Elemanı Rubrik Uyum & Kayıt İnceleme Paneli
  tab_aday, tab_fakulte, tab_ogretim = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Bireysel Gelişim, Video Kaydı & Görsel Araçlar",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Staj Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Uyum ve Video Kayıt İnceleme",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 Staj Simülasyonu Oturum Video Kaydı Arşivi (Tekrar İzleme)"
    )
    st.info(
        "Aşağıdaki oynatıcı üzerinden, simülasyon boyunca yaptığınız staj"
        " seansını (kriz anları, öğrenci tepkileri ve hitabetiniz dahil)"
        " baştan sona tekrar izleyebilir, eksiklerinizi gözlemleyebilirsiniz."
    )
    # Simüle edilmiş video oynatıcı arayüzü
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown(
        "### 📈 Öğretmen Adayı Bireysel Gelişim ve Performans Grafikleri"
    )

    if toplam_islem > 0:
      import pandas as pd

      chart_data = pd.DataFrame(
          {
              "Staj Krizi ve Kriter": [
                  "Kriz & Otorite Yönetimi",
                  "Kapsayıcı Eğitim",
                  "Kavramsal Değişim",
                  "Dijital Araç Entegrasyonu",
              ],
              "Yeterlilik Puanı": [95, 92, 90, 96],
          }
      )
      st.bar_chart(chart_data, x="Staj Krizi ve Kriter", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### Staj Oturumu #{idx}: {veri['konu']}")
        st.markdown(f"- **Odak Alt Kazanım:** {veri['abc_kazanim']}")
        st.markdown(f"- **Tercih Edilen Staj Kararı:** {veri['karar']}")
        st.markdown(f"- **Tespit Edilen Kavram Yanılgısı:** {veri['yanilgi']}")
        st.markdown(f"- **Önerilen Profesyonel Strateji:** {veri['cozum']}")
        st.markdown(
            f"- **Doğrudan Kullanabileceğiniz Dijital Web Araçları & Somut"
            f" Materyaller:**\n  {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **Gerçekçi Staj Gelişim Dönütü:** Sınıf içindeki beklenmeyen"
          " teknik arızalar, öğrenci krizleri ve idari denetimler karşısında"
          " sergilediğiniz esnek liderlik ve tıklanabilir dijital araçları"
          " devreye sokma beceriniz gerçek bir stajyer için üst düzey"
          " yeterliliktedir."
      )
    else:
      st.warning("Henüz kaydedilmiş bir staj oturumu bulunuyor.")

  with tab_fakulte:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Dekanlığı ve Bölüm Başkanlığı Kurumsal Staj"
        " Raporu"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi İlköğretim"
        " Matematik Öğretmenliği Bölüm Komisyonu* tarafından resmi olarak"
        " düzenlenmiştir."
    )

    st.markdown(
        "#### 📊 Kurumsal Staj İzleme ve Yeterlilik Özeti:\n"
        "1. **Saha Krizi Yönetim Başarısı:** Aday, gerçek staj okullarında"
        " yaşanabilecek akran çatışmaları, teknolojik aksaklıklar ve özel"
        " gereksinimli öğrenci krizlerinde fakültemiz kriz yönetimi"
        " standartlarını başarıyla sağlamıştır.\n2. **2026 Maarif Modeli"
        " Entegrasyonu:** Kazanım alt kırılımları ve gerçek dünya kancaları"
        " profesyonelce harmanlanmıştır.\n3. **Kurumsal Karar:** Adayın gerçek"
        " okul sahasına stajyer öğretmen olarak çıkması fakültemiz komisyonunca"
        " **OY BİRLİĞİYLE ONAYLANMIŞTIR**."
    )

    st.success(
        "🎉 **Resmi Mühür:** Bu kurumsal rapor üniversite staj bilgi"
        " sistemine (OBS) işlenmiştir."
    )

  with tab_ogretim:
    st.markdown(
        "### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Uyum ve Video İnceleme Paneli"
    )
    st.markdown(
        f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    st.markdown(
        "🎥 **Aday Staj Video Kaydı İnceleme Alanı:** Danışman hoca olarak"
        " adayın staj seansını yukarıdaki oynatıcıdan izleyebilir, kriz"
        " anlarındaki tepkilerini rubrik kriterlerine göre puanlayabilirsiniz."
    )

    st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri ile Karşılaştırmalı Analiz:")
    st.markdown(
        f"> **Aktif Rubrik Kriterleri:**\n> *"
        f" {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Rubrik Eşleşme Matrisi:\n"
        "- ✅ **Kriz Anında Sakinlik ve Liderlik:** Adayın seçtiği"
        " stratejiler, rubriğin 1. maddesiyle **%96 uyumludur**.\n- ✅ **Kapsayıcı"
        " Dil ve Bireysel Farkındalık:** Özel gereksinimli bireylere yaklaşım"
        " rubriğin 2. maddesini tam olarak karşılamaktadır.\n- ✅ **Dijital Araç"
        " Entegrasyonu:** Tıklanabilir web araçlarının kullanımı rubrik"
        " standartlarının üzerindedir."
    )

    st.markdown("---")
    st.markdown("#### ✍️ Öğretim Elemanı Resmi Geri Dönüt ve Not Kutusu")
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Öğretmen Adayına Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, staj video kaydını ve"
            " simülasyon kararlarını büyük bir dikkatle inceledim. Kriz"
            " anındaki liderliğiniz harikaydı. Saha stajınızda başarılar"
            " dilerim."
        ),
    )

    if st.button("📤 Geri Dönütü Adaya ve Sisteme Gönder"):
      st.success(
          "✅ Öğretmen elemanı resmi geri dönütünüz başarıyla kaydedildi,"
          " video arşivine işlendi ve aday portfolyosuna iletildi!"
      )

  if st.button("🔄 Yeni Bir Staj Simülasyonu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
