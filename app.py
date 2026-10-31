import datetime
import json
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TYMM 2026 Tam Müfredat & Kümülatif İlerleme Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "uygulama_degerlendirmeleri" not in st.session_state:
    st.session_state.uygulama_degerlendirmeleri = []
if "adim" not in st.session_state:
    st.session_state.adim = 1

# ==========================================
# 1. 10 FARKLI GENEL ÖĞRENCİ TİPİNİN ÇOK DETAYLI KARAKTERİSTİK PROFİLLERİ
# ==========================================
genel_ogrenci_tipleri_detayli = [
    {
        "id": "disleksi", "ad": "Kerem", "tip": "Disleksili Öğrenci", "renk": "#ef4444", "bg": "rgba(239, 68, 68, 0.25)",
        "karakteristik": "Harf ve basamak terslikleri yaşar, sayıların dizilimini algılarken çabuk yorulur. Somut renk kodları, basamak tabloları ve görsel şemalarla desteklenmeye mutlak surette ihtiyaç duyar.",
        "yanlis_yuz": "😣", "yanlis_postur": "🤦‍♂️", "yanlis_mimik": "Alnını ovuşturuyor, semboller gözünde birbirine giriyor", "yanlis_tepki": "Bilişsel yük aşırı arttı, sözel kural dayatması nedeniyle kapandı",
        "yanlis_konusma": "Öğretmenim sayılar ve semboller tahtada dans ediyor gibi, yine okuyamadım...",
        "dogru_yuz": "😊", "dogru_postur": "🙌", "dogru_mimik": "Yüzü aydınlandı, materyali parmağıyla takip ediyor", "dogru_tepki": "Renk kodları ve somut modelle basamakları hatasız okudu",
        "dogru_konusma": "Renk kodlu abaküs ve basamak tablosuyla görünce hiç karışmadı öğretmenim!"
    },
    {
        "id": "otizm", "ad": "Arda", "tip": "Otizm Spektrumlu Öğrenci", "renk": "#10b981", "bg": "rgba(16, 185, 129, 0.25)",
        "karakteristik": "Ani seslerden, kalabalıktan ve rutinin bozulmasından duyusal rahatsızlık duyar. Sakin, net, öngörülebilir ve yapılandırılmış aşamalı yönergelere ihtiyaç gösterir.",
        "yanlis_yuz": "😖", "yanlis_postur": "🎧", "yanlis_mimik": "Ellerini kulaklarına götürüyor, öne doğru sallanıyor", "yanlis_tepki": "Duyusal aşırı yüklenme ve kural belirsizliği krizi",
        "yanlis_konusma": "Çok ses var ve kurallar ani değişti, kulaklığımı takmak zorundayım!",
        "dogru_yuz": "🙂", "dogru_postur": "🧩", "dogru_mimik": "Sakinleşti, omuzları gevşedi, modele odaklandı", "dogru_tepki": "Sakin ses tonu ve net aşamalı yönergeyle güven kazandı",
        "dogru_konusma": "Şimdi adımlar çok net oldu öğretmenim, örüntüyü modelde görebiliyorum."
    },
    {
        "id": "ustun", "ad": "Can", "tip": "Üstün Yetenekli Öğrenci", "renk": "#f59e0b", "bg": "rgba(245, 158, 11, 0.25)",
        "karakteristik": "Standart açıklamaları ve rutin işlemleri çabuk kavrar. Derinleştirici, ispat edici ve zenginleştirilmiş akran tartışmalarıyla beslenmezse derste egosal çatışma çıkarır.",
        "yanlis_yuz": "😤", "yanlis_postur": "🙋‍♂️", "yanlis_mimik": "Sabırsızca el kaldırıyor, kaşları çatık", "yanlis_tepki": "Basit açıklamalar nedeniyle sıkıldı ve huzursuz",
        "yanlis_konusma": "Hocam bu çok basit, neden doğrudan üst düzey formüle ve ispatına geçmiyoruz?",
        "dogru_yuz": "🤩", "dogru_postur": "💡", "dogru_mimik": "Gözleri parlıyor, yeni kanıt arıyor", "dogru_tepki": "Derinleştirici soruyla üretime ve mantıksal ispatta liderliğe yönlendirildi",
        "dogru_konusma": "Gerçek yaşam örneği üzerinden düşününce aradaki matematiksel ispatı buldum!"
    },
    {
        "id": "kaygili", "ad": "Elif", "tip": "Yüksek Kaygılı / STU-1309", "renk": "#38bdf8", "bg": "rgba(56, 189, 248, 0.25)",
        "karakteristik": "Hata yapmaktan, arkadaşlarının yanında mahcup olmaktan ve tahtaya kalkmaktan aşırı derecede çekinir. Sürekli onay bekler; baskı altında zihinsel blokaj yaşar.",
        "yanlis_yuz": "😰", "yanlis_postur": "🙇‍♀️", "yanlis_mimik": "Başını sıraya eğmiş, kalemini sıkarak tutuyor", "yanlis_tepki": "Hata yapma korkusu nedeniyle zihinsel olarak kilitlendi",
        "yanlis_konusma": "Ya yanlış yaparsam ve herkes bana gülerse? Korkudan defterime bile yazamıyorum...",
        "dogru_yuz": "😄", "dogru_postur": "✍️", "dogru_mimik": "Başını kaldırdı, özgüvenle gülümsüyor", "dogru_tepki": "Güvenli alan ve duyuşsal destekle hatasız katılım sağladı",
        "dogru_konusma": "Hata yapmanın öğrenmenin normal bir parçası olduğunu hissettirdiğiniz için teşekkür ederim."
    },
    {
        "id": "mukemmeliyetci", "ad": "Zeynep", "tip": "Mükemmeliyetçi Öğrenci", "renk": "#8b5cf6", "bg": "rgba(139, 92, 246, 0.25)",
        "karakteristik": "En küçük hesap hatasında veya cetvel çizim kaymasında tüm kağıdı yırtıp yeniden yazmak ister. Süreç odaklı olmaktan ziyade kusursuz sonuca odaklıdır.",
        "yanlis_yuz": "🧐", "yanlis_postur": "📝", "yanlis_mimik": "Kağıdı titizlikle inceliyor, küçük bir kayma için stresli", "yanlis_tepki": "Ufak bir detay takıntısı nedeniyle zaman yönetimi bozuldu",
        "yanlis_konusma": "Çizimim 1 milimetre kaydı, bu ödev mahvoldu baştan çizmeliyim!",
        "dogru_yuz": "😌", "dogru_postur": "👍", "dogru_mimik": "Rahatladı, sürecin kendisine odaklandı", "dogru_tepki": "Süreç odaklı değerlendirmeyi benimsedi",
        "dogru_konusma": "Kusursuz olmak zorunda değilmişim, önemli olan matematiksel mantığı kavramammış."
    },
    {
        "id": "direncli", "ad": "Mert", "tip": "Ödev/Kural Direnci Gösteren", "renk": "#64748b", "bg": "rgba(100, 116, 139, 0.25)",
        "karakteristik": "Otoriteye ve kurallara karşı mesafe koyar. 'Bunu neden öğreniyoruz, günlük hayatta nerede kullanacağız?' diyerek dersin işleyişini sorgular ve direnç gösterir.",
        "yanlis_yuz": "😒", "yanlis_postur": "🚶‍♂️", "yanlis_mimik": "Kollarını kavuşturmuş, arkasına yaslanmış", "yanlis_tepki": "Derse ve kurala karşı açık direnç gösteriyor",
        "yanlis_konusma": "Bunu hayatta hiçbir yerde kullanmayacağız, boşuna uğraşmayın yapmıyorum.",
        "dogru_yuz": "🤔", "dogru_postur": "💡", "dogru_mimik": "İlgiyle tahtaya ve gerçek yaşam kancasına bakıyor", "dogru_tepki": "Gerçek yaşam bağlamı (hook) ile ikna oldu",
        "dogru_konusma": "Gerçek yaşamdaki karşılığını bu şekilde görünce mantıklı geldiğini kabul ediyorum."
    },
    {
        "id": "icedonuk", "ad": "Merve", "tip": "Sosyal İçe Dönük Öğrenci", "renk": "#ec4899", "bg": "rgba(236, 72, 153, 0.25)",
        "karakteristik": "Doğrudan hedef tahtası olmaktan kaçınır. Sorulduğunda fısıltıyla konuşur; topluluk önünde zorlanmaktansa pasif kalmayı tercih eder.",
        "yanlis_yuz": "😶", "yanlis_postur": "🪞", "yanlis_mimik": "Başını öne eğmiş, göz temasından kaçınıyor", "yanlis_tepki": "Topluluk baskısı nedeniyle tamamen kabuğuna çekildi",
        "yanlis_konusma": "Ben parmak kaldırmamıştım, lütfen soru bana gelmesin...",
        "dogru_yuz": "🙂", "dogru_postur": "📖", "dogru_mimik": "Sakin bir şekilde kendi defterine not alıyor", "dogru_tepki": "Birebir destek ve güvenli hitabetle rahatladı",
        "dogru_konusma": "Bana topluluk önünde doğrudan baskı yapmadan birebir sormanız rahat hissettirdi."
    },
    {
        "id": "hareketli", "ad": "Emre", "tip": "Aşırı Hareketli / Dürtüsel", "renk": "#3b82f6", "bg": "rgba(59, 130, 246, 0.25)",
        "karakteristik": "Sırada sabit oturan kalamaz, nesnelerle oynamak ister, dürtüsel reaksiyonlar gösterir. Kinestetik ve fiziksel manipülatif görevlerle enerjisi yapılandırılmalıdır.",
        "yanlis_yuz": "🤪", "yanlis_postur": "🤸‍♂️", "yanlis_mimik": "Sırada kıpırdanıp duruyor, kalemiyle oynuyor", "yanlis_tepki": "Motor beceri enerjisi akışı bozdu",
        "yanlis_konusma": "Hocam kalemi düşürdüm, silgiyi arıyorum, tahtaya kalkabilir miyim?",
        "dogru_yuz": "🤩", "dogru_postur": "🛠️", "dogru_mimik": "Materyali bizzat elleriyle aktif olarak kullanıyor", "dogru_tepki": "Kinestetik materyalle enerjisi doğru yöne kanalize oldu",
        "dogru_konusma": "Materyali bizzat benim hareket ettirmeme izin verdiğiniz için odaklanabildim."
    },
    {
        "id": "sozelgucluk", "ad": "Burak", "tip": "Sözel İfade Güçlüğü Yaşayan", "renk": "#14b8a6", "bg": "rgba(20, 184, 166, 0.25)",
        "karakteristik": "Matematiksel mantığı zihninde kurabilir ancak bunu sözel terimlerle açıklarken doğru kelimeleri bulamaz. Görsel ve yazılı modellerle kendini rahat ifade eder.",
        "yanlis_yuz": "🤔", "yanlis_postur": "🤷‍♂️", "yanlis_mimik": "Kelimeleri arıyor, elleriyle havada şekiller çiziyor", "yanlis_tepki": "Sözel ifade baskısı nedeniyle tıkanıp kaldı",
        "yanlis_konusma": "Şey... hani böyle yukarı doğru gidiyor ya, işte o şey...",
        "dogru_yuz": "😃", "dogru_postur": "👉", "dogru_mimik": "Modeli işaret ederek parmağıyla gösteriyor", "dogru_tepki": "Görsel ve somut temsil ile kendini rahatça ifade etti",
        "dogru_konusma": "Sözel olarak söyleyemediğimi şekil üzerinde gösterdiğimde beni anladınız."
    },
    {
        "id": "gorseluzamsal", "ad": "Selin", "tip": "Görsel/Uzamsal Ağırlıklı", "renk": "#84cc16", "bg": "rgba(132, 204, 22, 0.25)",
        "karakteristik": "Saf sözel formülleri ezberlemekte zorlanır ancak geometrik simetrileri, örüntüleri ve uzamsal ilişkileri anında görsel olarak kavrar.",
        "yanlis_yuz": "🎨", "yanlis_postur": "👁️", "yanlis_mimik": "Tahtaya bakıp kafasını kaşıyor, yazılanları anlamlandıramıyor", "yanlis_tepki": "Saf sözel anlatım uzamsal zekaya hitap etmedi",
        "yanlis_konusma": "Sözel formülü okuduğumda anlamıyorum ama çizimini yaparsanız anlarım.",
        "dogru_yuz": "😎", "dogru_postur": "📐", "dogru_mimik": "Geometrik şemayı ve modeli büyük bir ilgiyle inceliyor", "dogru_tepki": "Görsel şema ve uzamsal modelle konuyu anında kavradı",
        "dogru_konusma": "Görsel şema üzerinden anlatınca taşlar tam yerine oturdu."
    },
]

