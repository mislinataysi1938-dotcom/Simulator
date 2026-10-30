import streamlit as st

st.set_page_config(
    page_title="Smart Pedagogy Class & Student Simulator v5.0",
    page_icon="🧠",
    layout="wide",
)

st.title("🎓 Akıllı Pedagoji Sınıf ve Öğrenci Profili Simülatörü v5.0")
st.markdown(
    "**Ortaokul Matematik Öğretmenliği | Profesyonel Pedagojik Karar ve Kavram"
    " Yanılgısı Arşivi**"
)

# ==========================================
# 1. KAPSAMLI SINIF VE KAVRAM YANILGISI VERİTABANI
# ==========================================
kapsamli_veritabani = {
    "5. Sınıf": {
        "Doğal Sayılar ve Basamak Değeri": {
            "ogrenci_ifadesi": (
                "Öğretmenim, '405.020' sayısını okurken sıfırları"
                " okumamamıza gerek yok, zaten değerleri yok ki, o yüzden"
                " '452' diye okusak da olur."
            ),
            "kavram_yanilgisi": (
                "Sıfırın basamak tutucu (placeholder) rolünü ve basamak"
                " değerine etkisini kavrayamama."
            ),
            "bilissel_kok": (
                "Doğal sayılarda etkisiz eleman mantığı ile basamak sistemini"
                " birbirine karıştırma."
            ),
            "pedagojik_cozum": (
                "Onluk taban blokları veya abaküs kullanarak her basamağın"
                " değerini somutlaştırmak; '0' rakamının o basamakta boşluk"
                " olmadığını, o birimden 0 tane bulunduğunu gösteren basamak"
                " tablosu çalışmaları yapmak."
            ),
        },
        "Kesirler ve Karşılaştırma": {
            "ogrenci_ifadesi": (
                "1/4 kesri 1/2 kesrinden kesinlikle daha büyüktür, çünkü 4"
                " sayısı 2'den büyüktür."
            ),
            "kavram_yanilgisi": (
                "Doğal sayı mantığını kesirlere aktararak paydadaki sayı"
                " büyüdükçe kesrin değerinin de büyüyeceğini zannetme."
            ),
            "bilissel_kok": (
                "Bütünün parçalandıkça parça boyutunun küçüldüğü gerçeğini"
                " ters yorumlama."
            ),
            "pedagojik_cozum": (
                "Özdeş iki pizzayı birine 2, diğerine 4 eş parça bölüp"
                " öğrencilere dilimleri fiziksel olarak göstererek"
                " karşılaştırma (kesir takımları) yaptırmak."
            ),
        },
        "Temel Geometrik Kavramlar": {
            "ogrenci_ifadesi": (
                "Çizdiğimiz bu ışının ucunda ok işareti var, demek ki bu"
                " çizgiyi cetvelle ölçebiliriz, sınırlıdır."
            ),
            "kavram_yanilgisi": (
                "Işın ve doğru parçası kavramlarının sınır özelliklerini"
                " karıştırma, geometrik çizimdeki görsel sembolleri eksik"
                " yorumlama."
            ),
            "bilissel_kok": (
                "Görsel olarak kağıt üzerinde biten her çizginin sonlu"
                " olduğunu düşünme."
            ),
            "pedagojik_cozum": (
                "El fenerinden çıkan ışığın ve uzaydaki yıldız ışığının"
                " bir yönde sonsuza kadar gittiği metaforunu kullanmak; ip ve"
                " lazer işaretçi modelleriyle sonsuzluk vurgusu yapmak."
            ),
        },
    },
    "6. Sınıf": {
        "Ondalık Gösterimler": {
            "ogrenci_ifadesi": (
                "0.45 sayısı 0.5'ten büyüktür, çünkü 45 sayısı 5'ten büyüktür."
            ),
            "kavram_yanilgisi": (
                "Ondalık kısmın basamak sayısını dikkate almayıp sadece"
                " sayısal değere bakarak karşılaştırma yapma."
            ),
            "bilissel_kok": (
                "Doğal sayı karşılaştırma kurallarını ondalık sayılara körü"
                " körüne uygulama."
            ),
            "pedagojik_cozum": (
                "Ondalık sayıların basamak sayısını eşitlemek için sağlarına"
                " sıfır ekleme stratejisini kullanmak (0.5 yerine 0.50 yazıp"
                " 0.45 ile karşılaştırmak) ve ondalık basamak tablosu"
                " kullanmak."
            ),
        },
        "Cebirsel İfadeler": {
            "ogrenci_ifadesi": (
                "Bir ifademiz var: '3x + 5'. Ben bunu toplarım ve '8x' veya"
                " '8' yazarım."
            ),
            "kavram_yanilgisi": (
                "Değişken içeren terimler ile sabit terimleri benzer terim"
                " zannederek toplama."
            ),
            "bilissel_kok": (
                "Cebirdeki harfleri nesne veya sayı yerine koyamama;"
                " aritmetik işlemleri cebire zorla uyarlama."
            ),
            "pedagojik_cozum": (
                "Cebir karoları (algebra tiles) kullanarak x'leri (uzun"
                " çubuklar) ve 1'leri (küçük kareler) modellemek; elinizde 3"
                " tane kutu ve 5 tane serbest taş varken bunları"
                " birleştiremeyeceğinizi somut olarak göstermek."
            ),
        },
        "Çarpanlar ve Katlar (Asal Sayılar)": {
            "ogrenci_ifadesi": (
                "1 sayısı asal sayıdır, çünkü sadece 1'e bölünür. Hem de"
                " tek başınadır."
            ),
            "kavram_yanilgisi": (
                "Asal sayı tanımını eksik ezberleme ('yalnızca 1'e ve kendine"
                " bölünen' tanımına 1'i dahil etme)."
            ),
            "bilissel_kok": (
                "1 sayısının özel konumunu ve iki farklı pozitif tam"
                " böleni olması gerektiği kuralını göz ardı etme."
            ),
            "pedagojik_cozum": (
                "Asal sayıların tam 2 farklı pozitif böleni olması gerektiğini"
                " alan modelleriyle (dikdörtgen oluşturma) açıklamak; 1"
                " sayısının sadece 1 tane böleni olduğunu kanıtlamak."
            ),
        },
    },
    "7. Sınıf": {
        "Oran ve Orantı (Ters Orantı)": {
            "ogrenci_ifadesi": (
                "Bir işi 2 işçi 6 günde bitiriyorsa, 4 işçi 12 günde bitirir"
                " tabii ki, işçi arttıkça gün de artar."
            ),
            "kavram_yanilgisi": (
                "Ters orantı gerektiren durumlarda her zaman doğru orantı"
                " şablonunu (içler dışlar çarpımı) uygulama."
            ),
            "bilissel_kok": (
                "Miktarların birlikte artması veya azalması genellemesini"
                " her probleme dayatma."
            ),
            "pedagojik_cozum": (
                "Mantıksal sorgulama yaptırmak: 'İşçi sayısı 2 katına çıkarsa"
                " işin bitiş süresi kısalmalı mı uzamalı mı?' sorusuyla"
                " bilişsel çelişki yaratmak ve tablo ile test etmek."
            ),
        },
        "Rasyonel Sayılar ve Sıralama": {
            "ogrenci_ifadesi": (
                "-3/4 sayısı -1/2 sayısından daha büyüktür, çünkü 3/4"
                " kesri 1/2'den büyüktür."
            ),
            "kavram_yanilgisi": (
                "Negatif sayılarda sıfıra uzaklık ile büyüklük/küçüklük"
                " ilişkisini ters yorumlama."
            ),
            "bilissel_kok": (
                "Pozitif rasyonel sayılardaki büyüklük algısını negatiflere"
                " aynen aktarma."
            ),
            "pedagojik_cozum": (
                "Sayı doğrusu üzerinde sıfırın soluna doğru gidildikçe"
                " değerin azaldığını borç/sıcaklık metaforları ve renkli oklar"
                " kullanarak görselleştirmek."
            ),
        },
        "Yüzdeler ve Baz Değişimi": {
            "ogrenci_ifadesi": (
                "Bir ürüne önce %20 indirim yapılıp sonra tekrar %20 zam"
                " yapılırsa ürün ilk fiyatına geri döner."
            ),
            "kavram_yanilgisi": (
                "Yüzde hesaplamalarının her zaman ilk ana fiyat üzerinden"
                " yapıldığını sanma (baz değişimini fark edememe)."
            ),
            "bilissel_kok": (
                "Yüzdelerin sabit bir mutlak miktar olduğunu düşünme."
            ),
            "pedagojik_cozum": (
                "100 TL'lik bir ürün üzerinden adım adım simülasyon yapmak:"
                " 100 TL -> %20 indirimle 80 TL -> 80 TL'nin %20'si 16 TL'dir,"
                " yeni fiyat 96 TL olur. İlk fiyata dönmediğini rakamlarla"
                " kanıtlamak."
            ),
        },
    },
    "8. Sınıf": {
        "Üslü İfadeler": {
            "ogrenci_ifadesi": "2 üssü 3, 2 ile 3'ün çarpımıdır yani 6'dır.",
            "kavram_yanilgisi": (
                "Taban ile üssü birbiriyle çarpma (tekrarlı çarpım mantığını"
                " kuramama)."
            ),
            "bilissel_kok": (
                "Üslü gösterimi toplama veya çarpma gibi standart aritmetik"
                " işlemlerle karıştırma."
            ),
            "pedagojik_cozum": (
                "Alan ve hacim modelleri kullanmak; üssün, tabanın kaç kez"
                " yan yana yazılıp çarpılacağını gösteren bir 'tekrar"
                " sayacı' olduğunu vurgulamak."
            ),
        },
        "Kareköklü İfadeler": {
            "ogrenci_ifadesi": (
                "Kök içinde (9 + 16) ifadesi kök 9 + kök 16 eşittir, yani"
                " 3 + 4 = 7'dir."
            ),
            "kavram_yanilgisi": (
                "Karekok alma işleminin toplama ve çıkarma işlemi üzerine"
                " dağılabileceğini varsayma."
            ),
            "bilissel_kok": (
                "Çarpma/bölmedeki dağılma özelliğini hatalı bir şekilde"
                " toplama üzerine uyarlama."
            ),
            "pedagojik_cozum": (
                "İçeriği önce toplatıp işlem yapma (kök 25 = 5) ile ayrı ayrı"
                " kök alıp toplama (3+4=7) sonuçlarının çeliştiğini gösterip"
                " matematiksel tutarsızlığı kanıtlamak."
            ),
        },
        "Cebirsel Özdeşlikler": {
            "ogrenci_ifadesi": "(a + b) in karesi açılımı a kare + b karedir.",
            "kareköklü_ifadeler_ek": (
                "Ortadaki 2ab terimini tamamen unutma ve üssü parantez içine"
                " dağıtma."
            ),
            "kavram_yanilgisi": (
                "Cebirsel ifadelerde parantez karesini toplama üzerine dağılma"
                " kuralı sanma."
            ),
            "bilissel_kok": (
                "Geometrik alan hesaplarındaki eksikliği cebire yansıtma."
            ),
            "pedagojik_cozum": (
                "Geometrik alan modeli (Kenarları a ve b olan bir karenin"
                " alanının, a^2, b^2 ve iki tane ab lik dikdörtgenin"
                " toplamından oluştuğunu görsel olarak) tahtada"
                " yapılandırmak."
            ),
        },
    },
}

