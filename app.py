"""
TYMM Ortaokul Matematik (5-8. Sınıflar) Öğrenci Profilleri,
28 Öğrenme Çıktısı ve Deterministik Kural Motoru Sözlükleri.
"""

STUDENT_PROFILES = {
    "disleksi": {
        "ad": "Defne",
        "cinsiyet": "Kız",
        "profil": "Disleksi",
        "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Metin okuma ve sembolik harf/rakam karışıklığında hızlı yorulma ve çekinme",
        "tepki_tarzi": "Satır atlama, sembol yer değiştirme ve metin yoğunlaştıkça sessizleşip defteri kapatma",
        "kok_neden": "Okuma yükü ve sembol karmaşası nedeniyle bilişsel aşırı yüklenme yaşanması.",
        "uygun_materyal": "Kesir Çubukları",
        "materyaller": ["Kesir Çubukları", "Cebir Karoları", "Birim Küpler", "Oran Tahtası", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Duyuşsal yatıştırma ve okuma/metin yükünü azaltma": 12.5,
            "Yüksek sesle ve hızlı biçimde metni baştan okumasını isteme": 2.0,
            "Tahtaya kalkıp sınıf önünde okuması için zorlama": 0.0,
        },
        "ikinci_eylemler": {
            "Kesir çubuklarıyla görsel modellemeye güvenli geçiş yapma": 12.5,
            "Uzun sözel yönerge zinciri vererek soyut işlem isteme": 3.0,
            "Doğrudan formül ezberletmeye geçme": 1.0,
        },
        "avatar_renk": "#4A90E2",
    },
    "otizm": {
        "ad": "Kerem",
        "cinsiyet": "Erkek",
        "profil": "Otizm Spektrumu",
        "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Ani ses, kalabalık gürültüsü ve belirsiz/değişken yönergelere karşı hassasiyet",
        "tepki_tarzi": "Beklenmedik uyaran veya belirsiz ifadede kulakları kapatma, sallanma ve net yapı arayışı",
        "kok_neden": "Ani duyusal/çevresel değişim nedeniyle duyusal regülasyonun bozulması.",
        "uygun_materyal": "Oran Tahtası",
        "materyaller": ["Oran Tahtası", "Kesir Çubukları", "Birim Küpler", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Duyusal yüklenmeyi azaltan sakin, net ve öngörülebilir yatıştırma": 12.5,
            "Ani dokunma veya yüksek sesle dikkatini çekmeye çalışma": 0.0,
            "Soru yağmuruna tutarak hemen yanıt bekleme": 2.0,
        },
        "ikinci_eylemler": {
            "Net adımlı Oran Tahtası üzerinde yapılandırılmış görsel eşleştirme": 12.5,
            "Belirsiz ve mecazlı ifadelerle soyut akıl yürütme isteme": 2.0,
            "Grup içi rekabetçi yarışmaya dahil etme": 1.0,
        },
        "avatar_renk": "#50B89A",
    },
    "ustun_yetenek": {
        "ad": "Elif",
        "cinsiyet": "Kız",
        "profil": "Üstün Yetenek",
        "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Düşük bilişsel meydan okuma ve tekrarlı alıştırmalarda çabuk sıkılma",
        "tepki_tarzi": "Rutin adımlarda sabırsızlanma, alaycı yorum yapma ve genelleme/derinlik talep etme",
        "kok_neden": "Bilişsel uyarım eksikliği ve düşük meydan okuma düzeyi.",
        "uygun_materyal": "Cebir Karoları",
        "materyaller": ["Cebir Karoları", "Birim Küpler", "Oran Tahtası", "Kesir Çubukları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Davranışı sınırlarken bilişsel potansiyeli genelleme/keşfe yönlendirme": 12.5,
            "Sınıf önünde azarlayarak utandırma": 0.0,
            "Yalnızca daha fazla rutin işlem yaprağı verme": 3.0,
        },
        "ikinci_eylemler": {
            "Cebir karolarıyla alan modelinden genelleme/ilişki kurgulatma": 12.5,
            "Ezber kural verip mekanik işlem yaptırma": 3.0,
            "Görev vermeden boş bırakma": 1.0,
        },
        "avatar_renk": "#9B59B6",
    },
    "yuksek_kaygi": {
        "ad": "Mert",
        "cinsiyet": "Erkek",
        "profil": "Yüksek Matematik Kaygısı",
        "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Zaman baskısı ve yanlış yapma korkusuyla donma/geri çekilme",
        "tepki_tarzi": "'Yanlış yapacağım' kaygısıyla kalemi bırakma, kararsız kalma ve onay arama",
        "kok_neden": "Başarısızlık ve değerlendirilme kaygısına bağlı donma tepkisi.",
        "uygun_materyal": "Birim Küpler",
        "materyaller": ["Birim Küpler", "Kesir Çubukları", "Oran Tahtası", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Zaman baskısını kaldırıp hata yapmanın doğal olduğunu vurgulama": 12.5,
            "'Çok kolay, neden yapamıyorsun?' diyerek küçümseme": 0.0,
            "Süreyi daha da kısaltarak hızlandırmaya çalışma": 1.0,
        },
        "ikinci_eylemler": {
            "Birim küplerle küçük, risksiz adımlarla somut model kurma": 12.5,
            "Anında puan/doğru-yanlış baskısı kurma": 2.0,
            "Doğrudan cebirsel denklem yazmasını isteme": 3.0,
        },
        "avatar_renk": "#E67E22",
    },
    "mukemmeliyetcilik": {
        "ad": "Zeynep",
        "cinsiyet": "Kız",
        "profil": "Mükemmeliyetçilik",
        "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Kusursuzluk beklentisi ve küçük hatalarda yüksek hayal kırıklığı",
        "tepki_tarzi": "Çizim/işlem kusursuz değilse silip yırtma, yeniden başlama ve çalışmayı durdurma",
        "kok_neden": "Kusursuzluk beklentisi ve hatayı kişisel yetersizlik olarak görme.",
        "uygun_materyal": "İki Renkli Sayma Pulları",
        "materyaller": ["İki Renkli Sayma Pulları", "Birim Küpler", "Cebir Karoları", "Oran Tahtası", "Kesir Çubukları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Kusursuz olma baskısını düşüren, deneme sürecini onaylayan yaklaşım": 12.5,
            "'Kağıdı mahvettin, düzgün çiz' diyerek eleştirme": 0.0,
            "Müdahale etmeden yırtmaya devam etmesini izleme": 3.0,
        },
        "ikinci_eylemler": {
            "İki renkli sayma pullarıyla sıfır çifti mantığını adım adım kurgulama": 12.5,
            "Tek bir 'doğru' kalıba sıkıştırma": 3.0,
            "Soyut kuralı ezberletmeye geçme": 2.0,
        },
        "avatar_renk": "#E91E63",
    },
    "davranis_bozuklugu": {
        "ad": "Kaan",
        "cinsiyet": "Erkek",
        "profil": "Davranış Bozukluğu / Karşı Gelme",
        "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Otoriter buyruklara ve anlamsız görünen görevlere karşı direnç",
        "tepki_tarzi": "İtiraz etme, sıraya vurma, materyali itme ve 'Bu ne işime yarayacak?' tepkisi verme",
        "kok_neden": "Otoriteye karşı direnç, dışlanma algısı ve anlamlandırma güçlüğü.",
        "uygun_materyal": "GeoGebra 3B",
        "materyaller": ["GeoGebra 3B", "Cebir Karoları", "Oran Tahtası", "Birim Küpler", "Kesir Çubukları", "İki Renkli Sayma Pulları", "Simetri Aynası"],
        "ilk_eylemler": {
            "Güç mücadelesine girmeden sınırları sakin ve net biçimde koyma": 12.5,
            "Sınıf önünde bağırarak tehdit veya ceza verme": 0.0,
            "Tamamen görmezden gelip sınıf düzenini bozmasına izin verme": 2.0,
        },
        "ikinci_eylemler": {
            "GeoGebra 3B üzerinde dinamik değişimle somut ilişkiyi keşfettirme": 12.5,
            "Kuru kural dayatma": 2.0,
            "Sadece yazılı ceza/uyarı verme": 1.0,
        },
        "avatar_renk": "#C0392B",
    },
    "sosyal_ice_donukluk": {
        "ad": "Eylül",
        "cinsiyet": "Kız",
        "profil": "Sosyal İçe Dönüklük",
        "sinif_duzeyi": "5. Sınıf",
        "duyusal_ozellik": "Kalabalık önünde konuşma ve ani söz verilmesi durumunda çekinme",
        "tepki_tarzi": "Başını eğme, sessiz kalma, grup baskısında geri çekilme ve güvenli alan arama",
        "kok_neden": "Sosyal etkileşim ve kalabalık önünde konuşma çekincesi.",
        "uygun_materyal": "Simetri Aynası",
        "materyaller": ["Simetri Aynası", "Birim Küpler", "GeoGebra 3B", "Kesir Çubukları", "Oran Tahtası", "Cebir Karoları", "İki Renkli Sayma Pulları"],
        "ilk_eylemler": {
            "Zorlamadan güvenli bireysel alan ve sakin iletişim kurma": 12.5,
            "'Herkesin içinde konuş, niye susuyorsun?' diye baskı yapma": 0.0,
            "Hiç dahil etmeden tamamen dışarıda bırakma": 3.0,
        },
        "ikinci_eylemler": {
            "Simetri aynasıyla bireysel keşif sonrası küçük adımlı paylaşım sunma": 12.5,
            "Ani sunum yapmaya zorlama": 2.0,
            "Sadece sözel tanım isteme": 3.0,
        },
        "avatar_renk": "#16A085",
    },
    "asiri_hareketlilik": {
        "ad": "Aras",
        "cinsiyet": "Erkek",
        "profil": "Aşırı Hareketlilik / Dürtüsellik",
        "sinif_duzeyi": "6. Sınıf",
        "duyusal_ozellik": "Yüksek hareket enerjisi, beklemede zorlanma ve aceleyle yanıt verme",
        "tepki_tarzi": "Soru bitmeden atılma, materyalleri hızla karıştırma ve kısa/net yönergelere ihtiyaç duyma",
        "kok_neden": "Dürtü kontrolü ve dikkat sürdürmede zorlanma; kinestetik enerji fazlalığı.",
        "uygun_materyal": "Birim Küpler",
        "materyaller": ["Birim Küpler", "GeoGebra 3B", "Oran Tahtası", "Kesir Çubukları", "Cebir Karoları", "İki Renkli Sayma Pulları", "Simetri Aynası"],
        "ilk_eylemler": {
            "Kısa, somut ve yapılandırılmış hareket/görev sınırıyla regüle etme": 12.5,
            "'Yerine çivilen, kıpırdama!' şeklinde sert uyarı verme": 0.0,
            "Uzun ve karmaşık çok adımlı yönerge verme": 2.0,
        },
        "ikinci_eylemler": {
            "Birim küplerle kontrollü inşa ve sayma adımlarına yönlendirme": 12.5,
            "Sürekli tek başına hız yarışı yaptırma": 2.0,
            "Açıklamasız soyut formül verme": 2.0,
        },
        "avatar_renk": "#D35400",
    },
    "sozel_ifade_guclugu": {
        "ad": "Miraç",
        "cinsiyet": "Erkek",
        "profil": "Sözel İfade Güçlüğü",
        "sinif_duzeyi": "7. Sınıf",
        "duyusal_ozellik": "Kavramı bilmesine karşın kelimeleri toparlama ve sözel aktarımda zorlanma",
        "tepki_tarzi": "'Şey... anlatamıyorum' diyerek duraksama, görsel/parçalı gösterimle anlatmak isteme",
        "kok_neden": "İfade edici dil ve kavram bulma güçlüğü.",
        "uygun_materyal": "Oran Tahtası",
        "materyaller": ["Oran Tahtası", "İki Renkli Sayma Pulları", "Kesir Çubukları", "Birim Küpler", "Cebir Karoları", "Simetri Aynası", "GeoGebra 3B"],
        "ilk_eylemler": {
            "Kelime bulma baskısını kaldıran, alternatif gösterimlere izin veren yaklaşım": 12.5,
            "Cümlesini sabırsızlıkla tamamlama veya 'Cümleni kur' diye zorlama": 1.0,
            "Sadece uzun yazılı açıklama isteme": 2.0,
        },
        "ikinci_eylemler": {
            "Oran tahtası ve görsel eşleştirmeyle gerekçelendirmeyi destekleme": 12.5,
            "Yalnızca soyut sözel tanımla yetinme": 2.0,
            "Soruyu geri çekme": 1.0,
        },
        "avatar_renk": "#2980B9",
    },
    "gorsel_uzamsal": {
        "ad": "Duru",
        "cinsiyet": "Kız",
        "profil": "Görsel / Uzamsal Öğrenme Ağırlığı",
        "sinif_duzeyi": "8. Sınıf",
        "duyusal_ozellik": "Uzamsal döndürme, şekil ve konum ilişkilerinde güçlü kavrayış; soyut tabloda zorlanma",
        "tepki_tarzi": "Tablo/kural ezberinde takılma ancak şekil/model döndürüldüğünde hızla bağlantı kurma",
        "kok_neden": "Sembolik-sözel sunum yerine uzamsal/görsel temsillerde daha yüksek verim alma.",
        "uygun_materyal": "GeoGebra 3B",
        "materyaller": ["GeoGebra 3B", "Simetri Aynası", "Birim Küpler", "Cebir Karoları", "Oran Tahtası", "Kesir Çubukları", "İki Renkli Sayma Pulları"],
        "ilk_eylemler": {
            "Uzamsal/görsel güçlü yönünü merkeze alan destekleyici ilk müdahale": 12.5,
            "Uzamsal ipucunu yok sayıp yalnızca formül tablosuna hapsetme": 2.0,
            "Kıyaslayıcı/etiketleyici dil kullanma": 0.0,
        },
        "ikinci_eylemler": {
            "GeoGebra 3B ve dönüşüm adımlarıyla görsel-sembolik köprü kurma": 12.5,
            "Görsel inceleme yaptırmadan ezber kural verme": 3.0,
            "Tek yönlü anlatımla bırakma": 2.0,
        },
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

EMPATIK_IFADELER = [
    "anladım", "birlikte", "yanındayım", "acele yok", "hata yapabilirsin",
    "normal", "güvendesin", "adım adım", "senin hızında", "kabul ediyorum",
    "haklısın", "deneyelim", "keşfedelim", "fark ettim", "sakin"
]

TYMM_SORGU_IFADELERI = [
    "neden", "nasıl", "ne fark", "ilişki", "örüntü", "tahmin",
    "gerekçe", "açıklar mısın", "ne gözlemledin", "başka nasıl",
    "genelleyebilir", "neden böyle oldu", "sence"
]

YARGILAYICI_IFADELER = [
    "neden hala", "anlamadın", "arkadaşların çözdü", "yerine otur",
    "saçma", "tembel", "beceriksiz", "çocukça", "kapa çeneni", "sus",
    "zaten söyledim", "içler dışlar çarpımı yap"
]

KURULUM_ANAHTARLARI = ["kurulum", "yerleştir", "hazırla", "aç", "temsil", "tanımla", "başla", "koy"]
MANIPULASYON_ANAHTARLARI = ["öğrenci", "birlikte", "hareket", "taşı", "ayır", "birleştir", "döndür", "uygula", "manipüle", "çek"]
SEMBOLIK_ANAHTARLARI = ["sembol", "ifade", "denklem", "oran", "kesir", "yaz", "ilişkilendir", "genelle", "kural"]
"""
Profil-Kazanım Yapay Zekâ Tepki Motoru (Yerel Ollama veya Yerel Dinamik Üretici),
Deterministik Kural Motoru (Boyut 1-3), Yerel Kayıt ve Körleme Dışa Aktarımı.
"""

import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from curriculum_and_profiles import (
    EMPATIK_IFADELER,
    KURULUM_ANAHTARLARI,
    MANIPULASYON_ANAHTARLARI,
    SEMBOLIK_ANAHTARLARI,
    TYMM_SORGU_IFADELERI,
    YARGILAYICI_IFADELER,
)

DATA_DIR = Path("sim_local_data")
DATA_DIR.mkdir(exist_ok=True)
LOG_FILE = DATA_DIR / "session_logs.jsonl"
JOURNAL_FILE = DATA_DIR / "reflective_journals.jsonl"


def _yerel_ollama_tepkisi_al(prompt: str, model: str = "llama3.1", timeout_sec: float = 2.0) -> str | None:
    """Yerel ağda (localhost:11434) çalışan Ollama varsa profil/kazanım tepkisi üretir."""
    url = "http://localhost:11434/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            metin = (data.get("response") or "").strip()
            return metin if metin else None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, Exception):
        return None


def uret_profil_kazanim_tepkisi(prof: dict, sinif_duzeyi: str, kazanim: str, use_local_llm: bool = False, llm_model: str = "llama3.1") -> dict:
    """
    Seçilen öğrenci profiline ve kazanıma göre öğrencinin o kazanımda vereceği
    otomatik sınıf içi tepkiyi ve kriz durumunu üretir.
    """
    profil_adi = prof["profil"]
    ad = prof["ad"]
    kazanim_kisa = kazanim.lower()

    if use_local_llm:
        prompt = (
            f"Sen ortaokul matematik dersinde {sinif_duzeyi} öğrencisi olan {ad}'sın. "
            f"Öğrenci profilin: {profil_adi}. Özelliklerin: {prof['duyusal_ozellik']}. "
            f"Kazanım: '{kazanim}'. "
            f"Bu kazanım işlenirken profiline uygun gerçekçi, klişelerden uzak, kısa bir sınıf içi tepki ve cümle yaz."
        )
        llm_yanit = _yerel_ollama_tepkisi_al(prompt, model=llm_model)
        if llm_yanit:
            return {
                "kaynak": f"Yerel Yapay Zekâ (Ollama - {llm_model})",
                "kriz_durumu": llm_yanit,
                "ogrenci_sozu": llm_yanit,
                "uygun_materyal": prof["uygun_materyal"],
            }

    # Yerel dinamik AI/kural tabanlı profil-kazanım tepki sentezi (10 profil x 28 kazanım)
    if profil_adi == "Otizm Spektrumu":
        ogrenci_sozu = f"Öğretmenim, '{kazanim_kisa}' konusunda ses çok karıştı ve neyin önce yapılacağı net değil; kulaklarımı kapatmak istiyorum."
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' etkinliğinde ani ortam sesi veya belirsiz yönerge nedeniyle "
            f"kulaklarını kapatıp sallanıyor ve net, yapılandırılmış bir adım bekliyor."
        )
    elif profil_adi == "Disleksi":
        ogrenci_sozu = f"'{kazanim_kisa}' ile ilgili yazıları takip ederken satırlar birbirine giriyor, sayıları/sembolleri karıştırıyorum."
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' sırasında yoğun metin ve sembol okumada zorlandığı için "
            f"defterini kapatıp geri çekiliyor."
        )
    elif profil_adi == "Üstün Yetenek":
        ogrenci_sozu = f"'{kazanim_kisa}' adımını zaten gördüm; hep aynı alıştırmayı yapmak sıkıcı, bunun genellemesi veya daha derin bir sorunu yok mu?"
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' çalışmasında düşük meydan okuma nedeniyle sıkılıyor "
            f"ve rutin adımlara karşı sabırsız/alaycı tepki veriyor."
        )
    elif profil_adi == "Yüksek Matematik Kaygısı":
        ogrenci_sozu = f"'{kazanim_kisa}' konusunda yanlış yaparsam ya da süre biterse ne olacak? Yapamayacağım galiba..."
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' etkinliğinde hata yapma ve değerlendirilme kaygısıyla "
            f"kalemini bırakıp donup kalıyor."
        )
    elif profil_adi == "Mükemmeliyetçilik":
        ogrenci_sozu = f"'{kazanim_kisa}' çizimim/işlemim tam istediğim gibi olmadı, baştan yapmak istiyorum ama yine bozulacak."
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' sırasında kusursuzluk beklentisi yüzünden kağıdı/çizimi "
            f"tekrar tekrar silip çalışmayı durduruyor."
        )
    elif profil_adi == "Davranış Bozukluğu / Karşı Gelme":
        ogrenci_sozu = f"'{kazanim_kisa}' ne işime yarayacak ki? Zorla yaptırılacak bir şey değil bu!"
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' etkinliğinde karşı gelme tepkisi vererek materyali kenara itiyor "
            f"ve sınıf düzenini zorluyor."
        )
    elif profil_adi == "Sosyal İçe Dönüklük":
        ogrenci_sozu = f"'{kazanim_kisa}' hakkında... şey, şimdi konuşmasam, önce kendi kendime baksam olur mu?"
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' sırasında kalabalık/söz alma baskısı hissedince başını eğip "
            f"sessizleşerek geri çekiliyor."
        )
    elif profil_adi == "Aşırı Hareketlilik / Dürtüsellik":
        ogrenci_sozu = f"Ben buldum! Dur beklemeden şunu hemen koyayım, ha bir de şu tarafı nasıl oluyor?"
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' etkinliğinde yönerge bitmeden hızlı ve dürtüsel davranarak "
            f"materyalleri/adımları karıştırıyor."
        )
    elif profil_adi == "Sözel İfade Güçlüğü":
        ogrenci_sozu = f"'{kazanim_kisa}' mantığını kafamda kurdum ama... kelimeler gelmiyor, göstererek anlatabilir miyim?"
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' üzerine düşünürken sözel ifade güçlüğü yaşadığı için "
            f"kelime bulmakta zorlanıp duraksıyor."
        )
    else:  # Görsel / Uzamsal Öğrenme Ağırlığı
        ogrenci_sozu = f"'{kazanim_kisa}' kuralını yazıda ezberlemek zor geliyor ama şekli/modeli çevirince gözümde canlanıyor."
        kriz_durumu = (
            f"{ad} ({sinif_duzeyi}), '{kazanim}' kazanımında sözel/sembolik anlatımda zorlanırken "
            f"uzamsal/görsel modellemede daha rahat ilerliyor."
        )

    return {
        "kaynak": "Yerel Profil-Kazanım Yapay Zekâ Tepki Motoru",
        "kriz_durumu": kriz_durumu,
        "ogrenci_sozu": ogrenci_sozu,
        "uygun_materyal": prof["uygun_materyal"],
    }


