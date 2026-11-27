import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="2024 TYMM - Ultra Detaylı Akademik Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
    <style>
    .sade-kart {
        background-color: #F8FAFC; border: 1px solid #CBD5E1;
        border-left: 5px solid #1D4ED8; border-radius: 8px;
        padding: 20px 24px; margin-bottom: 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .baslik-mavi { color: #1E3A8A; font-weight: 800; font-size: 1.2rem; margin-bottom: 12px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; }
    .rozet {
        display: inline-block; background-color: #EFF6FF; color: #1D4ED8;
        border: 1px solid #BFDBFE; padding: 4px 12px; border-radius: 12px;
        font-size: 0.9rem; font-weight: 700; margin-bottom: 8px;
    }
    .transkript-kutu {
        background-color: #FFFFFF; border: 1px solid #94A3B8; border-radius: 8px;
        padding: 24px; line-height: 1.7; font-size: 0.95rem;
    }
    .anlik-bildirim {
        background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 15px; 
        margin-top: 10px; margin-bottom: 15px; border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

if "simulasyon_gecmisi" not in st.session_state: st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state: st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state: st.session_state.secili_ogrenciler = []
if "otur_seed" not in st.session_state: st.session_state.otur_seed = random.randint(1, 1000)

UNIVERSITELER = [
    "Seçiniz...", "Kahramanmaraş Sütçü İmam Üniversitesi", "Ankara Üniversitesi", "Gazi Üniversitesi", 
    "Hacettepe Üniversitesi", "Marmara Üniversitesi", "Boğaziçi Üniversitesi", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 
    "Yıldız Teknik Üniversitesi", "Ege Üniversitesi", "Dokuz Eylül Üniversitesi", "Çukurova Üniversitesi", "Diğer"
]

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ VE BİLİŞSEL DETAYLARI
# ==========================================
ogrenci_profilleri = {
    "Kerem": {"durum": "Disleksi", "ikon": "👦", "mimik": "Basamaklara ve harflere odaklanmakta zorlanıyor, gözlerini kısıyor", "ozellik": "Rakamları ve sembolleri ters algılayabilir; görsel-dokunsal ayrıştırmaya ve renk kodlu yönlendirmelere ihtiyaç duyar."},
    "Arda": {"durum": "Otizm Spektrumu", "ikon": "👦", "mimik": "Kulaklık takılı, hafifçe ileri geri sallanıyor", "ozellik": "Ani seslere ve belirsiz yönergelere aşırı hassastır; soyut metaforlar yerine net, ardışık ve öngörülebilir yönergeler bekler."},
    "Can": {"durum": "Üstün Yetenekli", "ikon": "👦", "mimik": "Sabırsızca parmak kaldırıyor, ofluyor", "ozellik": "Rutin tekrardan ve ezberden anında kopar; kavramın felsefi nedenini, genellemesini ve formülün ispatını sorgular."},
    "Elif": {"durum": "Yüksek Kaygılı", "ikon": "👧", "mimik": "Başını öne eğmiş, elleriyle sırayı sıkıyor", "ozellik": "Hata yapmaktan aşırı çekinir; akademik baskı hissederse donup kalır (fight/flight/freeze), önce yargısız bir güven alanı ister."},
    "Zeynep": {"durum": "DEHB", "ikon": "👧", "mimik": "Sürekli etrafa bakınıyor, kalemiyle ritim tutuyor", "ozellik": "Sürdürülebilir dikkati kısadır; uzun sözel anlatımlarda kopar. Harekete dayalı, aktif katılımlı ve kısa döngülü görevlere ihtiyaç duyar."},
    "Mehmet": {"durum": "İşitme Yetersizliği", "ikon": "👦", "mimik": "Konuşanın dudaklarına ve mimiklerine odaklanmış", "ozellik": "Sadece işitsel olan yönergeleri kaçırır; tahtadaki yazılı pekiştireçlere, net dudak okuma açılarına ve güçlü görsel ipuçlarına dayanır."},
    "Ayşe": {"durum": "Az Gören", "ikon": "👧", "mimik": "Materyale çok yakından bakıyor, kağıda eğilmiş", "ozellik": "Küçük puntolu, karmaşık görsellerde kaybolur; yüksek kontrastlı, dokunarak hissedilebilen materyaller ve ekran büyütücü destekler bekler."},
    "Ali": {"durum": "Diskalkuli", "ikon": "👦", "mimik": "Parmaklarıyla gizlice saymaya çalışıyor, kaşları çatık", "ozellik": "Sayıların büyüklük (nicelik) ilişkisini ve işlemsel akıl yürütmeyi zihinde kuramaz; mutlaka fiziksel (somut) manipülatiflerle kavramı inşa etmesi gerekir."},
    "Merve": {"durum": "Bedensel Yetersizlik", "ikon": "👧", "mimik": "Elleri sırasında, bedensel hareketleri kısıtlı ama gözleri odaklı", "ozellik": "Bilişsel hiçbir engeli yoktur ancak yoğun çizim, kesme-biçme veya ince motor beceri gerektiren materyallerde teknolojik/akran erişilebilirlik desteği şarttır."},
    "Burak": {"durum": "Düşük Motivasyon", "ikon": "👦", "mimik": "Kolları bağlı, sıraya yayılmış, ilgisiz bakıyor", "ozellik": "Soyut kuralların \"ne işe yarayacağını\" sorgular; matematiğin gerçek yaşamla, mesleklerle veya kendi ilgi alanlarıyla otantik bir bağı kurulmadıkça direnç gösterir."}
}

MATERYAL_SECENEKLER = [
    "Seçiniz...", 
    "Materyal Kullanmadan (Sadece Sözel/Soyut İletişimle) İlerle",
    "Kendi Geliştirdiğim / Tasarladığım Materyal",
    "Somut Materyal (Onluk Taban Blokları, Kesir Takımı, Cebir Karoları, Birim Küpler vb.)",
    "Dinamik Matematik Yazılımı (GeoGebra, Desmos, Tinkercad)", 
    "Yüksek Kontrastlı Görsel & Dokunsal Kartlar",
    "Günlük Yaşam Nesneleri ve Hassas Ölçüm Araçları (Terazi, Mezura vb.)", 
    "Geometrik Şekil / 3D Açınım ve Simetri Aynaları",
    "Koordinat / Grafik / Tablo Çalışma Panosu (Çivili Tahta - Geoboard)", 
    "Olasılık ve Veri Deneyi Araçları (Zar, Çark, Renkli Toplar, Gerçek Anket Verisi)",
    "Klasik Çalışma Kâğıdı / Yaprak Test / Formül Özeti"
]

# ==========================================
# 2. DİNAMİK YAPAY ZEKA ŞIK ÜRETİCİSİ
# ==========================================
def dinamik_eylem_secenekleri_uret(tema, kazanim_kod, surec, kriz):
    tema_kisa = tema.split(":", 1)[1].strip() if ":" in tema else tema
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    kriz_kisa = (kriz[:60] + '...') if len(kriz) > 60 else kriz

    e1_secenekler = [
        "Seçiniz...",
        f"Öğrencinin '{kriz_kisa}' krizinde yaşadığı duygusal yükü onaylayıp, ona yargısız ve güvenli bir pedagojik alan açmak (Duyuşsal)",
        f"Öğrencinin yanına eğilerek '{surec_kisa}' adımında onu neyin durdurduğunu samimi ve sakin bir ses tonuyla sormak (Duyuşsal)",
        f"Tüm sınıfın '{tema_kisa}' akışını bozmadan, öğrenciye zihinsel toparlanması için bireysel esneklik ve zaman tanımak (Duyuşsal)",
        f"Öğrenci kriz yaşadığında doğrudan sınıf kurallarını hatırlatıp onu disiplinli bir şekilde derse odaklanmaya zorlamak (Disiplin/Otoriter)",
        f"Öğrencinin hislerini göz ardı edip derhal '{kazanim_kod}' hedefinin akademik tanımını yüksek sesle tekrar etmek (Bilişsel Baskı)",
        f"Kriz anını hiç yaşanmamış gibi varsayıp '{kazanim_kod}' anlatımına tahtada aynı hızda devam etmek (Görmezden Gelme)"
    ]

    e2_secenekler = [
        "Seçiniz...",
        f"Materyal üzerinden açık uçlu sorular sorarak '{surec_kisa}' ardındaki matematiksel ilişkiyi öğrencinin bizzat keşfetmesini sağlamak (Yapılandırmacı/Keşif)",
        f"'{tema_kisa}' kavramını öğrencinin kendi hayatından bir bağlamla eşleştirip, durumu kendi kelimeleriyle ifade etmesine rehberlik etmek (Yapılandırmacı/Keşif)",
        f"Karmaşık gelen '{kazanim_kod}' hedefini parçalara bölerek, kavramı farklı bir temsile (şekilden tabloya vb.) dönüştürmesini sağlamak (Temsil Dönüşümü)",
        f"İlk durumu birlikte modelleyip, benzer bir senaryoyu öğrenciye bırakarak '{surec_kisa}' için kendisinin kural genellemesi yapmasını istemek (Tümevarım/Keşif)",
        f"Zaman kaybetmemek adına '{kazanim_kod}' kuralını/formülünü doğrudan defterine yazdırıp derhal ezberlemesini istemek (Geleneksel/Ezber)",
        f"Öğrenci zorlandığı için o kısmı atlayıp, işlemleri onun yerine tahtada hızlıca çözerek doğru cevabı göstermek (Pasifleştirme)"
    ]
    return e1_secenekler, e2_secenekler

# ==========================================
# 3. KAPSAMLI YAPAY ZEKA DEĞERLENDİRME VE GELİŞİM MOTORU
# ==========================================
def kapsamli_ai_degerlendirmesi(eylem1, eylem2, materyal, mat_aciklama, sesli_girdi, ogr_durumlar, onceki_rapor, kazanim_obj):
    e1_tur = "duyussal" if any(kw in eylem1 for kw in ["kabul edip", "kabul ederek", "neyi kaçırdığını", "bireysel toparlanma", "kendi hızında", "onaylayıp"]) else "bilissel"
    if any(kw in eylem1 for kw in ["disiplinli", "doğrudan ilerlemek", "Otoriter", "zorlamak", "Bilişsel Baskı"]): e1_tur = "disiplin"

    e2_tur = "kesif" if any(kw in eylem2 for kw in ["keşfetmesini", "kendi ifadesiyle", "yeniden denetmek", "genelleme aramak", "Tümevarım"]) else "ezber"
    if any(kw in eylem2 for kw in ["ezberlemesini", "atlayarak", "Pasifleştirme", "Geleneksel"]): e2_tur = "ezber"
    
    puan = 100
    hatalar_ve_sebepleri = []
    pedagojik_oneriler = []
    mat_raporu = ""
    materyalsiz = materyal == "Materyal Kullanmadan (Sadece Sözel/Soyut İletişimle) İlerle"

    # 3.1. Pedagojik Sıralama ve Kriz Yönetimi Değerlendirmesi
    if e1_tur == "duyussal" and e2_tur == "kesif":
        pedagojik_oneriler.append("✅ Eylem Sırası Yönetimi: Önce öğrencinin duyuşsal (psikolojik) krizini yatıştırdınız, ardından bilişsel keşif sürecini başlattınız. Bu sıralama mükemmel.")
    elif e1_tur == "disiplin":
        puan -= 25
        hatalar_ve_sebepleri.append("❌ Hata (Kriz Yönetimi): Kriz anında doğrudan otoriteye, kurallara veya ilerlemeye odaklandınız.\n   *Sebep/Sonuç:* Özel gereksinimli (örn: Yüksek Kaygılı, Otizm Spektrumu) öğrencilerde bu yaklaşım krizin derinleşmesine, öğrencinin içe kapanmasına (freeze) veya dersten kopmasına neden olur.")
        pedagojik_oneriler.append("💡 Öneri: Kriz anında öğrencinin duygusunu kabul eden (empati kuran) ve ona toparlanması için güvenli alan tanıyan 'duyuşsal' eylemlerle sürece giriş yapın.")
    elif e1_tur == "bilissel" and (e2_tur == "ezber" or e2_tur == "kesif"):
        puan -= 15
        hatalar_ve_sebepleri.append("❌ Hata (Pedagojik Sıralama): Öğrencinin kriz anındaki psikolojik ihtiyacını atlayarak doğrudan akademik/bilişsel hedefe yöneldiniz.\n   *Sebep/Sonuç:* Duygusal olarak regüle olmamış (sakinleşmemiş) bir beyin yeni bilgiyi işlemleyemez. Yaklaşımınız havada kalacaktır.")
        pedagojik_oneriler.append("💡 Öneri: Maslow teorisi gereği, önce güvenlik/duygu ihtiyacını karşılayın, ardından Bloom taksonomisindeki bilişsel adımlara geçin.")
    
    # 3.2. 2024 TYMM Süreç Bileşenleri Uyumu
    if e2_tur == "ezber":
        puan -= 25
        hatalar_ve_sebepleri.append("❌ Hata (TYMM Süreç Uyumu): Öğrenci zorlandığında kavramı doğrudan verip, formülü ezberletme veya adımı atlama yolunu seçtiniz.\n   *Sebep/Sonuç:* 2024 Türkiye Yüzyılı Maarif Modeli 'beceri ve süreç' odaklıdır. Sonuç odaklı ezber, kalıcı anlamlandırmayı yok eder.")
        pedagojik_oneriler.append("💡 Öneri: Öğrenciye kuralı dikte etmek veya onun yerine çözmek yerine; sorularla, alt problemlere bölerek veya tümevarım yaptırarak kendi keşfini yapmasına rehberlik edin.")

    # 3.3. Materyal ve Somutlaştırma Değerlendirmesi
    if materyalsiz:
        if "Diskalkuli" in ogr_durumlar or "Az Gören" in ogr_durumlar or "Disleksi" in ogr_durumlar:
            puan -= 30
            hatalar_ve_sebepleri.append(f"❌ KRİTİK HATA (Kapsayıcılık/Materyal): {ogr_durumlar[0]} profiline sahip bir öğrenciye tamamen SÖZEL ve SOYUT bir anlatım seçtiniz.\n   *Sebep/Sonuç:* Bu profiller zihinsel sembolleştirmeyi tek başına yapamaz. Materyal kullanılmaması öğrenmeyi imkânsız hale getirir.")
        else:
            puan -= 20
            hatalar_ve_sebepleri.append("❌ Hata (Somutlaştırma Eksikliği): Soyut matematiksel krizleri sadece konuşarak aşmayı denediniz.\n   *Sebep/Sonuç:* Ortaokul dönemi somuttan soyuta geçiş evresidir. Öğrencinin tutunacağı fiziksel bir dal kalmamıştır.")
        
        oneri_mat = kazanim_obj.get("somut_materyal_onerisi", "Uygun somut manipülatifler.")
        pedagojik_oneriler.append(f"💡 Materyal Önerisi: Bu kazanım için müfredat ve profil bağlamında özellikle şu materyalleri kullanmalısınız: **{oneri_mat}**")
        mat_raporu = "Materyal kullanımı reddedilerek sınıf içi iletişim kısıtlanmıştır."
    
    elif materyal == "Klasik Çalışma Kâğıdı / Yaprak Test / Formül Özeti":
        puan -= 15
        hatalar_ve_sebepleri.append(f"❌ Hata (Yanlış Materyal): Seçtiğiniz '{materyal}', {ogr_durumlar[0]} krizini çözmekte etkisiz bir geleneksel araçtır.\n   *Sebep/Sonuç:* Klasik kağıtlar sadece soyut tekrardır, kavramın özünü (nasıl/neden) göstermez.")
        oneri_mat = kazanim_obj.get("somut_materyal_onerisi", "Görsel ve dinamik araçlar.")
        pedagojik_oneriler.append(f"💡 Materyal Önerisi: İki boyutlu testler yerine şu araçlara yönelin: **{oneri_mat}**")
        mat_raporu = "Seçilen materyal, yapılandırmacı sürece katkı sağlamayan pasif bir araçtır."
        
    else:
        if len(mat_aciklama.strip()) < 40:
            puan -= 10
            hatalar_ve_sebepleri.append("❌ Hata (Yüzeysel Planlama): Materyali nasıl kullanacağınızı yeterince detaylandırmadınız.\n   *Sebep/Sonuç:* Teoride doğru materyali seçmiş olsanız da, sahada bu materyalin adım adım nasıl devreye gireceği belirsizdir.")
            pedagojik_oneriler.append("💡 Öneri: Materyali masaya koymak yetmez. Öğrencinin materyale nasıl dokunacağını, hangi aşamada neyi fark etmesini beklediğinizi adım adım yazmalısınız.")
            mat_raporu = f"Seçilen '{materyal}' doğru bir araçtır ancak eylem planı (nasıl kullanılacağı) yüzeysel geçilmiştir."
        else:
            mat_raporu = f"Seçilen '{materyal}', hem öğrencinin gereksinimine hem de TYMM yapısına çok uygundur. Uygulama planınız detaylı ve sahadaki karşılığı güçlüdür."

    # 3.4. İletişim ve Hitabet Değerlendirmesi
    if len(sesli_girdi.strip()) < 20 and not materyalsiz:
        puan -= 10
        hatalar_ve_sebepleri.append("❌ Hata (İletişim Eksikliği): Öğrenciyle kurduğunuz sözlü iletişim metni çok yetersiz.\n   *Sebep/Sonuç:* Doğru materyali kullansanız bile öğrenciyi yönlendirecek, ona güven verecek didaktik hitabetiniz (öğretmen dili) eksik kalmış.")

    # 3.5. Gelişim Takibi Modülü (Önceki Rapora Göre)
    gelisim_metni = ""
    if onceki_rapor and onceki_rapor.strip():
        if puan >= 85:
            gelisim_metni = "🌟 **Gelişim İlerlemesi:** Sisteme yüklediğiniz önceki ders hedefleri incelendiğinde; bu derste eski hatalarınızdan arındığınız, 2024 TYMM felsefesine ve kapsayıcı eğitime tam uygun, oldukça olgun bir pedagojik refleks gösterdiğiniz tespit edilmiştir."
        else:
            gelisim_metni = "⚠️ **Gelişim Uyarısı:** Önceki ders raporunuzdaki hedef ve tespitlere rağmen; bu kriz simülasyonunda da süreç yönetiminde ve kriz-materyal eşleştirmesinde benzer stratejik zayıflıkların devam ettiği saptanmıştır. Lütfen aşağıdaki spesifik hata nedenlerini ve önerileri dikkatle inceleyiniz."
    else:
        gelisim_metni = "ℹ️ **Gelişim Takibi:** Sisteme bir önceki staj/ders raporunuz yüklenmediği veya boş bırakıldığı için, geçmiş performansınıza kıyasla bir ilerleme analizi (yansıtıcı düşünme) yapılamamıştır."

    rapor_metni = f"**📊 Sistem ve Rubrik Temelli Detaylı Puanınız: {max(0, puan)} / 100**\n\n"
    rapor_metni += "### 📈 Gelişim ve İlerleme Takibi (Yansıtıcı Düşünme)\n"
    rapor_metni += f"- {gelisim_metni}\n\n"
    rapor_metni += "### ⚠️ Yapılan Hatalar ve Akademik Sebepleri\n"
    if hatalar_ve_sebepleri:
        for h in hatalar_ve_sebepleri: rapor_metni += f"{h}\n\n"
    else:
        rapor_metni += "- Tebrikler. Duyuşsal destekten bilişsel keşfe geçişte, pedagojik süreç yönetiminizde hiçbir hata bulunmamaktadır.\n\n"

    rapor_metni += "### 🛠️ Materyal Kullanım Değerlendirmesi\n"
    rapor_metni += f"- {mat_raporu}\n\n"
    rapor_metni += "### 💡 Kapsamlı Pedagojik Öneriler\n"
    if pedagojik_oneriler:
        for o in pedagojik_oneriler: rapor_metni += f"{o}\n\n"
    else:
        rapor_metni += "- 2024 TYMM'nin beceri temelli yapısına ve özel gereksinimli profillerin kapsayıcılık ilkelerine eksiksiz biçimde uydunuz. Mevcut yaklaşımınızı diğer kazanımlarda da sürdürünüz.\n"

    return puan, rapor_metni

def ai_profil_davranisi_uret(ogrenci_adi, sinif, tema, kazanim_kod, kazanim_cikti, surec, temel_kriz, aday_sozu="", eylem_1="", eylem_2="", materyal_etiketi=""):
    profil = ogrenci_profilleri[ogrenci_adi]
    durum = profil["durum"]
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    mudahale_var = bool(aday_sozu.strip() or eylem_1 or materyal_etiketi)
    
    e1_tur = "duyussal" if any(kw in eylem_1 for kw in ["kabul", "neyi kaçırdığını", "bireysel toparlanma", "kendi hızında", "onaylayıp"]) else "diger"
    e2_tur = "kesif" if any(kw in eylem_2 for kw in ["keşfetmesini", "kendi ifadesiyle", "yeniden denetmek", "genelleme aramak", "Tümevarım"]) else "ezber"
    
    d1 = (e1_tur == "duyussal")
    d2 = (e2_tur == "kesif")

    materyalsiz = (materyal_etiketi == "Materyal Kullanmadan (Sadece Sözel/Soyut İletişimle) İlerle")

    if not mudahale_var:
        return f"*{ogrenci_adi} ({durum}):* `{kazanim_kod}` ({surec_kisa}) adımında '{temel_kriz}' zorluğunu yaşar ve profiline ({profil['ozellik']}) uygun bir destek arar."

    soz_ozet = aday_sozu.strip()[:65]

    if materyalsiz and durum in ["Diskalkuli", "Az Gören", "Disleksi"]:
        return f"*{ogrenci_adi} ({durum}):* Öğretmenin sözlerine rağmen ortada hiçbir somut materyal/araç olmadığı için zihinsel olarak konudan tamamen kopar ve kriz derinleşir."
    
    if not (d1 and d2):
        return f"*{ogrenci_adi} ({durum}):* Öğretmenin \"{soz_ozet}...\" demesine rağmen, '{surec_kisa}' basamağında seçilen yaklaşım ({profil['ozellik']}) ihtiyacına uymadığı için gerginliği sürer."

    mat_isim = "yönlendirmeler" if materyalsiz else f"'{materyal_etiketi}'"
    return f"*{ogrenci_adi} ({durum}):* Öğretmenin duyuşsal yaklaşımıyla sakinleşir ve {mat_isim} desteği sayesinde `{kazanim_kod}` ilişkisini kendi kendine yapılandırmaya başlar."

# ==========================================
# 4. 2024 TYMM ORTAOKUL MATEMATİK TAM MÜFREDATI (MATERYAL ÖNERİLERİYLE)
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler", "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler", "3. Tema: Geometrik Nicelikler", "4. Tema: İstatistiksel Araştırma Süreci", "5. Tema: Veriden Olasılığa"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1", 
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme", 
                    "surec": ["a) Çok basamaklı sayılar hakkında bilgi toplar.", "b) Ortak özellikleri belirler.", "c) Farklılıkları belirler.", "ç) Örüntüler üzerinden önermelerde bulunur."], 
                    "hook": "Kütüphane arşiv kodlama sistemi veya astronomik uzaklıklar.", 
                    "kriz": "Sıfır içeren bölükleri (ör: 100.005) okurken basamakları atlar veya karıştırır.",
                    "somut_materyal_onerisi": "Çok tabanlı bloklar (MAB), basamak değer kartları, renkli pullar ve bölük tabloları."
                },
                {
                    "kod": "MAT.5.1.4", 
                    "cikti": "Kesirlerin farklı gösterimlerini ve sayı doğrusundaki yerlerini ilişkilendirebilme", 
                    "surec": ["a) Basit, bileşik ve tam sayılı kesirleri inceler.", "b) Denk kesirleri modeller ve karşılaştırır."], 
                    "hook": "Mutfak ölçülerinde veya pasta paylaşımlarında çeyrek/yarım ilişkileri.", 
                    "kriz": "Payda büyüdükçe (ör: 1/8 < 1/4) kesrin küçüldüğünü zihnen kabullenmekte zorlanır.",
                    "somut_materyal_onerisi": "Kesir takımları, dairesel kesir dilimleri, katlanabilir şeffaf kesir kartları ve Cuisenaire çubukları."
                },
                {
                    "kod": "MAT.5.1.7", 
                    "cikti": "Kesir, ondalık ve yüzde gösterimleri arasındaki ilişkileri yorumlayabilme", 
                    "surec": ["a) Yüzlük kart ve modeller üzerinden eşleştirir.", "b) Farklı gösterimler arasında dönüşüm yapar."], 
                    "hook": "Cep telefonu batarya doluluk yüzdesi veya mağaza indirim etiketleri.", 
                    "kriz": "Ondalık kısmı yüzdeye çevirirken basamak değerlerini (ör: 0,2 = %20 yerine %2 yazar) karıştırır.",
                    "somut_materyal_onerisi": "100'lük kare ızgaralar (yüzlük kartlar), onluk taban bloklarının yüzlük düzlemleri."
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.5.2.1", 
                    "cikti": "Temel geometrik çizimler (nokta, doğru, ışın) için araç ve teknolojiden yararlanabilme", 
                    "surec": ["a) Uygun araçlarla çizer.", "b) Özelliklerini ve ilişkilerini açıklar."], 
                    "hook": "Mahalle krokisindeki sokakların kesişimi ve uzanışı.", 
                    "kriz": "Işın ile doğru parçasının uç noktalarındaki sonsuzluk farkını algılayamaz.",
                    "somut_materyal_onerisi": "GeoGebra geometri modülü, ipler, elastik bantlar ve çivili tahta (Geoboard)."
                }
            ],
            "3. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.3.2", 
                    "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkileri yorumlayabilme", 
                    "surec": ["a) Birim karelerle alan/çevre hesaplar.", "b) Çevreleri eşit dikdörtgenlerin alanlarını karşılaştırır."], 
                    "hook": "Belirli uzunluktaki çit teliyle en geniş bahçe parselini oluşturma tasarımı.", 
                    "kriz": "Çevre formülü ile alan hesaplama mantığını birbirine karıştırarak iç bölgeyi saymak yerine kenarları çarpar.",
                    "somut_materyal_onerisi": "İzometrik kağıt, birim kare plastik küpler ve çevre ipi."
                }
            ],
            "4. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.4.1", 
                    "cikti": "Kategorik veriyle çalışabilme ve veriye dayalı karar verebilme", 
                    "surec": ["a) Araştırma sorusu oluşturur ve veri toplar.", "b) Sıklık tablosu ve sütun grafiğiyle görselleştirir.", "c) Veriyi analiz edip yorumlar."], 
                    "hook": "Okul kantininde en çok satılması gereken sağlıklı ürünlerin araştırılması.", 
                    "kriz": "Sütun grafiği çizerken eksenleri eşit ölçeklendirmeyi unutur veya eksen isimlerini yazmaz.",
                    "somut_materyal_onerisi": "Renkli yapışkan notlar (post-it) ile tahtada canlı sütun grafiği inşası, Excel grafik araçları."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.5.1", 
                    "cikti": "Herhangi bir olayın olasılığının 0 ile 1 arasında olduğunu yorumlayabilme", 
                    "surec": ["a) İmkânsız, olası ve kesin olayları inceler.", "b) Olayların ihtimalini 0-1 aralığına yerleştirir."], 
                    "hook": "Hava durumu raporlarındaki yağmur ihtimali ve kura çekimi.", 
                    "kriz": "Olasılığı 1'den büyük bir tam sayı olarak ifade etmeye çalışır (ör: İhtimal 5'tir).",
                    "somut_materyal_onerisi": "Torba içine konan renkli toplar, olasılık çarkı (spinner)."
                }
            ]
        }
    },
    "6. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler", "2. Tema: İşlemlerle Cebirsel Düşünme", "3. Tema: Geometrik Şekiller", "4. Tema: Geometrik Nicelikler", "5. Tema: İstatistiksel Araştırma Süreci", "6. Tema: Veriden Olasılığa"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1", 
                    "cikti": "Doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme", 
                    "surec": ["a) Varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Modellerle gösterir."], 
                    "hook": "Farklı otobüs hatlarının duraktan aynı anda kalkış saatlerinin tespiti.", 
                    "kriz": "Çarpan ile kat kavramlarını zıt algılar; sayıyı büyütmesi gerekirken küçültür.",
                    "somut_materyal_onerisi": "Cuisenaire çubukları ile uzunlukları eşitleme modelleri, çarpım tablosu yüzlük ızgarası."
                },
                {
                    "kod": "MAT.6.1.6", 
                    "cikti": "Tam sayıları ve sayı doğrusunda sıralanışını yorumlayabilme", 
                    "surec": ["a) Yönlü sayıları gerçek yaşamla ilişkilendirir.", "b) Sayı doğrusunda sıralar ve mutlak değeri yorumlar."], 
                    "hook": "Asansör katları (zemin altı) veya kış mevsiminde Erzurum hava sıcaklıkları.", 
                    "kriz": "Negatif sayılarda rakamsal değer büyüdükçe (ör: -10) sayının aslında küçüldüğünü algılamakta zorlanır.",
                    "somut_materyal_onerisi": "Dikey ve yatay fiziksel sayı doğruları, termometre modelleri."
                }
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.6.2.1", 
                    "cikti": "Nicelikleri cebirsel ifadelerle modelleyebilme", 
                    "surec": ["a) Sabit ve değişkeni belirler.", "b) İlişkiyi tablo/cebirsel temsil eder."], 
                    "hook": "Kumbaradaki başlangıç parasına her hafta eklenen sabit harçlığın formülize edilmesi.", 
                    "kriz": "Harf sembolünün (x, y) sadece bir etiket değil, değişebilen herhangi bir sayı olduğunu anlamaz.",
                    "somut_materyal_onerisi": "Cebir karoları (Algebra tiles), kapalı kutu (bilinmeyen) ve misket modellemesi."
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1", 
                    "cikti": "Açı çeşitlerini ve iki paralel doğru ile bir kesenin oluşturduğu açıları sınıflandırabilme", 
                    "surec": ["a) Komşu, tümler, bütünler açıları inceler.", "b) Paralel doğru/kesen ile yöndeş, iç/dış ters açıları sınıflandırır."], 
                    "hook": "Tren raylarındaki çapraz makaslar ve köprü direk tasarımları.", 
                    "kriz": "Kesen doğru eğik olduğunda veya şekil döndürüldüğünde Z, U kuralını, yöndeş açıları göremez.",
                    "somut_materyal_onerisi": "Hareketli açı çubukları, GeoGebra açı kaydırma modülü, şeffaf asetat kağıtları."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.1", 
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarına yansıtma yapabilme", 
                    "surec": ["a) Dikdörtgen alan bağıntısından yola çıkar.", "b) Parçalama-birleştirme ile üçgen/paralelkenar alanı çıkarır."], 
                    "hook": "Yamuk veya paralelkenar şeklindeki tarla parsellerinin alanının hesabı.", 
                    "kriz": "Üçgenin alanını hesaplarken yüksekliği tabanla çarpıp ikiye bölmeyi unutarak, onu dikdörtgen sanır.",
                    "somut_materyal_onerisi": "Noktalı kağıt, makasla kesilip dikdörtgene dönüştürülebilen karton paralelkenarlar."
                },
                {
                    "kod": "MAT.6.4.2", 
                    "cikti": "Çemberin uzunluğu ile çapı arasındaki orana (pi) ilişkin çıkarım yapabilme", 
                    "surec": ["a) Farklı çemberlerin çevre ve çaplarını ölçer.", "b) Çevre/çap oranının sabitliğini geneller."], 
                    "hook": "Bisiklet tekerleğinin bir tam tur döndüğünde aldığı mesafenin ölçümü.", 
                    "kriz": "Yarıçap (r) ile çap (R) uzunluğunu formülde birbirine karıştırır.",
                    "somut_materyal_onerisi": "Farklı boylarda dairesel kapaklar, ip, cetvel ve esnek mezura."
                }
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1", 
                    "cikti": "Veriyle araştırma yapıp merkezî eğilim ve yayılımı yorumlayabilme", 
                    "surec": ["a) Araştırma sorusu oluşturur.", "b) Ortalama, ortanca, tepe değer ve açıklığı hesaplayıp yorumlar."], 
                    "hook": "Sınıfın matematik sınavı puan dağılımlarının veya okul takımı oyuncu boylarının incelenmesi.", 
                    "kriz": "Açıklığı (ranj) bulurken en küçük değer ile en büyük değer farkı yerine, en küçük değeri sıfır varsayar.",
                    "somut_materyal_onerisi": "Fiziksel boy sırasına girme etkinliği, blok dizilimleriyle ortalama alma (düzleştirme) modelleri."
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1", 
                    "cikti": "Bir olayın olasılığını deneysel gözleme dayalı tahmin edebilme", 
                    "surec": ["a) Deney çıktılarını kaydeder.", "b) Deneme sayısı arttıkça göreli sıklığın kararlılığını yorumlar."], 
                    "hook": "Madeni paranın 10 kez atılması ile 1000 kez atılması sonuçlarının kıyaslanması.", 
                    "kriz": "Kısa bir denemede üst üste 3 kez tura gelince, olasılığın değiştiğini ve sıradakinin kesin yazı geleceğini sanır (Kumarbaz yanılgısı).",
                    "somut_materyal_onerisi": "Madeni paralar, zar, dijital olasılık simülatörleri."
                }
            ]
        }
    },
    "7. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler", "2. Tema: Cebirsel Düşünme", "3. Tema: Dönüşüm Geometrisi", "4. Tema: Geometrik Nicelikler", "5. Tema: Geometrik Şekiller", "6. Tema: İstatistiksel Araştırma", "7. Tema: Olasılık"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.3", 
                    "cikti": "Doğru ve ters orantı durumlarını ayırt etme ve problem çözme", 
                    "surec": ["a) Nicelikler arası orantı türünü belirler.", "b) Orantı sabiti ve denklemle problemi çözer."], 
                    "hook": "İşçi sayısı ile işin bitme süresi veya aynı hızda giden aracın zaman-yol ilişk.", 
                    "kriz": "Ters orantılı çokluklarda değişkenleri çarpmak (k=x.y) yerine, doğru orantıdaki gibi bölmeye çalışır.",
                    "somut_materyal_onerisi": "Denge terazisi, su kapları ve birim küpler, orantı tabloları."
                }
            ],
            "2. Tema: Cebirsel Düşünme": [
                {
                    "kod": "MAT.7.2.1", 
                    "cikti": "Birinci dereceden bir bilinmeyenli denklemleri çözebilme", 
                    "surec": ["a) Cebirsel ifadeyle modeller.", "b) Eşitliğin korunumu ilkesiyle denklemi çözer."], 
                    "hook": "Tahterevalli dengesi veya bilinmeyen ağırlık barındıran eşit kollu terazi durumları.", 
                    "kriz": "Eşitliğin karşı tarafına geçen terimin işaretini değiştirmeyi (toplamaya göre tersini almayı) unutur.",
                    "somut_materyal_onerisi": "Fiziksel denklem terazisi, cebir karoları."
                }
            ],
            "3. Tema: Dönüşüm Geometrisi": [
                {
                    "kod": "MAT.7.3.1", 
                    "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturma", 
                    "surec": ["a) Yansıma eksenine göre simetriyi inceler.", "b) Görüntüyü oluşturur ve karşılaştırır."], 
                    "hook": "Aynadaki yansımalar, göl yüzeyindeki simetri veya kelebek kanatları.", 
                    "kriz": "Çapraz simetri eksenlerinde şekli katlamak veya dik uzaklık almak yerine, şekli doğrudan aşağı öteler.",
                    "somut_materyal_onerisi": "Simetri aynası (Mira), şeffaf asetat kağıdı (katlamak için), noktalı kağıt."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.7.4.2", 
                    "cikti": "Dairenin ve daire diliminin alan bağıntılarına çıkarım yapabilme", 
                    "surec": ["a) Merkez açı ile yay/alan orantısını kurar.", "b) Alanı hesaplar."], 
                    "hook": "Pizza diliminin alan hesabı veya döner fıskiyenin suladığı bahçe alanı.", 
                    "kriz": "Dilim alanı hesaplarken tam daire (360 derece) üzerinden oran kurmayı tamamen atlar.",
                    "somut_materyal_onerisi": "Daire dilimleri takımı, iletki, GeoGebra çember modülü."
                }
            ],
            "5. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1", 
                    "cikti": "Üçgende kenarortay, açıortay ve yüksekliği çözümleyebilme", 
                    "surec": ["a) Yardımcı elemanları çizer.", "b) Özelliklerini ve kesişimlerini inceler."], 
                    "hook": "Çatı iskeletinin ağırlık merkezi (kenarortay kesişimi) ve taşıyıcı dikmeleri.", 
                    "kriz": "Yükseklik ile kenarortay kavramlarını ve çizimlerini (özellikle geniş açılı üçgende) birbirine karıştırır.",
                    "somut_materyal_onerisi": "Kağıt katlama (origami) ile açıortay/kenarortay bulma, pergel ve cetvel inşası."
                }
            ],
            "6. Tema: İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.6.1", 
                    "cikti": "Sürekli veri ile çalışıp çizgi grafiği ile analiz edebilme", 
                    "surec": ["a) Sürekli veri toplar.", "b) Çizgi grafiği çizer ve eğilimleri yorumlar."], 
                    "hook": "Bir fidanın aylara göre boy uzama grafiği veya haftalık sıcaklık değişimleri.", 
                    "kriz": "Çizgi grafiğini sürekli olmayan (kategorik - örn: sevilen renkler) veriler için kullanmaya çalışır.",
                    "somut_materyal_onerisi": "Sensör verileri toplama yazılımları, iplerle duvarda çizgi grafiği ağı örme."
                }
            ],
            "7. Tema: Olasılık": [
                {
                    "kod": "MAT.7.7.1", 
                    "cikti": "Bir olayın ve tümleyeninin olasılığına tümevarımsal akıl yürütebilme", 
                    "surec": ["a) Çıktıları gözlemler.", "b) Olay + Tümleyen = 1 ilişkisini geneller."], 
                    "hook": "Basket atışında topun potaya girmesi ve girmemesi olasılıklarının toplamı.", 
                    "kriz": "Tümleyeni bulmak için olayın olasılığını 1'den (bütünden) çıkarmak yerine farklı bir bağıntı uydurur.",
                    "somut_materyal_onerisi": "İki yüzü farklı renkli pullar, olasılık kutusu."
                }
            ]
        }
    },
    "8. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler", "2. Tema: Cebirsel Düşünme", "3. Tema: Geometrik Şekiller", "4. Tema: Geometrik Nicelikler", "5. Tema: Dönüşüm Geometrisi", "6. Tema: İstatistik", "7. Tema: Olasılık"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.2", 
                    "cikti": "Kareköklü ifadelerin yaklaşık değerini bulma ve işlem yapma", 
                    "surec": ["a) Tam kare ilişkiyi belirler.", "b) Tam kare olmayanların hangi iki sayı arasında olduğunu bulur."], 
                    "hook": "Alanı 50 metrekare olarak bilinen kare biçimindeki odanın bir kenar uzunluğunu tahmin etme.", 
                    "kriz": "Karekök bulurken sayıyı ikiye böler (Ör: Kök 36'ya 18 der, Kök 50'ye 25 der).",
                    "somut_materyal_onerisi": "Birim karelerden oluşturulan fiziksel karesel bölgeler, karekök spirali çizimi."
                }
            ],
            "2. Tema: Cebirsel Düşünme": [
                {
                    "kod": "MAT.8.2.2", 
                    "cikti": "Doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme", 
                    "surec": ["a) Tablo, grafik ve denklem geçişlerini yapar.", "b) Eğim (değişim oranı) yorumu yapar."], 
                    "hook": "Taksimetre açılış ücreti ve gidilen kilometreye göre artan fiyat grafiği.", 
                    "kriz": "Eğimi hesaplarken dikey değişim / yatay değişim yapmak yerine, tam tersi yatayı dikeye böler.",
                    "somut_materyal_onerisi": "Fiziksel rampa modelleri ile eğim ölçümü, Desmos Dinamik Grafik Çizici."
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.2", 
                    "cikti": "Pisagor bağıntısını (a²+b²=c²) yorumlayıp problem çözebilme", 
                    "surec": ["a) Dik kenarlar ve hipotenüs karelerini inceler.", "b) Bağıntıyı modelleyip uygular."], 
                    "hook": "Duvara dayalı duran bir merdivenin yüksekliği ve taban uzaklığı ilişkisi.", 
                    "kriz": "Hipotenüs uzunluğunu bulmak için dik kenarların karelerini almak yerine doğrudan kenar uzunluklarını toplar.",
                    "somut_materyal_onerisi": "Pisagor su çarkı modeli, kare ve dik üçgen puzzle'ları (Pisagor ispat panoları)."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1", 
                    "cikti": "Prizmalar, silindir, piramit ve koni açınımlarını çözümleyebilme", 
                    "surec": ["a) Yüzey şekillerini belirler.", "b) Açınım ile kapalı cisim arasındaki eşleşmeleri kurar."], 
                    "hook": "Fabrikada tasarlanan karton hediye ve ambalaj kutularının açınım planları.", 
                    "kriz": "Silindirin yanal yüzeyi açıldığında oluşan dikdörtgenin uzun kenarının, taban dairesinin çevresine eşit olduğunu göremez.",
                    "somut_materyal_onerisi": "İçinden kağıt açınım çıkan şeffaf 3D geometrik cisim setleri."
                }
            ],
            "5. Tema: Dönüşüm Geometrisi": [
                {
                    "kod": "MAT.8.5.1", 
                    "cikti": "Dik koordinat sisteminde öteleme ve yansıma dönüşümlerini yapabilme", 
                    "surec": ["a) Koordinat değişimlerine dair kuralı bulur.", "b) Ardışık dönüşümler uygular."], 
                    "hook": "Video oyunlarındaki karakterin piksel piksel eksenlere göre hareketi (Pac-Man mantığı).", 
                    "kriz": "x eksenine göre yansıma yaparken, x koordinatının sabit kalıp y koordinatının işaret değiştirmesi gerektiğini karıştırır.",
                    "somut_materyal_onerisi": "Koordinat düzlemi çizili manyetik tahta ve mıknatıslı çokgen şekilleri."
                }
            ],
            "6. Tema: İstatistik": [
                {
                    "kod": "MAT.8.6.1", 
                    "cikti": "Farklı veri setlerini ve grafikleri karşılaştırıp karar verebilme", 
                    "surec": ["a) Veri toplar.", "b) Uygun grafiği seçip yayılım/merkez analizi yapar."], 
                    "hook": "İki farklı şubenin veya iki basketbol oyuncusunun sezon boyu performans istikrarının analizi.", 
                    "kriz": "Sadece aritmetik ortalamaya bakıp karar verir; yayılımı (standart sapmayı/açıklığı) istikrar ölçütü olarak göz ardı eder.",
                    "somut_materyal_onerisi": "İki farklı hedefe atılan dart oklarının dağılım simülasyonu, histogram blokları."
                }
            ],
            "7. Tema: Olasılık": [
                {
                    "kod": "MAT.8.7.1", 
                    "cikti": "Olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı seçebilme", 
                    "surec": ["a) Karara uygun bilgi toplar.", "b) Yaklaşımları kıyaslayıp uygun olanı kullanır."], 
                    "hook": "Penaltı atışında gol olma tahmini (deneysel/öznel) ile zar atışının (teorik) farkı.", 
                    "kriz": "Deneysel olasılık (geçmiş veri) kullanılması gereken bir durumda, salt teorik olasılık diyerek kesin hüküm verir.",
                    "somut_materyal_onerisi": "Sporcu istatistik kartları, hileli/ağırlıklı zarlar."
                }
            ]
        }
    }
}
# ==========================================
# 5. UI AKIŞI (KURULUM, GELİŞİM TAKİBİ, 3D SINIF, TRANSKRİPT)
# ==========================================

