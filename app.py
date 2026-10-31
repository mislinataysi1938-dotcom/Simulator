import datetime
import json
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Ortaokul Matematik Eğitimi - TYMM 2026 3B Staj Simülatörü",
    page_icon="📐",
    layout="wide",
)

if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "uygulama_degerlendirmeleri" not in st.session_state:
    st.session_state.uygulama_degerlendirmeleri = []
if "adim" not in st.session_state:
    st.session_state.adim = 1

# ==========================================
# 1. ORTAOKUL MATEMATİK BÖLÜMÜ İÇİN CİNSİYETLERİ BELİRLENMİŞ 10 DETAYLI ÖĞRENCİ PROFİLİ
# ==========================================
genel_ogrenci_tipleri_detayli = [
    {
        "id": "disleksi", "ad": "Kerem", "cinsiyet": "Erkek", "tip": "Disleksili Öğrenci", "renk": "#ef4444", "bg": "rgba(239, 68, 68, 0.25)",
        "karakteristik": "Harf, sembol ve basamak terslikleri yaşar; çok adımlı sembolik dizilimleri okurken bilişsel yorgunluk hisseder.",
        "hitabet_rehberi": "Kerem'e asla hızlı sözlü komutlar vermeyin. Sayıları ve basamakları renk kodlu somut nesnelerle (abaküs/tablo) eşleştirin. Hata yaptığında yargılamadan 'Gel birlikte parmağımızla takip edelim' diyerek güvenli alan kurun.",
        "kriz_yuz": "😣", "kriz_postur": "🤦‍♂️", "kriz_mimik": "Alnını ovuşturuyor, basamakları karıştırıyor", "kriz_tepki": "Bilişsel yük arttı, sembolleri okuyamıyor",
        "kriz_konusma": "Öğretmenim sayılar birbirine giriyor, okurken sırasını şaşırdım...",
        "dogru_yuz": "😊", "dogru_postur": "🙌", "dogru_mimik": "Yüzü aydınlandı, materyali takip ediyor", "dogru_tepki": "Renk kodlu somut materyalle basamakları kavradı",
        "dogru_konusma": "Renk kodlu abaküsle görünce hiç karışmadı öğretmenim!"
    },
    {
        "id": "otizm", "ad": "Arda", "cinsiyet": "Erkek", "tip": "Otizm Spektrumlu Öğrenci", "renk": "#10b981", "bg": "rgba(16, 185, 129, 0.25)",
        "karakteristik": "Ani seslerden ve yönerge değişiminden duyusal rahatsızlık duyar. Sakin ses tonuna ve yapılandırılmış net adımlara ihtiyaç gösterir.",
        "hitabet_rehberi": "Arda ile iletişimde sakin, alçak ve net bir ses tonu kullanın. Rutini bozmadan, yapacağı adımları teker teker ve yazılı/görsel olarak önceden açıklayın.",
        "kriz_yuz": "😖", "kriz_postur": "🎧", "kriz_mimik": "Ellerini kulaklarına götürüyor, sallanıyor", "kriz_tepki": "Duyusal aşırı yüklenme ve belirsizlik krizi",
        "kriz_konusma": "Çok ses var ve sıra bozuldu! Şimdi ne yapacağız?",
        "dogru_yuz": "🙂", "dogru_postur": "🧩", "dogru_mimik": "Sakinleşti, omuzları gevşedi, modele odaklandı", "dogru_tepki": "Sakin ses tonu ve net yönergeyle güven kazandı",
        "dogru_konusma": "Adımları sırayla söylediğiniz için çok rahatladım öğretmenim."
    },
    {
        "id": "ustun", "ad": "Can", "cinsiyet": "Erkek", "tip": "Üstün Yetenekli Öğrenci", "renk": "#f59e0b", "bg": "rgba(245, 158, 11, 0.25)",
        "karakteristik": "Rutin işlemleri çabuk kavrar. Derinleştirici, ispat edici ve zenginleştirilmiş sorularla beslenmezse egosal çatışma çıkarır.",
        "hitabet_rehberi": "Can'a doğrudan basit formüller vermek yerine 'Bu kuralın her durumda çalıştığını nasıl ispatlarsın?' gibi zenginleştirici ve ispat odaklı üst düzey sorular yöneltin.",
        "kriz_yuz": "😤", "kriz_postur": "🙋‍♂️", "kriz_mimik": "Sabırsızca el kaldırıyor, kaşları çatık", "kriz_tepki": "Temel anlatımdan sıkıldı, kuralı sorguluyor",
        "kriz_konusma": "Hocam bu çok basit, neden doğrudan ispatına geçmiyoruz?",
        "dogru_yuz": "🤩", "dogru_postur": "💡", "dogru_mimik": "Gözleri parlıyor, yeni kanıt arıyor", "dogru_tepki": "Zenginleştirilmiş sorgulama ile üretime yönlendirildi",
        "dogru_konusma": "Model üzerinden genel formülün kanıtını buldum öğretmenim!"
    },
    {
        "id": "kaygili", "ad": "Elif", "cinsiyet": "Kız", "tip": "Yüksek Kaygılı / STU-1309", "renk": "#38bdf8", "bg": "rgba(56, 189, 248, 0.25)",
        "karakteristik": "Hata yapmaktan aşırı derecede çekinir. Baskı altında zihinsel blokaj yaşar; somut materyalle güvenli keşif ortamında açılır.",
        "hitabet_rehberi": "Elif'e asla doğrudan 'Tahtaya kalk çöz' baskısı yapmayın. 'Hata yapmak öğrenmenin en güzel parçasıdır, gel birlikte model üzerinde deneyelim' diyerek duyuşsal güven sağlayın.",
        "kriz_yuz": "😰", "kriz_postur": "🙇‍♀️", "kriz_mimik": "Başını sıraya eğmiş, kalemini sıkıyor", "kriz_tepki": "Hata yapma korkusuyla zihinsel kilitlenme yaşadı",
        "kriz_konusma": "Ya yanlış yaparsam ve gülerlerse? Korkudan yazamıyorum...",
        "dogru_yuz": "😄", "dogru_postur": "✍️", "dogru_mimik": "Başını kaldırdı, özgüvenle gülümsüyor", "dogru_tepki": "Güvenli alan ve somut materyal ile kaygısını yendi",
        "dogru_konusma": "Ezberlemek zorunda olmadığımı bilmek beni çok rahatlattı!"
    },
    {
        "id": "mukemmeliyetci", "ad": "Zeynep", "cinsiyet": "Kız", "tip": "Mükemmeliyetçi Öğrenci", "renk": "#8b5cf6", "bg": "rgba(139, 92, 246, 0.25)",
        "karakteristik": "En küçük hesap hatasında tüm kağıdı yırtmak ister. Süreç odaklı olmaktan ziyade kusursuz sonuca odaklıdır.",
        "hitabet_rehberi": "Zeynep'e sonucun küsuratlı veya çizimin ufak hatalı olmasının normal olduğunu, önemli olanın 'matematiksel muhakeme süreci' olduğunu vurgulayın.",
        "kriz_yuz": "🧐", "kriz_postur": "📝", "kriz_mimik": "Kağıdı titizlikle inceliyor, küçük bir kayma için stresli", "kriz_tepki": "Ufak detay takıntısı nedeniyle zaman yönetimi bozuldu",
        "kriz_konusma": "Çizimim milimetrik kaydı, hepsini silip baştan yapmalıyım!",
        "dogru_yuz": "😌", "dogru_postur": "👍", "dogru_mimik": "Rahatladı, sürecin kendisine odaklandı", "dogru_tepki": "Süreç odaklı geri bildirimle mantığa odaklandı",
        "dogru_konusma": "Önemli olanın çözüm stratejim olduğunu anlamak beni rahatlattı."
    },
    {
        "id": "direncli", "ad": "Mert", "cinsiyet": "Erkek", "tip": "Ödev/Kural Direnci Gösteren", "renk": "#64748b", "bg": "rgba(100, 116, 139, 0.25)",
        "karakteristik": "Otoriteye direnç gösterir. Konunun gerçek yaşamda ne işe yarayacağını somut olarak görmeden katılmak istemez.",
        "hitabet_rehberi": "Mert'e kuralı ezberletmeyin. Dersin başındaki 'Gerçek Yaşam Kancası'nı hatırlatarak bu matematiğin mesleklerde veya günlük hayatta nasıl hayat kurtardığını gösterin.",
        "kriz_yuz": "😒", "kriz_postur": "🚶‍♂️", "kriz_mimik": "Kollarını kavuşturmuş, arkasına yaslanmış", "kriz_tepki": "Kural ezberlemeye direnç gösteriyor",
        "kriz_konusma": "Bunu hayatta hiçbir yerde kullanmayacağız, yapmıyorum.",
        "dogru_yuz": "🤔", "dogru_postur": "💡", "dogru_mimik": "İlgiyle tahtaya ve gerçek yaşam kancasına bakıyor", "dogru_tepki": "Gerçek yaşam bağlamı ile ikna oldu",
        "dogru_konusma": "Günlük hayattaki karşılığını görünce mantıklı geldiğini kabul ediyorum."
    },
    {
        "id": "icedonuk", "ad": "Merve", "cinsiyet": "Kız", "tip": "Sosyal İçe Dönük Öğrenci", "renk": "#ec4899", "bg": "rgba(236, 72, 153, 0.25)",
        "karakteristik": "Doğrudan hedef tahtası olmaktan kaçınır. Fikirlerini önce bireysel veya küçük akran grubunda paylaşmayı tercih eder.",
        "hitabet_rehberi": "Merve'ye tüm sınıfın önünde ani sorular sormayın. Birebir masasına giderek fısıltıyla rehberlik edin veya ikili küçük gruplarda çalışmasını sağlayın.",
        "kriz_yuz": "😶", "kriz_postur": "🪞", "kriz_mimik": "Başını öne eğmiş, göz temasından kaçınıyor", "kriz_tepki": "Topluluk baskısı nedeniyle kapandı",
        "kriz_konusma": "Lütfen beni tahtaya kaldırmayın, herkes bakınca konuşamıyorum...",
        "dogru_yuz": "🙂", "dogru_postur": "📖", "dogru_mimik": "Sakin bir şekilde sıra arkadaşıyla çalışıyor", "dogru_tepki": "Güvenli küçük grup çalışmasıyla sürece katıldı",
        "dogru_konusma": "Bana topluluk önünde baskı yapmadan birebir sormanız rahat hissettirdi."
    },
    {
        "id": "hareketli", "ad": "Emre", "cinsiyet": "Erkek", "tip": "Aşırı Hareketli / Dürtüsel", "renk": "#3b82f6", "bg": "rgba(59, 130, 246, 0.25)",
        "karakteristik": "Sırada sabit oturan kalamaz, nesnelerle oynamak ister. Kinestetik ve fiziksel manipülatif görev sorumluluğu verilmelidir.",
        "hitabet_rehberi": "Emre'nin enerjisini bastırmak yerine, materyali bizzat tahtada veya masada hareket ettiren 'görevli kişi' yaparak enerjisini matematiksel keşfe yönlendirin.",
        "kriz_yuz": "🤪", "kriz_postur": "🤸‍♂️", "kriz_mimik": "Sırada kıpırdanıp duruyor, kalemiyle oynuyor", "kriz_tepki": "Pasif dinlemede enerjisini yönetemedi",
        "kriz_konusma": "Hocam tahtaya ben kalkıp materyali hareket ettireyim mi?",
        "dogru_yuz": "🤩", "dogru_postur": "🛠️", "dogru_mimik": "Materyali büyük bir dikkatle kurup kullanıyor", "dogru_tepki": "Kinestetik görev ile enerjisi odaklandı",
        "dogru_konusma": "Modeli kurma görevini bana verdiğiniz için hiç sıkılmadım!"
    },
    {
        "id": "sozelgucluk", "ad": "Burak", "cinsiyet": "Erkek", "tip": "Sözel İfade Güçlüğü Yaşayan", "renk": "#14b8a6", "bg": "rgba(20, 184, 166, 0.25)",
        "karakteristik": "Matematiksel mantığı bilir ancak sözel terimleri organize edemez. Görsel ve yazılı modellerle kendini rahat ifade eder.",
        "hitabet_rehberi": "Burak'tan tanım ve terimleri sözlü olarak ezberden söylemesini istemeyin. 'Kelimeyi bulamıyorsan model üzerinde parmağınla göster' diyerek görsel anlatımı teşvik edin.",
        "kriz_yuz": "🤔", "kriz_postur": "🤷‍♂️", "kriz_mimik": "Kelimeleri arıyor, elleriyle havada şekiller çiziyor", "kriz_tepki": "Sözel ifade baskısı nedeniyle tıkanıp kaldı",
        "kriz_konusma": "Cevabı biliyorum ama hani o terim vardı ya, söyleyemiyorum!",
        "dogru_yuz": "😃", "dogru_postur": "👉", "dogru_mimik": "Modeli işaret ederek parmağıyla gösteriyor", "dogru_tepki": "Görsel ve somut temsil ile kendini ifade etti",
        "dogru_konusma": "Model üstünde göstererek anlatmama izin verdiğiniz için tam açıklayabildim."
    },
    {
        "id": "gorseluzamsal", "ad": "Selin", "cinsiyet": "Kız", "tip": "Görsel/Uzamsal Ağırlıklı", "renk": "#84cc16", "bg": "rgba(132, 204, 22, 0.25)",
        "karakteristik": "Saf sözel formüllerde zorlanır; geometrik şekilleri, simetrileri ve uzamsal ilişkileri anında görsel olarak kavrar.",
        "hitabet_rehberi": "Selin'e asla tahtaya düz formül yazarak ders anlatmayın. Geometrik şemalar, izometrik kağıtlar ve 3B uzamsal çizimler üzerinden konuyu görselleştirin.",
        "kriz_yuz": "🎨", "kriz_postur": "👁️", "kriz_mimik": "Tahtadaki düz yazıya bakıp kafasını kaşıyor", "kriz_tepki": "Saf sözel anlatım uzamsal zekasına hitap etmedi",
        "kriz_konusma": "Sözel formülü okuduğumda anlamıyorum ama çizimini yaparsanız anlarım.",
        "dogru_yuz": "😎", "dogru_postur": "📐", "dogru_mimik": "Geometrik şemayı ve 3B modeli büyük ilgiyle inceliyor", "dogru_tepki": "Görsel şema ile konuyu anında kavradı",
        "dogru_konusma": "Görsel şema üzerinden anlatınca taşlar tam yerine oturdu."
    },
]