def puanla_boyut2_materyal(secilen_materyal: str, dogru_materyal: str, aciklama: str):
    """Boyut 2 (0-25 puan): Materyal seçimi (12.5) + 3 aşamalı kullanım açıklaması (12.5)."""
    puan_secim = 12.5 if secilen_materyal == dogru_materyal else 5.0
    txt = (aciklama or "").lower().strip()

    asama_1 = any(k in txt for k in KURULUM_ANAHTARLARI)
    asama_2 = any(k in txt for k in MANIPULASYON_ANAHTARLARI)
    asama_3 = any(k in txt for k in SEMBOLIK_ANAHTARLARI)
    sayac = sum([asama_1, asama_2, asama_3])

    if len(txt) < 15 or sayac == 0:
        puan_aciklama = 2.0
    elif sayac == 1:
        puan_aciklama = 5.5
    elif sayac == 2:
        puan_aciklama = 9.0
    else:
        puan_aciklama = 12.5

    toplam = round(min(25.0, puan_secim + puan_aciklama), 2)
    donut = {
        "materyal_uyumu": "Tam uyumlu" if secilen_materyal == dogru_materyal else f"Alternatif seçildi (Önerilen: {dogru_materyal})",
        "kurulum_temsil": asama_1,
        "ogrenci_manipulasyonu": asama_2,
        "sembolik_gecis": asama_3,
    }
    return toplam, donut