# ----------------- ADIM 1 -----------------
if st.session_state.adim == 1:
    st.markdown('<span class="rozet">ADIM 1 / 3</span>', unsafe_allow_html=True)
    st.subheader("📝 2024 TYMM Kurulum ve Gelişim Takibi Paneli")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">Aday ve Danışman Bilgileri</div>', unsafe_allow_html=True)
        ogretmen_adi = st.text_input("Öğretmen Adayı *", placeholder="Örn: Mislina Taysi")
        okul_numarasi = st.text_input("Okul Numarası *", placeholder="Örn: 20220000000")
        universite_adi = st.selectbox("Üniversite Seçimi *", UNIVERSITELER, index=1)
        uygulama_ogretim_elemani = st.text_input("Uygulama Öğretim Elemanı *")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">Rubrik ve Gelişim Takibi (Yansıtma)</div>', unsafe_allow_html=True)
        rubrik_metni = st.text_area(
            "Değerlendirme Rubriği (AI Bu Kriterleri Esas Alacaktır) *",
            value="1. Kapsayıcı ve duyuşsal iletişim (25 Puan).\n2. Pedagojik eylem sırası (25 Puan).\n3. Profile ve kazanıma uygun materyal seçimi/kullanımı (30 Puan).\n4. 2024 TYMM keşif odaklı süreç uyumu (20 Puan).",
            height=80,
        )
        st.markdown('**Önceki Dersin Raporu / Yansıtma Notu**')
        onceki_rapor = st.text_area(
            "Gelişiminizi görebilmemiz için önceki dersteki hata/hedefleriniz:",
            placeholder="Örn: Bir önceki stajımda kriz anında öğrenciyi dinlemeden doğrudan tahtada kuralı vermiştim, somutlaştırma yapmamıştım. Bu derste materyal kullanımına odaklanacağım...",
            height=70,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 3D Staj Simülasyonunu Başlat", type="primary", use_container_width=True):
        if not all([ogretmen_adi.strip(), okul_numarasi.strip(), uygulama_ogretim_elemani.strip(), rubrik_metni.strip()]) or universite_adi == "Seçiniz...":
            st.error("❌ Zorunlu (*) alanlar doldurulmadan ilerlenemez.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi.strip()
            st.session_state.okul_numarasi = okul_numarasi.strip()
            st.session_state.universite_adi = universite_adi
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani.strip()
            st.session_state.rubrik_metni = rubrik_metni.strip()
            st.session_state.onceki_rapor = onceki_rapor.strip() if onceki_rapor else ""
            st.session_state.adim = 2
            st.rerun()

# ----------------- ADIM 2 -----------------
elif st.session_state.adim == 2:
    st.markdown('<span class="rozet">ADIM 2 / 3</span>', unsafe_allow_html=True)
    st.markdown(f"### 🏫 3D Canlı Sınıf | Aday: {st.session_state.ogretmen_adi} - {st.session_state.universite_adi}")

    with st.expander("📚 2024 TYMM Detaylı Müfredat Seçimi", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1: secilen_sinif = st.selectbox("Sınıf Düzeyi *", list(tyym_master_arsiv.keys()))
        with col_s2: secilen_tema = st.selectbox("Tema *", tyym_master_arsiv[secilen_sinif]["Temalar"])
        kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"].get(secilen_tema, [])
        with col_s3:
            kazanim_sec = ["Seçiniz..."] + [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
            secilen_kazanim_str = st.selectbox("Kazanım / Öğrenme Çıktısı *", kazanim_sec)

        if secilen_kazanim_str == "Seçiniz...": st.stop()
        secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str)
        secilen_surec = st.selectbox("Süreç Bileşeni (Aşama) *", ["Seçiniz..."] + secilen_kazanim_obj["surec"])
        if secilen_surec == "Seçiniz...": st.stop()
        st.success(f"💡 **Bağlam:** {secilen_kazanim_obj['hook']}")

    st.markdown('<div class="sade-kart"><div class="baslik-mavi">👥 Öğrenci Seçimi (1-10 Arası Onay Kutuları) *</div>', unsafe_allow_html=True)
    ogrenci_adlari = list(ogrenci_profilleri.keys())
    secili_liste = []
    cb_cols = st.columns(5)
    for idx in range(10):
        ad = ogrenci_adlari[idx]
        bilgi = ogrenci_profilleri[ad]
        with cb_cols[idx % 5]:
            if st.checkbox(f"{bilgi['ikon']} {ad}", key=f"cb_{ad}"): secili_liste.append(ad)
            st.caption(f"{bilgi['durum']}")
    st.session_state.secili_ogrenciler = secili_liste
    st.markdown('</div>', unsafe_allow_html=True)

    if not secili_liste:
        st.error("❌ Sınıf etkileşimi için en az 1 öğrenci profili seçilmelidir.")
        st.stop()

    st.markdown("#### 🧠 Seçili Öğrencilerin Başlangıç (Kriz) Durumları")
    kart_cols = st.columns(min(len(secili_liste), 3))
    for idx, ogr_ad in enumerate(secili_liste):
        bilgi = ogrenci_profilleri[ogr_ad]
        davranis = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"])
        with kart_cols[idx % len(kart_cols)]:
            with st.container(border=True):
                st.markdown(f"**{ogr_ad} ({bilgi['durum']})**")
                st.write(davranis)

    # Dinamik Eylem Üretimi
    dinamik_eylem_1_list, dinamik_eylem_2_list = dinamik_eylem_secenekleri_uret(secilen_tema, secilen_kazanim_obj["kod"], secilen_surec, secilen_kazanim_obj["kriz"])

    col_sol, col_sag = st.columns([1.2, 0.8], gap="large")
    with col_sol:
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">🎙️ Pedagojik Müdahale Konsolu</div>', unsafe_allow_html=True)
        sesli_girdi = st.text_area("✍️ Öğrenci(ler)e doğrudan söyleyeceğiniz hitabet metni *", placeholder="Örn: Ali'cim şu an kafanın karıştığını görüyorum, bu çok normal. Hadi birlikte şu modeli inceleyelim...", height=85)
        
        eylem_1 = st.selectbox("1. Pedagojik Eylem Sırası (AI Dinamik Şıklar) *", dinamik_eylem_1_list)
        eylem_2 = st.selectbox("2. Pedagojik Eylem Sırası (AI Dinamik Şıklar) *", dinamik_eylem_2_list)
        materyal = st.selectbox("Materyal Seçimi (Kapsayıcılık Açısından Kritik) *", MATERYAL_SECENEKLER)
        
        ozgun_tanitim, ozgun_ad = "", ""
        if materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal":
            ozgun_ad = st.text_input("Özgün Materyalinizin Adı *")
            ozgun_tanitim = st.text_area("Materyali Detaylıca Tanıtın *")
            materyal_etiketi = f"{ozgun_ad} (Özgün Materyal)"
        elif materyal == "Materyal Kullanmadan (Sadece Sözel/Soyut İletişimle) İlerle":
            materyal_etiketi = materyal
        else:
            materyal_etiketi = materyal
            
        mat_label = "Sözel stratejinizi açıklayın *" if materyal == "Materyal Kullanmadan (Sadece Sözel/Soyut İletişimle) İlerle" else "Materyali nasıl (hangi adımlarla) kullanacaksınız? *"
        mat_aciklama = st.text_area(mat_label, height=85)

        if st.button("📥 Analizi Transkripte İşle ve 3. Adıma (Raporlamaya) Geç", type="primary", use_container_width=True):
            eksik_ozgun = materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal" and (not ozgun_ad.strip() or not ozgun_tanitim.strip())
            if not sesli_girdi.strip() or eylem_1 == "Seçiniz..." or eylem_2 == "Seçiniz..." or materyal == "Seçiniz..." or not mat_aciklama.strip() or eksik_ozgun:
                st.error("❌ Tüm zorunlu (*) alanları doldurunuz.")
            else:
                ai_tepkileri = {}
                for ogr_ad in secili_liste:
                    ai_tepkileri[ogr_ad] = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"], sesli_girdi, eylem_1, eylem_2, materyal_etiketi)
                
                durumlar = [ogrenci_profilleri[o]["durum"] for o in secili_liste]
                
                ai_puan, ai_mesaj = kapsamli_ai_degerlendirmesi(eylem_1, eylem_2, materyal_etiketi, mat_aciklama, sesli_girdi, durumlar, st.session_state.onceki_rapor, secilen_kazanim_obj)

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
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">💡 Canlı Analiz ve Anlık Öğrenci Dönütleri</div>', unsafe_allow_html=True)
        if eylem_1 != "Seçiniz..." and eylem_2 != "Seçiniz..." and materyal != "Seçiniz...":
            durumlar = [ogrenci_profilleri[o]["durum"] for o in secili_liste]
            gecici_etiket = f"{ozgun_ad.strip()} (Özgün Materyal)" if materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal" else materyal
            gecici_aciklama = mat_aciklama if mat_aciklama.strip() else "..."
            
            ai_puan, ai_mesaj = kapsamli_ai_degerlendirmesi(eylem_1, eylem_2, gecici_etiket, gecici_aciklama, sesli_girdi, durumlar, st.session_state.onceki_rapor, secilen_kazanim_obj)
            
            st.markdown(f"<div class='anlik-bildirim'>{ai_mesaj}</div>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Şıklara Göre Anlık Öğrenci Tepkisi:")
            for ogr_ad in secili_liste:
                gecici_soz = sesli_girdi.strip() if sesli_girdi.strip() else "İletişim kuruluyor..."
                tepki = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"], gecici_soz, eylem_1, eylem_2, gecici_etiket)
                st.write(tepki)
        else:
            st.info("👈 Sol taraftan seçimlerinizi yaptığınız anda yapay zeka, pedagojik yaklaşımınızı canlı olarak analiz edecek, hata ve önerileri burada gerekçeleriyle gösterecektir.")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- ADIM 3 -----------------
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 2024 TYMM Kapsamlı Ders Transkripti ve Öğretim Elemanı Kararı")
    
    son_kayit = st.session_state.simulasyon_gecmisi[-1]
    tab_trans, tab_hoca = st.tabs(["📝 Detaylı Rapor & Ders Transkripti", "👨‍🏫 Öğretim Elemanı Değerlendirmesi"])
    
    with tab_trans:
        st.markdown(f"<div class='anlik-bildirim'>{son_kayit['ai_mesaj']}</div>", unsafe_allow_html=True)
        ozg_metin = f"\n- **Özgün Materyal Tanıtımı:** {son_kayit['ozgun_tanitim']}" if son_kayit["ozgun_tanitim"] else ""
        
        ogrenci_satirlari = "\n".join([f"  - {t}" for ogr, t in son_kayit["ai_tepkileri"].items()])
        transkript = (
            f"**Oturum Tarihi:** {son_kayit['tarih']} \n**Aday:** {st.session_state.ogretmen_adi} ({st.session_state.universite_adi})\n"
            f"**Kazanım:** {son_kayit['kod']} ({son_kayit['surec']})\n\n"
            f"**1. Eylem (Dinamik Seçim):** {son_kayit['eylem_1']}\n**2. Eylem (Dinamik Seçim):** {son_kayit['eylem_2']}\n"
            f"**Materyal:** {son_kayit['materyal_etiketi']}{ozg_metin}\n"
            f"**Kullanım Açıklaması:** {son_kayit['mat_aciklama']}\n**Adayın Sözel Hitabeti:** {son_kayit['sesli_girdi']}\n\n"
            f"**Öğrenci Tepkileri Sonucu:**\n{ogrenci_satirlari}"
        )
        st.markdown(f"<div class='transkript-kutu'>{transkript}</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="⬇️ Yazılı Ders Transkripti ve AI Akademik Raporunu İndir (.txt)",
            data=(son_kayit['ai_mesaj'] + "\n\n=== DERS TRANSKRİPTİ ===\n\n" + transkript).replace("**", "").replace("*", "").replace("`", ""),
            file_name=f"2024_TYMM_Transkript_Rapor_{st.session_state.get('okul_numarasi', 'aday')}.txt",
            mime="text/plain",
        )

    with tab_hoca:
        st.markdown("### Danışman Öğretim Elemanı Geri Dönütü")
        hoca_notu = st.text_area("AI detaylı analiz raporunu ve adayın eylem transkriptini göz önünde bulundurarak resmî geri dönütünüzü yazın *", height=150)
        if st.button("📤 Dönütü Sisteme Kaydet", type="primary"):
            if hoca_notu.strip(): st.success("✅ Öğretim elemanı akademik geri dönütü başarıyla sisteme kaydedildi.")
            else: st.error("❌ Geri dönüt alanı boş bırakılamaz.")
                
    st.divider()
    st.warning("⚠️ Ezber/deneme-yanılma oluşmasını önlemek amacıyla aynı senaryoya geri dönülemez. Hata nedenlerini ve spesifik materyal önerilerini inceledikten sonra yepyeni bir simülasyon başlatınız.")
    if st.button("🔄 Yeni Bir Kriz Simülasyonu Başlat (Sıfırla)"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.secili_ogrenciler = []
        st.session_state.otur_seed = random.randint(1, 1000)
        st.session_state.adim = 1
        st.rerun()