materyal_havuzu = [
    "Oran Tahtası ve Renkli Boncuklar",
    "Onluk Taban Blokları ve Sayı Doğrusu",
    "Birim Küpler ve 3B Prizma Modelleri",
    "Cebir Karoları ve Eşit Kollu Terazi",
    "Simetri Aynası ve İzometrik Noktalı Kağıt",
    "GeoGebra Dinamik Geometri ve 3B Yazılımı",
    "Basamak Tablosu ve Renkli Abaküs",
    "Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar",
    "Olasılık Spektrumu Şeridi ve Renkli Çark",
    "KVKK Etkileşimli Veri Toplama ve Grafik Panosu",
]

# Yapılandırılmış Materyal Adım Adım Kullanım Yönerge Rehberi
materyal_adim_rehberi = {
    "Oran Tahtası ve Renkli Boncuklar": "1. Adım: Tahtadaki sabit eksenleri gösterin.\n2. Adım: Boncuk sayısını artırarak aradaki mesafenin değişimini inceletin.\n3. Adım: Kat oranının sabit kalıp kalmadığını öğrenciye soru olarak yöneltin.",
    "Onluk Taban Blokları ve Sayı Doğrusu": "1. Adım: Birlik, onluk ve yüzlük blokları somut olarak masaya koyun.\n2. Adım: Sayı doğrusu üzerinde sıçramalar yaparak toplama/çıkarma işlemini modelletin.\n3. Adım: Öğrencinin zihinden stratejisini bloklar üzerinde test etmesini isteyin.",
    "Birim Küpler ve 3B Prizma Modelleri": "1. Adım: 24 birim küpü masaya verin.\n2. Adım: Farklı boyutlarda (1x1x24, 2x3x4 vb.) dikdörtgen prizmalar oluşturun.\n3. Adım: Hacmin sabit kalırken yüzey alanının nasıl değiştiğini inceletin.",
    "Cebir Karoları ve Eşit Kollu Terazi": "1. Adım: Terazinin iki kefesine eşit kütleli karolar yerleştirin.\n2. Adım: Bir kefeden eleman eksiltirken diğer kefede yapılan aynı işlemi simüle edin.\n3. Adım: Eşitliğin korunumu ilkesini denklem çözümüne uyarlayın.",
    "Simetri Aynası ve İzometrik Noktalı Kağıt": "1. Adım: Noktalı kağıda temel bir çokgen çizin.\n2. Adım: Simetri aynasını doğru üzerine dik yerleştirip yansıma görüntüyü gözletin.\n3. Adım: Uzamsal dönüşüm koordinat değişimini şemalaştırın.",
    "GeoGebra Dinamik Geometri ve 3B Yazılımı": "1. Adım: Akıllı tahtada GeoGebra 3B ekranını açın.\n2. Adım: Doğruları veya cisimleri dinamik olarak hareket ettirin.\n3. Adım: Öğrencinin ekrandaki değişimi kendi gözleriyle gözlemlemesini sağlayın.",
    "Basamak Tablosu ve Renkli Abaküs": "1. Adım: Abaküsteki çubukları birler, onlar ve yüzler olarak renklendirin.\n2. Adım: Çok basamaklı sayıyı boncuklarla abaküse işleyin.\n3. Adım: Bölükler arası okunuş farkını tablodan okutun.",
    "Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar": "1. Adım: Bütünü temsil eden çubuğu ortaya koyun.\n2. Adım: Farklı birim kesirleri yan yana getirerek büyüklük ilişkisini kurdurun.\n3. Adım: Payda büyüdükçe parçanın neden küçüldüğünü görselleştirin.",
    "Olasılık Spektrumu Şeridi ve Renkli Çark": "1. Adım: Spektrum şeridini 'imkânsız'dan 'kesin'e kadar tahtaya asın.\n2. Adım: Çarkı çevirip gelen sonucu spektrum üzerinde konumlandırın.\n3. Adım: Öznel ve teorik olasılık farkını tartışın.",
    "KVKK Etkileşimli Veri Toplama Panosu": "1. Adım: Kategorik veri için etik araştırma sorusu belirleyin.\n2. Adım: Kişisel verileri koruma (KVKK) ilkelerine uygun şekilde verileri toplayın.\n3. Adım: Sıklık tablosu ve sütun grafiği ile panoda görselleştirin.",
}

