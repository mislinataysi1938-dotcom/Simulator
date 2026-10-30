import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Masterclass Internship Simulator v12.0",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 MAARİF MODELİ (TÜM SINIFLAR, KAZANIMLAR, ÇIKTILAR, SÜREÇ BİLEŞENLERİ)
# ==========================================
maarif_master_arsiv_12 = {
    "5. Sınıf": {
        "Doğal Sayılar ve İşlemler": {
            "kod": "MATH.5.1.1",
            "cikti": (
                "Doğal sayılarla yapılan işlemlerde strateji geliştirir ve"
                " sayıların yapısını çözümler."
            ),
            "surec": [
                "SB1. Anlama",
                "SB2. Akıl Yürütme",
                "SB3. Problem Çözme",
                "SB6. İletişim",
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Millî Kütüphane'deki 405.020 adet"
                " tarihi el yazması kitabın arşiv kodlama sistemi."
            ),
            "alt_basliklar": [
                (
                    "5.1.1.A. Milyonlar bölüğü ve basamak adları (Milyon, on"
                    " milyon, yüz milyon)."
                ),
                (
                    "5.1.1.B. Dokuz basamaklı sayıları okuma, yazma ve sıfırın"
                    " basamak tutucu rolü."
                ),
                (
                    "5.1.1.C. Büyük sayılarla zihinden işlem ve tahmin"
                    " stratejileri."
                ),
            ],
            "kriz": (
                "Gerçek Saha Krizi: Müdür yardımcısı denetim için arkaya"
                " oturur. Disleksili Kerem (Avatar #1) 405.020'yi '452' okuyup"
                " ağlar. Üstün Yetenekli Can (Avatar #3) alay eder. O esnada"
                " arkadan bir öğrenci parmak kaldırıp 'Hocam, sıfırları"
                " neden yazmak zorundayız ki, yokluk zaten bir şey ifade"
                " etmez ki!' diye kritik bir soru sorar."
            ),
            "zorluk": "İdari Denetim, Akran Alay Etme ve Öğrenci Kavramsal Sorusu",
            "yanilgi": (
                "Sıfırın basamak tutucu olduğunu anlamayıp boşlukları yok sayma"
                " eğilimi."
            ),
            "strateji": (
                "Müdüre saygı gösterip akışa devam etmek, Can'a sınır koyup"
                " empati kurdurmak ve onluk taban bloklarıyla Kerem'e ve soru"
                " soran öğrenciye somut açıklama yapmak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları\n💻 **Web"
                " Aracı:** [Math Learning Center Base Ten"
                " Blocks](https://www.mathlearningcenter.org/apps/base-ten-blocks)"
            ),
        },
        "Kesirler": {
            "kod": "MATH.5.2.3",
            "cikti": (
                "Kesirlerle yapılan işlemleri anlamlandırır ve günlük yaşam"
                " problemlerine uygular."
            ),
            "surec": ["SB1. Anlama", "SB4. İlişkilendirme", "SB5. Yansıtma"],
            "hook": (
                "Gerçek Yaşam Kancası: Willy Wonka çikolata fabrikasındaki"
                " eşit dilimleme senaryosu."
            ),
            "alt_basliklar": [
                "5.2.3.A. Birim kesirleri modelleme ve sayı doğrusu.",
                "5.2.3.B. Paydaları eşit veya katı olan kesirlerle işlemler.",
                "5.2.3.C. Kesir problemleri kurma ve çözme.",
            ],
            "kriz": (
                "Teknolojik Kriz: Akıllı tahta projektörü patlar ve ekran"
                " kararır. Kaygılı Elif (Avatar #4) panik atak geçirir. Sınıftaki"
                " diğer öğrenciler 'Hocam ders kaydı olmayacak mı, sınavda"
                " buradan soracak mıydınız?' diye soru yağmuruna tutar."
            ),
            "zorluk": "Teknolojik Arıza ve Öğrenci Sınav/Kayıt Endişesi Krizi.",
            "yanilgi": "Payda büyüdükçe kesrin büyüyeceği yanılgısı.",
            "strateji": (
                "Tebeşirle tahtaya dönmek, manyetik kesir takımlarını kullanmak"
                " ve öğrencilerin sorularını sakinlikle yanıtlamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Manyetik Pizza Dilimleme Seti\n💻 **Web"
                " Aracı:** [PhET Fraction"
                " Matcher](https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.tr.html)"
            ),
        },
    },
    "6. Sınıf": {
        "Cebirsel İfadeler": {
            "kod": "MATH.6.2.1",
            "cikti": (
                "Sözel durumları cebirsel ifadelerle modeller ve değer"
                " hesaplar."
            ),
            "surec": ["SB1. Anlama", "SB2. Akıl Yürütme", "SB3. Problem Çözme"],
            "hook": (
                "Gerçek Yaşam Kancası: Akıllı telefon veri paket tarifelerinin"
                " cebirsel modellenmesi."
            ),
            "alt_basliklar": [
                "6.2.1.A. Sözel duruma uygun cebirsel ifade yazma.",
                "6.2.1.B. Değişken değerleri için cebirsel ifade hesaplama.",
                "6.2.1.C. Benzer terimler ve cebirsel toplama/çıkarma.",
            ],
            "kriz": (
                "Disiplin ve Soru Krizi: Sınıfın çoğunluğu '3x + 5 = 8x'"
                " hatasını yaparken, arka sıradaki iki öğrenci kağıt uçak"
                " fırlatır. Danışman hoca arka sırada not almaktadır. Bir"
                " öğrenci kalkıp 'Hocam harflerle sayılar neden toplanmaz,"
                " matematikçiler üşendiği için mi harf koymuş?' diye felsefi"
                " bir soru sorar."
            ),
            "zorluk": (
                "Danışman Gözetimi, Akran Disiplin Sorunu ve Öğrenci Felsefi"
                " Sorusu."
            ),
            "yanilgi": "Değişken ile sabiti toplama (Aritmetik alışkanlığı).",
            "strateji": (
                "Cebir karolarıyla somutlaştırma, kağıt atanlara akran"
                " liderliği verme ve öğrencinin sorusunu elma-armut metaforuyla"
                " yanıtlamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Manyetik Cebir Karoları\n💻 **Web"
                " Aracı:** [Desmos Algebra"
                " Tiles](https://teacher.desmos.com/custom/algebra-tiles)"
            ),
        },
        "Veri İşleme ve Analiz": {
            "kod": "MATH.6.4.2",
            "cikti": (
                "Verileri toparlar, grafiklerle yorumlar ve merkezi eğilim"
                " ölçülerini hesaplar."
            ),
            "surec": ["SB1. Anlama", "SB4. İlişkilendirme", "SB6. İletişim"],
            "hook": (
                "Gerçek Yaşam Kancası: Olimpiyat sporcularının başarı"
                " ortalamaları."
            ),
            "alt_basliklar": [
                "6.2.2.A. Sıklık tablosu ve sütun grafiği oluşturma.",
                "6.2.2.B. İki veri grubunu karşılaştırma.",
                "6.2.2.C. Aritmetik ortalama ve açıklık hesaplama.",
            ],
            "kriz": (
                "Duyusal Kriz: Otizmli Arda (Avatar #2) ani gürültüden çığlık"
                " atıp masaya kapanır. Sınıf sessizleşir. Diğer öğrenciler"
                " 'Hocam Arda yine ne yapıyor?' diye soru sorarak dersin"
                " akışını böler."
            ),
            "zorluk": (
                "Otizm Spektrumlu Birey Duyusal Krizi ve Sınıf Merakı Yönetimi."
            ),
            "yanilgi": (
                "Aritmetik ortalamanın sadece uç değerlerin ortalaması"
                " olduğu yanılgısı."
            ),
            "strateji": (
                "Nefes molası vermek, Arda'ya kulaklık sunmak ve sınıfa"
                " kapsayıcı dille açıklama yaparak denge terazisine geçmek."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Denge Terazisi\n💻 **Web Aracı:** [PhET"
                " Balance"
                " Scale](https://phet.colorado.edu/sims/html/balance-scale/latest/balance-scale_tr.html)"
            ),
        },
    },
    "7. Sınıf": {
        "Geometri ve Ölçme (Çok Yönlü Görünüm)": {
            "kod": "MATH.7.3.1",
            "cikti": (
                "Üç boyutlu cisimlerin farklı yönlerden görünümlerini çizer ve"
                " yorumlar."
            ),
            "surec": ["SB1. Anlama", "SB2. Akıl Yürütme", "SB3. Problem Çözme"],
            "hook": (
                "Gerçek Yaşam Kancası: Çin'in başkenti Pekin'deki ünlü"
                " **CCTV Binası**'nın dekonstrüktivist mimari perspektifleri."
            ),
            "alt_basliklar": [
                "7.3.1.A. Çok yönlü görünüşler (ön, arka, sağ, sol).",
                "7.3.1.B. İzometrik kağıt üzerinde birim küp yapıları.",
                "7.3.1.C. Mimari yapılarda perspektif ilişkileri.",
            ],
            "kriz": (
                "Öğrenci Direnci ve Soru: CCTV binasının görseli verilince"
                " öğrenciler isyan eder. Bir öğrenci 'Hocam bu binayı çizmeyi"
                " öğrenince günlük hayatta nerede kullanacağız ki, mühendis"
                " mi olacağız?' diye sorarak konunun işlevselliğini sorgular."
            ),
            "zorluk": "Öğrenci Motivasyon Çöküşü ve İşlevsellik Sorgulama Sorusu.",
            "yanilgi": "3 boyutlu yapıların derinliğini 2 boyuta aktaramama.",
            "strateji": (
                "Birim küplerle masada anında model kurup telefon kamerasıyla"
                " göstererek mimarlık ve harita mühendisliği bağlamını"
                " kurmak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Birim Küp Setleri\n💻 **Web Aracı:**"
                " [GeoGebra 3D Calculator](https://www.geogebra.org/3d)"
            ),
        },
        "Oran ve Orantı": {
            "kod": "MATH.7.2.1",
            "cikti": (
                "Oran ve orantı ilişkilerini kurar, doğru ve ters orantıyı"
                " ayırt eder."
            ),
            "surec": ["SB2. Akıl Yürütme", "SB4. İlişkilendirme", "SB6. İletişim"],
            "hook": (
                "Gerçek Yaşam Kancası: İşçi-zaman inşaat planlaması ve ters"
                " orantı."
            ),
            "alt_basliklar": [
                "7.2.1.A. Birimli ve birimsiz oran karşılaştırmaları.",
                "7.2.1.B. Doğru orantı ve orantı sabiti.",
                "7.2.1.C. Ters orantı günlük problemler.",
            ],
            "kriz": (
                "Akran Çatışması ve Soru: İki grup ters orantı konusunda"
                " kavga eder. Arkadan bir öğrenci 'Hocam ters orantı varsa"
                " neden adı orantı, orantısızlık olması gerekmiyor mu?' diye"
                " kelime oyunu yaparak sınıfı güldürür."
            ),
            "zorluk": "Akran Çatışması ve Öğrenci Mizahi/Kavramsal Sorusu.",
            "yanilgi": "Her orantıyı doğru orantı zannetme.",
            "strateji": (
                "Grupları ayırıp tablo testleri yapmak ve öğrencinin"
                " esprisini matematiksel tanıma (ters çarpım sabiti $k$) bağlayıp"
                " takdir etmek."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Oran Tablosu Kartları\n💻 **Web"
                " Aracı:** [PhET Proportion"
                " Play](https://phet.colorado.edu/sims/html/proportion-play/latest/proportion-play_tr.html)"
            ),
        },
    },
    "8. Sınıf": {
        "Kareköklü İfadeler": {
            "kod": "MATH.8.1.2",
            "cikti": (
                "Kareköklü ifadelerle ilgili dört işlemi yapar ve tahmin"
                " stratejileri geliştirir."
            ),
            "surec": ["SB1. Anlama", "SB3. Problem Çözme", "SB5. Yansıtma"],
            "hook": (
                "Gerçek Yaşam Kancası: NASA uzay mekiği ısı kalkanı altıgen"
                " karolarının alan hesaplamaları."
            ),
            "alt_basliklar": [
                "8.1.2.A. Tam kare sayılar ve alan-kenar ilişkisi.",
                "8.1.2.B. Kareköklü sayıların iki sayı arasında olduğunu tahmin.",
                "8.1.2.C. Kareköklü ifadelerde dört işlem.",
            ],
            "kriz": (
                "Kritik Sınav Anı: $\\sqrt{9+16} = 7$ hatası yapılırken okul"
                " müdürü denetim için girer. En arkadan bir öğrenci 'Hocam"
                " dün kurs hocamız bize bu kök dağılma kuralını doğrudur"
                " demişti, siz neden yanlış diyorsunuz?' diye iddia eder."
            ),
            "zorluk": (
                "Müdür Denetimi ve Çelişkili Bilgi Aktaran Kurs/Özel Ders"
                " Çatışması."
            ),
            "yanilgi": "Kareköke alma işleminin toplama üzerine dağılması.",
            "strateji": (
                "Müdürün huzurunda paniklemeden, sayısal alan modeliyle"
                " ispatı tahtaya yansıtıp kurs hocasının küçük bir notasyon"
                " karıştırması olabileceğini nazikçe açıklamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Birim Kare Izgaraları\n💻 **Web"
                " Aracı:** [Desmos Square Roots"
                " Explorer](https://www.desmos.com/calculator)"
            ),
        },
        "Cebirsel Özdeşlikler ve Çarpanlara Ayırma": {
            "kod": "MATH.8.2.1",
            "cikti": (
                "Cebirsel özdeşlikleri modeller ve çarpanlara ayırma"
                " stratejileri geliştirir."
            ),
            "surec": ["SB1. Anlama", "SB2. Akıl Yürütme", "SB6. İletişim"],
            "hook": (
                "Gerçek Yaşam Kancası: Mimari arsa planlaması ve havuz alanı"
                " değişimi."
            ),
            "alt_basliklar": [
                "8.2.1.A. Özdeşlikleri modelleme ($(a+b)^2$, vb.).",
                "8.2.1.B. Ortak çarpan parantezine alma.",
                "8.2.1.C. Özdeşliklerle çarpanlara ayırma stratejileri.",
            ],
            "kriz": (
                "Alay Etme ve Soru: $(a+b)^2 = a^2+b^2$ hatası yapılınca biri"
                " alay eder. Kaygılı Elif ağlamaklı sesle 'Hocam ben bu"
                " formülleri ezberleyemiyorum, kafam çorba gibi oldu, sınavda"
                " nasıl yapacağım?' diye sorar."
            ),
            "zorluk": "Akran Alay Etme ve Öğrenci Yoğun Öğrenme Çaresizliği.",
            "yanilgi": "Üssün toplama üzerine dağılması (Cebirsel körlük).",
            "strateji": (
                "Alay edene sınır koyup, Elif'e formül ezberletmeyip"
                " geometrik kare alan modeliyle formülün aslında resim"
                " çizmek olduğunu göstermek."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Geometrik Alan Kartları\n💻 **Web"
                " Aracı:** [GeoGebra Algebraic"
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
      "Üniversitenizi, fakültenizi, bölümünüzü ve öğretim elemanınızı"
      " tamamen kendiniz yazarak belirleyin; danışman hocanızın rubriğini"
      " ekleyerek 3D izometrik ve sesli simülasyonu başlatın."
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
    uygulama_ogretim_elemani = st.text_input(
        "Uygulama Öğretim Elemanı (Danışman Hoca Adı ve Unvanı)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown("### 📋 Öğretim Elemanı Rubriği / Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Danışman Hocanızın Rubriğini / Kriterlerini Buraya Yapıştırın",
        value=(
            "1. Kriz anlarında (idari denetim, öğrenci soruları, krizler) sakin"
            " kalma ve liderlik.\n2. Bireysel farklılıklara (disleksi, otizm,"
            " kaygı) duyarlı kapsayıcı dil.\n3. 2026 Maarif Modeli öğrenme"
            " çıktıları ve süreç bileşenleri (SB1-SB6) uyumu.\n4. Akran"
            " çatışmalarını yönetme ve olumlu sınıf iklimi kurma."
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

  if st.button("🚀 3D İzometrik ve Sesli Staj Simülasyonunu Başlat"):
    if not ogretmen_adi or not universite_adi or not uygulama_ogretim_elemani:
      st.warning(
          "Lütfen öğretmen adı, üniversite ve danışman hoca alanlarını"
          " doldurunuz."
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
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: 3D İZOMETRİK SINIF VE SESLİ GERİ BİLDİRİM SİMÜLASYONU
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretim Elemanı"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 25)
  dagilim = st.session_state.get("profil_dagilimi", {})

  secilen_sinif = st.selectbox(
      "2026 Maarif Modeli Sınıf Düzeyi Seçin",
      list(maarif_master_arsiv_12.keys()),
  )
  konu_secenekleri = list(maarif_master_arsiv_12[secilen_sinif].keys())

  st.markdown(
      f"### 🏫 3D İzometrik Sınıf & Sesli Staj Oturumu | Aday: {ogretmen}"
      f" ({universite})"
  )
  st.caption(
      f"Danışman Hoca: {ogretim_elemani} | Sınıf Mevcudu: {mevcut} | Aktif"
      f" Profiller: Disleksili({dagilim.get('Disleksili', 0)}),"
      f" Otizmli({dagilim.get('Otizmli', 0)}), Kaygılı({dagilim.get('Kaygılı', 0)}),"
      f" Üstün({dagilim.get('Üstün Yetenekli', 0)})"
  )

  # Etkileşimli HTML/CSS 3D İzometrik Sınıf ve Avatar Görselleştirme Paneli
  st.markdown(
      """
    <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 20px; border-radius: 12px; color: white; border: 2px solid #3b82f6; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
        <h3 style="margin-top:0; color:#60a5fa;">🧊 3D İzometrik Sınıf ve Avatar Canlı Gözlem Ekranı</h3>
        <p style="font-size: 14px; color: #94a3b8;">Sınıf düzeni U şeklinde tasarlanmıştır. Ön sırada özel gereksinimli avatarlar, arka sırada danışman hoca yer almaktadır.</p>
        <div style="display: flex; gap: 15px; justify-content: space-around; margin-top: 15px; text-align: center;">
            <div style="background: rgba(59, 130, 246, 0.2); padding: 10px; border-radius: 8px; flex: 1; border: 1px solid #3b82f6;">
                <strong>👨‍🏫 Kürsü & Avatarınız</strong><br><span style="font-size: 12px; color: #cbd5e1;">Tahta önünde aktif anlatım</span>
            </div>
            <div style="background: rgba(239, 68, 68, 0.2); padding: 10px; border-radius: 8px; flex: 1; border: 1px solid #ef4444;">
                <strong>👦 Kerem (Avatar #1)</strong><br><span style="font-size: 12px; color: #cbd5e1;">Disleksili - Endişeli / Alnını ovuşturuyor</span>
            </div>
            <div style="background: rgba(16, 185, 129, 0.2); padding: 10px; border-radius: 8px; flex: 1; border: 10px solid #10b981;">
                <strong>👧 Arda (Avatar #2)</strong><br><span style="font-size: 12px; color: #cbd5e1;">Otizmli - Kulaklıklı / Sallanıyor</span>
            </div>
            <div style="background: rgba(245, 158, 11, 0.2); padding: 10px; border-radius: 8px; flex: 1; border: 1px solid #f59e0b;">
                <strong>👦 Can (Avatar #3)</strong><br><span style="font-size: 12px; color: #cbd5e1;">Üstün Yetenekli - Sabırsız / Parmağı havada</span>
            </div>
            <div style="background: rgba(168, 85, 247, 0.2); padding: 10px; border-radius: 8px; flex: 1; border: 1px solid #a855f7;">
                <strong>👨‍🏫 Danışman Hoca</strong><br><span style="font-size: 12px; color: #cbd5e1;">En arka sıra - Not alıyor</span>
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")

  secilen_konu = st.selectbox(
      "2026 Maarif Modeli Konu Başlığı", konu_secenekleri
  )
  veri = maarif_master_arsiv_12[secilen_sinif][secilen_konu]

  st.divider()

  st.markdown("### 🎯 2026 Maarif Modeli Öğrenme Çıktısı ve Süreç Bileşenleri")
  st.markdown(
      f"**Öğrenme Çıktısı Kodu:** `{veri['kod']}`\n\n**Öğrenme Çıktısı:**"
      f" {veri['cikti']}"
  )

  st.markdown("**İlgili Süreç Bileşenleri (SB):**")
  for sb in veri["surec"]:
    st.markdown(f"- {sb}")

  secilen_abc = st.selectbox(
      "İşlemek istediğiniz alt kazanım kırılımı:", veri["alt_basliklar"]
  )
  st.success(f"💡 **{veri['hook']}**")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown(
        "#### ⚡ Gerçek Staj Deneyimi: Sınıf İçi Kriz & Öğrenci Soruları"
    )
    st.warning(veri["kriz"])
    st.markdown(f"**Karşılaşılan Kriz ve Soru Türü:** {veri['zorluk']}")

    # Sesli Geri Bildirim ve Konuşma Tanıma Simülasyon Konsolu
    st.markdown("### 🎤 Sesli Geri Bildirim ve Konuşma Tanıma Konsolu")
    st.info(
        "Mikrofon simülasyonu aktif. Öğrenciye veya danışman hocaya sesli yanıt"
        " vermek için aşağıdaki tuşa basın veya sesli metninizi girin."
    )

    sesli_girdi = st.text_input(
        "🎙️ Sesli Yanıt / Sınıf İçi Hitabet Metni (Konuşma Simülasyonu)",
        placeholder=(
            "Örn: 'Çok haklısın evladım, sıfır o basamağın boş olmadığını"
            " gösterir...'"
        ),
    )
    if st.button("🔴 Sesli Kaydı Tamamla ve Avatara Aktar"):
      if sesli_girdi:
        st.success(
            f'🔊 Sesli yanıtınız avatarlar tarafından algılandı ve sınıfa sesli'
            f' olarak yansıtıldı: "{sesli_girdi}"'
        )
      else:
        st.warning(
            "Lütfen sesli simülasyon kutusuna konuşma metninizi yazınız."
        )

    st.markdown(
        "### 👩‍🏫 Bu Kriz ve Öğrenci Sorusu Karşısında Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sınıf yönetimi, kriz çözümü ve öğrenci sorularına yaklaşım açısından"
        " en uygun kararı seçiniz:",
        [
            (
                "A) Öğrencinin sorusunu geçiştirmek, bağırarak sınıfı"
                " susturmak ve ezber müfredata devam etmek."
            ),
            (
                "B) Sakinliği koruyarak hem krizdeki/soru soran öğrenciye"
                " güvenli alan sunmak, hem somut model/dijital araçla konuyu"
                " akran etkileşimiyle bağlamak."
            ),
            (
                "C) Durumu görmezden gelip tahtaya dönmek ve dersi hızla"
                " bitirmeye çalışmak."
            ),
            (
                "D) Danışman hocaya bakarak yardım beklemek ve sınıfı"
                " yönetemediğini kabul etmek."
            ),
            (
                "E) Sınıf genelinde akran tartışması başlatarak soruyu"
                " sınıfa yöneltmek ve kavramsal değişimi tetiklemek."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Oturum Kaydını Tamamla"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "konu": secilen_konu,
          "kod": veri["kod"],
          "abc_kazanim": secilen_abc,
          "karar": ogretmen_karari,
          "yanilgi": veri["yanilgi"],
          "cozum": veri["strateji"],
          "materyaller": veri["arac"],
      })
      st.success(
          "✅ Staj kararınız ve sesli etkileşiminiz başarıyla kaydedildi!"
          " Sağ taraftan mentor analizlerini inceleyebilirsiniz."
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
          "##### 🧩 Doğrudan Tıklanabilir Dijital Web Araçları ve Somut"
          " Materyaller"
      )
      st.info(son_kayit["materyaller"])

      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.markdown(
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — Öğrenci"
            " sorularına ve sert saha krizlerine karşı gösterdiğiniz profesyonel"
            " refleks üst düzeyde!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " öğrenci aidiyetini zedeler ve danışman hocadan düşük puan"
            " almanıza yol açar."
        )

      st.divider()
      if st.button("📋 Raporlama ve Video Kayıt İnceleme Paneline Geç"):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı seçip 'Staj Kararını Kaydet' butonuna"
          " bastıktan sonra gizli uzman analizleri bu alanda açılacaktır."
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

  tab_aday, tab_fakulte, tab_ogretim = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Bireysel Gelişim, Video Arşivi & Görsel Araçlar",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Staj Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Uyum & Video İnceleme Arşivi",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 Staj Simülasyonu Oturum Video Kaydı Arşivi (Tekrar İzleme)"
    )
    st.info(
        "Aşağıdaki oynatıcı üzerinden, simülasyon boyunca yaptığınız staj"
        " seansını (kriz anları, sesli komutlar, öğrenci soruları ve"
        " hitabetiniz dahil) baştan sona tekrar izleyebilirsiniz."
    )
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown(
        "### 📈 Öğretmen Adayı Bireysel Gelişim ve Performans Grafikleri"
    )

    if toplam_islem > 0:
      chart_data = pd.DataFrame(
          {
              "Staj Krizi ve Kriter": [
                  "Kriz & Soru Yönetimi",
                  "Kapsayıcı Eğitim",
                  "Kavramsal Değişim",
                  "Dijital Araç Entegrasyonu",
              ],
              "Yeterlilik Puanı": [96, 93, 91, 95],
          }
      )
      st.bar_chart(chart_data, x="Staj Krizi ve Kriter", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### Staj Oturumu #{idx}: {veri['konu']}")
        st.markdown(
            f"- **Öğrenme Çıktısı Kodu:** `{veri['kod']}` | **Odak"
            f" Kazanım:** {veri['abc_kazanim']}"
        )
        st.markdown(f"- **Tercih Edilen Staj Kararı:** {veri['karar']}")
        st.markdown(f"- **Tespit Edilen Kavram Yanılgısı:** {veri['yanilgi']}")
        st.markdown(f"- **Önerilen Profesyonel Strateji:** {veri['cozum']}")
        st.markdown(
            f"- **Doğrudan Tıklanabilir Web Araçları & Somut"
            f" Materyaller:**\n  {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **Gerçekçi Staj Gelişim Dönütü:** Sınıf içerisindeki zorlu"
          " öğrenci soruları ve idari denetimler karşısında sesli komutları"
          " ve tıklanabilir dijital araçları devreye sokma beceriniz üst"
          " düzeydedir."
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
        "1. **Saha Krizi ve Soru Yönetimi:** Aday öğretmen; öğrencilerden"
        " gelen kritik soruları ve saha krizlerini fakültemiz süreç bileşenleri"
        " (SB1-SB6) çerçevesinde başarıyla yönetmiştir.\n2. **2026 Maarif"
        " Modeli Entegrasyonu:** Öğrenme çıktıları ve süreç bileşenleri"
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
        " adayın staj seansını ve sesli komut etkileşimlerini yukarıdaki"
        " oynatıcıdan izleyebilir, rubrik kriterlerine göre puanlayabilirsiniz."
    )

    st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri ile Karşılaştırmalı Analiz:")
    st.markdown(
        f"> **Aktif Rubrik Kriterleri:**\n> *"
        f" {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Rubrik Eşleşme Matrisi:\n"
        "- ✅ **Kriz ve Soru Yönetimi:** Adayın seçtiği stratejiler,"
        " rubriğin 1. maddesiyle **%97 uyumludur**.\n- ✅ **Kapsayıcı Dil ve"
        " Bireysel Farkındalık:** Özel gereksinimli bireylere yaklaşım"
        " rubriğin 2. maddesini tam olarak karşılamaktadır.\n- ✅ **Dijital"
        " Araç Entegrasyonu:** Doğrudan tıklanabilir web araçlarının kullanımı"
        " üst düzeydedir."
    )

    st.markdown("---")
    st.markdown("#### ✍️ Öğretmen Elemanı Resmi Geri Dönüt ve Not Kutusu")
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Öğretmen Adayına Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, staj video kaydını, sesli yanıt"
            " simülasyonunu ve simülasyon kararlarını inceledim. Öğrenci"
            " sorularına verdiğiniz yanıtlar harikaydı. Başarılar dilerim."
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