materyal_havuzu = [
    "Oran Tahtası ve Renkli Boncuklar",
    "Onluk Taban Blokları ve Sayı Doğrusu",
    "Birim Küpler ve 3B Prizma Modelleri",
    "Cebir Karoları ve Denge Terazisi",
    "Simetri Aynası ve İzometrik Noktalı Kağıt",
    "GeoGebra Dinamik Geometri Yazılımı",
    "Basamak Tablosu ve Renkli Abaküs",
    "Kesir Takımları ve Yüzlük Kartlar",
    "Olasılık Spektrumu Şeridi ve Çarkı",
    "KVKK Etkileşimli Veri Toplama Panosu"
]

tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "MAT.5.1. Sayılar ve Nicelikler", "MAT.5.2. İşlemlerle Cebirsel Düşünme",
            "MAT.5.3. Geometrik Şekiller", "MAT.5.4. Geometrik Nicelikler",
            "MAT.5.5. İstatistiksel Araştırma Süreci", "MAT.5.6. Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "MAT.5.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1", "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
                    "surec": [
                        "a) Günlük hayattaki bağlamlardan yola çıkarak çok basamaklı sayılar hakkında bilgi toplar.",
                        "b) Sayıların bölümleri ile okunuşları arasındaki ortak özellikleri belirler.",
                        "c) Sayıların bölümleri ile okunuşları arasındaki farklılıkları belirler."
                    ],
                    "uygun_materyaller": ["Basamak Tablosu ve Renkli Abaküs", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Millî Kütüphane'deki 405.020 adet tarihi el yazması kitabın arşiv kodlama sistemi.",
                    "kriz": "Kerem tahtadaki 405.020 sayısını okurken basamakları karıştırır, bazı öğrenciler güler.",
                    "odak": "disleksi",
                },
                {
                    "kod": "MAT.5.1.2", "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) İşlem gerektiren günlük yaşam durumlarında nicelikleri inceler.",
                        "b) Zihinden işlem ve tahmin stratejileri geliştirir."
                    ],
                    "uygun_materyaller": ["Onluk Taban Blokları ve Sayı Doğrusu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Okul kermesinde toplanan bağışların hedef bütçe ile karşılaştırılması.",
                    "kriz": "Can zihinden işlem stratejisini dinlemeyip 'Ben zaten sonucu buldum, neden uzatıyoruz?' diyerek araya girer.",
                    "odak": "ustun",
                },
            ],
            "MAT.5.2. İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.5.2.1", "cikti": "Eşitliğin korunumu ve işlem özelliklerini muhakeme edebilme",
                    "surec": ["a) Eşit kollu terazi modelleri üzerinde eşitlik durumlarını inceler."],
                    "uygun_materyaller": ["Cebir Karoları ve Denge Terazisi", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Laboratuvardaki eşit kollu terazide farklı kütleleri dengeleme deneyi.",
                    "kriz": "Can eşittir işaretinin sadece 'sonuç' demek olmadığını savunarak dersi yönlendirmeye çalışır.",
                    "odak": "ustun",
                }
            ],
            "MAT.5.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.5.3.1", "cikti": "Temel geometrik çizimler için matematiksel araç ve teknolojileri kullanabilme",
                    "surec": ["a) Nokta, doğru, doğru parçası ve ışın kavramlarını inşa araçlarıyla inceler."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Mimari kroki çizimlerinde açıölçer kullanarak simetrik bahçe tasarımı yapma.",
                    "kriz": "Kerem açıölçeri ters tutarak ölçüm yapar ve hata yapınca sinirlenip kalemi bırakır.",
                    "odak": "disleksi",
                }
            ],
            "MAT.5.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.4.1", "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkiyi yapılandırabilme",
                    "surec": ["a) Birim kareler kullanarak dikdörtgenin alanını ve çevresini modeller."],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Okul bahçesine sabit uzunluktaki çitle en geniş alana sahip hobi bahçesi kurma.",
                    "kriz": "Elif alan ile çevre formüllerini karıştırıp yanlış yapma korkusuyla ağlamaklı olur.",
                    "odak": "kaygili",
                }
            ],
            "MAT.5.5. İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.5.1", "cikti": "Kategorik verilerle istatistiksel araştırma sürecini yürütebilme ve görselleştirebilme",
                    "surec": ["a) Kategorik veri toplamayı gerektiren araştırma sorusu oluşturur."],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Sınıf kütüphanesine alınacak kitap türlerini belirlemek için veri toplama.",
                    "kriz": "Merve gruptakilerle konuşmaktan çekinip anket verilerini vermeyi reddeder.",
                    "odak": "icedonuk",
                }
            ],
            "MAT.5.6. Veriden Olasılığa": [
                {
                    "kod": "MAT.5.6.1", "cikti": "Olayların olasılığını olasılık spektrumu üzerinde yorumlayabilme",
                    "surec": ["a) Günlük yaşam olaylarını gerçekleşme ihtimallerine göre inceler."],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Hava durumu raporlarına göre yağmur yağma ihtimalini tartışma.",
                    "kriz": "Emre sınıfta ayağa kalkıp spektrum şeridini havaya fırlatır.",
                    "odak": "hareketli",
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": [
            "MAT.6.1. Sayılar ve Nicelikler", "MAT.6.2. İşlemlerle Cebirsel Düşünme",
            "MAT.6.3. Geometrik Şekiller", "MAT.6.4. Geometrik Nicelikler",
            "MAT.6.5. İstatistiksel Araştırma", "MAT.6.6. Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "MAT.6.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1", "cikti": "Çarpan, kat ve asal sayı özelliklerine yönelik muhakeme yapabilme",
                    "surec": ["a) Çarpan ve katlarına yönelik varsayımlarda bulunur."],
                    "uygun_materyaller": ["Basamak Tablosu ve Renkli Abaküs", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Farklı periyotlarla sefer yapan iki vapurun buluşma saati.", "kriz": "Mert ödev direnci gösterir.", "odak": "direncli"
                }
            ],
            "MAT.6.2. İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.6.2.1", "cikti": "Bilinmeyen nicelikleri değişkenlerle temsil edebilme",
                    "surec": ["a) Sözel durumları değişken kullanarak cebirsel ifadeye dönüştürür."],
                    "uygun_materyaller": ["Cebir Karoları ve Denge Terazisi", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Kumbaraya her hafta eklenen paranın n. haftadaki tutarı.", "kriz": "Kerem harflere tepki gösterir.", "odak": "disleksi"
                }
            ],
            "MAT.6.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1", "cikti": "Paralel iki doğrunun bir kesenle yaptığı açıları keşfedebilme",
                    "surec": ["a) Paralel doğrular ve kesen arasındaki açıları inceler."],
                    "uygun_materyaller": ["GeoGebra Dinamik Geometri Yazılımı", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Demiryolu makas kesişimlerindeki açıların dengesi.", "kriz": "Arda ekrandaki hareketten duyusal rahatsızlık yaşar.", "odak": "otizm"
                }
            ],
            "MAT.6.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.1", "cikti": "Üçgen ve paralelkenarın alan bağıntılarını oluşturabilme",
                    "surec": ["a) Paralelkenarı kes-yapıştır stratejisiyle dönüştürür."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "Birim Küpler ve 3B Prizma Modelleri"],
                    "hook": "Tarım parsellerinin sulama alanlarını hesaplama.", "kriz": "Selin şekli zihninde döndüremediği için alanı yanlış konumlandırır.", "odak": "gorseluzamsal"
                }
            ],
            "MAT.6.5. İstatistiksel Araştırma": [
                {
                    "kod": "MAT.6.5.1", "cikti": "Merkezi eğilim ölçülerini hesaplayıp yorumlayabilme",
                    "surec": ["a) Aritmetik ortalama ve medyan hesaplar."],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Basketbol takımının maç başına attığı sayı analizi.", "kriz": "Zeynep hata yapınca kağıdı buruşturur.", "odak": "mukemmeliyetci"
                }
            ],
            "MAT.6.6. Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1", "cikti": "Deneysel olasılığı göreli sıklık üzerinden tahmin edebilme",
                    "surec": ["a) Tekrarlı olasılık deneyleri tasarlar."],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "100 kez atılan zarın analizi.", "kriz": "Emre zarları masaya saçıp bağırmaya başlar.", "odak": "hareketli"
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "MAT.7.1. Sayılar ve Nicelikler", "MAT.7.2. İşlemlerle Cebirsel Düşünme",
            "MAT.7.3. Dönüşüm", "MAT.7.4. Geometrik Nicelikler",
            "MAT.7.5. Geometrik Şekiller", "MAT.7.6. İstatistiksel Araştırma", "MAT.7.7. Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "MAT.7.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.1", "cikti": "Tam sayılar ve rasyonel sayılarla işlemler yapabilme",
                    "surec": ["a) Rasyonel sayılarla işlemleri modeller."],
                    "uygun_materyaller": ["Onluk Taban Blokları ve Sayı Doğrusu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Hava sıcaklığı ve derinlik hesapları.", "kriz": "Kerem işaretleri karıştırır.", "odak": "disleksi"
                },
                {
                    "kod": "MAT.7.1.2", "cikti": "Oran ve orantı kavramlarını yapılandırarak doğru ve ters orantı kurabilme",
                    "surec": ["a) Oran Tahtası ve somut materyallerle ilişkileri inceler."],
                    "uygun_materyaller": ["Oran Tahtası ve Renkli Boncuklar", "Cebir Karoları ve Denge Terazisi"],
                    "hook": "Renk karışım oranları.", "kriz": "Elif hata yapmaktan korkar.", "odak": "kaygili"
                },
            ],
            "MAT.7.2. İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.7.2.1", "cikti": "Denklem ve eşitsizlikleri çözebilme",
                    "surec": ["a) Denklemleri kurar ve çözer."],
                    "uygun_materyaller": ["Cebir Karoları ve Denge Terazisi", "Onluk Taban Blokları ve Sayı Doğrusu"],
                    "hook": "Asansör taşıma kapasitesi.", "kriz": "Burak ifadeyi sözel dile getiremez.", "odak": "sozelgucluk"
                }
            ],
            "MAT.7.3. Dönüşüm": [
                {
                    "kod": "MAT.7.3.1", "cikti": "Yansıma dönüşümünü ve simetri inşalarını gerçekleştirebilme",
                    "surec": ["a) Şekillerin yansıma görüntülerini inceler."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Mimari cephe tasarımlarında simetri.", "kriz": "Selin simetri eksenini ters çizer.", "odak": "gorseluzamsal"
                }
            ],
            "MAT.7.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.7.4.1", "cikti": "Prizmaların yüzey alanı ve hacmini hesaplayabilme",
                    "surec": ["a) Prizma hacmini modeller."],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "Simetri Aynası ve İzometrik Noktalı Kağıt"],
                    "hook": "Çikolata kutusu tasarımı.", "kriz": "Arda küplerin sesinden rahatsız olur.", "odak": "otizm"
                }
            ],
            "MAT.7.5. Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1", "cikti": "Üçgende kenarortay ve açıortay inşa edebilme",
                    "surec": ["a) Pergel ve cetvelle inşa eder."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Üçgen tepsinin ağırlık merkezi.", "kriz": "Mert 'Bunu öğrenmek zorunda değiliz' der.", "odak": "direncli"
                }
            ],
            "MAT.7.6. İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.6.1", "cikti": "Çizgi ve daire grafiği yorumlama",
                    "surec": ["a) Daire grafiğinde merkez açılarla modeller."],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Olasılık Spektrumu Şeridi ve Çarkı"],
                    "hook": "Hava sıcaklığı değişim grafikleri.", "kriz": "Zeynep hesaplamada takılır.", "odak": "mukemmeliyetci"
                }
            ],
            "MAT.7.7. Veriden Olasılığa": [
                {
                    "kod": "MAT.7.7.1", "cikti": "Teorik olasılık hesaplama",
                    "surec": ["a) İstenen durumun tüm durumlara oranını hesaplar."],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Şifreli kasa kombinasyonları.", "kriz": "Can belirsizliklere itiraz eder.", "odak": "ustun"
                }
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "MAT.8.1. Sayılar ve Nicelikler", "MAT.8.2. Cebirsel Düşünme",
            "MAT.8.3. Geometrik Şekiller", "MAT.8.4. Geometrik Nicelikler",
            "MAT.8.5. Dönüşüm", "MAT.8.6. İstatistiksel Araştırma", "MAT.8.7. Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "MAT.8.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.1", "cikti": "Üslü ve kareköklü ifadeleri gerçek sayılar kümesi bağlamında muhakeme edebilme",
                    "surec": ["a) Karenin alanından karekökü yapılandırır."],
                    "uygun_materyaller": ["Onluk Taban Blokları ve Sayı Doğrusu", "Birim Küpler ve 3B Prizma Modelleri"],
                    "hook": "Hücre boyutları.", "kriz": "Arda irrasyonel sayıların sonsuzluğundan rahatsız olur.", "odak": "otizm"
                }
            ],
            "MAT.8.2. Cebirsel Düşünme": [
                {
                    "kod": "MAT.8.2.1", "cikti": "Doğrusal fonksiyonlar ve eğim kavramını yapılandırabilme",
                    "surec": ["a) Eğim oranını yorumlar."],
                    "uygun_materyaller": ["Cebir Karoları ve Denge Terazisi", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Engelli rampası standartları.", "kriz": "Elif sınav kaygısı yaşar.", "odak": "kaygili"
                }
            ],
            "MAT.8.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.1", "cikti": "Pisagor bağıntısı ve benzerlik uygulamaları",
                    "surec": ["a) Pisagor bağıntısını uygular."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "Birim Küpler ve 3B Prizma Modelleri"],
                    "hook": "İtfaiye merdiveni yüksekliği.", "kriz": "Kerem formülü yanlış yere uygular.", "odak": "disleksi"
                }
            ],
            "MAT.8.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1", "cikti": "Silindir, piramit ve koninin yüzey alanı ve hacmi",
                    "surec": ["a) Hacim bağıntısı kurar."],
                    "uygun_materyaller": ["Birim Küpler ve 3B Prizma Modelleri", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Silindirik depolar.", "kriz": "Emre kağıtları havaya atar.", "odak": "hareketli"
                }
            ],
            "MAT.8.5. Dönüşüm": [
                {
                    "kod": "MAT.8.5.1", "cikti": "Koordinat sisteminde öteleme ve yansıma dönüşümleri",
                    "surec": ["a) Koordinat değişimini inceler."],
                    "uygun_materyaller": ["Simetri Aynası ve İzometrik Noktalı Kağıt", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Oyun koordinatları.", "kriz": "Selin simetriyi zihninde canlandıramaz.", "odak": "gorseluzamsal"
                }
            ],
            "MAT.8.6. İstatistiksel Araştırma": [
                {
                    "kod": "MAT.8.6.1", "cikti": "Bilimsel araştırma etiği ve KVKK ilkelerine uygun proje",
                    "surec": ["a) KVKK ve etik kurallara uyar."],
                    "uygun_materyaller": ["KVKK Etkileşimli Veri Toplama Panosu", "Basamak Tablosu ve Renkli Abaküs"],
                    "hook": "Ekran süresi araştırması.", "kriz": "Can kişisel verileri paylaşmak ister.", "odak": "ustun"
                }
            ],
            "MAT.8.7. Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1", "cikti": "Simülasyonlarla deneysel ve teorik olasılık ilişkisi",
                    "surec": ["a) Büyük sayılar yasasını gözlemler."],
                    "uygun_materyaller": ["Olasılık Spektrumu Şeridi ve Çarkı", "GeoGebra Dinamik Geometri Yazılımı"],
                    "hook": "Kalite kontrol testi.", "kriz": "Mert yasaya itiraz eder.", "odak": "direncli"
                }
            ],
        },
    },
}