# 2026 TYMM Ortaokul Matematik Öğretim Programı Master Arşivi
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: İşlemlerle Cebirsel Düşünme",
            "3. Tema: Geometrik Şekiller",
            "4. Tema: Geometrik Nicelikler",
            "5. Tema: İstatistiksel Araştırma Süreci",
            "6. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
                    "surec": [
                        "a) Günlük hayattaki bağlamlardan yola çıkarak çok basamaklı sayılar hakkında bilgi toplar.",
                        "b) Sayıların bölükleri ve basamakları ile okunuşları arasındaki ortak özellikleri belirler.",
                        "c) Sayıların bölükleri ile okunuşları arasındaki farklılıkları belirler.",
                        "ç) Örüntüler üzerinden basamak sayısı çok olan sayıların okunuş ve yazılışları hakkında önermelerde bulunur.",
                    ],
                    "uygun_materyaller": ["Basamak Tablosu ve Renkli Abaküs", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Millî Kütüphane'deki 405.020 adet tarihi el yazması kitabın arşiv kodlama sistemi.",
                    "kriz": "Kerem tahtadaki çok basamaklı sayıyı okurken bölüklerdeki rakamların yerini karıştırır, sınıfta gülüşmeler başlar.",
                    "odak": "disleksi",
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) İşlem gerektiren günlük yaşam durumlarında verilen ve istenen nicelikleri belirler.",
                        "b) Doğal sayılarla zihinden işlem ve tahmin stratejileri geliştirir.",
                        "c) Geliştirdiği stratejileri uygulayarak ulaştığı sonuçların anlamlılığını değerlendirir.",
                    ],
                    "uygun_materyaller": ["Onluk Taban Blokları ve Sayı Doğrusu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Okul kermesinde toplanan bağışların hedef bütçe ile karşılaştırılması.",
                    "kriz": "Can zihinden işlem stratejisini dinlemeyip 'Ben zaten sonucu buldum, neden uzatıyoruz?' diyerek araya girer.",
                    "odak": "ustun",
                },
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.5.1.3",
                    "cikti": "Gerçek yaşam durumlarına karşılık gelen kesirleri farklı biçimlerde (bileşik, tam sayılı, ondalık ve yüzde) temsil edebilme",
                    "surec": [
                        "a) Kesirlerin farklı gösterimlerini somut modeller üzerinde inceler.",
                        "b) Bileşik, tam sayılı kesir, ondalık ve yüzde gösterimleri arasındaki dönüşümleri ilişkilendirir.",
                        "c) Bağlama uygun kesir gösterimini seçerek gerçek yaşam durumlarını yorumlar.",
                    ],
                    "uygun_materyaller": ["Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Market indirim afişlerindeki yüzde sembolleri ile kasa fişindeki ondalık gösterimlerin karşılaştırılması.",
                    "kriz": "Elif payda büyüdükçe birim kesir değerinin neden küçüldüğünü anlayamadığını söyleyerek kaygılanır.",
                    "odak": "kaygili",
                }
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.5.2.1",
                    "cikti": "Eşitliğin korunumu ve işlem özelliklerini (değişme, birleşme, dağılma) muhakeme edebilme",
                    "surec": [
                        "a) Eşit kollu terazi modelleri üzerinde eşitliğin korunumu durumlarını inceler.",
                        "b) İşlem özelliklerini kullanarak eşitliklerin korunduğuna yönelik varsayımlarda bulunur.",
                        "c) İşlem önceliği kurallarını içeren günlük yaşam durumlarını çözümler.",
                    ],
                    "uygun_materyaller": ["Cebir Karoları ve Eşit Kollu Terazi", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Laboratuvardaki eşit kollu terazide farklı kütleleri dengeleme deneyi.",
                    "kriz": "Can eşittir işaretinin sadece 'işlem sonucu' demek olmadığını, sınıftakilerin bunu yanlış bildiğini sertçe söyler.",
                    "odak": "ustun",
                },
                {
                    "kod": "MAT.5.2.2",
                    "cikti": "Sayı ve şekil örüntülerinin kuralını bularak algoritmik düşünme süreçlerini yürütebilme",
                    "surec": [
                        "a) Tekrarlayan ve genişleyen örüntülerdeki adımlar arası değişimi belirler.",
                        "b) Örüntünün genel kuralını sözel ve sembolik olarak ifade eder.",
                        "c) Temel algoritmik akış şeması üzerinde örüntü adımlarını test eder.",
                    ],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Geleneksel Türk çini motiflerindeki geometrik dizilimlerin adımlarını modelleme.",
                    "kriz": "Arda şekil örüntüsündeki renklerin sırası değiştiğinde duyusal huzursuzluk yaşayıp kulaklarını kapatır.",
                    "odak": "otizm",
                },
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.5.3.1",
                    "cikti": "Temel geometrik çizimler için matematiksel araç ve teknolojileri kullanabilme",
                    "surec": [
                        "a) Nokta, doğru, doğru parçası ve ışın kavramlarını inşa araçlarıyla inceler.",
                        "b) Açıları açıölçer ve dinamik geometri yazılımıyla ölçerek sınıflandırır.",
                        "c) Çokgenleri ve çemberi temel elemanlarıyla inşa eder.",
                    ],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri ve 3B Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Mimari kroki çizimlerinde açıölçer ve pergel kullanarak simetrik bahçe tasarımı yapma.",
                    "kriz": "Kerem açıölçerin iç ve dış kadranındaki dereceleri ters okur ve çizimini silip defterini kapatır.",
                    "odak": "disleksi",
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.4.1",
                    "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkiyi yapılandırabilme",
                    "surec": [
                        "a) Birim kareler kullanarak dikdörtgenin alanını ve çevresini modeller.",
                        "b) Aynı çevre uzunluğuna sahip farklı dikdörtgenlerin alanlarını karşılaştırır.",
                        "c) Aynı alana sahip farklı dikdörtgenlerin çevre uzunluklarını muhakeme eder.",
                    ],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Okul bahçesine sabit uzunluktaki çitle en geniş alana sahip hobi bahçesi kurma.",
                    "kriz": "Elif alan ile çevre formüllerini birbirine karıştırıp hata yapma korkusuyla ağlamaklı olur.",
                    "odak": "kaygili",
                }
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.5.1",
                    "cikti": "Kategorik verilerle istatistiksel araştırma sürecini yürütebilme",
                    "surec": [
                        "a) Kategorik veri toplamayı gerektiren araştırma sorusu oluşturur.",
                        "b) Verileri toplar, sıklık tablosu ve sütun grafiği ile görselleştirir.",
                        "c) Elde edilen bulguları araştırma sorusu bağlamında yorumlar.",
                    ],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama ve Grafik Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Sınıf kütüphanesine alınacak kitap türlerini belirlemek için veri toplama.",
                    "kriz": "Merve grup arkadaşlarıyla konuşmaktan çekinip anket verilerini paylaşmayı reddeder.",
                    "odak": "icedonuk",
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.6.1",
                    "cikti": "Olayların olasılığını olasılık spektrumu (imkânsızdan kesine) üzerinde öznel olarak yorumlayabilme",
                    "surec": [
                        "a) Günlük yaşam olaylarını gerçekleşme ihtimallerine göre inceler.",
                        "b) Olayları imkânsız, daha az olası, eşit olası, daha çok olası ve kesin olarak sınıflandırır.",
                        "c) Olasılık spektrumu üzerindeki yerleşimleri gerekçelendirir.",
                    ],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Renkli Çark", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Hava durumu raporlarına göre hafta sonu yağmur yağma ihtimalini tartışma.",
                    "kriz": "Emre sınıfta ayağa kalkıp olasılık spektrumu şeridini havaya fırlatır.",
                    "odak": "hareketli",
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
                    "cikti": "Doğal sayıların çarpan, kat ve asal sayı özelliklerine yönelik muhakeme yapabilme",
                    "surec": [
                        "a) Doğal sayıların çarpan ve katlarına yönelik varsayımlarda bulunur.",
                        "b) Bölünebilme kurallarını ve asal çarpanları örüntüler üzerinden geneller.",
                        "c) Ortak kat ve ortak bölen kavramlarını gerçek yaşam durumlarında doğrular.",
                    ],
                    "uygun_materyaller": ["Basamak Tablosu ve Renkli Abaküs", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Farklı periyotlarla sefer yapan iki vapurun iskelede aynı anda buluşma saatlerini planlama.",
                    "kriz": "Mert 'Bu kuralları ezberlemek zorunda mıyız, hayatta ne işimize yarayacak?' diyerek etkinliği reddeder.",
                    "odak": "direncli",
                }
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.6.1.2",
                    "cikti": "Kesirlerle ve ondalık gösterimlerle işlemleri içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Kesirlerle çarpma ve bölme işlemlerini alan ve sayı doğrusu modelleriyle anlamlandırır.",
                        "b) Ondalık gösterimlerle dört işlem stratejileri geliştirir.",
                        "c) Çözüm sonuçlarının bağlama uygunluğunu kontrol eder.",
                    ],
                    "uygun_materyaller": ["Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Tasarım atölyesinde kumaş parçalarını eşit kesirli ölçülerde bölüştürme.",
                    "kriz": "Elif iki basit kesir çarpıldığında sonucun neden çarpanlardan daha küçük çıktığını anlamayıp panikler.",
                    "odak": "kaygili",
                }
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.6.2.1",
                    "cikti": "Bilinmeyen nicelikleri değişkenlerle temsil edebilme ve cebirsel ifadeleri anlamlandırabilme",
                    "surec": [
                        "a) Sözel olarak verilen durumları değişken kullanarak cebirsel ifadeye dönüştürür.",
                        "b) Cebirsel ifadelerin farklı doğal sayı değerleri için sonuçlarını hesaplar.",
                        "c) Aritmetik dizilerin kuralını harfli ifadelerle ve algoritmalarla modeller.",
                    ],
                    "uygun_materyaller": ["Cebir Karoları ve Eşit Kollu Terazi", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Kumbaraya her hafta sabit miktarda eklenen paranın n. haftadaki toplam tutarını modelleme.",
                    "kriz": "Kerem matematikte sayıların arasına harflerin (x, y) girmesine tepki gösterip sembolleri karıştırır.",
                    "odak": "disleksi",
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1",
                    "cikti": "Paralel iki doğrunun bir kesenle yaptığı açıları, üçgen ve dörtgenlerin özelliklerini keşfedebilme",
                    "surec": [
                        "a) Paralel doğrular ve kesen arasındaki yöndeş, iç ters ve dış ters açıları dinamik yazılımla inceler.",
                        "b) Üçgen ve dörtgenlerin iç açıları toplamına yönelik varsayımları test eder.",
                        "c) Çokgenlerin köşegen, kenar ve açı özelliklerini sınıflandırır.",
                    ],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri ve 3B Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Demiryolu makas kesişimlerindeki ve köprü kirişlerindeki açıların dengesini inceleme.",
                    "kriz": "Arda dinamik geometri ekranındaki doğrular hızlı hareket ettirildiğinde duyusal rahatsızlık yaşar.",
                    "odak": "otizm",
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.1",
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarını dikdörtgenin alanından yararlanarak oluşturabilme",
                    "surec": [
                        "a) Paralelkenarı kes-yapıştır stratejisiyle dikdörtgene dönüştürerek alan bağıntısını bulur.",
                        "b) Üçgenin alanını paralelkenar ve dikdörtgen alanı üzerinden geneller.",
                        "c) Çemberin çevre uzunluğu ile çapı arasındaki oranı (pi) keşfeder.",
                    ],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "Birim Küpler ve 3B Prizma Modelleri"],
                    "hook": "Üçgen ve paralelkenar şeklindeki tarım parsellerinin sulama alanlarını hesaplama.",
                    "kriz": "Selin sözel alan formülünü ezberleyemediği için çizim olmadan soruyu çözmeyi bırakır.",
                    "odak": "gorseluzamsal",
                }
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": "Nicel kesikli verilerle kök-yaprak gösterimi oluşturabilme ve merkezi eğilim ölçülerini yorumlayabilme",
                    "surec": [
                        "a) Nicel kesikli veri toplar ve kök-yaprak gösterimi ile organize eder.",
                        "b) Aritmetik ortalama, ortanca (medyan) ve tepe değer (mod) ölçülerini hesaplar.",
                        "c) Uç değerlerin aritmetik ortalama üzerindeki etkisini muhakeme eder.",
                    ],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Okul basketbol takımındaki oyuncuların maç başına attıkları sayıların istatistiksel analizi.",
                    "kriz": "Zeynep tablo çiziminde küçük bir kayma olunca tüm kağıdını yırtıp ağlamaklı olur.",
                    "odak": "mukemmeliyetci",
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1",
                    "cikti": "Bir olayın deneysel olasılığını deneme sayısına bağlı göreli sıklık üzerinden tahmin edebilme",
                    "surec": [
                        "a) Tekrarlı olasılık deneyleri tasarlar ve sonuçların çetelesini tutar.",
                        "b) Göreli sıklığı hesaplayarak deneysel olasılık değerini belirler.",
                        "c) Deneme sayısı arttıkça göreli sıklığın nasıl değiştiğini yorumlar.",
                    ],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Dijital simülasyonla 10, 100 ve 1000 kez atılan hilesiz zarın üst yüzüne gelen sayıların analizi.",
                    "kriz": "Emre deney zarlarını masanın üstüne fırlatıp sınıfın dikkatini dağıtır.",
                    "odak": "hareketli",
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
                    "cikti": "Tam sayılar ve rasyonel sayılarla işlemler içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Tam sayılardan rasyonel sayılara geçişi sayı doğrusu ve sayma pullarıyla modeller.",
                        "b) Rasyonel sayılarla dört işlem özelliklerini ve stratejilerini uygular.",
                        "c) Çok adımlı rasyonel sayı problemlerini çözerek sonuçların anlamlılığını değerlendirir.",
                    ],
                    "uygun_materyaller": ["Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Hava sıcaklığı değişimleri, deniz altı dalış derinlikleri ve finansal bütçe hesaplamaları.",
                    "kriz": "Kerem negatif rasyonel sayılarda eksi işaretinin pay, payda veya kesir çizgisi önünde olmasını karıştırır.",
                    "odak": "disleksi",
                }
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {
                    "kod": "MAT.7.1.2",
                    "cikti": "Oran ve orantı kavramlarını yapılandırarak doğru ve ters orantı problemlerini muhakeme edebilme",
                    "surec": [
                        "a) Oran Tahtası ve somut materyaller üzerinde çokluklar arası çarpımsal ilişkiyi inceler.",
                        "b) Doğru ve ters orantılı nicelikler arasındaki değişim sabiti örüntüsünü belirler.",
                        "c) Gerçek yaşam durumlarındaki orantı problemlerini farklı stratejilerle çözer.",
                    ],
                    "uygun_materyaller": ["Oran Tahtası ve Renkli Boncuklar", "Cebir Karoları ve Eşit Kollu Terazi"],
                    "hook": "Görsel sanatlar atölyesinde renk karışım oranları ve ölçekli maket tasarımı.",
                    "kriz": "Elif Oran Tahtası üzerindeki boncuk sayısını artırırken hata yapmaktan korkarak materyale dokunamaz.",
                    "odak": "kaygili",
                }
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.7.2.1",
                    "cikti": "Cebirsel ifadelerle işlemler yapabilme, birinci dereceden bir bilinmeyenli denklem ve eşitsizlikleri çözebilme",
                    "surec": [
                        "a) Cebirsel ifadelerle toplama, çıkarma ve çarpma işlemlerini cebir karolarıyla modeller.",
                        "b) Eşitliğin korunumu ilkesiyle birinci dereceden denklemleri çözer.",
                        "c) Günlük yaşam durumlarını eşitsizliklerle ifade ederek sayı doğrusunda gösterir.",
                    ],
                    "uygun_materyaller": ["Cebir Karoları ve Eşit Kollu Terazi", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Asansör taşıma kapasitesi sınırları ve kargo ağırlık ücretlendirme algoritmaları.",
                    "kriz": "Burak denklemin çözüm mantığını zihninde kurmasına rağmen sözel olarak açıklarken kelimeleri bulamaz.",
                    "odak": "sozelgucluk",
                }
            ],
            "3. Tema: Dönüşüm": [
                {
                    "kod": "MAT.7.3.1",
                    "cikti": "Düzlemde şekillerin doğruya göre yansıma dönüşümünü ve simetri inşalarını gerçekleştirebilme",
                    "surec": [
                        "a) Geometrik şekillerin simetri doğrularına göre yansıma görüntülerini inceler.",
                        "b) Yansıma dönüşümünde şekil ile görüntüsü arasındaki eşlik özelliklerini belirler.",
                        "c) Dijital matematik araçlarıyla yansıma tasarımları oluşturur.",
                    ],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Mimari cephe tasarımlarında ve kilim desenlerinde ayna simetrisi analizi.",
                    "kriz": "Selin görsel model gösterilmeden sadece sözel yansıma kuralı verildiğinde şekli çizemez.",
                    "odak": "gorseluzamsal",
                }
            ],
            "4. Tema: Geometrik Nicelikler (1)": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": "Özel dörtgenlerin (eşkenar dörtgen, yamuk) ve dairenin alan bağıntılarını yapılandırabilme",
                    "surec": [
                        "a) Eşkenar dörtgen ve yamuğun alan bağıntılarını bilinen çokgenlerin alanlarından türetir.",
                        "b) Dairenin ve daire diliminin alanını merkez açı ile ilişkilendirir.",
                        "c) Gerçek yaşam problemlerinde alan hesaplamalarını uygular.",
                    ],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri ve 3B Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Dairesel döner kavşak peyzaj tasarımı ve yamuk parsellerin alan hesabı.",
                    "kriz": "Zeynep pi sayısının küsuratlı çıkması nedeniyle alanın tam sayı olmamasına takılıp işlemi siler.",
                    "odak": "mukemmeliyetci",
                }
            ],
            "4. Tema: Geometrik Nicelikler (2)": [
                {
                    "kod": "MAT.7.4.2",
                    "cikti": "Dik prizmaların yüzey alanı ve hacim bağıntılarını somut ve dijital modellerle oluşturabilme",
                    "surec": [
                        "a) Birim küpler kullanarak dikdörtgenler prizmasının hacmini farklı boyutlarla modeller.",
                        "b) Dik prizmaların açınımlarını inceleyerek yüzey alanı bağıntısını kurar.",
                        "c) Hacim ve yüzey alanı içeren gerçek yaşam problemlerini çözer.",
                    ],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Çikolata fabrikası için 24 birim küpten oluşan farklı boyutlarda prizmatik ambalaj tasarımı.",
                    "kriz": "Arda birim küplerin masaya düşüp çıkardığı sesten rahatsız olur ve kulaklarını kapatır.",
                    "odak": "otizm",
                }
            ],
            "5. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Üçgende kenarortay, açıortay ve yükseklik elemanlarını pergel-cetvel veya dinamik yazılımla inşa edebilme",
                    "surec": [
                        "a) Kağıt katlama ve pergel-cetvel yardımıyla açıortay, kenarortay ve yüksekliği inşa eder.",
                        "b) Üçgenin yardımcı elemanlarının kesişim noktalarını (ağırlık merkezi vb.) keşfeder.",
                    ],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri ve 3B Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Üçgen şeklindeki bir tepsinin tam dengede duracağı ağırlık merkezini bulma.",
                    "kriz": "Mert 'Cetvelle üçgen çizmek ne işimize yarayacak?' diyerek etkinliğe katılmayı reddeder.",
                    "odak": "direncli",
                }
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.7.6.1",
                    "cikti": "Nicel sürekli verileri çizgi grafiği ve daire grafiği ile temsil ederek yayılım ölçülerini yorumlayabilme",
                    "surec": [
                        "a) Zamana bağlı değişen sürekli verileri çizgi grafiği ile görselleştirir.",
                        "b) Parça-bütün ilişkisini daire grafiğinde merkez açılarla modeller.",
                        "c) Veri grubunun açıklığını ve çeyrekler açıklığını hesaplayarak yayılımı yorumlar.",
                    ],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Oran Tahtası ve Renkli Boncuklar"],
                    "hook": "Bir haftalık hava sıcaklığı değişimi ve enerji tüketim oranlarının grafiksel analizi.",
                    "kriz": "Kerem daire grafiğinde yüzde 25'i 360 dereceyle oranlamak yerine doğrudan 25 derece olarak çizer.",
                    "odak": "disleksi",
                }
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.7.7.1",
                    "cikti": "Eş olasılıklı olayların teorik olasılığını, tümleyen ile ayrık ve ayrık olmayan olayları muhakeme edebilme",
                    "surec": [
                        "a) Bir olayın teorik olasılığını istenen durumların tüm durumlara oranı olarak hesaplar.",
                        "b) Bir olay ile tümleyeninin olasılıkları toplamının 1 olduğunu doğrular.",
                        "c) Ayrık ve ayrık olmayan olayları örnek uzay üzerinde ayırt eder.",
                    ],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Renkli Çark", "Kesir Çubukları, İki Renkli Sayma Pulları ve Yüzlük Kartlar"],
                    "hook": "Şifreli kasa kombinasyonları ve bilgi yarışması çarkıfelek olasılık hesapları.",
                    "kriz": "Can gerçek hayatta hiçbir olayın tam olarak eş olasılıklı olamayacağını savunarak soruya itiraz eder.",
                    "odak": "ustun",
                }
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
                    "cikti": "Üslü ve kareköklü ifadeleri gerçek sayılar kümesi bağlamında muhakeme edebilme",
                    "surec": [
                        "a) Tam sayıların tam sayı kuvvetlerini ve bilimsel gösterimi inceler.",
                        "b) Karenin alanı ile kenar uzunluğu arasındaki ilişkiden kareköklü ifadeleri yapılandırır.",
                        "c) Rasyonel ve irrasyonel sayıları ayırt ederek gerçek sayılar kümesini açıklar.",
                    ],
                    "uygun_materyaller": ["Onluk Taban Blokları ve Sayı Doğrusu", "Birim Küpler ve 3B Prizma Modelleri"],
                    "hook": "Mikroskobik hücre boyutlarının bilimsel gösterimi ve alanı 50 metrekare olan kare bahçenin kenar uzunluğu.",
                    "kriz": "Arda tam kare olmayan sayıların karekök değerlerinin sonsuza kadar düzensiz gitmesinden rahatsız olur.",
                    "odak": "otizm",
                }
            ],
            "2. Tema: Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": "Doğrusal fonksiyonları, dik koordinat sistemindeki grafiklerini ve eğim kavramını yapılandırabilme",
                    "surec": [
                        "a) İki değişken arasındaki doğrusal ilişkiyi tablo, denklem ve grafikle temsil eder.",
                        "b) Doğrunun eğimini dikey değişimin yatay değişime oranı olarak yorumlar.",
                        "c) Özdeşlikleri ve çarpanlara ayırma süreçlerini geometrik alan modelleriyle doğrular.",
                    ],
                    "uygun_materyaller": ["Cebir Karoları ve Eşit Kollu Terazi", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Engelli rampalarının standartlara uygun eğim hesabı ve taksi ücret tarifesi grafiği.",
                    "kriz": "Elif LGS sınav kaygısıyla 'Bu grafik ve eğim sorularını sınavda asla yapamayacağım' diyerek kalemi bırakır.",
                    "odak": "kaygili",
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": "Üçgenlerde açı-kenar ilişkilerini, Pisagor bağıntısını ve çokgenlerde eşlik-benzerliği uygulayabilme",
                    "surec": [
                        "a) Üçgen eşitsizliğini ve açı-kenar bağıntılarını dinamik geometri yazılımıyla keşfeder.",
                        "b) Dik üçgende Pisagor bağıntısını alan modelleriyle ispatlayarak uygular.",
                        "c) Eş ve benzer çokgenlerin kenar ve açı oranlarını gerçek yaşam modellerinde kullanır.",
                    ],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri ve 3B Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "İtfaiye merdiveninin binaya ulaşma yüksekliği (Pisagor) ve mimari maket ölçeklendirme (Benzerlik).",
                    "kriz": "Kerem Pisagor bağıntısını hipotenüs yerine dik kenara uygulayıp yanlış sonuç bulunca defterini karalar.",
                    "odak": "disleksi",
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1",
                    "cikti": "Dik prizma, dik dairesel silindir, dik piramit ve dik koninin yüzey alanı ve hacim bağıntılarını kurabilme",
                    "surec": [
                        "a) Üç boyutlu cisimlerin açınımlarını 3B dijital araçlarla inceler.",
                        "b) Silindir, piramit ve koninin yüzey alanı ile hacim bağıntılarını prizmalar üzerinden geneller.",
                        "c) Üç boyutlu cisimlerin hacim ve alanlarıyla ilgili gerçek yaşam problemlerini çözer.",
                    ],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Endüstriyel silindirik su depolarının ve konik tahıl silolarının kapasite hesabı.",
                    "kriz": "Emre üç boyutlu açınım kartonlarını katlayıp uçak yaparak sınıfta havaya atar.",
                    "odak": "hareketli",
                }
            ],
            "5. Tema: Dönüşüm": [
                {
                    "kod": "MAT.8.5.1",
                    "cikti": "Dik koordinat sisteminde şekillerin öteleme ve yansıma dönüşümleri altındaki görüntülerini belirleyebilme",
                    "surec": [
                        "a) Koordinat düzleminde öteleme hareketinin köşe koordinatlarına etkisini inceler.",
                        "b) Eksenlere göre yansıma dönüşümünde koordinat işaretlerinin değişimini geneller.",
                        "c) Ardışık öteleme ve yansıma dönüşümlerini dijital tahtada modeller.",
                    ],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Bilgisayar oyunlarında karakterlerin ekran üzerindeki koordinat hareket algoritmaları.",
                    "kriz": "Selin koordinat düzlemi çizilmeden sadece sözel işaret kuralı verildiğinde yansımayı zihninde canlandıramaz.",
                    "odak": "gorseluzamsal",
                }
            ],
            "6. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.8.6.1",
                    "cikti": "Bilimsel araştırma etiği, KVKK ve veri mahremiyeti ilkelerine uygun istatistiksel proje yürütebilme",
                    "surec": [
                        "a) Kişisel verilerin korunması (KVKK) ve etik ilkelere uygun veri toplama planı hazırlar.",
                        "b) Çoklu veri gruplarını uygun grafik türleriyle karşılaştırmalı analiz eder.",
                        "c) Veriye dayalı çıkarımlar yaparak yanlı/hatalı grafik gösterimlerini eleştirir.",
                    ],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Okul genelinde dijital ekran süresi araştırması yaparken kişisel veri mahremiyetini koruma.",
                    "kriz": "Can arkadaşlarının isimlerini grafikte açıkça paylaşmak ister, KVKK mahremiyet uyarısına itiraz eder.",
                    "odak": "ustun",
                }
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1",
                    "cikti": "Simülasyonlar aracılığıyla deneysel ve teorik olasılık ilişkisini kurarak veriye dayalı karar verebilme",
                    "surec": [
                        "a) Dijital olasılık simülasyonlarında büyük sayılar yasasını gözlemler.",
                        "b) Deneysel olasılık sonuçlarının teorik olasılığa yakınsamasını yorumlar.",
                        "c) Belirsizlik içeren gerçek yaşam durumlarında olasılık verilerine dayanarak optimal karar verir.",
                    ],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri ve 3B Yazılımı"],
                    "hook": "Kalite kontrol mühendisliğinde üretim hattındaki hatalı ürün olasılığını simülasyonla test etme.",
                    "kriz": "Mert 'Büyük sayılar yasası gerçek hayatta tek seferlik kararlarda işe yaramaz' diyerek derse direnç gösterir.",
                    "odak": "direncli",
                }
            ],
        },
    },
}
# ==========================================
# 3. YARDIMCI FONKSİYONLAR: MATERYAL REHBERİ VE EYLEMSEL ÖĞRENCİ TEPKİ MOTORU
# ==========================================
def materyal_rehberi_getir(materyal_adi):
    if materyal_adi in materyal_adim_rehberi:
        return materyal_adim_rehberi[materyal_adi]
    ilk_kelime = materyal_adi.split()[0]
    for anahtar, deger in materyal_adim_rehberi.items():
        if anahtar.startswith(ilk_kelime):
            return deger
    return (
        "1. Adım: Materyali öğrencilerin görebileceği ve dokunabileceği şekilde masaya yerleştirin.\n"
        "2. Adım: Kazanımın süreç bileşenine uygun olarak nicelikler arası ilişkiyi materyal üzerinde modelletin.\n"
        "3. Adım: Öğrencinin somut gözleminden matematiksel genellemeye ulaşmasını açık uçlu sorularla destekleyin."
    )


