import datetime
import json
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="TYMM 2026 3B Sesli Sınıf & Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# ==========================================
# OTURUM DURUMU (SESSION STATE) YÖNETİMİ
# ==========================================
if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "uygulama_degerlendirmeleri" not in st.session_state:
    st.session_state.uygulama_degerlendirmeleri = []
if "hoca_geri_donutleri" not in st.session_state:
    st.session_state.hoca_geri_donutleri = []
if "adim" not in st.session_state:
    st.session_state.adim = 1  # 1: Kurulum, 2: 3B Sınıf, 3: Detaylı Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) TAM MÜFREDAT ARŞİVİ (5, 6, 7 VE 8. SINIFLAR)
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "MAT.5.1. Sayılar ve Nicelikler",
            "MAT.5.2. İşlemlerle Cebirsel Düşünme",
            "MAT.5.3. Geometrik Şekiller",
            "MAT.5.4. Geometrik Nicelikler",
            "MAT.5.5. İstatistiksel Araştırma Süreci",
            "MAT.5.6. Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "MAT.5.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
                    "surec": [
                        "a) Günlük hayattaki bağlamlardan yola çıkarak çok basamaklı sayılar hakkında bilgi toplar.",
                        "b) Sayıların bölümleri ile okunuşları arasındaki ortak özellikleri belirler.",
                        "c) Sayıların bölümleri ile okunuşları arasındaki farklılıkları belirler.",
                        "ç) Örüntüler üzerinden basamak sayısı çok olan sayıların okunuş ve yazılışları hakkında önermelerde bulunur.",
                    ],
                    "materyal": "Basamak Tablosu ve Renkli Abaküs",
                    "hook": "Millî Kütüphane'deki 405.020 adet tarihi el yazması kitabın arşiv kodlama sistemi.",
                    "kriz": "Kerem tahtadaki 405.020 sayısını okurken basamakları karıştırır, bazı öğrenciler güler.",
                    "kriz_odak_ogrenci": "Kerem",
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) İşlem gerektiren günlük yaşam durumlarında nicelikleri inceler.",
                        "b) Zihinden işlem ve tahmin stratejileri geliştirir.",
                        "c) Geliştirdiği stratejilerin doğruluğunu somut modellerle test eder.",
                    ],
                    "materyal": "Onluk Taban Blokları ve Sayı Doğrusu",
                    "hook": "Okul kermesinde toplanan bağışların hedef bütçe ile karşılaştırılması.",
                    "kriz": "Can zihinden işlem stratejisini dinlemeyip 'Ben zaten sonucu buldum, neden uzatıyoruz?' diyerek araya girer.",
                    "kriz_odak_ogrenci": "Can",
                },
                {
                    "kod": "MAT.5.1.3",
                    "cikti": "Kesirlerin farklı gösterimlerini (bileşik, tam sayılı, ondalık ve yüzde) ilişkilendirebilme",
                    "surec": [
                        "a) Kesir, ondalık ve yüzde gösterimlerini somut modeller üzerinde inceler.",
                        "b) Farklı gösterimler arasındaki dönüşümleri açıklar.",
                        "c) Günlük yaşam bağlamlarında uygun gösterimi seçerek yorumlar.",
                    ],
                    "materyal": "Kesir Takımları ve Yüzlük Kartlar",
                    "hook": "Market indirim afişlerindeki yüzde sembolleri ile kasa fişindeki ondalık fiyatların karşılaştırılması.",
                    "kriz": "Elif payda büyüdükçe birim kesir değerinin neden küçüldüğünü anlayamadığını söyleyerek kaygılanır.",
                    "kriz_odak_ogrenci": "Elif",
                },
            ],
            "MAT.5.2. İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.5.2.1",
                    "cikti": "Eşitliğin korunumu ve işlem özelliklerini (değişme, birleşme, dağılma) muhakeme edebilme",
                    "surec": [
                        "a) Eşit kollu terazi modelleri üzerinde eşitlik durumlarını inceler.",
                        "b) İşlem özelliklerini kullanarak eşitliklerin korunduğunu gösterir.",
                        "c) İşlem önceliği kurallarını günlük yaşam senaryolarında uygular.",
                    ],
                    "materyal": "Eşit Kollu Terazi Simülasyonu",
                    "hook": "Laboratuvardaki eşit kollu terazide farklı kütleleri dengeleme deneyi.",
                    "kriz": "Can eşittir işaretinin sadece 'sonuç' demek olmadığını, sınıftakilerin bunu yanlış bildiğini sertçe söyler.",
                    "kriz_odak_ogrenci": "Can",
                },
                {
                    "kod": "MAT.5.2.2",
                    "cikti": "Sayı ve şekil örüntülerinin kuralını bularak algoritmik düşünme süreçlerini yürütebilme",
                    "surec": [
                        "a) Tekrarlayan ve genişleyen örüntülerdeki adımlar arası değişimi belirler.",
                        "b) Örüntüyü devam ettirecek genel adımı sözel olarak ifade eder.",
                        "c) Temel algoritmik akış şeması üzerinde örüntü adımlarını test eder.",
                    ],
                    "materyal": "Örüntü Blokları ve Akış Şeması Kartları",
                    "hook": "Geleneksel Türk çini motiflerindeki geometrik dizilimlerin adımlarını modelleme.",
                    "kriz": "Arda şekil örüntüsündeki renklerin sırası değiştiğinde duyusal huzursuzluk yaşayıp kulaklarını kapatır.",
                    "kriz_odak_ogrenci": "Arda",
                },
            ],
            "MAT.5.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.5.3.1",
                    "cikti": "Temel geometrik çizimler için matematiksel araç ve teknolojileri (cetvel, gönye, açıölçer, dinamik yazılım) kullanabilme",
                    "surec": [
                        "a) Nokta, doğru, doğru parçası ve ışın kavramlarını inşa araçlarıyla inceler.",
                        "b) Açıları açıölçer ve dinamik geometri yazılımıyla ölçerek sınıflandırır.",
                        "c) Çokgenleri ve çemberi temel elemanlarıyla inşa eder.",
                    ],
                    "materyal": "Açıölçer, Pergel ve GeoGebra Tahtası",
                    "hook": "Mimari kroki çizimlerinde açıölçer ve pergel kullanarak simetrik bahçe tasarımı yapma.",
                    "kriz": "Kerem açıölçerin iç ve dış kadranındaki dereceleri ters okur ve çizimini silip defterini kapatır.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.5.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.4.1",
                    "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkiyi yapılandırabilme",
                    "surec": [
                        "a) Birim kareler kullanarak dikdörtgenin alanını ve çevresini modeller.",
                        "b) Aynı çevre uzunluğuna sahip farklı alanlardaki dikdörtgenleri karşılaştırır.",
                        "c) Aynı alana sahip farklı çevre uzunluğundaki dikdörtgenleri muhakeme eder.",
                    ],
                    "materyal": "Geometri Tahtası (Geoboard) ve Birim Kareler",
                    "hook": "Okul bahçesine sabit uzunluktaki çitle en geniş alana sahip hobi bahçesi kurma.",
                    "kriz": "Elif alan ile çevre hesaplamalarını birbirine karıştırıp 'Yapamıyorum' diyerek içe kapanır.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
            "MAT.5.5. İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.5.1",
                    "cikti": "Kategorik verilerle istatistiksel araştırma sürecini yürütebilme ve görselleştirebilme",
                    "surec": [
                        "a) Kategorik veri toplamayı gerektiren araştırma sorusu oluşturur.",
                        "b) Verileri toplar, sıklık tablosu ve sütun grafiği ile görselleştirir.",
                        "c) Elde edilen bulguları araştırma sorusu bağlamında yorumlar.",
                    ],
                    "materyal": "Veri Toplama Formu ve Dijital Grafik Aracı",
                    "hook": "Sınıf kütüphanesine alınacak kitap türlerini belirlemek için veri toplama ve grafik oluşturma.",
                    "kriz": "Can anket sorularının yanlı hazırlandığını iddia ederek grup arkadaşlarıyla tartışmaya girer.",
                    "kriz_odak_ogrenci": "Can",
                }
            ],
            "MAT.5.6. Veriden Olasılığa": [
                {
                    "kod": "MAT.5.6.1",
                    "cikti": "Olayların olasılığını olasılık spektrumu (imkânsızdan kesine) üzerinde öznel olarak yorumlayabilme",
                    "surec": [
                        "a) Günlük yaşam olaylarını gerçekleşme ihtimallerine göre inceler.",
                        "b) Olayları imkânsız, daha az olası, eşit olası, daha çok olası ve kesin olarak sınıflandırır.",
                        "c) Olasılık spektrumu üzerindeki yerleşimleri gerekçelendirir.",
                    ],
                    "materyal": "Olasılık Spektrumu Şeridi ve Renkli Çark",
                    "hook": "Meteoroloji verilerine göre hafta sonu yapılacak doğa yürüyüşünde yağmur yağma ihtimalini tartışma.",
                    "kriz": "Elif 'Ya tahminimiz yanlış çıkarsa ve puan kırılırsa?' diyerek spektrum üzerinde işaretleme yapmaktan çekinir.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": [
            "MAT.6.1. Sayılar ve Nicelikler",
            "MAT.6.2. İşlemlerle Cebirsel Düşünme ve Değişimler",
            "MAT.6.3. Geometrik Şekiller",
            "MAT.6.4. Geometrik Nicelikler",
            "MAT.6.5. İstatistiksel Araştırma Süreci",
            "MAT.6.6. Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "MAT.6.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1",
                    "cikti": "Doğal sayıların çarpan, kat ve asal sayı özelliklerine yönelik muhakeme yapabilme",
                    "surec": [
                        "a) Doğal sayıların çarpan ve katlarına yönelik varsayımlarda bulunur.",
                        "b) Bölünebilme kurallarını ve asal çarpanları örüntüler üzerinden geneller.",
                        "c) Ortak kat ve ortak bölen kavramlarını gerçek yaşam durumlarında doğrular.",
                    ],
                    "materyal": "Yüzlük Tablo (Eratosthenes Kalburu) ve Çarpan Ağacı",
                    "hook": "Farklı periyotlarla sefer yapan iki vapurun iskelede aynı anda buluşma saatlerini planlama.",
                    "kriz": "Can 'Bu kuralları ezberlemek yerine modüler aritmetik kullansak olmaz mı?' diyerek sınıfın kafasını karıştırır.",
                    "kriz_odak_ogrenci": "Can",
                },
                {
                    "kod": "MAT.6.1.2",
                    "cikti": "Kesirlerle ve ondalık gösterimlerle işlemleri içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Kesirlerle çarpma ve bölme işlemlerini alan ve sayı doğrusu modelleriyle anlamlandırır.",
                        "b) Ondalık gösterimlerle dört işlem stratejileri geliştirir.",
                        "c) Uzunluk ölçme birimleri arasındaki dönüşümleri ondalık gösterimlerle ilişkilendirir.",
                    ],
                    "materyal": "Şeffaf Kesir Asetatları ve Sayı Doğrusu",
                    "hook": "Tasarım atölyesinde kumaş parçalarını eşit kesirli ölçülerde bölüştürme.",
                    "kriz": "Elif iki basit kesir çarpıldığında sonucun neden çarpanlardan daha küçük çıktığını anlamayıp panikler.",
                    "kriz_odak_ogrenci": "Elif",
                },
            ],
            "MAT.6.2. İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.6.2.1",
                    "cikti": "Bilinmeyen nicelikleri değişkenlerle temsil edebilme ve cebirsel ifadeleri anlamlandırabilme",
                    "surec": [
                        "a) Sözel olarak verilen durumları değişken kullanarak cebirsel ifadeye dönüştürür.",
                        "b) Cebirsel ifadelerin farklı doğal sayı değerleri için sonuçlarını hesaplar.",
                        "c) Aritmetik dizilerin kuralını harfli ifadelerle ve algoritmalarla modeller.",
                    ],
                    "materyal": "Cebir Karoları ve Değişken Kutuları",
                    "hook": "Kumbaraya her hafta sabit miktarda eklenen paranın n. haftadaki toplam tutarını cebirsel modelleme.",
                    "kriz": "Kerem matematikte sayıların arasına harflerin (x, y) girmesine tepki gösterip sembolleri birbirine karıştırır.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.6.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1",
                    "cikti": "Paralel iki doğrunun bir kesenle yaptığı açıları, üçgen ve dörtgenlerin özelliklerini keşfedebilme",
                    "surec": [
                        "a) Paralel doğrular ve kesen arasındaki yöndeş, iç ters ve dış ters açıları dinamik yazılımla inceler.",
                        "b) Üçgen ve dörtgenlerin iç açıları toplamına yönelik varsayımları test eder.",
                        "c) Çokgenlerin köşegen, kenar ve açı özelliklerini sınıflandırır.",
                    ],
                    "materyal": "GeoGebra Dinamik Açı Simülasyonu",
                    "hook": "Demiryolu makas kesişimlerindeki ve köprü kirişlerindeki açıların dengesini inceleme.",
                    "kriz": "Arda dinamik geometri ekranındaki doğrular hızlı hareket ettirildiğinde duyusal rahatsızlık yaşar.",
                    "kriz_odak_ogrenci": "Arda",
                }
            ],
            "MAT.6.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.1",
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarını dikdörtgenin alanından yararlanarak oluşturabilme",
                    "surec": [
                        "a) Paralelkenarı kes-yapıştır stratejisiyle dikdörtgene dönüştürerek alan bağıntısını bulur.",
                        "b) Üçgenin alanını paralelkenar ve dikdörtgen alanı üzerinden geneller.",
                        "c) Alan ölçme birimleri arasında dönüşüm yaparak problemleri çözer.",
                    ],
                    "materyal": "Noktalı İzometrik Kağıt ve Tangram Parçaları",
                    "hook": "Üçgen ve paralelkenar şeklindeki tarım parsellerinin sulama alanlarını hesaplama.",
                    "kriz": "Kerem geniş açılı üçgende yüksekliğin şeklin dışına çizilmesini anlamlandırırken zorlanır.",
                    "kriz_odak_ogrenci": "Kerem",
                },
                {
                    "kod": "MAT.6.4.2",
                    "cikti": "Çemberin çevre uzunluğu ile çapı arasındaki oranı (pi) keşfederek yay uzunluğunu hesaplayabilme",
                    "surec": [
                        "a) Farklı büyüklükteki dairesel nesnelerin çevresini çapına bölerek sabit oranı inceler.",
                        "b) Çemberin uzunluğu ve çember parçasının (yay) uzunluğu bağıntısını kurar.",
                    ],
                    "materyal": "Dairesel Silindirler, İp ve Mezura",
                    "hook": "Bisiklet tekerleğinin bir tam turda aldığı mesafeyi tekerlek çapı üzerinden hesaplama.",
                    "kriz": "Can pi sayısının virgülden sonraki basamaklarının hiç bitmemesini sorgulayıp arkadaşlarının sözünü keser.",
                    "kriz_odak_ogrenci": "Can",
                },
            ],
            "MAT.6.5. İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": "Nicel kesikli verilerle kök-yaprak gösterimi oluşturabilme ve merkezi eğilim ölçülerini yorumlayabilme",
                    "surec": [
                        "a) Nicel kesikli veri toplar ve kök-yaprak gösterimi ile organize eder.",
                        "b) Aritmetik ortalama, ortanca (medyan) ve tepe değer (mod) ölçülerini hesaplar.",
                        "c) Uç değerlerin aritmetik ortalama üzerindeki etkisini muhakeme eder.",
                    ],
                    "materyal": "Kök-Yaprak Tablosu ve Veri Analiz Kartları",
                    "hook": "Okul basketbol takımındaki oyuncuların maç başına attıkları sayıların istatistiksel analizi.",
                    "kriz": "Elif uç değer yüzünden ortalamanın değişmesini anlamayıp yanlış işlem yaptığını düşünerek panikler.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
            "MAT.6.6. Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1",
                    "cikti": "Bir olayın deneysel olasılığını deneme sayısına bağlı göreli sıklık üzerinden tahmin edebilme",
                    "surec": [
                        "a) Tekrarlı olasılık deneyleri tasarlar ve sonuçların çetelesini tutar.",
                        "b) Göreli sıklığı hesaplayarak deneysel olasılık değerini belirler.",
                        "c) Deneme sayısı arttıkça göreli sıklığın nasıl değiştiğini yorumlar.",
                    ],
                    "materyal": "Olasılık Deney Simülatörü ve Çetele Tablosu",
                    "hook": "Dijital simülasyonla 10, 100 ve 1000 kez atılan hilesiz zarın üst yüzüne gelen sayıların analizi.",
                    "kriz": "Arda zar atma seslerinden ve sınıfın gürültüsünden rahatsız olup kulaklarını kapatarak sallanmaya başlar.",
                    "kriz_odak_ogrenci": "Arda",
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "MAT.7.1. Sayılar ve Nicelikler",
            "MAT.7.2. İşlemlerle Cebirsel Düşünme ve Değişimler",
            "MAT.7.3. Dönüşüm",
            "MAT.7.4. Geometrik Nicelikler",
            "MAT.7.5. Geometrik Şekiller",
            "MAT.7.6. İstatistiksel Araştırma Süreci",
            "MAT.7.7. Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "MAT.7.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.1",
                    "cikti": "Tam sayılar ve rasyonel sayılarla işlemler içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Tam sayılardan rasyonel sayılara geçişi sayı doğrusu ve pullarla modeller.",
                        "b) Rasyonel sayılarla dört işlem özelliklerini ve stratejilerini uygular.",
                        "c) Çok adımlı rasyonel sayı problemlerini çözerek sonuçların anlamlılığını değerlendirir.",
                    ],
                    "materyal": "Tam Sayı Pulları ve Rasyonel Sayı Doğrusu",
                    "hook": "Hava sıcaklığı değişimleri, deniz altı dalış derinlikleri ve finansal bütçe hesaplamaları.",
                    "kriz": "Kerem negatif rasyonel sayılarda eksi işaretinin pay, payda veya kesir çizgisi önünde olmasını karıştırır.",
                    "kriz_odak_ogrenci": "Kerem",
                },
                {
                    "kod": "MAT.7.1.2",
                    "cikti": "Oran ve orantı kavramlarını yapılandırarak doğru ve ters orantı problemlerini muhakeme edebilme",
                    "surec": [
                        "a) Oran Tahtası ve somut materyaller üzerinde çokluklar arası çarpımsal ilişkiyi inceler.",
                        "b) Doğru ve ters orantılı nicelikler arasındaki değişim sabiti örüntüsünü belirler.",
                        "c) Gerçek yaşam durumlarındaki orantı problemlerini farklı stratejilerle çözer.",
                    ],
                    "materyal": "Oran Tahtası ve Renkli Boncuklar",
                    "hook": "Görsel sanatlar atölyesinde renk karışım oranları ve ölçekli maket tasarımı.",
                    "kriz": "Elif Oran Tahtası üzerindeki boncuk sayısını artırırken çarpımsal ilişki yerine toplamsal ilişki kurar ve hata yapmaktan korkar.",
                    "kriz_odak_ogrenci": "Elif",
                },
            ],
            "MAT.7.2. İşlemlerle Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.7.2.1",
                    "cikti": "Cebirsel ifadelerle işlemler yapabilme, birinci dereceden bir bilinmeyenli denklem ve eşitsizlikleri çözebilme",
                    "surec": [
                        "a) Cebirsel ifadelerle toplama, çıkarma ve çarpma işlemlerini cebir karolarıyla modeller.",
                        "b) Eşitliğin korunumu ilkesiyle birinci dereceden denklemleri çözer.",
                        "c) Günlük yaşam durumlarını eşitsizliklerle ifade ederek sayı doğrusunda gösterir.",
                    ],
                    "materyal": "Cebir Karoları ve Denge Terazisi",
                    "hook": "Asansör taşıma kapasitesi sınırları ve kargo ağırlık ücretlendirme algoritmaları.",
                    "kriz": "Elif eşitsizliklerde negatif sayıyla çarpma yapıldığında yönün neden değiştiğini karıştırıp stres yaşar.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
            "MAT.7.3. Dönüşüm": [
                {
                    "kod": "MAT.7.3.1",
                    "cikti": "Düzlemde şekillerin doğruya göre yansıma dönüşümünü ve simetri inşalarını gerçekleştirebilme",
                    "surec": [
                        "a) Geometrik şekillerin simetri doğrularına göre yansıma görüntülerini inceler.",
                        "b) Yansıma dönüşümünde şekil ile görüntüsü arasındaki eşlik özelliklerini belirler.",
                        "c) Dijital matematik araçlarıyla yansıma tasarımları oluşturur.",
                    ],
                    "materyal": "Simetri Aynası ve Dijital Noktalı Kağıt",
                    "hook": "Mimari cephe tasarımlarında ve kilim desenlerinde ayna simetrisi analizi.",
                    "kriz": "Kerem eğik simetri doğrusuna göre yansıma alırken köşe noktalarının yerini ters çizer ve moral bozukluğu yaşar.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.7.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": "Özel dörtgenlerin, dairenin alanını ve dik prizmaların yüzey alanı ile hacmini hesaplayabilme",
                    "surec": [
                        "a) Eşkenar dörtgen ve yamuğun alan bağıntılarını bilinen şekillerden türetir.",
                        "b) Dairenin ve daire diliminin alanını merkez açı ile ilişkilendirir.",
                        "c) Birim küpler ve GeoGebra simülasyonlarıyla dik prizmaların hacim ve yüzey alanını modeller.",
                    ],
                    "materyal": "Somut Birim Küpler ve 3B GeoGebra Prizma Modeli",
                    "hook": "Çikolata fabrikası için birim küplerle hacmi hesaplanmış prizmatik ambalaj tasarımı.",
                    "kriz": "Arda birim küplerin masaya düşüp çıkardığı sesten rahatsız olur, Elif ise yüzey alanı ile hacmi karıştırır.",
                    "kriz_odak_ogrenci": "Arda",
                }
            ],
            "MAT.7.5. Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Üçgende kenarortay, açıortay ve yükseklik elemanlarını pergel-cetvel veya dinamik yazılımla inşa edebilme",
                    "surec": [
                        "a) Kağıt katlama ve pergel-cetvel yardımıyla açıortay ve kenarortayı inşa eder.",
                        "b) Üçgenin yardımcı elemanlarının kesişim noktalarını (ağırlık merkezi vb.) keşfeder.",
                    ],
                    "materyal": "Origami Kağıtları, Pergel-Cetvel ve GeoGebra",
                    "hook": "Üçgen şeklindeki bir tepsinin tam dengede duracağı ağırlık merkezini bulma.",
                    "kriz": "Arda pergelin sivri ucunu kullanmaktan çekinerek grup çalışmasına katılmak istemez.",
                    "kriz_odak_ogrenci": "Arda",
                }
            ],
            "MAT.7.6. İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.7.6.1",
                    "cikti": "Nicel sürekli verileri çizgi grafiği ve daire grafiği ile temsil ederek yayılım ölçülerini yorumlayabilme",
                    "surec": [
                        "a) Zamana bağlı değişen sürekli verileri çizgi grafiği ile görselleştirir.",
                        "b) Parça-bütün ilişkisini daire grafiğinde merkez açılarla modeller.",
                        "c) Veri grubunun açıklığını ve çeyrekler açıklığını hesaplayarak yayılımı yorumlar.",
                    ],
                    "materyal": "Daire Grafiği Açı Diski ve Veri Tablosu",
                    "hook": "Bir haftalık hava sıcaklığı değişimi ve enerji tüketim oranlarının grafiksel analizi.",
                    "kriz": "Kerem daire grafiğinde yüzde 25'i 360 dereceyle oranlamak yerine doğrudan 25 derece olarak çizer.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.7.7. Veriden Olasılığa": [
                {
                    "kod": "MAT.7.7.1",
                    "cikti": "Eş olasılıklı olayların teorik olasılığını, tümleyen ile ayrık ve ayrık olmayan olayları muhakeme edebilme",
                    "surec": [
                        "a) Bir olayın teorik olasılığını istenen durumların tüm durumlara oranı olarak hesaplar.",
                        "b) Bir olay ile tümleyeninin olasılıkları toplamının 1 olduğunu doğrular.",
                        "c) Ayrık ve ayrık olmayan olayları örnek uzay üzerinde ayırt eder.",
                    ],
                    "materyal": "Renkli Toplar, Ven Şeması ve Olasılık Ağacı",
                    "hook": "Şifreli kasa kombinasyonları ve bilgi yarışması çarkıfelek olasılık hesapları.",
                    "kriz": "Can gerçek hayatta hiçbir olayın tam olarak eş olasılıklı olamayceğini savunarak soruya itiraz eder.",
                    "kriz_odak_ogrenci": "Can",
                }
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "MAT.8.1. Sayılar ve Nicelikler",
            "MAT.8.2. Cebirsel Düşünme ve Değişimler",
            "MAT.8.3. Geometrik Şekiller",
            "MAT.8.4. Geometrik Nicelikler",
            "MAT.8.5. Dönüşüm",
            "MAT.8.6. İstatistiksel Araştırma Süreci",
            "MAT.8.7. Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "MAT.8.1. Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.1",
                    "cikti": "Üslü ve kareköklü ifadeleri gerçek sayılar kümesi bağlamında muhakeme edebilme",
                    "surec": [
                        "a) Tam sayıların tam sayı kuvvetlerini ve bilimsel gösterimi inceler.",
                        "b) Karenin alanı ile kenar uzunluğu arasındaki ilişkiden kareköklü ifadeleri yapılandırır.",
                        "c) Rasyonel ve irrasyonel sayıları ayırt ederek gerçek sayılar kümesini açıklar.",
                    ],
                    "materyal": "Karesel Alan Modelleri ve Gerçek Sayı Doğrusu",
                    "hook": "Mikroskobik hücre boyutlarının bilimsel gösterimi ve alanı 50 metrekare olan kare bahçenin kenar uzunluğu.",
                    "kriz": "Arda tam kare olmayan sayıların karekök değerlerinin sonsuza kadar düzensiz gitmesinden rahatsız olup kulaklarını kapatır.",
                    "kriz_odak_ogrenci": "Arda",
                }
            ],
            "MAT.8.2. Cebirsel Düşünme ve Değişimler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": "Doğrusal fonksiyonları, dik koordinat sistemindeki grafiklerini ve eğim kavramını yapılandırabilme",
                    "surec": [
                        "a) İki değişken arasındaki doğrusal ilişkiyi tablo, denklem ve grafikle temsil eder.",
                        "b) Doğrunun eğimini dikey değişimin yatay değişime oranı olarak yorumlar.",
                        "c) Özdeşlikleri ve çarpanlara ayırma süreçlerini geometrik alan modelleriyle doğrular.",
                    ],
                    "materyal": "Koordinat Tahtası, Eğim Rampası ve Cebir Karoları",
                    "hook": "Engelli rampalarının standartlara uygun eğim hesabı ve taksi ücret tarifesi grafiği.",
                    "kriz": "Elif LGS sınav kaygısıyla 'Bu grafik ve eğim sorularını sınavda asla yapamayacağım' diyerek kalemi bırakır.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
            "MAT.8.3. Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": "Üçgenlerde açı-kenar ilişkilerini, Pisagor bağıntısını ve çokgenlerde eşlik-benzerliği uygulayabilme",
                    "surec": [
                        "a) Üçgen eşitsizliğini ve açı-kenar bağıntılarını dinamik geometri yazılımıyla keşfeder.",
                        "b) Dik üçgende Pisagor bağıntısını alan modelleriyle ispatlayarak uygular.",
                        "c) Eş ve benzer çokgenlerin kenar ve açı oranlarını gerçek yaşam modellerinde kullanır.",
                    ],
                    "materyal": "Pisagor Su/Alan Modeli ve Dinamik Geometri Yazılımı",
                    "hook": "İtfaiye merdiveninin binaya ulaşma yüksekliği (Pisagor) ve mimari maket ölçeklendirme (Benzerlik).",
                    "kriz": "Kerem Pisagor bağıntısını hipotenüs yerine dik kenara uygulayıp yanlış sonuç bulunce defterini karalar.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.8.4. Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1",
                    "cikti": "Dik prizma, dik dairesel silindir, dik piramit ve dik koninin yüzey alanı ve hacim bağıntılarını kurabilme",
                    "surec": [
                        "a) Üç boyutlu cisimlerin açınımlarını 3D dijital araçlarla inceler.",
                        "b) Silindir, piramit ve koninin yüzey alanı ile hacim bağıntılarını prizmalar üzerinden geneller.",
                        "c) Üç boyutlu cisimlerin hacim ve alanlarıyla ilgili gerçek yaşam problemlerini çözer.",
                    ],
                    "materyal": "3B Açınım Modelleri, Birim Küpler ve GeoGebra 3D",
                    "hook": "Endüstriyel silindirik su depolarının ve konik tahıl silolarının kapasite hesabı.",
                    "kriz": "Kerem silindirin yan yüzey açınımındaki dikdörtgenin kenarını dairenin çevresiyle eşleştirmekte zorlanır.",
                    "kriz_odak_ogrenci": "Kerem",
                }
            ],
            "MAT.8.5. Dönüşüm": [
                {
                    "kod": "MAT.8.5.1",
                    "cikti": "Dik koordinat sisteminde şekillerin öteleme ve yansıma dönüşümleri altındaki görüntülerini belirleyebilme",
                    "surec": [
                        "a) Koordinat düzleminde öteleme hareketinin köşe koordinatlarına etkisini inceler.",
                        "b) Eksenlere göre yansıma dönüşümünde koordinat işaretlerinin değişimini geneller.",
                        "c) Ardışık öteleme ve yansıma dönüşümlerini dijital tahtada modeller.",
                    ],
                    "materyal": "Dijital Koordinat Tahtası ve Çoklu Görünüm Birim Küp Modelleri",
                    "hook": "Bilgisayar oyunlarında karakterlerin ekran üzerindeki koordinat hareket algoritmaları.",
                    "kriz": "Elif x eksenine göre yansımada neden y koordinatının işaret değiştirdiğini karıştırıp kaygılanır.",
                    "kriz_odak_ogrenci": "Elif",
                }
            ],
            "MAT.8.6. İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.8.6.1",
                    "cikti": "Bilimsel araştırma etiği, KVKK ve veri mahremiyeti ilkelerine uygun istatistiksel proje yürütebilme",
                    "surec": [
                        "a) Kişisel verilerin korunması (KVKK) ve etik ilkelere uygun veri toplama planı hazırlar.",
                        "b) Çoklu veri gruplarını uygun grafik türleriyle karşılaştırmalı analiz eder.",
                        "c) Veriye dayalı çıkarımlar yaparak yanlı/hatalı grafik gösterimlerini eleştirir.",
                    ],
                    "materyal": "KVKK Etik Kontrol Listesi ve Karşılaştırmalı Grafik Paneli",
                    "hook": "Okul genelinde dijital ekran süresi araştırması yaparken kişisel veri mahremiyetini koruma.",
                    "kriz": "Can arkadaşlarının isimlerini grafikte açıkça paylaşmak ister, mahremiyet uyarısına itiraz eder.",
                    "kriz_odak_ogrenci": "Can",
                }
            ],
            "MAT.8.7. Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1",
                    "cikti": "Simülasyonlar aracılığıyla deneysel ve teorik olasılık ilişkisini kurarak veriye dayalı karar verebilme",
                    "surec": [
                        "a) Dijital olasılık simülasyonlarında büyük sayılar yasasını gözlemler.",
                        "b) Deneysel olasılık sonuçlarının teorik olasılığa yakınsamasını yorumlar.",
                        "c) Belirsizlik içeren gerçek yaşam durumlarında olasılık verilerine dayanarak optimal karar verir.",
                    ],
                    "materyal": "Monte Carlo Dijital Olasılık Simülatörü",
                    "hook": "Kalite kontrol mühendisliğinde üretim hattındaki hatalı ürün olasılığını simülasyonla test etme.",
                    "kriz": "Can 'Büyük sayılar yasası gerçek hayatta tek seferlik kararlarda işe yaramıyor' diyerek tartışma başlatır.",
                    "kriz_odak_ogrenci": "Can",
                }
            ],
        },
    },
}
# ==========================================
# YARDIMCI FONKSİYON: 3B İZOMETRİK SINIF SAHNESİ OLUŞTURUCU
# (Sadece Öğretmen Adayı ve Öğrenciler Bulunur)
# ==========================================
def render_3d_classroom(
    ogretmen_adi,
    sinif_duzeyi,
    tema,
    kazanim_kodu,
    materyal,
    odak_ogrenci,
    mudahale_yapildi,
    mudahale_basarili,
    ogretmen_sozu,
    ogrenci_verileri,
):
    tahta_durum = (
        "🟢 Yapılandırmacı Keşif & Somut Materyal Aktif"
        if (mudahale_yapildi and mudahale_basarili)
        else (
            "🔴 Sınıf İçi Kriz Devam Ediyor"
            if mudahale_yapildi
            else "🟡 Kriz Anı: Öğretmen Adayının Müdahalesi Bekleniyor"
        )
    )

    ogretmen_balon = (
        ogretmen_sozu
        if ogretmen_sozu
        else "Arkadaşlar, tahtadaki modeli ve elimizdeki materyalleri birlikte inceleyelim..."
    )

    kartlar_html = ""
    for ogr in ogrenci_verileri:
        vurgu_stil = (
            "box-shadow: 0 0 18px rgba(250, 204, 21, 0.95); transform: translateY(-6px) scale(1.03);"
            if ogr["ad"].startswith(odak_ogrenci)
            else ""
        )
        kartlar_html += f"""
        <div class="desk-unit" style="border-color: {ogr['renk']}; {vurgu_stil}">
            <div class="speech-bubble" style="border-left: 4px solid {ogr['renk']};">
                💬 "{ogr['konusma']}"
            </div>
            <div class="avatar-circle" style="background: {ogr['arka_plan']}; border-color: {ogr['renk']};">
                <span class="avatar-face">{ogr['yuz']}</span>
                <span class="posture-badge">{ogr['postur_ikon']}</span>
            </div>
            <div class="desk-surface">
                <div class="student-name">{ogr['ad']}</div>
                <div class="gesture-tag" style="color: {ogr['renk']};">🎭 Jest/Mimik: {ogr['mimik']}</div>
                <div class="reaction-tag">⚡ Tepki: {ogr['tepki']}</div>
                <div class="manipulative-mini">🧩 {materyal}</div>
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
        body {{ margin: 0; padding: 8px; background: transparent; }}
        .scene-wrapper {{
            background: radial-gradient(circle at 50% 15%, #1e293b 0%, #0f172a 100%);
            border-radius: 18px;
            padding: 20px;
            color: #f8fafc;
            border: 2px solid #334155;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.6), 0 12px 24px rgba(0,0,0,0.25);
            perspective: 1100px;
        }}
        .classroom-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.75);
            padding: 8px 16px;
            border-radius: 10px;
            border: 1px solid #475569;
            margin-bottom: 14px;
            font-size: 13px;
        }}
        .smartboard {{
            background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
            border: 6px solid #b45309;
            border-radius: 12px;
            padding: 14px 20px;
            text-align: center;
            max-width: 82%;
            margin: 0 auto 18px auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            transform: rotateX(6deg);
        }}
        .smartboard-title {{
            color: #fde047;
            font-weight: 700;
            font-size: 15px;
            letter-spacing: 0.4px;
        }}
        .smartboard-sub {{
            color: #d1fae5;
            font-size: 13px;
            margin-top: 4px;
        }}
        .smartboard-tool {{
            display: inline-block;
            margin-top: 8px;
            background: rgba(255,255,255,0.12);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            color: #38bdf8;
            border: 1px dashed #38bdf8;
        }}
        .teacher-zone {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin: 12px auto 22px auto;
            padding: 12px 18px;
            max-width: 78%;
            background: linear-gradient(90deg, rgba(30, 58, 138, 0.65), rgba(30, 64, 175, 0.45));
            border: 2px solid #60a5fa;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
        }}
        .teacher-avatar {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #1d4ed8;
            border: 3px solid #93c5fd;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            flex-shrink: 0;
        }}
        .teacher-speech {{
            background: #eff6ff;
            color: #1e3a8a;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 13.5px;
            font-weight: 600;
            line-height: 1.4;
            flex-grow: 1;
            border-left: 5px solid #2563eb;
        }}
        .isometric-floor {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            padding: 12px 4px;
            transform: rotateX(8deg);
        }}
        @media (max-width: 900px) {{
            .isometric-floor {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        .desk-unit {{
            background: rgba(30, 41, 59, 0.92);
            border: 2px solid #64748b;
            border-radius: 14px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: all 0.3s ease;
            box-shadow: 0 10px 18px rgba(0,0,0,0.45);
        }}
        .speech-bubble {{
            background: #f8fafc;
            color: #0f172a;
            font-size: 12px;
            font-weight: 600;
            padding: 8px 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: 100%;
            min-height: 52px;
            display: flex;
            align-items: center;
            line-height: 1.35;
            box-shadow: 0 3px 8px rgba(0,0,0,0.25);
        }}
        .avatar-circle {{
            width: 66px;
            height: 66px;
            border-radius: 50%;
            border: 3px solid;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            margin-bottom: 8px;
        }}
        .avatar-face {{
            font-size: 34px;
        }}
        .posture-badge {{
            position: absolute;
            bottom: -4px;
            right: -6px;
            background: #0f172a;
            border-radius: 50%;
            padding: 2px 5px;
            font-size: 16px;
            border: 1px solid #94a3b8;
        }}
        .desk-surface {{
            width: 100%;
            background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
            border-top: 4px solid #ca8a04;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }}
        .student-name {{
            font-weight: 700;
            font-size: 13.5px;
            color: #f1f5f9;
            margin-bottom: 4px;
        }}
        .gesture-tag {{
            font-size: 11.5px;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .reaction-tag {{
            font-size: 11px;
            color: #cbd5e1;
            background: rgba(15, 23, 42, 0.65);
            padding: 4px 6px;
            border-radius: 6px;
            margin-bottom: 5px;
        }}
        .manipulative-mini {{
            font-size: 10.5px;
            color: #fde047;
            font-style: italic;
        }}
    </style>
    </head>
    <body>
    <div class="scene-wrapper">
        <div class="classroom-header">
            <span>🏫 <strong>3B İzometrik Sınıf Ortamı</strong> (Sınıfta Yalnızca Öğretmen Adayı ve Öğrenciler Bulunmaktadır)</span>
            <span>{tahta_durum}</span>
        </div>

        <div class="smartboard">
            <div class="smartboard-title">📐 AKILLI TAHTA | {sinif_duzeyi} - {tema} ({kazanim_kodu})</div>
            <div class="smartboard-sub">Etkinlik Odağı: Somut ve Dijital Temsillerle Matematiksel Muhakeme</div>
            <div class="smartboard-tool">🛠️ Aktif Sınıf Materyali: {materyal}</div>
        </div>

        <div class="teacher-zone">
            <div class="teacher-avatar">👩‍🏫</div>
            <div>
                <div style="font-size: 12px; color: #93c5fd; font-weight: 700; margin-bottom: 3px;">
                    ÖĞRETMEN ADAYI ({ogretmen_adi}) - SESLİ HİTABETİ & YÖNLENDİRMESİ:
                </div>
                <div class="teacher-speech">🎙️ "{ogretmen_balon}"</div>
            </div>
        </div>

        <div class="isometric-floor">
            {kartlar_html}
        </div>
    </div>
    </body>
    </html>
    """
    components.html(html_code, height=620, scrolling=True)


