"""
TÜBİTAK 2209-A - TYMM Uyumlu 3B Matematik Sınıf Simülatörü Ana Arayüzü
Tek Dosya Modeli: Profil, Kazanım, Sentez Motoru ve Arayüz Tek Bir Dosyada Birleştirildi.
"""

import json
import hashlib
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. VERİ SÖZLÜKLERİ (ÖĞRENCİ PROFİLLERİ, KAZANIMLAR VE KURAL MOTORU)
# ==============================================================================

STUDENT_PROFILES = {
    "disleksi": {
        "ad": "Defne", "cinsiyet": "Kız", "profil": "Disleksi", "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Metin okuma ve sembolik harf/rakam karışıklığında hızlı yorulma ve çekinme",
        "kok_neden": "Okuma yükü ve sembol karmaşası nedeniyle bilişsel aşırı yüklenme yaşanması.",
        "uygun_materyal": "Kesir Çubukları",
        "materyaller": ["Kesir Çubukları", "Cebir Karoları", "Birim Küpler", "Oran Tahtası", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Duyuşsal yatıştırma ve okuma/metin yükünü azaltma": 12.5, "Yüksek sesle metni baştan okutma": 2.0, "Tahtaya kalkıp okumaya zorlama": 0.0},
        "ikinci_eylemler": {"Görsel modellemeye güvenli geçiş yapma": 12.5, "Uzun sözel yönergeyle soyut işlem isteme": 3.0, "Formül ezberletme": 1.0},
        "avatar_renk": "#4A90E2",
    },
    "otizm": {
        "ad": "Kerem", "cinsiyet": "Erkek", "profil": "Otizm Spektrumu", "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Ani ses, kalabalık gürültüsü ve belirsiz/soyut yönergelere karşı hassasiyet",
        "kok_neden": "Ani duyusal/çevresel değişim veya belirsizlik nedeniyle regülasyonun bozulması.",
        "uygun_materyal": "Oran Tahtası",
        "materyaller": ["Oran Tahtası", "Kesir Çubukları", "Birim Küpler", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Sakin, net ve öngörülebilir yatıştırma": 12.5, "Ani dokunma veya yüksek sesle uyarma": 0.0, "Soru yağmuruna tutma": 2.0},
        "ikinci_eylemler": {"Yapılandırılmış görsel eşleştirmeye geçme": 12.5, "Mecazlı ifadelerle soyut akıl yürütme isteme": 2.0, "Grup yarışmasına dahil etme": 1.0},
        "avatar_renk": "#50B89A",
    },
    "ustun_yetenek": {
        "ad": "Elif", "cinsiyet": "Kız", "profil": "Üstün Yetenek", "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Düşük bilişsel meydan okuma ve tekrarlı alıştırmalarda çabuk sıkılma",
        "kok_neden": "Bilişsel uyarım eksikliği ve düşük meydan okuma düzeyi.",
        "uygun_materyal": "Cebir Karoları",
        "materyaller": ["Cebir Karoları", "Birim Küpler", "Oran Tahtası", "Kesir Çubukları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Bilişsel potansiyeli genelleme/keşfe yönlendirme": 12.5, "Azarlayarak utandırma": 0.0, "Daha fazla rutin işlem verme": 3.0},
        "ikinci_eylemler": {"Alan modelinden genelleme/ispat kurgulatma": 12.5, "Mekanik işlem yaptırma": 3.0, "Görev vermeden boş bırakma": 1.0},
        "avatar_renk": "#9B59B6",
    },
    "yuksek_kaygi": {
        "ad": "Mert", "cinsiyet": "Erkek", "profil": "Yüksek Matematik Kaygısı", "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Zaman baskısı ve yanlış yapma korkusuyla donma/geri çekilme",
        "kok_neden": "Başarısızlık ve değerlendirilme kaygısına bağlı donma tepkisi.",
        "uygun_materyal": "Birim Küpler",
        "materyaller": ["Birim Küpler", "Kesir Çubukları", "Oran Tahtası", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Zaman baskısını kaldırıp hatayı normalleştirme": 12.5, "'Çok kolay' diyerek küçümseme": 0.0, "Süreyi kısaltıp hızlandırma": 1.0},
        "ikinci_eylemler": {"Küçük, risksiz adımlarla somut model kurma": 12.5, "Anında puan baskısı kurma": 2.0, "Doğrudan denklem yazdırma": 3.0},
        "avatar_renk": "#E67E22",
    },
    "mukemmeliyetcilik": {
        "ad": "Zeynep", "cinsiyet": "Kız", "profil": "Mükemmeliyetçilik", "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Kusursuzluk beklentisi ve küçük hatalarda yüksek hayal kırıklığı",
        "kok_neden": "Kusursuzluk beklentisi ve hatayı kişisel yetersizlik olarak görme.",
        "uygun_materyal": "İki Renkli Sayma Pulları",
        "materyaller": ["İki Renkli Sayma Pulları", "Birim Küpler", "Cebir Karoları", "Oran Tahtası", "Kesir Çubukları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Kusursuz olma baskısını düşüren yaklaşım": 12.5, "Eleştirme": 0.0, "Müdahale etmeden izleme": 3.0},
        "ikinci_eylemler": {"Adım adım kurgulama": 12.5, "Tek bir 'doğru' kalıba sıkıştırma": 3.0, "Soyut kuralı ezberletme": 2.0},
        "avatar_renk": "#E91E63",
    },
    "davranis_bozuklugu": {
        "ad": "Kaan", "cinsiyet": "Erkek", "profil": "Davranış Bozukluğu / Karşı Gelme", "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Otoriter buyruklara ve anlamsız görünen görevlere karşı direnç",
        "kok_neden": "Otoriteye karşı direnç, dışlanma algısı ve anlamlandırma güçlüğü.",
        "uygun_materyal": "GeoGebra 3B",
        "materyaller": ["GeoGebra 3B", "Cebir Karoları", "Oran Tahtası", "Birim Küpler", "Kesir Çubukları", "İki Renkli Sayma Pulları", "Simetri Aynası"],
        "ilk_eylemler": {"Güç mücadelesine girmeden sakin sınır koyma": 12.5, "Sınıf önünde bağırarak ceza verme": 0.0, "Görmezden gelip düzene izin verme": 2.0},
        "ikinci_eylemler": {"Dinamik değişimle somut ilişkiyi keşfettirme": 12.5, "Kuru kural dayatma": 2.0, "Sadece yazılı ceza verme": 1.0},
        "avatar_renk": "#C0392B",
    },
    "sosyal_ice_donukluk": {
        "ad": "Eylül", "cinsiyet": "Kız", "profil": "Sosyal İçe Dönüklük", "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Kalabalık önünde konuşma ve ani söz verilmesi durumunda çekinme",
        "kok_neden": "Sosyal etkileşim ve kalabalık önünde konuşma çekincesi.",
        "uygun_materyal": "Simetri Aynası",
        "materyaller": ["Simetri Aynası", "Birim Küpler", "GeoGebra 3B", "Kesir Çubukları", "Oran Tahtası", "Cebir Karoları", "İki Renkli Sayma Pulları"],
        "ilk_eylemler": {"Güvenli bireysel alan ve sakin iletişim kurma": 12.5, "Herkesin içinde konuşmaya zorlama": 0.0, "Hiç dahil etmeden bırakma": 3.0},
        "ikinci_eylemler": {"Bireysel keşif sonrası küçük paylaşım sunma": 12.5, "Ani sunum yapmaya zorlama": 2.0, "Sadece sözel tanım isteme": 3.0},
        "avatar_renk": "#16A085",
    },
    "asiri_hareketlilik": {
        "ad": "Aras", "cinsiyet": "Erkek", "profil": "Aşırı Hareketlilik / Dürtüsellik", "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Yüksek hareket enerjisi, beklemede zorlanma ve aceleyle yanıt verme",
        "kok_neden": "Dürtü kontrolü ve dikkat sürdürmede zorlanma; kinestetik enerji fazlalığı.",
        "uygun_materyal": "Birim Küpler",
        "materyaller": ["Birim Küpler", "GeoGebra 3B", "Oran Tahtası", "Kesir Çubukları", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası"],
        "ilk_eylemler": {"Kısa, somut ve yapılandırılmış hareket sınırı": 12.5, "Sert uyarı verme": 0.0, "Uzun ve karmaşık yönerge verme": 2.0},
        "ikinci_eylemler": {"Kontrollü inşa ve sayma adımlarına yönlendirme": 12.5, "Hız yarışı yaptırma": 2.0, "Açıklamasız formül verme": 2.0},
        "avatar_renk": "#D35400",
    },
    "sozel_ifade_guclugu": {
        "ad": "Miraç", "cinsiyet": "Erkek", "profil": "Sözel İfade Güçlüğü", "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Kavramı bilmesine karşın kelimeleri toparlama ve sözel aktarımda zorlanma",
        "kok_neden": "İfade edici dil ve kavram bulma güçlüğü.",
        "uygun_materyal": "Oran Tahtası",
        "materyaller": ["Oran Tahtası", "İki Renkli Sayma Pulları", "Kesir Çubukları", "Birim Küpler", "Cebir Karoları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {"Kelime bulma baskısını kaldıran yaklaşım": 12.5, "Cümlesini sabırsızlıkla tamamlama": 1.0, "Sadece uzun yazılı açıklama isteme": 2.0},
        "ikinci_eylemler": {"Görsel eşleştirmeyle gerekçelendirmeyi destekleme": 12.5, "Yalnızca soyut tanımla yetinme": 2.0, "Soruyu geri çekme": 1.0},
        "avatar_renk": "#2980B9",
    },
    "gorsel_uzamsal": {
        "ad": "Duru", "cinsiyet": "Kız", "profil": "Görsel / Uzamsal Öğrenme Ağırlığı", "sinif_duzeyi": "8. Sınıf",
        "duyusal_ozellik": "Uzamsal döndürme ve şekil ilişkilerinde güçlü kavrayış; soyut tabloda zorlanma",
        "kok_neden": "Sembolik-sözel sunum yerine uzamsal/görsel temsillerde daha yüksek verim alma.",
        "uygun_materyal": "GeoGebra 3B",
        "materyaller": ["GeoGebra 3B", "Simetri Aynası", "Birim Küpler", "Cebir Karoları", "Oran Tahtası", "Kesir Çubukları", "İki Renkli Sayma Pulları"],
        "ilk_eylemler": {"Uzamsal/görsel güçlü yönünü merkeze alan destek": 12.5, "Yalnızca formül tablosuna hapsetme": 2.0, "Kıyaslayıcı dil kullanma": 0.0},
        "ikinci_eylemler": {"Görsel-sembolik köprü kurma": 12.5, "Görsel inceleme yaptırmadan ezber verme": 3.0, "Tek yönlü anlatımla bırakma": 2.0},
        "avatar_renk": "#8E44AD",
    },
}

TYMM_28_OUTCOMES = {
    "5. Sınıf": [
        "Doğal sayılarla çok basamaklı işlemleri ve tahminleri ilişkilendirme",
        "Kesirlerle toplama ve çıkarma işlemlerini modellerle ilişkilendirme",
        "Ondalık gösterimlerle kesirler arasındaki ilişkiyi çözümleme",
        "Simetri ve geometrik örüntülerde dönüşüm ilişkilerini inceleme",
        "Çevre ve alan kavramlarını birim kareler/modellerle ilişkilendirme",
        "Veri toplama, düzenleme ve sütun grafiğiyle yorumlama",
        "Temel geometrik şekillerin özelliklerini sınıflandırma",
    ],
    "6. Sınıf": [
        "Oran ve orantı ilişkilerini somut temsillerle çözümleme",
        "Tam sayılarla toplama ve çıkarma işlemlerini modelleme",
        "Alan ve hacim ilişkilerini üç boyutlu modellerle inceleme",
        "Kesirlerle çarpma ve bölme işlemlerini modellerle açıklama",
        "Cebirsel ifadeleri sözel durumlarla ilişkilendirme",
        "Açılar ve çokgenlerde iç/dış açı ilişkilerini keşfetme",
        "Merkezi eğilim ve yayılımı veri setleri üzerinden yorumlama",
    ],
    "7. Sınıf": [
        "Cebirsel ifadelerde özdeşlik ve çarpanlara ayırma genellemeleri",
        "Doğrusal ilişkiler ve değişkenler arası değişimi yorumlama",
        "Olasılık ve veri analizinde örnek uzay ve oran yorumlama",
        "Rasyonel sayılarla işlemler ve çok adımlı problemler",
        "Eşlik ve temel geometrik dönüşümlerle ilişkiler kurma",
        "Dairenin çevresi ve daire diliminin alanını modelleme",
        "Prizma ve silindirin yüzey alanı ve hacmini ilişkilendirme",
    ],
    "8. Sınıf": [
        "Dönüşüm geometrisi, eşlik ve benzerlik ilişkileri",
        "Çarpanlara ayırma ve özdeşlikleri cebirsel/geometrik modelleme",
        "Doğrusal denklemler ve eğim kavramını bağlam içinde yorumlama",
        "Olasılık kavramını çıktı sayılarıyla ilişkilendirme",
        "Kareköklü ifadelerle işlemler ve yaklaşık değer bulma",
        "Üslü ifadeler ve bilimsel gösterimi çözümleme",
        "Geometrik cisimlerde kesit ve temel ölçü ilişkilerini inceleme",
    ],
}

# 28 Kazanım için Matematiksel Tema Çıkarım Sözlüğü
MATH_KEYWORDS = {
    "kesir": "pay, payda ve parça-bütün ilişkisi",
    "doğal sayı": "büyük sayılar, basamak değerleri ve işlemler",
    "ondalık": "virgüllü sayılar ve ondalık kısımlar",
    "simetri": "katlama, ayna ekseni ve yansıma",
    "çevre": "şeklin etrafı ve kenar uzunlukları toplamı",
    "alan": "yüzey kaplama ve birim kareler",
    "veri": "tablolar, grafikler ve istatistiksel sayımlar",
    "geometrik": "şekiller, köşeler, ayrıtlar ve yüzeyler",
    "oran": "iki çokluğun karşılaştırılması ve kat ilişkisi",
    "tam sayı": "artı-eksi işaretleri, borç-alacak ve sıfırın altı",
    "hacim": "üç boyutlu boşluk ve birim küpler",
    "cebirsel": "x, y gibi bilinmeyen değişkenler ve harfli ifadeler",
    "açı": "köşe açıklığı, dereceler ve iç/dış ilişkileri",
    "olasılık": "ihtimaller, kesinlik, imkansızlık ve şans",
    "rasyonel": "eksi kesirler ve rasyonel işlemler",
    "eşlik": "birebir aynı olma ve örtüşme",
    "dönüşüm": "öteleme (kaydırma) ve yansıma (çevirme)",
    "daire": "çember, yarıçap, pi ve yay uzunluğu",
    "prizma": "taban, yükseklik ve üç boyutlu cisimler",
    "çarpan": "ortak paranteze alma ve parçalama",
    "doğrusal": "eğim, diklik ve koordinat sistemi",
    "kareköklü": "kök içi, tam kare sayılar ve yaklaşık değer",
    "üslü": "tekrarlı çarpım, taban ve kuvvet",
}

EMPATIK_IFADELER = ["anladım", "birlikte", "yanındayım", "acele yok", "hata yapabilirsin", "normal", "güvendesin", "adım adım", "senin hızında", "haklısın"]
TYMM_SORGU_IFADELERI = ["neden", "nasıl", "ne fark", "ilişki", "örüntü", "tahmin", "gerekçe", "açıklar mısın", "ne gözlemledin", "genelleyebilir"]
YARGILAYICI_IFADELER = ["neden hala", "anlamadın", "arkadaşların çözdü", "yerine otur", "saçma", "beceriksiz", "çocukça", "sus", "içler dışlar"]
KURULUM_ANAHTARLARI = ["kurulum", "yerleştir", "hazırla", "aç", "temsil", "tanımla", "başla", "koy"]
MANIPULASYON_ANAHTARLARI = ["öğrenci", "birlikte", "hareket", "taşı", "ayır", "birleştir", "döndür", "uygula", "manipüle", "çek"]
SEMBOLIK_ANAHTARLARI = ["sembol", "ifade", "denklem", "oran", "kesir", "yaz", "ilişkilendir", "genelle", "kural"]


# ==============================================================================
# 2. MOTOR FONKSİYONLARI VE DIŞA AKTARIM MODÜLLERİ
# ==============================================================================

def uret_profil_kazanim_tepkisi(prof: dict, sinif_duzeyi: str, kazanim: str) -> dict:
    """
    Seçilen 28 kazanımdan herhangi birini analiz eder, matematiksel temasını bulur
    ve öğrenci profilinin kriziyle dinamik olarak sentezler.
    """
    kazanim_kisa = kazanim.lower()
    mat_konusu = "matematiksel işlemler" # varsayılan
    for key, desc in MATH_KEYWORDS.items():
        if key in kazanim_kisa:
            mat_konusu = desc
            break

    profil_adi = prof["profil"]
    ad = prof["ad"]

    if profil_adi == "Disleksi":
        ogrenci_sozu = f"Öğretmenim, '{kazanim}' konusundaki {mat_konusu} ile ilgili yazıları okurken satırlar birbirine giriyor. Sembolleri karıştırıyorum."
        kriz_durumu = f"{ad}, metin ve {mat_konusu} yoğunlaştığı için bilişsel yüklenme yaşayıp defterini kapatıyor."
    elif profil_adi == "Otizm Spektrumu":
        ogrenci_sozu = f"'{kazanim}' işlerken {mat_konusu} hakkında çok fazla ses ve belirsiz talimat var. Neyin önce yapılacağı net değil!"
        kriz_durumu = f"{ad}, {mat_konusu} etkinliğindeki ani duyusal değişim ve belirsizlikten dolayı kulaklarını kapatıp sallanıyor."
    elif profil_adi == "Üstün Yetenek":
        ogrenci_sozu = f"'{kazanim}' çok rutin. {mat_konusu} ile ilgili hep aynı alıştırmayı yapmak sıkıcı, bunun daha derin bir genellemesi yok mu?"
        kriz_durumu = f"{ad}, {mat_konusu} çalışmasında düşük meydan okuma nedeniyle sıkılıp alaycı yorumlar yaparak düzeni bozuyor."
    elif profil_adi == "Yüksek Matematik Kaygısı":
        ogrenci_sozu = f"Ya '{kazanim}' konusunda {mat_konusu} yaparken hata yaparsam? Süre de bitiyor, yapamayacağım galiba..."
        kriz_durumu = f"{ad}, {mat_konusu} etkinliğinde değerlendirilme kaygısıyla kalemini bırakıp donup kalıyor."
    elif profil_adi == "Mükemmeliyetçilik":
        ogrenci_sozu = f"'{kazanim}' çizimim kusursuz olmadı. {mat_konusu} tam istediğim gibi durmuyor, baştan yapmalıyım."
        kriz_durumu = f"{ad}, {mat_konusu} sırasında küçük bir hatayı yetersizlik olarak görüp kağıdı siliyor ve çalışmayı durduruyor."
    elif profil_adi == "Davranış Bozukluğu / Karşı Gelme":
        ogrenci_sozu = f"'{kazanim}' ne işime yarayacak ki? {mat_konusu} tamamen saçmalık, bunu yapmak istemiyorum!"
        kriz_durumu = f"{ad}, {mat_konusu} etkinliğinde otoriteye karşı gelerek materyali itiyor ve sınıfın dikkatini dağıtıyor."
    elif profil_adi == "Sosyal İçe Dönüklük":
        ogrenci_sozu = f"'{kazanim}' hakkında konuşmasam... {mat_konusu} için kendi kendime baksam olur mu?"
        kriz_durumu = f"{ad}, {mat_konusu} sırasında söz alma baskısı hissedince başını eğip sessizleşerek geri çekiliyor."
    elif profil_adi == "Aşırı Hareketlilik / Dürtüsellik":
        ogrenci_sozu = f"Ben buldum! {mat_konusu} böyle olacak, dur hemen şunu da yapayım!"
        kriz_durumu = f"{ad}, '{kazanim}' yönergesi bitmeden dürtüsel davranıp {mat_konusu} materyallerini hızla karıştırıyor."
    elif profil_adi == "Sözel İfade Güçlüğü":
        ogrenci_sozu = f"'{kazanim}' mantığını anladım, yani {mat_konusu} şöyle... kelimeler gelmiyor, çizerek anlatsam?"
        kriz_durumu = f"{ad}, {mat_konusu} üzerine düşünürken kelime bulmakta zorlanıp duraksıyor ve pes etme eğilimi gösteriyor."
    else:  # Görsel / Uzamsal Öğrenme Ağırlığı
        ogrenci_sozu = f"'{kazanim}' için tablodaki kural karışık. Ama {mat_konusu} kısmını şekilde görünce anlıyorum."
        kriz_durumu = f"{ad}, {mat_konusu} kavramını sembolik tabloda oturtamazken görsel materyali gördüğünde hızla kavramaya çalışıyor."

    return {
        "kaynak": "28 Kazanım x 10 Profil Zenginleştirilmiş Dinamik Motor",
        "kriz_durumu": kriz_durumu,
        "ogrenci_sozu": ogrenci_sozu,
        "uygun_materyal": prof["uygun_materyal"],
    }

def puanla_boyut2_materyal(secilen_materyal: str, dogru_materyal: str, aciklama: str):
    puan_secim = 12.5 if secilen_materyal == dogru_materyal else 5.0
    txt = (aciklama or "").lower().strip()
    asama_1 = any(k in txt for k in KURULUM_ANAHTARLARI)
    asama_2 = any(k in txt for k in MANIPULASYON_ANAHTARLARI)
    asama_3 = any(k in txt for k in SEMBOLIK_ANAHTARLARI)
    sayac = sum([asama_1, asama_2, asama_3])

    if len(txt) < 15 or sayac == 0: puan_aciklama = 2.0
    elif sayac == 1: puan_aciklama = 5.5
    elif sayac == 2: puan_aciklama = 9.0
    else: puan_aciklama = 12.5

    return round(min(25.0, puan_secim + puan_aciklama), 2), {"materyal_uyumu": "Tam uyumlu" if secilen_materyal == dogru_materyal else f"Alternatif (Önerilen: {dogru_materyal})", "kurulum": asama_1, "manipulasyon": asama_2, "sembolik": asama_3}

def puanla_boyut3_hitabet(sozlu_metin: str):
    txt = (sozlu_metin or "").lower().strip()
    empati = sum(1 for k in EMPATIK_IFADELER if k in txt)
    tymm = sum(1 for k in TYMM_SORGU_IFADELERI if k in txt)
    yargi = sum(1 for k in YARGILAYICI_IFADELER if k in txt)

    p1 = max(0.0, 8.0 - (yargi * 3.0)) if yargi > 0 else (21.0 if empati >= 2 else (14.0 if empati == 1 else 9.0))
    p2 = 21.0 if tymm >= 2 else (14.0 if tymm == 1 else 6.0)
    
    return round(min(50.0, max(0.0, p1 + p2)), 2), {"empati": empati, "tymm_sorgu": tymm, "yargilayici_uyari": yargi}

def build_blind_expert_export(all_logs: list[dict]) -> str:
    blind_items = []
    for idx, item in enumerate(all_logs, start=1):
        raw = f"{item.get('anonim_kod', '')}|{item.get('oturum_no', '')}|{item.get('tarih_saat', '')}|{idx}"
        blind_items.append({
            "kor_kayit_kodu": "KOR-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper(),
            "profil_adi": item.get("profil_adi"), "kazanim": item.get("kazanim"),
            "eylem_1": item.get("eylem_1"), "eylem_2": item.get("eylem_2"),
            "sec_materyal": item.get("sec_materyal"), "materyal_aciklama": item.get("materyal_aciklama"),
            "sozlu_hitabet": item.get("sozlu_hitabet"),
            "uzman_1_puan_0_100": None, "uzman_2_puan_0_100": None
        })
    return json.dumps(blind_items, ensure_ascii=False, indent=2)

def build_lawshe_export() -> str:
    lawshe_data = {
        "aciklama": "TÜBİTAK 2209-A: Özel Eğitim, PDR ve Matematik Eğitimi Uzmanı Değerlendirme Formu. (1=Uygun, 2=Düzeltilmeli, 3=Çıkarılmalı)",
        "ögrenci_profilleri": [],
        "öğrenme_cıktıları": TYMM_28_OUTCOMES
    }
    for key, val in STUDENT_PROFILES.items():
        lawshe_data["ögrenci_profilleri"].append({
            "profil_adi": val["profil"],
            "kriz_kok_nedeni": val["kok_neden"],
            "lawshe_puani_1_3": None,
            "uzman_notu_klişe_riski": ""
        })
    return json.dumps(lawshe_data, ensure_ascii=False, indent=2)


# ==============================================================================
# 3. STREAMLIT ARAYÜZÜ
# ==============================================================================

st.set_page_config(page_title="TYMM 3B Matematik Sınıf Simülatörü", layout="wide")

if "session_logs" not in st.session_state: st.session_state.session_logs = []
if "journal_logs" not in st.session_state: st.session_state.journal_logs = []

def render_3d_classroom(profile_key: str, kazanim: str, step_status: str):
    prof = STUDENT_PROFILES[profile_key]
    kazanim_kisa = (kazanim[:35] + '...') if len(kazanim) > 35 else kazanim
    
    html = f"""
    <div style="display:flex;justify-content:center;align-items:center;padding:12px;background:#0f172a;border-radius:12px;overflow:hidden;">
      <div style="position:relative;width:500px;height:320px;perspective:1000px;">
        <div style="
          width:380px;height:260px;margin:40px auto 0;
          background:linear-gradient(135deg,#cbd5e1 0%,#94a3b8 100%);
          border:3px solid #475569;border-radius:8px;
          transform:rotateX(60deg) rotateZ(-40deg);
          box-shadow:0 30px 50px rgba(0,0,0,0.5);
          position:relative;transform-style:preserve-3d;">
          
          <div style="position:absolute;inset:0;background-image:linear-gradient(#cbd5e1 1px,transparent 1px),linear-gradient(90deg,#cbd5e1 1px,transparent 1px);background-size:40px 40px;opacity:0.3;"></div>
          
          <div style="position:absolute;top:-60px;left:50px;width:280px;height:24px;background:#1e3a2f;border:3px solid #78350f;border-radius:4px;transform:translateZ(40px) rotateX(-90deg);transform-origin:bottom;display:flex;align-items:center;justify-content:center;color:white;font-size:8px;font-family:sans-serif;box-shadow:0 -5px 15px rgba(0,0,0,0.5);">
             {kazanim_kisa}
          </div>

          <div style="position:absolute;top:10px;left:140px;width:100px;height:40px;background:#92400e;border-radius:4px;box-shadow:inset 0 0 10px rgba(0,0,0,0.3), 10px 10px 15px rgba(0,0,0,0.4);"></div>
          
          <div style="position:absolute;top:90px;left:40px;width:60px;height:35px;background:#b45309;border-radius:4px;box-shadow:5px 5px 10px rgba(0,0,0,0.4);"></div>
          <div style="position:absolute;top:90px;left:140px;width:60px;height:35px;background:#b45309;border-radius:4px;box-shadow:5px 5px 10px rgba(0,0,0,0.4);"></div>
          <div style="position:absolute;top:90px;left:240px;width:60px;height:35px;background:#b45309;border-radius:4px;box-shadow:5px 5px 10px rgba(0,0,0,0.4);"></div>
          
          <div style="position:absolute;top:160px;left:140px;width:60px;height:35px;background:#b45309;border-radius:4px;box-shadow:5px 5px 10px rgba(0,0,0,0.4);">
             <div style="position:absolute;top:-10px;left:15px;width:30px;height:30px;border-radius:50%;background:{prof['avatar_renk']};border:2px solid white;transform:translateZ(20px) rotateX(-90deg) rotateY(-40deg);transform-origin:bottom;box-shadow:0 0 15px {prof['avatar_renk']};">
                 <div style="position:absolute;top:-15px;left:10px;width:10px;height:10px;border-radius:50%;background:#ef4444;animation: bounce 1s infinite alternate;"></div>
             </div>
          </div>
          <div style="position:absolute;top:160px;left:240px;width:60px;height:35px;background:#b45309;border-radius:4px;box-shadow:5px 5px 10px rgba(0,0,0,0.4);"></div>
        </div>
        
        <style>@keyframes bounce {{ from {{ transform: translateY(0); opacity: 1; }} to {{ transform: translateY(-10px); opacity: 0.5; }} }}</style>

        <div style="position:absolute;bottom:6px;left:12px;right:12px;color:#f8fafc;font-family:sans-serif;font-size:12px;display:flex;justify-content:space-between;">
          <span><b>Hedef Öğrenci:</b> {prof['ad']} ({prof['profil']})</span>
          <span><b>Durum:</b> {step_status}</span>
        </div>
      </div>
    </div>
    """
    components.html(html, height=330)

st.title("TYMM Uyumlu 3B Matematik Sınıf Simülatörü")
st.caption("Tek Dosya Dağıtımı • Gelişmiş 3B Sahne • Lawshe Uzman Dışa Aktarımı")

with st.sidebar:
    st.header("1. Öğretmen Adayı Ekranı")
    anon_code = st.text_input("Anonim Katılımcı Kodu", value="KA01").strip().upper()
    oturum_no = st.selectbox("Oturum No", [1, 2, 3, 4], format_func=lambda x: f"{x}. Oturum ({'Transfer Görevi' if x==4 else 'Eğitim'})")
    is_transfer = oturum_no == 4

    profile_key = st.selectbox("Öğrenci Seçin", list(STUDENT_PROFILES.keys()), format_func=lambda k: f"{STUDENT_PROFILES[k]['ad']} ({STUDENT_PROFILES[k]['profil']})")
    prof = STUDENT_PROFILES[profile_key]

    sinif_secimi = st.selectbox("Sınıf Düzeyi", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"], index=["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"].index(prof["sinif_duzeyi"]))
    kazanim_secimi = st.selectbox("Öğrenme Çıktısı (28 Kazanım)", TYMM_28_OUTCOMES[sinif_secimi])

    st.divider()
    st.header("2. Araştırmacı / Uzman Menüsü (İP-1 & İP-2)")
    st.download_button("İP-1 Lawshe Uzman Formu (JSON)", data=build_lawshe_export(), file_name="ip1_lawshe_uzman_formu.json", mime="application/json")
    st.download_button("İP-2 Körleme Puanlama Paketi (JSON)", data=build_blind_expert_export(st.session_state.session_logs), file_name="ip2_korleme_puanlama.json", mime="application/json")

ai_tepki = uret_profil_kazanim_tepkisi(prof, sinif_secimi, kazanim_secimi)

col_left, col_right = st.columns([1.1, 1.3])

with col_left:
    st.subheader("3B Sınıf Sahnesi ve Sentezlenmiş Kriz")
    render_3d_classroom(profile_key, kazanim_secimi, "Transfer Görevi (İpuçsuz)" if is_transfer else "Aktif Müdahale Bekleniyor")
    st.markdown(f"**Öğrenci:** {prof['ad']} ({prof['profil']}) | **Konu:** {sinif_secimi}")
    st.info(f"**Öğrencinin Anlık Tepkisi:**\n\n\"{ai_tepki['ogrenci_sozu']}\"")
    st.markdown(f"**Sınıf İçi Durum Gözlemi:** {ai_tepki['kriz_durumu']}")
    st.caption(f"Üretim Kaynağı: {ai_tepki['kaynak']}")

with col_right:
    st.subheader("Pedagojik Karar, Materyal ve Hitabet Konsolu")
    with st.form("sim_form"):
        eylem_1 = st.radio("**Boyut 1: 1. Adım İlk Müdahale Kararı:**", list(prof["ilk_eylemler"].keys()))
        eylem_2 = st.radio("**Boyut 1: 2. Adım Öğretime Geçiş Kararı:**", list(prof["ikinci_eylemler"].keys()))
        sec_materyal = st.selectbox("**Boyut 2: Materyal Seçin:**", prof["materyaller"])
        materyal_aciklama = st.text_area("Materyali adım adım nasıl uygulatacağınızı yazın (Kurulum, Manipülasyon, Sembolik):", height=70)
        sozlu_hitabet = st.text_area("**Boyut 3: Sözlü geri bildirim ve açık uçlu (TYMM) sorgulama ifadeleri:**", height=70)
        submitted = st.form_submit_button("Değerlendirmeyi Tamamla ve Kaydet")

if submitted:
    puan_b1 = round(prof["ilk_eylemler"][eylem_1] + prof["ikinci_eylemler"][eylem_2], 2)
    puan_b2, donut_b2 = puanla_boyut2_materyal(sec_materyal, prof["uygun_materyal"], materyal_aciklama)
    puan_b3, donut_b3 = puanla_boyut3_hitabet(sozlu_hitabet)
    toplam_puan = round(puan_b1 + puan_b2 + puan_b3, 2)

    st.session_state.session_logs.append({
        "tarih_saat": datetime.now().isoformat(timespec="seconds"), "anonim_kod": anon_code, "oturum_no": oturum_no,
        "profil_adi": prof["profil"], "kazanim": kazanim_secimi, "boyut_1_puan": puan_b1, "boyut_2_puan": puan_b2,
        "boyut_3_puan": puan_b3, "toplam_puan": toplam_puan, "eylem_1": eylem_1, "eylem_2": eylem_2,
        "sec_materyal": sec_materyal, "materyal_aciklama": materyal_aciklama, "sozlu_hitabet": sozlu_hitabet,
    })

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Boyut 1 (Kronoloji)", f"{puan_b1}/25")
    c2.metric("Boyut 2 (Materyal)", f"{puan_b2}/25")
    c3.metric("Boyut 3 (Hitabet)", f"{puan_b3}/50")
    c4.metric("Toplam Rubrik Puanı", f"{toplam_puan}/100")

    if is_transfer: st.info("4. Oturum: İpucu veya dönüt sunulmamaktadır.")
    else:
        st.success(f"Kök Neden: {prof['kok_neden']}")
        st.write(f"- Materyal: {donut_b2} | Hitabet: {donut_b3}")

st.divider()
st.subheader("Oturum Sonu Bireysel Gelişim Portfolyosu")
user_logs = [r for r in st.session_state.session_logs if r.get("anonim_kod") == anon_code]
if user_logs:
    st.dataframe(user_logs, use_container_width=True)
    st.download_button("Portfolyoyu İndir (JSON)", data=json.dumps(user_logs, ensure_ascii=False, indent=2), file_name=f"portfolyo_{anon_code}.json", mime="application/json")