def uygun_materyal_mi_kontrol(secilen_materyal, uygun_materyaller_listesi):
    secilen_ilk = secilen_materyal.split()[0].lower()
    for u in uygun_materyaller_listesi:
        if u.lower().startswith(secilen_ilk) or secilen_materyal == u:
            return True
    return False


def ogrenci_eylemsel_durum_belirle(ogr, odak_ogrenci_id, secilen_materyal, analiz_sonucu):
    is_odak = ogr["id"] == odak_ogrenci_id
    cinsiyet_ikon = "👦" if ogr.get("cinsiyet") == "Erkek" else "👧"

    # Henüz öğretmen müdahalesi yapılmamışsa (Kriz Başlangıç Durumu)
    if analiz_sonucu is None:
        if is_odak:
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": ogr["kriz_yuz"],
                "postur": ogr["kriz_postur"],
                "mimik": ogr["kriz_mimik"],
                "tepki": f"Kriz Eylemi: {ogr['kriz_tepki']}",
                "konusma": ogr["kriz_konusma"],
                "renk": "#ef4444",
            }
        return {
            "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
            "yuz": "😐",
            "postur": "👀",
            "mimik": "Sırasında duraksadı, öğretmen adayının yaklaşımını gözlemliyor",
            "tepki": "Gözlem Eylemi: Kalemini bıraktı, krizin nasıl çözüleceğini izliyor",
            "konusma": "Öğretmenimiz arkadaşımıza nasıl yaklaşacak acaba?",
            "renk": "#94a3b8",
        }

    # Öğretmen müdahalesi sonrası pedagojik eylem ve sesli dönüte göre sağlıklı/eylemsel tepkiler
    seviye = analiz_sonucu["mudahale_seviyesi"]  # "tam", "kismi", "olumsuz"

    eylemsel_kismi_harita = {
        "disleksi": (
            "😕",
            "✋",
            "Sakinleşti ancak basamakları parmağıyla hizalarken hala tereddüt ediyor",
            f"Kısmi Eylem: {secilen_materyal} aracına uzandı fakat renk/basamak eşleştirmesi için öğretmenden adım adım yönlendirme bekliyor",
            "Kızmadığınız için rahatladım öğretmenim ama bu materyalde önce hangi basamağı eşleştireceğimi tam göremedim.",
        ),
        "otizm": (
            "😐",
            "👀",
            "Ellerini kulaklarından indirdi, materyale bakıyor",
            f"Kısmi Eylem: Sallanmayı azalttı ancak {secilen_materyal} parçalarına dokunmak için net sıra yönergesi bekliyor",
            "Sesiniz sakinleştirdi ama materyali hangi sırayla dizeceğimi adım adım söyler misiniz?",
        ),
        "ustun": (
            "🤨",
            "💭",
            "Kalemini tıklatmayı bıraktı, modeli inceliyor",
            f"Kısmi Eylem: {secilen_materyal} üzerinde temel adımı yaptı, daha zorlayıcı bir genelleme sorusu bekliyor",
            "Bu adımı hemen yaptım öğretmenim, peki sayılar çok büyüdüğünde veya negatif olduğunda da bu model çalışır mı?",
        ),
        "kaygili": (
            "😟",
            "✏️",
            "Başını hafifçe kaldırdı, çekinerek materyale dokunuyor",
            f"Kısmi Eylem: Silgisini bıraktı, {secilen_materyal} üzerinde ilk denemesini yaparken onay almak için öğretmene bakıyor",
            "Denemeye çalışıyorum öğretmenim, ilk adımı böyle kursam yanlış olmaz değil mi?",
        ),
        "mukemmeliyetci": (
            "😐",
            "📏",
            "Kağıdı yırtmaktan vazgeçti ama cetvelle tekrar ölçüyor",
            f"Kısmi Eylem: {secilen_materyal} ile modeli kurdu fakat sonucun kusursuz görünmemesine hala takılıyor",
            "Silmedim öğretmenim ama çizimim ve modelim tam simetrik durmuyor, yine de kabul eder misiniz?",
        ),
        "direncli": (
            "🫤",
            "🪑",
            "Kollarını çözdü, sırasına düzgün oturdu",
            f"Kısmi Eylem: İtiraz etmeyi bıraktı ve {secilen_materyal} aracını önüne çekti ama henüz tam motive olmadı",
            "Tamam öğretmenim materyale bakıyorum ama bunun gerçek hayatta tam olarak ne işimize yarayacağını biraz daha açıklar mısınız?",
        ),
        "icedonuk": (
            "😶",
            "📓",
            "Omuzları biraz gevşedi, defterine küçük bir şema çiziyor",
            f"Kısmi Eylem: Bireysel olarak {secilen_materyal} parçalarını dizdi ancak henüz sıra arkadaşıyla paylaşmadı",
            "Modeli kendi önümde kurdum öğretmenim, yüksek sesle söylemeden size göstersem olur mu?",
        ),
        "hareketli": (
            "😮",
            "🪑",
            "Yerine oturdu fakat parmaklarıyla masada ritim tutuyor",
            f"Kısmi Eylem: Ayağa kalkmayı bıraktı, enerjisini yönlendirmek için {secilen_materyal} üzerinde aktif görev bekliyor",
            "Yerime oturdum öğretmenim! Şimdi materyalin parçalarını ben yerleştirsem olur mu?",
        ),
        "sozelgucluk": (
            "😬",
            "👆",
            "Heyecanı azaldı, materyalin bir kısmını parmağıyla işaret ediyor",
            f"Kısmi Eylem: {secilen_materyal} üzerinde doğru parçayı tuttu ancak matematiksel terimi söylemek için ipucu bekliyor",
            "İşte buradaki parçalar birbirine denk geliyor öğretmenim ama bunun matematikteki adını dilimin ucuna getiremiyorum.",
        ),
        "gorseluzamsal": (
            "🧐",
            "📐",
            "Tahtaya dikkatle bakıyor, defterine şekil çizmeye çalışıyor",
            f"Kısmi Eylem: Sözel açıklamayı şekle dökmeye çalıştı, {secilen_materyal} üzerinde görsel gösterim bekliyor",
            "Anlattığınızı gözümde canlandırmaya çalışıyorum öğretmenim, materyal üzerinde şekille gösterir misiniz?",
        ),
    }

    if is_odak:
        if seviye == "tam":
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": ogr["dogru_yuz"],
                "postur": ogr["dogru_postur"],
                "mimik": ogr["dogru_mimik"],
                "tepki": f"Sağlıklı Eylemsel Tepki: {ogr['dogru_tepki']} ({secilen_materyal} aracını aktif kullanarak problemi çözdü)",
                "konusma": ogr["dogru_konusma"],
                "renk": "#22c55e",
            }
        elif seviye == "kismi":
            k_yuz, k_postur, k_mimik, k_tepki, k_konusma = eylemsel_kismi_harita.get(
                ogr["id"],
                ("😕", "✋", "Kısmen rahatladı", "Materyal yönergesi bekliyor", "Biraz anladım ama materyalde nasıl göstereceğiz?"),
            )
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": k_yuz,
                "postur": k_postur,
                "mimik": k_mimik,
                "tepki": k_tepki,
                "konusma": k_konusma,
                "renk": "#f59e0b",
            }
        else:
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": ogr["kriz_yuz"],
                "postur": ogr["kriz_postur"],
                "mimik": ogr["kriz_mimik"],
                "tepki": "Olumsuz Eylemsel Tepki: Uygunsuz/otoriter müdahale nedeniyle materyali bıraktı ve dersten tamamen koptu",
                "konusma": ogr["kriz_konusma"],
                "renk": "#dc2626",
            }
    else:
        if seviye == "tam":
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": ogr["dogru_yuz"],
                "postur": ogr["dogru_postur"],
                "mimik": ogr["dogru_mimik"],
                "tepki": f"Sağlıklı Akran Eylemi: {secilen_materyal} ile kendi profiline uygun şekilde grup etkinliğine katıldı",
                "konusma": ogr["dogru_konusma"],
                "renk": "#38bdf8",
            }
        elif seviye == "kismi":
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": "🙂",
                "postur": "🧩",
                "mimik": "Materyali incelemeye başladı, öğretmenin ikinci adımını takip ediyor",
                "tepki": f"Kısmi Eylem: {secilen_materyal} parçalarını hazırladı, tartışma sorusunu bekliyor",
                "konusma": "Materyallerimizi hazırladık öğretmenim, şimdi hangi adımı uygulayalım?",
                "renk": "#fbbf24",
            }
        else:
            return {
                "cinsiyet_etiket": f"{cinsiyet_ikon} {ogr.get('cinsiyet', '')} Öğrenci",
                "yuz": "😟",
                "postur": "🙇",
                "mimik": "Sınıf iklimi gerildiği için omuzlarını büzdü, sessizleşti",
                "tepki": "Savunmacı Eylem: Hata yapıp azarlanmamak için parmak kaldırmaktan vazgeçti",
                "konusma": "Sınıf çok gerildi, yanlış bir şey söylersem ben de uyarı alırım...",
                "renk": "#f87171",
            }