def puanla_boyut3_hitabet(sozlu_metin: str):
    """Boyut 3 (0-50 puan): Kapsayıcı/Empatik hitabet (25) + TYMM süreç bileşeni sorgulama (25)."""
    txt = (sozlu_metin or "").lower().strip()
    empati_say = sum(1 for k in EMPATIK_IFADELER if k in txt)
    tymm_say = sum(1 for k in TYMM_SORGU_IFADELERI if k in txt)
    yargi_say = sum(1 for k in YARGILAYICI_IFADELER if k in txt)

    if yargi_say > 0:
        puan_31 = max(0.0, 8.0 - (yargi_say * 3.0))
    elif empati_say >= 2:
        puan_31 = 21.0
    elif empati_say == 1:
        puan_31 = 14.0
    else:
        puan_31 = 9.0

    if tymm_say >= 2:
        puan_32 = 21.0
    elif tymm_say == 1:
        puan_32 = 14.0
    else:
        puan_32 = 6.0

    toplam = round(min(50.0, max(0.0, puan_31 + puan_32)), 2)
    donut = {
        "empati_eslesme": empati_say,
        "tymm_sorgulama_eslesme": tymm_say,
        "yargilayici_ifade_uyarisi": yargi_say,
    }
    return toplam, donut


def save_session_log(record: dict):
    """Yerel diske (localhost) JSONL formatında oturum kaydı ekler."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_session_logs(anon_code: str | None = None):
    """Kayıtlı oturumları yükler; anon_code verilirse o adaya göre filtreler."""
    if not LOG_FILE.exists():
        return []
    rows = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
                if anon_code is None or item.get("anonim_kod") == anon_code:
                    rows.append(item)
            except json.JSONDecodeError:
                continue
    return rows


def save_journal_entry(entry: dict):
    """Oturum sonu yansıtıcı günlüğü yerel diske kaydeder."""
    entry["kayit_zamani"] = datetime.now().isoformat(timespec="seconds")
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_blind_expert_export():
    """İki bağımsız uzman puanlaması için körleme değerlendirme paketi üretir."""
    all_logs = load_session_logs(anon_code=None)
    blind_items = []
    for idx, item in enumerate(all_logs, start=1):
        raw_token = f"{item.get('anonim_kod', '')}|{item.get('oturum_no', '')}|{item.get('tarih_saat', '')}|{idx}"
        kor_kod = "KOR-" + hashlib.sha256(raw_token.encode("utf-8")).hexdigest()[:8].upper()
        blind_items.append({
            "kor_kayit_kodu": kor_kod,
            "profil_adi": item.get("profil_adi"),
            "sinif_duzeyi": item.get("sinif_duzeyi"),
            "kazanim": item.get("kazanim"),
            "ogrenci_tepkisi": item.get("ogrenci_tepkisi"),
            "eylem_1": item.get("eylem_1"),
            "eylem_2": item.get("eylem_2"),
            "sec_materyal": item.get("sec_materyal"),
            "materyal_aciklama": item.get("materyal_aciklama"),
            "sozlu_hitabet": item.get("sozlu_hitabet"),
            "uzman_1_puan_0_100": None,
            "uzman_2_puan_0_100": None,
            "uzman_notu": "",
        })
    return json.dumps(blind_items, ensure_ascii=False, indent=2)
    """