# ==========================================
# DETAYLI ANALİZ VE KÖK NEDEN MOTORU
# ==========================================
def detayli_pedagojik_analiz_uret(
    sesli_metin,
    secilen_karar,
    sinif,
    tema,
    kod,
    cikti,
    surec,
    materyal,
    rubrik_metni,
    ses_kaydi_var,
):
    kucuk_metin = sesli_metin.lower()
    yapilandirmaci_secim = "B)" in secilen_karar or "E)" in secilen_karar

    empati_kelimeleri = [
        "sakin", "birlikte", "anlıyorum", "endişelenme", "nefes", "yanındayım",
        "dinliyorum", "haklısın", "normal", "güven", "merak etme",
    ]
    materyal_kelimeleri = [
        "materyal", "model", "oran tahtası", "boncuk", "küp", "geogebra",
        "kesir", "terazi", "karo", "görsel", "tablo", "şekil", "cetvel", "somut",
    ]
    sorgulama_kelimeleri = [
        "nasıl", "neden", "ne fark ettin", "inceleyelim", "düşün", "örüntü",
        "ilişki", "keşf", "sence", "tahmin", "karşılaştır",
    ]
    olumsuz_kelimeler = [
        "ezberle", "sustur", "sus", "kuralı yaz", "formülü yaz", "ceza",
        "görmezden", "bağır", "otur yerine", "yanlış yaptın",
    ]

    empati_var = any(k in kucuk_metin for k in empati_kelimeleri)
    materyal_var = any(k in kucuk_metin for k in materyal_kelimeleri)
    sorgulama_var = any(k in kucuk_metin for k in sorgulama_kelimeleri)
    olumsuz_var = any(k in kucuk_metin for k in olumsuz_kelimeler)

    kriz_puan = 12
    if yapilandirmaci_secim:
        kriz_puan += 10
    if empati_var and not olumsuz_var:
        kriz_puan += 8
    kriz_puan = min(30, kriz_puan)

    kapsayici_puan = 12
    if yapilandirmaci_secim:
        kapsayici_puan += 10
    if not olumsuz_var and len(sesli_metin.strip()) > 20:
        kapsayici_puan += 8
    kapsayici_puan = min(30, kapsayici_puan)

    maarif_puan = 8
    if sorgulama_var:
        maarif_puan += 6
    if materyal_var:
        maarif_puan += 6
    maarif_puan = min(20, maarif_puan)

    saha_puan = 8
    if yapilandirmaci_secim:
        saha_puan += 8
    if ses_kaydi_var or len(sesli_metin.strip()) > 25:
        saha_puan += 4
    saha_puan = min(20, saha_puan)

    if olumsuz_var or not yapilandirmaci_secim:
        kriz_puan = max(8, kriz_puan - 10)
        kapsayici_puan = max(8, kapsayici_puan - 10)
        maarif_puan = max(6, maarif_puan - 6)
        saha_puan = max(6, saha_puan - 8)

    toplam_puan = kriz_puan + kapsayici_puan + maarif_puan + saha_puan

    iyi_yonler = []
    if yapilandirmaci_secim:
        iyi_yonler.append(
            f"**TYMM 2026 Yapılandırmacı Sınıf Yönetimi:** Kriz anında otoriter veya dışlayıcı tutum yerine öğrenciyi sürece dahil eden, güvenli öğrenme ortamı oluşturan pedagojik kararı seçtiniz."
        )
    if empati_var:
        iyi_yonler.append(
            "**Duyuşsal Düzenleme ve Empatik Hitabet:** Sesli geri bildiriminizde öğrencinin kaygısını/duyusal hassasiyetini yatıştıran kapsayıcı ve destekleyici ifadeler kullandınız."
        )
    if materyal_var:
        iyi_yonler.append(
            f"**Somut ve Dijital Temsil Entegrasyonu:** `{kod}` kazanımına uygun olarak ({materyal}) kullanımını teşvik edip soyut kavramları somutlaştırdınız."
        )
    if sorgulama_var:
        iyi_yonler.append(
            f"**Süreç Bileşeni Odaklı Sorgulama:** '{surec}' süreç bileşenini harekete geçirecek açık uçlu ve düşündürücü yönlendirmeler yaptınız."
        )
    if ses_kaydi_var:
        iyi_yonler.append(
            "**Doğrudan Sesli İletişim:** Mikrofon kullanarak sınıf içi sözlü iletişim ve ses tonu kontrolü pratiğini aktif olarak gerçekleştirdiniz."
        )
    if not iyi_yonler:
        iyi_yonler.append(
            "**Temel Sınıf Farkındalığı:** Kriz durumunu fark ederek sınıf içi müdahale sürecini başlattınız."
        )

    eksik_yonler = []
    kok_nedenler = []
    cozum_onerileri = []

    if not yapilandirmaci_secim or olumsuz_var:
        eksik_yonler.append(
            "**Davranışçı ve Kural Odaklı Müdahale Eğilimi:** Öğrencinin yaşadığı bilişsel veya duyusal krizi disiplin sopasıyla, susturarak ya da doğrudan formül/kural dikte ederek çözmeye yöneldiniz."
        )
        kok_nedenler.append(
            "**Geleneksel Öğretim Alışkanlıkları ve Zaman Kaygısı:** Müfredatı yetiştirme baskısı veya geleneksel sınıf yönetimi kalıpları nedeniyle, kriz anlarında öğrenciyi dinlemek yerine hızlıca konuyu anlatıp geçme refleksinin devreye girmesi."
        )
        cozum_onerileri.append(
            "**Güvenli Alan ve Akran Desteği Protokolü:** Kriz anında önce 5 saniye bekleme süresi (wait-time) tanıyın. Öğrenciyi yargılamadan 'Zorlanman çok doğal, gel bunu basamak basamak model üzerinde inceleyelim' diyerek süreci yapılandırın."
        )

    if not materyal_var:
        eksik_yonler.append(
            f"**Somut/Dijital Materyal Referansının Eksikliği:** Sesli geri bildiriminizde dersin ana aracı olan **{materyal}** materyalini öğrencinin nasıl kullanacağına dair açık bir yönlendirme yer almadı."
        )
        kok_nedenler.append(
            "**Soyut Sembolik Düzeye Erken Geçiş:** Matematik öğretiminde Somut -> Yarı Somut -> Soyut (CPA) aşamalarını atlayarak doğrudan sözel veya cebirsel açıklamayla kavramı kazandırma yanılgısı."
        )
        cozum_onerileri.append(
            f"**Çoklu Temsil Köprüsü Kurma:** Hitabetinizde doğrudan materyale işaret ederek *'Elindeki {materyal} üzerinde bu değişimi denediğinde ne görüyorsun?'* şeklinde somut deneyimle matematiksel kural arasında kurun kurun."
        )

    if not sorgulama_var:
        eksik_yonler.append(
            f"**Süreç Bileşenini Tetikleyen Keşif Sorularının Yetersizliği:** Seçilen `{surec}` basamağında öğrencinin kendi çıkarımını yapmasını sağlayacak üst düzey muhakeme soruları eksik kaldı."
        )
        kok_nedenler.append(
            "**Cevabı Öğretmenin Verme Eğilimi (Tersine İpucu):** Öğrenci zorlandığında bilişsel yükü öğrenciden alıp cevabı doğrudan söylemenin öğrenciye yardımcı olacağı düşüncesi."
        )
        cozum_onerileri.append(
            "**Yapılandırılmış İpucu (Scaffolding) Soruları:** Doğrudan bilgi vermek yerine *'Önceki adımda ne değişti?', 'Buradaki ortak örüntü sence ne olabilir?'* gibi yönlendirici sorularla öğrencinin kavramı kendisinin inşa etmesini sağlayın."
        )

    if not empati_var:
        eksik_yonler.append(
            "**Bireysel Farklılıklara Duyarlı Hitabet Eksikliği:** Özel gereksinimli veya yüksek kaygılı öğrencinin o anki duyuşsal ihtiyacını doğrudan karşılayan empatik kelimeler sesli ifadede yeterince yer almadı."
        )
        kok_nedenler.append(
            "**Yalnızca Akademik İçeriğe Odaklanma:** Matematik dersinde bilişsel hedefe odaklanırken öğrencinin öz-düzenleme ve duyuşsal hazırbulunuşluk ihtiyacının geri planda kalması."
        )
        cozum_onerileri.append(
            "**Kapsayıcı Dil Kalıpları Kullanımı:** Disleksili, otizmli, kaygılı veya üstün yetenekli öğrencilere hitap ederken önce duygularını onaylayın (*'Seni anlıyorum, farklı bir yoldan giderek birlikte bakalım'*), ardından farklılaştırılmış görevi verin."
        )

    if not eksik_yonler:
        eksik_yonler.append(
            "**İleri Düzey Akran Tartışması ve Zenginleştirme Entegrasyonu:** Bireysel kriz başarıyla yönetilmiş olmakla birlikte, kriz anındaki matematiksel yanılgının tüm sınıfın katılımıyla bir 'kavramsal sorgulama fırsatına' dönüştürülmesi derinleştirilebilir."
        )
        kok_nedenler.append(
            "**Birebir Müdahale ile Sınıf Geneli Etkileşim Dengesi:** Odak öğrenciyle ilgilenirken sınıftaki diğer öğrencilerin bilişsel süreçten kopma riski."
        )
        cozum_onerileri.append(
            "**Farklılaştırma (Destekleme & Zenginleştirme) Eşzamanlılığı:** Odak öğrenciyle somut materyal çalışırken, diğer öğrencilere *'Bu kuralın geçerli olmadığı bir karşıt örnek bulabilir misiniz?'* sorusunu yönelterek tüm sınıfı aktif tutun."
        )

    rubrik_satirlari = [s.strip() for s in rubrik_metni.split("\n") if s.strip()]
    rubrik_analiz_listesi = []
    for idx, satir in enumerate(rubrik_satirlari, 1):
        oran = toplam_puan / 100.0
        durum = (
            "Tam Uyumlu / Başarılı"
            if oran >= 0.8
            else (
                "Kısmen Uyumlu / Geliştirilmeli"
                if oran >= 0.55
                else "Yetersiz / Müdahale Gerekli"
            )
        )
        rubrik_analiz_listesi.append({
            "Kriter No": f"Kriter {idx}",
            "Rubrik Maddesi": satir,
            "Uyum Durumu": durum,
            "Başarı Yüzdesi": f"%{int(oran * 100)}",
        })

    return {
        "toplam_puan": toplam_puan,
        "alt_puanlar": {
            "kriz": kriz_puan,
            "kapsayici": kapsayici_puan,
            "maarif": maarif_puan,
            "saha": saha_puan,
        },
        "iyi_yonler": iyi_yonler,
        "eksik_yonler": eksik_yonler,
        "kok_nedenler": kok_nedenler,
        "cozum_onerileri": cozum_onerileri,
        "rubrik_analiz_listesi": rubrik_analiz_listesi,
        "yapilandirmaci_mi": yapilandirmaci_secim and not olumsuz_var,
    }