def render_3d_classroom_10_students(
    ogretmen_adi,
    ogretmen_cinsiyeti,
    sinif_duzeyi,
    tema,
    kazanim_kodu,
    secilen_materyal,
    odak_ogrenci_id,
    ogretmen_sozu,
    analiz_sonucu,
):
    ogretmen_ikon = "👩‍🏫" if ogretmen_cinsiyeti == "Kadın" else "👨‍🏫"
    ogretmen_balon = (
        ogretmen_sozu
        if ogretmen_sozu
        else f"Arkadaşlar, bugünkü matematik dersimizde {secilen_materyal} kullanarak birlikte keşif yapacağız."
    )

    kartlar_html = ""
    for ogr in genel_ogrenci_tipleri_detayli:
        is_odak = ogr["id"] == odak_ogrenci_id
        durum = ogrenci_eylemsel_durum_belirle(ogr, odak_ogrenci_id, secilen_materyal, analiz_sonucu)
        vurgu_stil = (
            "box-shadow: 0 0 22px rgba(250, 204, 21, 0.95); transform: translateY(-5px) scale(1.03); border-width: 3px;"
            if is_odak
            else ""
        )

        kartlar_html += f"""
        <div class="desk-unit" style="border-color: {durum['renk']}; {vurgu_stil}">
            <div class="speech-bubble" style="border-left: 4px solid {durum['renk']};">
                💬 "{durum['konusma']}"
            </div>
            <div class="avatar-circle" style="background: {ogr['bg']}; border-color: {durum['renk']};">
                <span class="avatar-face">{durum['yuz']}</span>
                <span class="posture-badge">{durum['postur']}</span>
            </div>
            <div class="desk-surface">
                <div class="student-name">{ogr['ad']} {'⭐' if is_odak else ''}</div>
                <div class="student-gender">{durum['cinsiyet_etiket']} | {ogr['tip']}</div>
                <div class="gesture-tag" style="color: {durum['renk']};">🎭 {durum['mimik']}</div>
                <div class="reaction-tag">⚡ {durum['tepki']}</div>
            </div>
        </div>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
        body {{ margin: 0; padding: 4px; background: transparent; }}
        .scene-wrapper {{
            background: radial-gradient(circle at 50% 10%, #0f172a 0%, #020617 100%);
            border-radius: 16px; padding: 16px; color: #f8fafc; border: 2px solid #334155;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.7), 0 10px 20px rgba(0,0,0,0.3);
        }}
        .classroom-header {{
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(15, 23, 42, 0.85); padding: 8px 14px; border-radius: 8px; border: 1px solid #475569; margin-bottom: 12px; font-size: 12.5px;
        }}
        .smartboard {{
            background: linear-gradient(135deg, #064e3b 0%, #022c22 100%); border: 5px solid #b45309; border-radius: 10px;
            padding: 10px 16px; text-align: center; max-width: 88%; margin: 0 auto 14px auto; box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        }}
        .smartboard-title {{ color: #fde047; font-weight: 700; font-size: 14px; }}
        .smartboard-sub {{ color: #d1fae5; font-size: 12px; margin-top: 3px; }}
        .teacher-zone {{
            display: flex; align-items: center; justify-content: center; gap: 14px; margin: 10px auto 16px auto;
            padding: 10px 14px; max-width: 86%; background: linear-gradient(90deg, rgba(30, 58, 138, 0.7), rgba(30, 64, 175, 0.5));
            border: 2px solid #60a5fa; border-radius: 12px;
        }}
        .teacher-avatar {{
            width: 56px; height: 56px; border-radius: 50%; background: #1d4ed8; border: 2px solid #93c5fd;
            display: flex; align-items: center; justify-content: center; font-size: 30px; flex-shrink: 0;
        }}
        .teacher-speech {{
            background: #eff6ff; color: #1e3a8a; padding: 8px 12px; border-radius: 10px; font-size: 13px; font-weight: 600; line-height: 1.35; flex-grow: 1; border-left: 4px solid #2563eb;
        }}
        .isometric-floor-10 {{
            display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; padding: 4px;
        }}
        @media (max-width: 1100px) {{ .isometric-floor-10 {{ grid-template-columns: repeat(3, 1fr); }} }}
        @media (max-width: 700px) {{ .isometric-floor-10 {{ grid-template-columns: repeat(2, 1fr); }} }}
        .desk-unit {{
            background: rgba(30, 41, 59, 0.95); border: 2px solid #64748b; border-radius: 10px;
            padding: 8px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        }}
        .speech-bubble {{
            background: #f8fafc; color: #0f172a; font-size: 11px; font-weight: 600;
            padding: 6px 8px; border-radius: 8px; margin-bottom: 8px; width: 100%;
            min-height: 52px; display: flex; align-items: center; line-height: 1.3;
        }}
        .avatar-circle {{
            width: 50px; height: 50px; border-radius: 50%; border: 2px solid;
            display: flex; align-items: center; justify-content: center; position: relative; margin-bottom: 6px;
        }}
        .avatar-face {{ font-size: 25px; }}
        .posture-badge {{
            position: absolute; bottom: -2px; right: -4px; background: #0f172a;
            border-radius: 50%; padding: 1px 3px; font-size: 12px; border: 1px solid #94a3b8;
        }}
        .desk-surface {{
            width: 100%; background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
            border-top: 3px solid #ca8a04; border-radius: 6px; padding: 6px; text-align: center;
        }}
        .student-name {{ font-weight: 700; font-size: 12.5px; color: #f1f5f9; }}
        .student-gender {{ font-size: 10px; color: #cbd5e1; margin-bottom: 3px; font-weight: 600; }}
        .gesture-tag {{ font-size: 10px; font-weight: 600; margin-bottom: 3px; }}
        .reaction-tag {{ font-size: 9.5px; color: #e2e8f0; background: rgba(15, 23, 42, 0.75); padding: 4px; border-radius: 4px; line-height: 1.25; }}
    </style>
    </head>
    <body>
    <div class="scene-wrapper">
        <div class="classroom-header">
            <span>🏫 <strong>Ortaokul Matematik Öğretmenliği 3B Sınıf Ortamı</strong> (Yalnızca Öğretmen Adayı ve 10 Öğrenci Bulunur)</span>
            <span>🟢 Cinsiyet ve Profil Duyarlı Eylemsel Tepki Modu</span>
        </div>
        <div class="smartboard">
            <div class="smartboard-title">📐 {sinif_duzeyi} | {tema} ({kazanim_kodu})</div>
            <div class="smartboard-sub">🛠️ Öğretmen Adayının Seçtiği Materyal: {secilen_materyal}</div>
        </div>
        <div class="teacher-zone">
            <div class="teacher-avatar">{ogretmen_ikon}</div>
            <div>
                <div style="font-size: 11px; color: #93c5fd; font-weight: 700; margin-bottom: 2px;">
                    ORTAOKUL MATEMATİK ÖĞRETMEN ADAYI ({ogretmen_adi} - {ogretmen_cinsiyeti}) HİTABETİ:
                </div>
                <div class="teacher-speech">🎙️ "{ogretmen_balon}"</div>
            </div>
        </div>
        <div class="isometric-floor-10">
            {kartlar_html}
        </div>
    </div>
    </body>
    </html>
    """
    components.html(html_code, height=650, scrolling=True)


