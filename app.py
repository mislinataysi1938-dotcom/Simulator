import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="2024 TYMM - Dinamik Şıklı 3D Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
    <style>
    .sade-kart {
        background-color: #F8FAFC; border: 1px solid #CBD5E1;
        border-left: 4px solid #1D4ED8; border-radius: 8px;
        padding: 18px 22px; margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .baslik-mavi { color: #1E3A8A; font-weight: 700; font-size: 1.15rem; margin-bottom: 10px; border-bottom: 1px solid #E2E8F0; padding-bottom: 5px; }
    .rozet {
        display: inline-block; background-color: #EFF6FF; color: #1D4ED8;
        border: 1px solid #BFDBFE; padding: 4px 12px; border-radius: 12px;
        font-size: 0.9rem; font-weight: 600; margin-bottom: 8px;
    }
    .transkript-kutu {
        background-color: #FFFFFF; border: 1px solid #94A3B8; border-radius: 8px;
        padding: 20px; line-height: 1.7; font-size: 0.95rem;
    }
    .anlik-bildirim {
        background-color: #FFFBEB; border-left: 4px solid #F59E0B; padding: 15px; 
        margin-top: 10px; margin-bottom: 15px; border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu Yönetimi (Anti-Ezber ve Kademeli Kilitleme)
if "simulasyon_gecmisi" not in st.session_state: st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state: st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state: st.session_state.secili_ogrenciler = []
if "otur_seed" not in st.session_state: st.session_state.otur_seed = random.randint(1, 1000)

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ (KAPSAYICI EĞİTİM)
# ==========================================
ogrenci_profilleri = {
    "Kerem": {"durum": "Disleksi", "ikon": "👦", "mimik": "Basamaklara odaklanıyor", "ozellik": "Rakamları, basamakları ve sembolleri ters algılayabilir; görsel-dokunsal gruplamaya ihtiyaç duyar."},
    "Arda": {"durum": "Otizm Spektrumu", "ikon": "👦", "mimik": "Kulaklık takılı, sallanıyor", "ozellik": "Ani seslere ve belirsiz yönergelere hassastır; net, öngörülebilir adımlar ister."},
    "Can": {"durum": "Üstün Yetenekli", "ikon": "👦", "mimik": "Sabırsızca parmak kaldırıyor", "ozellik": "Ezberden sıkılır; kavramın nedenini, genellemesini ve farklı durumlarını sorgular."},
    "Elif": {"durum": "Yüksek Kaygılı", "ikon": "👧", "mimik": "Başını öne eğmiş, gergin", "ozellik": "Hata yapmaktan çekinir; baskı hissederse donup kalabilir, destekleyici dil ister."},
    "Zeynep": {"durum": "DEHB", "ikon": "👧", "mimik": "Sürekli etrafa bakınıyor", "ozellik": "Dikkati çabuk dağılır; kısa, odaklanmış ve aktif katılımlı adımlarda kalır."},
    "Mehmet": {"durum": "İşitme Yetersizliği", "ikon": "👦", "mimik": "Konuşanın yüzüne odaklanmış", "ozellik": "Görsel ipuçlarına, açık yüz ifadesine ve yazılı/görsel pekiştireçlere ihtiyaç duyar."},
    "Ayşe": {"durum": "Az Gören", "ikon": "👧", "mimik": "Gözlerini kısarak inceliyor", "ozellik": "Küçük görsellerde zorlanır; net kontrastlı, dokunsal ve açık sözel betimleme bekler."},
    "Ali": {"durum": "Diskalkuli", "ikon": "👦", "mimik": "Parmaklarıyla saymaya çalışıyor", "ozellik": "Sayıların büyüklük ilişkisini zihinde kurmakta zorlanır; somut model ister."},
    "Merve": {"durum": "Bedensel Yetersizlik", "ikon": "👧", "mimik": "Elleri sırasında, izliyor", "ozellik": "Bilişsel sorunu yoktur ancak yoğun yazma/çizim gerektiren adımlarda erişilebilir destek ister."},
    "Burak": {"durum": "Düşük Motivasyon", "ikon": "👦", "mimik": "Kolları bağlı, ilgisiz", "ozellik": "Soyut kurallara mesafelidir; gerçek yaşamla anlamlı bağ kurulduğunda katılım gösterir."}
}

MATERYAL_SECENEKLER = [
    "Seçiniz...", 
    "Kendi Geliştirdiğim / Tasarladığım Materyal",
    "Somut Materyal (Onluk Taban Blokları, Kesir Takımı, Birim Küpler vb.)",
    "Dinamik Matematik Yazılımı (GeoGebra / Desmos)", 
    "Yüksek Kontrastlı Görsel & Dokunsal Kartlar",
    "Günlük Yaşam Nesneleri ve Ölçüm Araçları", 
    "Geometrik Şekil / Açınım ve Simetri Modelleri",
    "Koordinat / Grafik / Tablo Çalışma Panosu", 
    "Olasılık ve Veri Deneyi Araçları (Zar, Çark, Anket)",
    "Klasik Çalışma Kâğıdı / Formül ve Kural Özeti"
]

# ==========================================
# 2. DİNAMİK YAPAY ZEKA ŞIK ÜRETİCİSİ (BAĞLAMA ÖZEL)
# ==========================================
def dinamik_eylem_secenekleri_uret(tema, kazanim_kod, surec, kriz):
    """Kazanım, süreç bileşeni ve kriz bağlamına göre her oturumda benzersiz şıklar üretir."""
    tema_kisa = tema.split(":", 1)[1].strip() if ":" in tema else tema
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    kriz_kisa = (kriz[:60] + '...') if len(kriz) > 60 else kriz

    e1_secenekler = [
        "Seçiniz...",
        f"Öğrencinin '{kriz_kisa}' nedeniyle yaşadığı zorlanmayı kabul ederek ona güvenli bir alan sunmak",
        f"Sıranın başına gidip '{surec_kisa}' adımında neyi kaçırdığını kısa ve sakin ifadelerle sormak",
        f"Sınıfın '{tema_kisa}' akışını bozmadan öğrenciye bireysel toparlanma süresi tanımak",
        f"Dikkati dağılan öğrenciye '{kazanim_kod}' hedefini hatırlatıp onu disiplinli bir şekilde odaklanmaya davet etmek",
        f"Öğrenciyi zorlamadan '{surec_kisa}' basamağını kendi hızında incelemesini istemek",
        f"Yaşanan '{kriz_kisa}' durumunu not alıp '{kazanim_kod}' anlatımında mevcut basamakta doğrudan ilerlemek"
    ]

    e2_secenekler = [
        "Seçiniz...",
        f"Seçilen materyal üzerinden yönlendirici sorularla '{surec_kisa}' ilişkisini öğrencinin keşfetmesini sağlamak",
        f"'{tema_kisa}' kavramını günlük yaşam örneğiyle eşleştirip öğrenciden kendi ifadesiyle açıklamasını istemek",
        f"Adımları parçalara ayırarak farklı bir temsil üzerinden '{kazanim_kod}' hedefini yeniden denetmek",
        f"Öğrenciyle birlikte ilk örneği kurup benzer durumu karşılaştırarak '{surec_kisa}' için genelleme aramak",
        f"Kuralın mantığını doğrudan tahtaya yazıp akran etkileşimiyle '{kazanim_kod}' adımını hemen ezberlemesini istemek",
        f"Zorlanılan '{surec_kisa}' basamağını atlayarak bir sonraki alt probleme geçmek"
    ]
    return e1_secenekler, e2_secenekler

# ==========================================
# 3. RUBRİK TABANLI ANLIK YAZILIMSAL DEĞERLENDİRME & AI DAVRANIŞ MOTORU
# ==========================================
def eylem_uygunlugu_degerlendir(eylem_1, eylem_2, ogr_durum):
    # Dinamik şıklar içindeki anahtar kelimeleri arayarak pedagojik işlevi tespit eder
    d1 = any(kw in eylem_1 for kw in ["zorlanmayı kabul ederek", "neyi kaçırdığını", "bireysel toparlanma", "kendi hızında"])
    d2 = any(kw in eylem_2 for kw in ["keşfetmesini sağlamak", "kendi ifadesiyle", "yeniden denetmek", "genelleme aramak"])
    
    # Profile özel istisnai esneklikler
    if ogr_durum == "Otizm Spektrumu" and "kendi hızında" in eylem_1: d1 = True
    if ogr_durum == "Üstün Yetenekli" and ("keşfetmesini sağlamak" in eylem_2 or "genelleme aramak" in eylem_2): d2 = True
    if ogr_durum == "Düşük Motivasyon" and "kendi ifadesiyle" in eylem_2: d2 = True
    
    return d1, d2

def ai_rubrik_degerlendirmesi(eylem1, eylem2, materyal, d1, d2, ogr_durumlar):
    puan = 100
    mesaj = f"**🤖 ANLIK SİSTEM DEĞERLENDİRMESİ (2024 TYMM Rubrik Analizi):**\n\n"
    
    if not d1:
        puan -= random.choice([25, 30, 20])
        mesaj += f"❌ **İletişim ve Empati (30 Puan):** Seçtiğiniz 1. eylem, {ogr_durumlar[0]} profiline duyarlı iletişim beklentisini karşılamıyor. Otoriter/pasif kalmak yerine önce duyuşsal regülasyon (güven) sağlanmalıdır.\n\n"
    else:
        mesaj += f"✅ **İletişim ve Empati (30 Puan):** 1. adımda seçtiğiniz duyuşsal yaklaşım, kapsayıcı iletişim beklentisiyle uyumlu.\n\n"
        
    if not d2:
        puan -= random.choice([25, 30, 20])
        mesaj += f"❌ **2024 TYMM Süreç Uyumu (30 Puan):** Seçtiğiniz 2. adım, yapılandırmacı keşif ilkesiyle çelişiyor. Öğrenciye formülü doğrudan veren veya adımı atlayan yollar yerine materyal destekli keşif aranmalıdır.\n\n"
    else:
        mesaj += f"✅ **2024 TYMM Süreç Uyumu (30 Puan):** 2. adımdaki keşif odaklı eyleminiz Maarif Modeli'ne ve rubrik hedeflerine tam uygun.\n\n"
        
    if materyal == "Klasik Çalışma Kâğıdı / Formül ve Kural Özeti":
        puan -= 20
        mesaj += f"⚠️ **Materyal Kriteri (40 Puan):** Klasik kural özeti, {ogr_durumlar[0]} gibi özel gereksinimli öğrencilerin krizlerini çözmekte yetersiz kalır."
    else:
        mesaj += f"✅ **Materyal Kriteri (40 Puan):** Seçilen/Geliştirilen materyal, yapılandırmacı süreci desteklemek açısından isabetlidir."
        
    return puan, mesaj

def ai_profil_davranisi_uret(ogrenci_adi, sinif, tema, kazanim_kod, kazanim_cikti, surec, temel_kriz, aday_sozu="", eylem_1="", eylem_2="", materyal_etiketi="", materyal_aciklama=""):
    profil = ogrenci_profilleri[ogrenci_adi]
    durum = profil["durum"]
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    mudahale_var = bool(aday_sozu.strip() or eylem_1 or materyal_etiketi)
    d1, d2 = eylem_uygunlugu_degerlendir(eylem_1, eylem_2, durum)

    if not mudahale_var:
        return f"*{ogrenci_adi} ({durum}):* `{kazanim_kod}` ({surec_kisa}) adımında '{temel_kriz}' zorluğunu yaşar ve profiline ({profil['ozellik']}) uygun bir destek arar."

    soz_ozet = aday_sozu.strip()[:65]
    if not (d1 and d2):
        return f"*{ogrenci_adi} ({durum}):* Öğretmenin \"{soz_ozet}...\" sözüne rağmen, '{surec_kisa}' basamağında seçilen yaklaşım profiline tam uymadığı için '{materyal_etiketi}' ile ilerlemekte güçlük çeker."

    return f"*{ogrenci_adi} ({durum}):* Öğretmenin \"{soz_ozet}...\" yaklaşımıyla sakinleşir ve '{materyal_etiketi}' desteği sayesinde `{kazanim_kod}` ilişkisini kendi kendine keşfetmeye başlar."
    # ==========================================
# 4. 2024 TYMM ORTAOKUL MATEMATİK TAM MÜFREDAT ARŞİVİ
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler", 
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler", 
            "3. Tema: Geometrik Nicelikler", 
            "4. Tema: İstatistiksel Araştırma Süreci", 
            "5. Tema: Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {"kod": "MAT.5.1.1", "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme", "surec": ["a) Çok basamaklı sayılar hakkında bilgi toplar.", "b) Ortak özellikleri belirler.", "c) Farklılıkları belirler.", "ç) Örüntüler üzerinden önermelerde bulunur."], "hook": "Kütüphane arşiv kodlama sistemi.", "kriz": "Sıfır içeren bölükleri okurken basamakları karıştırır."},
                {"kod": "MAT.5.1.2", "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini stratejiler geliştirerek yapabilme", "surec": ["a) İşlem gerektiren durumları inceler.", "b) Zihinden işlem stratejileri geliştirir.", "c) Stratejilerin doğruluğunu test eder."], "hook": "Market kasasında para üstü hesaplama.", "kriz": "Zihinden işlem yaparken adımları karıştırır."},
                {"kod": "MAT.5.1.3", "cikti": "Doğal sayılarla çarpma ve bölme işlemlerini stratejiler geliştirerek yapabilme", "surec": ["a) Çarpma/bölme gerektiren durumları inceler.", "b) Zihinden işlem stratejileri geliştirir.", "c) Çözümün mantıklılığını değerlendirir."], "hook": "Toptan ürün alımında maliyet hesaplama.", "kriz": "Bölme işleminde kalanlı durumlarda ne yapacağını bilemez."},
                {"kod": "MAT.5.1.4", "cikti": "Kesirlerin farklı gösterimlerini ve sayı doğrusundaki yerlerini ilişkilendirebilme", "surec": ["a) Basit, bileşik ve tam sayılı kesirleri inceler.", "b) Denk kesirleri modeller ve karşılaştırır."], "hook": "Mutfak ölçülerinde bardak eşleştirmeleri.", "kriz": "Payda büyüdükçe kesrin küçüldüğünü görselleştiremez."},
                {"kod": "MAT.5.1.5", "cikti": "Kesirlerle toplama ve çıkarma işlemlerini yapabilme", "surec": ["a) Paydaları eşit/farklı kesirlerde işlemi modeller.", "b) İşlem stratejisi geliştirir ve çözer."], "hook": "Kalan pasta dilimlerinin toplanması.", "kriz": "Paydaları eşitlemeden doğrudan payları ve paydaları toplar."},
                {"kod": "MAT.5.1.6", "cikti": "Ondalık gösterimleri çözümleme ve sayı doğrusunda ilişkilendirebilme", "surec": ["a) Basamak değerlerini belirler.", "b) Sayı doğrusunda konumlandırır ve sıralar."], "hook": "Para birimlerindeki kuruş gösterimleri.", "kriz": "Virgülden sonraki basamak sayısına bakarak büyüklük yanılgısına düşer."},
                {"kod": "MAT.5.1.7", "cikti": "Kesir, ondalık ve yüzde gösterimleri arasındaki ilişkileri yorumlayabilme", "surec": ["a) Yüzlük kart ve modeller üzerinden eşleştirir.", "b) Farklı gösterimler arasında dönüşüm yapar."], "hook": "Cihaz batarya doluluk yüzdesi.", "kriz": "Kesri yüzdeye çevirirken paydayı 100 yapmayı unutur."}
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {"kod": "MAT.5.2.1", "cikti": "Temel geometrik çizimler (nokta, doğru, ışın) için araç ve teknolojiden yararlanabilme", "surec": ["a) Uygun araçlarla çizer.", "b) Özelliklerini ve ilişkilerini açıklar."], "hook": "Mahalle krokisindeki sokaklar.", "kriz": "Doğru ile doğru parçası arasındaki uç nokta farkını karıştırır."},
                {"kod": "MAT.5.2.2", "cikti": "İki noktanın birbirine göre konumunu yön ve birim kullanarak ifade edebilme", "surec": ["a) Referans noktası belirler.", "b) Yön ve birim ile konumu tanımlar."], "hook": "Satranç tahtasında veya haritada hareket.", "kriz": "Sağ-sol ve yukarı-aşağı yönergelerini ters uygular."},
                {"kod": "MAT.5.2.3", "cikti": "Çokgenlerin ve üçgenlerin temel elemanlarını ve açı özelliklerini çözümleyebilme", "surec": ["a) Çokgenleri özelliklerine göre sınıflandırır.", "b) Üçgenleri açılarına/kenarlarına göre inceler."], "hook": "Mimari yapılardaki çokgen formlar.", "kriz": "Geniş açılı üçgeni dar açılı üçgenden ayırt edemez."}
            ],
            "3. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.5.3.1", "cikti": "Zaman ölçme birimleri (saat, dakika, saniye) arasındaki ilişkileri yorumlayabilme", "surec": ["a) Birimler arası dönüşüm yapar.", "b) Geçen süreyi hesaplar ve problem çözer."], "hook": "Otobüs veya uçak seyahat sürelerinin hesabı.", "kriz": "Zamanı toplarken 60 tabanı yerine 100 tabanına göre onluk elde eder."},
                {"kod": "MAT.5.3.2", "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkileri yorumlayabilme", "surec": ["a) Birim karelerle alan/çevre hesaplar.", "b) Çevreleri eşit dikdörtgenlerin alanlarını karşılaştırır."], "hook": "Eşit çit teliyle oluşturulan farklı bahçeler.", "kriz": "Çevre ve alan hesaplama yöntemlerini birbirine karıştırır."}
            ],
            "4. Tema: İstatistiksel Araştırma Süreci": [
                {"kod": "MAT.5.4.1", "cikti": "Kategorik veriyle çalışabilme ve veriye dayalı karar verebilme", "surec": ["a) Araştırma sorusu oluşturur ve veri toplar.", "b) Sıklık tablosu ve sütun grafiğiyle veriyi görselleştirir.", "c) Veriyi analiz edip yorumlar."], "hook": "Sınıfın en sevdiği spor dalları araştırması.", "kriz": "Sütun grafiğinde eksenleri isimlendirmeyi veya eşit ölçeklendirmeyi unutur."}
            ],
            "5. Tema: Veriden Olasılığa": [
                {"kod": "MAT.5.5.1", "cikti": "Herhangi bir olayın olasılığının 0 ile 1 arasında olduğunu yorumlayabilme", "surec": ["a) İmkânsız, olası ve kesin olayları inceler.", "b) Olayların ihtimalini 0-1 aralığına yerleştirir."], "hook": "Hava durumu raporlarındaki yağmur ihtimali.", "kriz": "Olasılığı 1'den büyük bir tam sayı olarak bulmaya çalışır."}
            ]
        }
    },
    "6. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: İşlemlerle Cebirsel Düşünme",
            "3. Tema: Geometrik Şekiller",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: İstatistiksel Araştırma Süreci",
            "6. Tema: Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {"kod": "MAT.6.1.1", "cikti": "Doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Modellerle gösterir."], "hook": "Farklı otobüs hatlarının aynı anda duraktan kalkış saatleri.", "kriz": "Çarpan ile kat kavramlarını tersine çevirerek algılar."},
                {"kod": "MAT.6.1.2", "cikti": "2, 3, 4, 5, 6, 9 ve 10 ile bölünebilme kriterlerine çıkarım yapabilme", "surec": ["a) Basamak yapısından varsayımlar kurar.", "b) Genellemeleri örneklerle sınar."], "hook": "Öğrencileri veya nesneleri artansız gruplara ayırma.", "kriz": "Rakamları toplamı kuralı ile son basamak kuralını birbirine uygular."},
                {"kod": "MAT.6.1.3", "cikti": "Doğal sayının asal olma durumunu ve asal çarpanlarını çözümleyebilme", "surec": ["a) Asal ve bileşik sayıları ayırt eder.", "b) Sayıyı asal çarpanlarına ayırır."], "hook": "Sayısal şifreleme ve asal çarpan algoritmaları.", "kriz": "Çift sayıların (2 hariç) asal olamayacağını unutur veya 1'i asal sayar."},
                {"kod": "MAT.6.1.4", "cikti": "İki doğal sayının ortak bölenleri ile ortak katlarını yorumlayabilme", "surec": ["a) Ortak bölen/katları belirler.", "b) Çizim/tablo üzerinde karşılaştırır."], "hook": "Farklı uzunluktaki kumaşları eşit parçalara ayırma.", "kriz": "EBOB ile EKOK'u nerede kullanacağını karıştırır."},
                {"kod": "MAT.6.1.5", "cikti": "Kümelerle ilgili temel kavramları çözümleyebilme", "surec": ["a) Küme elemanlarını belirler.", "b) Kesişim ve birleşim ilişkilerini oluşturur."], "hook": "İki farklı kursa giden öğrencilerin listesi.", "kriz": "Kesişim ve birleşim sembollerini karıştırır."},
                {"kod": "MAT.6.1.6", "cikti": "Tam sayıları ve sayı doğrusunda sıralanışını yorumlayabilme", "surec": ["a) Yönlü sayıları gerçek yaşamla ilişkilendirir.", "b) Sayı doğrusunda sıralar ve mutlak değeri yorumlar."], "hook": "Asansör katları ve hava sıcaklığı.", "kriz": "Negatif sayıların sıfırdan uzaklaştıkça küçüldüğünü anlayamaz."},
                {"kod": "MAT.6.1.7", "cikti": "Kesirler ve ondalık gösterimlerle dört işlem gerektiren problemleri çözebilme", "surec": ["a) İşlem bileşenlerini belirler.", "b) Uygun temsil ile problemi çözer.", "c) Çözümü değerlendirir."], "hook": "Market alışverişi ve indirim oranları.", "kriz": "Kesirlerde bölme işlemi yaparken ikinci kesri ters çevirmeyi unutur."}
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme": [
                {"kod": "MAT.6.2.1", "cikti": "Nicelikleri cebirsel ifadelerle modelleyebilme", "surec": ["a) Sabit ve değişkeni belirler.", "b) İlişkiyi tablo/cebirsel temsil eder."], "hook": "Kumbaraya eklenen sabit miktar.", "kriz": "Harfin değişken olduğunu anlamakta zorlanır."},
                {"kod": "MAT.6.2.2", "cikti": "Sayı ve şekil örüntülerinin kuralını cebirsel olarak ifade edebilme", "surec": ["a) Adımlar arası değişimi inceler.", "b) Örüntünün genel kuralını bulur."], "hook": "Kibrit çöpleriyle oluşturulan geometrik desenler.", "kriz": "Değişim miktarını bulur ancak kuraldaki sabit terimi (başlangıç) hatalı kurar."}
            ],
            "3. Tema: Geometrik Şekiller": [
                {"kod": "MAT.6.3.1", "cikti": "Açı çeşitlerini ve iki paralel doğru ile bir kesenin oluşturduğu açıları sınıflandırabilme", "surec": ["a) Komşu, tümler, bütünler açıları inceler.", "b) Paralel doğru/kesen ile yöndeş, iç/dış ters açıları sınıflandırır."], "hook": "Tren rayları, makaslar ve köprü tasarımlarındaki açılar.", "kriz": "Kesen doğru eğik olduğunda Z, U, yöndeş açıları göremez."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.6.4.1", "cikti": "Üçgen ve paralelkenarın alan bağıntılarına yansıtma yapabilme", "surec": ["a) Dikdörtgen alan bağıntısından yola çıkar.", "b) Parçalama-birleştirme ile üçgen/paralelkenar alanı çıkarır."], "hook": "Farklı şekillerdeki tarla parsellerinin alanı.", "kriz": "Üçgenin alanını hesaplarken ikiye bölmeyi unutur."},
                {"kod": "MAT.6.4.2", "cikti": "Çemberin uzunluğu ile çapı arasındaki orana (pi) ilişkin çıkarım yapabilme", "surec": ["a) Farklı çemberlerin çevre ve çaplarını ölçer.", "b) Çevre/çap oranının sabitliğini geneller."], "hook": "Tekerleklerin bir tam turda aldığı mesafenin ölçülmesi.", "kriz": "Yarıçap (r) ile çapı (R) birbirine karıştırır."}
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {"kod": "MAT.6.5.1", "cikti": "Veriyle araştırma yapıp merkezî eğilim ve yayılımı yorumlayabilme", "surec": ["a) Araştırma sorusu/planı oluşturur.", "b) Ortalama, ortanca, tepe değer ve açıklığı yorumlar."], "hook": "Sınıfın boy veya sınav puan dağılımlarının incelenmesi.", "kriz": "Açıklığı (ranj) bulurken en küçük değer yerine sıfırı temel alır."}
            ],
            "6. Tema: Veriden Olasılığa": [
                {"kod": "MAT.6.6.1", "cikti": "Bir olayın olasılığını deneysel gözleme dayalı tahmin edebilme", "surec": ["a) Deney çıktılarını kaydeder.", "b) Deneme sayısı arttıkça göreli sıklığın kararlılığını yorumlar."], "hook": "Madeni paranın 10 kez ve 100 kez atılması sonuçları.", "kriz": "Kısa denemede (ör. 3 kez tura) olasılığın değiştiğini (daha çok tura geleceğini) sanır."}
            ]
        }
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Cebirsel Düşünme",
            "3. Tema: Dönüşüm Geometrisi",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: Geometrik Şekiller",
            "6. Tema: İstatistiksel Araştırma",
            "7. Tema: Olasılık"
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {"kod": "MAT.7.1.1", "cikti": "Rasyonel sayıları tanıma ve sayı doğrusunda sıralama", "surec": ["a) Rasyonel sayıları sayı doğrusuna yerleştirir.", "b) Sıralama ve mutlak değer yorumu yapar."], "hook": "Hissedilen sıcaklık ve deniz seviyesi ölçümleri.", "kriz": "Negatif rasyonel sayılarda sıfıra yakın olanın daha büyük olduğunu kavrayamaz."},
                {"kod": "MAT.7.1.2", "cikti": "Rasyonel sayılarla dört işlem içeren problemleri çözebilme", "surec": ["a) İşlem adımlarını planlar.", "b) Strateji uygulayıp çözer."], "hook": "Pasta dilimleme ve maaş bütçeleme problemleri.", "kriz": "Negatif sayılarla çarpma/bölmede işaretleri karıştırır."},
                {"kod": "MAT.7.1.3", "cikti": "Doğru ve ters orantı durumlarını ayırt etme ve problem çözme", "surec": ["a) Nicelikler arası orantı türünü belirler.", "b) Orantı sabiti ve denklemle problemi çözer."], "hook": "İşçi-zaman veya yol-zaman hesaplamaları.", "kriz": "Ters orantıda değişkenleri çarpmak yerine birbirine böler."}
            ],
            "2. Tema: Cebirsel Düşünme": [
                {"kod": "MAT.7.2.1", "cikti": "Birinci dereceden bir bilinmeyenli denklemleri çözebilme", "surec": ["a) Cebirsel ifadeyle modeller.", "b) Eşitliğin korunumu ilkesiyle denklemi çözer."], "hook": "Tahterevalli ve terazi dengesi problemleri.", "kriz": "Eşitliğin karşı tarafına geçen terimin işaretini değiştirmeyi unutur."}
            ],
            "3. Tema: Dönüşüm Geometrisi": [
                {"kod": "MAT.7.3.1", "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturma", "surec": ["a) Yansıma eksenine göre simetriyi inceler.", "b) Görüntüyü oluşturur ve karşılaştırır."], "hook": "Aynadaki veya durgun sudaki yansımalar.", "kriz": "Çapraz simetri eksenlerinde şekli katlamak yerine direkt öteler."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.7.4.1", "cikti": "Eş küplerle oluşturulan yapıların görünümlerini çizebilme", "surec": ["a) Önden, sağdan, üstten görünümleri çizer.", "b) Görünümlerden yapıyı oluşturur."], "hook": "Mimari maket tasarımı.", "kriz": "Görünmeyen (arkada kalan) küpleri hayal edemez."},
                {"kod": "MAT.7.4.2", "cikti": "Dairenin ve daire diliminin alan bağıntılarına çıkarım yapabilme", "surec": ["a) Merkez açı ile yay/alan orantısını kurar.", "b) Alanı hesaplar."], "hook": "Pizza dilimi ve sulama fıskiyesi alanı.", "kriz": "Tam daire (360 derece) üzerinden oran kurmayı unutur."}
            ],
            "5. Tema: Geometrik Şekiller": [
                {"kod": "MAT.7.5.1", "cikti": "Üçgende kenarortay, açıortay ve yüksekliği çözümleyebilme", "surec": ["a) Yardımcı elemanları çizer.", "b) Özelliklerini ve kesişimlerini inceler."], "hook": "Çatı iskeleti ağırlık merkezi ve dikmeleri.", "kriz": "Yükseklik ile kenarortay kavramlarını ve çizimlerini birbirine karıştırır."}
            ],
            "6. Tema: İstatistiksel Araştırma": [
                {"kod": "MAT.7.6.1", "cikti": "Sürekli veri ile çalışıp çizgi grafiği ile analiz edebilme", "surec": ["a) Sürekli veri toplar.", "b) Çizgi grafiği çizer ve eğilimleri yorumlar."], "hook": "Haftalık sıcaklık değişimi veya borsa takibi.", "kriz": "Çizgi grafiğini sürekli olmayan (kategorik) veriler için kullanmaya çalışır."}
            ],
            "7. Tema: Olasılık": [
                {"kod": "MAT.7.7.1", "cikti": "Bir olayın ve tümleyeninin olasılığına tümevarımsal akıl yürütebilme", "surec": ["a) Çıktıları gözlemler.", "b) Olay + Tümleyen = 1 ilişkisini geneller."], "hook": "Hedefi vurma ve vuramama olasılıkları.", "kriz": "Tümleyeni bulmak için olayın olasılığını 1'den çıkarmak yerine farklı işlem yapar."}
            ]
        }
    },
    "8. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Cebirsel Düşünme",
            "3. Tema: Geometrik Şekiller",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: Dönüşüm Geometrisi",
            "6. Tema: İstatistik",
            "7. Tema: Olasılık"
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {"kod": "MAT.8.1.1", "cikti": "Üslü ifadelere, özelliklerine ve işlemlerine çıkarım yapabilme", "surec": ["a) Üslü ifadelerde çarpma/bölme varsayımı kurar.", "b) Genellemeleri belirler ve modeller."], "hook": "Bakteri üremesi ve astronomik uzaklıklar.", "kriz": "Üssün üssü alınırken üstleri çarpmak yerine toplar."},
                {"kod": "MAT.8.1.2", "cikti": "Kareköklü ifadelerin yaklaşık değerini bulma ve işlem yapma", "surec": ["a) Tam kare ilişkiyi belirler.", "b) Tam kare olmayanların hangi iki sayı arasında olduğunu bulur."], "hook": "Alanı bilinen kare odanın kenar uzunluğu.", "kriz": "Karekök bulurken sayıyı ikiye böler (ör. Kök 16 = 8 der)."}
            ],
            "2. Tema: Cebirsel Düşünme": [
                {"kod": "MAT.8.2.1", "cikti": "Dik koordinat sistemini çözümleyebilme", "surec": ["a) Eksenleri ve bölgeleri belirler.", "b) Nokta koordinatlarını bulur."], "hook": "Haritada ve navigasyonda konum belirleme.", "kriz": "Apsis (x) ve ordinat (y) eksenlerinin yerini karıştırır."},
                {"kod": "MAT.8.2.2", "cikti": "Doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme", "surec": ["a) Tablo, grafik ve denklem geçişlerini yapar.", "b) Eğim (değişim oranı) yorumu yapar."], "hook": "Taksimetre grafiği ve maaş hesaplamaları.", "kriz": "Eğimi dikey/yatay oran yerine yatay/dikey oran olarak hesaplar."}
            ],
            "3. Tema: Geometrik Şekiller": [
                {"kod": "MAT.8.3.1", "cikti": "Üçgen eşitsizliğini ve açı-kenar ilişkilerini yorumlayabilme", "surec": ["a) Kenar ve açı büyüklüklerini sıralar.", "b) İki kenar toplamı ve farkı kuralını çıkarır."], "hook": "Çubuklarla üçgen yapma deneyi.", "kriz": "İki kısa kenar toplamının üçüncüden büyük olması gerektiğini unutur."},
                {"kod": "MAT.8.3.2", "cikti": "Pisagor bağıntısını (a²+b²=c²) yorumlayıp problem çözebilme", "surec": ["a) Dik kenarlar ve hipotenüs karelerini inceler.", "b) Bağıntıyı modelleyip uygular."], "hook": "Duvara dayalı merdiven yüksekliği.", "kriz": "Hipotenüs uzunluğunu bulmak için dik kenarları doğrudan toplar."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.8.4.1", "cikti": "Prizmalar, silindir, piramit ve koni açınımlarını çözümleyebilme", "surec": ["a) Yüzey şekillerini belirler.", "b) Açınım ile kapalı cisim arasındaki eşleşmeleri kurar."], "hook": "Karton ambalaj kutularının açınımı.", "kriz": "Silindirin yanal dikdörtgen kenarının, taban dairesinin çevresine eşit olduğunu göremez."},
                {"kod": "MAT.8.4.2", "cikti": "Dik dairesel silindirin hacim bağıntısına analojik akıl yürütebilme", "surec": ["a) Daire alanı ile prizma hacmini ilişkilendirir.", "b) Taban alanı x yükseklik genellemesini yapar."], "hook": "Silindirik su deposu kapasitesi.", "kriz": "Hacim hesabında yanal alan formülünü kullanır."}
            ],
            "5. Tema: Dönüşüm Geometrisi": [
                {"kod": "MAT.8.5.1", "cikti": "Dik koordinat sisteminde öteleme ve yansıma dönüşümlerini yapabilme", "surec": ["a) Koordinat değişimlerine dair kuralı bulur.", "b) Ardışık dönüşümler uygular."], "hook": "Oyun karakterinin eksenlere göre hareketi.", "kriz": "x eksenine göre yansımada, x koordinatının işaretini değiştirir."}
            ],
            "6. Tema: İstatistik": [
                {"kod": "MAT.8.6.1", "cikti": "Farklı veri setlerini ve grafikleri karşılaştırıp karar verebilme", "surec": ["a) Veri toplar.", "b) Uygun grafiği seçip yayılım/merkez analizi yapar."], "hook": "İki şubenin deneme sınavı başarı analizi.", "kriz": "Sadece ortalamaya bakarak yayılımı/açıklığı (standart sapmayı) göz ardı eder."}
            ],
            "7. Tema: Olasılık": [
                {"kod": "MAT.8.7.1", "cikti": "Olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı seçebilme", "surec": ["a) Karara uygun bilgi toplar.", "b) Yaklaşımları kıyaslayıp uygun olanı kullanır."], "hook": "Penaltı atışı veya hava durumu tahmini.", "kriz": "Deneysel olasılık gereken durumda salt teorik olasılıkla kesin hüküm verir."}
            ]
        }
    }
}
# ==========================================
# 5. ADIM 1: KURULUM VE RUBRİK YÜKLEME
# ==========================================
if st.session_state.adim == 1:
    st.markdown('<span class="rozet">ADIM 1 / 3</span>', unsafe_allow_html=True)
    st.subheader("📝 2024 TYMM Kurulum ve Rubrik Yükleme Paneli")
    st.info("Aday bilgileri ve danışman öğretim elemanının rubriği doldurulmadan 2. adıma geçilemez.")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">Aday ve Danışman Bilgileri</div>', unsafe_allow_html=True)
        ogretmen_adi = st.text_input("Öğretmen Adayı *", placeholder="Örn: Mislina Taysi")
        okul_numarasi = st.text_input("Okul Numarası *", placeholder="Örn: 20220000000")
        universite_adi = st.text_input("Üniversite Adı *", value="Eğitim Fakültesi")
        uygulama_ogretim_elemani = st.text_input("Danışman Öğretim Elemanı *")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">Değerlendirme Rubriği</div>', unsafe_allow_html=True)
        rubrik_metni = st.text_area(
            "Rubrik Kriterleri (AI Değerlendirmesine Esas Olacaktır) *",
            value="1. Öğrenci profillerine duyarlı kapsayıcı iletişim (30 Puan).\n2. 2024 TYMM keşif odaklı süreç uyumu (30 Puan).\n3. Profile ve kazanıma uygun materyal seçimi/kullanımı (40 Puan).",
            height=130,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 3D Staj Simülasyonunu Başlat", type="primary", use_container_width=True):
        if not all([ogretmen_adi.strip(), okul_numarasi.strip(), universite_adi.strip(), uygulama_ogretim_elemani.strip(), rubrik_metni.strip()]):
            st.error("❌ Zorunlu (*) alanlar doldurulmadan ilerlenemez.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi.strip()
            st.session_state.okul_numarasi = okul_numarasi.strip()
            st.session_state.universite_adi = universite_adi.strip()
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani.strip()
            st.session_state.rubrik_metni = rubrik_metni.strip()
            st.session_state.adim = 2
            st.rerun()

# ==========================================
# 6. ADIM 2: 3D SINIF, ONAY KUTULU ÖĞRENCİ SEÇİMİ VE DİNAMİK MÜDAHALE
# ==========================================
elif st.session_state.adim == 2:
    st.markdown('<span class="rozet">ADIM 2 / 3</span>', unsafe_allow_html=True)
    st.markdown(f"### 🏫 3D Canlı Sınıf | Aday: {st.session_state.ogretmen_adi}")

    with st.expander("📚 2024 TYMM Müfredat Seçimi", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: secilen_sinif = st.selectbox("Sınıf Düzeyi *", list(tyym_master_arsiv.keys()))
        with col_s2: secilen_tema = st.selectbox("Tema *", tyym_master_arsiv[secilen_sinif]["Temalar"])
        kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"].get(secilen_tema, [])
        with col_s3:
            kazanim_sec = ["Seçiniz..."] + [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
            secilen_kazanim_str = st.selectbox("Kazanım *", kazanim_sec)

        if secilen_kazanim_str == "Seçiniz...": st.stop()
        secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str)
        secilen_surec = st.selectbox("Süreç Bileşeni *", ["Seçiniz..."] + secilen_kazanim_obj["surec"])
        if secilen_surec == "Seçiniz...": st.stop()
        st.success(f"💡 **Bağlam:** {secilen_kazanim_obj['hook']}")

    st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
    st.markdown('<div class="baslik-mavi">👥 Öğrenci Seçimi (1-10 Arası Onay Kutuları) *</div>', unsafe_allow_html=True)
    ogrenci_adlari = list(ogrenci_profilleri.keys())
    secili_liste = []
    cb_cols = st.columns(5)
    for idx in range(10):
        ad = ogrenci_adlari[idx]
        bilgi = ogrenci_profilleri[ad]
        with cb_cols[idx % 5]:
            if st.checkbox(f"{bilgi['ikon']} {ad}", key=f"cb_{ad}"): secili_liste.append(ad)
            st.caption(bilgi["durum"])
    st.session_state.secili_ogrenciler = secili_liste
    st.markdown('</div>', unsafe_allow_html=True)

    if not secili_liste:
        st.error("❌ En az 1 öğrenci seçilmelidir.")
        st.stop()

    st.markdown("#### 🧠 Seçili Öğrencilerin Başlangıç Durumları")
    kart_cols = st.columns(min(len(secili_liste), 3))
    for idx, ogr_ad in enumerate(secili_liste):
        bilgi = ogrenci_profilleri[ogr_ad]
        davranis = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"])
        with kart_cols[idx % len(kart_cols)]:
            with st.container(border=True):
                st.markdown(f"**{ogr_ad} ({bilgi['durum']})**")
                st.write(davranis)

    # Yapay Zekanın Bağlamsal Şık Üretimi
    dinamik_eylem_1_list, dinamik_eylem_2_list = dinamik_eylem_secenekleri_uret(secilen_tema, secilen_kazanim_obj["kod"], secilen_surec, secilen_kazanim_obj["kriz"])

    col_sol, col_sag = st.columns([1.2, 0.8], gap="large")
    with col_sol:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">🎙️ Pedagojik Müdahale Konsolu</div>', unsafe_allow_html=True)
        sesli_girdi = st.text_area("✍️ Öğrencilere Söyleyecekleriniz *", placeholder="Hitabınızı yazın...", height=85)
        
        # Dinamik şıkları kullanıyoruz
        eylem_1 = st.selectbox("1. Pedagojik Eylem (AI Dinamik Seçenekleri) *", dinamik_eylem_1_list)
        eylem_2 = st.selectbox("2. Pedagojik Eylem (AI Dinamik Seçenekleri) *", dinamik_eylem_2_list)
        materyal = st.selectbox("Materyal Seçimi *", MATERYAL_SECENEKLER)
        
        ozgun_tanitim = ""
        if materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal":
            ozgun_ad = st.text_input("Özgün Materyal Adı *")
            ozgun_tanitim = st.text_area("Materyali Tanıtın *")
            materyal_etiketi = f"{ozgun_ad} (Özgün Materyal)"
        else:
            materyal_etiketi = materyal
            
        mat_aciklama = st.text_area("Nasıl Kullanacaksınız? *", height=85)

        if st.button("📥 Müdahaleyi Kaydet ve AI Değerlendirmesini Gör", type="primary", use_container_width=True):
            eksik_ozgun = materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal" and (not ozgun_ad.strip() or not ozgun_tanitim.strip())
            if not sesli_girdi.strip() or eylem_1 == "Seçiniz..." or eylem_2 == "Seçiniz..." or materyal == "Seçiniz..." or not mat_aciklama.strip() or eksik_ozgun:
                st.error("❌ Tüm zorunlu alanları doldurunuz.")
            else:
                ai_tepkileri = {}
                for ogr_ad in secili_liste:
                    ai_tepkileri[ogr_ad] = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"], sesli_girdi, eylem_1, eylem_2, materyal_etiketi, mat_aciklama)
                
                # Rubrik AI Değerlendirmesi
                durumlar = [ogrenci_profilleri[o]["durum"] for o in secili_liste]
                d1, d2 = eylem_uygunlugu_degerlendir(eylem_1, eylem_2, durumlar[0])
                ai_puan, ai_mesaj = ai_rubrik_degerlendirmesi(eylem_1, eylem_2, materyal_etiketi, st.session_state.rubrik_metni, d1, d2, durumlar)

                st.session_state.simulasyon_gecmisi.append({
                    "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sinif": secilen_sinif, "tema": secilen_tema, "kod": secilen_kazanim_obj["kod"], "cikti": secilen_kazanim_obj["cikti"],
                    "surec": secilen_surec, "secili_ogrenciler": secili_liste, "eylem_1": eylem_1, "eylem_2": eylem_2,
                    "materyal_etiketi": materyal_etiketi, "ozgun_tanitim": ozgun_tanitim, "mat_aciklama": mat_aciklama,
                    "sesli_girdi": sesli_girdi, "ai_tepkileri": ai_tepkileri, "ai_puan": ai_puan, "ai_mesaj": ai_mesaj
                })
                st.session_state.adim = 3
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_sag:
        st.info("Müdahaleyi kaydettikten sonra; sistem rubriği analiz edip anlık değerlendirme ve öğrenci tepkileriyle birlikte sizi 3. Adıma aktaracaktır.")

# ==========================================
# 7. ADIM 3: ANLIK AI DEĞERLENDİRMESİ VE DERS TRANSKRİPTİ
# ==========================================
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 Anlık Rubrik Geri Dönütü ve Transkript")
    
    son_kayit = st.session_state.simulasyon_gecmisi[-1]
    
    # ANLIK AI GERİ BİLDİRİMİ EKRANDA
    st.markdown(f"<div class='anlik-bildirim'>{son_kayit['ai_mesaj']}<br><b>Sistem Puanı:</b> {son_kayit['ai_puan']} / 100</div>", unsafe_allow_html=True)
    
    tab_trans, tab_hoca = st.tabs(["📝 Detaylı Ders Transkripti & Öğrenci Tepkileri", "👨‍🏫 Öğretim Elemanı Kararı"])
    
    with tab_trans:
        st.markdown("#### Öğretmen Adayının Dersteki Eylemleri ve Öğrenci Yanıtları")
        for ogr, tepki in son_kayit["ai_tepkileri"].items():
            st.write(f"- {tepki}")
            
        st.divider()
        ozg_metin = f"\n- **Özgün Materyal:** {son_kayit['ozgun_tanitim']}" if son_kayit["ozgun_tanitim"] else ""
        transkript = (
            f"**Tarih:** {son_kayit['tarih']} | **Aday:** {st.session_state.ogretmen_adi}\n"
            f"**Kazanım:** {son_kayit['kod']} ({son_kayit['surec']})\n\n"
            f"**1. Eylem (AI Dinamik Seçimi):** {son_kayit['eylem_1']}\n**2. Eylem (AI Dinamik Seçimi):** {son_kayit['eylem_2']}\n"
            f"**Materyal:** {son_kayit['materyal_etiketi']}{ozg_metin}\n"
            f"**Kullanım:** {son_kayit['mat_aciklama']}\n**Adayın İletişimi:** {son_kayit['sesli_girdi']}\n"
        )
        st.markdown(f"<div class='transkript-kutu'>{transkript}</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="⬇️ Yazılı Ders Transkriptini İndir (.txt)",
            data=transkript.replace("**", "").replace("*", "").replace("`", ""),
            file_name=f"2024_TYMM_Ders_Transkripti_{st.session_state.get('okul_numarasi', 'aday')}.txt",
            mime="text/plain",
        )

    with tab_hoca:
        st.markdown("### Danışman Öğretim Elemanı Geri Dönütü")
        hoca_notu = st.text_area("AI ön değerlendirmesini ve transkripti göz önünde bulundurarak adaya resmî geri dönütünüzü yazın *")
        if st.button("📤 Geri Dönütü Kaydet", type="primary"):
            if hoca_notu.strip():
                st.success("✅ Öğretim elemanı geri dönütü kaydedildi.")
            else:
                st.error("❌ Geri dönüt alanı boş bırakılamaz.")
                
    st.divider()
    st.warning("⚠️ Ezber oluşmasını önlemek amacıyla aynı senaryoya dönülemez. Lütfen yeni bir simülasyon başlatınız.")
    if st.button("🔄 Yeni Bir Simülasyon Başlat (Sıfırla)"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.secili_ogrenciler = []
        st.session_state.otur_seed = random.randint(1, 1000) # Yeni varyasyon tohumu
        st.session_state.adim = 1
        st.rerun()
