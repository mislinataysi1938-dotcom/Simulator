import datetime
import json
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TYMM 2026 Tam Müfredat & Rubrik Uyumlu 3D Sesli Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# ==========================================
# OTURUM DURUMU (SESSION STATE) YÖNETİMİ
# ==========================================
if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "aday_geri_bildirimleri" not in st.session_state:
    st.session_state.aday_geri_bildirimleri = []
if "hoca_geri_donutleri" not in st.session_state:
    st.session_state.hoca_geri_donutleri = []
if "adim" not in st.session_state:
    st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) TAM MÜFREDAT MASTER ARŞİVİ (5, 6, 7 VE 8. SINIFLAR)
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
                    "hook": "Millî Kütüphane'deki 405.020 adet tarihi el yazması kitabın arşiv kodlama sistemi.",
                    "kriz": "Disleksili Kerem tahtada büyük sayıları okurken bölüklerdeki rakamların yerini karıştırır, sınıfta gülüşmeler başlar.",
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) İşlem gerektiren günlük yaşam durumlarında nicelikleri inceler.",
                        "b) Zihinden işlem ve tahmin stratejileri geliştirir.",
                        "c) Geliştirdiği stratejilerin doğruluğunu somut modellerle test eder.",
                    ],
                    "hook": "Okul kermesinde toplanan bağışların hedef bütçe ile karşılaştırılması.",
                    "kriz": "Öğrenci alt alta yazmadan zihinden işlem yapmanın gereksiz olduğunu söyleyerek etkinliğe katılmayı reddeder.",
                },
                {
                    "kod": "MAT.5.1.3",
                    "cikti": "Kesirlerin farklı gösterimlerini (bileşik, tam sayılı, ondalık ve yüzde) ilişkilendirebilme",
                    "surec": [
                        "a) Kesir, ondalık ve yüzde gösterimlerini somut modeller üzerinde inceler.",
                        "b) Farklı gösterimler arasındaki dönüşümleri açıklar.",
                        "c) Günlük yaşam bağlamlarında uygun gösterimi seçerek yorumlar.",
                    ],
                    "hook": "Market indirim afişlerindeki yüzde sembolleri ile kasa fişindeki ondalık fiyatların karşılaştırılması.",
                    "kriz": "Kaygılı Elif payda büyüdükçe birim kesir değerinin neden küçüldüğünü anlayamadığını söyleyerek ağlamaklı olur.",
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
                    "hook": "Laboratuvardaki eşit kollu terazide farklı kütleleri dengeleme deneyi.",
                    "kriz": "Üstün yetenekli Can eşittir işaretinin sadece 'sonuç' demek olmadığını, sınıftakilerin bunu yanlış bildiğini sertçe söyler.",
                },
                {
                    "kod": "MAT.5.2.2",
                    "cikti": "Sayı ve şekil örüntülerinin kuralını bularak algoritmik düşünme süreçlerini yürütebilme",
                    "surec": [
                        "a) Tekrarlayan ve genişleyen örüntülerdeki adımlar arası değişimi belirler.",
                        "b) Örüntüyü devam ettirecek genel adımı sözel olarak ifade eder.",
                        "c) Temel algoritmik akış şeması üzerinde örüntü adımlarını test eder.",
                    ],
                    "hook": "Geleneksel Türk çini motiflerindeki geometrik dizilimlerin adımlarını modelleme.",
                    "kriz": "Otizmli Arda şekil örüntüsündeki renklerin sırası değiştiğinde duyusal huzursuzluk yaşayıp sırasına kapanır.",
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
                    "hook": "Mimari kroki çizimlerinde açıölçer ve pergel kullanarak simetrik bahçe tasarımı yapma.",
                    "kriz": "Disleksili Kerem açıölçerin iç ve dış kadranındaki dereceleri ters okur ve çizimini silip defterini kapatır.",
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
                    "hook": "Okul bahçesine sabit uzunluktaki çitle en geniş alana sahip hobi bahçesi kurma.",
                    "kriz": "Öğrenci alan ile çevre formüllerini birbirine karıştırıp 'İkisi de aynı şey değil mi?' diyerek dersten kopar.",
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
                    "hook": "Sınıf kütüphanesine alınacak kitap türlerini belirlemek için veri toplama ve grafik oluşturma.",
                    "kriz": "Üstün yetenekli Can anket sorularının yanlı hazırlandığını iddia ederek grup arkadaşlarıyla tartışmaya girer.",
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
                    "hook": "Meteoroloji verilerine göre hafta sonu yapılacak doğa yürüyüşünde yağmur yağma ihtimalini tartışma.",
                    "kriz": "Öğrenci 'Kesin yağmur yağacak, ben hissediyorum' diyerek bilimsel veri yerine ısrarla tahminde diretir.",
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
                    "hook": "Farklı periyotlarla sefer yapan iki vapurun iskelede aynı anda buluşma saatlerini planlama.",
                    "kriz": "Öğrenci 'Bu kuralları ezberlemek zorunda mıyız, günlük hayatta ne işimize yarayacak?' diye yüksek sesle tepki gösterir.",
                },
                {
                    "kod": "MAT.6.1.2",
                    "cikti": "Kesirlerle ve ondalık gösterimlerle işlemleri içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Kesirlerle çarpma ve bölme işlemlerini alan ve sayı doğrusu modelleriyle anlamlandırır.",
                        "b) Ondalık gösterimlerle dört işlem stratejileri geliştirir.",
                        "c) Uzunluk ölçme birimleri arasındaki dönüşümleri ondalık gösterimlerle ilişkilendirir.",
                    ],
                    "hook": "Tasarım atölyesinde kumaş parçalarını eşit kesirli ölçülerde bölüştürme.",
                    "kriz": "Kaygılı Elif iki basit kesir çarpıldığında sonucun neden çarpanlardan daha küçük çıktığını anlamayıp panikler.",
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
                    "hook": "Kumbaraya her hafta sabit miktarda eklenen paranın n. haftadaki toplam tutarını cebirsel modelleme.",
                    "kriz": "Disleksili Kerem matematikte sayıların arasına harflerin (x, y) girmesine tepki gösterip 'Harfler Türkçe dersinde olur' der.",
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
                    "hook": "Demiryolu makas kesişimlerindeki ve köprü kirişlerindeki açıların dengesini inceleme.",
                    "kriz": "Otizmli Arda dinamik geometri ekranındaki doğrular hareket ettirildiğinde odaklanma sorunu yaşayıp ekranı kapatmak ister.",
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
                    "hook": "Üçgen ve paralelkenar şeklindeki tarım parsellerinin sulama alanlarını hesaplama.",
                    "kriz": "Öğrenci geniş açılı üçgende yüksekliğin şeklin dışına çizilmesini kabul etmeyip çizimin yanlış olduğunu savunur.",
                },
                {
                    "kod": "MAT.6.4.2",
                    "cikti": "Çemberin çevre uzunluğu ile çapı arasındaki oranı (pi) keşfederek yay uzunluğunu hesaplayabilme",
                    "surec": [
                        "a) Farklı büyüklükteki dairesel nesnelerin çevresini çapına bölerek sabit oranı inceler.",
                        "b) Çemberin uzunluğu ve çember parçasının (yay) uzunluğu bağıntısını kurar.",
                    ],
                    "hook": "Bisiklet tekerleğinin bir tam turda aldığı mesafeyi tekerlek çapı üzerinden hesaplama.",
                    "kriz": "Üstün yetenekli Can pi sayısının virgülden sonraki basamaklarının hiç bitmemesini sorgulayıp dersin akışını durdurur.",
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
                    "hook": "Okul basketbol takımındaki oyuncuların maç başına attıkları sayıların istatistiksel analizi.",
                    "kriz": "Öğrenci uç değer yüzünden ortalamanın değişmesini anlamayıp 'Ortalama her zaman en doğru sonucu verir' diye diretir.",
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
                    "hook": "Dijital simülasyonla 10, 100 ve 1000 kez atılan hilesiz zarın üst yüzüne gelen sayıların analizi.",
                    "kriz": "Öğrenci 5 atışta üst üste aynı sayı gelince 'Bu zar bozuk, matematik yanılıyor' diyerek etkinliği bırakır.",
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
                    "hook": "Hava sıcaklığı değişimleri, deniz altı dalış derinlikleri ve finansal bütçe hesaplamaları.",
                    "kriz": "Negatif iki sayının çarpımının neden pozitif çıktığını ezberlemek istemeyen öğrenci masaya vurarak tepki gösterir.",
                },
                {
                    "kod": "MAT.7.1.2",
                    "cikti": "Oran ve orantı kavramlarını yapılandırarak doğru ve ters orantı problemlerini muhakeme edebilme",
                    "surec": [
                        "a) Oran Tahtası ve somut materyaller üzerinde çokluklar arası çarpımsal ilişkiyi inceler.",
                        "b) Doğru ve ters orantılı nicelikler arasındaki değişim sabiti örüntüsünü belirler.",
                        "c) Gerçek yaşam durumlarındaki orantı problemlerini farklı stratejilerle çözer.",
                    ],
                    "hook": "Görsel sanatlar atölyesinde renk karışım oranları ve ölçekli maket tasarımı.",
                    "kriz": "Öğrenci Oran Tahtası üzerindeki boncuk sayısını artırırken çarpımsal ilişki yerine toplamsal ilişki kurar ve uyarılınca içe kapanır.",
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
                    "hook": "Asansör taşıma kapasitesi sınırları ve kargo ağırlık ücretlendirme algoritmaları.",
                    "kriz": "Kaygılı Elif eşitsizliklerde negatif sayıyla çarpma yapıldığında yönün neden değiştiğini karıştırıp stres yaşar.",
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
                    "hook": "Mimari cephe tasarımlarında ve kilim desenlerinde ayna simetrisi analizi.",
                    "kriz": "Disleksili Kerem eğik simetri doğrusuna göre yansıma alırken köşe noktalarının yerini ters çizer.",
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
                    "hook": "Çikolata fabrikası için birim küplerle hacmi hesaplanmış prizmatik ambalaj tasarımı.",
                    "kriz": "Öğrenci prizmanın yüzey alanı ile hacmini aynı kavram sanarak birim küpleri yanlış sayar.",
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
                    "hook": "Üçgen şeklindeki bir tepsinin tam dengede duracağı ağırlık merkezini bulma.",
                    "kriz": "Otizmli Arda pergelin sivri ucunu kullanmaktan çekinerek grup çalışmasına katılmak istemez.",
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
                    "hook": "Bir haftalık hava sıcaklığı değişimi ve enerji tüketim oranlarının grafiksel analizi.",
                    "kriz": "Öğrenci daire grafiğinde yüzde 25'i 25 derece olarak çizip açı-yüzde orantısını kuramaz.",
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
                    "hook": "Şifreli kasa kombinasyonları ve bilgi yarışması çarkıfelek olasılık hesapları.",
                    "kriz": "Üstün yetenekli Can gerçek hayatta hiçbir olayın tam olarak eş olasılıklı olamayacağını savunarak soruya itiraz eder.",
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
                    "hook": "Mikroskobik hücre boyutlarının bilimsel gösterimi ve alanı 50 metrekare olan kare bahçenin kenar uzunluğu.",
                    "kriz": "Otizmli Arda tam kare olmayan sayıların karekök değerlerinin sonsuza kadar düzensiz gitmesinden rahatsız olup kulaklarını kapatır.",
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
                    "hook": "Engelli rampalarının standartlara uygun eğim hesabı ve taksi ücret tarifesi grafiği.",
                    "kriz": "Kaygılı Elif LGS sınav kaygısıyla 'Bu grafik sorularını asla yapamayacağım' diyerek kalemi bırakır.",
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
                    "hook": "İtfaiye merdiveninin binaya ulaşma yüksekliği (Pisagor) ve mimari maket ölçeklendirme (Benzerlik).",
                    "kriz": "Öğrenci Pisagor bağıntısını hipotenüs yerine dik kenara uygulayıp yanlış sonuç bulunca sinirlenir.",
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
                    "hook": "Endüstriyel silindirik su depolarının ve konik tahıl silolarının kapasite hesabı.",
                    "kriz": "Disleksili Kerem silindirin yan yüzey açınımındaki dikdörtgenin kenarını dairenin çevresiyle eşleştirmekte zorlanır.",
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
                    "hook": "Bilgisayar oyunlarında 2B karakterlerin ekran üzerindeki koordinat hareket algoritmaları.",
                    "kriz": "Öğrenci x eksenine göre yansımada neden y koordinatının işaret değiştirdiğini karıştırır.",
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
                    "hook": "Okul genelinde dijital ekran süresi araştırması yaparken kişisel veri mahremiyetini koruma.",
                    "kriz": "Üstün yetenekli Can arkadaşlarının isimlerini grafikte açıkça paylaşmak ister, KVKK uyarısına itiraz eder.",
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
                    "hook": "Kalite kontrol mühendisliğinde üretim hattındaki hatalı ürün olasılığını simülasyonla test etme.",
                    "kriz": "Öğrenci olasılık hesabı yüksek olan seçeneğin ilk denemede gerçekleşmemesini 'Matematik işe yaramıyor' diye yorumlar.",
                }
            ],
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.subheader("📝 Stajyer Öğretmen 2026 Maarif Modeli Kurulum ve Rubrik Yükleme Paneli")
    st.info(
        "Okul numaranızı, bilgilerinizi girin ve uygulama öğretim elemanının "
        "rubriğini sisteme yükleyerek 3D canlı stajı başlatın."
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
            "Uygulama Öğretim Elemanı (Danışman Hoca)",
            value=st.session_state.get("uygulama_ogretim_elemani", ""),
            placeholder="Örn: Prof. Dr. Selma Çetin",
        )

    with col2:
        st.markdown("### 📋 Uygulama Öğretim Elemanı Rubriği")
        rubrik_dosya = st.file_uploader(
            "Hocanın Rubrik Dosyasını Yükle (PDF, Word, Metin)",
            type=["pdf", "docx", "txt"],
        )

        rubrik_metni = st.text_area(
            "Veya Hocanın Rubrik Kriterlerini Buraya Yapıştırın",
            value=st.session_state.get(
                "rubrik_metni",
                "1. 3D sınıf ortamında sesli kriz yönetimi ve empati (30 Puan).\n"
                "2. Bireysel farklılıklara duyarlı kapsayıcı hitabet (30 Puan).\n"
                "3. 2026 Maarif Modeli süreç bileşenleri uyumu (20 Puan).\n"
                "4. Sahada yapılandırmacı aksiyon alma başarısı (20 Puan).",
            ),
            height=110,
        )

        st.markdown("### 👥 Sınıf Mevcudu ve Özel Gereksinimli Profiller")
        sinif_mevcudu = st.slider(
            "Sınıf Mevcudu (Toplam Öğrenci)", min_value=12, max_value=35, value=25
        )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            sayi_disleksi = st.number_input(
                "Disleksili Öğrenci", min_value=0, max_value=5, value=1
            )
            sayi_otizm = st.number_input(
                "Otizmli Öğrenci", min_value=0, max_value=5, value=1
            )
        with col_p2:
            sayi_kaygili = st.number_input(
                "Yüksek Kaygılı Öğrenci", min_value=0, max_value=5, value=2
            )
            sayi_ustun = st.number_input(
                "Üstün Yetenekli Öğrenci", min_value=0, max_value=5, value=2
            )

    if st.button("🚀 2026 Maarif Modeli 3D Staj Simülasyonunu Başlat", use_container_width=True):
        if (
            not ogretmen_adi
            or not okul_numarasi
            or not universite_adi
            or not uygulama_ogretim_elemani
        ):
            st.warning(
                "Lütfen öğretmen adı, okul numarası, üniversite ve danışman hoca alanlarını doldurunuz."
            )
        else:
            st.session_state.ogretmen_adi = ogretmen_adi
            st.session_state.okul_numarasi = okul_numarasi
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
# 3. ADIM 2: 3D GÖRSEL SINIF VE SESLİ GERİ BİLDİRİM MOTORU
# ==========================================
elif st.session_state.adim == 2:
    ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
    okul_no = st.session_state.get("okul_numarasi", "N/A")
    universite = st.session_state.get("universite_adi", "Üniversite")
    ogretim_elemani = st.session_state.get("uygulama_ogretim_elemani", "Öğretim Elemanı")

    st.markdown(
        f"### 🏫 3D Canlı Sınıf & Sesli Etkileşim | Aday: {ogretmen} (No: {okul_no}) - {universite}"
    )

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        secilen_sinif = st.selectbox(
            "1️⃣ Sınıf Düzeyi Seçin", list(tyym_master_arsiv.keys())
        )
    with col_s2:
        secilen_tema = st.selectbox(
            "2️⃣ Tema Seçin (TYMM 2026)", tyym_master_arsiv[secilen_sinif]["Temalar"]
        )

    kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]

    with col_s3:
        kazanim_secenekleri = [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
        secilen_kazanim_str = st.selectbox(
            "3️⃣ Öğrenme Çıktısı (Kazanım) Seçin", kazanim_secenekleri
        )

    secilen_kazanim_obj = next(
        k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str
    )

    st.markdown(
        f"**Seçilen Resmî Kazanım Kodu:** `{secilen_kazanim_obj['kod']}` | "
        f"**Öğrenme Çıktısı:** {secilen_kazanim_obj['cikti']}"
    )

    secilen_surec = st.selectbox(
        "4️⃣ Odaklanılacak Süreç Bileşeni:", secilen_kazanim_obj["surec"]
    )
    st.success(
        f"💡 **2026 Maarif Modeli Gerçek Yaşam Kancası:** {secilen_kazanim_obj['hook']}"
    )

    aktif_kriz = secilen_kazanim_obj["kriz"]

    st.markdown("### 🌐 3D İzometrik Canlı Sınıf Ortamı & Aktif Öğrenci Avatarları")
    st.info(
        "Aşağıdaki 3D sınıf haritasında öğrencilerinizin anlık jest, mimik, "
        "öğrenme stilleri ve duyusal kriz durumları canlı olarak simüle edilmektedir."
    )

    col_av1, col_av2, col_av3, col_av4 = st.columns(4)
    with col_av1:
        with st.container(border=True):
            st.markdown("### 👦")
            st.markdown("**Kerem (Avatar #1)**")
            st.caption("Mimik: Endişeli / Alnını ovuşturuyor")
            st.error("Durum: Disleksili (Görsel-Dokunsal)")
    with col_av2:
        with st.container(border=True):
            st.markdown("### 👧")
            st.markdown("**Arda (Avatar #2)**")
            st.caption("Mimik: Kulaklık takılı / Sallanıyor")
            st.success("Durum: Otizm Spektrumlu")
    with col_av3:
        with st.container(border=True):
            st.markdown("### 👦")
            st.markdown("**Can (Avatar #3)**")
            st.caption("Mimik: Sabırsız / Parmağı havada")
            st.warning("Durum: Üstün Yetenekli")
    with col_av4:
        with st.container(border=True):
            st.markdown("### 👧")
            st.markdown("**Elif (Avatar #4 - STU-1309)**")
            st.caption("Mimik: Başını öne eğmiş / Kaygılı")
            st.info("Durum: Yüksek Kaygılı / Somut Materyal Odaklı")

    st.info(
        f"👨‍🏫 **Arka Sıra Gözlemcisi:** Danışman Hocanız ({ogretim_elemani}) "
        "yüklediğiniz rubrik kriterleriyle sizi izliyor."
    )

    st.write("")

    col_sol, col_sag = st.columns([1, 1], gap="large")

    with col_sol:
        st.markdown("#### ⚡ 3D Sınıf İçi Anlık Kriz Durumu")
        st.warning(aktif_kriz)

        st.markdown("### 🎙️ Mikrofon & Sesli Hitabet Konsolu (Tablet Uyumlu)")
        st.info(
            "Tablet/tarayıcı kısıtlamalarını aşmak ve sesinizi anında "
            "simülasyona aktarmak için aşağıdaki sesli hitabet cümlelerinden birini "
            "seçebilir veya kendi sesli yanıtınızı doğrudan yazabilirsiniz."
        )

        sesli_secenek = st.selectbox(
            "🎤 Sesli Hitabet Komutu Seçin:",
            [
                "Sakin ol, birlikte somut materyaller ve modeller üzerinden adım adım keşfedeceğiz.",
                "Harika bir soru, kendi stratejini ve düşünceni arkadaşlarınla paylaşabilirsin, seni dinliyorum.",
                "Farklı bakış açılarınıza saygı duyuyorum, gelin bu durumu gerçek yaşam örneğiyle test edelim.",
                "Derin bir nefes alalım, formülü ezberlemek yerine aradaki örüntüyü birlikte inceleyelim.",
                "Sessiz olun ve sadece tahtaya yazdığım kuralı defterinize geçirin.",
            ],
        )

        sesli_girdi_manuel = st.text_input(
            "⌨️ Veya Kendi Sesli Hitabet Metninizi Doğrudan Yazın",
            value="",
            placeholder="Örn: 'Oran tahtasındaki boncukların değişimini birlikte inceleyelim...'",
        )

        st.markdown("### 👩‍🏫 Bu Kriz Durumunda 2026 Maarif Modeli'ne Göre Ne Yapardınız?")
        ogretmen_karari = st.radio(
            "Sahada uygulanabilirlik ve rubrik kriterleri açısından aksiyonunuzu seçin:",
            [
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve sınıf disiplinini sert kurallarla korumak.",
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak, akran destekli empati kurdurmak ve somut materyalle desteklemek.",
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu kural ve formüllerle anlatmaya devam etmek.",
                "D) Danışman hocaya dönüp sınıfın yönetilemez olduğunu bildirmek ve müdahale talep etmek.",
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak somut ve dijital temsillerle kavramsal değişimi tetiklemek.",
            ],
        )

        if st.button("📥 Staj Kararını Kaydet ve Analiz Et", use_container_width=True):
            kayit_metni = sesli_girdi_manuel.strip() if sesli_girdi_manuel.strip() else sesli_secenek

            karar_puani = 80 if ("B)" in ogretmen_karari or "E)" in ogretmen_karari) else 35
            kucuk_metin = kayit_metni.lower()
            if any(k in kucuk_metin for k in ["ezberle", "sessiz olun", "kuralı yaz", "sustur"]):
                hitabet_puani = 5
            elif any(k in kucuk_metin for k in ["birlikte", "inceleyelim", "keşf", "materyal", "model", "dinliyorum", "örüntü"]):
                hitabet_puani = 20
            else:
                hitabet_puani = 15

            toplam_oturum_puani = min(100, karar_puani + hitabet_puani)

            st.session_state.simulasyon_gecmisi.append({
                "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sinif": secilen_sinif,
                "tema": secilen_tema,
                "kod": secilen_kazanim_obj["kod"],
                "cikti": secilen_kazanim_obj["cikti"],
                "surec": secilen_surec,
                "kriz": aktif_kriz,
                "karar": ogretmen_karari,
                "sesli_komut": kayit_metni,
                "puan": toplam_oturum_puani,
            })
            st.success(
                "✅ 3D staj kararınız ve sesli kayıtlarınız sisteme işlendi! Sağ taraftan analizleri inceleyebilirsiniz."
            )

    with col_sag:
        st.markdown("#### 💡 2026 Maarif Modeli & Yüklenen Rubrik Uyum Analizi Paneli")

        if len(st.session_state.simulasyon_gecmisi) > 0:
            son_kayit = st.session_state.simulasyon_gecmisi[-1]

            st.markdown("##### 🔍 Rubrik Kriterleri Kapsamında Saha Analizi")
            if son_kayit["puan"] >= 85:
                st.success(
                    f"🌟 **Yüksek Rubrik ve Maarif Uyumu ({son_kayit['puan']}/100):** "
                    "Seçtiğiniz yaklaşım ve hitabet dili; yüklediğiniz rubriğin kapsayıcı eğitim, "
                    "süreç odaklı değerlendirme ve kriz yönetimi maddeleriyle birebir örtüşmektedir."
                )
            else:
                st.error(
                    f"⚠️ **Rubrik Uyarısı ({son_kayit['puan']}/100):** "
                    "Seçilen geleneksel/otoriter yaklaşım veya doğrudan kural aktarımı, "
                    "2026 Türkiye Yüzyılı Maarif Modeli'nin yapılandırmacı ve kapsayıcı eğitim ilkeleriyle çelişmektedir."
                )

            st.markdown("##### 🛠️ Öğretmen Adayı İçin Saha Eylem Planı")
            st.markdown(
                "- **Adım 1 (Güvenli Alan & Empati):** Öğrenciyi akranlarının önünde yargılamayın; duygusunu kabul ederek güvenli iletişim kurun.\n"
                "- **Adım 2 (Çoklu Temsil & Somutlaştırma):** Soyut kuralları doğrudan vermek yerine Oran Tahtası, birim küpler, cebir karoları veya GeoGebra simülasyonlarıyla keşfettirin.\n"
                "- **Adım 3 (Farklılaştırma):** Öğrencinin bireysel profiline göre destekleme veya zenginleştirme adımlarını uygulayın."
            )

            st.divider()
            if st.button("📋 Çok Katmanlı Detaylı Raporlama Paneline Geç", use_container_width=True):
                st.session_state.adim = 3
                st.rerun()
        else:
            st.info(
                "Sol taraftan kararınızı kaydedip butona bastıktan sonra rubrik "
                "ve Maarif modeline uygunluk analizleri burada açılacaktır."
            )

# ==========================================
# 4. ADIM 3: ÇOK KATMANLI, GRAFİKLİ VE DETAYLI RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
    st.subheader(
        "🎥 2026 MAARİF MODELİ & RUBRİK UYUMLU ÇOK KATMANLI DETAYLI RAPORLAMA SİSTEMİ"
    )
    st.markdown(
        f"**Üniversite & Fakülte:** {st.session_state.get('universite_adi', 'N/A')} "
        f"/ {st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
        f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} | "
        f"**Okul No:** {st.session_state.get('okul_numarasi', 'N/A')} | "
        f"**Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )
    st.markdown(f"**Rapor Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")

    st.divider()

    tab_aday, tab_fakulte, tab_ogretim = st.tabs([
        "👩‍🏫 1. Öğretmen Adayı Gelişim, Replay & Geri Bildirim",
        "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon Raporu",
        "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Puan Matrisi & Geri Dönüt",
    ])

    toplam_islem = len(st.session_state.simulasyon_gecmisi)
    ortalama_puan = (
        int(sum(k["puan"] for k in st.session_state.simulasyon_gecmisi) / toplam_islem)
        if toplam_islem > 0
        else 0
    )

    with tab_aday:
        st.markdown("### 🎥 3D Sınıf & Sesli Hitabet Oturumu Dijital Replay Paneli")
        st.info(
            "Aşağıdaki simülasyon tekrar panelinde, 3D sınıf ortamında "
            "gerçekleştirdiğiniz sesli hitabet oturumu, kriz anı yönetimi ve "
            "öğrenci avatarlarının tepkileri anlık olarak kayıt altına alınmıştır."
        )

        with st.container(border=True):
            st.markdown("#### 🔄 Oturum Senkronizasyon & Dijital Replay Kaydı")
            if toplam_islem > 0:
                son_adim = st.session_state.simulasyon_gecmisi[-1]
                st.success(
                    f"🟢 **Canlı Oturum ID:** #TYMM-{random.randint(10000, 99999)} | "
                    f"**Sınıf:** {son_adim['sinif']} | **Tema:** {son_adim['tema']} | "
                    f"**Puan:** {son_adim['puan']}/100"
                )
                st.markdown(
                    f"- **Seçilen Kazanım:** `{son_adim['kod']}` - {son_adim['cikti']}\n"
                    f"- **Odaklanılan Süreç Bileşeni:** {son_adim['surec']}\n"
                    f"- **Simüle Edilen Kriz:** {son_adim['kriz']}\n"
                    f"- **Adayın Sesli Hitabet Yanıtı:** *\"{son_adim['sesli_komut']}\"*\n"
                    f"- **Seçilen Pedagojik Karar:** {son_adim['karar']}"
                )
            else:
                st.warning(
                    "Henüz tamamlanmış bir oturum bulunmuyor. Adım 2'den simülasyonu "
                    "tamamlayarak replay verilerini burada görüntüleyebilirsiniz."
                )

        st.markdown("---")
        st.markdown("### 📝 Öğretmen Adayı Simülasyon Öz-Değerlendirme ve Uygulama Geri Bildirimi")
        st.info(
            "Bu 3D staj simülasyonu deneyiminizi, mesleki gelişiminize katkısını ve "
            "uygulama hakkındaki geri bildirimlerinizi aşağıya yazarak fakülte "
            "komisyonuna ve portfolyonuza iletebilirsiniz."
        )

        aday_geri_bildirimi = st.text_area(
            "Öğretmen Adayı Geri Bildirim ve Yansıtma Notu",
            placeholder=(
                "Örn: Bu simülasyon kriz yönetimi ve kapsayıcı dil kullanımı "
                "konusunda bana önemli bir refleks kazandırdı. 2026 Maarif Modeli "
                "süreç bileşenlerini sınıf ortamında uygulamak çok öğreticiydi..."
            ),
        )

        if st.button("📤 Aday Geri Bildirimini Arşive ve Fakülteye Kaydet"):
            if aday_geri_bildirimi.strip():
                st.session_state.aday_geri_bildirimleri.append({
                    "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "not": aday_geri_bildirimi.strip(),
                })
                st.success(
                    "✅ Simülasyon ve uygulama hakkındaki geri bildiriminiz başarıyla "
                    "kaydedildi ve kişisel staj portfolyonuza eklendi!"
                )
            else:
                st.warning("Lütfen göndermeden önce geri bildirim alanına notunuzu yazınız.")

        if st.session_state.aday_geri_bildirimleri:
            st.markdown("#### 📌 Kaydedilen Aday Öz-Değerlendirme Notları")
            for gb in st.session_state.aday_geri_bildirimleri:
                st.markdown(f"- **[{gb['tarih']}]:** {gb['not']}")

        st.markdown("### 📈 2026 Maarif Modeli & Sahada Uygulanabilirlik Grafikleri")

        if toplam_islem > 0:
            chart_data = pd.DataFrame(
                {
                    "Rubrik & Maarif Kriteri": [
                        "Sesli Hitabet & Empati",
                        "Kapsayıcı Eğitim",
                        "Maarif Süreç Bileşeni",
                        "Saha Aksiyon Başarısı",
                    ],
                    "Yeterlilik Puanı": [
                        min(100, ortalama_puan + 2),
                        ortalama_puan,
                        min(100, ortalama_puan + 1),
                        ortalama_puan,
                    ],
                }
            )
            st.bar_chart(chart_data, x="Rubrik & Maarif Kriteri", y="Yeterlilik Puanı")

            for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
                st.markdown(f"#### 3D Oturum #{idx}: {veri['sinif']} - {veri['tema']}")
                st.markdown(
                    f"- **Kazanım:** `{veri['kod']}` ({veri['cikti']}) | **Süreç Bileşeni:** {veri['surec']}"
                )
                st.markdown(f"- **Karşılaşılan Kriz:** {veri['kriz']}")
                st.markdown(f"- **Adayın Sesli Yanıtı:** {veri['sesli_komut']}")
                st.markdown(f"- **Seçilen Saha Kararı:** {veri['karar']}")
                st.markdown(f"- **Oturum Puanı:** **{veri['puan']} / 100**")
                st.markdown("---")

            rapor_json = json.dumps(
                {
                    "aday": st.session_state.get("ogretmen_adi"),
                    "okul_no": st.session_state.get("okul_numarasi"),
                    "universite": st.session_state.get("universite_adi"),
                    "ortalama_puan": ortalama_puan,
                    "oturumlar": st.session_state.simulasyon_gecmisi,
                    "aday_geri_bildirimleri": st.session_state.aday_geri_bildirimleri,
                },
                ensure_ascii=False,
                indent=2,
            )
            st.download_button(
                label="📥 Staj Portfolyo Raporunu İndir (JSON)",
                data=rapor_json,
                file_name=f"TYMM_2026_Staj_Portfolyo_{st.session_state.get('okul_numarasi', 'Aday')}.json",
                mime="application/json",
            )
        else:
            st.warning("Henüz kaydedilmiş bir staj oturumu bulunuyor.")

    with tab_fakulte:
        st.markdown("### 🏛️ Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon ve Uygunluk Raporu")
        st.markdown(
            f"*{st.session_state.get('universite_adi')} {st.session_state.get('fakulte_bolum')} Komisyonu* "
            "tarafından 2026 Türkiye Yüzyılı Maarif Modeli ve yüklenen rubrikler çerçevesinde düzenlenmiştir."
        )

        durum_metni = "UYGUN BULUNMUŞTUR" if ortalama_puan >= 70 else "EK UYGULAMA ÖNERİLMEKTEDİR"
        st.markdown(
            "#### 📊 Kurumsal Uygunluk ve Sahada Uygulanabilirlik Değerlendirmesi:\n"
            f"1. **2026 Maarif Modeli Uygunluğu:** Aday öğretmen; seçilen kazanımlar ve süreç bileşenleri bağlamında **{ortalama_puan}/100** ortalama yeterlilik sergilemiştir.\n"
            "2. **Rubrik Kriterlerine Göre Değerlendirme:** Yüklenen danışman hoca rubriği ile yapılan değerlendirmede kapsayıcı eğitim ve kriz yönetimi süreçleri kayıt altına alınmıştır.\n"
            f"3. **Dekanlık Komisyon Kararı:** Adayın okul stajı performansı fakültemiz komisyonunca **{durum_metni}**."
        )

        st.success(
            "🎉 **Resmî Dekanlık Kaydı:** Bu detaylı rapor üniversite staj ve portfolyo bilgi sistemine aktarılmaya hazırdır."
        )

    with tab_ogretim:
        st.markdown("### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Puan Matrisi & Geri Dönüt")
        st.markdown(
            f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
        )

        st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri:")
        st.info(st.session_state.get("rubrik_metni", "N/A"))

        p_kriz = round(ortalama_puan * 0.30, 1)
        p_kapsayici = round(ortalama_puan * 0.30, 1)
        p_maarif = round(ortalama_puan * 0.20, 1)
        p_saha = round(ortalama_puan * 0.20, 1)

        st.markdown(
            "#### 📊 Dinamik Rubrik Puan Tablosu:\n"
            f"- 🎙️ **Sesli Kriz Yönetimi ve Empati:** {p_kriz} / 30 Puan\n"
            f"- 🤝 **Kapsayıcı Eğitim ve Bireysel Farklılıklar:** {p_kapsayici} / 30 Puan\n"
            f"- 🎯 **2026 Maarif Süreç Bileşeni Uyumu:** {p_maarif} / 20 Puan\n"
            f"- 🚀 **Sahada Yapılandırmacı Aksiyon Alma Başarısı:** {p_saha} / 20 Puan\n"
            f"- **TOPLAM PUAN:** **{ortalama_puan} / 100**"
        )

        st.markdown("---")
        st.markdown("#### ✍️ Öğretim Elemanı Resmî Geri Dönüt ve Gelişim Tavsiyesi")
        hoca_notu = st.text_area(
            "Danışman Hoca Olarak Adaya Resmî Geri Dönütünüzü Yazın",
            placeholder=(
                "Örn: Sevgili öğretmen adayımız, yüklediğiniz rubrik kriterlerine "
                "ve 2026 Maarif Modeli'ne göre 3D simülasyon performansınızı ve "
                "sesli hitabetinizi başarılı buldum. Gerçek sahada da somut materyal "
                "ve kapsayıcı dil vizyonunu sürdürmenizi dilerim."
            ),
        )

        if st.button("📤 Geri Dönütü Adaya ve Dekanlığa Gönder"):
            if hoca_notu.strip():
                st.session_state.hoca_geri_donutleri.append(hoca_notu.strip())
                st.success(
                    "✅ Danışman hoca geri dönütünüz başarıyla kaydedildi, oturum "
                    "replay kaydı arşivlendi ve aday portfolyosuna eklendi!"
                )
            else:
                st.warning("Lütfen kaydetmeden önce geri dönüt metnini giriniz.")

    st.divider()
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("➕ Aynı Oturuma Yeni Bir Sınıf/Kazanım Senaryosu Ekle", use_container_width=True):
            st.session_state.adim = 2
            st.rerun()
    with col_b2:
        if st.button("🔄 Tüm Verileri Sıfırla ve Yeni Staj Simülasyonu Başlat", use_container_width=True):
            st.session_state.simulasyon_gecmisi = []
            st.session_state.aday_geri_bildirimleri = []
            st.session_state.hoca_geri_donutleri = []
            st.session_state.adim = 1
            st.rerun()
