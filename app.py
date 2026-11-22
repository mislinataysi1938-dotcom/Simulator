import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TYMM 2026 Ortaokul Matematik 3D Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# Göz yormayan, uyumlu renk paleti ve sade kart tasarımı
st.markdown("""
    <style>
    .sade-kart {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .baslik-mavi {
        color: #1E3A8A;
        font-weight: 700;
        font-size: 1.08rem;
        margin-bottom: 8px;
    }
    .rozet {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
    st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state:
    st.session_state.secili_ogrenciler = ["Kerem", "Arda"]

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ VE BAĞLAMSAL AI DAVRANIŞ MOTORU
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


def ai_profil_davranisi_uret(ogrenci_adi, sinif, tema, kazanim_kod, kazanim_cikti, surec, temel_kriz, aday_sozu="", eylem_1="", eylem_2="", materyal=""):
    """
    Seçilen öğrencinin profiline ve aktif (sınıf, tema, kazanım, süreç bileşeni) bağlamına
    uygun öğrenci davranışı ve tepkisi üretir.
    """
    profil = ogrenci_profilleri[ogrenci_adi]
    durum = profil["durum"]
    tema_kisa = tema.split(":", 1)[1].strip() if ":" in tema else tema
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec

    mudahale_var = bool(aday_sozu.strip() or eylem_1 or materyal)
    dogru_eylem = (
        eylem_1 == "1. Öğrencinin duygusunu kabul edip güvenli alan sunmak (Empati kurmak)"
        and eylem_2 == "2. Somut/Dijital materyal üzerinden yönlendirici sorularla keşfettirmek"
    )

    if not mudahale_var:
        # Kriz anındaki başlangıç profil davranışı
        if durum == "Otizm Spektrumu":
            return f"{ogrenci_adi} (Otizm Spektrumu): {sinif} '{tema_kisa}' teması `{kazanim_kod}` ({surec_kisa}) adımında kulaklığını yoklayarak net ve adım adım bir yönerge bekler; '{temel_kriz}' belirsizliğinden rahatsız olur."
        if durum == "Disleksi":
            return f"{ogrenci_adi} (Disleksi): `{kazanim_kod}` ({kazanim_cikti}) ve '{surec_kisa}' sürecinde sayı/sembol sıralarını karıştırır; '{temel_kriz}' anında renkli/dokunsal ayrıştırmaya ihtiyaç duyar."
        if durum == "Üstün Yetenekli":
            return f"{ogrenci_adi} (Üstün Yetenekli): '{tema_kisa}' bağlamında '{surec_kisa}' adımı için hazır kuralı yeterli bulmaz; '{temel_kriz}' sırasında genellemenin gerekçesini sorgular."
        if durum == "Yüksek Kaygılı":
            return f"{ogrenci_adi} (Yüksek Kaygılı): `{kazanim_kod}` ve '{surec_kisa}' sürecinde yanlış yapmaktan çekinip geri çekilir; '{temel_kriz}' anında yargılamayan bir destek bekler."
        if durum == "DEHB":
            return f"{ogrenci_adi} (DEHB): '{tema_kisa}' temasında '{surec_kisa}' adımı uzadıkça odağını kaybeder; '{temel_kriz}' sırasında kısa ve etkileşimli bir görev ister."
        if durum == "İşitme Yetersizliği":
            return f"{ogrenci_adi} (İşitme Yetersizliği): `{kazanim_kod}` ve '{surec_kisa}' adımında yüz ifadesi ve görsel temsil arar; '{temel_kriz}' anında açık görsel şema bekler."
        if durum == "Az Gören":
            return f"{ogrenci_adi} (Az Gören): '{tema_kisa}' temasında '{surec_kisa}' sırasında küçük detayları seçmekte zorlanır; '{temel_kriz}' anında dokunsal ve açık sözel betimleme ister."
        if durum == "Diskalkuli":
            return f"{ogrenci_adi} (Diskalkuli): `{kazanim_kod}` ({surec_kisa}) sürecinde nicelik ve işlem ilişkilerini zihninde canlandıramaz; '{temel_kriz}' anında somut model arar."
        if durum == "Bedensel Yetersizlik":
            return f"{ogrenci_adi} (Bedensel Yetersizlik): '{tema_kisa}' temasında '{surec_kisa}' mantığını takip eder ancak yoğun çizim/yazım gerektiren '{temel_kriz}' adımında erişilebilir araç ister."
        return f"{ogrenci_adi} (Düşük Motivasyon): `{kazanim_kod}` ve '{surec_kisa}' sürecinde konunun günlük hayattaki işlevini sorgular; '{temel_kriz}' anında gerçek yaşam bağı arar."

    # Öğretmen adayı müdahale ettikten sonraki AI tepkisi
    soz_ozet = aday_sozu.strip()[:70]
    if not dogru_eylem:
        if durum == "Otizm Spektrumu":
            return f"{ogrenci_adi} (Otizm Spektrumu): \"{soz_ozet}\" dediniz ama '{surec_kisa}' adımını netleştirmeden ve güvenli alan kurmadan ilerlediğiniz için huzursuzluğu sürer."
        if durum == "Disleksi":
            return f"{ogrenci_adi} (Disleksi): \"{soz_ozet}\" yaklaşımında `{kazanim_kod}` sembolleri hâlâ karmaşık görünüyor; materyalle adım adım keşif bekliyor."
        if durum == "Üstün Yetenekli":
            return f"{ogrenci_adi} (Üstün Yetenekli): Hazır kural verildiğinde '{tema_kisa}' temasındaki '{surec_kisa}' ilişkisi yüzeysel kalıyor; kendi çıkarımını yapmak istiyor."
        if durum == "Yüksek Kaygılı":
            return f"{ogrenci_adi} (Yüksek Kaygılı): Önce duygusal güven sağlanmadığı için `{kazanim_kod}` sorusunda hata yapma kaygısı devam ediyor."
        return f"{ogrenci_adi} ({durum}): `{kazanim_kod}` ({surec_kisa}) adımında doğrudan kural yerine önce empati ve ardından materyalle keşif bekliyor."

    if durum == "Otizm Spektrumu":
        return f"{ogrenci_adi} (Otizm Spektrumu): Sakin ses tonunuz ve '{materyal}' ile '{surec_kisa}' adımını sırayla göstermeniz sayesinde `{kazanim_kod}` sürecine uyum sağlar."
    if durum == "Disleksi":
        return f"{ogrenci_adi} (Disleksi): Baskı kurmadan '{materyal}' üzerinden `{kazanim_kod}` ({surec_kisa}) ilişkilerini görsel-dokunsal biçimde ayırt eder."
    if durum == "Üstün Yetenekli":
        return f"{ogrenci_adi} (Üstün Yetenekli): Kuralı hazır vermek yerine '{materyal}' ile '{surec_kisa}' genellemesini kendisinin bulmasına alan açmanızla derse aktif katılır."
    if durum == "Yüksek Kaygılı":
        return f"{ogrenci_adi} (Yüksek Kaygılı): Güven veren yaklaşımınızla kaygısı azalır; '{materyal}' desteğiyle `{kazanim_kod}` adımını denemeye başlar."
    if durum == "DEHB":
        return f"{ogrenci_adi} (DEHB): Kısa, net yönergeler ve '{materyal}' ile uygulamalı ilerlemeniz sayesinde '{surec_kisa}' odağını korur."
    if durum == "İşitme Yetersizliği":
        return f"{ogrenci_adi} (İşitme Yetersizliği): Göz teması ve '{materyal}' üzerinden sunduğunuz açık görsel temsille `{kazanim_kod}` adımını kavrar."
    if durum == "Az Gören":
        return f"{ogrenci_adi} (Az Gören): Açık sözel betimlemeniz ve dokunsal '{materyal}' desteğiyle '{surec_kisa}' basamağını rahatlıkla takip eder."
    if durum == "Diskalkuli":
        return f"{ogrenci_adi} (Diskalkuli): '{materyal}' ile nicelikleri somutlaştırmanız sayesinde `{kazanim_kod}` ({surec_kisa}) arasındaki sayısal ilişkiyi kurar."
    if durum == "Bedensel Yetersizlik":
        return f"{ogrenci_adi} (Bedensel Yetersizlik): Erişilebilir '{materyal}' ve destekleyici yönlendirmenizle '{surec_kisa}' çıkarımını başarıyla tamamlar."
    return f"{ogrenci_adi} (Düşük Motivasyon): Günlük yaşam bağlantısı ve '{materyal}' uygulamasıyla `{kazanim_kod}` sürecine ilgiyle katılır."


# ==========================================
# 2. ORTAOKUL MATEMATİK TYMM (5–8. SINIF) TAM MÜFREDAT ARŞİVİ
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: Geometrik Şekiller",
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
                        "ç) Örüntüler üzerinden basamak sayısı çok olan sayıların okunuş ve yazılışlarına dair önermelerde bulunur.",
                    ],
                    "hook": "Millî Kütüphane ve nüfus verilerindeki çok basamaklı arşiv kodlama sistemi.",
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
                    "hook": "Okul gezisi bütçesi ve ulaşım planlaması hesaplamaları.",
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
                    "hook": "Mutfak ölçülerinde yarım, çeyrek ve tam bardak eşleştirmeleri.",
                    "kriz": "Payda büyüdükçe birim kesrin küçüldüğünü görsel olarak kabullenmekte zorlanır.",
                },
                {
                    "kod": "MAT.5.1.4",
                    "cikti": "Kesir, ondalık ve yüzde gösterimleri arasındaki ilişkileri yorumlayabilme",
                    "surec": [
                        "a) Yüzlük kart ve modeller üzerinden kesir, ondalık ve yüzde temsillerini eşleştirir.",
                        "b) Farklı gösterimler arasında dönüşüm yaparak karşılaştırma yapar.",
                    ],
                    "hook": "Batarya doluluk yüzdesi ile kesir/ondalık gösterimlerin karşılaştırılması.",
                    "kriz": "Ondalık gösterimdeki basamak değerleriyle yüzde gösterimini karıştırır.",
                },
            ],
            "2. Tema: Geometrik Şekiller": [
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
                    "hook": "Sınıfın en çok tercih ettiği okuma etkinlikleri araştırması.",
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
                    "hook": "Farklı uzunluktaki iki kurdeleyi eşit parçalara ayırma problemi.",
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
                    "kriz": "Harf sembolünün tek bir gizli sayı değil değişken olduğunu anlamakta zorlanır.",
                },
                {
                    "kod": "MAT.6.2.2",
                    "cikti": "Sayı ve şekil örüntülerinin kuralını cebirsel olarak ifade edebilme",
                    "surec": [
                        "a) Ardışık adımlar arasındaki değişim miktarını inceler.",
                        "b) Örüntünün genel kuralını tablo ve cebirsel ifadeyle gösterir.",
                    ],
                    "hook": "Kibrit çöpleriyle adım adım büyüyen geometrik desenler.",
                    "kriz": "Artış miktarını bulur ancak başlangıç terimi düzeltmesini unutur.",
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
                        "b) Çevre/çap oranının sabitliğini (pi) geneller.",
                    ],
                    "hook": "Farklı tekerleklerin bir tam turda aldığı yol ile çaplarının karşılaştırılması.",
                    "kriz": "Yarıçap ile çapı karıştırıp çevre formülünde iki kat hata yapar.",
                },
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": "Kategorik veya kesikli nicel veriyle araştırma yapıp merkezî eğilim ve yayılımı yorumlayabilme",
                    "surec": [
                        "a) Araştırma sorusu ve veri toplama planı oluşturur.",
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
                        "a) Toplamsal ve çarpımsal ilişkileri ayırt eder.",
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
                    "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturmaya dair çıkarım yapabilme",
                    "surec": [
                        "a) Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturmaya dair varsayımlarda bulunur.",
                        "b) Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturur.",
                        "c) Varsayımlarını doğrulamaya yönelik karşılaştırmalar yapar.",
                        "ç) Bir şekil ile yansıma dönüşümü altındaki görüntüsü arasındaki ilişkilere dair önermeler sunar.",
                        "d) Önermenin verilen iki eş şeklin simetrik olup olmadığını belirlemeye katkısını değerlendirir.",
                    ],
                    "hook": "Durgun göl yüzeyinde veya aynada oluşan simetrik yansımalar.",
                    "kriz": "Yansıma eksenine dik uzaklığı saymadan şekli doğrudan kaydırarak çizer.",
                },
                {
                    "kod": "MAT.7.3.2",
                    "cikti": "Yansıma dönüşümündeki deneyimlerini orta dikme ve açıortay inşasına yansıtabilme",
                    "surec": [
                        "a) Yansıma dönüşümünde simetri doğrusunun özelliklerini gözden geçirir.",
                        "b) Bir doğru parçasına ait orta dikmenin ve bir açıya ait açıortayın inşasına dair çıkarım yapar.",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir.",
                    ],
                    "hook": "İki yerleşim noktasına eşit uzaklıktaki durak noktasının belirlenmesi.",
                    "kriz": "Orta dikme ile açıortay inşasındaki eş uzaklık özelliğini karıştırır.",
                },
            ],
            "4. Tema: Geometrik Nicelikler (1)": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": "Eş küplerle oluşturulan yapılar ile görünümleri arasındaki ilişkiyi çözümleyebilme",
                    "surec": [
                        "a) Eş küplerle oluşturulan yapıların farklı yönlerden görünümlerini çizer ve yapıyı oluşturur.",
                        "b) Oluşturduğu yapı ile görünümleri arasındaki ilişkileri belirler.",
                    ],
                    "hook": "Mimari maketlerin önden, üstten ve sağdan görünüm çizimleri.",
                    "kriz": "Arka sırada kalan küplerin üstten ve yandan görünüme etkisini unutur.",
                },
                {
                    "kod": "MAT.7.4.2",
                    "cikti": "Dikdörtgenler prizmasının yüzey alanını yorumlayabilme",
                    "surec": [
                        "a) Dikdörtgenler prizmasının farklı yüzey açınımlarını inceler.",
                        "b) Yüzey açınımı ile yüzey alanı arasındaki ilişkileri ifade eder.",
                        "c) Yüzey açınımlarından yararlanarak yüzey alanlarını hesaplar.",
                    ],
                    "hook": "Hediye kutusunun tamamını kaplamak için gereken kâğıt alanının hesabı.",
                    "kriz": "Karşılıklı eş yüzlerden yalnızca birini hesaplayıp ikiyle çarpmayı unutur.",
                },
                {
                    "kod": "MAT.7.4.4",
                    "cikti": "Dikdörtgenler prizmasının hacim bağıntısını değerlendirebilme",
                    "surec": [
                        "a) Hacmi belirlemede ölçüt olarak birim küpleri belirler.",
                        "b) Prizmaların içine yerleştirilen birim küpleri sayar.",
                        "c) Toplam birim küp sayısı ile ayrıt uzunluklarını karşılaştırır.",
                        "ç) Hacmi taban alanı ile yüksekliğin çarpımı olarak ifade eder.",
                    ],
                    "hook": "Eş kolilerin dikdörtgen prizma biçimindeki depoya katman katman dizilmesi.",
                    "kriz": "Yüzey alanı ile hacim birimlerini ve bağıntılarını birbirine karıştırır.",
                },
                {
                    "kod": "MAT.7.4.5",
                    "cikti": "Hacim ölçme birimleri arasındaki ilişkileri değerlendirebilme",
                    "surec": [
                        "a) Bir cismin hacmini ölçmede metreküpü ve litreyi ölçüt olarak belirler.",
                        "b) Metreküp ve litreyi kullanarak ölçme yapar.",
                        "c) Hacim ve sıvı ölçme birimlerini ilişkilendirerek karşılaştırır.",
                        "ç) Karşılaştırmalarına ilişkin yargıda bulunur.",
                    ],
                    "hook": "Su deposunun metreküp kapasitesi ile litre cinsinden karşılığı.",
                    "kriz": "Hacim birimlerinde biner basamak dönüşümü yerine yüzer dönüşüm yapar.",
                },
            ],
            "4. Tema: Geometrik Nicelikler (2)": [
                {
                    "kod": "MAT.7.4.7",
                    "cikti": "Dikdörtgen, paralelkenarın alanına ve çemberin uzunluğuna ilişkin deneyimlerini dairenin alan bağıntısına yansıtabilme",
                    "surec": [
                        "a) Dikdörtgen, paralelkenar alanı ve çember uzunluğu deneyimlerini gözden geçirir.",
                        "b) Dairenin alan bağıntısına yönelik çıkarım yapar.",
                        "c) Çıkarımını farklı örnekler üzerinden değerlendirir.",
                    ],
                    "hook": "Dairesel dilimlere ayrılan dairenin paralelkenara dönüştürülmesi.",
                    "kriz": "Daire alanında yarıçapın karesi yerine çapı kullanır.",
                },
                {
                    "kod": "MAT.7.4.8",
                    "cikti": "Çemberde merkez açı ve gördüğü yay uzunluğundan yola çıkarak daire diliminin alanına yönelik analojik akıl yürütebilme",
                    "surec": [
                        "a) Merkez açı ve yay uzunluğu ile daire diliminin alanı arasındaki ilişkileri gözlemler.",
                        "b) Merkez açı ile daire dilimi alanı arasındaki orantıyı tespit eder.",
                        "c) Daire diliminin alanına dair çıkarım yapar.",
                    ],
                    "hook": "Dilimlere ayrılmış pizzada merkez açıya göre dilim alanının bulunması.",
                    "kriz": "Tam daire açısı olan 360 derece ile orantı kurmayı unutur.",
                },
                {
                    "kod": "MAT.7.4.9",
                    "cikti": "Eşkenar dörtgen ve yamuğun alan bağıntılarına dair çıkarım yapabilme",
                    "surec": [
                        "a) Ön bilgileriyle eşkenar dörtgen ve yamuğun alan hesabına yönelik varsayımda bulunur.",
                        "b) Parçalayarak veya tamamlayarak oluşturduğu şekillerin alanlarını belirler.",
                        "c) Oluşturulan alanları varsayımlarıyla karşılaştırır ve önermeler sunar.",
                    ],
                    "hook": "Yamuk biçimindeki çatı yüzeyi ve eşkenar dörtgen karo kaplaması.",
                    "kriz": "Yamukta alt ve üst taban toplamını ikiye bölmeyi unutur.",
                },
            ],
            "5. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Matematiksel araç ve teknolojiden yararlanarak üçgende kenarortayı, açıortayı ve yüksekliği çözümleyebilme",
                    "surec": [
                        "a) Üçgende kenarortayı, açıortayı ve yüksekliği belirler.",
                        "b) Üçgende kenarortay, açıortay ve yükseklik arasındaki ilişkileri belirler.",
                    ],
                    "hook": "İkizkenar ve eşkenar üçgen çatılarda yardımcı elemanların çakışması.",
                    "kriz": "Geniş açılı üçgende yüksekliğin üçgenin dışına düşmesini anlamakta zorlanır.",
                }
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.7.6.1",
                    "cikti": "Kategorik veya nicel (sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme",
                    "surec": [
                        "a) Sürekli veriye dayanan istatistiksel araştırma durumlarını fark eder.",
                        "b) Araştırma sorusu oluşturur ve veri toplar.",
                        "c) Çizgi/nokta grafiği ve özetleme araçlarını seçip analiz eder.",
                        "ç) Ulaştığı sonuçlara yönelik gerekçeler sunar.",
                    ],
                    "hook": "Haftalık hava sıcaklığı ve boy uzunluğu değişim verilerinin analizi.",
                    "kriz": "Sürekli veri ile kesikli veriye uygun grafik türünü karıştırır.",
                }
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.7.7.1",
                    "cikti": "Bir olayın ve tümleyeninin olasılığına ilişkin tümevarımsal akıl yürütebilme",
                    "surec": [
                        "a) Bir olayın olasılığını hesaplamaya ilişkin olası tüm çıktıları gözlemler.",
                        "b) Bir olayın ve tümleyeninin olasılığını hesaplamak için matematiksel ilişkiyi bulur.",
                        "c) Bir olayın ve tümleyeninin olasılığının ilişkisine yönelik genelleme yapar.",
                    ],
                    "hook": "Hedef tahtasında isabet etme ile isabet etmeme olasılıkları toplamı.",
                    "kriz": "Tümleyen olasılığını 1'den çıkarmak yerine doğrudan olay sayısını yazar.",
                },
                {
                    "kod": "MAT.7.7.3",
                    "cikti": "Olayları ayrık olma ve ayrık olmama durumlarına göre sınıflandırabilme",
                    "surec": [
                        "a) Çıktıların ortak olup olmamasını ölçüt olarak belirler.",
                        "b) Olayları ayrık olma ve ayrık olmama durumuna göre ayrıştırır ve etiketler.",
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
                    "cikti": "Farklı bağlamlardaki üslü ifadelere, özelliklerine ve üslü ifadelerle yapılan işlemlere ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) Üslü ifadeler ve işlemlere yönelik varsayımlarda bulunur.",
                        "b) Örnek ve temsillerle genellemeleri belirler ve sınar.",
                        "c) Önermeleri sözel ve cebirsel olarak ifade eder.",
                    ],
                    "hook": "Mikroorganizmaların belirli zaman aralıklarında ikiye katlanarak çoğalması.",
                    "kriz": "Üslü ifadelerde çarpma yaparken tabanlar eşitken üstleri toplamak yerine çarpar.",
                },
                {
                    "kod": "MAT.8.1.2",
                    "cikti": "Karşılaştığı problem durumlarında kareköklü ifadeler ile ilgili muhakeme yapabilme",
                    "surec": [
                        "a) Bir karenin alanı ile kenar uzunluğu arasındaki ilişkiyi belirler.",
                        "b) Tam kare pozitif tam sayılar ile kareköklerini ilişkilendirir.",
                        "c) Tam kare olmayan pozitif sayının karekökünün hangi iki doğal sayı arasında olduğunu ifade eder.",
                    ],
                    "hook": "Alanı 50 metrekare olan kare biçimindeki odanın kenar uzunluğunun kestirilmesi.",
                    "kriz": "Tam kare olmayan bir sayının karekökünü bulurken sayıyı ikiye bölmeye çalışır.",
                },
                {
                    "kod": "MAT.8.1.3",
                    "cikti": "Sayıların rasyonel ya da irrasyonelliğini değerlendirebilme",
                    "surec": [
                        "a) Ondalık gösterimlerini ölçüt olarak belirler.",
                        "b) Ondalık gösterimleri elde eder ve ölçüt ile karşılaştırır.",
                        "c) Sayının rasyonel olup olmadığına yönelik yargıda bulunur.",
                    ],
                    "hook": "Pi sayısı, kök 2 ve devirli ondalık sayıların ondalık açılımlarının incelenmesi.",
                    "kriz": "Devirli ondalık sayıları sonsuza gittiği için irrasyonel sanır.",
                },
                {
                    "kod": "MAT.8.1.4",
                    "cikti": "Gerçek sayıları ve aralıklarını sayı doğrusunda yorumlayabilme",
                    "surec": [
                        "a) Doğal sayılardan başlamak üzere tüm gerçek sayıları ve aralarındaki ilişkileri inceler.",
                        "b) Gerçek sayıları sayı doğrusuna yerleştirir ve aralıkları açıklar.",
                    ],
                    "hook": "Sıcaklık ve hız limitlerindeki açık/kapalı aralık gösterimleri.",
                    "kriz": "Sayı kümelerinin kapsama ilişkisini kurmakta zorlanır.",
                },
            ],
            "2. Tema: Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": "Gerçek yaşam durumları üzerinden dik koordinat sistemini çözümleyebilme",
                    "surec": [
                        "a) Dik koordinat sisteminin bileşenlerini (düzlem, eksenler, sayı ikilileri) belirler.",
                        "b) Bileşenler arasındaki ilişkileri belirler.",
                    ],
                    "hook": "Harita ve oyun düzleminde referans noktasına göre konum belirleme.",
                    "kriz": "Sıralı ikilide yatay (apsis) ve dikey (ordinat) eksenlerin yerini karıştırır.",
                },
                {
                    "kod": "MAT.8.2.2",
                    "cikti": "Gerçek yaşam durumlarındaki doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme",
                    "surec": [
                        "a) Doğrusal fonksiyonların cebirsel, tablo ve grafik temsillerini tanır.",
                        "b) Uygun temsili belirler ve temsiller arası geçiş yapar.",
                        "c) Temsillerin ekonomiklik ve kullanışlılığını karşılaştırır.",
                    ],
                    "hook": "Taksimetre açılış ücreti ve gidilen kilometreye göre ücret grafiği.",
                    "kriz": "Doğrusal ilişkideki sabit değişim oranını (eğimi) yorumlamakta zorlanır.",
                },
                {
                    "kod": "MAT.8.2.3",
                    "cikti": "Dik koordinat sisteminde iki doğrusal fonksiyonun birbirine göre durumuna ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) İki doğrunun birbirine göre durumuna ilişkin varsayım oluşturur.",
                        "b) Eğim ilişkilerini inceleyerek paralellik ve diklik genellemeleri yapar.",
                    ],
                    "hook": "İki farklı abonelik paketinin maliyet doğrularının kesişimi.",
                    "kriz": "Eğimleri eşit iki doğrunun paralel olduğunu grafikte fark edemez.",
                },
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": "Üçgenin kenarları ve açıları arasındaki ilişkiyi yorumlayabilme",
                    "surec": [
                        "a) Üçgenin kenar ve açı özelliklerini inceler.",
                        "b) Kenar uzunluklarının büyüklüğüne göre açıları, açılara göre kenarları sıralar.",
                    ],
                    "hook": "Açılan rampanın eğimi ile karşısındaki kenar uzunluğunun değişimi.",
                    "kriz": "Büyük açının karşısında büyük kenar bulunduğunu ters yorumlar.",
                },
                {
                    "kod": "MAT.8.3.2",
                    "cikti": "Üçgenin kenar uzunlukları arasındaki ilişkiye (üçgen eşitsizliği) yönelik çıkarım yapabilme",
                    "surec": [
                        "a) Üçgen oluşturabilen üç doğru parçasının uzunluklarına dair varsayımda bulunur.",
                        "b) Oluşturduğu üçgenleri listeleyip kenar uzunlukları arasındaki ilişkiye dair önerme sunar.",
                    ],
                    "hook": "Üç farklı çubuk parçasından üçgen çerçeve oluşturulup oluşturulamayacağı.",
                    "kriz": "İki kenarın toplamının üçüncü kenara eşit olduğu durumda üçgen oluşacağını sanır.",
                },
                {
                    "kod": "MAT.8.3.5",
                    "cikti": "Dik üçgenlerde dik kenar uzunluklarının kareleri toplamının hipotenüsün karesine eşit olduğunu (Pisagor) yorumlayabilme",
                    "surec": [
                        "a) a^2 + b^2 = c^2 eşitliğini sağlayan üçgenleri inceler.",
                        "b) Pisagor bağıntısını açı-kenar ilişkisi ve üçgen eşitsizliğiyle ilişkilendirir.",
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
                        "a) Yüzey açınımlarında yer alan şekilleri belirler.",
                        "b) Açınımdaki şekiller arasındaki ayrıt ve çevre ilişkilerini belirler.",
                    ],
                    "hook": "Silindir ve piramit biçimindeki ambalaj kutularının karton açınımları.",
                    "kriz": "Silindirin yanal dikdörtgen kenarının taban çevresine eşit olduğunu göremez.",
                },
                {
                    "kod": "MAT.8.4.3",
                    "cikti": "Dairenin alan bağıntısından hareketle dik dairesel silindirin hacim bağıntısına yönelik analojik akıl yürütebilme",
                    "surec": [
                        "a) Daire alanı ile dik dairesel silindir arasındaki ilişkiyi gözden geçirir.",
                        "b) Taban alanı ile yüksekliğin çarpımı üzerinden silindirin hacmine yönelik çıkarım yapar.",
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
                        "a) Öteleme dönüşümü altındaki görüntülerin kenar ve açı özelliklerini belirler.",
                        "b) Geometrik şekiller ile öteleme altındaki görüntüleri arasındaki eşlik ilişkilerini belirler.",
                    ],
                    "hook": "Bir şeklin yönü ve boyutu değişmeden düzlemde kaydırılması.",
                    "kriz": "Öteleme sonrasında şeklin yönünün veya boyutunun değişeceğini düşünür.",
                },
                {
                    "kod": "MAT.8.5.2",
                    "cikti": "Dik koordinat sisteminde noktaların öteleme ve eksenlere göre yansıma dönüşümündeki değişimlerine ilişkin çıkarım yapabilme",
                    "surec": [
                        "a) Apsis ve ordinat değişimlerine dair varsayımlarda bulunur.",
                        "b) Öteleme ve yansıma görüntülerini oluşturup koordinat değişimlerini önerme olarak sunar.",
                    ],
                    "hook": "Dijital oyun sahnesinde karakterin koordinat eksenlerine göre hareketi.",
                    "kriz": "x eksenine göre yansımada ordinat yerine apsisin işaretini değiştirir.",
                },
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.8.6.1",
                    "cikti": "Kategorik veya nicel (kesikli-sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme",
                    "surec": [
                        "a) Araştırma sorusu oluşturur ve uygun veri toplama planı yapar.",
                        "b) Veri görselleştirme ve özetleme araçlarını seçme gerekçelerini belirtir.",
                        "c) Toplanan veriyi analiz edip ulaştığı sonuçlara gerekçeler sunar.",
                    ],
                    "hook": "İki şubenin deneme sınavı dağılımlarının merkez ve yayılım ölçülerine göre kıyası.",
                    "kriz": "Veri dağılımını yorumlarken yalnızca aritmetik ortalamaya bakıp yayılımı ihmal eder.",
                }
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1",
                    "cikti": "Gerçek yaşamda karşılaşabileceği bir olayın olasılığına ilişkin farklı olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı belirleyerek karar verebilme",
                    "surec": [
                        "a) Karar vermeye yönelik amacı belirler ve bilgi toplar.",
                        "b) Olasılık yaklaşımlarına yönelik önermeler oluşturur ve sorgular.",
                        "c) Uygun olasılık yaklaşımını seçerek kararına yansıtır.",
                    ],
                    "hook": "Penaltı atışı, zar deneyi ve hava tahmini durumlarında olasılık yaklaşımı seçimi.",
                    "kriz": "Deneysel veriyle tahmin edilmesi gereken durumda öznel tahmine yönelir.",
                }
            ],
        },
    },
}
# ==========================================
# 3. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.markdown('<span class="rozet">ADIM 1 / 3</span>', unsafe_allow_html=True)
    st.subheader("📝 2026 Maarif Modeli Kurulum ve Rubrik Paneli")
    st.info("Aday bilgilerini ve danışman öğretim elemanının rubriğini girerek 3D canlı sınıf stajını başlatın.")

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
                "2. Pedagojik eylem sırasının doğruluğu ve kapsayıcı hitabet (30 Puan).\n"
                "3. 2026 Maarif Modeli öğrenme çıktısı ve süreç bileşenleri uyumu (20 Puan).\n"
                "4. Materyal seçimi, kullanımı ve sahada aksiyon alma başarısı (20 Puan)."
            ),
            height=115,
        )
        sinif_mevcudu = st.slider("Sınıf Mevcudu", min_value=12, max_value=35, value=25)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 3D Staj Simülasyonunu Başlat", type="primary", use_container_width=True):
        if not all([ogretmen_adi.strip(), okul_numarasi.strip(), universite_adi.strip(), uygulama_ogretim_elemani.strip(), rubrik_metni.strip()]):
            st.warning("Lütfen yıldızlı (*) tüm zorunlu alanları doldurunuz.")
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
# 4. ADIM 2: 3D GÖRSEL SINIF, ÇOKLU ÖĞRENCİ SEÇİMİ VE SESLİ ETKİLEŞİM
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    okul_no = st.session_state.get("okul_numarasi", "N/A")
    universite = st.session_state.get("universite_adi", "Üniversite")
    ogretim_elemani = st.session_state.get("uygulama_ogretim_elemani", "Öğretim Elemanı")

    st.markdown('<span class="rozet">ADIM 2 / 3</span>', unsafe_allow_html=True)
    st.markdown(f"### 🏫 3D Canlı Sınıf & Sesli Etkileşim | {ogretmen} ({okul_no}) — {universite}")

    with st.expander("📚 Ortaokul Matematik TYMM Sınıf, Tema, Kazanım ve Süreç Bileşeni Seçimi", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            secilen_sinif = st.selectbox("Sınıf Düzeyi", list(tyym_master_arsiv.keys()))
        with col_s2:
            secilen_tema = st.selectbox("Tema", tyym_master_arsiv[secilen_sinif]["Temalar"])
        kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]
        with col_s3:
            kazanim_secenekleri = [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
            secilen_kazanim_str = st.selectbox("Öğrenme Çıktısı / Kazanım", kazanim_secenekleri)

        secilen_kazanim_obj = next(
            k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str
        )
        secilen_surec = st.selectbox("Süreç Bileşeni", secilen_kazanim_obj["surec"])
        st.success(f"💡 **Günlük Yaşam Bağlamı:** {secilen_kazanim_obj['hook']}")

    # Sınıftaki 10 Öğrenciden İstediği Sayıda (1, 3, 5 veya 10) Seçim Yapabilme
    st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
    st.markdown('<div class="baslik-mavi">👥 Sınıftaki Öğrencileri Seçin (1 ile 10 Arası İstediğiniz Kadar Seçebilirsiniz)</div>', unsafe_allow_html=True)

    col_hizli1, col_hizli2, col_hizli3 = st.columns([2, 1, 1])
    with col_hizli2:
        if st.button("✅ Tümünü Seç (10 Öğrenci)", use_container_width=True):
            st.session_state.secili_ogrenciler = list(ogrenci_profilleri.keys())
            st.rerun()
    with col_hizli3:
        if st.button("🧹 Seçimi Temizle", use_container_width=True):
            st.session_state.secili_ogrenciler = []
            st.rerun()

    secilen_ogrenciler = st.multiselect(
        "Simülasyona dahil edilecek öğrenci profilleri:",
        options=list(ogrenci_profilleri.keys()),
        default=st.session_state.secili_ogrenciler,
        format_func=lambda x: f"{ogrenci_profilleri[x]['ikon']} {x} ({ogrenci_profilleri[x]['durum']})",
    )
    st.session_state.secili_ogrenciler = secilen_ogrenciler
    st.markdown('</div>', unsafe_allow_html=True)

    if not secilen_ogrenciler:
        st.warning("Lütfen sınıfa dahil etmek için en az 1 öğrenci profili seçiniz.")
        st.stop()

    st.info(f"👨‍🏫 **Gözlemci:** {ogretim_elemani} | **Sınıftaki Seçili Öğrenci Sayısı:** {len(secilen_ogrenciler)} / 10")

    # Seçilen Öğrencilerin Canlı Profil Kartları ve Bağlamsal AI Davranışları
    st.markdown("#### 🧠 Seçili Öğrencilerin Aktif Kazanım ve Süreç Bileşenine Göre AI Davranışları")
    kart_sutunlari = st.columns(min(len(secilen_ogrenciler), 3))
    baslangic_davranislari = {}

    for idx, ogr_ad in enumerate(secilen_ogrenciler):
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
    col_sol, col_sag = st.columns([1.15, 0.85], gap="large")

    with col_sol:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">🎙️ Öğretmen Adayı Müdahale, Eylem Sırası ve Materyal Konsolu</div>', unsafe_allow_html=True)

        sesli_kayit = None
        try:
            sesli_kayit = st.audio_input("🎤 Mikrofonla Sesli Tepkinizi Kaydedin")
        except Exception:
            st.caption("Mikrofon bu tarayıcıda desteklenmiyorsa yazılı alanı kullanabilirsiniz.")

        sesli_girdi_manuel = st.text_area(
            "✍️ Sesli Hitabet / Öğrencilere Söyleyeceğiniz Sözler *",
            placeholder="Seçtiğiniz öğrencilerin düzeyine ve özel gereksinimlerine uygun hitabınızı yazın...",
            height=90,
        )

        eylem_1 = st.selectbox(
            "1. Pedagojik Eylem Adımı *",
            [
                "Seçiniz...",
                "1. Öğrencinin duygusunu kabul edip güvenli alan sunmak (Empati kurmak)",
                "2. Sınıf kurallarını hatırlatıp sessiz olmalarını istemek",
                "3. Durumu görmezden gelip tahtada anlatıma devam etmek",
            ],
        )

        eylem_2 = st.selectbox(
            "2. Pedagojik Eylem Adımı *",
            [
                "Seçiniz...",
                "2. Somut/Dijital materyal üzerinden yönlendirici sorularla keşfettirmek",
                "1. Kuralı veya formülü doğrudan tahtaya yazıp ezberletmek",
                "3. Zorlanılan adımı atlayıp sonraki örneğe geçmek",
            ],
        )

        secilen_materyal = st.selectbox(
            "Kullanılacak Materyal *",
            [
                "Seçiniz...",
                "Somut Materyal (Onluk Taban Blokları, Kesir Takımı, Birim Küpler vb.)",
                "Dinamik Matematik Yazılımı (GeoGebra / Desmos)",
                "Yüksek Kontrastlı Görsel & Dokunsal Kartlar",
                "Günlük Yaşam Nesneleri ve Ölçüm Araçları",
                "Klasik Çalışma Kâğıdı / Formül Listesi",
            ],
        )

        materyal_aciklama = st.text_area(
            "Materyali Nasıl Kullanacaksınız? *",
            placeholder="Seçtiğiniz materyali bu kazanım ve süreç bileşeninde öğrencilere nasıl kullandıracağınızı açıklayın...",
            height=80,
        )

        if st.button("📥 Müdahaleyi Kaydet ve AI Öğrenci Tepkilerini Gör", type="primary", use_container_width=True):
            if (
                (sesli_kayit is None and not sesli_girdi_manuel.strip())
                or eylem_1 == "Seçiniz..."
                or eylem_2 == "Seçiniz..."
                or secilen_materyal == "Seçiniz..."
                or not materyal_aciklama.strip()
            ):
                st.error("Lütfen sesli/yazılı hitabeti, 1. ve 2. eylem sırasını, materyali ve kullanım planını doldurunuz.")
            else:
                kayit_metni = (
                    sesli_girdi_manuel.strip()
                    if sesli_girdi_manuel.strip()
                    else "Mikrofon üzerinden sesli hitabet kaydedildi."
                )
                ai_sonuc_tepkileri = {}
                for ogr_ad in secilen_ogrenciler:
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
                        secilen_materyal,
                    )

                sira_dogru = (
                    eylem_1 == "1. Öğrencinin duygusunu kabul edip güvenli alan sunmak (Empati kurmak)"
                    and eylem_2 == "2. Somut/Dijital materyal üzerinden yönlendirici sorularla keşfettirmek"
                )

                st.session_state.simulasyon_gecmisi.append({
                    "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sinif": secilen_sinif,
                    "tema": secilen_tema,
                    "kod": secilen_kazanim_obj["kod"],
                    "cikti": secilen_kazanim_obj["cikti"],
                    "surec": secilen_surec,
                    "secilen_ogrenciler": list(secilen_ogrenciler),
                    "baslangic_davranislari": baslangic_davranislari,
                    "ai_sonuc_tepkileri": ai_sonuc_tepkileri,
                    "eylem_1": eylem_1,
                    "eylem_2": eylem_2,
                    "sira_dogru": sira_dogru,
                    "materyal": secilen_materyal,
                    "materyal_aciklama": materyal_aciklama.strip(),
                    "sesli_komut": kayit_metni,
                })
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sag:
        st.markdown('<div class="sade-kart">', unsafe_allow_html=True)
        st.markdown('<div class="baslik-mavi">💡 Rubrik Analizi ve Seçili Öğrencilerin AI Tepkileri</div>', unsafe_allow_html=True)
        if st.session_state.simulasyon_gecmisi:
            son_kayit = st.session_state.simulasyon_gecmisi[-1]
            if son_kayit["sira_dogru"]:
                st.success("🌟 **Doğru Pedagojik Eylem Sırası ve Maarif Uyumu:** Önce güvenli alan kurdunuz, ardından materyalle keşfe yönlendirdiniz.")
            else:
                st.error("⚠️ **Geri Dönüt Uyarısı:** Kriz anında önce duyuşsal güven sağlanmalı, ardından hazır kural yerine materyalle keşif yaptırılmalıdır.")

            for ogr_ad, tepki in son_kayit["ai_sonuc_tepkileri"].items():
                st.markdown(f"- {tepki}")

            st.divider()
            if st.button("📋 Detaylı Raporlama Paneline Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()
        else:
            st.info("Müdahalenizi kaydettiğinizde seçtiğiniz tüm öğrencilerin AI tepkileri ve rubrik geri dönütü burada yer alır.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. ADIM 3: ÇOK KATMANLI RAPORLAMA VE ÖĞRETİM ELEMANI DÖNÜT PANELİ
# ==========================================
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 2026 Maarif Modeli Çok Katmanlı Staj Raporlama Sistemi")
    st.markdown(
        f"**Aday:** {st.session_state.get('ogretmen_adi', 'N/A')} | "
        f"**No:** {st.session_state.get('okul_numarasi', 'N/A')} | "
        f"**Kurum:** {st.session_state.get('universite_adi', 'N/A')} | "
        f"**Danışman:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )
    st.divider()

    tab_aday, tab_fakulte, tab_ogretim = st.tabs([
        "👩‍🏫 Aday Gelişim & Dijital Replay",
        "🏛️ Dekanlık Kurumsal Rapor",
        "👨‍🏫 Öğretim Elemanı Raporu & Geri Dönüt",
    ])

    toplam_islem = len(st.session_state.simulasyon_gecmisi)

    with tab_aday:
        if toplam_islem > 0:
            son_adim = st.session_state.simulasyon_gecmisi[-1]
            st.success(f"Oturum ID: #TYMM-{random.randint(10000, 99999)} | {son_adim['sinif']} — {son_adim['tema']}")
            st.markdown(
                f"- **Kazanım:** `{son_adim['kod']}` — {son_adim['cikti']}\n"
                f"- **Süreç Bileşeni:** {son_adim['surec']}\n"
                f"- **Seçilen Öğrenciler ({len(son_adim['secilen_ogrenciler'])}):** {', '.join(son_adim['secilen_ogrenciler'])}\n"
                f"- **Eylem Sırası:** {son_adim['eylem_1']} → {son_adim['eylem_2']}\n"
                f"- **Materyal ve Kullanımı:** {son_adim['materyal']} ({son_adim['materyal_aciklama']})\n"
                f"- **Aday İfadesi:** *\"{son_adim['sesli_komut']}\"*"
            )
            st.markdown("#### 🤖 Seçili Öğrencilerin AI Tepki Kayıtları")
            for ogr_ad, tepki in son_adim["ai_sonuc_tepkileri"].items():
                st.write(f"- {tepki}")

            puanlar = [98, 96, 95, 97] if son_adim["sira_dogru"] else [68, 65, 72, 70]
            chart_data = pd.DataFrame({
                "Kriter": ["Sesli Hitabet", "Kapsayıcı Eğitim", "Maarif Süreci", "Materyal & Aksiyon"],
                "Puan": puanlar,
            })
            st.bar_chart(chart_data, x="Kriter", y="Puan")
        else:
            st.warning("Henüz kayıtlı simülasyon oturumu bulunmuyor.")

        aday_geri_bildirimi = st.text_area("Aday Öz-Değerlendirme ve Yansıtma Notu")
        if st.button("📤 Öz-Değerlendirmeyi Kaydet"):
            if aday_geri_bildirimi.strip():
                st.session_state.simulasyon_gecmisi[-1]["oz_degerlendirme"] = aday_geri_bildirimi.strip()
                st.success("✅ Öz-değerlendirme notunuz kaydedildi.")
            else:
                st.warning("Lütfen yansıtma notunuzu giriniz.")

    with tab_fakulte:
        st.markdown("### 🏛️ Kurumsal Uygunluk Değerlendirmesi")
        st.markdown(
            "1. **TYMM 2026 Uyumu:** Ortaokul matematik öğrenme çıktıları ve süreç bileşenleri temel alınmıştır.\n"
            "2. **Kapsayıcı Sınıf Yönetimi:** Seçilen öğrenci profillerine göre çoklu sınıf dinamiği izlenmiştir.\n"
            "3. **Komisyon Görüşü:** Staj uygulama portfolyosu değerlendirmeye uygundur."
        )

    with tab_ogretim:
        st.markdown("### 👨‍🏫 Öğretim Elemanı Değerlendirme Raporu ve Geri Dönüt")
        st.info(f"**Yüklenen Rubrik:**\n\n{st.session_state.get('rubrik_metni', 'N/A')}")
        if toplam_islem > 0:
            son_adim = st.session_state.simulasyon_gecmisi[-1]
            st.markdown(
                f"**Aday Süreç Özeti:** `{son_adim['kod']}` | **{son_adim['surec']}** | "
                f"**Seçilen Öğrenciler:** {', '.join(son_adim['secilen_ogrenciler'])} | "
                f"**Materyal:** {son_adim['materyal']}"
            )
            st.write(f"**Aday Öz-Değerlendirmesi:** {son_adim.get('oz_degerlendirme', 'Henüz girilmedi.')}")

        hoca_notu = st.text_area("Danışman Öğretim Elemanı Geri Dönütü")
        if st.button("📤 Geri Dönütü Kaydet", type="primary"):
            if hoca_notu.strip():
                st.success("✅ Danışman öğretim elemanı geri dönütü kaydedildi.")
            else:
                st.warning("Lütfen geri dönüt metni giriniz.")

    st.divider()
    if st.button("🔄 Yeni Bir 3D Staj Simülasyonu Başlat"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.adim = 1
        st.rerun()
