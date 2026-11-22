import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="2024 Türkiye Yüzyılı Maarif Modeli - Ortaokul Matematik 3D Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# Göz yormayan, uyumlu renk paleti ve sade kart tasarımı
st.markdown("""
    <style>
    .sade-kart {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #1E40AF;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .baslik-mavi {
        color: #1E3A8A;
        font-weight: 700;
        font-size: 1.06rem;
        margin-bottom: 8px;
    }
    .rozet {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .transkript-kutu {
        background-color: #FFFFFF;
        border: 1px solid #94A3B8;
        border-radius: 8px;
        padding: 16px;
        line-height: 1.65;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
    st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state:
    st.session_state.secili_ogrenciler = []

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ
# ==========================================
ogrenci_profilleri = {
    "Kerem": {
        "durum": "Disleksi",
        "ikon": "👦",
        "mimik": "Alnını ovuşturuyor / Basamak ve sembollere odaklanıyor",
        "ozellik": "Rakamları, basamakları ve sembolleri ters algılayabilir veya yer değiştirebilir; görsel-dokunsal gruplamaya ihtiyaç duyar.",
    },
    "Arda": {
        "durum": "Otizm Spektrumu",
        "ikon": "👦",
        "mimik": "Kulaklık takılı / Hafifçe sallanıyor",
        "ozellik": "Ani seslere ve belirsiz yönergelere hassastır; net, öngörülebilir adımlar ve sakin ton ister.",
    },
    "Can": {
        "durum": "Üstün Yetenekli",
        "ikon": "👦",
        "mimik": "Sabırsız / Parmağı havada",
        "ozellik": "Ezberden ve tekrardan sıkılır; kavramın nedenini, genellemesini ve farklı durumlarını sorgular.",
    },
    "Elif": {
        "durum": "Yüksek Kaygılı",
        "ikon": "👧",
        "mimik": "Başını öne eğmiş / Tedirgin",
        "ozellik": "Hata yapmaktan çekinir; baskı hissederse donup kalabilir, destekleyici ve güvenli bir dille açılır.",
    },
    "Zeynep": {
        "durum": "DEHB",
        "ikon": "👧",
        "mimik": "Sürekli etrafa bakınıyor / Kalemle oynuyor",
        "ozellik": "Dikkati çabuk dağılabilir; kısa, odaklanmış ve aktif katılımlı adımlarda daha iyi kalır.",
    },
    "Mehmet": {
        "durum": "İşitme Yetersizliği",
        "ikon": "👦",
        "mimik": "Konuşmacının yüzüne odaklanmış",
        "ozellik": "Görsel ipuçlarına, açık yüz ifadesine ve yazılı/görsel pekiştireçlere ihtiyaç duyar.",
    },
    "Ayşe": {
        "durum": "Az Gören",
        "ikon": "👧",
        "mimik": "Gözlerini kısarak yakından inceliyor",
        "ozellik": "Küçük/karmaşık görsellerde zorlanır; net kontrastlı, dokunsal ve açık sözel betimlemelere dayanır.",
    },
    "Ali": {
        "durum": "Diskalkuli",
        "ikon": "👦",
        "mimik": "Parmaklarıyla saymaya çalışıyor",
        "ozellik": "Sayıların büyüklük/oran ilişkisini ve işlem mantığını zihinde kurmakta zorlanır; somut model ister.",
    },
    "Merve": {
        "durum": "Bedensel Yetersizlik",
        "ikon": "👧",
        "mimik": "Elleri sıranın üzerinde / Odaklı",
        "ozellik": "Bilişsel olarak konuyu takip eder; ancak yoğun yazma/çizim gerektiren adımlarda erişilebilir destek ister.",
    },
    "Burak": {
        "durum": "Düşük Motivasyon",
        "ikon": "👦",
        "mimik": "Kolları bağlı / İlgisiz görünüyor",
        "ozellik": "Soyut kurallara mesafelidir; gerçek yaşamla anlamlı bağ kurulduğunda katılım gösterir.",
    },
}

# ==========================================
# 2. BİRBİRİNE YAKIN 6'ŞAR PEDAGOJİK EYLEM SEÇENEĞİ VE MATERYAL LİSTESİ
# ==========================================
EYLEM_1_SECENEKLER = [
    "Seçiniz...",
    "Öğrencinin duygusunu ve yaşadığı zorlanmayı kabul ederek güvenli alan sunmak",
    "Sıranın başına gidip öğrencinin neyi kaçırdığını kısa ve sakin ifadelerle sormak",
    "Sınıfın genel akışını bozmadan öğrenciye bireysel olarak toparlanma süresi tanımak",
    "Dikkati dağılan veya zorlanan öğrenciye sınıf kuralını nazikçe hatırlatıp odak davet etmek",
    "Öğrenciyi akranlarının önünde zorlamadan konuyu kendi hızında incelemesini istemek",
    "Yaşanan duraksamayı not alıp anlatımı hızlandırmadan mevcut basamakta kalmak",
]

EYLEM_2_SECENEKLER = [
    "Seçiniz...",
    "Seçilen/tasarlanan materyal üzerinden yönlendirici sorularla ilişkiyi öğrencinin keşfetmesini sağlamak",
    "Kavramı günlük yaşam örneğiyle eşleştirip öğrenciden kendi ifadesiyle açıklamasını istemek",
    "Adımları parçalara ayırarak farklı bir temsil (şekil, tablo, model) üzerinden yeniden denetmek",
    "Öğrenciyle birlikte ilk örneği kurup benzer bir durumu karşılaştırarak genelleme aramak",
    "Kuralın temel mantığını kısa bir örnekle gösterip akran etkileşimiyle sınamasını istemek",
    "Zorlanılan basamağı basitleştirilmiş bir alt problemle destekleyip adımı yeniden kurmak",
]

MATERYAL_SECENEKLER = [
    "Seçiniz...",
    "Kendi Geliştirdiğim / Tasarladığım Materyal",
    "Somut Materyal (Onluk Taban Blokları, Kesir Takımı, Birim Küpler vb.)",
    "Dinamik Matematik Yazılımı (GeoGebra / Desmos)",
    "Yüksek Kontrastlı Görsel & Dokunsal Kartlar",
    "Günlük Yaşam Nesneleri ve Ölçüm Araçları",
    "Geometrik Şekil / Açınım ve Simetri Modelleri",
    "Koordinat / Grafik / Tablo Çalışma Panosu",
    "Olasılık ve Veri Deneyi Araçları (Zar, Çark, Kart, Anket Formu)",
    "Klasik Çalışma Kâğıdı / Formül ve Kural Özeti",
]


def eylem_uygunlugu_degerlendir(eylem_1, eylem_2, ogr_durum):
    duygusal_destekli_1 = eylem_1 in [
        "Öğrencinin duygusunu ve yaşadığı zorlanmayı kabul ederek güvenli alan sunmak",
        "Sıranın başına gidip öğrencinin neyi kaçırdığını kısa ve sakin ifadelerle sormak",
        "Sınıfın genel akışını bozmadan öğrenciye bireysel olarak toparlanma süresi tanımak",
        "Öğrenciyi akranlarının önünde zorlamadan konuyu kendi hızında incelemesini istemek",
    ]
    kesif_destekli_2 = eylem_2 in [
        "Seçilen/tasarlanan materyal üzerinden yönlendirici sorularla ilişkiyi öğrencinin keşfetmesini sağlamak",
        "Kavramı günlük yaşam örneğiyle eşleştirip öğrenciden kendi ifadesiyle açıklamasını istemek",
        "Adımları parçalara ayırarak farklı bir temsil (şekil, tablo, model) üzerinden yeniden denetmek",
        "Öğrenciyle birlikte ilk örneği kurup benzer bir durumu karşılaştırarak genelleme aramak",
    ]

    if ogr_durum == "Otizm Spektrumu" and eylem_1 == "Öğrenciyi akranlarının önünde zorlamadan konuyu kendi hızında incelemesini istemek":
        duygusal_destekli_1 = True
    if ogr_durum == "Üstün Yetenekli" and eylem_2 in [
        "Seçilen/tasarlanan materyal üzerinden yönlendirici sorularla ilişkiyi öğrencinin keşfetmesini sağlamak",
        "Öğrenciyle birlikte ilk örneği kurup benzer bir durumu karşılaştırarak genelleme aramak",
    ]:
        kesif_destekli_2 = True
    if ogr_durum == "Düşük Motivasyon" and eylem_2 == "Kavramı günlük yaşam örneğiyle eşleştirip öğrenciden kendi ifadesiyle açıklamasını istemek":
        kesif_destekli_2 = True

    return duygusal_destekli_1, kesif_destekli_2


def ai_profil_davranisi_uret(
    ogrenci_adi,
    sinif,
    tema,
    kazanim_kod,
    kazanim_cikti,
    surec,
    temel_kriz,
    aday_sozu="",
    eylem_1="",
    eylem_2="",
    materyal_etiketi="",
    materyal_aciklama="",
):
    profil = ogrenci_profilleri[ogrenci_adi]
    durum = profil["durum"]
    tema_kisa = tema.split(":", 1)[1].strip() if ":" in tema else tema
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec

    mudahale_var = bool(aday_sozu.strip() or eylem_1 or materyal_etiketi)
    d1, d2 = eylem_uygunlugu_degerlendir(eylem_1, eylem_2, durum)

    if not mudahale_var:
        if durum == "Otizm Spektrumu":
            return f"{ogrenci_adi} (Otizm Spektrumu): {sinif} '{tema_kisa}' temasında `{kazanim_kod}` ({surec_kisa}) adımında kulaklığını yoklayarak net ve öngörülebilir bir sıra bekler; '{temel_kriz}' belirsizliğinden rahatsız olur."
        if durum == "Disleksi":
            return f"{ogrenci_adi} (Disleksi): `{kazanim_kod}` ({kazanim_cikti}) ve '{surec_kisa}' sürecinde sayı/sembol sıralarını karıştırır; '{temel_kriz}' anında görsel-dokunsal ayrıştırma arar."
        if durum == "Üstün Yetenekli":
            return f"{ogrenci_adi} (Üstün Yetenekli): '{tema_kisa}' bağlamında '{surec_kisa}' adımı için yüzeysel açıklamayı yeterli bulmaz; '{temel_kriz}' sırasında genellemenin gerekçesini sorgular."
        if durum == "Yüksek Kaygılı":
            return f"{ogrenci_adi} (Yüksek Kaygılı): `{kazanim_kod}` ve '{surec_kisa}' sürecinde hata yapmaktan çekinip omuzlarını çeker; '{temel_kriz}' anında yargılamayan destek bekler."
        if durum == "DEHB":
            return f"{ogrenci_adi} (DEHB): '{tema_kisa}' temasında '{surec_kisa}' adımı uzadıkça dikkati dağılır; '{temel_kriz}' sırasında kısa ve aktif katılımlı adım ister."
        if durum == "İşitme Yetersizliği":
            return f"{ogrenci_adi} (İşitme Yetersizliği): `{kazanim_kod}` ve '{surec_kisa}' adımında yüz ifadesine ve görsel temsile odaklanır; '{temel_kriz}' anında net görsel ipucu bekler."
        if durum == "Az Gören":
            return f"{ogrenci_adi} (Az Gören): '{tema_kisa}' temasında '{surec_kisa}' sırasında küçük ayrıntıları seçmekte zorlanır; '{temel_kriz}' anında dokunsal ve açık sözel betimleme ister."
        if durum == "Diskalkuli":
            return f"{ogrenci_adi} (Diskalkuli): `{kazanim_kod}` ({surec_kisa}) sürecinde nicelik ve işlem ilişkisini zihninde kurmakta zorlanır; '{temel_kriz}' anında somut model arar."
        if durum == "Bedensel Yetersizlik":
            return f"{ogrenci_adi} (Bedensel Yetersizlik): '{tema_kisa}' temasında '{surec_kisa}' mantığını takip eder ancak yoğun yazma/çizim gerektiren '{temel_kriz}' adımında erişilebilir araç ister."
        return f"{ogrenci_adi} (Düşük Motivasyon): `{kazanim_kod}` ve '{surec_kisa}' sürecinde konunun günlük yaşam karşılığını sorgular; '{temel_kriz}' anında anlamlı bir bağlam sunulursa katılır."

    soz_ozet = aday_sozu.strip()[:75]
    mat_ozet = materyal_aciklama.strip()[:65]

    if not (d1 and d2):
        return (
            f"{ogrenci_adi} ({durum}): Öğretmenin \"{soz_ozet}\" ifadesine rağmen "
            f"'{surec_kisa}' basamağında seçilen eylem sırası profil ihtiyaçlarını tam "
            f"karşılamadığı için '{materyal_etiketi}' ile ilerlerken temkinli veya kararsız kalır."
        )

    return (
        f"{ogrenci_adi} ({durum}): Öğretmenin \"{soz_ozet}\" yaklaşımına karşılık "
        f"'{materyal_etiketi}' ({mat_ozet}...) ile '{surec_kisa}' basamağını izler ve "
        f"`{kazanim_kod}` ({kazanim_cikti}) ilişkisini daha rahat yapılandırır."
    )


# ==========================================
# 3. 2024 TÜRKİYE YÜZYILI MAARİF MODELİ ORTAOKUL MATEMATİK (5–8. SINIF) ARŞİVİ
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Geometrik Nicelikler",
            "4. Tema: İstatistiksel Araştırma Süreci",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
                    "surec": [
                        "a) Günlük hayattaki bağlamlardan yola çıkarak çok basamaklı sayılar hakkında bilgi toplar.",
                        "b) Sayıların bölümleri ile okunuşları arasındaki ortak özellikleri belirler.",
                        "c) Sayıların bölümleri ile okunuşları arasındaki farklılıkları belirler.",
                        "ç) Örüntüler üzerinden basamak sayısı çok olan sayıların okunuş/yazılışlarına dair önermelerde bulunur.",
                    ],
                    "hook": "Millî Kütüphane ve arşiv kayıtlarındaki çok basamaklı kodlama sistemleri.",
                    "kriz": "Çok basamaklı sayılarda sıfır içeren bölükleri okurken basamakları karıştırır.",
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": "Doğal sayılar ve işlemler içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Problemdeki sayı ve işlem bileşenlerini belirler.",
                        "b) Uygun strateji ve temsiller geliştirerek problemi çözer.",
                        "c) Çözümün doğruluğunu ve farklı yollarını değerlendirir.",
                    ],
                    "hook": "Okul gezisi bütçesi, bilet ve ulaşım planlaması hesaplamaları.",
                    "kriz": "Çok adımlı problemde hangi işlemin önce yapılacağını belirlemekte zorlanır.",
                },
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.5.1.3",
                    "cikti": "Kesirlerin farklı gösterimlerini ve sayı doğrusundaki yerlerini ilişkilendirebilme",
                    "surec": [
                        "a) Bütün-parça ilişkisinden hareketle basit, bileşik ve tam sayılı kesirleri inceler.",
                        "b) Denk kesirleri modeller ve sayı doğrusu üzerinde karşılaştırır.",
                    ],
                    "hook": "Tarif ve paylaşım durumlarında yarım, çeyrek ve tam bütün eşleştirmeleri.",
                    "kriz": "Payda büyüdükçe birim kesrin küçüldüğünü görsel olarak kabullenmekte zorlanır.",
                },
                {
                    "kod": "MAT.5.1.4",
                    "cikti": "Kesir, ondalık ve yüzde gösterimleri arasındaki ilişkileri yorumlayabilme",
                    "surec": [
                        "a) Yüzlük kart ve modeller üzerinden kesir, ondalık ve yüzde temsillerini eşleştirir.",
                        "b) Farklı gösterimler arasında dönüşüm yaparak karşılaştırma yapar.",
                    ],
                    "hook": "Cihaz batarya yüzdesi ile kesir ve ondalık gösterimlerin karşılaştırılması.",
                    "kriz": "Ondalık gösterimdeki basamak değerleriyle yüzde gösterimini karıştırır.",
                },
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.5.2.1",
                    "cikti": "Temel geometrik çizimler için matematiksel araç ve teknolojiden yararlanabilme",
                    "surec": [
                        "a) Nokta, doğru, doğru parçası, ışın ve açıyı uygun araçlarla çizer.",
                        "b) Çizdiği geometrik elemanların özelliklerini ve ilişkilerini açıklar.",
                    ],
                    "hook": "Mahalle krokisindeki kavşaklar, sokaklar ve dönemeç açıları.",
                    "kriz": "Işın ile doğru parçasının uç noktalarındaki farkı çizimde karıştırır.",
                },
                {
                    "kod": "MAT.5.2.2",
                    "cikti": "Çokgenlerin ve üçgenlerin temel elemanlarını ve açı özelliklerini çözümleyebilme",
                    "surec": [
                        "a) Çokgenleri kenar ve köşe özelliklerine göre sınıflandırır.",
                        "b) Üçgenleri açılarına ve kenarlarına göre inceleyerek genellemeler yapar.",
                    ],
                    "hook": "Trafik levhaları ve mimari cephelerdeki çokgen formlar.",
                    "kriz": "Geniş açılı üçgen ile dar açılı üçgeni ayırt ederken tüm açılara bakmayı unutur.",
                },
            ],
            "3. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.3.1",
                    "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkileri yorumlayabilme",
                    "surec": [
                        "a) Birim kareler kullanarak dikdörtgenin alanını ve çevresini hesaplar.",
                        "b) Aynı çevreye sahip farklı dikdörtgenlerin alanlarını karşılaştırır.",
                    ],
                    "hook": "Eşit uzunlukta çit teliyle farklı boyutlarda bahçe parseli oluşturma.",
                    "kriz": "Çevre uzunluğu ile alan kavramlarını birbirine karıştırır.",
                }
            ],
            "4. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.4.1",
                    "cikti": "Kategorik veriyle çalışabilme ve veriye dayalı karar verebilme",
                    "surec": [
                        "a) Araştırma sorusu oluşturur ve veri toplama planı yapar.",
                        "b) Sıklık tablosu ve sütun grafiğiyle veriyi görselleştirip yorumlar.",
                    ],
                    "hook": "Sınıfın en çok tercih ettiği okuma ve spor etkinlikleri araştırması.",
                    "kriz": "Araştırma sorusu ile tek cevaplı soruyu ayırt etmekte zorlanır.",
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.5.1",
                    "cikti": "Herhangi bir olayın olasılığının 0 ile 1 arasında olduğunu yorumlayabilme",
                    "surec": [
                        "a) İmkânsız, olası ve kesin olayları günlük yaşam örnekleriyle inceler.",
                        "b) Olayların gerçekleşme ihtimalini 0 ile 1 aralığında konumlandırır.",
                    ],
                    "hook": "Hava durumu tahmini ve renkli torbadan çekiliş senaryoları.",
                    "kriz": "Olasılığı 1'den büyük bir sayı olarak ifade etmeye çalışır.",
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler",
            "3. Tema: Geometrik Şekiller",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: İstatistiksel Araştırma Süreci",
            "6. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {
                    "kod": "MAT.6.1.1",
                    "cikti": "Bir doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme",
                    "surec": [
                        "a) Çarpan ve kat ilişkilerine yönelik varsayımlarda bulunur.",
                        "b) Örnek durumların ilişkilerini inceleyerek genellemeleri belirler.",
                        "c) Genellemeleri farklı temsillerle gösterir.",
                    ],
                    "hook": "İki farklı otobüs hattının duraktan aynı anda hareket etme saatleri.",
                    "kriz": "Çarpan ve kat kavramlarını karıştırıp kuralları ezberlemeye çalışır.",
                },
                {
                    "kod": "MAT.6.1.2",
                    "cikti": "2, 3, 4, 5, 6, 9 ve 10 ile tam bölünebilme kriterlerine ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) Basamak yapısı üzerinden bölünebilme varsayımları kurar.",
                        "b) Örnekler üzerinde genellemeleri sınar ve önermeler sunar.",
                    ],
                    "hook": "Öğrencileri artansız takımlara ayırma planlaması.",
                    "kriz": "3 ve 9 ile bölünebilme kuralını son basamağa göre uygulamaya çalışır.",
                },
                {
                    "kod": "MAT.6.1.3",
                    "cikti": "Doğal sayının asal olma durumunu ve asal çarpanlarını çözümleyebilme",
                    "surec": [
                        "a) Çarpan sayısına göre asal ve bileşik sayıları ayırt eder.",
                        "b) Sayıyı asal çarpanlarının çarpımı biçiminde ifade eder.",
                    ],
                    "hook": "Sayıların temel yapı taşları olarak asal çarpanların şifrelemede kullanımı.",
                    "kriz": "1 sayısını asal kabul eder veya çift asal sayıyı gözden kaçırır.",
                },
                {
                    "kod": "MAT.6.1.4",
                    "cikti": "İki doğal sayının ortak bölenleri ile ortak katlarını yorumlayabilme",
                    "surec": [
                        "a) Ortak bölen ve ortak kat ilişkilerini problem durumlarında belirler.",
                        "b) Sayı doğrusu, tablo veya şema üzerinde ortak değerleri karşılaştırır.",
                    ],
                    "hook": "Farklı uzunluktaki iki kurdeleyi eşit parçalara ayırma ve ortak uzunlukta buluşturma.",
                    "kriz": "Problemde ortak bölen mi yoksa ortak kat mı kullanacağını ayırt edemez.",
                },
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.6.1.5",
                    "cikti": "Ondalık gösterimlerin basamak değerlerini kesirlerle ilişkilendirerek yorumlayabilme",
                    "surec": [
                        "a) Ondalık gösterimdeki basamak değerlerini inceler.",
                        "b) Kesir toplamlarıyla yeniden ifade ederek çözümleme yapar.",
                    ],
                    "hook": "Dijital tartıda kilogram ve gram cinsinden hassas ölçümler.",
                    "kriz": "Binde birler basamağındaki sıfırların basamak değerini yazarken şaşırır.",
                },
                {
                    "kod": "MAT.6.1.7",
                    "cikti": "Kesir, ondalık ve yüzde gösterimleriyle dört işlem gerektiren problemleri çözebilme",
                    "surec": [
                        "a) Problemdeki sayı ve işlem bileşenlerini belirler.",
                        "b) Uygun temsil ve strateji geliştirerek problemi çözer.",
                        "c) Çözüm yollarını kontrol eder ve değerlendirir.",
                    ],
                    "hook": "İndirim oranları ve ürün etiketlerinin karşılaştırılması.",
                    "kriz": "Kesirlerde bölme işleminde ikinci kesri ters çevirme mantığını kuramaz.",
                },
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.6.2.1",
                    "cikti": "Gerçek yaşam durumlarındaki nicelikleri cebirsel ifadelerle modelleyebilme",
                    "surec": [
                        "a) Sabit ve değişken nicelikleri belirler.",
                        "b) İlişkiyi tablo ve cebirsel ifadeyle temsil eder.",
                    ],
                    "hook": "Kumbaradaki başlangıç tutarına her hafta eklenen sabit miktar.",
                    "kriz": "Harf sembolünün değişken olduğunu anlamakta zorlanır.",
                },
                {
                    "kod": "MAT.6.2.2",
                    "cikti": "Sayı ve şekil örüntülerinin kuralını cebirsel olarak ifade edebilme",
                    "surec": [
                        "a) Ardışık adımlar arasındaki değişim miktarını inceler.",
                        "b) Örüntünün genel kuralını tablo ve cebirsel ifadeyle gösterir.",
                    ],
                    "hook": "Kibrit çöpleriyle adım adım büyüyen geometrik desenler.",
                    "kriz": "Artış miktarını bulur ancak başlangıç terimi ilişkisini kuramaz.",
                },
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1",
                    "cikti": "İki paralel doğru ve bir kesenin oluşturduğu açıları sınıflandırabilme",
                    "surec": [
                        "a) Paralel doğrular ve kesenle oluşan açıları belirler.",
                        "b) Yöndeş, iç ters ve dış ters açıları ilişkilendirir.",
                    ],
                    "hook": "Tren rayları ve makas bağlantılarındaki açı ilişkileri.",
                    "kriz": "Kesen doğrunun eğimi değişince iç ters açıları bulmakta zorlanır.",
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.2",
                    "cikti": "Dikdörtgenin alan deneyimlerini paralelkenar ve üçgenin alan bağıntısına yansıtabilme",
                    "surec": [
                        "a) Dikdörtgen alan bağıntısını gözden geçirir.",
                        "b) Parçalama-birleştirme yoluyla paralelkenar ve üçgen alanı çıkarımı yapar.",
                    ],
                    "hook": "Tarım parsellerinin eş üçgen ve paralelkenar alanlara ayrılması.",
                    "kriz": "Geniş açılı üçgende yüksekliği tabana dik indirmekte zorlanır.",
                },
                {
                    "kod": "MAT.6.4.4",
                    "cikti": "Çemberin uzunluğu ile çap uzunluğu arasındaki orana ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) Farklı çemberlerin çevre ve çaplarını ölçer.",
                        "b) Çevre/çap oranının sabitliğini geneller.",
                    ],
                    "hook": "Farklı tekerleklerin bir tam turda aldığı yol ile çaplarının karşılaştırılması.",
                    "kriz": "Yarıçap ile çapı karıştırıp çevre uzunluğu hesabında hata yapar.",
                },
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": "Kategorik veya kesikli nicel veriyle araştırma yapıp merkezî eğilim ve yayılımı yorumlayabilme",
                    "surec": [
                        "a) Araştırma sorusu ve veri toplama planı yapar.",
                        "b) Aritmetik ortalama, ortanca, tepe değer ve açıklığı yorumlar.",
                    ],
                    "hook": "Basketbol takımının maç başı sayı dağılımının analizi.",
                    "kriz": "Uç değerin aritmetik ortalamayı nasıl etkilediğini yorumlamakta zorlanır.",
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1",
                    "cikti": "Bir olayın olasılığını deneysel gözleme dayalı tahmin edebilme",
                    "surec": [
                        "a) Deney tekrarlarının çıktılarını kaydeder.",
                        "b) Deneme sayısı arttıkça göreli sıklığın kararlılığını yorumlar.",
                    ],
                    "hook": "Madeni para atma deneyinde 10 atış ile 100 atış sonuçlarının karşılaştırılması.",
                    "kriz": "Kısa denemede üst üste aynı yüz gelince olasılığın değiştiğini sanır.",
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler",
            "3. Tema: Dönüşüm",
            "4. Tema: Geometrik Nicelikler (1)",
            "4. Tema: Geometrik Nicelikler (2)",
            "5. Tema: Geometrik Şekiller",
            "6. Tema: İstatistiksel Araştırma Süreci",
            "7. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {
                    "kod": "MAT.7.1.1",
                    "cikti": "Tam sayıları rasyonel sayılara genişletme ve sayı doğrusunda yorumlayabilme",
                    "surec": [
                        "a) Tam sayılar ve rasyonel sayıların sayı doğrusundaki konumlarını inceler.",
                        "b) Mutlak değer ve sıralama ilişkilerini yorumlar.",
                    ],
                    "hook": "Deniz seviyesi altı/üstü yükseklikler ve termometre okumaları.",
                    "kriz": "Negatif rasyonel sayıları sayı doğrusunda sıfıra uzaklığına göre yanlış sıralar.",
                },
                {
                    "kod": "MAT.7.1.4",
                    "cikti": "Rasyonel sayılarla işlemler içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Problemdeki sayı ve işlem bileşenlerini belirler.",
                        "b) Uygun stratejiyle çözer ve sonucun anlamlılığını kontrol eder.",
                    ],
                    "hook": "Aylık bütçe planlaması, gelir-gider ve kesirli paylaştırma.",
                    "kriz": "Negatif rasyonel sayılarda çarpma ve bölmenin işaret kuralında hata yapar.",
                },
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.7.1.5",
                    "cikti": "Gerçek yaşam durumları üzerinden oran ilişkileri hakkında muhakeme yapabilme",
                    "surec": [
                        "a) Toplamsal ve çarpımsal karşılaştırmaları ayırt eder.",
                        "b) Denk oran ve birim oran ilişkilerine dair çıkarım yapar.",
                    ],
                    "hook": "Harita ölçeği ve karışım tariflerindeki malzeme oranları.",
                    "kriz": "İki çokluk arasındaki farkı sabit tutarak oran kurmaya çalışır.",
                },
                {
                    "kod": "MAT.7.1.7",
                    "cikti": "Doğru ve ters orantılı durumlara ilişkin problemleri çözebilme",
                    "surec": [
                        "a) Nicelikler arasındaki değişim yönünü ve sabit oranı belirler.",
                        "b) Tablo, grafik ve orantı kurarak problemi çözer.",
                    ],
                    "hook": "Sabit hızla giden aracın süresi ile musluk sayısına göre havuz dolma süresi.",
                    "kriz": "Ters orantılı çokluklarda çarpım yerine bölüm sabiti kurmaya çalışır.",
                },
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.7.2.1",
                    "cikti": "Cebirsel ifadelerle işlemler yapma ve birinci dereceden bir bilinmeyenli denklem çözme",
                    "surec": [
                        "a) Durumdaki bilinmeyen ve ilişkileri cebirsel ifadeyle modeller.",
                        "b) Eşitliğin korunumu ilkesiyle denklemi çözüp yorumlar.",
                    ],
                    "hook": "Sabit açılış ücreti ve kullanım miktarına göre fatura modellemesi.",
                    "kriz": "Parantez önündeki eksi işaretini terimlere dağıtırken işaret hatası yapar.",
                }
            ],
            "3. Tema: Dönüşüm": [
                {
                    "kod": "MAT.7.3.1",
                    "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturmaya dair çıkarım yapabilme[span_0](start_span)[span_0](end_span)",
                    "surec": [
                        "a) Şekillerin yansıma dönüşümleri altındaki görüntülerini oluşturmaya dair varsayımlarda bulunur[span_1](start_span)[span_1](end_span).",
                        "b) Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturur[span_2](start_span)[span_2](end_span).",
                        "c) Varsayımlarını doğrulamaya yönelik karşılaştırmalar yapar[span_3](start_span)[span_3](end_span).",
                        "ç) Bir şekil ile yansıma dönüşümü altındaki görüntüsü arasındaki ilişkilere dair önermeler sunar[span_4](start_span)[span_4](end_span).",
                        "d) Önermenin verilen iki eş şeklin bir doğruya göre simetrik olup olmadığını belirlemeye ve simetrik bir şeklin simetri doğrusunu oluşturmaya yönelik katkısını değerlendirir[span_5](start_span)[span_5](end_span).",
                    ],
                    "hook": "Durgun göl yüzeyinde veya aynada oluşan simetrik yansımalar.",
                    "kriz": "Yansıma eksenine dik uzaklığı saymadan şekli doğrudan kaydırarak çizer.",
                },
                {
                    "kod": "MAT.7.3.2",
                    "cikti": "Yansıma dönüşümündeki deneyimlerini orta dikme ve açıortay inşasına yansıtabilme[span_6](start_span)[span_6](end_span)",
                    "surec": [
                        "a) Yansıma dönüşümünde simetri doğrusunun özelliklerini gözden geçirir[span_7](start_span)[span_7](end_span).",
                        "b) Simetri doğrusunun özelliklerinden hareketle bir doğru parçasına ait orta dikmenin ve bir açıya ait açıortayın inşasına dair çıkarım yapar[span_8](start_span)[span_8](end_span).",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir[span_9](start_span)[span_9](end_span).",
                    ],
                    "hook": "İki yerleşim noktasına eşit uzaklıktaki durak noktasının belirlenmesi.",
                    "kriz": "Orta dikme ile açıortay inşasındaki eş uzaklık özelliğini karıştırır.",
                },
            ],
            "4. Tema: Geometrik Nicelikler (1)": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": "Eş küplerle oluşturulan yapılar ile görünümleri arasındaki ilişkiyi çözümleyebilme[span_10](start_span)[span_10](end_span)",
                    "surec": [
                        "a) Eş küplerle oluşturulan yapıların farklı yönlerden görünümlerini çizer ve görünümleri verilen yapıları eş küplerle oluşturur[span_11](start_span)[span_11](end_span).",
                        "b) Oluşturduğu yapı ile görünümleri arasındaki ilişkileri belirler[span_12](start_span)[span_12](end_span).",
                    ],
                    "hook": "Mimari maketlerin önden, üstten ve sağdan görünüm çizimleri.",
                    "kriz": "Arka sırada kalan küplerin üstten ve yandan görünüme etkisini unutur.",
                },
                {
                    "kod": "MAT.7.4.2",
                    "cikti": "Dikdörtgenler prizmasının yüzey alanını yorumlayabilme[span_13](start_span)[span_13](end_span)",
                    "surec": [
                        "a) Dikdörtgenler prizmasının farklı yüzey açınımlarını inceler[span_14](start_span)[span_14](end_span).",
                        "b) Dikdörtgenler prizmasının yüzey açınımı ile yüzey alanı arasındaki ilişkileri ifade eder[span_15](start_span)[span_15](end_span).",
                        "c) Dikdörtgenler prizmalarının yüzey açınımlarından yararlanarak yüzey alanlarını hesaplar[span_16](start_span)[span_16](end_span).",
                    ],
                    "hook": "Hediye kutusunun tamamını kaplamak için gereken kâğıt alanının hesabı.",
                    "kriz": "Karşılıklı eş yüzlerden yalnızca birini hesaplayıp ikiyle çarpmayı unutur.",
                },
                {
                    "kod": "MAT.7.4.4",
                    "cikti": "Dikdörtgenler prizmasının hacim bağıntısını değerlendirebilme[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span)",
                    "surec": [
                        "a) Dikdörtgenler prizmasının hacmini belirlemede ölçüt olarak birim küpleri belirler[span_19](start_span)[span_19](end_span)[span_20](start_span)[span_20](end_span).",
                        "b) Dikdörtgenler prizmasının hacmini belirlemek için prizmaların içine yerleştirilen birim küpleri sayar[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span).",
                        "c) Toplam birim küp sayısı ile dikdörtgenler prizmasının ayrıt uzunluklarını karşılaştırır[span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span).",
                        "ç) Birim küpleri farklı stratejilerle sayarak dikdörtgenler prizmasının hacmini taban alanı ile yüksekliğin çarpımı olarak ifade eder[span_25](start_span)[span_25](end_span)[span_26](start_span)[span_26](end_span).",
                    ],
                    "hook": "Eş kolilerin dikdörtgen prizma biçimindeki depoya katman katman dizilmesi.",
                    "kriz": "Yüzey alanı ile hacim birimlerini ve bağıntılarını birbirine karıştırır.",
                },
                {
                    "kod": "MAT.7.4.5",
                    "cikti": "Hacim ölçme birimleri arasındaki ilişkileri değerlendirebilme[span_27](start_span)[span_27](end_span)",
                    "surec": [
                        "a) Bir cismin hacmini ölçmede metreküpü ve litreyi ölçüt olarak belirler[span_28](start_span)[span_28](end_span).",
                        "b) Metreküp ve litreyi kullanarak ölçme yapar[span_29](start_span)[span_29](end_span).",
                        "c) Hacim ölçme sonuçlarını desimetreküp, santimetreküp ve milimetreküp; sıvı ölçme sonuçlarını desilitre, santilitre ve mililitre ile ilişkilendirerek karşılaştırır[span_30](start_span)[span_30](end_span).",
                        "ç) Karşılaştırmalarına ilişkin yargıda bulunur[span_31](start_span)[span_31](end_span).",
                    ],
                    "hook": "Su deposunun metreküp kapasitesi ile litre cinsinden karşılığı.",
                    "kriz": "Hacim birimlerinde biner basamak dönüşümü yerine yüzer dönüşüm yapar.",
                },
            ],
            "4. Tema: Geometrik Nicelikler (2)": [
                {
                    "kod": "MAT.7.4.7",
                    "cikti": "Dikdörtgenin, paralelkenarın alanına ve çemberin uzunluğuna ilişkin deneyimlerini dairenin alan bağıntısına yansıtabilme[span_32](start_span)[span_32](end_span)",
                    "surec": [
                        "a) Dikdörtgenin, paralelkenarın alanı ve çemberin uzunluğuna yönelik deneyimlerini gözden geçirir[span_33](start_span)[span_33](end_span).",
                        "b) Dikdörtgenin alan bağıntısı ve çemberin uzunluğundan yola çıkarak dairenin alan bağıntısına yönelik çıkarım yapar[span_34](start_span)[span_34](end_span).",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir[span_35](start_span)[span_35](end_span).",
                    ],
                    "hook": "Dairesel dilimlere ayrılan dairenin paralelkenara dönüştürülmesi.",
                    "kriz": "Daire alanında yarıçapın karesi yerine çapı kullanır.",
                },
                {
                    "kod": "MAT.7.4.8",
                    "cikti": "Çemberde merkez açı ve gördüğü yay uzunluğu arasındaki ilişkiden yola çıkarak daire ve daire diliminin alanları arasındaki ilişkiye yönelik analojik akıl yürütebilme[span_36](start_span)[span_36](end_span)",
                    "surec": [
                        "a) Çemberde merkez açı ve gördüğü yay uzunluğu ile daire ve daire diliminin alanı arasındaki ilişkileri gözlemler[span_37](start_span)[span_37](end_span).",
                        "b) Çemberde merkez açı ve gördüğü yay uzunluğu ile daire ve daire diliminin alanı arasındaki ilişkiyi tespit eder[span_38](start_span)[span_38](end_span).",
                        "c) Çemberde merkez açı ve gördüğü yay uzunluğuyla daire ve daire diliminin alanı arasında kurulan ilişkiden hareketle daire diliminin alanına dair çıkarım yapar[span_39](start_span)[span_39](end_span).",
                    ],
                    "hook": "Dilimlere ayrılmış pizzada merkez açıya göre dilim alanının bulunması.",
                    "kriz": "Tam daire açısı olan 360 derece ile orantı kurmayı unutur.",
                },
                {
                    "kod": "MAT.7.4.9",
                    "cikti": "Eşkenar dörtgen ve yamuğun alan bağıntılarına dair çıkarım yapabilme[span_40](start_span)[span_40](end_span)[span_41](start_span)[span_41](end_span)",
                    "surec": [
                        "a) Dikdörtgen, paralelkenar ve üçgenin alan bağıntısına dair ön bilgisiyle eşkenar dörtgenin ve yamuğun alan hesabına yönelik varsayımda bulunur[span_42](start_span)[span_42](end_span)[span_43](start_span)[span_43](end_span).",
                        "b) Eşkenar dörtgeni ve yamuğu parçalayarak veya tamamlayarak oluşturduğu geometrik şekillerin alanlarını belirler[span_44](start_span)[span_44](end_span)[span_45](start_span)[span_45](end_span).",
                        "c) Oluşturulan geometrik şekillerin alanlarını varsayımlarıyla karşılaştırır[span_46](start_span)[span_46](end_span)[span_47](start_span)[span_47](end_span).",
                        "ç) Eşkenar dörtgenin ve yamuğun alan bağıntılarına dair önermeler sunar[span_48](start_span)[span_48](end_span)[span_49](start_span)[span_49](end_span).",
                        "d) Çeşitli geometrik şekillerin alanlarının hesaplanmasında eşkenar dörtgenin ve yamuğun alan bağıntılarının katkılarını değerlendirir[span_50](start_span)[span_50](end_span)[span_51](start_span)[span_51](end_span).",
                    ],
                    "hook": "Yamuk biçimindeki çatı yüzeyi ve eşkenar dörtgen karo kaplaması.",
                    "kriz": "Yamukta alt ve üst taban toplamını ikiye bölmeyi unutur.",
                },
            ],
            "5. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Matematiksel araç ve teknolojiden yararlanarak üçgende kenarortayı, açıortayı ve yüksekliği çözümleyebilme[span_52](start_span)[span_52](end_span)",
                    "surec": [
                        "a) Üçgende kenarortayı, açıortayı ve yüksekliği belirler[span_53](start_span)[span_53](end_span).",
                        "b) Üçgende kenarortay, açıortay ve yükseklik arasındaki ilişkileri belirler[span_54](start_span)[span_54](end_span).",
                    ],
                    "hook": "İkizkenar ve eşkenar üçgen çatılarda yardımcı elemanların çakışması.",
                    "kriz": "Geniş açılı üçgende yüksekliğin üçgenin dışına düşmesini anlamakta zorlanır.",
                },
                {
                    "kod": "MAT.7.5.2",
                    "cikti": "Orta dikme inşasına yönelik deneyimlerini üçgende kenarortay inşasına yansıtabilme[span_55](start_span)[span_55](end_span)",
                    "surec": [
                        "a) Orta dikme inşasına yönelik deneyimlerini gözden geçirir[span_56](start_span)[span_56](end_span).",
                        "b) Üçgende kenarortay inşasına yönelik çıkarım yapar[span_57](start_span)[span_57](end_span).",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir[span_58](start_span)[span_58](end_span).",
                    ],
                    "hook": "Üçgen bir parkın kenar orta noktaları ve merkez yaklaşımı.",
                    "kriz": "Kenarortay ile yüksekliği birbirine karıştırıp çizimde zorlanır.",
                },
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.7.6.1",
                    "cikti": "Kategorik veya nicel (sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme[span_59](start_span)[span_59](end_span)",
                    "surec": [
                        "a) Kategorik veya nicel (sürekli) veriye dayanan istatistiksel araştırma gerektiren durumları fark eder[span_60](start_span)[span_60](end_span).",
                        "b) Kategorik veya nicel (sürekli) veriye dayanan betimleme veya karşılaştırma gerektirebilecek araştırma soruları oluşturur[span_61](start_span)[span_61](end_span).",
                        "c) Kategorik veya nicel (sürekli) veriye ulaşmak için plan yapar[span_62](start_span)[span_62](end_span).",
                        "ç) Araştırma sorusuna uygun hazırlanan anket sorularını kullanarak veri toplar veya hazır veriye ulaşır[span_63](start_span)[span_63](end_span).",
                        "d) Veri görselleştirme (çizgi grafiği, nokta grafiği gibi) ve özetleme (aritmetik ortalama, ortanca, tepe değer, açıklık ve ortalama mutlak sapma) araçlarını seçme gerekçelerini belirtir[span_64](start_span)[span_64](end_span).",
                        "e) Toplanan veriyi uygun araçlarla analiz eder[span_65](start_span)[span_65](end_span).",
                        "f) Araştırmada ulaştığı sonuçlara yönelik gerekçeler sunar[span_66](start_span)[span_66](end_span).",
                        "g) Araştırma sonuçlarının araştırma sorusuna ne düzeyde cevap verdiğini değerlendirerek araştırma sürecine uygun olmayan adımları yeniden planlar[span_67](start_span)[span_67](end_span).",
                    ],
                    "hook": "Haftalık hava sıcaklığı ve boy uzunluğu değişim verilerinin analizi.",
                    "kriz": "Sürekli veri ile kesikli veriye uygun grafik türünü karıştırır.",
                },
                {
                    "kod": "MAT.7.6.2",
                    "cikti": "Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme[span_68](start_span)[span_68](end_span)",
                    "surec": [
                        "a) Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç veya yorumlara yönelik istatistiksel temellendirme yapar[span_69](start_span)[span_69](end_span).",
                        "b) Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç veya yorumlara yönelik hataları ya da yanlılıkları tespit eder[span_70](start_span)[span_70](end_span).",
                        "c) Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç veya yorumları çürütür ya da kabul eder[span_71](start_span)[span_71](end_span).",
                    ],
                    "hook": "Haber ve reklamlarda sunulan grafiklerin eksen ve ölçek yanlılıklarını inceleme.",
                    "kriz": "Grafikteki yanlılığı fark etmeden sunulan yorumu doğrudan kabul eder.",
                },
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.7.7.1",
                    "cikti": "Bir olayın ve tümleyeninin olasılığına ilişkin tümevarımsal akıl yürütebilme[span_72](start_span)[span_72](end_span)",
                    "surec": [
                        "a) Bir olayın olasılığını hesaplamaya ilişkin olası tüm çıktıları gözlemler[span_73](start_span)[span_73](end_span).",
                        "b) Bir olayın ve tümleyeninin olasılığını hesaplamak için matematiksel ilişkiyi bulur[span_74](start_span)[span_74](end_span).",
                        "c) Bir olayın ve tümleyeninin olasılığının ilişkisine yönelik genelleme yapar[span_75](start_span)[span_75](end_span).",
                    ],
                    "hook": "Hedef tahtasında isabet etme ile isabet etmeme olasılıkları toplamı.",
                    "kriz": "Tümleyen olasılığını 1'den çıkarmak yerine doğrudan olay sayısını yazar.",
                },
                {
                    "kod": "MAT.7.7.2",
                    "cikti": "Aynı deneye ait olayların eşit olasılıklı olma durumlarını değerlendirebilme[span_76](start_span)[span_76](end_span)",
                    "surec": [
                        "a) Eşit olasılıklı olan ve eşit olasılıklı olmayan olaylara ilişkin ölçüt belirler[span_77](start_span)[span_77](end_span).",
                        "b) Olayların eşit olasılıklı olma veya olmama olasılığına ilişkin hesaplama yapar[span_78](start_span)[span_78](end_span).",
                        "c) Hesaplama sonuçlarını belirlediği ölçütlerle karşılaştırır[span_79](start_span)[span_79](end_span).",
                        "ç) Karşılaştırmalarına ilişkin yargıda bulunur[span_80](start_span)[span_80](end_span).",
                    ],
                    "hook": "Farklı sayılarda renkli kart bulunan torbadan çekiliş durumları.",
                    "kriz": "Çıktı sayıları farklı olduğu halde olayları eşit olasılıklı sanır.",
                },
                {
                    "kod": "MAT.7.7.3",
                    "cikti": "Olayları ayrık olma ve ayrık olmama durumlarına göre sınıflandırabilme[span_81](start_span)[span_81](end_span)",
                    "surec": [
                        "a) Olayların ayrık olma ve ayrık olmama durumlarını olaylara ait çıktıların ortak olup olmamasını ölçüt alarak belirler[span_82](start_span)[span_82](end_span).",
                        "b) Olayları ayrık olma ve ayrık olmama durumuna göre ayrıştırır[span_83](start_span)[span_83](end_span).",
                        "c) Ayrık olan ve ayrık olmayan olayları tasnif eder[span_84](start_span)[span_84](end_span).",
                        "ç) Olayları ayrık olma veya olmama durumuna göre etiketler[span_85](start_span)[span_85](end_span).",
                    ],
                    "hook": "Tek zar atışında 'çift gelmesi' ile 'asal gelmesi' olaylarının kesişimi.",
                    "kriz": "Ortak çıktısı bulunan olayları ayrık olay sanarak sınıflandırır.",
                },
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Cebirsel Düşünme ve Değişimler",
            "3. Tema: Geometrik Şekiller",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: Dönüşüm",
            "6. Tema: İstatistiksel Araştırma Süreci",
            "7. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.1",
                    "cikti": "Farklı bağlamlardaki üslü ifadelere, özelliklerine ve üslü ifadelerle yapılan işlemlere ilişkin çıkarım yapabilme[span_86](start_span)[span_86](end_span)",
                    "surec": [
                        "a) Karşılaştığı bağlamlardaki üslü ifadeler, özellikleri ve üslü ifadelerle yapılan işlemlere yönelik varsayımlarda bulunur[span_87](start_span)[span_87](end_span).",
                        "b) Üslü ifadeleri, özelliklerini ve üslü ifadelerle yapılan işlemleri inceleyerek genellemeleri belirler[span_88](start_span)[span_88](end_span).",
                        "c) Ulaştığı genellemelerin varsayımını karşılayıp karşılamadığını örnekler ve çeşitli temsiller (şekil ve tablo gibi) ile sınar[span_89](start_span)[span_89](end_span).",
                        "ç) Üslü ifadelere, özelliklere ve üslü ifadelerle işlem yapmaya ilişkin önermeleri sözel ve cebirsel olarak ifade eder[span_90](start_span)[span_90](end_span).",
                        "d) Sunduğu önermelerin matematiksel süreçlere katkısını sözel olarak açıklar[span_91](start_span)[span_91](end_span).",
                    ],
                    "hook": "Mikroorganizmaların belirli zaman aralıklarında ikiye katlanarak çoğalması.",
                    "kriz": "Üslü ifadelerde çarpma yaparken tabanlar eşitken üstleri toplamak yerine çarpar.",
                },
                {
                    "kod": "MAT.8.1.2",
                    "cikti": "Karşılaştığı problem durumlarında kareköklü ifadeler ile ilgili muhakeme yapabilme[span_92](start_span)[span_92](end_span)[span_93](start_span)[span_93](end_span)",
                    "surec": [
                        "a) Bir karenin alanı ile kenar uzunluğu arasındaki ilişkiyi belirler[span_94](start_span)[span_94](end_span)[span_95](start_span)[span_95](end_span).",
                        "b) Karenin alanından hareketle tam kare pozitif tam sayılar ile kareköklerini ilişkilendirir[span_96](start_span)[span_96](end_span)[span_97](start_span)[span_97](end_span).",
                        "c) Tam kare olmayan pozitif bir sayının karekökünün hangi iki doğal sayı arasında olduğunu ve yaklaşık değerini matematiksel temsillerle (sayı doğrusu, şekil, tablo gibi) ifade eder[span_98](start_span)[span_98](end_span)[span_99](start_span)[span_99](end_span).",
                        "ç) Bir sayının karekökünü kendi ifadeleri ile açıklar[span_100](start_span)[span_100](end_span)[span_101](start_span)[span_101](end_span).",
                    ],
                    "hook": "Alanı 50 metrekare olan kare biçimindeki odanın kenar uzunluğunun kestirilmesi.",
                    "kriz": "Tam kare olmayan bir sayının karekökünü bulurken sayıyı ikiye bölmeye çalışır.",
                },
                {
                    "kod": "MAT.8.1.3",
                    "cikti": "Sayıların rasyonel ya da irrasyonelliğini değerlendirebilme[span_102](start_span)[span_102](end_span)[span_103](start_span)[span_103](end_span)",
                    "surec": [
                        "a) Sayıların rasyonel ya da irrasyonel sayılar olup olmadığına ilişkin ondalık gösterimlerini ölçüt olarak belirler[span_104](start_span)[span_104](end_span)[span_105](start_span)[span_105](end_span).",
                        "b) Sayıların ondalık gösterimlerini bölme işlemi ya da hesap makinesi kullanarak elde eder[span_106](start_span)[span_106](end_span)[span_107](start_span)[span_107](end_span).",
                        "c) Elde ettiği ondalık gösterimi ölçütü ile karşılaştırır[span_108](start_span)[span_108](end_span)[span_109](start_span)[span_109](end_span).",
                        "ç) Karşılaştırmalarından hareketle bir sayının rasyonel olup olmadığına yönelik yargıda bulunur[span_110](start_span)[span_110](end_span)[span_111](start_span)[span_111](end_span).",
                    ],
                    "hook": "Pi sayısı, kök 2 ve devirli ondalık sayıların ondalık açılımlarının incelenmesi.",
                    "kriz": "Devirli ondalık sayıları sonsuza gittiği için irrasyonel sanır.",
                },
                {
                    "kod": "MAT.8.1.4",
                    "cikti": "Gerçek sayıları ve aralıklarını sayı doğrusunda yorumlayabilme[span_112](start_span)[span_112](end_span)[span_113](start_span)[span_113](end_span)",
                    "surec": [
                        "a) Doğal sayılardan başlamak üzere tüm gerçek sayıları ve sayılar arası ilişkileri inceler[span_114](start_span)[span_114](end_span).",
                        "b) Gerçek sayıları sayı doğrusuna yerleştirir[span_115](start_span)[span_115](end_span).",
                        "c) Gerçek sayı aralıkları arasındaki ilişkiyi açıklar[span_116](start_span)[span_116](end_span).",
                    ],
                    "hook": "Sıcaklık ve hız limitlerindeki açık/kapalı aralık gösterimleri.",
                    "kriz": "Sayı kümelerinin kapsama ilişkisini kurmakta zorlanır.",
                },
            ],
            "2. Tema: Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": "Gerçek yaşam durumları üzerinden dik koordinat sistemini çözümleyebilme[span_117](start_span)[span_117](end_span)",
                    "surec": [
                        "a) Dik koordinat sisteminin bileşenlerini (düzlem, eksenler, sayı ikilileri gibi) belirler[span_118](start_span)[span_118](end_span).",
                        "b) Dik koordinat sisteminde bileşenler arasındaki ilişkileri belirler[span_119](start_span)[span_119](end_span).",
                    ],
                    "hook": "Harita ve oyun düzleminde referans noktasına göre konum belirleme.",
                    "kriz": "Sıralı ikilide yatay ve dikey eksenlerin yerini karıştırır.",
                },
                {
                    "kod": "MAT.8.2.2",
                    "cikti": "Gerçek yaşam durumlarındaki doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme[span_120](start_span)[span_120](end_span)",
                    "surec": [
                        "a) Doğrusal fonksiyonların cebirsel, tablo ve grafik temsillerini tanır[span_121](start_span)[span_121](end_span).",
                        "b) Gerçek yaşam durumlarındaki doğrusal ilişkileri incelemek için doğrusal fonksiyonların temsillerinden uygun olanını belirler[span_122](start_span)[span_122](end_span).",
                        "c) Belirlediği temsili gerçek yaşam durumunu modellemek veya problemi çözmek için gerektiğinde temsiller arası geçiş yaparak kullanır[span_123](start_span)[span_123](end_span).",
                        "ç) Kullandığı temsilin problem durumuna uygunluğunu değerlendirir[span_124](start_span)[span_124](end_span).",
                        "d) Aynı durumda kullanılabilecek farklı temsilleri ekonomiklik ve kullanışlılık açısından karşılaştırır[span_125](start_span)[span_125](end_span).",
                        "e) Karşılaştırdığı temsillerin ekonomikliğine ve kullanışlılığına ilişkin karar verir[span_126](start_span)[span_126](end_span).",
                    ],
                    "hook": "Taksimetre açılış ücreti ve gidilen kilometreye göre ücret grafiği.",
                    "kriz": "Doğrusal ilişkideki sabit değişim oranını yorumlamakta zorlanır.",
                },
                {
                    "kod": "MAT.8.2.3",
                    "cikti": "Dik koordinat sisteminde iki doğrusal fonksiyonun birbirine göre durumuna ilişkin çıkarım yapabilme[span_127](start_span)[span_127](end_span)",
                    "surec": [
                        "a) Dik koordinat sisteminde iki doğrusal fonksiyonun birbirine göre durumuna ilişkin varsayım oluşturur[span_128](start_span)[span_128](end_span).",
                        "b) Dik koordinat sisteminde farklı doğrusal fonksiyonların birbirlerine göre durumlarını inceleyerek genellemeler yapar[span_129](start_span)[span_129](end_span).",
                        "c) Genellemeleri ile varsayımlarını karşılaştırır[span_130](start_span)[span_130](end_span).",
                        "ç) Bulmuş olduğu ilişkilere yönelik önermeler sunar[span_131](start_span)[span_131](end_span).",
                        "d) Dik koordinat sisteminde verilen doğruların konumlarını değerlendirir[span_132](start_span)[span_132](end_span).",
                    ],
                    "hook": "İki farklı abonelik paketinin maliyet doğrularının kesişimi.",
                    "kriz": "Eğimleri eşit iki doğrunun paralel olduğunu grafikte fark edemez.",
                },
                {
                    "kod": "MAT.8.2.4",
                    "cikti": "Doğrusal fonksiyonlara ilişkin problemlerin çözümlerini algoritma ifade yöntemlerini kullanarak yapılandırabilme",
                    "surec": [
                        "a) Doğrusal fonksiyonlara ilişkin problemlerin çözümlerindeki adımları ve ilişkileri açıklar.",
                        "b) Algoritma ifade yöntemlerini kullanarak incelediği adımlar ve ilişkilerden uyumlu bir bütün oluşturur.",
                    ],
                    "hook": "Sabit ücret ve birim maliyet hesabının adım adım çözüm algoritmasına dönüştürülmesi.",
                    "kriz": "Çözüm adımlarının sıralamasını kurarken koşul ve işlem adımlarını karıştırır.",
                },
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": "Matematiksel araç ve teknoloji yardımıyla üçgenin kenarları ve açıları arasındaki ilişkiyi yorumlayabilme",
                    "surec": [
                        "a) Üçgenin kenar ve açı özelliklerini inceler.",
                        "b) Üçgenin kenar uzunluklarının büyüklüğüne göre açıların ölçülerini, açıların ölçülerinin büyüklüğüne göre kenar uzunluklarını sıralar.",
                        "c) Üçgenin kenar uzunlukları ve açı ölçüleri arasındaki ilişkiyi ifade eder.",
                    ],
                    "hook": "Açılan rampanın eğimi ile karşısındaki kenar uzunluğunun değişimi.",
                    "kriz": "Büyük açının karşısında büyük kenar bulunduğunu ters yorumlar.",
                },
                {
                    "kod": "MAT.8.3.2",
                    "cikti": "Matematiksel araç ve teknoloji yardımıyla üçgenin kenar uzunlukları arasındaki ilişkiye yönelik çıkarım yapabilme",
                    "surec": [
                        "a) Üçgen oluşturabilen üç doğru parçasının uzunluklarına dair varsayımda bulunur.",
                        "b) Varsayımda bulunduğu doğru parçaları ile oluşturduğu üçgenleri listeler.",
                        "c) Üçgen oluşturan doğru parçalarının uzunlukları ile varsayımlarını karşılaştırır.",
                        "ç) Üçgen oluşturan doğru parçalarının uzunlukları arasındaki ilişkiye dair önerme sunar.",
                        "d) Sunduğu önermenin katkısına yönelik gerekçeler sunar.",
                    ],
                    "hook": "Üç farklı çubuk parçasından üçgen çerçeve oluşturulup oluşturulamayacağı.",
                    "kriz": "İki kenarın toplamının üçüncü kenara eşit olduğu durumda üçgen oluşacağını sanır.",
                },
                {
                    "kod": "MAT.8.3.5",
                    "cikti": "Kenar uzunlukları a^2 + b^2 = c^2 eşitliğini sağlayan üçgenleri oluşturarak dik üçgen olduklarını; dik üçgenlerde dik kenar uzunluklarının kareleri toplamının hipotenüs uzunluğunun karesine eşit olduğunu yorumlayabilme",
                    "surec": [
                        "a) a^2 + b^2 = c^2 eşitliğini sağlayan rasyonel sayıları inceler.",
                        "b) Kenar uzunlukları a^2 + b^2 = c^2 eşitliğini sağlayan üçgeni oluşturarak dik üçgen olduğunu; dik üçgenlerde hipotenüs uzunluğunun karesinin diğer iki kenarın uzunluklarının kareleri toplamına eşit olduğunu belirler.",
                        "c) Pisagor bağıntısını üçgende açı-kenar ilişkisi ve üçgen eşitsizliği ile ilişkilendirerek dar açılı ve geniş açılı üçgenlerdeki kenar uzunluklarının ilişkisini ifade eder.",
                    ],
                    "hook": "Duvara dayalı merdivenin eriştiği yükseklik ve taban uzaklığı hesabı.",
                    "kriz": "Hipotenüsü dik kenarlarla karıştırıp toplama yerine çıkarma yapar.",
                },
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1",
                    "cikti": "Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve dik dairesel koninin yüzey açınımlarını çözümleyebilme",
                    "surec": [
                        "a) Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve dik dairesel koninin yüzey açınımlarında yer alan şekilleri belirler.",
                        "b) Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve dik dairesel koninin yüzey açınımlarında yer alan şekiller arasındaki ilişkileri belirler.",
                    ],
                    "hook": "Silindir ve piramit biçimindeki ambalaj kutularının karton açınımları.",
                    "kriz": "Silindirin yanal dikdörtgen kenarının taban çevresine eşit olduğunu göremez.",
                },
                {
                    "kod": "MAT.8.4.2",
                    "cikti": "Dik dairesel silindirin yüzey açınımına ilişkin deneyimlerini dik dairesel silindirin yüzey alanına yansıtabilme",
                    "surec": [
                        "a) Dik dairesel silindirin yüzey açınımına ilişkin deneyimlerini gözden geçirir.",
                        "b) Dik dairesel silindirin yüzey alanına yönelik çıkarım yapar.",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir.",
                    ],
                    "hook": "Silindirik kutunun taban ve yanal yüzeyini kaplamak için gereken malzeme alanı.",
                    "kriz": "Taban dairesinden iki tane bulunduğunu veya yanal kenar uzunluğunu gözden kaçırır.",
                },
                {
                    "kod": "MAT.8.4.3",
                    "cikti": "Dairenin alan bağıntısının oluşturulma sürecinden hareketle dik dairesel silindirin hacim bağıntısına yönelik analojik akıl yürütebilme",
                    "surec": [
                        "a) Dairenin alan bağıntısının oluşturulma sürecini ve daire ile dik dairesel silindir arasındaki ilişkiyi gözden geçirir.",
                        "b) Dairenin alan bağıntısının oluşturulma süreci ile dik dairesel silindirin hacim bağıntısının oluşturulma süreci arasındaki ilişkileri belirler.",
                        "c) İlişkilerden hareketle dik dairesel silindirin hacmine yönelik çıkarım yapar.",
                    ],
                    "hook": "Silindirik su deposunun alabileceği su hacminin hesaplanması.",
                    "kriz": "Silindirin hacmi ile yanal alan formüllerini birbirine karıştırır.",
                },
            ],
            "5. Tema: Dönüşüm": [
                {
                    "kod": "MAT.8.5.1",
                    "cikti": "Matematiksel araç ve teknoloji yardımıyla öteleme dönüşümünü çözümleyebilme",
                    "surec": [
                        "a) Matematiksel araç ve teknoloji yardımıyla düzlemde geometrik şekillerin öteleme dönüşümü altındaki görüntülerinin kenar ve açı özelliklerini belirler.",
                        "b) Geometrik şekiller ile öteleme dönüşümü altındaki görüntüleri arasındaki ilişkileri belirler.",
                    ],
                    "hook": "Bir şeklin yönü ve boyutu değişmeden düzlemde kaydırılması.",
                    "kriz": "Öteleme sonrasında şeklin yönünün veya boyutunun değişeceğini düşünür.",
                },
                {
                    "kod": "MAT.8.5.2",
                    "cikti": "Dik koordinat sisteminde geometrik şekillere ait noktaların apsis ve ordinatlarının öteleme dönüşümündeki değişimlerine ve eksenlere göre yansıma dönüşümündeki değişimlerine ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) Geometrik şekillere ait noktaların apsis ve ordinatlarının öteleme dönüşümündeki değişimlerine ve eksenlere göre yansıma dönüşümündeki değişimlerine dair varsayımlarda bulunur.",
                        "b) Geometrik şekillerin öteleme dönüşümü altındaki görüntülerini ve koordinat eksenlerine göre yansıma dönüşümü altındaki görüntülerini oluşturur.",
                        "c) Oluşturduğu görüntülere ait noktaların apsis ve ordinatlarını varsayımları ile karşılaştırır.",
                        "ç) Geometrik şekillere ait noktaların apsis ve ordinatlarının öteleme dönüşümündeki değişimlerine ve koordinat eksenlerine göre yansıma dönüşümündeki değişimlerine dair önermeler sunar.",
                        "d) Sundukları önermelerinin dik koordinat sisteminde konumları verilen iki geometrik şekil arasında öteleme veya eksenlere göre yansıma dönüşümüne dayalı bir ilişkinin bulunup bulunmadığını incelemeye sağladığı katkıyı değerlendirir.",
                    ],
                    "hook": "Dijital oyun sahnesinde karakterin koordinat eksenlerine göre hareketi.",
                    "kriz": "Eksenlere göre yansımada hangi koordinatın işaretinin değişeceğini karıştırır.",
                },
                {
                    "kod": "MAT.8.5.3",
                    "cikti": "Öteleme ve yansıma dönüşümlerini içeren problemleri çözebilme",
                    "surec": [
                        "a) Öteleme ve yansıma dönüşümlerine ilişkin problemlerde ilgili matematiksel bileşenleri (eşlik, uzaklık, diklik, paralellik, koordinatlar gibi) belirler.",
                        "b) Matematiksel bileşenler arasındaki ilişkileri belirler.",
                        "c) Problem bağlamındaki temsilleri farklı temsillere dönüştürür.",
                        "ç) Matematiksel temsillere dönüştürdüğü problemi kendi ifadeleri ile açıklar.",
                        "d) Öteleme ve yansıma dönüşümlerini içeren problemlerin sonucuna ilişkin tahminde bulunur ve işlemleri gerçekleştirmek için stratejiler geliştirir.",
                        "e) Belirlenen stratejileri çözüm için uygular.",
                    ],
                    "hook": "Ardışık öteleme ve yansıma adımlarını içeren tasarım örüntüleri.",
                    "kriz": "Ardışık dönüşüm probleminde ilk dönüşümün görüntüsünü ikinci dönüşüme temel almayı unutur.",
                },
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.8.6.1",
                    "cikti": "Kategorik veya nicel (kesikli-sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme",
                    "surec": [
                        "a) Kategorik veya nicel (kesikli-sürekli) veriye dayanan istatistiksel araştırma gerektiren durumları fark eder.",
                        "b) Kategorik veya nicel (kesikli-sürekli) veriye dayanan betimleme veya karşılaştırma gerektirebilecek araştırma soruları oluşturur.",
                        "c) Kategorik veya nicel (kesikli-sürekli) veriye ulaşmak için plan yapar.",
                        "ç) Araştırma sorusuna uygun hazırlanan anket sorularını kullanarak veri toplar veya hazır veriye ulaşır.",
                        "d) Veri görselleştirme (çizgi grafiği, nokta grafiği gibi) ve özetleme (aritmetik ortalama, ortanca, tepe değer, açıklık veya ortalama mutlak sapma) araçlarını seçme gerekçelerini belirtir.",
                        "e) Toplanan veriyi uygun araçlarla analiz eder.",
                        "f) Araştırmada ulaştığı sonuçlara yönelik gerekçeler sunar.",
                        "g) Araştırma sonuçlarının araştırma sorusuna ne düzeyde cevap verdiğini değerlendirerek araştırma sürecine uygun olmayan adımları yeniden planlar.",
                    ],
                    "hook": "İki şubenin deneme sınavı dağılımlarının merkez ve yayılım ölçülerine göre kıyası.",
                    "kriz": "Veri dağılımını yorumlarken yalnızca ortalamaya bakıp yayılımı ihmal eder.",
                },
                {
                    "kod": "MAT.8.6.2",
                    "cikti": "Başkaları tarafından oluşturulan kategorik veya nicel (kesikli-sürekli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme",
                    "surec": [
                        "a) Başkaları tarafından oluşturulan kategorik veya nicel (kesikli-sürekli) veriye dayalı istatistiksel sonuç veya yorumlara yönelik istatistiksel temellendirme yapar.",
                        "b) Başkaları tarafından oluşturulan kategorik veya nicel (kesikli-sürekli) veriye dayalı istatistiksel sonuç veya yorumlara yönelik hataları ya da yanlılıkları tespit eder.",
                        "c) Başkaları tarafından oluşturulan kategorik veya nicel (kesikli-sürekli) veriye dayalı istatistiksel sonuç veya yorumları çürütür ya da kabul eder.",
                    ],
                    "hook": "Farklı veri setleri üzerinden yapılan istatistiksel iddiaların kanıtla sorgulanması.",
                    "kriz": "Veri dağılımındaki sapma ve açıklığı dikkate almadan genellemeyi doğrudan kabul eder.",
                },
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1",
                    "cikti": "Gerçek yaşamda karşılaşabileceği bir olayın olasılığına ilişkin farklı olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı belirleyerek karar verebilme",
                    "surec": [
                        "a) Bir olayın olasılığına ilişkin karar vermeye yönelik amacı belirler.",
                        "b) Karara ilişkin bilgi toplar.",
                        "c) Karara ilişkin olasılık yaklaşımlarına yönelik önermeler oluşturur.",
                        "ç) Karara ilişkin oluşturduğu önermeleri sorgular.",
                        "d) Ulaştığı sonuca göre olasılık yaklaşımlarına ilişkin seçim yapar.",
                        "e) Olasılık yaklaşımına ilişkin seçimini verdiği karara yansıtır.",
                    ],
                    "hook": "Penaltı atışı, zar deneyi ve hava tahmini durumlarında olasılık yaklaşımı seçimi.",
                    "kriz": "Deneysel veriyle tahmin edilmesi gereken durumda öznel tahmine yönelir.",
                }
            ],
        },
    },
}
# ==========================================
# 4. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.markdown('<span class="rozet">ADIM 1 / 3</span>', unsafe_allow_html=True)
    st.subheader("📝 2024 Türkiye Yüzyılı Maarif Modeli Kurulum ve Rubrik Paneli")
    st.info("Zorunlu aday bilgilerini ve danışman öğretim elemanının rubriğini doldurmadan sonraki adıma geçilemez.")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">Aday ve Danışman Bilgileri</div>', unsafe_allow_html=True)
        ogretmen_adi = st.text_input("Öğretmen Adayı Adı Soyadı *", placeholder="Örn: Mislina Taysi")
        okul_numarasi = st.text_input("Okul Numarası *", placeholder="Örn: 20220000000")
        universite_adi = st.text_input("Üniversite Adı *", value="Kahramanmaraş Sütçü İmam Üniversitesi")
        fakulte_bolum = st.text_input(
            "Fakülte ve Bölüm *",
            value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
        )
        uygulama_ogretim_elemani = st.text_input(
            "Uygulama Öğretim Elemanı *",
            placeholder="Örn: Dr. Öğr. Üyesi ...",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">Rubrik ve Sınıf Yapısı</div>', unsafe_allow_html=True)
        rubrik_dosya = st.file_uploader(
            "Rubrik Dosyası (PDF, Word, Metin)",
            type=["pdf", "docx", "txt"],
        )
        rubrik_metni = st.text_area(
            "Rubrik Kriterleri *",
            value=(
                "1. 3D sınıf ortamında kriz yönetimi ve öğrenci profillerine duyarlı iletişim (30 Puan).\n"
                "2. Pedagojik eylem sırasının tutarlılığı ve kapsayıcı hitabet (30 Puan).\n"
                "3. 2024 Türkiye Yüzyılı Maarif Modeli öğrenme çıktısı ve süreç bileşenleri uyumu (20 Puan).\n"
                "4. Özgün veya seçilen materyalin tanıtımı, kullanımı ve sahada aksiyon alma başarısı (20 Puan)."
            ),
            height=115,
        )
        sinif_mevcudu = st.slider("Sınıf Mevcudu", min_value=12, max_value=35, value=25)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 3D Staj Simülasyonunu Başlat", type="primary", use_container_width=True):
        if not all([
            ogretmen_adi.strip(),
            okul_numarasi.strip(),
            universite_adi.strip(),
            fakulte_bolum.strip(),
            uygulama_ogretim_elemani.strip(),
            rubrik_metni.strip(),
        ]):
            st.error("❌ Tüm zorunlu (*) alanlar doldurulmadan 2. adıma geçilemez.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi.strip()
            st.session_state.okul_numarasi = okul_numarasi.strip()
            st.session_state.universite_adi = universite_adi.strip()
            st.session_state.fakulte_bolum = fakulte_bolum.strip()
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani.strip()
            st.session_state.rubrik_metni = rubrik_metni.strip()
            st.session_state.sinif_mevcudu = sinif_mevcudu
            st.session_state.adim = 2
            st.rerun()

# ==========================================
# 5. ADIM 2: 3D GÖRSEL SINIF, ONAY KUTULU ÖĞRENCİ SEÇİMİ VE MÜDAHALE
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    okul_no = st.session_state.get("okul_numarasi", "N/A")
    universite = st.session_state.get("universite_adi", "Üniversite")
    ogretim_elemani = st.session_state.get("uygulama_ogretim_elemani", "Öğretim Elemanı")

    st.markdown('<span class="rozet">ADIM 2 / 3</span>', unsafe_allow_html=True)
    st.markdown(f"### 🏫 3D Canlı Sınıf & Sesli Etkileşim | {ogretmen} ({okul_no}) — {universite}")

    with st.expander("📚 2024 Türkiye Yüzyılı Maarif Modeli Sınıf, Tema, Kazanım ve Süreç Bileşeni Seçimi", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            secilen_sinif = st.selectbox("Sınıf Düzeyi *", list(tyym_master_arsiv.keys()))
        with col_s2:
            secilen_tema = st.selectbox("Tema *", tyym_master_arsiv[secilen_sinif]["Temalar"])
        kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"].get(secilen_tema, [])
        if not kazanim_listesi:
            st.error("❌ Bu tema için kazanım bulunamadı.")
            st.stop()
        with col_s3:
            kazanim_secenekleri = ["Seçiniz..."] + [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
            secilen_kazanim_str = st.selectbox("Öğrenme Çıktısı / Kazanım *", kazanim_secenekleri)

        if secilen_kazanim_str == "Seçiniz...":
            st.warning("Süreç bileşenine ve öğrenci seçimine geçmek için önce bir kazanım seçiniz.")
            st.stop()

        secilen_kazanim_obj = next(
            k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str
        )
        surec_secenekleri = ["Seçiniz..."] + secilen_kazanim_obj["surec"]
        secilen_surec = st.selectbox("Süreç Bileşeni *", surec_secenekleri)

        if secilen_surec == "Seçiniz...":
            st.warning("Öğrenci seçimi ve kriz müdahalesine geçmek için süreç bileşeni seçiniz.")
            st.stop()

        st.success(f"💡 **Günlük Yaşam Bağlamı:** {secilen_kazanim_obj['hook']}")

    # Onay kutulu (checkbox) çoklu öğrenci seçimi (1-10 arası)
    st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
    st.markdown('<div class="baslik-mavi">👥 Sınıftaki Öğrencileri Seçin * (1 ile 10 Arası İstediğiniz Öğrenciyi İşaretleyin)</div>', unsafe_allow_html=True)

    ogrenci_adlari = list(ogrenci_profilleri.keys())
    secili_liste = []

    cb_satir1 = st.columns(5)
    for idx in range(5):
        ad = ogrenci_adlari[idx]
        bilgi = ogrenci_profilleri[ad]
        with cb_satir1[idx]:
            with st.container(border=True):
                secili = st.checkbox(
                    f"{bilgi['ikon']} {ad}",
                    value=(ad in st.session_state.secili_ogrenciler),
                    key=f"cb_ogr_{ad}",
                )
                st.caption(bilgi["durum"])
                if secili:
                    secili_liste.append(ad)

    cb_satir2 = st.columns(5)
    for idx in range(5, 10):
        ad = ogrenci_adlari[idx]
        bilgi = ogrenci_profilleri[ad]
        with cb_satir2[idx - 5]:
            with st.container(border=True):
                secili = st.checkbox(
                    f"{bilgi['ikon']} {ad}",
                    value=(ad in st.session_state.secili_ogrenciler),
                    key=f"cb_ogr_{ad}",
                )
                st.caption(bilgi["durum"])
                if secili:
                    secili_liste.append(ad)

    st.session_state.secili_ogrenciler = secili_liste
    st.markdown('</div>', unsafe_allow_html=True)

    if not secili_liste:
        st.error("❌ En az 1 öğrenci seçilmeden müdahale ve raporlama aşamasına geçilemez.")
        st.stop()

    st.info(f"👨‍🏫 **Gözlemci:** {ogretim_elemani} | **Seçili Öğrenci Sayısı:** {len(secili_liste)} / 10")

    # Seçili Öğrencilerin Bağlamsal AI Davranış Kartları
    st.markdown("#### 🧠 Seçili Öğrencilerin Aktif Kazanım ve Süreç Bileşenine Göre AI Davranışları")
    kart_sutunlari = st.columns(min(len(secili_liste), 3))
    baslangic_davranislari = {}

    for idx, ogr_ad in enumerate(secili_liste):
        ogr_bilgi = ogrenci_profilleri[ogr_ad]
        davranis = ai_profil_davranisi_uret(
            ogr_ad,
            secilen_sinif,
            secilen_tema,
            secilen_kazanim_obj["kod"],
            secilen_kazanim_obj["cikti"],
            secilen_surec,
            secilen_kazanim_obj["kriz"],
        )
        baslangic_davranislari[ogr_ad] = davranis
        with kart_sutunlari[idx % len(kart_sutunlari)]:
            with st.container(border=True):
                st.markdown(f"**{ogr_bilgi['ikon']} {ogr_ad}** — *{ogr_bilgi['durum']}*")
                st.caption(f"Mimik: {ogr_bilgi['mimik']}")
                st.write(davranis)

    st.divider()
    col_sol, col_sag = st.columns([1.2, 0.8], gap="large")

    with col_sol:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">🎙️ Öğretmen Adayı Müdahale, Pedagojik Eylem Sırası ve Materyal Konsolu</div>', unsafe_allow_html=True)

        sesli_kayit = None
        try:
            sesli_kayit = st.audio_input("🎤 Mikrofonla Sesli Tepkinizi Kaydedin")
        except Exception:
            st.caption("Mikrofon bu tarayıcıda desteklenmiyorsa yazılı alanı kullanabilirsiniz.")

        sesli_girdi_manuel = st.text_area(
            "✍️ Sesli Hitabet / Öğrencilere Söyleyeceğiniz Sözler *",
            placeholder="Seçtiğiniz öğrencilerin düzeyine ve özel gereksinimlerine uygun hitabınızı yazın...",
            height=85,
        )

        eylem_1 = st.selectbox("1. Pedagojik Eylem Adımı *", EYLEM_1_SECENEKLER)
        eylem_2 = st.selectbox("2. Pedagojik Eylem Adımı *", EYLEM_2_SECENEKLER)
        secilen_materyal = st.selectbox("Materyal Seçimi *", MATERYAL_SECENEKLER)

        ozgun_materyal_adi = ""
        ozgun_materyal_tanitim = ""
        if secilen_materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal":
            ozgun_materyal_adi = st.text_input(
                "Kendi Geliştirdiğiniz Materyalin Adı *",
                placeholder="Örn: Katlanabilir Kesir ve Simetri Panosu",
            )
            ozgun_materyal_tanitim = st.text_area(
                "Geliştirdiğiniz Materyali Kısaca Tanıtın *",
                placeholder="Materyalin neyden oluştuğunu ve hangi kavramı somutlaştırdığını kısaca tanıtınız...",
                height=75,
            )

        materyal_aciklama = st.text_area(
            "Materyali Nasıl Kullanacaksınız? (Nasıl Kullanılması Gerektiği) *",
            placeholder="Materyalin derste ve kriz anında nasıl kullanılması gerektiğini kısaca anlatınız...",
            height=85,
        )

        if st.button("📥 Müdahaleyi Kaydet ve AI Öğrenci Tepkilerini Gör", type="primary", use_container_width=True):
            ozgun_eksik = (
                secilen_materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal"
                and (not ozgun_materyal_adi.strip() or not ozgun_materyal_tanitim.strip())
            )
            if (
                (sesli_kayit is None and not sesli_girdi_manuel.strip())
                or eylem_1 == "Seçiniz..."
                or eylem_2 == "Seçiniz..."
                or secilen_materyal == "Seçiniz..."
                or ozgun_eksik
                or not materyal_aciklama.strip()
            ):
                st.error("❌ Tüm zorunlu (*) alanlar (sesli/yazılı tepki, 1. ve 2. eylem, materyal seçimi, varsa kendi materyal tanıtımı ve nasıl kullanılacağı) doldurulmadan ilerlenemez.")
            else:
                kayit_metni = (
                    sesli_girdi_manuel.strip()
                    if sesli_girdi_manuel.strip()
                    else "Mikrofon üzerinden sesli hitabet kaydedildi."
                )

                materyal_etiketi = (
                    f"{ozgun_materyal_adi.strip()} (Özgün Materyal)"
                    if secilen_materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal"
                    else secilen_materyal
                )

                ai_sonuc_tepkileri = {}
                degerlendirmeler = []
                for ogr_ad in secili_liste:
                    ogr_durum = ogrenci_profilleri[ogr_ad]["durum"]
                    d1, d2 = eylem_uygunlugu_degerlendir(eylem_1, eylem_2, ogr_durum)
                    degerlendirmeler.append(d1 and d2)
                    ai_sonuc_tepkileri[ogr_ad] = ai_profil_davranisi_uret(
                        ogr_ad,
                        secilen_sinif,
                        secilen_tema,
                        secilen_kazanim_obj["kod"],
                        secilen_kazanim_obj["cikti"],
                        secilen_surec,
                        secilen_kazanim_obj["kriz"],
                        kayit_metni,
                        eylem_1,
                        eylem_2,
                        materyal_etiketi,
                        materyal_aciklama.strip(),
                    )

                genel_uyum = all(degerlendirmeler)

                st.session_state.simulasyon_gecmisi.append({
                    "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sinif": secilen_sinif,
                    "tema": secilen_tema,
                    "kod": secilen_kazanim_obj["kod"],
                    "cikti": secilen_kazanim_obj["cikti"],
                    "surec": secilen_surec,
                    "secilen_ogrenciler": list(secili_liste),
                    "baslangic_davranislari": baslangic_davranislari,
                    "ai_sonuc_tepkileri": ai_sonuc_tepkileri,
                    "eylem_1": eylem_1,
                    "eylem_2": eylem_2,
                    "genel_uyum": genel_uyum,
                    "materyal_turu": secilen_materyal,
                    "materyal_etiketi": materyal_etiketi,
                    "ozgun_materyal_tanitim": ozgun_materyal_tanitim.strip(),
                    "materyal_aciklama": materyal_aciklama.strip(),
                    "sesli_komut": kayit_metni,
                })
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sag:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">💡 2024 Türkiye Yüzyılı Maarif Modeli & Rubrik Analizi</div>', unsafe_allow_html=True)
        if st.session_state.simulasyon_gecmisi:
            son_kayit = st.session_state.simulasyon_gecmisi[-1]
            if son_kayit["genel_uyum"]:
                st.success("🌟 **Kapsayıcı ve Keşif Odaklı Uyum:** Seçilen eylem adımları ve materyal kullanımı 2024 Türkiye Yüzyılı Maarif Modeli ve öğrenci profilleriyle uyumlu ilerledi.")
            else:
                st.warning("⚠️ **Eylem ve Profil Uyum Analizi:** Seçilen eylem sırası bazı öğrenci profillerinde ek destek veya farklı bir yaklaşım gerektirebilir.")

            for _, tepki in son_kayit["ai_sonuc_tepkileri"].items():
                st.markdown(f"- {tepki}")

            st.divider()
            if st.button("📋 Detaylı Transkript ve Raporlama Paneline Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()
        else:
            st.info("Müdahalenizi kaydettikten sonra seçili öğrencilerin AI tepkileri ve rapor geçiş butonu burada aktifleşir.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. ADIM 3: DERS TRANSKRİPTİ, ÇOK KATMANLI RAPOR VE ÖĞRETİM ELEMANI DÖNÜTÜ
# ==========================================
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 2024 Türkiye Yüzyılı Maarif Modeli Ders Transkripti ve Değerlendirme Paneli")
    st.markdown(
        f"**Aday:** {st.session_state.get('ogretmen_adi', 'N/A')} | "
        f"**No:** {st.session_state.get('okul_numarasi', 'N/A')} | "
        f"**Kurum:** {st.session_state.get('universite_adi', 'N/A')} | "
        f"**Danışman:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )
    st.divider()

    tab_ogretim, tab_aday, tab_fakulte = st.tabs([
        "👨‍🏫 Öğretim Elemanı Ders Transkripti & Geri Dönüt",
        "👩‍🏫 Aday Gelişim & Dijital Replay",
        "🏛️ Dekanlık Kurumsal Rapor",
    ])

    toplam_islem = len(st.session_state.simulasyon_gecmisi)
    son_adim = st.session_state.simulasyon_gecmisi[-1] if toplam_islem > 0 else None

    with tab_ogretim:
        st.markdown("### 👨‍🏫 Öğretim Elemanına Sunulan Detaylı Yazılı Ders Transkripti")
        st.info(f"**Yüklenen Rubrik Kriterleri:**\n\n{st.session_state.get('rubrik_metni', 'N/A')}")

        if son_adim:
            ogrenci_etkilesim_satirlari = []
            for ogr_ad in son_adim["secilen_ogrenciler"]:
                ogr_durum = ogrenci_profilleri[ogr_ad]["durum"]
                ilk_hal = son_adim["baslangic_davranislari"].get(ogr_ad, "")
                son_hal = son_adim["ai_sonuc_tepkileri"].get(ogr_ad, "")
                ogrenci_etkilesim_satirlari.append(
                    f"**• {ogr_ad} ({ogr_durum}):**\n"
                    f"  - *Kriz / Başlangıç Davranışı:* {ilk_hal}\n"
                    f"  - *Öğretmen Adayının Karşılığı:* \"{son_adim['sesli_komut']}\" | *Materyal:* {son_adim['materyal_etiketi']}\n"
                    f"  - *Öğrencinin Bu Karşılığa Tepkisi:* {son_hal}"
                )

            ozgun_bilgi_metni = ""
            if son_adim.get("ozgun_materyal_tanitim"):
                ozgun_bilgi_metni = f"- **Özgün Materyal Tanıtımı:** {son_adim['ozgun_materyal_tanitim']}\n"

            transkript_metni = (
                f"**Model:** 2024 Türkiye Yüzyılı Maarif Modeli\n"
                f"**Oturum Zamanı:** {son_adim['tarih']}\n"
                f"**Sınıf ve Tema:** {son_adim['sinif']} — {son_adim['tema']}\n"
                f"**Öğrenme Çıktısı / Kazanım:** `{son_adim['kod']}` — {son_adim['cikti']}\n"
                f"**Süreç Bileşeni:** {son_adim['surec']}\n"
                f"**Seçilen Öğrenciler ({len(son_adim['secilen_ogrenciler'])}):** {', '.join(son_adim['secilen_ogrenciler'])}\n\n"
                f"**1. Seçilen Pedagojik Eylem Davranışları:**\n"
                f"- *1. Adım Davranışı:* {son_adim['eylem_1']}\n"
                f"- *2. Adım Davranışı:* {son_adim['eylem_2']}\n\n"
                f"**2. Materyal Seçimi, Tanıtımı ve Kullanım Akışı:**\n"
                f"- *Materyal:* {son_adim['materyal_etiketi']}\n"
                f"{ozgun_bilgi_metni}"
                f"- *Nasıl Kullanılması Gerektiği:* {son_adim['materyal_aciklama']}\n\n"
                f"**3. Öğrenci Tepkileri ve Öğretmen Adayının Cevapları (Etkileşim Transkripti):**\n"
                + "\n".join(ogrenci_etkilesim_satirlari)
                + f"\n\n**4. Aday Öz-Değerlendirmesi:**\n"
                f"- {son_adim.get('oz_degerlendirme') or 'Aday henüz öz-değerlendirme notu eklememiştir.'}"
            )

            st.markdown('<div class="transkript-kutu">', unsafe_allow_html=True)
            st.markdown(transkript_metni)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                label="⬇️ Yazılı Ders Transkriptini İndir (.txt)",
                data=transkript_metni.replace("**", "").replace("*", "").replace("`", ""),
                file_name=f"2024_TYMM_Ders_Transkripti_{st.session_state.get('okul_numarasi', 'aday')}.txt",
                mime="text/plain",
            )
        else:
            st.warning("Henüz tamamlanmış bir simülasyon oturumu bulunmuyor.")

        st.divider()
        st.markdown("#### ✍️ Öğretim Elemanı Geri Dönütü")
        hoca_notu = st.text_area(
            "Transkriptteki davranışlara, materyal kullanımına ve öğrenci tepkilerine ilişkin geri dönütünüz *",
            value=son_adim.get("hoca_donutu", "") if son_adim else "",
            height=130,
        )
        if st.button("📤 Öğretim Elemanı Geri Dönütünü Gönder", type="primary"):
            if not hoca_notu.strip():
                st.error("❌ Öğretim elemanı geri dönütü boş bırakılamaz.")
            elif son_adim is None:
                st.error("❌ Kayıtlı oturum bulunamadığı için dönüt eklenemedi.")
            else:
                st.session_state.simulasyon_gecmisi[-1]["hoca_donutu"] = hoca_notu.strip()
                st.success("✅ Öğretim elemanı geri dönütü kaydedildi.")

        if son_adim and son_adim.get("hoca_donutu"):
            st.success(f"**Kaydedilen Öğretim Elemanı Geri Dönütü:**\n\n{son_adim['hoca_donutu']}")

    with tab_aday:
        if son_adim:
            st.success(f"Oturum ID: #TYMM-{random.randint(10000, 99999)} | {son_adim['sinif']} — {son_adim['tema']}")
            st.markdown(
                f"- **Kazanım:** `{son_adim['kod']}` — {son_adim['cikti']}\n"
                f"- **Süreç Bileşeni:** {son_adim['surec']}\n"
                f"- **Seçilen Öğrenciler ({len(son_adim['secilen_ogrenciler'])}):** {', '.join(son_adim['secilen_ogrenciler'])}\n"
                f"- **1. Eylem:** {son_adim['eylem_1']}\n"
                f"- **2. Eylem:** {son_adim['eylem_2']}\n"
                f"- **Materyal:** {son_adim['materyal_etiketi']}\n"
                f"- **Nasıl Kullanılması Gerektiği:** {son_adim['materyal_aciklama']}\n"
                f"- **Aday İfadesi:** *\"{son_adim['sesli_komut']}\"*"
            )
            for _, tepki in son_adim["ai_sonuc_tepkileri"].items():
                st.write(f"- {tepki}")

            puanlar = [97, 95, 94, 96] if son_adim["genel_uyum"] else [76, 74, 78, 75]
            chart_data = pd.DataFrame({
                "Kriter": ["Sesli Hitabet", "Kapsayıcı Eğitim", "2024 TYMM Süreci", "Materyal & Aksiyon"],
                "Puan": puanlar,
            })
            st.bar_chart(chart_data, x="Kriter", y="Puan")
        else:
            st.warning("Henüz kayıtlı simülasyon oturumu bulunmuyor.")

        aday_geri_bildirimi = st.text_area(
            "Aday Öz-Değerlendirme ve Yansıtma Notu *",
            value=son_adim.get("oz_degerlendirme", "") if son_adim else "",
        )
        if st.button("📤 Öz-Değerlendirmeyi Kaydet"):
            if not aday_geri_bildirimi.strip():
                st.error("❌ Öz-değerlendirme notu boş bırakılamaz.")
            elif son_adim is None:
                st.error("❌ Kayıtlı oturum bulunamadığı için not eklenemedi.")
            else:
                st.session_state.simulasyon_gecmisi[-1]["oz_degerlendirme"] = aday_geri_bildirimi.strip()
                st.success("✅ Öz-değerlendirme notunuz kaydedildi.")

    with tab_fakulte:
        st.markdown("### 🏛️ Kurumsal Uygunluk Değerlendirmesi")
        st.markdown(
            "1. **2024 Türkiye Yüzyılı Maarif Modeli Uyumu:** Ortaokul matematik öğrenme çıktıları ve süreç bileşenleri temel alınmıştır.\n"
            "2. **Kapsayıcı Sınıf Yönetimi:** Seçilen öğrenci profillerine göre çoklu sınıf dinamiği izlenmiştir.\n"
            "3. **Komisyon Görüşü:** Staj uygulama portfolyosu ve yazılı ders transkripti değerlendirmeye uygundur."
        )

    st.divider()
    if st.button("🔄 Yeni Bir 3D Staj Simülasyonu Başlat"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.secili_ogrenciler = []
        st.session_state.adim = 1
        st.rerun()