# ==========================================
# 4. DETAYLI PEDAGOJİK ANALİZ, MATERYAL YÖNERGESİ VE PROFİL HİTABET MOTORU
# ==========================================
def detayli_pedagojik_analiz_uret(
    sesli_metin,
    ilk_eylem,
    ikinci_eylem,
    secilen_materyal,
    materyal_kullanim_aciklamasi,
    kazanim_obj,
    surec,
    rubrik_metni,
):
    birlesik_metin = f"{sesli_metin} {materyal_kullanim_aciklamasi}".lower()
    odak_id = kazanim_obj.get("odak", "disleksi")
    odak_ogr = next((o for o in genel_ogrenci_tipleri_detayli if o["id"] == odak_id), genel_ogrenci_tipleri_detayli[0])

    # 1. Kronolojik Eylem Sıralaması Puanı (25 Puan)
    ilk_dogru = ilk_eylem.startswith("B)") or ilk_eylem.startswith("E)")
    ikinci_dogru = ikinci_eylem.startswith("C)") or ikinci_eylem.startswith("D)")
    ters_sira = (ilk_eylem.startswith("C)") or ilk_eylem.startswith("D)")) and (
        ikinci_eylem.startswith("B)") or ikinci_eylem.startswith("E)")
    )

    if ilk_dogru and ikinci_dogru:
        siralama_puani = 25
        siralama_durumu = "Tam Doğru Sıralama (Önce Duyuşsal Güven/Regülasyon, Sonra Somut Materyalle Yapılandırma)"
    elif ters_sira:
        siralama_puani = 16
        siralama_durumu = "Ters Kronolojik Sıralama (Öğrenci Sakinleşmeden Doğrudan Bilişsel Göreve Geçildi)"
    elif ilk_dogru or ikinci_dogru:
        siralama_puani = 14
        siralama_durumu = "Kısmi Doğru Eylem (Adımlardan Biri Yapılandırmacı, Diğeri Geleneksel/Eksik)"
    else:
        siralama_puani = 5
        siralama_durumu = "Hatalı Eylem Tercihi (Otoriter/Geleneksel Müdahale)"

    # 2. Materyal Uygunluğu ve Derste Kullanım Değerlendirmesi (25 Puan)
    uygun_materyaller = kazanim_obj.get("uygun_materyaller", [])
    materyal_konuya_uygun = uygun_materyal_mi_kontrol(secilen_materyal, uygun_materyaller)
    materyal_kelimeler = [
        k.lower() for k in secilen_materyal.replace(",", "").split() if len(k) > 3
    ] + ["materyal", "model", "somut", "görsel", "tahta", "küp", "karo", "abaküs", "kesir", "geogebra", "çark", "tablo", "ayna"]
    materyal_aktif_kullanildi = any(k in birlesik_metin for k in materyal_kelimeler) and len(materyal_kullanim_aciklamasi.strip()) >= 15

    if materyal_konuya_uygun and materyal_aktif_kullanildi:
        materyal_puani = 25
    elif materyal_konuya_uygun or materyal_aktif_kullanildi:
        materyal_puani = 15
    else:
        materyal_puani = 6

    # 3. Sesli Geri Bildirim, Profil Odaklı Hitabet ve Süreç Bileşeni Analizi (50 Puan)
    empati_kelimeleri = ["sakin", "birlikte", "anlıyorum", "endişelenme", "nefes", "yanındayım", "dinliyorum", "haklısın", "normal", "güven", "çekinme", "adım adım"]
    sorgulama_kelimeleri = ["nasıl", "neden", "ne fark ettin", "inceleyelim", "düşün", "örüntü", "ilişki", "keşf", "sence", "tahmin", "karşılaştır", "göster"]
    olumsuz_kelimeler = ["ezberle", "sustur", "sus", "kuralı yaz", "formülü yaz", "ceza", "görmezden", "bağır", "otur yerine", "yanlış yaptın"]

    empati_var = any(k in birlesik_metin for k in empati_kelimeleri)
    sorgulama_var = any(k in birlesik_metin for k in sorgulama_kelimeleri)
    olumsuz_var = any(k in birlesik_metin for k in olumsuz_kelimeler)

    hitabet_puani = 15
    if empati_var:
        hitabet_puani += 12
    if sorgulama_var:
        hitabet_puani += 13
    if len(sesli_metin.strip()) >= 30:
        hitabet_puani += 10
    if olumsuz_var:
        hitabet_puani -= 25
    hitabet_puani = max(5, min(50, hitabet_puani))

    toplam_puan = min(100, siralama_puani + materyal_puani + hitabet_puani)

    if toplam_puan >= 80 and not olumsuz_var:
        mudahale_seviyesi = "tam"
    elif toplam_puan >= 50 and not olumsuz_var:
        mudahale_seviyesi = "kismi"
    else:
        mudahale_seviyesi = "olumsuz"

    # Doğru materyal ve adım adım yapılandırılmış yönerge metni
    dogru_materyal_adi = uygun_materyaller[0] if uygun_materyaller else secilen_materyal
    dogru_materyal_adimlari = materyal_rehberi_getir(dogru_materyal_adi)
    secilen_materyal_adimlari = materyal_rehberi_getir(secilen_materyal)

    # Profil odaklı detaylı hitabet ve davranış rehberi
    profil_ozel_davranis_rehberi = (
        f"📌 **Odak Öğrenci Profili:** {odak_ogr['ad']} ({odak_ogr['cinsiyet']} - {odak_ogr['tip']})\n"
        f"- **Psikolojik ve Bilişsel Özellik:** {odak_ogr['karakteristik']}\n"
        f"- **Yaşanan Kriz Durumu:** {kazanim_obj['kriz']}\n"
        f"- **Öğretmen Adayı Öğrenciye Nasıl Davranmalı?:** {odak_ogr['hitabet_rehberi']}\n"
        f"- **Örnek Doğru Sözlü Geri Bildirim Cümlesi:** *\"{odak_ogr['ad']}, yaşadığın zorluğu çok iyi anlıyorum, hiç endişelenme. "
        f"Kuralı ezberlemek zorunda değiliz; gel seninle {dogru_materyal_adi} üzerinde ilk adımı birlikte kuralım. "
        f"Buradaki parçaları eşleştirdiğimizde nasıl bir değişim fark ediyorsun?\"*"
    )

    # Nesnel İyi Yönler
    iyi_yonler = []
    if ilk_dogru and ikinci_dogru:
        iyi_yonler.append(f"**Kronolojik Pedagojik Eylem Sıralaması ({siralama_puani}/25):** Önce {odak_ogr['ad']} adlı öğrencinin duyuşsal/duyusal güvenliğini sağlayıp (1. Eylem), ardından somut materyal ve akran süreciyle matematiksel keşfe geçerek (2. Eylem) en sağlıklı sıralamayı uyguladınız.")
    if materyal_konuya_uygun:
        iyi_yonler.append(f"**Kazanım-Materyal Uyumu:** Seçtiğiniz **{secilen_materyal}**, `{kazanim_obj['kod']}` öğrenme çıktısının somutlaştırılması için ortaokul matematik öğretimine tam uygundur.")
    if materyal_aktif_kullanildi:
        iyi_yonler.append("**Materyalin Derste İşlevsel Kullanımı:** Materyalin derste öğrenci tarafından nasıl manipüle edileceğini açıklayarak öğrencinin eylemsel katılımını sağladınız.")
    if empati_var:
        iyi_yonler.append(f"**Profil Duyarlı Empatik Hitabet:** {odak_ogr['tip']} profilindeki {odak_ogr['ad']}'in duyuşsal ihtiyacını gözeten destekleyici bir geri bildirim sundunuz.")
    if sorgulama_var:
        iyi_yonler.append(f"**Süreç Bileşeni Odaklı Sorgulama:** `{surec}` basamağını işletmek için doğrudan formül vermek yerine keşif soruları yönelttiniz.")
    if not iyi_yonler:
        iyi_yonler.append("**Temel Kriz Farkındalığı:** Sınıf içi krizi fark ederek müdahale sürecini başlattınız.")

    # Nesnel Eksik Yönler, Kök Nedenler ve Detaylı Çözüm Önerileri
    eksik_yonler, kok_nedenler, cozum_onerileri = [], [], []

    if not (ilk_dogru and ikinci_dogru):
        eksik_yonler.append(f"**Kronolojik Eylem Sıralaması Eksikliği ({siralama_durumu}):** {odak_ogr['ad']} ({odak_ogr['tip']}) kriz yaşarken önce duyuşsal regülasyon yapılması, sonra materyalle bilişsel göreve geçilmesi gerekirken bu sıra bozuldu.")
        kok_nedenler.append("**Bilişsel Acelecilik veya Otoriter Sınıf Yönetimi Refleksi:** Öğrencinin yaşadığı duyusal/duygusal kilitlenmeyi çözmeden doğrudan matematiksel kuralı anlatmaya çalışma ya da sert disiplinle susturma eğilimi.")
        cozum_onerileri.append(
            f"**Doğru Kronolojik Eylem Planı:**\n"
            f"1. **Önce Yapılacak Eylem:** Ses tonunu yumuşatarak {odak_ogr['ad']}'in yanına gidin, duygusunu kabul edin ve kısa bir bekleme süresi tanıyarak güvenli alan oluşturun.\n"
            f"2. **Sonra Yapılacak Eylem:** Öğrenci sakinleşip göz teması kurduğunda **{dogru_materyal_adi}** aracını önüne koyarak adım adım keşif soruları yöneltin."
        )

    if not materyal_konuya_uygun:
        eksik_yonler.append(f"**Materyal-Konu Uyumsuzluğu:** Seçtiğiniz **{secilen_materyal}**, `{kazanim_obj['kod']}` kazanımının matematiksel yapısını doğrudan modellememektedir. Uygun materyaller: **{', '.join(uygun_materyaller)}**.")
        kok_nedenler.append("**Kazanımın Temsil Doğasını Analiz Etmeden Materyal Seçimi:** Ortaokul matematik konularındaki kavramların (kesir, oran, cebir, uzamsal yapı, olasılık) hangi somut modelle eşleştiğine dikkat edilmemesi.")
        cozum_onerileri.append(
            f"**Yapılandırılmış Materyal Yönergesi (Doğru Materyal: {dogru_materyal_adi}):**\n{dogru_materyal_adimlari}"
        )

    if not materyal_aktif_kullanildi:
        eksik_yonler.append(f"**Materyalin Derste Nasıl Kullanıldığının Açıklanmaması:** **{secilen_materyal}** seçilmiş olmasına rağmen öğrencinin bu araçla hangi somut adımları uygulayacağı yönergede eksik kaldı.")
        kok_nedenler.append("**Materyali Öğretmen Merkezli Gösteri Aracı Sanma:** Materyali öğrencinin bizzat dokunarak deneyimleyeceği bir öğrenme aracı yerine sadece adı geçen bir nesne olarak bırakma.")
        cozum_onerileri.append(
            f"**Yapılandırılmış Materyal Kullanım Adımları ({secilen_materyal}):**\n{secilen_materyal_adimlari}"
        )

    if not empati_var or olumsuz_var:
        eksik_yonler.append(f"**Profil Odaklı Hitabet ve Davranış Eksikliği:** {odak_ogr['ad']} ({odak_ogr['tip']}) için gereken bireyselleştirilmiş empatik geri bildirim ve davranış dili yeterince kurulmadı.")
        kok_nedenler.append("**Bireysel Farklılıkları Göz Ardı Eden Standart Hitabet:** Sınıftaki 10 farklı öğrenci profilinin kendine özgü bilişsel ve duyuşsal gereksinimlerine uygun iletişim kurmama.")
        cozum_onerileri.append(
            f"**Profil Odaklı Hitabet ve Davranış Rehberi:**\n{profil_ozel_davranis_rehberi}"
        )

    if not sorgulama_var:
        eksik_yonler.append(f"**Süreç Bileşenini İşleten Rehber Soruların Eksikliği:** `{surec}` basamağını öğrencinin kendi muhakemesiyle tamamlamasını sağlayacak yönlendirici sorular sorulmadı.")
        kok_nedenler.append("**Doğrudan Kural/Formül Verme Alışkanlığı:** Öğrenci zorlandığında cevabı hazır vererek matematiksel düşünme sürecini devre dışı bırakma.")
        cozum_onerileri.append(
            f"**Yapılandırılmış Sorgulama (Scaffolding):** Öğrenciye doğrudan kuralı söylemek yerine *{dogru_materyal_adi}* üzerinde; *'İlk adımda ne yaptık?', 'Miktarı değiştirdiğimizde modelde ne değişti?', 'Buradan hangi genel kurala ulaşabiliriz?'* sorularını sırasıyla yöneltin."
        )

    if not eksik_yonler:
        eksik_yonler.append("**Sınıf Geneli Eşzamanlı Zenginleştirme:** Odak öğrencideki kriz eksiksiz yönetildi; sınıftaki diğer 9 öğrenci profilini aynı anda üst düzey matematiksel tartışmaya katacak paralel görevler genişletilebilir.")
        kok_nedenler.append("**Tekil Müdahale Süresinde Sınıf Akışı:** Odak öğrenciyle birebir ilgilenirken üstün yetenekli veya aşırı hareketli öğrencilerin bekleme süresinde kalabilmesi.")
        cozum_onerileri.append("**Katmanlı Sınıf Görevi:** Odak öğrenciyle somut materyal adımını başlatırken diğer gruplara modelin farklı sayı değerleri için geçerliliğini test etme görevi verin.")

    # Rubrik Uygunluk Testi
    rubrik_satirlari = [s.strip() for s in rubrik_metni.split("\n") if s.strip()]
    alt_oranlar = [siralama_puani / 25.0, hitabet_puani / 50.0, materyal_puani / 25.0, toplam_puan / 100.0]
    rubrik_analiz_listesi = []
    for idx, satir in enumerate(rubrik_satirlari, 1):
        oran = alt_oranlar[(idx - 1) % len(alt_oranlar)]
        durum = "Rubriğe Tam Uygun" if oran >= 0.8 else ("Kısmen Uygun (Geliştirilmeli)" if oran >= 0.55 else "Rubrik Kriterini Karşılamıyor")
        rubrik_analiz_listesi.append({
            "Kriter No": f"Madde {idx}",
            "Uygulama Öğretim Elemanı Rubrik Kriteri": satir,
            "Davranış Test Sonucu": durum,
            "Uyum Yüzdesi": f"%{int(oran * 100)}",
        })

    # Öğretim Programı (TYMM 2026) Uygunluk Analizi
    program_uyum_analizi = {
        "kazanim_uyumu": "Tam Uyumlu" if (sorgulama_var and materyal_konuya_uygun) else "Kısmen Uyumlu / Geliştirilmeli",
        "surec_bileseni_degerlendirmesi": (
            f"Seçilen '{surec}' süreç bileşeni, öğrencinin aktif matematiksel muhakeme yapmasını gerektirmektedir. "
            + ("Adayın yönelttiği sorgulayıcı ifadeler bu süreç bileşenini başarıyla işletmiştir." if sorgulama_var else "Aday süreç bileşenini öğrenciye keşfettirmek yerine doğrudan açıklama eğilimi göstermiştir.")
        ),
        "materyal_ve_coklu_temsil": (
            f"Seçilen '{secilen_materyal}' aracı, `{kazanim_obj['kod']}` kazanımının doğasına {'uygundur' if materyal_konuya_uygun else 'uygun değildir (Doğru Materyal: ' + ', '.join(uygun_materyaller) + ')'}. "
            + ("Materyalin ders içi kullanımı somut-yarı somut-soyut geçişini desteklemiştir." if materyal_aktif_kullanildi else "Materyalin derste öğrenci tarafından adım adım nasıl kullanılacağı açıkça yapılandırılmamıştır.")
        ),
        "kapsayicilik_ve_farklilastirma": (
            f"TYMM 2026'nın bireysel farklılıkları ({odak_ogr['tip']} vb.) gözeten kapsayıcı eğitim ilkeleri "
            + ("doğru kronolojik müdahale ve empatik dille karşılanmıştır." if (ilk_dogru and empati_var) else "duyuşsal hazırlık ve profil odaklı hitabet eksikliği nedeniyle tam karşılanamamıştır.")
        ),
        "dogru_materyal_yonergesi": f"**{dogru_materyal_adi} İçin Adım Adım Kullanım Yönergesi:**\n{dogru_materyal_adimlari}",
        "profil_hitabet_rehberi": profil_ozel_davranis_rehberi,
    }

    return {
        "toplam_puan": toplam_puan,
        "siralama_puani": siralama_puani,
        "materyal_puani": materyal_puani,
        "hitabet_puani": hitabet_puani,
        "siralama_durumu": siralama_durumu,
        "materyal_konuya_uygun": materyal_konuya_uygun,
        "materyal_aktif_kullanildi": materyal_aktif_kullanildi,
        "mudahale_seviyesi": mudahale_seviyesi,
        "iyi_yonler": iyi_yonler,
        "eksik_yonler": eksik_yonler,
        "kok_nedenler": kok_nedenler,
        "cozum_onerileri": cozum_onerileri,
        "rubrik_analiz_listesi": rubrik_analiz_listesi,
        "program_uyum_analizi": program_uyum_analizi,
    }