# ==========================================
# 2. ÖZEL GEREKSİNİMLİ VE FARKLI ÖĞRENCİ PROFİLLERİ
# ==========================================
ogrenci_profilleri = {
    "Disleksili Öğrenci (Örn: Kerem)": {
        "ozellik": (
            "Rakamları ters algılama (örn. 6 ve 9, 12 ve 21), uzun metinli"
            " problemleri okumakta ve basamak sıralamasını takip etmekte"
            " zorlanır."
        ),
        "pedagojik_strateji": (
            "Yazı boyutu büyük, renk kontrastı yüksek materyaller"
            " kullanılmalı; uzun açıklamalar yerine işitsel destekler ve"
            " manipülatif dokunma araçları sağlanmalıdır."
        ),
    },
    "Matematik Kaygısı Yüksek Öğrenci (Örn: Elif)": {
        "ozellik": (
            "Tahtaya kalkmaktan çekinir, hata yapma korkusuyla işlemlere"
            " başlamakta tereddüt eder, ani panik yaşar."
        ),
        "pedagojik_strateji": (
            "Hata yapmanın öğrenme sürecinin en değerli parçası olduğu"
            " vurgulanmalı; küçük adımlarla başarı tattırılarak"
            " derecelendirilmiş olumlu pekiştireçler verilmelidir."
        ),
    },
    "Üstün Yetenekli / Farklı Düşünen Öğrenci (Örn: Can)": {
        "ozellik": (
            "Standart yöntemlerden hemen sıkılır, farklı ve kestirme yollar"
            " bulur ancak adımlarını açıklamaktan kaçınır."
        ),
        "pedagojik_strateji": (
            "Derinleştirilmiş (enrichment) zorlukta problemler verilmeli,"
            " 'Bunu başka hangi yolla ispatlardın?' sorularıyla üst düzey"
            " bilişsel becerileri tetiklenmelidir."
        ),
    },
    "Somut Dönem / Görsel Ağırlıklı Öğrenci (Örn: Deniz)": {
        "ozellik": (
            "Soyut semboller ve formüller havada kalır; problemi gözünde"
            " canlandıramadığı için hızla kopar."
        ),
        "pedagojik_strateji": (
            "Derse mutlaka GeoGebra dinamik yazılımları, günlük yaşam"
            " nesneleri veya somut sınıf içi modelleme etkinlikleriyle"
            " başlanmalıdır."
        ),
    },
}