TÜBİTAK 2209-A - TYMM Uyumlu 3B Matematik Sınıf Simülatörü Ana Arayüzü.
Çalıştırmak için: streamlit run app.py
"""

import json
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

from curriculum_and_profiles import STUDENT_PROFILES, TYMM_28_OUTCOMES
from scoring_and_storage import (
    build_blind_expert_export,
    load_session_logs,
    puanla_boyut2_materyal,
    puanla_boyut3_hitabet,
    save_journal_entry,
    save_session_log,
    uret_profil_kazanim_tepkisi,
)

st.set_page_config(
    page_title="TYMM 3B Matematik Sınıf Simülatörü",
    layout="wide",
)


def render_3d_classroom(profile_key: str, step_status: str):
    """HTML5/CSS3 izometrik 3B sınıf sahnesi."""
    prof = STUDENT_PROFILES[profile_key]
    html = f"""
    <div style="display:flex;justify-content:center;align-items:center;padding:12px;background:#0f172a;border-radius:12px;">
      <div style="position:relative;width:440px;height:255px;perspective:900px;">
        <div style="
          width:300px;height:180px;margin:38px auto 0;
          background:linear-gradient(135deg,#e2e8f0 0%,#cbd5e1 100%);
          border:2px solid #64748b;border-radius:10px;
          transform:rotateX(55deg) rotateZ(-35deg);
          box-shadow:0 20px 35px rgba(0,0,0,0.45);
          position:relative;">
          <div style="position:absolute;top:-42px;left:45px;width:210px;height:14px;background:#1e3a2f;border:2px solid #78350f;border-radius:3px;"></div>
          <div style="position:absolute;top:72px;left:110px;width:72px;height:44px;background:#b45309;border-radius:4px;"></div>
          <div style="
            position:absolute;top:52px;left:130px;width:32px;height:32px;
            border-radius:50%;background:{prof['avatar_renk']};
            border:3px solid #ffffff;box-shadow:0 4px 10px rgba(0,0,0,0.35);">
          </div>
        </div>
        <div style="position:absolute;bottom:6px;left:12px;right:12px;color:#f8fafc;font-family:sans-serif;font-size:12px;display:flex;justify-content:space-between;">
          <span><b>Öğrenci:</b> {prof['ad']} ({prof['profil']})</span>
          <span><b>Durum:</b> {step_status}</span>
        </div>
      </div>
    </div>
    """
    components.html(html, height=280)


st.title("TYMM Uyumlu 3B Matematik Sınıf Simülatörü")
st.caption("Yerel ağ (localhost) çalışma modu • Ham ses kaydı tutulmaz • Anonim kod (KA01–KA40) ile kayıt")

with st.sidebar:
    st.header("Öğrenci, Sınıf ve Kazanım Seçimi")
    anon_code = st.text_input("Anonim Katılımcı Kodu (KA01–KA40)", value="KA01").strip().upper()
    oturum_no = st.selectbox(
        "Oturum No",
        [1, 2, 3, 4],
        format_func=lambda x: f"{x}. Oturum ({'Transfer Görevi - İpuçsuz' if x == 4 else 'Eğitim & Hata Düzeltme'})",
    )
    is_transfer = oturum_no == 4

    # Öğretmen adayı istediği öğrenci profilini serbestçe seçebilir
    profile_key = st.selectbox(
        "Öğrenci Seçin (10 Profil)",
        options=list(STUDENT_PROFILES.keys()),
        format_func=lambda k: f"{STUDENT_PROFILES[k]['ad']} — {STUDENT_PROFILES[k]['profil']} ({STUDENT_PROFILES[k]['cinsiyet']})",
    )
    prof = STUDENT_PROFILES[profile_key]

    sinif_secimi = st.selectbox(
        "Sınıf Düzeyi (5–8. Sınıf)",
        ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"],
        index=["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf"].index(prof["sinif_duzeyi"]),
    )
    kazanim_secimi = st.selectbox(
        "Öğrenme Çıktısı Seçin (28 Kazanım)",
        TYMM_28_OUTCOMES[sinif_secimi],
    )

    st.divider()
    st.subheader("Yerel Yapay Zekâ Tepki Ayarı")
    use_local_llm = st.checkbox("Yerel Ollama (localhost:11434) ile tepki üret", value=False)
    llm_model = st.text_input("Ollama Model Adı", value="llama3.1", disabled=not use_local_llm)

    st.divider()
    st.subheader("Uzman Puanlama (Körleme)")
    st.download_button(
        label="Körleme Uzman Puanlama Paketi İndir (JSON)",
        data=build_blind_expert_export(),
        file_name="korleme_uzman_puanlama.json",
        mime="application/json",
    )

# Seçilen öğrenci profili ve kazanıma göre otomatik tepki üretimi
ai_tepki = uret_profil_kazanim_tepkisi(
    prof=prof,
    sinif_duzeyi=sinif_secimi,
    kazanim=kazanim_secimi,
    use_local_llm=use_local_llm,
    llm_model=llm_model,
)

col_left, col_right = st.columns([1.05, 1.35])

with col_left:
    st.subheader("3B Sınıf Sahnesi ve Otomatik Öğrenci Tepkisi")
    render_3d_classroom(profile_key, "Transfer Görevi (İpuçsuz)" if is_transfer else "Eğitim & Hata Düzeltme")
    st.markdown(f"**Seçilen Öğrenci:** {prof['ad']} ({prof['profil']})")
    st.markdown(f"**Sınıf & Kazanım:** {sinif_secimi} — *{kazanim_secimi}*")
    st.info(f"**Öğrencinin Kazanım Tepkisi ({ai_tepki['kaynak']}):**\n\n\"{ai_tepki['ogrenci_sozu']}\"")
    st.markdown(f"**Sınıf İçi Durum:** {ai_tepki['kriz_durumu']}")

with col_right:
    st.subheader("Pedagojik Karar, Materyal ve Sözlü Hitabet Konsolu")

    with st.form("sim_form"):
        st.markdown("**Boyut 1: Kronolojik Pedagojik Eylem Sıralaması (0–25 Puan)**")
        eylem_1 = st.radio("1. Adım — İlk Müdahale Kararı:", list(prof["ilk_eylemler"].keys()))
        eylem_2 = st.radio("2. Adım — İkinci Müdahale Kararı:", list(prof["ikinci_eylemler"].keys()))

        st.markdown("**Boyut 2: Kazanıma Uygun Materyal Seçimi ve 3 Adımlı Uygulama Açıklaması (0–25 Puan)**")
        sec_materyal = st.selectbox("Materyal Seçin:", prof["materyaller"])
        materyal_aciklama = st.text_area(
            "Materyali adım adım nasıl uygulatacağınızı yazın (1. Kurulum/Temsil, 2. Öğrenci manipülasyonu, 3. Sembolik ilişkilendirme):",
            height=90,
        )

        st.markdown("**Boyut 3: Kapsayıcı Sözlü Hitabet ve TYMM Süreç Bileşeni Sorgulama (0–50 Puan)**")
        sozlu_hitabet = st.text_area(
            "Sözlü geri bildirim ve açık uçlu sorgulama ifadeleri (Yerel konuşmadan metne çıktısı veya doğrudan metin girişi):",
            height=90,
        )

        submitted = st.form_submit_button("Değerlendirmeyi Tamamla ve Kaydet")

if submitted:
    puan_b1 = round(prof["ilk_eylemler"][eylem_1] + prof["ikinci_eylemler"][eylem_2], 2)
    puan_b2, donut_b2 = puanla_boyut2_materyal(sec_materyal, prof["uygun_materyal"], materyal_aciklama)
    puan_b3, donut_b3 = puanla_boyut3_hitabet(sozlu_hitabet)
    toplam_puan = round(puan_b1 + puan_b2 + puan_b3, 2)

    record = {
        "tarih_saat": datetime.now().isoformat(timespec="seconds"),
        "anonim_kod": anon_code,
        "oturum_no": oturum_no,
        "transfer_gorevi": is_transfer,
        "profil_key": profile_key,
        "profil_adi": prof["profil"],
        "ogrenci_adi": prof["ad"],
        "sinif_duzeyi": sinif_secimi,
        "kazanim": kazanim_secimi,
        "ogrenci_tepkisi": ai_tepki["ogrenci_sozu"],
        "tepki_kaynagi": ai_tepki["kaynak"],
        "boyut_1_puan": puan_b1,
        "boyut_2_puan": puan_b2,
        "boyut_3_puan": puan_b3,
        "toplam_puan": toplam_puan,
        "eylem_1": eylem_1,
        "eylem_2": eylem_2,
        "sec_materyal": sec_materyal,
        "materyal_aciklama": materyal_aciklama,
        "sozlu_hitabet": sozlu_hitabet,
    }
    save_session_log(record)

    st.divider()
    st.subheader("Değerlendirme Sonucu")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Boyut 1 (Kronoloji)", f"{puan_b1} / 25")
    c2.metric("Boyut 2 (Materyal)", f"{puan_b2} / 25")
    c3.metric("Boyut 3 (Hitabet & TYMM)", f"{puan_b3} / 50")
    c4.metric("Toplam Rubrik Puanı", f"{toplam_puan} / 100")

    if is_transfer:
        st.info("4. Oturum (Transfer Görevi): Bu oturumda ipucu veya kök neden dönütü sunulmamaktadır.")
    else:
        st.success("Kök Neden Geri Bildirimi (1–3. Oturum Hata Düzeltme Döngüsü):")
        st.write(f"- **Kriz Kök Nedeni:** {prof['kok_neden']}")
        st.write(f"- **Materyal Analizi:** {donut_b2}")
        st.write(f"- **Hitabet ve Sorgulama Analizi:** {donut_b3}")

st.divider()
st.subheader("Oturum Sonu Yansıtıcı Günlük")
with st.form("journal_form"):
    soru_1_etiket = (
        "Bu yeni senaryoda önceki oturumlardan edindiğiniz hangi stratejiyi kullandınız?"
        if is_transfer
        else "İlk müdahaleniz ve kök neden dönütü sonrası eylem sıranızda/hitabetinizde neyi değiştirdiniz?"
    )
    j_s1 = st.text_area(soru_1_etiket, height=75)
    j_s2 = st.text_area("Materyali adım adım uygulatırken hangi aşamada zorlandınız ve nasıl aştınız?", height=75)
    j_s3 = st.text_area("Bu deneyim gerçek sınıf ortamındaki öğrenci davranışlarına bakış açınızı nasıl etkiledi?", height=75)
    j_submitted = st.form_submit_button("Yansıtıcı Günlüğü Kaydet")

if j_submitted:
    save_journal_entry({
        "anonim_kod": anon_code,
        "oturum_no": oturum_no,
        "profil_adi": prof["profil"],
        "kazanim": kazanim_secimi,
        "soru_1": j_s1,
        "soru_2": j_s2,
        "soru_3": j_s3,
    })
    st.success("Yansıtıcı günlük kaydı yerel ortama eklendi.")

st.divider()
st.subheader("Dönem Sonu Bireysel Gelişim Portfolyosu")
user_logs = load_session_logs(anon_code)
if user_logs:
    st.dataframe(user_logs, use_container_width=True)
    st.download_button(
        label="Bireysel Gelişim Portfolyosunu İndir (JSON)",
        data=json.dumps(user_logs, ensure_ascii=False, indent=2),
        file_name=f"portfolyo_{anon_code}.json",
        mime="application/json",
    )
else:
    st.caption(f"`{anon_code}` kodu için henüz kayıtlı oturum verisi bulunmuyor.")
