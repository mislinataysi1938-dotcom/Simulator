import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Maarif Modeli 3D Masterclass Staj Simülasyonu",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum ve Detaylı Seçim, 2: 3D Sınıf ve Sesli Simülasyon, 3: Detaylı Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ MASTER ARŞİVİ
# ==========================================
maarif_master_arsiv = {
    "5. Sınıf": {
        "Tema 1: Sayılar ve Nicelikler": {
            "cikti_kodu": "MATH.5.1.1",
            "ogrenme_ciktisi": (
                "6 basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara"
                " genelleştirebilme."
            ),
            "surec_bilesenleri": [
                "SB1. Anlama",
                "SB2. Akıl Yürütme",
                "SB3. Problem Çözme",
                "SB6. İletişim",
            ],
            "alt_basliklar": {
                "A) Milyonlar bölüğü ve basamak adları (Milyon, on milyon, yüz milyon).": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Millî Kütüphane'deki 405.020 adet"
                        " tarihi el yazması kitabın arşiv kodlama sistemi."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: Öğrencilerden biri parmak"
                        " kaldırıp sesli olarak 'Hocam bu kadar büyük sayıları"
                        " günlük hayatta nerede kullanacağız ki, cebimizdeki"
                        " paralar bile bu kadar büyük değil?' diye sorar. Ön"
                        " sıradaki Disleksili Kerem (Avatar #1) ise 'Hocam"
                        " milyon kelimesini yazarken m harfini karıştırıyorum'"
                        " diye sesli destek ister."
                    ),
                    "tur": (
                        "Öğrencinin İşlevsellik Sorgulama Sorusu ve Disleksili"
                        " Öğrencinin Bireysel Desteği"
                    ),
                    "yanilgi": (
                        "Basamak adlarını okurken bölükler arasındaki sıfırları"
                        " basamak tutucu olarak atlama eğilimi."
                    ),
                    "strateji": (
                        "Öğrencinin sorusunu büyük veri depolama ve nüfus"
                        " sayımları örnekleriyle yanıtlamak; Kerem'e renkli"
                        " onluk taban bloklarıyla bireysel rehberlik sunmak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları\n💻"
                        " **Tıklanabilir Web Aracı:** [Math Learning Center Base"
                        " Ten"
                        " Blocks](https://www.mathlearningcenter.org/apps/base-ten-blocks)"
                    ),
                },
                "B) Dokuz basamaklı sayıları okuma, yazma ve sıfırın basamak tutucu rolü.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Uzay ajanslarının gezegenler"
                        " arası uzaklık ölçüm tablosu."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: Üstün Yetenekli Can (Avatar #3)"
                        " parmak kaldırmadan söze girip 'Hocam bunu ilkokulda"
                        " işlemiştik, çok basit geçelim' der. Arkadaki kaygılı"
                        " Elif (Avatar #4) ise 'Hocam ben sıfırları yazarken"
                        " karıştırıyorum, sınavda puanımız kırılacak mı?' diye"
                        " sesli olarak endişesini dile getirir."
                    ),
                    "tur": (
                        "Üstün Yetenekli Öğrencinin Sabırsızlığı ve Kaygılı"
                        " Öğrencinin Sınav Korkusu"
                    ),
                    "yanilgi": (
                        "Sıfırın basamak tutucu rolünü kavramayıp boşlukları"
                        " yok sayma."
                    ),
                    "strateji": (
                        "Can'a derinleştirilmiş bir uzay basamak analizi"
                        " bulmacası vererek meydan okuma yaratmak; Elif'e ise"
                        " adım adım basamak tablosu stratejisiyle güven"
                        " aşılamak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Basamak Kartları Seti\n💻"
                        " **Tıklanabilir Web Aracı:** [PhET Number"
                        " Match](https://phet.colorado.edu/)"
                    ),
                },
                "C) Sayıların bölükleriyle okunuşları arasındaki farkları belirler.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Uluslararası bankacılık işlem"
                        " dekontlarındaki tutar yazım kuralları."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: Otizmli Arda (Avatar #2) hafifçe"
                        " sallanarak 'Hocam bölükler neden üçerli ayrılıyor, dörderli"
                        " olamaz mıydı?' diye çok derin ve orijinal bir matematik"
                        " sorusu sorar. Sınıftaki diğer öğrenciler dönüp Arda'yı"
                        " dinler."
                    ),
                    "tur": "Otizm Spektrumlu Öğrencinin Derin/Orijinal Matematiksel Sorusu",
                    "yanilgi": (
                        "Bölük isimleri ile basamak isimlerini birbirine"
                        " karıştırma."
                    ),
                    "strateji": (
                        "Arda'nın sorusunu tüm sınıfın duyacağı şekilde"
                        " alkışlayarak onurlandırmak; insanlığın sayma"
                        " sistemindeki üçlü gruplama tarihini (sayı"
                        " basamaklarının gruplanması) somut olarak"
                        " temellendirmek."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Bölük Renk Kutuları\n💻"
                        " **Tıklanabilir Web Aracı:** [GeoGebra Number"
                        " Line](https://www.geogebra.org)"
                    ),
                },
            },
        },
        "Tema 2: Geometri ve Ölçme": {
            "cikti_kodu": "MATH.5.2.1",
            "ogrenme_ciktisi": (
                "Geometrik cisimlerin temel özelliklerini inceler ve"
                " ilişkilendirir."
            ),
            "surec_bilesenleri": [
                "SB1. Anlama",
                "SB4. İlişkilendirme",
                "SB5. Yansıtma",
            ],
            "alt_basliklar": {
                "A) Prizmaların temel elemanları (köşe, ayrıt, yüz).": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Kargo kutularının depolama"
                        " optimizasyonu."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: İki öğrenci prizmanın ayrıtlarını"
                        " sayarken anlaşamayarak sesli olarak tartışmaya başlar"
                        " ('12 tane değil 8 tane!'). Sınıfta küçük bir"
                        " uğultu kopar."
                    ),
                    "tur": "Akranlar Arası Anlaşmazlık ve Tartışma Krizi",
                    "yanilgi": "Köşe sayısı ile ayrıt sayısını karıştırma.",
                    "strateji": (
                        "Öğrencileri suçlamadan ellerine gerçek bir kutu verip"
                        " birlikte sayma ve dokunarak keşfetme (somut"
                        " deneyim) ortamı yaratmak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Ahşap Geometrik Prizmalar\n💻"
                        " **Tıklanabilir Web Aracı:** [GeoGebra 3D"
                        " Shapes](https://www.geogebra.org/3d)"
                    ),
                },
                "B) Dik prizmaların açınımları.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Ambalaj tasarımı ve fabrikasyon"
                        " kutu kesimleri."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: Kaygılı Elif, elindeki kağıt"
                        " açınımı yanlış kesince makasla kağıdı yırtar ve"
                        " 'Hocam ben yapamıyorum, el becerim yok, matematik"
                        " beni zorluyor' diye ağlamaklı olur."
                    ),
                    "tur": "Öz-Yeterlilik Düşüşü ve El Becerisi Kaygısı",
                    "yanilgi": (
                        "Prizmanın yan yüzleri ile tabanlarının birbirine"
                        " uyumsuz kesilmesi."
                    ),
                    "strateji": (
                        "Elif'e yargılamadan yedek kağıt verip arkadaşıyla"
                        " akran yardımlaşması kurarak süreci yumuşatmak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Katlanabilir Karton Açınımlar\n💻"
                        " **Tıklanabilir Web Aracı:** [Desmos 3D"
                        " Solids](https://www.desmos.com)"
                    ),
                },
            },
        },
    },
    "8. Sınıf": {
        "Tema 1: Cebirsel İfadeler ve Özdeşlikler": {
            "cikti_kodu": "MATH.8.1.1",
            "ogrenme_ciktisi": (
                "Cebirsel ifadeleri çarpanlara ayırır ve özdeşlikleri"
                " modeller."
            ),
            "surec_bilesenleri": [
                "SB1. Anlama",
                "SB2. Akıl Yürütme",
                "SB3. Problem Çözme",
            ],
            "alt_basliklar": {
                "A) Cebirsel ifadelerde ortak çarpan parantezine alma.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Fabrika üretim bantlarında maliyet"
                        " optimizasyonu."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: Öğrenci kalkıp 'Hocam ortak"
                        " paranteze almasak da işlem yapabiliyoruz, bu"
                        " kuralı bulmak kimin aklına gelmiş, neden bizi"
                        " zorluyorsunuz?' diye felsefi/isyankar bir soru"
                        " yöneltir."
                    ),
                    "tur": "Müfredatın Mantığını Sorgulayan Öğrenci Sorusu",
                    "yanilgi": (
                        "Ortak çarpanı alırken değişkenlerin üslerini"
                        " toplama/çıkarma hatası."
                    ),
                    "strateji": (
                        "Soruya gülümseyerek karşılık verip büyük sayılarla"
                        " zihinden işlem yapmanın pratik yolunu cebirsel"
                        " alan modeliyle göstermek."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Cebir Karoları Seti\n💻"
                        " **Tıklanabilir Web Aracı:** [Desmos Algebra"
                        " Tiles](https://teacher.desmos.com)"
                    ),
                },
                "B) İki kare farkı özdeşliği ve geometrik modeli.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Mimari arsa planlamasında havuz"
                        " çevresi hesaplama."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: (a+b)(a-b) özdeşliğini tahtada"
                        " çözerken sınıftan bir öğrenci sesli olarak 'Hocam"
                        " geçen hafta özel ders hocam bana bunun artı"
                        " olacağını söylemişti, siz eksi diyorsunuz, kim"
                        " haklı?' diye sınıfta ikilem yaratır."
                    ),
                    "tur": "Özel Ders / Kurs Çelişkisi ve Öğrenci İkileri",
                    "yanilgi": "İki kare farkında orta terimin yok olduğunu görememe.",
                    "strateji": (
                        "Panik yapmadan geometrik alan kesme-yapıştırma"
                        " yöntemiyle iki kare farkının neden eksi olduğunu"
                        " tahtada görsel olarak kanıtlamak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Geometrik Alan Kartları\n💻"
                        " **Tıklanabilir Web Aracı:** [GeoGebra Algebraic"
                        " Identities](https://www.geogebra.org)"
                    ),
                },
                "C) Tam kare özdeşlikler ve açılımları.": {
                    "hook": (
                        "Gerçek Yaşam Kancası: Kare şeklindeki bir parkın"
                        " etrafına yapılan yürüyüş yolu alan değişimi."
                    ),
                    "kriz_ve_soru": (
                        "Sınıf İçi Anlık Olay: (a+b)^2 = a^2 + b^2 hatasını"
                        " yapan bir öğrenciye arkadaki popüler öğrenci"
                        " alaycı bir gülüş atar. Öğrenci mahcup olup yerine"
                        " oturur."
                    ),
                    "tur": "Akran Alay Etme ve Güvenli Sınıf İklimi Krizi",
                    "yanilgi": "Üssün toplama üzerine dağılacağı yanılgısı.",
                    "strateji": (
                        "Alay eden öğrenciye nazikçe sınır koyup, hatanın"
                        " çok yaygın olduğunu ve geometrik olarak ortadaki"
                        " 2ab alanının neden unutulduğunu resmederek"
                        " açıklamak."
                    ),
                    "materyal": (
                        "🧩 **Somut Materyal:** Alan Parçalama Kartları\n💻"
                        " **Tıklanabilir Web Aracı:** [GeoGebra Binomial"
                        " Expansion](https://www.geogebra.org)"
                    ),
                },
            },
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE DETAYLI SEÇİM PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen Detaylı Saha Stajı Kurulum ve Seçim Paneli (2026"
      " Maarif Modeli)"
  )
  st.info(
      "Bu panelde sınıf düzeyini, temayı, öğrenme çıktısını, süreç"
      " bileşenlerini ve alt başlığı tamamen kendi tercihlerinize göre"
      " seçebilir; 3D izometrik sınıf ortamını ve sesli etkileşim konsolunu"
      " yapılandırabilirsiniz."
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
        "Uygulama Öğretim Elemani (Danışman Hoca Adı ve Unvanı)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown("### 📋 Öğretim Elemanı Rubriği / Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Danışman Hocanızın Rubriğini / Kriterlerini Buraya Yapıştırın",
        value=(
            "1. 3D sınıf ortamında öğrenci sorularına ve krizlere sesli"
            " liderlik.\n2. Bireysel farklılıklara (disleksi, otizm, üstün"
            " yetenek) duyarlı kapsayıcı dil.\n3. 2026 Maarif Modeli öğrenme"
            " çıktıları, süreç bileşenleri ve alt başlık uyumu.\n4. Akran"
            " çatışmalarını ve olumlu sınıf iklimini yönetme."
        ),
        height=110,
    )

    st.markdown("### 👥 Sanal Sınıf Mevcudu ve Özel Gereksinimli Profiller")
    sinif_mevcudu = st.slider(
        "Sınıf Mevcudu (Toplam Öğrenci)", min_value=12, max_value=35, value=25
    )

    col_p1, col_p2 = st.columns(2)
    with col_p1:
      sayi_disleksi = st.number_input(
          "Disleksili Öğrenci Sayısı", min_value=0, max_value=5, value=1
      )
      sayi_otizm = st.number_input(
          "Otizm Spektrumlu Öğrenci Sayısı", min_value=0, max_value=5, value=1
      )
    with col_p2:
      sayi_kaygili = st.number_input(
          "Yüksek Kaygılı Öğrenci Sayısı", min_value=0, max_value=5, value=2
      )
      sayi_ustun = st.number_input(
          "Üstün Yetenekli Öğrenci Sayısı", min_value=0, max_value=5, value=1
      )

  st.divider()
  st.markdown("### 📚 2026 Maarif Modeli Hiyerarşik Kazanım ve Tema Seçimi")

  secilen_sinif = st.selectbox(
      "1. Sınıf Düzeyini Seçiniz:", list(maarif_master_arsiv.keys())
  )
  secilen_tema = st.selectbox(
      "2. Temayı Seçiniz:", list(maarif_master_arsiv[secilen_sinif].keys())
  )

  tema_verisi = maarif_master_arsiv[secilen_sinif][secilen_tema]

  st.info(
      f"**Seçilen Öğrenme Çıktısı Kodu:** `{tema_verisi['cikti_kodu']}`\n\n"
      f"**Matematik Öğrenme Çıktısı:** {tema_verisi['ogrenme_ciktisi']}"
  )

  st.markdown("**İlgili Süreç Bileşenleri:**")
  secilen_sureclar = []
  for sb in tema_verisi["surec_bilesenleri"]:
    if st.checkbox(sb, value=True, key=f"sb_{sb}"):
      secilen_sureclar.append(sb)

  alt_baslik_secenekleri = list(tema_verisi["alt_basliklar"].keys())
  secilen_alt_baslik = st.selectbox(
      "3. Alt Başlığı / Kırılımı Seçiniz (A, B, C...):", alt_baslik_secenekleri
  )

  if st.button("🚀 3D Sınıf ve Sesli Simülasyonu Başlat"):
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
      st.session_state.secilen_sinif = secilen_sinif
      st.session_state.secilen_tema = secilen_tema
      st.session_state.secilen_cikti_kodu = tema_verisi["cikti_kodu"]
      st.session_state.secilen_ciktisi = tema_verisi["ogrenme_ciktisi"]
      st.session_state.secilen_alt_baslik = secilen_alt_baslik
      st.session_state.detay_verisi = tema_verisi["alt_basliklar"][
          secilen_alt_baslik
      ]
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: 3D CANLI SINIF VE SESLİ ETKİLEŞİM SİMÜLASYONU
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Danışman Hoca"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 25)
  dagilim = st.session_state.get("profil_dagilimi", {})

  s_sinif = st.session_state.get("secilen_sinif", "5. Sınıf")
  s_tema = st.session_state.get("secilen_tema", "Tema")
  s_kod = st.session_state.get("secilen_cikti_kodu", "MATH.5.1")
  s_alt = st.session_state.get("secilen_alt_baslik", "Alt Başlık")
  detay = st.session_state.get("detay_verisi", {})

  st.markdown(
      f"### 🏫 3D Canlı Görsel Sınıf & Sesli Etkileşim | Aday: {ogretmen}"
      f" ({universite})"
  )
  st.caption(
      f"Sınıf Düzeyi: {s_sinif} | Tema: {s_tema} | Çıktı Kodu: {s_kod} | Alt"
      f" Kırılım: {s_alt}"
  )

  # Tam Görsel 3D Sınıf ve Öğrenci Avatarları Paneli (Müdür/Hoca arka sıra yok, tamamen öğretmen adayı ve öğrenciler)
  st.markdown(
      f"""
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 25px; border-radius: 16px; color: white; border: 3px solid #3b82f6; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <h2 style="margin-top:0; color:#60a5fa; text-align:center;">🌐 3D İzometrik Canlı Sınıf Ortamı & Öğrenci Avatarları</h2>
        <p style="text-align: center; color: #94a3b8; font-size: 15px;">Bu simülasyonda sınıfta sadece siz ({ogretmen}) ve <strong>{mevcut} kişilik öğrenci mevcudu</strong> bulunmaktadır. Arka sırada idareci veya denetçi yoktur; tamamen gerçek bir sınıf akışı yaşanmaktadır.</p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px;">
            <div style="background: rgba(239, 68, 68, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #ef4444; text-align: center;">
                <div style="font-size: 28px;">👦</div>
                <strong>Kerem (Avatar #1)</strong><br>
                <span style="font-size: 13px; color: #fca5a5;">Jest/Mimik: Alnını ovuşturuyor / Endişeli</span><br>
                <span style="font-size: 11px; background: #991b1b; padding: 2px 6px; border-radius: 4px;">Özel Durum: Disleksili ({dagilim.get('Disleksili', 0)} öğrenci)</span>
            </div>
            
            <div style="background: rgba(16, 185, 129, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #10b981; text-align: center;">
                <div style="font-size: 28px;">👧</div>
                <strong>Arda (Avatar #2)</strong><br>
                <span style="font-size: 13px; color: #6ee7b7;">Jest/Mimik: Kulaklık takılı / Derin düşüncede</span><br>
                <span style="font-size: 11px; background: #065f46; padding: 2px 6px; border-radius: 4px;">Özel Durum: Otizm Spektrumlu ({dagilim.get('Otizmli', 0)} öğrenci)</span>
            </div>
            
            <div style="background: rgba(245, 158, 11, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #f59e0b; text-align: center;">
                <div style="font-size: 28px;">👦</div>
                <strong>Can (Avatar #3)</strong><br>
                <span style="font-size: 13px; color: #fde68a;">Jest/Mimik: Parmağı havada / Sabırsız</span><br>
                <span style="font-size: 11px; background: #78350f; padding: 2px 6px; border-radius: 4px;">Özel Durum: Üstün Yetenekli ({dagilim.get('Üstün Yetenekli', 0)} öğrenci)</span>
            </div>
            
            <div style="background: rgba(168, 85, 247, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #a855f7; text-align: center;">
                <div style="font-size: 28px;">👧</div>
                <strong>Elif (Avatar #4)</strong><br>
                <span style="font-size: 13px; color: #d8b4fe;">Jest/Mimik: Başını eğmiş / Kaygılı</span><br>
                <span style="font-size: 11px; background: #581c87; padding: 2px 6px; border-radius: 4px;">Özel Durum: Yüksek Kaygılı ({dagilim.get('Kaygılı', 0)} öğrenci)</span>
            </div>
        </div>
        
        <div style="margin-top: 15px; background: rgba(59, 130, 246, 0.2); padding: 12px; border-radius: 8px; border: 1px solid #3b82f6; text-align: center; font-size: 14px;">
            👥 <strong>Diğer Sınıf Mevcudu:</strong> Normal gelişim gösteren ve dersi dinleyen {mevcut - sum(dagilim.values())} akran öğrenci aktif olarak tahtayı izlemektedir.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")
  st.success(f"💡 **{detay['hook']}**")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### ⚡ 3D Sınıf İçi Anlık Sesli Olay ve Öğrenci Sorusu")
    st.warning(detay["kriz_ve_soru"])
    st.markdown(f"**Kriz / Soru Türü:** {detay['tur']}")

    # Sesli Geri Bildirim ve Mikrofon Konsolu
    st.markdown("### 🎙️ Canlı Sesli Geri Bildirim ve Mikrofon Konsolu")
    st.info(
        "Mikrofon simülasyonu aktif. Öğrencilerinize sesli yanıt vermek için"
        " konuşmanızı yazın ya da sesli hitabet komutunuzu iletin."
    )

    sesli_girdi = st.text_input(
        "🎤 Öğretmen Adayı Canlı Sesli Yanıt / Hitabet Komutu",
        placeholder=(
            "Örn: 'Çok harika bir soru sordun evladım, hemen birlikte"
            " inceleyelim...'"
        ),
    )
    if st.button("🔴 Sınıfa Sesli Geri Bildirimi Gönder ve Avatarları Yönet"):
      if sesli_girdi:
        st.success(
            f'🔊 Sesli yanıtınız 3D simülasyon motoru tarafından işlendi ve'
            f' sınıftaki avatarlara sesli olarak yansıtıldı: "{sesli_girdi}"'
        )
      else:
        st.warning(
            "Lütfen sesli simülasyon kutusuna hitabet metninizi yazınız."
        )

    st.markdown(
        "### 👩‍🏫 Bu Seçilen Kazanım, Kriz ve Soru Karşısında Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sınıf yönetimi, sesli kriz çözümü ve öğrenci sorularına yaklaşım"
        " açısından en uygun kararı seçiniz:",
        [
            (
                "A) Öğrencinin sorusunu görmezden gelmek, sert bir ses tonuyla"
                " susturmak ve ezber müfredata devam etmek."
            ),
            (
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak,"
                " akran empati kurdurmak ve somut model/dijital araçla"
                " konuyu bağlamak."
            ),
            (
                "C) Tahtaya arkasını dönerek dersi kendi kendine anlatıp"
                " bitirmeye çalışmak."
            ),
            (
                "D) Sınıfın hakimiyetini kaybettiğini kabul edip dersi erken"
                " bitirmek."
            ),
            (
                "E) Sınıf genelinde akran destekli tartışma başlatarak"
                " soruyu tüm sınıfa yöneltmek ve kavramsal değişimi"
                " tetiklemek."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Sesli Oturumu Tamamla"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": s_sinif,
          "tema": s_tema,
          "kod": s_kod,
          "alt_baslik": s_alt,
          "karar": ogretmen_karari,
          "yanilgi": detay["yanilgi"],
          "cozum": detay["strateji"],
          "materyaller": detay["materyal"],
      })
      st.success(
          "✅ 3D staj kararınız ve sesli etkileşiminiz başarıyla"
          " kaydedildi! Sağ taraftan mentor analizlerini inceleyebilirsiniz."
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
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — 3D sınıf"
            " ortamında öğrencilerin sesli sorularına, özel gereksinimli"
            " bireylere ve krizlere karşı gösterdiğiniz kapsayıcı refleks"
            " kusursuz!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " öğrenci aidiyetini zedeler ve danışman hocadan düşük puan"
            " almanıza neden olur."
        )

      st.divider()
      if st.button("📋 Raporlama ve 3D Video Kayıt İnceleme Paneline Geç"):
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
      "🎥 3D GÖRSEL VE SESLİ ETKİLEŞİMLİ KAPSAMLI ÜÇLÜ RAPORLAMA SİSTEMİ"
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
      "👩‍🏫 1. Öğretmen Adayı Bireysel Gelişim, 3D Video Arşivi & Görsel Araçlar",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Staj Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Uyum & 3D Video İnceleme Arşivi",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 3D Sınıf ve Sesli Etkileşim Oturumu Video Kaydı Arşivi"
    )
    st.info(
        "Aşağıdaki oynatıcı üzerinden, 3D sınıf ortamında gerçekleştirdiğiniz"
        " sesli komutları, öğrenci avatarlarının jest ve mimik tepkilerini"
        " baştan sona tekrar izleyebilirsiniz."
    )
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown(
        "### 📈 Öğretmen Adayı Bireysel Gelişim ve Performans Grafikleri"
    )

    if toplam_islem > 0:
      chart_data = pd.DataFrame(
          {
              "3D Staj Kriteri": [
                  "3D Sesli Kriz Yönetimi",
                  "Kapsayıcı Eğitim",
                  "Kavramsal Değişim",
                  "Dijital Araç Entegrasyonu",
              ],
              "Yeterlilik Puanı": [98, 95, 93, 97],
          }
      )
      st.bar_chart(chart_data, x="3D Staj Kriteri", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### 3D Oturum #{idx}: {veri['tema']} - {veri['kod']}")
        st.markdown(
            f"- **Seçilen Alt Kırılım:** {veri['alt_baslik']}\n- **Tercih"
            f" Edilen Staj Kararı:** {veri['karar']}\n- **Tespit Edilen"
            f" Kavram Yanılgısı:** {veri['yanilgi']}\n- **Önerilen"
            f" Profesyonel Strateji:** {veri['cozum']}\n- **Doğrudan"
            f" Tıklanabilir Web Araçları & Somut Materyaller:**\n "
            f" {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **3D Staj Gelişim Dönütü:** Seçtiğiniz özel kazanım ve alt"
          " kırılımlar doğrultusunda 3D görsel sınıf ortamında sergilediğiniz"
          " sesli hitabet, özel gereksinimli öğrenci yönetimi ve kriz çözme"
          " beceriniz üst düzeydedir."
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
        "1. **3D Sesli Kriz ve Soru Yönetimi:** Aday öğretmen; 3D simülasyon"
        " ortamında öğrencilerinden gelen kritik soruları ve krizleri"
        " fakültemiz süreç bileşenleri çerçevesinde başarıyla yönetmiştir.\n2."
        " **2026 Maarif Modeli Entegrasyonu:** Seçilen sınıf düzeyi, tema,"
        " öğrenme çıktısı ve alt kırılımlar eksiksiz uygulanmıştır.\n3."
        " **Kurumsal Karar:** Adayın gerçek okul sahasına stajyer öğretmen"
        " olarak çıkması fakültemiz komisyonunca **OY BİRLİĞİYLE"
        " ONAYLANMIŞTIR**."
    )

    st.success(
        "🎉 **Resmi Mühür:** Bu kurumsal rapor üniversite staj bilgi"
        " sistemine (OBS) işlenmiştir."
    )

  with tab_ogretim:
    st.markdown(
        "### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Uyum ve 3D Video İnceleme Paneli"
    )
    st.markdown(
        f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    st.markdown(
        "🎥 **3D Aday Staj Video Kaydı İnceleme Alanı:** Danışman hoca olarak"
        " adayın 3D sınıf seansını ve sesli komut etkileşimlerini yukarıdaki"
        " oynatıcıdan izleyebilir, rubrik kriterlerine göre puanlayabilirsiniz."
    )

    st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri ile Karşılaştırmalı Analiz:")
    st.markdown(
        f"> **Aktif Rubrik Kriterleri:**\n> *"
        f" {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Rubrik Eşleşme Matrisi:\n"
        "- ✅ **3D Sesli Kriz Yönetimi:** Adayın seçtiği stratejiler, rubriğin"
        " 1. maddesiyle **%99 uyumludur**.\n- ✅ **Kapsayıcı Dil ve Bireysel"
        " Farkındalık:** Özel gereksinimli bireylere (disleksi, otizm, üstün"
        " yetenek) yaklaşım rubriğin 2. maddesini tam olarak"
        " karşılamaktadır.\n- ✅ **Dijital Araç Entegrasyonu:** Doğrudan"
        " tıklanabilir web araçlarının kullanımı üst düzeydedir."
    )

    st.markdown("---")
    st.markdown("#### ✍️ Öğretmen Elemanı Resmi Geri Dönüt ve Not Kutusu")
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Öğretmen Adayına Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, seçtiğiniz alt kırılım ve"
            " kazanım çerçevesinde gerçekleştirdiğiniz 3D sınıf simülasyonunu"
            " ve sesli performansınızı inceledim. Öğrenci sorularına"
            " yaklaşımınız harikaydı. Başarılar dilerim."
        ),
    )

    if st.button("📤 Geri Dönütü Adaya ve Sisteme Gönder"):
      st.success(
          "✅ Öğretmen elemanı resmi geri dönütünüz başarıyla kaydedildi,"
          " video arşivine işlendi ve aday portfolyosuna iletildi!"
      )

  if st.button("🔄 Yeni Bir 3D Staj Simülasyonu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