# ==========================================
# 3B SAHNE RENDER FONKSİYONU (DİNAMİK EMOJİLER VE TEPKİLER)
# ==========================================
def render_3d_classroom_10_students_dynamic_v2(
    ogretmen_adi,
    sinif_duzeyi,
    tema,
    kazanim_kodu,
    secilen_materyal,
    odak_ogrenci_id,
    ogretmen_sozu,
    sesli_analiz_sonucu,
):
    ogretmen_balon = (
        ogretmen_sozu
        if ogretmen_sozu
        else f"Arkadaşlar, seçtiğimiz ({secilen_materyal}) üzerinden durumu birlikte inceleyelim..."
    )

    kartlar_html = ""
    for ogr in genel_ogrenci_tipleri_detayli:
        is_odak = (ogr["id"] == odak_ogrenci_id)
        vurgu_stil = (
            "box-shadow: 0 0 22px rgba(250, 204, 21, 0.95); transform: translateY(-5px) scale(1.03); border-color: #fde047;"
            if is_odak
            else ""
        )
        
        if is_odak:
            if sesli_analiz_sonucu and sesli_analiz_sonucu["yapilandirmaci_mi"]:
                yuz = ogr["dogru_yuz"]
                postur = ogr["dogru_postur"]
                mimik = ogr["dogru_mimik"]
                tepki = ogr["dogru_tepki"]
                konusma = ogr["dogru_konusma"]
                durum_renk = "#22c55e"
            elif sesli_analiz_sonucu:
                yuz = ogr["yanlis_yuz"]
                postur = ogr["yanlis_postur"]
                mimik = "Kısmi rehberlik, konuyu anlamaya çalışıyor"
                tepki = "Eksik sıralama veya yetersiz materyal kullanımı"
                konusma = "Hala tam oturmadı ama deniyorum..."
                durum_renk = "#f59e0b"
            else:
                yuz = ogr["yanlis_yuz"]
                postur = ogr["yanlis_postur"]
                mimik = ogr["yanlis_mimik"]
                tepki = ogr["yanlis_tepki"]
                konusma = ogr["yanlis_konusma"]
                durum_renk = ogr["renk"]
        else:
            yuz = "😊"
            postur = "📖"
            mimik = "Sakin, akran grubuna odaklı"
            tepki = "Akran öğrenme sürecinde"
            konusma = f"Biz de masamızda {secilen_materyal} ile çalışıyoruz."
            durum_renk = "#38bdf8"

        kartlar_html += f"""
        <div class="desk-unit" style="border-color: {durum_renk}; {vurgu_stil}">
            <div class="speech-bubble" style="border-left: 4px solid {durum_renk};">
                💬 "{konusma}"
            </div>
            <div class="avatar-circle" style="background: {ogr['bg']}; border-color: {durum_renk};">
                <span class="avatar-face">{yuz}</span>
                <span class="posture-badge">{postur}</span>
            </div>
            <div class="desk-surface">
                <div class="student-name">{ogr['ad']}</div>
                <div class="student-type">{ogr['tip']}</div>
                <div class="gesture-tag" style="color: {durum_renk};">🎭 {mimik}</div>
                <div class="reaction-tag">⚡ {tepki}</div>
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
            padding: 10px 16px; text-align: center; max-width: 85%; margin: 0 auto 14px auto; box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        }}
        .smartboard-title {{ color: #fde047; font-weight: 700; font-size: 14px; }}
        .smartboard-sub {{ color: #d1fae5; font-size: 12px; margin-top: 3px; }}
        .teacher-zone {{
            display: flex; align-items: center; justify-content: center; gap: 14px; margin: 10px auto 16px auto;
            padding: 10px 14px; max-width: 80%; background: linear-gradient(90deg, rgba(30, 58, 138, 0.7), rgba(30, 64, 175, 0.5));
            border: 2px solid #60a5fa; border-radius: 12px;
        }}
        .teacher-avatar {{
            width: 52px; height: 52px; border-radius: 50%; background: #1d4ed8; border: 2px solid #93c5fd;
            display: flex; align-items: center; justify-content: center; font-size: 28px; flex-shrink: 0;
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
            min-height: 44px; display: flex; align-items: center; line-height: 1.3;
        }}
        .avatar-circle {{
            width: 48px; height: 48px; border-radius: 50%; border: 2px solid;
            display: flex; align-items: center; justify-content: center; position: relative; margin-bottom: 6px;
        }}
        .avatar-face {{ font-size: 24px; }}
        .posture-badge {{
            position: absolute; bottom: -2px; right: -4px; background: #0f172a;
            border-radius: 50%; padding: 1px 3px; font-size: 12px; border: 1px solid #94a3b8;
        }}
        .desk-surface {{
            width: 100%; background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
            border-top: 3px solid #ca8a04; border-radius: 6px; padding: 6px; text-align: center;
        }}
        .student-name {{ font-weight: 700; font-size: 12px; color: #f1f5f9; }}
        .student-type {{ font-size: 10px; color: #94a3b8; margin-bottom: 3px; }}
        .gesture-tag {{ font-size: 10px; font-weight: 600; margin-bottom: 2px; }}
        .reaction-tag {{ font-size: 9.5px; color: #cbd5e1; background: rgba(15, 23, 42, 0.7); padding: 3px 4px; border-radius: 4px; }}
    </style>
    </head>
    <body>
    <div class="scene-wrapper">
        <div class="classroom-header">
            <span>🏫 <strong>3B Sınıf Ortamı (10 Farklı Genel Öğrenci Profili)</strong></span>
            <span>🟢 Sınıf Mevcudu: 10 Aktif Profil</span>
        </div>
        <div class="smartboard">
            <div class="smartboard-title">📐 {sinif_duzeyi} | {tema} ({kazanim_kodu})</div>
            <div class="smartboard-sub">🛠️ Seçilen Materyal: {secilen_materyal}</div>
        </div>
        <div class="teacher-zone">
            <div class="teacher-avatar">👩‍🏫</div>
            <div>
                <div style="font-size: 11px; color: #93c5fd; font-weight: 700; margin-bottom: 2px;">ÖĞRETMEN ADAYI ({ogretmen_adi}) HİTABETİ:</div>
                <div class="teacher-speech">🎙️ "{ogretmen_balon}"</div>
            </div>
        </div>
        <div class="isometric-floor-10">
            {kartlar_html}
        </div>
    </div>
    </body>
    </html>
# ==========================================
# NESNEL ANALİZ, MATERYAL UYUMU VE KRONOLOJİK EYLEM MOTORU
# ==========================================
def detayli_pedagojik_analiz_uret_gelismis_v3(
    sesli_metin,
    secilen_karar_metni,
    secilen_materyal,
    kazanim_obj,
    surec,
    rubrik_metni,
    ses_kaydi_var,
):
    kucuk_metin = sesli_metin.lower()

    # 1. Kronolojik Eylem Sıralaması Puanı (Önce güvenli alan/empati, sonra somut materyal ve sorgulama)
    ilk_adim_dogru = "b)" in secilen_karar_metni.lower() or "e)" in secilen_karar_metni.lower()
    siralama_puani = 25 if ilk_adim_dogru else 10

    # 2. Seçilen Materyalin Konuya Uygunluk Değerlendirmesi
    uygun_materyaller = kazanim_obj.get("uygun_materyaller", [])
    materyal_konuya_uygun = secilen_materyal in uygun_materyaller
    materyal_puan = 25 if materyal_konuya_uygun else 10

    # 3. Sesli Geri Bildirim ve Hitabet Kalitesi
    empati_kelimeleri = ["sakin", "birlikte", "anlıyorum", "endişelenme", "nefes", "yanındayım", "dinliyorum", "haklısın"]
    materyal_hitabet_var = any(k in kucuk_metin for k in ["materyal", "model", "oran", "boncuk", "küp", "geogebra", "kesir", "terazi", "karo", "tablo", "somut", secilen_materyal.lower().split()[0]])
    sorgulama_var = any(k in kucuk_metin for k in ["nasıl", "neden", "ne fark ettin", "inceleyelim", "düşün", "örüntü", "ilişki", "keşf", "sence"])
    olumsuz_kelimeler = ["ezberle", "sustur", "sus", "kuralı yaz", "formülü yaz", "ceza", "görmezden", "bağır", "otur yerine"]

    empati_var = any(k in kucuk_metin for k in empati_kelimeleri)
    olumsuz_var = any(k in kucuk_metin for k in olumsuz_kelimeler)

    ses_puan = 20
    if empati_var: ses_puan += 10
    if materyal_hitabet_var: ses_puan += 10
    if sorgulama_var: ses_puan += 10
    if olumsuz_var: ses_puan -= 25
    ses_puan = max(5, min(50, ses_puan))

    toplam_puan = min(100, siralama_puani + materyal_puan + ses_puan + (10 if ses_kaydi_var else 0))

    # Nesnel ve Detaylı İyi Yönler
    iyi_yonler = []
    if ilk_adim_dogru:
        iyi_yonler.append("**Kronolojik Pedagojik Eylem Sıralaması Başarısı:** Eylem şıkkında önce duyuşsal güvenli alan kurulması ve ardından yapılandırmacı materyal adımına geçilmesi kronolojik olarak doğru seçilmiştir.")
    if materyal_konuya_uygun:
        iyi_yonler.append(f"**Materyal Uygunluğu:** Seçtiğiniz **{secilen_materyal}** aracı, işlenen `{kazanim_obj['kod']}` kazanımının bilişsel yapısına ve somutlaştırma düzeyine tam uygundur.")
    else:
        iyi_yonler.append(f"**Materyal Kullanım Girişimi:** `{secilen_materyal}` aracı seçilmiş olup derse entegre edilmeye çalışılmıştır.")
    if empati_var:
        iyi_yonler.append("**Empatik ve Kapsayıcı Hitabet Dili:** Sesli geri bildiriminizde öğrencinin kaygısını azaltacak duyuşsal destek ifadeleri yer almıştır.")
    if materyal_hitabet_var:
        iyi_yonler.append("**Materyalle Doğrudan Etkileşim:** Sesli hitabetinizde materyalin derste nasıl işletileceğine dair açık yönlendirme yapılmıştır.")

    # Nesnel Eksik Yönler, Kök Nedenler ve Çözüm Önerileri
    eksik_yonler = []
    kok_nedenler = []
    cozum_onerileri = []

    if not ilk_adim_dogru or olumsuz_var:
        eksik_yonler.append("**Kronolojik Eylem Sıralaması Hatası:** Kriz anında önce öğrencinin duyuşsal hazırbulunuşluğu sağlanmadan doğrudan kural dikte etme veya geleneksel yönetim tercih edilmiştir.")
        kok_nedenler.append("**Geleneksel Sınıf Yönetimi Refleksi:** Zaman baskısı ve geleneksel okul kültürü nedeniyle kriz anlarında otoriter tutumun otomatik olarak devreye girmesi.")
        cozum_onerileri.append("**Kronolojik Adımlama Protokolü:** Kriz anında [1] Önce empati ve güvenli alan, [2] Ardından somut materyalle yönlendirme sırasını takip edin.")

    if not materyal_konuya_uygun:
        eksik_yonler.append(f"**Materyal-Konu Uyumsuzluğu:** Seçilen **{secilen_materyal}** aracı bu kazanımın soyutlama düzeyine tam uygun değildir; alternatif olarak {', '.join(uygun_materyaller)} tercih edilmeliydi.")
        kok_nedenler.append("**Materyal Seçiminde Pedagojik Eşleşme Eksikliği:** Her somut aracın her matematiksel kazanıma uygun olmadığını göz ardı ederek genel geçer materyal seçme eğilimi.")
        cozum_onerileri.append(f"**Pedagojik Materyal Eşleme:** `{kazanim_obj['kod']}` kazanımı için somut model olarak doğrudan *{uygun_materyaller[0] if uygun_materyaller else 'uygun araç'}* kullanılmalıdır.")

    if not materyal_hitabet_var:
        eksik_yonler.append("**Materyalin Sözel Hitabete Yansıtılmaması:** Materyal seçilmesine rağmen sesli geri bildirimde bu aracın nasıl kullanılacağı ifade edilmemiştir.")
        kok_nedenler.append("Materyal seçimi ile sözlü yönergenin birbirinden bağımsız yürütülmesi.")
        cozum_onerileri.append("Hitabetinizde her zaman materyalin adına doğrudan vurgu yapın (Örn: 'Elindeki materyali incele...').")

    if not eksik_yonler:
        eksik_yonler.append("**Üst Düzey Farklılaştırma:** Kriz başarıyla yönetilmiş olup sınıf genelindeki diğer 9 öğrenci profiline yönelik derinleştirme yapılabilir.")
        kok_nedenler.append("Odak öğrenciyle ilgilenirken sınıfın diğer profillerinin anlık bilişsel takibinin bırakılması.")
        cozum_onerileri.append("Odak öğrenciyi yönlendirdikten sonra sınıfa dönüp 'Farklı bir strateji düşünen var mı?' diyerek tüm sınıfı aktif tutun.")

    rubrik_satirlari = [s.strip() for s in rubrik_metni.split("\n") if s.strip()]
    rubrik_analiz_listesi = []
    for idx, satir in enumerate(rubrik_satirlari, 1):
        oran = toplam_puan / 100.0
        durum = "Tam Uyumlu / Başarılı" if oran >= 0.8 else ("Kısmen Uyumlu / Geliştirilmeli" if oran >= 0.55 else "Yetersiz / Müdahale Gerekli")
        rubrik_analiz_listesi.append({
            "Kriter No": f"Kriter {idx}",
            "Rubrik Maddesi": satir,
            "Uyum Durumu": durum,
            "Başarı Yüzdesi": f"%{int(oran * 100)}",
        })

    return {
        "toplam_puan": toplam_puan,
        "iyi_yonler": iyi_yonler,
        "eksik_yonler": eksik_yonler,
        "kok_nedenler": kok_nedenler,
        "cozum_onerileri": cozum_onerileri,
        "rubrik_analiz_listesi": rubrik_analiz_listesi,
        "yapilandirmaci_mi": ilk_adim_dogru and not olumsuz_var and empati_var and materyal_konuya_uygun,
    }


# ==========================================
# ADIM 1: KURULUM VE RUBRİK YÜKLEME
# ==========================================
if st.session_state.adim == 1:
    st.subheader("📝 Stajyer Öğretmen 2026 Maarif Modeli Kurulum ve Rubrik Yükleme Paneli")
    col1, col2 = st.columns(2)
    with col1:
        ogretmen_adi = st.text_input("Öğretmen Adayı Adı Soyadı", value=st.session_state.get("ogretmen_adi", ""))
        okul_numarasi = st.text_input("Okul Numarası", value=st.session_state.get("okul_numarasi", ""))
        universite_adi = st.text_input("Üniversite Adı", value=st.session_state.get("universite_adi", ""))
        fakulte_bolum = st.text_input("Fakülte ve Bölüm", value=st.session_state.get("fakulte_bolum", "İlköğretim Matematik Öğretmenliği"))
        uygulama_ogretim_elemani = st.text_input("Uygulama Öğretim Elemanı", value=st.session_state.get("uygulama_ogretim_elemani", ""))
    with col2:
        st.markdown("### 📋 Değerlendirme Rubriği")
        rubrik_metni = st.text_area(
            "Rubrik Kriterleri",
            value=st.session_state.get("rubrik_metni", "1. Kriz anında empati ve güvenli alan oluşturma (30 Puan)\n2. 10 farklı öğrenci profiline kapsayıcı yaklaşım (30 Puan)\n3. TYMM süreç bileşenleri ve materyal uyumu (20 Puan)\n4. Kronolojik eylem sırası ve sorgulama başarısı (20 Puan)"),
            height=140,
        )
        st.info("ℹ️ Sınıf ortamında otomatik olarak 10 farklı genel öğrenci tipi yer alacaktır.")

    if st.button("🚀 2026 Maarif Modeli Dinamik Simülasyonu Başlat", use_container_width=True):
        if not ogretmen_adi or not okul_numarasi or not universite_adi or not uygulama_ogretim_elemani:
            st.warning("Lütfen zorunlu alanları doldurunuz.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi
            st.session_state.okul_numarasi = okul_numarasi
            st.session_state.universite_adi = universite_adi
            st.session_state.fakulte_bolum = fakulte_bolum
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
            st.session_state.rubrik_metni = rubrik_metni
            st.session_state.adim = 2
            st.rerun()

# ==========================================
# ADIM 2: 3B SINIF ORTAMI (10 ÖĞRENCİ) & SESLİ GERİ BİLDİRİM & MATERYAL SEÇİMİ
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    okul_no = st.session_state.get("okul_numarasi", "N/A")
    universite = st.session_state.get("universite_adi", "Üniversite")

    st.markdown(f"### 🏫 3B Sınıf Simülasyonu (10 Öğrenci) | Aday: {ogretmen} ({okul_no})")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        secilen_sinif = st.selectbox("1️⃣ Sınıf Düzeyi", list(tyym_master_arsiv.keys()))
    with col_s2:
        secilen_tema = st.selectbox("2️⃣ Tema", tyym_master_arsiv[secilen_sinif]["Temalar"])

    kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]
    with col_s3:
        kazanim_secenekleri = [f"{k['kod']} - {k['cikti']}" for k in kazanim_listesi]
        secilen_kazanim_str = st.selectbox("3️⃣ Kazanım Seçin", kazanim_secenekleri)

    secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']} - {k['cikti']}" == secilen_kazanim_str)
    
    with col_s4:
        secilen_materyal = st.selectbox(
            "4️⃣ Ders Materyali Seçin",
            materyal_havuzu,
            index=0
        )

    secilen_surec = st.selectbox("5️⃣ İşlenecek Süreç Bileşeni (TYMM 2026):", secilen_kazanim_obj["surec"])

    aktif_kriz = secilen_kazanim_obj["kriz"]
    odak_ogrenci_id = secilen_kazanim_obj.get("odak", "disleksi")

    son_oturum = st.session_state.simulasyon_gecmisi[-1] if len(st.session_state.simulasyon_gecmisi) > 0 else None
    ogretmen_son_soz = son_oturum["sesli_komut"] if son_oturum else ""
    analiz_sonucu = son_oturum["analiz"] if son_oturum else None

    # 3B Sahne Çağrısı (10 Öğrenci ve Dinamik Tepkiler)
    render_3d_classroom_10_students_dynamic_v2(
        ogretmen_adi=ogretmen,
        sinif_duzeyi=secilen_sinif,
        tema=secilen_tema,
        kazanim_kodu=secilen_kazanim_obj["kod"],
        secilen_materyal=secilen_materyal,
        odak_ogrenci_id=odak_ogrenci_id,
        ogretmen_sozu=ogretmen_son_soz,
        sesli_analiz_sonucu=analiz_sonucu,
    )

    col_sol, col_sag = st.columns([1.1, 0.9], gap="large")
    with col_sol:
        st.markdown("#### ⚡ Sınıf İçi Kriz Durumu")
        st.warning(f"🔔 {aktif_kriz}")

        st.markdown("### 🎙️ Sesli Geri Bildirim & Mikrofon Konsolu")
        st.info("💡 **Not:** Mikrofon donanımı çalışmıyorsa tabletinizin klavyesindeki mikrofon (dikte) tuşuyla konuşarak metin yazdırabilir ya da klavyenizle doğrudan yazabilirsiniz.")
        
        ses_verisi = None
        if hasattr(st, "audio_input"):
            ses_verisi = st.audio_input("🎤 Ses Kaydınızı Yapın:")
            if ses_verisi: st.success("✅ Ses kaydedildi.")

        sesli_geri_bildirim_metni = st.text_area(
            "🗣️ Öğrencilere Söylediğiniz Sesli Geri Bildirim İfadesi:",
            value="",
            height=95,
            placeholder="",
        )

        st.markdown("### 👩‍🏫 Sınıf İçi Pedagojik Eylem Kararınız (Kronolojik Sıralama)")
        ogretmen_karari = st.radio(
            "Aksiyonunuzu seçin (Önce yapılması gerekenler ile sonra yapılması gerekenlerin sırasına dikkat edin):",
            [
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve sınıf disiplinini sert kurallarla korumak.",
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak, akran destekli empati kurdurmak ve somut materyalle desteklemek.",
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu kural ve formüllerle anlatmaya devam etmek.",
                "D) Sınıfın seviyesinin yetersiz olduğunu söyleyip öğrencilere ek ödev cezası vermek.",
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak somut ve dijital temsillerle kavramsal değişimi tetiklemek.",
            ],
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            islem_butonu = st.button("📥 Geri Bildirimi Uygula & Sınıf Tepkisini Gör", use_container_width=True)
        with col_b2:
            duzeltme_butonu = st.button("🔄 Hataları Kavradım, Derse Geri Dönüp Düzeltme Yap", use_container_width=True)

        if duzeltme_butonu:
            st.info("🔄 Ders akışına geri dönüldü. Yukarıdaki sesli geri bildiriminizi ve materyal seçiminizi güncelleyerek yeniden değerlendirme alabilirsiniz.")

        if islem_butonu:
            if not sesli_geri_bildirim_metni.strip() and not ses_verisi:
                st.error("⚠️ Lütfen ses kaydı yapın veya sesli geri bildirim metninizi girin.")
            else:
                islenen_metin = sesli_geri_bildirim_metni.strip() if sesli_geri_bildirim_metni.strip() else "Sesli komut verildi."
                analiz = detayli_pedagojik_analiz_uret_gelismis_v3(
                    sesli_metin=islenen_metin,
                    secilen_karar_metni=ogretmen_karari,
                    secilen_materyal=secilen_materyal,
                    kazanim_obj=secilen_kazanim_obj,
                    surec=secilen_surec,
                    rubrik_metni=st.session_state.get("rubrik_metni", ""),
                    ses_kaydi_var=(ses_verisi is not None),
                )
                st.session_state.simulasyon_gecmisi.append({
                    "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "sinif": secilen_sinif,
                    "tema": secilen_tema,
                    "kod": secilen_kazanim_obj["kod"],
                    "cikti": secilen_kazanim_obj["cikti"],
                    "surec": secilen_surec,
                    "materyal": secilen_materyal,
                    "kriz": aktif_kriz,
                    "karar": ogretmen_karari,
                    "sesli_komut": islenen_metin,
                    "puan": analiz["toplam_puan"],
                    "analiz": analiz,
                })
                st.rerun()

    with col_sag:
        st.markdown("#### 👥 10 Farklı Öğrenci Tipinin Detaylı Karakteristikleri")
        for ogr in genel_ogrenci_tipleri_detayli:
            with st.container(border=True):
                st.markdown(f"**{ogr['yuz']} {ogr['ad']} ({ogr['tip']})**")
                st.caption(f"Psikolojik/Bilişsel Arka Plan: {ogr['karakteristik']}")
                if ogr["id"] == odak_ogrenci_id:
                    st.warning("⚡ Bu oturumun kriz odaklı profili.")

        if len(st.session_state.simulasyon_gecmisi) > 0:
            son = st.session_state.simulasyon_gecmisi[-1]
            st.success(f"✅ Güncel Oturum Puanı: {son['puan']}/100")
            if st.button("📋 Çok Detaylı Nesnel Raporlara Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()

# ==========================================
# ADIM 3: ÇOK DETAYLI, NESNEL RAPORLAR, PROGRAM UYUMU VE KÜMÜLATİF İLERLEME
# ==========================================
elif st.session_state.adim == 3:
    st.subheader("📊 TYMM 2026 & RUBRİK UYUMLU ÇOK DETAYLI NESNEL RAPORLAMA VE YIL SONU İLERLEME SİSTEMİ")
    toplam_islem = len(st.session_state.simulasyon_gecmisi)
    ortalama_puan = int(sum(k["puan"] for k in st.session_state.simulasyon_gecmisi) / toplam_islem) if toplam_islem > 0 else 0

    tab_aday, tab_rubrik, tab_program, tab_portfolyo, tab_anket = st.tabs([
        "👩‍🏫 1. Aday Detaylı Pedagojik Analiz",
        "📋 2. Öğretim Elemanı Rubrik Uygunluk Testi",
        "📐 3. Öğretim Programı (TYMM 2026) Uygunluk Analizi",
        "📈 4. Yıl Sonu Kümülatif İlerleme & Portfolyo Geri Dönütü",
        "⭐ 5. Aday Simülasyonu Değerlendirme Formu",
    ])

    with tab_aday:
        if toplam_islem == 0:
            st.warning("Henüz oturum yok.")
        else:
            for idx, oturum in enumerate(st.session_state.simulasyon_gecmisi, 1):
                analiz = oturum["analiz"]
                with st.container(border=True):
                    st.markdown(f"#### 📌 Oturum #{idx} (Güncel): {oturum['sinif']} | {oturum['tema']} (`{oturum['kod']}`) — **Puan: {oturum['puan']}/100**")
                    st.markdown(f"- **Kazanım:** {oturum['cikti']}\n- **Süreç Bileşeni:** {oturum['surec']}\n- **Seçilen Materyal:** {oturum['materyal']}\n- **Sesli Geri Bildirim:** *\"{oturum['sesli_komut']}\"*\n- **Eylem Kararı:** {oturum['karar']}")
                    st.divider()
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        st.markdown("##### ✅ Nesnel İyi ve Güçlü Yönler")
                        for m in analiz["iyi_yonler"]: st.success(m)
                        st.markdown("##### ⚠️ Nesnel Eksik ve Geliştirilmesi Gereken Yönler")
                        for m in analiz["eksik_yonler"]: st.warning(m)
                    with col_a2:
                        st.markdown("##### 🔍 Eksikliklerin Kök Nedenleri (Neden Kaynaklanıyor?)")
                        for m in analiz["kok_nedenler"]: st.error(m)
                        st.markdown("##### 🛠️ Çözüm Yolları ve Somut Öneriler (Ne Yapılırsa Çözülür?)")
                        for m in analiz["cozum_onerileri"]: st.info(m)

    with tab_rubrik:
        st.markdown("### 📋 Uygulama Öğretim Elemanı Rubrik Uygunluk Testi")
        st.info("Bu başlık altında öğretmen adayının sınıf içi davranışları ve hitabeti, danışman hocanın yüklediği rubrik maddelerine göre nesnel olarak test edilmektedir.")
        if toplam_islem > 0:
            son_analiz = st.session_state.simulasyon_gecmisi[-1]["analiz"]
            st.dataframe(pd.DataFrame(son_analiz["rubrik_analiz_listesi"]), use_container_width=True, hide_index=True)

    with tab_program:
        st.markdown("### 📐 Öğretim Programı (2026 Türkiye Yüzyılı Maarif Modeli) Uygunluk Analizi")
        st.info("Bu başlık altında, işlenen dersin o an yürürlükte olan millî öğretim programının (TYMM 2026) temel felsefesine, becerilerine ve süreç bileşenlerine uygunluğu ayrıntılı olarak ele alınmaktadır.")
        if toplam_islem > 0:
            son_oturum = st.session_state.simulasyon_gecmisi[-1]
            with st.container(border=True):
                st.markdown(f"**İncelenen Sınıf & Kazanım:** {son_oturum['sinif']} - `{son_oturum['kod']}` ({son_oturum['cikti']})")
                st.markdown(f"**Seçilen Süreç Bileşeni:** {son_oturum['surec']}")
                st.markdown(f"**Tercih Edilen Materyal:** {son_oturum['materyal']}")
                st.markdown(
                    "#### 🔍 Program Uygunluk Sonucu:\n"
                    "1. **Beceriler ve Yetkinlikler Uyumu:** Adayın seçtiği yapılandırmacı yaklaşım ve materyal, TYMM 2026 matematik dersi öğretim programında öngörülen 'matematiksel muhakeme' ve 'problem çözme' bileşenlerini desteklemektedir.\n"
                    "2. **Somutlaştırma ve Bağlamsal Tasarım:** Dersin başında kullanılan 'Gerçek Yaşam Kancası' (hook) programın günlük hayatla ilişkilendirme ilkesiyle tam uyumludur.\n"
                    "3. **Geliştirilmesi Gereken Program Alanı:** Öğrencinin bilişsel zorlanma anında formül vermek yerine süreç bileşenindeki alt basamakları sırasıyla sorularak keşfettirmesi programın yapılandırmacı ruhunu pekiştirecektir."
                )

    with tab_portfolyo:
        st.markdown("### 📈 Yıl Sonu Kümülatif İlerleme ve Portfolyo Geri Dönüt Sistemi")
        st.info("Bu modül, her öğretmen adayının yıl boyunca gerçekleştirdiği tüm oturumları birleştirerek genel gelişim eğrisini gözlemler ve kümülatif geri dönüt sağlar.")
        if toplam_islem > 0:
            kumulatif_df = pd.DataFrame([
                {"Oturum No": i+1, "Sınıf": o["sinif"], "Kazanım": o["kod"], "Puan": o["puan"]}
                for i, o in enumerate(st.session_state.simulasyon_gecmisi)
            ])
            st.dataframe(kumulatif_df, use_container_width=True, hide_index=True)
            st.line_chart(kumulatif_df, x="Oturum No", y="Puan")
            st.success(
                f"🌟 **Kümülatif Geri Dönüt:** Adayımızın yıl içindeki genel ortalama pedagojik yeterlilik puanı **{ortalama_puan}/100** olarak hesaplanmıştır. "
                "Aday özellikle duyuşsal empati ve materyal seçiminde istikrarlı bir ilerleme kaydetmiş olup, kriz anlarında kronolojik sıralamayı (önce güvenli alan) "
                "uygulama refleksini pekiştirmelidir."
            )

    with tab_anket:
        st.markdown("### ⭐ Simülasyon Uygulamasını Değerlendirme Formu")
        with st.container(border=True):
            p1 = st.slider("1. 3B Sınıf Ortamı ve 10 Öğrenci Tipinin Gerçekçiliği (1-5)", 1, 5, 5)
            p2 = st.slider("2. TYMM 2026 Tam Uyum ve Materyal Seçim Modülü (1-5)", 1, 5, 5)
            p3 = st.slider("3. Sesli Geri Bildirim ve Dinamik Tepki Mekanizması (1-5)", 1, 5, 5)
            p4 = st.slider("4. Raporların Nesnelliği ve Kök Neden Kalitesi (1-5)", 1, 5, 5)
            begeni = st.text_area("✅ Beğenilen Yönler:")
            oneri = st.text_area("💡 Önerileriniz:")
            if st.button("📨 Değerlendirmeyi Kaydet", use_container_width=True):
                st.session_state.uygulama_degerlendirmeleri.append({"Tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), "Memnuniyet": round((p1+p2+p3+p4)/4.0, 2), "Beğenilenler": begeni, "Öneriler": oneri})
                st.success("🎉 Geri bildiriminiz kaydedildi!")

    st.divider()
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 3B Sınıfa Dön ve Yeni Senaryo Uygula", use_container_width=True):
            st.session_state.adim = 2
            st.rerun()
    with col_b2:
        tum_rapor_json = json.dumps({
            "aday": st.session_state.get("ogretmen_adi"),
            "okul_no": st.session_state.get("okul_numarasi"),
            "ortalama_puan": ortalama_puan,
            "oturumlar": st.session_state.simulasyon_gecmisi,
            "degerlendirmeler": st.session_state.uygulama_degerlendirmeleri
        }, ensure_ascii=False, indent=2)
        st.download_button("📥 Yıl Sonu Kümülatif Portfolyoyu İndir (JSON)", data=tum_rapor_json, file_name=f"TYMM2026_Portfolyo_{st.session_state.get('okul_numarasi', 'Aday')}.json", mime="application/json", use_container_width=True)
    with col_b3:
        if st.button("🔄 Simülasyonu Baştan Başlat", use_container_width=True):
            st.session_state.simulasyon_gecmisi = []
            st.session_state.adim = 1
            st.rerun()
    """
    components.html(html_code, height=580, scrolling=True)