# ==========================================
# 2. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.subheader("📝 Stajyer Öğretmen 2026 Maarif Modeli Kurulum ve Rubrik Yükleme Paneli")
    st.info(
        "Bilgilerinizi girin ve uygulama öğretim elemanının değerlendirme rubriğini "
        "sisteme tanımlayarak 3B canlı sınıf simülasyonunu başlatın."
    )

    col1, col2 = st.columns(2)
    with col1:
        ogretmen_adi = st.text_input(
            "Öğretmen Adayı Adı Soyadı",
            value=st.session_state.get("ogretmen_adi", ""),
            placeholder="Örn: Mislina Taysi",
        )
        okul_numarasi = st.text_input(
            "Okul Numarası",
            value=st.session_state.get("okul_numarasi", ""),
            placeholder="Örn: 20220504012",
        )
        universite_adi = st.text_input(
            "Üniversite Adı",
            value=st.session_state.get("universite_adi", ""),
            placeholder="Örn: Kahramanmaraş Sütçü İmam Üniversitesi",
        )
        fakulte_bolum = st.text_input(
            "Fakülte ve Bölüm",
            value=st.session_state.get(
                "fakulte_bolum", "Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği"
            ),
        )
        uygulama_ogretim_elemani = st.text_input(
            "Uygulama Öğretim Elemanı (Rapor Değerlendiricisi)",
            value=st.session_state.get("uygulama_ogretim_elemani", ""),
            placeholder="Örn: Prof. Dr. Selma Çetin",
        )

    with col2:
        st.markdown("### 📋 Uygulama Öğretim Elemanı Değerlendirme Rubriği")
        rubrik_dosya = st.file_uploader(
            "Değerlendirme Rubriği Dosyasını Yükle (TXT, CSV, PDF, DOCX)",
            type=["txt", "csv", "pdf", "docx"],
        )

        varsayilan_rubrik = (
            "1. Sınıf içi kriz anında sesli iletişim, empati ve duyuşsal düzenleme (30 Puan)\n"
            "2. Özel gereksinimli ve farklı profillerdeki öğrencilere kapsayıcı yaklaşım (30 Puan)\n"
            "3. TYMM 2026 öğrenme çıktısı ve süreç bileşenlerini somut materyallerle işletme (20 Puan)\n"
            "4. Yapılandırmacı sorgulama ve kavramsal yanılgıları giderme başarısı (20 Puan)"
        )
        if rubrik_dosya is not None and rubrik_dosya.name.endswith(".txt"):
            try:
                varsayilan_rubrik = rubrik_dosya.read().decode("utf-8")
            except Exception:
                pass

        rubrik_metni = st.text_area(
            "Uygulama Öğretim Elemanının Rubrik Kriterleri",
            value=st.session_state.get("rubrik_metni", varsayilan_rubrik),
            height=130,
        )

        st.markdown("### 👥 Sınıf Mevcudu ve Öğrenci Profili Dağılımı")
        sinif_mevcudu = st.slider(
            "Sınıf Mevcudu (Toplam Öğrenci)", min_value=12, max_value=35, value=24
        )

    if st.button("🚀 2026 Maarif Modeli 3B Sınıf Simülasyonunu Başlat", use_container_width=True):
        if (
            not ogretmen_adi
            or not okul_numarasi
            or not universite_adi
            or not uygulama_ogretim_elemani
        ):
            st.warning("Lütfen zorunlu alanları doldurunuz.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi
            st.session_state.okul_numarasi = okul_numarasi
            st.session_state.universite_adi = universite_adi
            st.session_state.fakulte_bolum = fakulte_bolum
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
            st.session_state.rubrik_metni = rubrik_metni
            st.session_state.sinif_mevcudu = sinif_mevcudu
            st.session_state.adim = 2
            st.rerun()

# ==========================================
# 3. ADIM 2: 3B SINIF ORTAMI & SESLİ GERİ BİLDİRİM
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    okul_no = st.session_state.get("okul_numarasi", "N/A")
    universite = st.session_state.get("universite_adi", "Üniversite")

    st.markdown(
        f"### 🏫 3B Sınıf Simülasyonu | Öğretmen Adayı: {ogretmen} ({okul_no}) - {universite}"
    )

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        secilen_sinif = st.selectbox(
            "1️⃣ Sınıf Düzeyi Seçin (TYMM 2026)", list(tyym_master_arsiv.keys())
        )
    with col_s2:
        secilen_tema = st.selectbox(
            "2️⃣ Tema Seçin (TYMM 2026)", tyym_master_arsiv[secilen_sinif]["Temalar"]
        )

    kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]

    with col_s3:
        kazanim_secenekleri = [f"{k['kod']} - {k['cikti']}" for k in kazanim_listesi]
        secilen_kazanim_str = st.selectbox(
            "3️⃣ Öğrenme Çıktısı / Kazanım Seçin", kazanim_secenekleri
        )

    secilen_kazanim_obj = next(
        k for k in kazanim_listesi if f"{k['kod']} - {k['cikti']}" == secilen_kazanim_str
    )

    secilen_surec = st.selectbox(
        "4️⃣ İşlenecek Süreç Bileşenini Seçin (TYMM 2026):",
        secilen_kazanim_obj["surec"],
    )

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.info(
            f"📌 **Resmî Öğrenme Çıktısı (`{secilen_kazanim_obj['kod']}`):** {secilen_kazanim_obj['cikti']}\n\n"
            f"🔄 **Aktif Süreç Bileşeni:** {secilen_surec}"
        )
    with col_info2:
        st.success(
            f"💡 **Gerçek Yaşam Bağlamı:** {secilen_kazanim_obj['hook']}\n\n"
            f"🛠️ **Sınıf İçi Matematiksel Araç/Materyal:** {secilen_kazanim_obj['materyal']}"
        )

    aktif_kriz = secilen_kazanim_obj["kriz"]
    odak_ogrenci = secilen_kazanim_obj.get("kriz_odak_ogrenci", "Kerem")

    son_oturum = (
        st.session_state.simulasyon_gecmisi[-1]
        if len(st.session_state.simulasyon_gecmisi) > 0
        else None
    )
    aktif_mudahale_var = (
        son_oturum is not None and son_oturum["kod"] == secilen_kazanim_obj["kod"]
    )
    mudahale_basarili = (
        aktif_mudahale_var and son_oturum["analiz"]["yapilandirmaci_mi"]
    )
    ogretmen_son_soz = son_oturum["sesli_komut"] if aktif_mudahale_var else ""

    if not aktif_mudahale_var:
        ogrenci_avatar_verileri = [
            {
                "ad": "Kerem (Disleksili Öğrenci)",
                "yuz": "😣",
                "postur_ikon": "🤦‍♂️",
                "mimik": "Alnını ovuşturuyor, gözlerini kısıyor",
                "tepki": "Tahtadaki sembolleri ve basamakları ters algılayıp gerildi",
                "konusma": "Öğretmenim sayılar ve semboller birbirine giriyor, okurken karıştırıyorum!",
                "renk": "#ef4444",
                "arka_plan": "rgba(239, 68, 68, 0.25)",
            },
            {
                "ad": "Arda (Otizm Spektrumlu)",
                "yuz": "😖",
                "postur_ikon": "🎧",
                "mimik": "Ellerini kulaklarına götürüyor, öne sallanıyor",
                "tepki": "Sınıftaki ani gürültü ve düzensizlikten duyusal olarak rahatsız oldu",
                "konusma": "Çok ses var ve sıra bozuldu! Materyalin kuralı neden değişti?",
                "renk": "#10b981",
                "arka_plan": "rgba(16, 185, 129, 0.25)",
            },
            {
                "ad": "Can (Üstün Yetenekli)",
                "yuz": "😤",
                "postur_ikon": "🙋‍♂️",
                "mimik": "Sabırsızca el kaldırıyor, kaşları çatık",
                "tepki": "Temel açıklamayı basit bulup kuralların sınırlarını sorguluyor",
                "konusma": "Öğretmenim bu kural her zaman geçerli olamaz, neden direkt üst düzeye geçmiyoruz?",
                "renk": "#f59e0b",
                "arka_plan": "rgba(245, 158, 11, 0.25)",
            },
            {
                "ad": "Elif (STU-1309 | Kaygılı)",
                "yuz": "😰",
                "postur_ikon": "🙇‍♀️",
                "mimik": "Başını sıraya eğmiş, kalemini sıkıyor",
                "tepki": "Hata yapma korkusuyla somut materyale dokunmaya çekiniyor",
                "konusma": "Öğretmenim formülü unutursam yanlış yaparım diye çok korkuyorum...",
                "renk": "#38bdf8",
                "arka_plan": "rgba(56, 189, 248, 0.25)",
            },
        ]
    elif mudahale_basarili:
        ogrenci_avatar_verileri = [
            {
                "ad": "Kerem (Disleksili Öğrenci)",
                "yuz": "😊",
                "postur_ikon": "🙌",
                "mimik": "Yüzü aydınlandı, materyali parmağıyla takip ediyor",
                "tepki": "Somut materyal ve renk kodlarıyla basamak/şekil ilişkisini kavradı",
                "konusma": "Harika! Somut model üzerinde renklerle eşleştirince hiç karışmadı öğretmenim!",
                "renk": "#22c55e",
                "arka_plan": "rgba(34, 197, 94, 0.25)",
            },
            {
                "ad": "Arda (Otizm Spektrumlu)",
                "yuz": "🙂",
                "postur_ikon": "🧩",
                "mimik": "Sakinleşti, omuzları gevşedi, modele odaklandı",
                "tepki": "Sakin ses tonunuz ve yapılandırılmış yönergenizle güven kazandı",
                "konusma": "Şimdi adımlar çok net oldu öğretmenim, örüntüyü modelde görebiliyorum.",
                "renk": "#22c55e",
                "arka_plan": "rgba(34, 197, 94, 0.25)",
            },
            {
                "ad": "Can (Üstün Yetenekli)",
                "yuz": "🤩",
                "postur_ikon": "💡",
                "mimik": "Gözleri parlıyor, arkadaşına modeli gösteriyor",
                "tepki": "Akran tartışması ve derinleştirici soruyla enerjisini üretime yönlendirdi",
                "konusma": "Gerçek yaşam örneği üzerinden düşününce aradaki matematiksel kanıtı buldum!",
                "renk": "#22c55e",
                "arka_plan": "rgba(34, 197, 94, 0.25)",
            },
            {
                "ad": "Elif (STU-1309 | Kaygılı)",
                "yuz": "😄",
                "postur_ikon": "✍️",
                "mimik": "Başını kaldırdı, özgüvenle gülümsüyor",
                "tepki": "Ezber baskısı kalkınca materyal üzerinde keşfetmeye başladı",
                "konusma": "Ezberlemek zorunda olmadığımı bilmek beni çok rahatlattı, oran sabitini buldum!",
                "renk": "#22c55e",
                "arka_plan": "rgba(34, 197, 94, 0.25)",
            },
        ]
    else:
        ogrenci_avatar_verileri = [
            {
                "ad": "Kerem (Disleksili Öğrenci)",
                "yuz": "😞",
                "postur_ikon": "🙅‍♂️",
                "mimik": "Defterini kapattı, kollarını kavuşturdu",
                "tepki": "Soyut kural dayatması nedeniyle öğrenilmiş çaresizlik yaşıyor",
                "konusma": "Kuralı deftere yazsam da yine okuyamıyorum, yapamayacağım...",
                "renk": "#dc2626",
                "arka_plan": "rgba(220, 38, 38, 0.3)",
            },
            {
                "ad": "Arda (Otizm Spektrumlu)",
                "yuz": "😣",
                "postur_ikon": "🙈",
                "mimik": "Sırasına kapandı, iletişimi tamamen kesti",
                "tepki": "Sert ve kuralcı uyarı duyusal aşırı yüklenmesini artırdı",
                "konusma": "İstemiyorum, çok karışık!",
                "renk": "#dc2626",
                "arka_plan": "rgba(220, 38, 38, 0.3)",
            },
            {
                "ad": "Can (Üstün Yetenekli)",
                "yuz": "😒",
                "postur_ikon": "💤",
                "mimik": "Sıkılmış ifadeyle pencereden dışarı bakıyor",
                "tepki": "Sorgulaması bastırıldığı için derse olan ilgisini kaybetti",
                "konusma": "Sadece formül ezberleyeceksek düşünmemize gerek yok ki...",
                "renk": "#dc2626",
                "arka_plan": "rgba(220, 38, 38, 0.3)",
            },
            {
                "ad": "Elif (STU-1309 | Kaygılı)",
                "yuz": "😢",
                "postur_ikon": "💧",
                "mimik": "Gözleri doldu, silgisiyle kağıdı siliyor",
                "tepki": "Otoriter tutum nedeniyle hata yapma kaygısı zirveye çıktı",
                "konusma": "Anlamadım diyemiyorum, öğretmen kızacak diye çok korkuyorum...",
                "renk": "#dc2626",
                "arka_plan": "rgba(220, 38, 38, 0.3)",
            },
        ]

    render_3d_classroom(
        ogretmen_adi=ogretmen,
        sinif_duzeyi=secilen_sinif,
        tema=secilen_tema,
        kazanim_kodu=secilen_kazanim_obj["kod"],
        materyal=secilen_kazanim_obj["materyal"],
        odak_ogrenci=odak_ogrenci,
        mudahale_yapildi=aktif_mudahale_var,
        mudahale_basarili=mudahale_basarili,
        ogretmen_sozu=ogretmen_son_soz,
        ogrenci_verileri=ogrenci_avatar_verileri,
    )

    col_sol, col_sag = st.columns([1.15, 0.85], gap="large")

    with col_sol:
        st.markdown("#### ⚡ Sınıfta Yaşanan Anlık Durum")
        st.warning(f"🔔 **Aktif Sınıf Senaryosu:** {aktif_kriz}")

        st.markdown("### 🎙️ Öğretmen Adayı Sesli Geri Bildirim & Mikrofon Konsolu")
        st.info(
            "1️⃣ **Gerçek Ses Kaydı:** Aşağıdaki mikrofon butonuna basarak öğrencilerinize sesli geri bildiriminizi doğrudan kaydedin.\n\n"
            "2️⃣ **Sesli Geri Bildirim Metni (Dikte / Klavye):** Söylediğiniz ifadelerin kelimesi kelimesine analiz edilmesi için tabletinizin klavyesindeki mikrofon tuşuyla konuşarak yazdırabilirsiniz."
        )

        ses_verisi = None
        if hasattr(st, "audio_input"):
            ses_verisi = st.audio_input("🎤 Mikrofonu Açıp Sesli Geri Bildiriminizi Kaydedin:")
            if ses_verisi is not None:
                st.success("✅ Ses kaydınız alındı:")
                st.audio(ses_verisi)

        sesli_geri_bildirim_metni = st.text_area(
            "🗣️ Öğrencilere Söylediğiniz Sesli Geri Bildirim İfadesi:",
            value="",
            height=95,
            placeholder=(
                f"Örn: Sakin ol {odak_ogrenci}, seni çok iyi anlıyorum. Ezberlemek zorunda değiliz; "
                f"gel birlikte {secilen_kazanim_obj['materyal']} üzerinde adım adım inceleyelim, ne fark ettin?"
            ),
        )

        st.markdown("### 👩‍🏫 Sınıf İçi Pedagojik Eylem Kararınız")
        ogretmen_karari = st.radio(
            "Sesli geri bildiriminizle birlikte sınıfta hangi pedagojik aksiyonu uyguluyorsunuz?",
            [
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve sınıf disiplinini sert kurallarla korumak.",
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak, akran destekli empati kurdurmak ve somut materyalle desteklemek.",
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu kural ve formüllerle anlatmaya devam etmek.",
                "D) Sınıfın seviyesinin yetersiz olduğunu söyleyip öğrencilere ek ödev cezası vermek.",
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak somut ve dijital temsillerle kavramsal değişimi tetiklemek.",
            ],
        )

        if st.button("📥 Sesli Geri Bildirimi Uygula & 3B Sınıf Tepkisini Gör", use_container_width=True):
            if not sesli_geri_bildirim_metni.strip() and ses_verisi is None:
                st.error("⚠️ Lütfen ses kaydı yapın veya sesli geri bildirim metninizi girin.")
            else:
                islenen_metin = (
                    sesli_geri_bildirim_metni.strip()
                    if sesli_geri_bildirim_metni.strip()
                    else "Öğrencilere mikrofon üzerinden sesli geri bildirim verildi."
                )
                analiz_sonucu = detayli_pedagojik_analiz_uret(
                    sesli_metin=islenen_metin,
                    secilen_karar=ogretmen_karari,
                    sinif=secilen_sinif,
                    tema=secilen_tema,
                    kod=secilen_kazanim_obj["kod"],
                    cikti=secilen_kazanim_obj["cikti"],
                    surec=secilen_surec,
                    materyal=secilen_kazanim_obj["materyal"],
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
                    "materyal": secilen_kazanim_obj["materyal"],
                    "kriz": aktif_kriz,
                    "odak_ogrenci": odak_ogrenci,
                    "karar": ogretmen_karari,
                    "sesli_komut": islenen_metin,
                    "ses_dosyasi": ses_verisi.getvalue() if ses_verisi is not None else None,
                    "puan": analiz_sonucu["toplam_puan"],
                    "analiz": analiz_sonucu,
                })
                st.rerun()

    with col_sag:
        st.markdown("#### 💬 Öğrencilerin Anlık Diyalogları ve Tepki Özeti")
        for ogr in ogrenci_avatar_verileri:
            with st.container(border=True):
                st.markdown(f"**{ogr['yuz']} {ogr['ad']}**")
                st.caption(f"🎭 **Jest ve Mimik:** {ogr['mimik']} | ⚡ **Durum:** {ogr['tepki']}")
                st.markdown(f"> 🗣️ *\"{ogr['konusma']}\"*")

        if len(st.session_state.simulasyon_gecmisi) > 0:
            son = st.session_state.simulasyon_gecmisi[-1]
            st.success(
                f"✅ **Son Müdahale Puanı: {son['puan']}/100** — Yukarıdaki 3B sınıf sahnesinde "
                "öğrencilerin jest, mimik ve konuşmalarının verdiğiniz sesli geri bildirime göre "
                "nasıl değiştiğini inceleyebilirsiniz."
            )
            if st.button("📋 Çok Katmanlı Detaylı Raporlara ve Analizlere Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()

# ==========================================
# 4. ADIM 3: RAPORLAR, BÖLÜM ÖZ-DEĞERLENDİRME VE ANKET
# ==========================================
elif st.session_state.adim == 3:
    st.subheader("📊 TYMM 2026 & RUBRİK UYUMLU ÇOK KATMANLI DETAYLI ANALİZ VE RAPORLAMA SİSTEMİ")
    st.markdown(
        f"**Üniversite & Bölüm:** {st.session_state.get('universite_adi', 'N/A')} / "
        f"{st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
        f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} ({st.session_state.get('okul_numarasi', 'N/A')}) | "
        f"**Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    toplam_islem = len(st.session_state.simulasyon_gecmisi)
    ortalama_puan = (
        int(sum(k["puan"] for k in st.session_state.simulasyon_gecmisi) / toplam_islem)
        if toplam_islem > 0
        else 0
    )

    tab_aday, tab_rubrik, tab_dekanlik, tab_anket = st.tabs([
        "👩‍🏫 1. Aday Detaylı Pedagojik Analiz (İyi/Eksik Yönler, Kök Neden & Çözüm)",
        "📋 2. Öğretim Elemanı Rubriği & Maarif Programı Değerlendirme Matrisi",
        "🏛️ 3. Dekanlık & Bölüm Öz-Değerlendirme ve Program Geliştirme Raporu",
        "⭐ 4. Adayların Simülasyon Uygulamasını Değerlendirme Formu",
    ])

    with tab_aday:
        if toplam_islem == 0:
            st.warning("Henüz kaydedilmiş bir simülasyon oturumu bulunmuyor.")
        else:
            st.markdown("### 🎯 Oturum Bazlı Detaylı Öğretim Programı ve Sınıf Yönetimi Analizi")
            for idx, oturum in enumerate(st.session_state.simulasyon_gecmisi, 1):
                analiz = oturum["analiz"]
                with st.container(border=True):
                    st.markdown(
                        f"#### 📌 Oturum #{idx}: {oturum['sinif']} | {oturum['tema']} (`{oturum['kod']}`) — **Puan: {oturum['puan']}/100**"
                    )
                    st.markdown(
                        f"- **Öğrenme Çıktısı:** {oturum['cikti']}\n"
                        f"- **Süreç Bileşeni:** {oturum['surec']}\n"
                        f"- **Kullanılan Materyal:** {oturum['materyal']}\n"
                        f"- **Sınıf İçi Kriz:** {oturum['kriz']}\n"
                        f"- **Adayın Sesli Geri Bildirimi:** *\"{oturum['sesli_komut']}\"*"
                    )

                    if oturum.get("ses_dosyasi") is not None:
                        st.markdown("**🔊 Sesli Geri Bildirim Kaydınız:**")
                        st.audio(oturum["ses_dosyasi"])

                    st.divider()
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        st.markdown("##### ✅ İyi ve Güçlü Yönler")
                        for m in analiz["iyi_yonler"]:
                            st.success(m)
                        st.markdown("##### ⚠️ Eksik ve Geliştirilmesi Gereken Yönler")
                        for m in analiz["eksik_yonler"]:
                            st.warning(m)
                    with col_a2:
                        st.markdown("##### 🔍 Eksikliklerin Kök Nedenleri")
                        for m in analiz["kok_nedenler"]:
                            st.error(m)
                        st.markdown("##### 🛠️ Çözüm Yolları ve Öneriler (Ne Yapılırsa Çözülür?)")
                        for m in analiz["cozum_onerileri"]:
                            st.info(m)

    with tab_rubrik:
        st.markdown("### 👨‍🏫 Uygulama Öğretim Elemanı Değerlendirme Rubriği ve TYMM 2026 Uyum Raporu")
        if toplam_islem == 0:
            st.warning("Değerlendirme matrisi için önce en az bir oturum tamamlayınız.")
        else:
            son_analiz = st.session_state.simulasyon_gecmisi[-1]["analiz"]
            alt_p = son_analiz["alt_puanlar"]

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Sesli Kriz Yönetimi & Empati", f"{alt_p['kriz']} / 30")
            col_m2.metric("Kapsayıcı Eğitim Yaklaşımı", f"{alt_p['kapsayici']} / 30")
            col_m3.metric("TYMM 2026 Süreç Bileşeni", f"{alt_p['maarif']} / 20")
            col_m4.metric("Yapılandırmacı Saha Aksiyonu", f"{alt_p['saha']} / 20")

            st.markdown("#### 📋 Rubrik Maddelerine Göre Değerlendirme Tablosu")
            df_rubrik = pd.DataFrame(son_analiz["rubrik_analiz_listesi"])
            st.dataframe(df_rubrik, use_container_width=True, hide_index=True)

            st.markdown("#### 📈 Maarif Modeli Alan Becerileri ve Rubrik Performans Grafiği")
            grafik_df = pd.DataFrame({
                "Değerlendirme Boyutu": [
                    "Sesli Kriz Yönetimi (30p)",
                    "Kapsayıcı Pedagoji (30p)",
                    "Maarif Süreç Bileşeni (20p)",
                    "Materyal & Saha Uygulaması (20p)",
                ],
                "Tamlanan Yüzde (%)": [
                    int((alt_p["kriz"] / 30) * 100),
                    int((alt_p["kapsayici"] / 30) * 100),
                    int((alt_p["maarif"] / 20) * 100),
                    int((alt_p["saha"] / 20) * 100),
                ],
            })
            st.bar_chart(grafik_df, x="Değerlendirme Boyutu", y="Tamlanan Yüzde (%)")

            st.markdown("---")
            st.markdown("#### ✍️ Öğretim Elemanının Adaya Özel Geri Dönütü")
            hoca_notu = st.text_area(
                "Uygulama Öğretim Elemanı Değerlendirme ve Gelişim Notu:",
                placeholder="Örn: Adayımız somut materyal kullanımında başarılı...",
            )
            if st.button("📤 Öğretim Elemanı Geri Dönütünü Raporlara İşle"):
                if hoca_notu.strip():
                    st.session_state.hoca_geri_donutleri.append(hoca_notu.strip())
                    st.success("✅ Öğretim elemanı geri dönütü başarıyla rapora eklendi!")

    with tab_dekanlik:
        st.markdown("### 🏛️ Eğitim Fakültesi Dekanlığı & İlköğretim Matematik Öğretmenliği Bölümü Öz-Değerlendirme Raporu")
        st.info(
            "📌 **Raporun Amacı:** Bu rapor, adayın staja çıkıp çıkmamasına karar veren bir eleme belgesi **değildir**. "
            "Simülasyon verilerinden hareketle **bölümün kendi öğretmen yetiştirme programındaki güçlü yönlerini ve eksikliklerini fark etmesi**, "
            "bu eksikliklerin neden kaynaklandığını saptaması ve dersleri nasıl geliştirebileceğine dair somut çözümler üretmesi amacıyla oluşturulmuştur."
        )

        with st.container(border=True):
            st.markdown("#### 1. Bölümün Güçlü Yönleri (Adaylara Kazandırılan Yetkinlikler)")
            st.markdown(
                "- **Kuramsal Müfredat Okuryazarlığı:** Adayların 2026 Türkiye Yüzyılı Maarif Modeli temalarını ve süreç bileşenlerini tanıma farkındalığı yüksektir.\n"
                "- **Matematiksel Materyal Bilgisi:** Somut materyallerin (oran tahtası, birim küpler vb.) pedagojik işlevi güçlü bilinmektedir."
            )
            st.markdown("#### 2. Bölüm Eğitiminde Fark Edilen Eksik Yönler")
            st.markdown(
                "- **Kriz Anında Kuramdan Uygulamaya Geçiş Boşluğu:** Adaylar sınıfta anlık kriz (disleksi, otizm, kaygı) çıktığında panikleyebilmektedir.\n"
                "- **Mikro-Rehberlik (Scaffolding) Dili Eksikliği:** Öğrenciye doğrudan formül vermeden keşfettirecek soru sorma pratikleri geliştirilmelidir."
            )
            st.markdown("#### 3. Eksikliklerin Kök Nedenleri (Neden Kaynaklanıyor?)")
            st.markdown(
                "- **Teori-Uygulama Kopukluğu:** Vakaların kağıt üzerinde kalması ve gerçekçi sesli sınıf simülasyonlarının yetersizliği."
            )
            st.markdown("#### 4. Bölüm ve Dekanlık İçin Çözüm Önerileri (Ne Yapılırsa Çözülebilir?)")
            st.markdown(
                "1. **3B Simülasyon Laboratuvarları:** Staj öncesi derslerde bu simülasyonun kullanılması zorunlu tutulmalıdır.\n"
                "2. **Özel Eğitim Entegrasyonu:** Matematik öğretimi derslerine özel gereksinimli birey uyarlama modülleri eklenmelidir."
            )

    with tab_anket:
        st.markdown("### ⭐ Öğretmen Adaylarının 3B Simülasyon Uygulamasını Değerlendirme Formu")
        st.info("Simülasyon uygulamasının kendisini (3B ortam, maarif uyumu, sesli geri bildirim, raporlar) değerlendirin.")

        with st.container(border=True):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_ortam = st.slider("1. 3B Sınıf Ortamı ve Jest/Mimik Temsillerinin Gerçekçiliği (1-5)", 1, 5, 5)
                p_mufredat = st.slider("2. TYMM 2026 Uyumu (1-5)", 1, 5, 5)
                p_ses = st.slider("3. Sesli Geri Bildirim Mekanizmasının Kullanışlılığı (1-5)", 1, 5, 5)
            with col_p2:
                p_rapor = st.slider("4. Raporların Detaylılığı ve Kök Neden Kalitesi (1-5)", 1, 5, 5)
                p_mesleki = st.slider("5. Mesleki Hazırbulunuşluğa Katkısı (1-5)", 1, 5, 5)

            uygulama_begeni = st.text_area("✅ En Çok Beğendiğiniz Özellikler:")
            uygulama_oneri = st.text_area("💡 Geliştirilmesi İçin Önerileriniz:")

            if st.button("📨 Uygulama Değerlendirme Geri Bildirimini Kaydet", use_container_width=True):
                if not uygulama_begeni.strip() and not uygulama_oneri.strip():
                    st.warning("Lütfen değerlendirme alanlarını doldurunuz.")
                else:
                    st.session_state.uygulama_degerlendirmeleri.append({
                        "Tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                        "Aday": st.session_state.get("ogretmen_adi", "Aday"),
                        "Ortalama Memnuniyet": round((p_ortam + p_mufredat + p_ses + p_rapor + p_mesleki) / 5.0, 2),
                        "Beğenilenler": uygulama_begeni.strip(),
                        "Öneriler": uygulama_oneri.strip(),
                    })
                    st.success("🎉 Geri bildiriminiz kaydedildi!")

        if st.session_state.uygulama_degerlendirmeleri:
            st.markdown("#### 📊 Uygulama Hakkındaki Değerlendirme Kayıtları")
            st.dataframe(pd.DataFrame(st.session_state.uygulama_degerlendirmeleri), use_container_width=True, hide_index=True)

    st.divider()
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("➕ 3B Sınıfa Dön ve Yeni Senaryo Uygula", use_container_width=True):
            st.session_state.adim = 2
            st.rerun()
    with col_b2:
        tum_rapor_json = json.dumps(
            {
                "aday": st.session_state.get("ogretmen_adi"),
                "ortalama_puan": ortalama_puan,
                "oturumlar": [
                    {k: v for k, v in o.items() if k != "ses_dosyasi"}
                    for o in st.session_state.simulasyon_gecmisi
                ],
                "uygulama_degerlendirmeleri": st.session_state.uygulama_degerlendirmeleri,
            },
            ensure_ascii=False,
            indent=2,
        )
        st.download_button(
            label="📥 Tüm Raporları İndir (JSON)",
            data=tum_rapor_json,
            file_name=f"TYMM2026_Rapor_{st.session_state.get('okul_numarasi', 'Aday')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_b3:
        if st.button("🔄 Simülasyonu Baştan Başlat", use_container_width=True):
            st.session_state.simulasyon_gecmisi = []
            st.session_state.adim = 1
            st.rerun()