# ==========================================
# ADIM 1: ORTAOKUL MATEMATİK ÖĞRETMENLİĞİ KURULUM VE RUBRİK PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.subheader("📐 İlköğretim / Ortaokul Matematik Öğretmenliği Bölümü 3B Staj Simülatörü Kurulum Paneli")
    st.info("Bu simülasyon özel olarak **Eğitim Fakültesi - İlköğretim / Ortaokul Matematik Öğretmenliği Bölümü** öğretmen adaylarının 2026 Türkiye Yüzyılı Maarif Modeli (5, 6, 7 ve 8. Sınıf) kapsamındaki sınıf yönetimi ve pedagojik alan becerilerini geliştirmek için tasarlanmıştır.")

    col1, col2 = st.columns(2)
    with col1:
        ogretmen_adi = st.text_input("Öğretmen Adayı Adı Soyadı", value=st.session_state.get("ogretmen_adi", ""))
        ogretmen_cinsiyeti = st.radio(
            "Öğretmen Adayı Cinsiyeti",
            ["Kadın", "Erkek"],
            horizontal=True,
            index=0 if st.session_state.get("ogretmen_cinsiyeti", "Kadın") == "Kadın" else 1,
        )
        okul_numarasi = st.text_input("Okul Numarası", value=st.session_state.get("okul_numarasi", ""))
        universite_adi = st.text_input("Üniversite Adı", value=st.session_state.get("universite_adi", ""))
        fakulte_bolum = "Eğitim Fakültesi - İlköğretim / Ortaokul Matematik Öğretmenliği"
        st.markdown(f"**Bölüm:** `{fakulte_bolum}` *(Bu simülasyon yalnızca Ortaokul Matematik Öğretmenliği Bölümü içindir)*")
        uygulama_ogretim_elemani = st.text_input("Uygulama Öğretim Elemanı", value=st.session_state.get("uygulama_ogretim_elemani", ""))

    with col2:
        st.markdown("### 📋 Uygulama Öğretim Elemanı Değerlendirme Rubriği")
        rubrik_dosya = st.file_uploader("Rubrik Dosyasını Yükle (TXT, CSV, PDF, DOCX)", type=["txt", "csv", "pdf", "docx"])
        varsayilan_rubrik = (
            "1. Kriz anında kronolojik olarak önce duyuşsal güven ve empati oluşturma (25 Puan)\n"
            "2. 10 farklı öğrenci profiline duyarlı kapsayıcı sözlü geri bildirim ve sorgulama (50 Puan)\n"
            "3. TYMM 2026 ortaokul matematik kazanımına uygun materyal seçimi ve derste adım adım kullanım (25 Puan)"
        )
        if rubrik_dosya is not None and rubrik_dosya.name.endswith(".txt"):
            try:
                varsayilan_rubrik = rubrik_dosya.read().decode("utf-8")
            except Exception:
                pass
        rubrik_metni = st.text_area("Değerlendirme Rubriği Maddeleri", value=st.session_state.get("rubrik_metni", varsayilan_rubrik), height=120)

        st.markdown("### 📂 Yıl Sonu İlerleme Takibi İçin Önceki Portfolyo Dosyasını Yükle (İsteğe Bağlı)")
        eski_portfolyo = st.file_uploader("Önceki JSON Portfolyo Dosyanızı Yükleyin", type=["json"])
        if eski_portfolyo is not None:
            try:
                yuklenen_veri = json.loads(eski_portfolyo.read().decode("utf-8"))
                if "oturumlar" in yuklenen_veri and len(st.session_state.simulasyon_gecmisi) == 0:
                    st.session_state.simulasyon_gecmisi = yuklenen_veri["oturumlar"]
                    st.success(f"✅ {len(yuklenen_veri['oturumlar'])} geçmiş oturum yıl sonu gelişim dosyanıza eklendi!")
            except Exception:
                st.error("Dosya okunamadı.")

    if st.button("🚀 Ortaokul Matematik Öğretmenliği 3B Sınıf Simülasyonunu Başlat", use_container_width=True):
        if not ogretmen_adi.strip() or not okul_numarasi.strip() or not universite_adi.strip() or not uygulama_ogretim_elemani.strip():
            st.warning("Lütfen tüm kurulum alanlarını doldurunuz.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi.strip()
            st.session_state.ogretmen_cinsiyeti = ogretmen_cinsiyeti
            st.session_state.okul_numarasi = okul_numarasi.strip()
            st.session_state.universite_adi = universite_adi.strip()
            st.session_state.fakulte_bolum = fakulte_bolum
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani.strip()
            st.session_state.rubrik_metni = rubrik_metni.strip()
            st.session_state.adim = 2
            st.rerun()

# ==========================================
# ADIM 2: 3B SINIF ORTAMI (10 ÖĞRENCİ), MATERYAL SEÇİMİ VE KRONOLOJİK MÜDAHALE
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    ogretmen_cinsiyeti = st.session_state.get("ogretmen_cinsiyeti", "Kadın")
    okul_no = st.session_state.get("okul_numarasi", "")

    st.markdown(f"### 🏫 Ortaokul Matematik 3B Sınıf Simülasyonu | Aday: {ogretmen} ({ogretmen_cinsiyeti} - {okul_no})")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        secilen_sinif = st.selectbox("1️⃣ Sınıf Düzeyi (TYMM)", list(tyym_master_arsiv.keys()))
    with col_s2:
        secilen_tema = st.selectbox("2️⃣ Tema (TYMM)", tyym_master_arsiv[secilen_sinif]["Temalar"])

    kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]
    with col_s3:
        kazanim_secenekleri = [f"{k['kod']} - {k['cikti']}" for k in kazanim_listesi]
        secilen_kazanim_str = st.selectbox("3️⃣ Öğrenme Çıktısı / Kazanım", kazanim_secenekleri)

    secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']} - {k['cikti']}" == secilen_kazanim_str)

    with col_s4:
        secilen_materyal = st.selectbox("4️⃣ Derste Kullanacağınız Materyali Seçin", materyal_havuzu)

    secilen_surec = st.selectbox("5️⃣ İşlenecek Süreç Bileşeni (TYMM 2026):", secilen_kazanim_obj["surec"])

    aktif_kriz = secilen_kazanim_obj["kriz"]
    odak_ogrenci_id = secilen_kazanim_obj.get("odak", "disleksi")

    ilgili_oturumlar = [o for o in st.session_state.simulasyon_gecmisi if o["kod"] == secilen_kazanim_obj["kod"]]
    aktif_oturum = ilgili_oturumlar[-1] if ilgili_oturumlar else None
    ogretmen_son_soz = aktif_oturum["sesli_komut"] if aktif_oturum else ""
    analiz_sonucu = aktif_oturum["analiz"] if aktif_oturum else None

    render_3d_classroom_10_students(
        ogretmen_adi=ogretmen,
        ogretmen_cinsiyeti=ogretmen_cinsiyeti,
        sinif_duzeyi=secilen_sinif,
        tema=secilen_tema,
        kazanim_kodu=secilen_kazanim_obj["kod"],
        secilen_materyal=secilen_materyal,
        odak_ogrenci_id=odak_ogrenci_id,
        ogretmen_sozu=ogretmen_son_soz,
        analiz_sonucu=analiz_sonucu,
    )

    col_sol, col_sag = st.columns([1.15, 0.85], gap="large")
    with col_sol:
        st.markdown("#### ⚡ Sınıf İçi Anlık Kriz ve Gerçek Yaşam Bağlamı")
        st.info(f"**Gerçek Yaşam Kancası:** {secilen_kazanim_obj['hook']}")
        st.warning(f"🔔 **Yaşanan Kriz Durumu:** {aktif_kriz}")

        st.markdown("### 🎙️ Sözlü / Sesli Geri Bildirim ve Materyal Kullanım Konsolu")
        st.caption("Cihazınızın klavyesindeki mikrofon (dikte) tuşuyla konuşarak veya doğrudan yazarak yanıtlarınızı girin. Yönlendirici gri metin bulunmamaktadır.")

        sesli_geri_bildirim_metni = st.text_area(
            "1. Öğrenciye Verdiğiniz Sözlü/Sesli Geri Bildirim ve Yaklaşım İfadesi:",
            value="",
            height=90,
        )

        materyal_kullanim_aciklamasi = st.text_area(
            "2. Seçtiğiniz Materyali Bu Kazanım İçin Derste Adım Adım Nasıl Kullandığınızı Yazın:",
            value="",
            height=85,
        )

        st.markdown("### 👩‍🏫 Kronolojik Pedagojik Eylem Sıralaması (Önce ve Sonra Yapılacaklar)")
        eylem_secenekleri = [
            "A) Öğrenciyi uyararak susturmak ve sınıf disiplinini sert kurallarla sağlamak.",
            "B) Ses tonunu yumuşatarak öğrencinin duygusunu kabul etmek ve güvenli iletişim alanı oluşturmak.",
            "C) Seçilen materyal üzerinden adım adım yönlendirici sorular sorarak kavramı öğrenciye keşfettirmek.",
            "D) Akran destekli grup tartışması başlatarak farklı çözüm stratejilerini karşılaştırmak.",
            "E) Duyusal/bilişsel yükü azaltmak için öğrenciye kısa bekleme süresi tanıyıp bireysel hazırbulunuşluğu desteklemek.",
            "F) Zaman kaybetmemek için kuralı ve formülü doğrudan tahtaya yazıp deftere geçirtmek.",
        ]

        ilk_eylem = st.selectbox("1. ÖNCE Yapacağınız Pedagojik Eylem:", eylem_secenekleri, index=0)
        ikinci_eylem = st.selectbox("2. SONRA Yapacağınız Pedagojik Eylem:", eylem_secenekleri, index=2)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            uygula_btn = st.button("📥 Kararları Uygula & Öğrenci Tepkilerini Güncelle", use_container_width=True)
        with col_btn2:
            if aktif_oturum is not None:
                st.button("🔄 Hataları Düzeltmek İçin Aynı Dersi Yeniden Uygula", use_container_width=True)

        if uygula_btn:
            if not sesli_geri_bildirim_metni.strip() or not materyal_kullanim_aciklamasi.strip():
                st.error("⚠️ Lütfen hem sözlü geri bildirim ifadenizi hem de materyali derste nasıl kullandığınızı eksiksiz yazınız.")
            else:
                onceki_puan = aktif_oturum["puan"] if aktif_oturum else None
                analiz = detayli_pedagojik_analiz_uret(
                    sesli_metin=sesli_geri_bildirim_metni.strip(),
                    ilk_eylem=ilk_eylem,
                    ikinci_eylem=ikinci_eylem,
                    secilen_materyal=secilen_materyal,
                    materyal_kullanim_aciklamasi=materyal_kullanim_aciklamasi.strip(),
                    kazanim_obj=secilen_kazanim_obj,
                    surec=secilen_surec,
                    rubrik_metni=st.session_state.get("rubrik_metni", ""),
                )
                st.session_state.simulasyon_gecmisi.append({
                    "oturum_no": len(st.session_state.simulasyon_gecmisi) + 1,
                    "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "sinif": secilen_sinif,
                    "tema": secilen_tema,
                    "kod": secilen_kazanim_obj["kod"],
                    "cikti": secilen_kazanim_obj["cikti"],
                    "surec": secilen_surec,
                    "materyal": secilen_materyal,
                    "materyal_kullanim": materyal_kullanim_aciklamasi.strip(),
                    "kriz": aktif_kriz,
                    "ilk_eylem": ilk_eylem,
                    "ikinci_eylem": ikinci_eylem,
                    "sesli_komut": sesli_geri_bildirim_metni.strip(),
                    "onceki_puan": onceki_puan,
                    "puan": analiz["toplam_puan"],
                    "analiz": analiz,
                })
                st.rerun()

        if aktif_oturum is not None:
            st.markdown("#### 📊 Anlık Müdahale, Puan Değişimi ve Rehber Dönüt")
            if aktif_oturum["onceki_puan"] is not None:
                fark = aktif_oturum["puan"] - aktif_oturum["onceki_puan"]
                st.success(
                    f"🔁 **Derse Geri Dönüp Düzeltme Etkisi:** Önceki Puanınız: **{aktif_oturum['onceki_puan']}** ➡️ "
                    f"Güncel Puanınız: **{aktif_oturum['puan']} / 100** (Değişim: **{'+' if fark >= 0 else ''}{fark} Puan**)"
                )
            else:
                st.info(f"🎯 **İlk Uygulama Puanınız:** **{aktif_oturum['puan']} / 100** (Aşağıdaki materyal ve profil hitabet rehberini inceleyip aynı dersi tekrar uygulayarak puan ve öğrenci tepkisi değişimini gözlemleyebilirsiniz.)")

            with st.expander("🔍 Anlık Hata Analizi, Yapılandırılmış Materyal Yönergesi ve Profil Hitabet Rehberi", expanded=True):
                for eks in aktif_oturum["analiz"]["eksik_yonler"]:
                    st.warning(eks)
                for coz in aktif_oturum["analiz"]["cozum_onerileri"]:
                    st.info(coz)
                st.markdown("##### 🛠️ Doğru Materyal Adım Adım Kullanım Yönergesi")
                st.success(aktif_oturum["analiz"]["program_uyum_analizi"]["dogru_materyal_yonergesi"])
                st.markdown("##### 🗣️ Profil Odaklı Hitabet ve Öğrenciye Davranış Rehberi")
                st.info(aktif_oturum["analiz"]["program_uyum_analizi"]["profil_hitabet_rehberi"])

            if st.button("📋 Tüm Detaylı Raporlara ve Yıl Sonu İlerleme Paneline Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()

    with col_sag:
        st.markdown("#### 👥 Cinsiyet ve Profillerine Göre 10 Öğrencinin Eylemsel Tepkileri")
        for ogr in genel_ogrenci_tipleri_detayli:
            durum = ogrenci_eylemsel_durum_belirle(ogr, odak_ogrenci_id, secilen_materyal, analiz_sonucu)
            with st.container(border=True):
                st.markdown(f"**{durum['yuz']} {ogr['ad']} ({durum['cinsiyet_etiket']}) — {ogr['tip']}** {'⭐ *(Kriz Odağı)*' if ogr['id'] == odak_ogrenci_id else ''}")
                st.caption(f"**Profil Özelliği:** {ogr['karakteristik']}")
                st.markdown(f"**Anlık Mimik & Eylemsel Tepki:** {durum['mimik']} | *{durum['tepki']}*")
                st.markdown(f"> 💬 *\"{durum['konusma']}\"*")

# ==========================================
# ADIM 3: DETAYLI RAPORLAR, RUBRİK TESTİ, PROGRAM UYUMU VE YIL SONU PORTFOLYOSU
# ==========================================
elif st.session_state.adim == 3:
    st.subheader("📊 ORTAOKUL MATEMATİK ÖĞRETMENLİĞİ DETAYLI RAPORLAMA VE YIL SONU İLERLEME SİSTEMİ")
    toplam_islem = len(st.session_state.simulasyon_gecmisi)
    ortalama_puan = int(sum(k["puan"] for k in st.session_state.simulasyon_gecmisi) / toplam_islem) if toplam_islem > 0 else 0

    tab_aday, tab_rubrik, tab_program, tab_dekanlik, tab_portfolyo, tab_anket = st.tabs([
        "👩‍🏫 1. Aday Detaylı Pedagojik Analiz & Rehberler",
        "📋 2. Uygulama Öğretim Elemanı Rubrik Uygunluk Testi",
        "📐 3. Öğretim Programı (TYMM 2026) & Materyal Yönergesi",
        "🏛️ 4. Dekanlık & Ortaokul Matematik Bölümü Raporu",
        "📈 5. Yıl Sonu Kümülatif İlerleme Dosyası",
        "⭐ 6. Adayların Uygulamayı Değerlendirme Formu",
    ])

    with tab_aday:
        if toplam_islem == 0:
            st.warning("Henüz oturum kaydedilmedi.")
        else:
            for idx, oturum in enumerate(st.session_state.simulasyon_gecmisi, 1):
                analiz = oturum["analiz"]
                prg = analiz["program_uyum_analizi"]
                with st.container(border=True):
                    baslik_ek = f" (Önceki Puan: {oturum['onceki_puan']} ➡️ Güncel: {oturum['puan']})" if oturum.get("onceki_puan") is not None else f" — Puan: {oturum['puan']}/100"
                    st.markdown(f"#### 📌 Uygulama #{idx}: {oturum['sinif']} | {oturum['tema']} (`{oturum['kod']}`){baslik_ek}")
                    st.markdown(
                        f"- **Öğrenme Çıktısı:** {oturum['cikti']}\n"
                        f"- **Süreç Bileşeni:** {oturum['surec']}\n"
                        f"- **Seçilen Materyal ve Adayın Kullanım Açıklaması:** {oturum['materyal']} — *{oturum['materyal_kullanim']}*\n"
                        f"- **1. Eylem (Önce):** {oturum['ilk_eylem']}\n"
                        f"- **2. Eylem (Sonra):** {oturum['ikinci_eylem']}\n"
                        f"- **Adayın Sözlü Geri Bildirimi:** *\"{oturum['sesli_komut']}\"*"
                    )
                    st.divider()
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        st.markdown("##### ✅ Nesnel İyi ve Güçlü Yönler")
                        for m in analiz["iyi_yonler"]:
                            st.success(m)
                        st.markdown("##### ⚠️ Eksik ve Geliştirilmesi Gereken Yönler")
                        for m in analiz["eksik_yonler"]:
                            st.warning(m)
                    with col_a2:
                        st.markdown("##### 🔍 Eksikliklerin Kök Nedenleri (Neden Kaynaklanıyor?)")
                        for m in analiz["kok_nedenler"]:
                            st.error(m)
                        st.markdown("##### 🛠️ Somut Çözüm Yolları (Ne Yapılırsa Çözülür?)")
                        for m in analiz["cozum_onerileri"]:
                            st.info(m)

                    st.markdown("##### 🧩 Yapılandırılmış Materyal Yönergesi (Adım Adım Doğru Kullanım)")
                    st.success(prg["dogru_materyal_yonergesi"])
                    st.markdown("##### 🗣️ Profil Odaklı Hitabet ve Öğrenciye Davranış Rehberi")
                    st.info(prg["profil_hitabet_rehberi"])

    with tab_rubrik:
        st.markdown("### 👨‍🏫 Uygulama Öğretim Elemanının Rubriğine Göre Davranış Uygunluk Testi")
        if toplam_islem > 0:
            son_oturum = st.session_state.simulasyon_gecmisi[-1]
            son_analiz = son_oturum["analiz"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Kronolojik Eylem Sırası", f"{son_analiz['siralama_puani']} / 25")
            c2.metric("Profil Odaklı Sözlü Hitabet", f"{son_analiz['hitabet_puani']} / 50")
            c3.metric("Materyal Seçimi & Kullanımı", f"{son_analiz['materyal_puani']} / 25")
            c4.metric("Toplam Rubrik Puanı", f"{son_analiz['toplam_puan']} / 100")

            st.dataframe(pd.DataFrame(son_analiz["rubrik_analiz_listesi"]), use_container_width=True, hide_index=True)

            st.markdown("#### 📘 Aynı Raporda Öğretim Programı (TYMM 2026 Ortaokul Matematik) Uygunluk Bölümü")
            prg = son_analiz["program_uyum_analizi"]
            st.info(
                f"- **Kazanım ve Program Felsefesi Uyumu:** {prg['kazanim_uyumu']}\n"
                f"- **Süreç Bileşeni İşletimi:** {prg['surec_bileseni_degerlendirmesi']}\n"
                f"- **Materyal ve Çoklu Temsil:** {prg['materyal_ve_coklu_temsil']}\n"
                f"- **Kapsayıcılık ve Farklılaştırma:** {prg['kapsayicilik_ve_farklilastirma']}"
            )

    with tab_program:
        st.markdown("### 📐 Dersin O An Kullanılan Ortaokul Matematik Öğretim Programına (TYMM 2026) Uygunluk Analizi")
        if toplam_islem > 0:
            for idx, oturum in enumerate(st.session_state.simulasyon_gecmisi, 1):
                prg = oturum["analiz"]["program_uyum_analizi"]
                with st.container(border=True):
                    st.markdown(f"#### 📐 Oturum #{idx} — `{oturum['kod']}` ({oturum['sinif']}) Program ve Materyal Uygunluk Raporu")
                    st.markdown(f"- **Genel Program Uyumu:** **{prg['kazanim_uyumu']}**")
                    st.markdown(f"- **Süreç Bileşeni Analizi:** {prg['surec_bileseni_degerlendirmesi']}")
                    st.markdown(f"- **Materyal Uygunluğu ve Kullanım Analizi:** {prg['materyal_ve_coklu_temsil']}")
                    st.markdown(f"- **10 Öğrenci Profiline Göre Farklılaştırma:** {prg['kapsayicilik_ve_farklilastirma']}")
                    st.markdown(prg["dogru_materyal_yonergesi"])
                    st.markdown(prg["profil_hitabet_rehberi"])

    with tab_dekanlik:
        st.markdown("### 🏛️ Dekanlık & İlköğretim / Ortaokul Matematik Öğretmenliği Bölümü Öz-Değerlendirme Raporu")
        st.info("Bu rapor, öğretmen adayının staja çıkıp çıkmamasına karar veren bir eleme belgesi değildir; **İlköğretim / Ortaokul Matematik Öğretmenliği Bölümü**'nün kendi öğretmen yetiştirme programındaki güçlü ve eksik yönlerini fark etmesi ve bölüm derslerini geliştirmesi içindir.")
        with st.container(border=True):
            st.markdown(
                "#### 1. Ortaokul Matematik Öğretmenliği Bölümünün Güçlü Yönleri\n"
                "- **TYMM 2026 Müfredat Hakimiyeti:** Öğretmen adayları 5, 6, 7 ve 8. sınıf matematik temalarını, öğrenme çıktılarını ve alt süreç bileşenlerini (`a, b, c, ç`) tanımaktadır.\n"
                "- **Somut ve Dijital Matematik Araçları Bilgisi:** Adaylar Oran Tahtası, birim küpler, cebir karoları, kesir çubukları ve GeoGebra gibi araçların kuramsal işlevini bilmektedir.\n\n"
                "#### 2. Bölüm Eğitiminde Fark Edilen Eksik Yönler\n"
                "- **Kriz Anında Kronolojik Eylem Sıralaması:** 10 farklı öğrenci profilinin bulunduğu ortaokul sınıflarında adaylar önce duyuşsal güven oluşturmadan doğrudan bilişsel/materyalsel yönergeye geçebilmektedir.\n"
                "- **Materyalin Adım Adım Sözel Yönergeye Dönüştürülmesi:** Doğru materyal seçilse bile özel gereksinimli veya kaygılı öğrenciye bu materyalin adım adım nasıl kullandırılacağının ifade edilmesinde eksiklikler gözlenmektedir.\n\n"
                "#### 3. Eksikliklerin Kök Nedenleri\n"
                "- Lisans düzeyindeki *Ortaokul Matematik Öğretimi* ve *Sınıf Yönetimi* derslerinde özel gereksinimli öğrenci profilleriyle matematiksel materyal uyarlamalarının uygulamalı olarak yeterince birleştirilmemesi.\n\n"
                "#### 4. Bölüm İçin Somut Çözüm Önerileri\n"
                "1. Ortaokul Matematik Öğretmenliği 3. ve 4. sınıf uygulama derslerinde bu 3B simülasyonun düzenli kullanılarak her adayın 10 öğrenci profiliyle deneyim kazanması.\n"
                "2. Her ortaokul matematik kazanımı için 'doğru materyal eşleştirmesi, adım adım materyal yönergesi ve profil odaklı hitabet' atölyelerinin ders içeriklerine eklenmesi."
            )

    with tab_portfolyo:
        st.markdown("### 📈 Öğretmen Adayı Yıl Sonu Kümülatif İlerleme Dosyası ve Genel Geri Dönüt")
        if toplam_islem > 0:
            df_portfolyo = pd.DataFrame([
                {
                    "Uygulama No": i + 1,
                    "Tarih": o["tarih"],
                    "Sınıf & Kazanım": f"{o['sinif']} - {o['kod']}",
                    "Seçilen Materyal": o["materyal"],
                    "Kronolojik Sıra Puanı (25)": o["analiz"]["siralama_puani"],
                    "Materyal Puanı (25)": o["analiz"]["materyal_puani"],
                    "Profil Hitabet Puanı (50)": o["analiz"]["hitabet_puani"],
                    "Toplam Puan (100)": o["puan"],
                }
                for i, o in enumerate(st.session_state.simulasyon_gecmisi)
            ])
            st.dataframe(df_portfolyo, use_container_width=True, hide_index=True)
            st.line_chart(df_portfolyo, x="Uygulama No", y="Toplam Puan (100)")

            ilk_p = st.session_state.simulasyon_gecmisi[0]["puan"]
            son_p = st.session_state.simulasyon_gecmisi[-1]["puan"]
            gelisim_farki = son_p - ilk_p
            st.success(
                f"📌 **Yıl Sonu Genel İlerleme Değerlendirmesi:** Ortaokul Matematik Öğretmenliği adayı toplam **{toplam_islem}** simülasyon uygulaması gerçekleştirmiştir. "
                f"İlk uygulama puanı **{ilk_p}**, son uygulama puanı **{son_p}** (Net Gelişim: **{'+' if gelisim_farki >= 0 else ''}{gelisim_farki} Puan**), "
                f"yıl genel ortalaması ise **{ortalama_puan}/100**'dür."
            )

    with tab_anket:
        st.markdown("### ⭐ Uygulamayı Kullanan Ortaokul Matematik Öğretmen Adayları İçin Değerlendirme Formu")
        with st.container(border=True):
            p1 = st.slider("1. 3B Sınıf Ortamı, Cinsiyet/Profil Temsili ve Eylemsel Öğrenci Tepkileri (1-5)", 1, 5, 5)
            p2 = st.slider("2. TYMM 2026 Ortaokul Matematik Kazanımları ve Adım Adım Materyal Yönergesi (1-5)", 1, 5, 5)
            p3 = st.slider("3. Profil Odaklı Hitabet Rehberi ve Hataları Düzeltip Tekrar Uygulama (1-5)", 1, 5, 5)
            p4 = st.slider("4. Rubrik Testi, Bölüm Öz-Değerlendirme ve Yıl Sonu İlerleme Raporu (1-5)", 1, 5, 5)
            begeni = st.text_area("Uygulamada Güçlü ve Faydalı Bulduğunuz Yönler:")
            oneri = st.text_area("Uygulamanın Geliştirilmesi İçin Önerileriniz:")
            if st.button("📨 Uygulama Değerlendirmesini Kaydet", use_container_width=True):
                if begeni.strip() or oneri.strip():
                    st.session_state.uygulama_degerlendirmeleri.append({
                        "Tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "Aday": st.session_state.get("ogretmen_adi", "Aday"),
                        "Ortalama Puan": round((p1 + p2 + p3 + p4) / 4.0, 2),
                        "Güçlü Yönler": begeni.strip(),
                        "Öneriler": oneri.strip(),
                    })
                    st.success("✅ Uygulama değerlendirmeniz kaydedildi!")

        if st.session_state.uygulama_degerlendirmeleri:
            st.dataframe(pd.DataFrame(st.session_state.uygulama_degerlendirmeleri), use_container_width=True, hide_index=True)

    st.divider()
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 3B Sınıfa Dön (Hatayı Düzelt veya Yeni Ders Uygula)", use_container_width=True):
            st.session_state.adim = 2
            st.rerun()
    with col_b2:
        tum_rapor_json = json.dumps({
            "aday": st.session_state.get("ogretmen_adi"),
            "cinsiyet": st.session_state.get("ogretmen_cinsiyeti"),
            "okul_no": st.session_state.get("okul_numarasi"),
            "universite": st.session_state.get("universite_adi"),
            "bolum": st.session_state.get("fakulte_bolum"),
            "ogretim_elemani": st.session_state.get("uygulama_ogretim_elemani"),
            "yil_sonu_ortalama_puan": ortalama_puan,
            "oturumlar": st.session_state.simulasyon_gecmisi,
            "uygulama_degerlendirmeleri": st.session_state.uygulama_degerlendirmeleri,
        }, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 Yıl Sonu Kümülatif İlerleme Dosyasını İndir (JSON)",
            data=tum_rapor_json,
            file_name=f"Ortaokul_Matematik_Portfolyo_{st.session_state.get('okul_numarasi', 'Aday')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_b3:
        if st.button("🔄 Tüm Simülasyonu Sıfırla", use_container_width=True):
            st.session_state.simulasyon_gecmisi = []
            st.session_state.adim = 1
            st.rerun()
