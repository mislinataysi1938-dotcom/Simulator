import datetime
import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Custom Virtual Classroom & Institutional Simulator",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu (Session State) Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum & Sınıf Oluşturma, 2: Sanal Sınıf, 3: Raporlar

# ==========================================
# 1. 2026 MAARİF MODELİ (A, B, C ALT KAZANIM VE KAVRAM YANILGISI VERİTABANI)
# ==========================================
maarif_abc_veritabani = {
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
            "ogrenci_senaryosu": (
                "Seçtiğiniz öğrenci profilleri arasından biri (örneğin"
                " Disleksili Kerem), tahtaya kalkarak 405.020 sayısını 5.1.1.B"
                " alt kazanımı gereği okurken sıfırları atlar ve '452' olarak"
                " seslendirir. Sınıftaki diğer öğrenciler farklı tepkiler"
                " verir."
            ),
            "gercek_yanilgi": (
                "Sıfırın basamak tutucu (placeholder) rolünü kavramama; okunuş"
                " sırasını doğrudan rakamsal değere aktaramama."
            ),
            "bilissel_kok": (
                "Görsel simgeler ile sayısal soyut değerler arasındaki"
                " basamak basamak ilerleme kuralını kuramama."
            ),
            "cozum_stratejisi": (
                "Onluk taban blokları ve renkli basamak tabloları"
                " kullanılmalı; sıfırın o basamakta 'yokluk' değil, o birimden"
                " '0 tane' olduğunu gösteren basamak tutucu olduğu somut"
                " olarak hissettirilmelidir."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları, Manyetik"
                " Basamak Abaküsü\n💻 **Dijital / Web Araçları:** Base Ten Blocks"
                " (Math Learning Center), Baamboozle Basamak Oyunu"
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
            "ogrenci_senaryosu": (
                "Seçtiğiniz profillerden biri (örneğin Kaygılı Elif), 5.2.3.A"
                " kapsamında 1/4 kesrinin 1/2'den büyük olduğunu iddia eder"
                " ve payda büyüdükçe kesrin büyüdüğünü savunur."
            ),
            "gercek_yanilgi": (
                "Doğal sayı mantığını kesirlere transfer etme; paydadaki"
                " sayı büyüdükçe kesrin değerinin de büyüyeceğini sanma."
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
                " Dilimleme Seti\n💻 **Dijital / Web Araçları:** PhET Interactive"
                " Simulations (Fraction Matcher), GeoGebra Kesir Çarkları"
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
            "ogrenci_senaryosu": (
                "Seçtiğiniz profillerden biri (örneğin Sabırsız Can), 6.2.1.C"
                " kapsamında '3x + 5' ifadesini doğrudan '8x' veya '8'"
                " yaptığını söyler."
            ),
            "gercek_yanilgi": (
                "Değişken içeren terimler ile sabit terimleri benzer terim"
                " kabul ederek hatalı toplama yapma (cebirsel körlük)."
            ),
            "bilissel_kok": (
                "Cebirsel harfleri nesne veya değer yerine koyma aşamasında"
                " aritmetik toplama refleksini körü körüne uygulama."
            ),
            "cozum_stratejisi": (
                "Cebir karoları (uzun çubuklar ve birim kareler) kullanılarak"
                " x ile sayıların elma ile armut gibi farklı birimler"
                " olduğu somut olarak modelletilmelidir."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Manyetik Cebir Karoları (Algebra"
                " Tiles), Renkli Kutular ve Birim Küpler\n💻 **Dijital / Web"
                " Araçları:** National Library of Virtual Manipulatives"
                " (NLVM) Algebra Tiles, Desmos Cebir Karoları"
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
            "ogrenci_senaryosu": (
                "Seçtiğiniz profillerden biri (örneğin Kinestetik Deniz),"
                " 7.2.1.C kapsamında ters orantı probleminde işçi sayısı"
                " arttıkça gün sayısının da artacağını iddia eder."
            ),
            "gercek_yanilgi": (
                "Ters orantı gerektiren senaryolarda dahi her zaman doğru"
                " orantı şablonu kurmaya çalışma."
            ),
            "bilissel_kok": (
                "Niceliklerin her zaman birlikte artması veya azalması"
                " genellemesini hatalı bir şekilde tüm problemlere dayatma."
            ),
            "cozum_stratejisi": (
                "Mantıksal sorgulama yaptırılmalı: 'İşçi sayısı 2 katına"
                " çıkarsa işin bitiş süresi kısalmalı mı uzamalı mı?' sorusuyla"
                " bilişsel çelişki yaratılıp tablo ile test edilmelidir."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Oran Tahtası, Renkli Boncuklar ve İşçi"
                " Çizelge Tabloları\n💻 **Dijital / Web Araçları:** GeoGebra"
                " Orantı ve Oran Simülasyonları, PhET Proportional Reasoning"
            ),
        },
    },
    "8. Sınıf": {
        "Kareköklü İfadeler (8.1.2.)": {
            "alt_baslik_a": (
                "8.1.2.A. Tam Kare Sayılar ve Karekök: Alanı verilen karenin"
                " kenar uzunluğunu bulur ve kök sembolünü açıklar."
            ),
            "alt_baslik_b": (
                "8.1.2.B. Kareköklü Sayılarda Tahmin: Tam kare olmayan"
                " kareköklü sayıların hangi iki doğal sayı arasında"
                " olduğunu belirler."
            ),
            "alt_baslik_c": (
                "8.1.2.C. Kareköklü İfadelerde İşlemler: Çarpma, bölme ve"
                " toplama/çıkarma kurallarını uygular."
            ),
            "ogrenci_senaryosu": (
                "Sınıftaki öğrenciler 8.1.2.C kapsamında 'kök içinde (9 + 16)"
                " ifadesi kök 9 + kök 16 demektir' diyerek toplama üzerine"
                " dağılma hatası yapar."
            ),
            "gercek_yanilgi": (
                "Kareköklü ifadelerde toplama ve çıkarma işlemi üzerine kök"
                " alma işleminin dağılabileceğini varsayma."
            ),
            "bilissel_kok": (
                "Çarpma ve bölmedeki dağılma özelliğini hatalı bir biçimde"
                " toplama işlemine uyarlama."
            ),
            "cozum_stratejisi": (
                "İçeriği önce toplayıp işlem yapma (kök 25 = 5) ile ayrı"
                " ayrı kök alıp toplama (3+4=7) sonuçlarının çeliştiği"
                " sayısal örneklerle kanıtlanmalıdır."
            ),
            "materyal_ve_araclar": (
                "🧩 **Somut Materyal:** Kare Alan Ölçüm Izgaraları, Birim Kare"
                " Kartları\n💻 **Dijital / Web Araçları:** GeoGebra Dinamik Geometri"
                " Karekök Alan Modeli, Desmos Square Roots Explorer"
            ),
        },
    },
}

# ==========================================
# 2. ADIM 1: ÖZELLEŞTİRİLEBİLİR SINIF OLUŞTURMA VE KURUMSAL PANEL
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Özelleştirilebilir Sanal Sınıf ve Kurumsal Staj Kurulum Paneli (2026"
      " Maarif Modeli)"
  )
  st.info(
      "Bu ekranda kendi sanal sınıfınızın mevcudunu belirleyebilir, sınıfta"
      " yer almasını istediğiniz öğrenci türlerini dilediğiniz sayıda"
      " yapılandırabilirsiniz."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Mehmet Aksoy"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Gazi Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )
    uygulama_ogretim_elemani = st.selectbox(
        "Uygulama Öğretim Elemanı (Danışman / Hoca)",
        [
            "Prof. Dr. Ahmet Yılmaz (Matematik Eğitimi ABD)",
            "Doç. Dr. Fatma Demir (Özel Öğretim Yöntemleri)",
            "Dr. Öğr. Üyesi Mustafa Çelik (Eğitim Teknolojileri ve Staj Koordinatörü)",
            "Prof. Dr. Seda Kaya (Yapılandırmacı Öğretim ve Ölçme Değerlendirme)",
        ],
    )

  with col2:
    st.markdown("### 👥 Sanal Sınıf Mevcudu ve Öğrenci Profili Dağılımı")
    sinif_mevcudu = st.slider(
        "Sınıf Mevcudu (Toplam Öğrenci Sayısı)",
        min_value=10,
        max_value=35,
        value=24,
    )

    st.markdown("Sınıfta Bulunacak Özel Gereksinimli / Farklı Profil Oranları:")
    sayi_disleksi = st.number_input(
        "Disleksili / Özel Öğrenme Güçlüğü Olan Öğrenci Sayısı",
        min_value=0,
        max_value=10,
        value=2,
    )
    sayi_kaygili = st.number_input(
        "Matematik Kaygısı Yüksek Öğrenci Sayısı",
        min_value=0,
        max_value=10,
        value=4,
    )
    sayi_ustun = st.number_input(
        "Üstün Yetenekli / Sabırsız Öğrenci Sayısı",
        min_value=0,
        max_value=10,
        value=3,
    )
    sayi_kinestetik = st.number_input(
        "Somut / Kinestetik / Görsel Ağırlıklı Öğrenci Sayısı",
        min_value=0,
        max_value=15,
        value=5,
    )

  st.markdown("### 📋 Öğretim Elemanı Değerlendirme Kriterleri (Rubrik Seçimi)")
  krit_col1, krit_col2 = st.columns(2)
  with krit_col1:
    kriter_1 = st.checkbox(
        "Kapsayıcı Eğitim ve Bireysel Farklılıklara Duyarlılık", value=True
    )
    kriter_2 = st.checkbox(
        "Kavramsal Değişim ve Bilişsel Çelişki Oluşturma Becerisi", value=True
    )
    kriter_3 = st.checkbox(
        "Sınıf Yönetimi ve Pozitif Sınıf İklimi Oluşturma", value=True
    )
  with krit_col2:
    kriter_4 = st.checkbox(
        "2026 Maarif Modeli A-B-C Kazanım Başlıklarına Tam Uyum", value=True
    )
    kriter_5 = st.checkbox(
        "Somut Materyal ve Dijital Web Araçları Entegrasyonu", value=True
    )
    kriter_6 = st.checkbox(
        "Hata Analizi ve Biçimlendirici Geri Bildirim Verme", value=True
    )

  st.markdown("### 🏫 Sanal Sınıf Ortamı ve Etkileşim Tercihleri")
  sanal_3d_gorus = st.checkbox(
      "3D İzometrik Sınıf Ortamı Görünümünü Etkinleştir (Sıralar, Tahta ve"
      " Öğrenci Jest/Mimikleri)",
      value=True,
  )
  sesli_mikrofon = st.checkbox(
      "Sesli Komut ve Konuşma Tanıma Entegrasyonunu Aç (Mikrofon ile simüle"
      " edilmiş sesli yanıt)",
      value=True,
  )

  if st.button("🚀 Özelleştirilmiş Sanal Sınıf Oturumunu Başlat"):
    if not ogretmen_adi or not universite_adi:
      st.warning(
          "Lütfen öğretmen adı ve üniversite alanlarını eksiksiz doldurunuz."
      )
    else:
      st.session_state.ogretmen_adi = ogretmen_adi
      st.session_state.universite_adi = universite_adi
      st.session_state.fakulte_bolum = fakulte_bolum
      st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
      st.session_state.sinif_mevcudu = sinif_mevcudu
      st.session_state.profil_dagilimi = {
          "Disleksili": sayi_disleksi,
          "Kaygılı": sayi_kaygili,
          "Üstün Yetenekli": sayi_ustun,
          "Kinestetik": sayi_kinestetik,
      }
      st.session_state.secilen_kriterler = {
          "Kapsayıcı Eğitim": kriter_1,
          "Kavramsal Değişim": kriter_2,
          "Sınıf Yönetimi": kriter_3,
          "Maarif Modeli Uyumu": kriter_4,
          "Materyal Entegrasyonu": kriter_5,
          "Hata Analizi": kriter_6,
      }
      st.session_state.sanal_3d_gorus = sanal_3d_gorus
      st.session_state.sesli_mikrofon = sesli_mikrofon
      st.session_state.adim = 2
      st.rerun()

# ==========================================
# 3. ADIM 2: SANAL SINIF ORTAMI VE DETAYLI A-B-C KAZANIM SENARYOSU
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
      "Sınıf Düzeyi Seçin", list(maarif_abc_veritabani.keys())
  )
  konu_secenekleri = list(maarif_abc_veritabani[secilen_sinif].keys())

  st.markdown(
      f"### 🏫 Özel Sanal Sınıf Ortamı | {ogretmen} ({universite})"
  )
  st.caption(
      f"Sınıf Mevcudu: {mevcut} Öğrenci | Özel Profiller: Disleksili("
      f"{dagilim.get('Disleksili', 0)}), Kaygılı({dagilim.get('Kaygılı', 0)}),"
      f" Üstün({dagilim.get('Üstün Yetenekli', 0)}), Kinestetik("
      f"{dagilim.get('Kinestetik', 0)}) | Danışman: {ogretim_elemani}"
  )

  if st.session_state.get("sanal_3d_gorus", True):
    st.markdown(
        "> 🪑 **[3D İzometrik Sanal Sınıf Kuşbakışı Gözlem]**\n"
        "> *U şeklinde dizilmiş öğrenci masaları ve ön sırada konumlanan"
        " özel gereksinimli öğrenciler gözlenmektedir.*\n"
        "> *📌 Öğrenciler öğretmenin tahtadaki sunumunu takip etmekte,"
        " parmak kaldırma ve tedirginlik jest/mimikleri sergilemektedir.*"
    )

  secilen_konu = st.selectbox(
      "2026 Maarif Modeli Konu ve Kapsam Başlığı", konu_secenekleri
  )
  veri = maarif_abc_veritabani[secilen_sinif][secilen_konu]

  st.divider()

  # A, B, C Alt Kazanım Seçimi
  st.markdown("### 🎯 2026 Maarif Modeli A, B, C Alt Kazanım Detayları")
  secilen_abc = st.radio(
      "İşlemek istediğiniz spesifik alt kazanım bölümünü seçiniz:",
      [veri["alt_baslik_a"], veri["alt_baslik_b"], veri["alt_baslik_c"]],
  )

  st.info(f"**Seçilen Alt Kazanım Odak Metni:**\n\n{secilen_abc}")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### 💬 Sanal Sınıf İçi Anlık Öğrenci Tepkisi / Senaryo")
    st.warning(veri["ogrenci_senaryosu"])

    if st.session_state.get("sesli_mikrofon", True):
      st.markdown(
          "🎤 *[Sesli Mikrofon Modülü Aktif]*: Öğrenciye sesli yanıt vermek"
          " için konuşabilir ya da simülasyon kutusunu kullanabilirsiniz."
      )
      st.text_input(
          "Öğretmen Sesli Yanıt / Hitabet Simülasyonu",
          placeholder="Örn: 'Harika bir çaba, gelin bu adımı tahtada birlikte"
          " modelleyelim...'",
      )

    st.markdown("### 👩‍🏫 Bu Durumda Pedagojik Kararınız Ne Olurdu?")
    ogretmen_karari = st.radio(
        "Lütfen sınıf yönetimi ve kavramsal değişim açısından en uygun"
        " kararınızı seçiniz:",
        [
            (
                "A) Doğru kuralı hızlıca tahtaya yazıp geçmek, öğrenciye"
                " ezberletmek ve dersin akışını bozmamak."
            ),
            (
                "B) Öğrencinin bireysel profilini ve kavram yanılgısının"
                " kökenini hesaba katarak çelişki yaratacak somut modeller"
                " ve rehberli sorular sunmak."
            ),
            (
                "C) Öğrencinin verdiği yanıtı tamamen görmezden gelip"
                " müfredat planına sadık kalmak."
            ),
            (
                "D) Öğrenciyi tahtadan hemen indirip yerine oturtmak ve"
                " konuyu bilen başka bir öğrenciye söz hakkı vermek."
            ),
            (
                "E) Sınıf genelinde akran tartışması (peer-discussion)"
                " başlatarak öğrencilerin birbirlerinin fikirlerini"
                " sorgulamasını sağlamak."
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
          "yanilgi": veri["gercek_yanilgi"],
          "bilissel_kok": veri["bilissel_kok"],
          "cozum": veri["cozum_stratejisi"],
          "materyaller": veri["materyal_ve_araclar"],
      })
      st.success(
          "✅ Kararınız sisteme kaydedildi! Sağ taraftan uzman analizlerini"
          " ve materyal önerilerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown("#### 💡 Uzman / Mentor Geri Bildirim ve Materyal Paneli")

    # KRİTİK KURAL: Uzman analizleri ve somut materyal önerileri yalnızca karar verildikten sonra açılır!
    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Tespit Edilen Temel Kavram Yanılgısı")
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
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — A-B-C"
            " kazanımlarına ve yapılandırmacı yaklaşıma tam uygun refleks!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " kavram yanılgısını kalıcılaştırabilir."
        )

      st.divider()
      if st.button(
          "📋 Simülasyonu Tamamla ve Çift Yönlü Rapor Paneline Git"
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
# 4. ADIM 3: ÇİFT YÖNLÜ NİHAİ RAPOR (ÖĞRENCİ VE FAKÜLTE RAPORU)
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "📋 ÇİFT YÖNLÜ PEDAGOJİK DEĞERLENDİRME VE KURUMSAL STAJ RAPORU"
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

  tab1, tab2 = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Bireysel Gelişim ve Dönüt Raporu",
      "🏛️ 2. Eğitim Fakültesi Kurumsal Staj ve Bölüm Değerlendirme Raporu",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab1:
    st.markdown(
        "### 📈 Öğretmen Adayı Oturum Deneyimi ve Materyal Kullanım Rehberi"
    )
    if toplam_islem > 0:
      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### Oturum #{idx}: {veri['konu']}")
        st.markdown(f"- **Odak A-B-C Kazanım Bölümü:** {veri['abc_kazanim']}")
        st.markdown(f"- **Tercih Edilen Pedagojik Karar:** {veri['karar']}")
        st.markdown(f"- **Hedeflenen Kavram Yanılgısı:** {veri['yanilgi']}")
        st.markdown(f"- **Bilişsel Kök Analizi:** {veri['bilissel_kok']}")
        st.markdown(f"- **Önerilen Profesyonel Strateji:** {veri['cozum']}")
        st.markdown(
            f"- **Kullanılması Önerilen Somut/Dijital Araçlar:**\n"
            f"  {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **Öğretmen Adayına Özel Gelişim Dönütü:** Sınıf mevcudunu ve"
          " farklı öğrenci profillerini dikkate alarak yaptığınız seçimler,"
          " somut materyal ve dijital araç entegrasyonu konularında güçlü"
          " bir staj altyapısına sahip olduğunuzu göstermektedir."
      )
    else:
      st.warning("Henüz kaydedilmiş bir simülasyon oturumu bulunmuyor.")

  with tab2:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Bölümsel Staj ve Kurumsal İzleme Raporu"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi İlköğretim"
        " Matematik Öğretmenliği Bölüm Başkanlığı ve Staj Komisyonu*"
        " tarafindan onaylanmıştır."
    )

    secilen_kriterler = st.session_state.get("secilen_kriterler", {})
    st.markdown(
        "#### Seçilen Kurumsal Kriterler Kapsamında Aday Yetkinlik Puanları:"
    )

    for kriter, aktif in secilen_kriterler.items():
      if aktif:
        st.markdown(f"- ✅ **{kriter}:** 96 / 100 (Üst Düzey Yeterli)")

    st.markdown("---")
    st.markdown(
        "#### 🔍 Fakülte/Bölüm Özelinde Genel Değerlendirme ve Gelişim"
        " Önerileri"
    )
    st.markdown(
        "1. **Bölümsel Yeterlilik Analizi:** Aday, 2026 Türkiye Yüzyılı Maarif"
        " Modeli A, B, C kazanım kırılımlarına tam hakimiyet göstermiş,"
        " özelleştirilmiş sınıf mevcudu simülasyonunda kapsayıcı eğitim"
        " standartlarını sağlamıştır.\n2. **Geliştirilmesi Gereken Yönler"
        " (Eksiklikler):** Gerçek saha stajında, heterojen sınıf"
        " yapılarındaki zaman yönetimi ve grup içi akran değerlendirme"
        " ölçeklerinin çeşitlendirilmesi konusunda ek danışmanlık"
        " alması önerilir.\n3. **Kurumsal Staj Sonuç Kararı:** Adayın"
        " simülasyon performans raporu fakülte portfolyosuna işlenmiş olup"
        " staj okulu sahasına çıkışı **ONAYLANMIŞTIR**."
    )

    st.success(
        "🎉 **Kurumsal Mühür:** Bu rapor ilgili Eğitim Fakültesi"
        " departmanına resmi olarak sunulmuştur."
    )

  if st.button("🔄 Yeni Bir Simülasyon Oturumu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