# ==========================================
# 3. KULLANICI ARAYÜZÜ (SIDEBAR & MAIN)
# ==========================================
st.sidebar.header("⚙️ Simülasyon Ayarları")
ogretman_adi = st.sidebar.text_input(
    "Öğretmen Adayı Adı Soyadı", "Değerli Öğretmen Adayı"
)

secilen_sinif = st.sidebar.selectbox(
    "Sınıf Düzeyi Seçin", list(kapsamli_veritabani.keys())
)
secilen_konu = st.sidebar.selectbox(
    "Konu / Alt Kazanım Seçin", list(kapsamli_veritabani[secilen_sinif].keys())
)

st.sidebar.divider()
st.sidebar.header("👤 Sınıftaki Hedef Öğrenci Profili")
secilen_profil_adi = st.sidebar.selectbox(
    "Öğrenci Profili Seçin", list(ogrenci_profilleri.keys())
)

# Verileri çekme
konu_verisi = kapsamli_veritabani[secilen_sinif][secilen_konu]
profil_verisi = ogrenci_profilleri[secilen_profil_adi]

st.divider()

# İki sütunlu profesyonel arayüz tasarımı
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
  st.subheader(f"📖 Sınıf İçi Senaryo ({secilen_sinif} - {secilen_konu})")

  st.info(
      f"💬 **Öğrenci İfadesi / Davranışı:**\n\n"
      f'"{konu_verisi["ogrenci_ifadesi"]}"'
  )

  st.warning(
      f"🎯 **Seçilen Öğrenci Profili ({secilen_profil_adi}):**\n\n"
      f"{profil_verisi['ozellik']}"
  )

  st.markdown("### 👩‍🏫 Pedagojik Kararınız Ne Olurdu?")
  ogretmen_karari = st.radio(
      "Bu durum karşısında öğretmen olarak nasıl bir müdahalede"
      " bulunursunuz?",
      [
          (
              "A) Doğru kuralı veya formülü doğrudan tahtaya yazıp geçmek,"
              " öğrenciye ezberletmek."
          ),
          (
              "B) Öğrencinin bilişsel kökenini ve profil özelliklerini"
              " gözeterek çelişki yaratacak somut modeller ve rehberli"
              " sorular sunmak."
          ),
          (
              "C) Öğrencinin hatasını görmezden gelerek ders müfredatına hızla"
              " devam etmek."
          ),
      ],
  )

  if st.button("Kararı ve Pedagojik Etkinliği Değerlendir"):
    if "B)" in ogretmen_karari:
      st.success(
          "🌟 **Mükemmel Öğretmenlik Refleksi!** Yapılandırmacı yaklaşımı,"
          " öğrencinin bireysel profilini ve kavram yanılgısının kök"
          " nedenini harmanlayarak kusursuz bir bilişsel değişim süreci"
          " başlattınız."
      )
    else:
      st.error(
          "⚠️ **Geliştirilebilir:** Ezberci veya kaçıngan yaklaşımlar,"
          " öğrencinin kavram yanılgısını kalıcı hale getirebilir ve derse"
          " olan aidiyetini zedeleyebilir."
      )

with col2:
  st.subheader("💡 Uzman / Mentor Geri Bildirim ve Analiz Raporu")

  st.markdown("#### 🔍 Tespit Edilen Temel Kavram Yanılgısı")
  st.error(konu_verisi["kavram_yanilgisi"])

  st.markdown("#### 🧠 Yanılgının Bilişsel Kökü")
  st.warning(konu_verisi["bilissel_kok"])

  st.markdown("#### 🛠️ Önerilen Pedagojik Çözüm Stratejisi")
  st.success(konu_verisi["pedagojik_cozum"])

  st.markdown("#### 📌 Seçilen Profil İçin Özel Destek Tavsiyesi")
  st.info(profil_verisi["pedagojik_strateji"])

st.divider()
st.caption(
    f"Smart Pedagogy Class & Student Simulator v5.0 • Geliştiren:"
    f" {ogretman_adi} • Tüm Hakları Saklıdır ©️ 2026"
)
