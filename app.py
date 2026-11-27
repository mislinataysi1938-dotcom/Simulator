import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="2024 TYMM - İlköğretim Matematik Staj Simülatörü",
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
    .rapor-baslik { color: #0F766E; font-weight: bold; font-size: 1.1rem; margin-top: 15px;}
    .hata-metni { color: #B91C1C; font-weight: 600; }
    .oneri-metni { color: #1D4ED8; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

if "simulasyon_gecmisi" not in st.session_state: st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state: st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state: st.session_state.secili_ogrenciler = []
if "otur_seed" not in st.session_state: st.session_state.otur_seed = random.randint(1, 1000)

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ VE BİLİŞSEL DETAYLARI
# ==========================================
ogrenci_profilleri = {
    "Kerem": {"durum": "Disleksi", "ikon": "👦", "mimik": "Basamaklara ve harflere odaklanmakta zorlanıyor, gözlerini kısıyor", "ozellik": "Rakamları ve sembolleri ters algılayabilir; görsel-dokunsal ayrıştırmaya ve renk kodlu yönlendirmelere ihtiyaç duyar."},
    "Arda": {"durum": "Otizm Spektrumu", "ikon": "👦", "mimik": "Kulaklık takılı, hafifçe ileri geri sallanıyor", "ozellik": "Ani seslere ve belirsiz yönergelere aşırı hassastır; soyut metaforlar yerine net, ardışık ve öngörülebilir yönergeler bekler."},
    "Can": {"durum": "Üstün Yetenekli", "ikon": "👦", "mimik": "Sabırsızca parmak kaldırıyor, ofluyor", "ozellik": "Rutin tekrardan ve ezberden anında kopar; kavramın felsefi nedenini, genellemesini ve formülün ispatını sorgular."},
    "Elif": {"durum": "Yüksek Kaygılı", "ikon": "👧", "mimik": "Başını öne eğmiş, elleriyle sırayı sıkıyor", "ozellik": "Hata yapmaktan aşırı çekinir; akademik baskı hissederse donup kalır, önce yargısız bir güven alanı ister."},
    "Zeynep": {"durum": "DEHB", "ikon": "👧", "mimik": "Sürekli etrafa bakınıyor, kalemiyle ritim tutuyor", "ozellik": "Sürdürülebilir dikkati kısadır; uzun sözel anlatımlarda kopar. Harekete dayalı, aktif katılımlı görevlere ihtiyaç duyar."},
    "Mehmet": {"durum": "İşitme Yetersizliği", "ikon": "👦", "mimik": "Konuşanın dudaklarına ve mimiklerine odaklanmış", "ozellik": "Sadece işitsel olan yönergeleri kaçırır; tahtadaki yazılı pekiştireçlere, net dudak okuma açılarına ve görsel ipuçlarına dayanır."},
    "Ayşe": {"durum": "Az Gören", "ikon": "👧", "mimik": "Materyale çok yakından bakıyor, kağıda eğilmiş", "ozellik": "Küçük puntolu, karmaşık görsellerde kaybolur; yüksek kontrastlı, dokunarak hissedilebilen materyaller bekler."},
    "Ali": {"durum": "Diskalkuli", "ikon": "👦", "mimik": "Parmaklarıyla gizlice saymaya çalışıyor, kaşları çatık", "ozellik": "Sayıların büyüklük (nicelik) ilişkisini ve işlemsel akıl yürütmeyi zihinde kuramaz; somut manipülatiflerle kavramı inşa etmesi gerekir."},
    "Merve": {"durum": "Bedensel Yetersizlik", "ikon": "👧", "mimik": "Elleri sırasında, bedensel hareketleri kısıtlı ama gözleri odaklı", "ozellik": "Bilişsel hiçbir engeli yoktur ancak yoğun çizim veya ince motor beceri gerektiren materyallerde erişilebilirlik desteği şarttır."},
    "Burak": {"durum": "Düşük Motivasyon", "ikon": "👦", "mimik": "Kolları bağlı, sıraya yayılmış, ilgisiz bakıyor", "ozellik": "Soyut kuralların ne işe yarayacağını sorgular; matematiğin gerçek yaşamla otantik bir bağı kurulmadıkça direnç gösterir."}
}

MATERYAL_SECENEKLER = [
    "Seçiniz...", 
    "Materyal Kullanmadan İlerle",
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
# 2. DİNAMİK YAPAY ZEKA ŞIK ÜRETİCİSİ (İPUÇSUZ)
# ==========================================
def dinamik_eylem_secenekleri_uret(tema, kazanim_kod, surec, kriz):
    tema_kisa = tema.split(":", 1)[1].strip() if ":" in tema else tema
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec

    e1_secenekler = [
        "Seçiniz...",
        f"Öğrencinin yaşadığı zorlanmayı kabul ederek ona toparlanması için zaman tanımak",
        f"Öğrencinin yanına gidip '{surec_kisa}' adımında neyi kaçırdığını sakin bir şekilde sormak",
        f"Sınıfın genel '{tema_kisa}' akışını bozmadan, öğrenciye esneklik sağlamak",
        f"Öğrenciye sınıf kurallarını hatırlatıp derse odaklanmasını söylemek",
        f"'{kazanim_kod}' hedefinin tanımını tahtada yüksek sesle tekrar etmek",
        f"'{kazanim_kod}' anlatımına plandaki hızda devam etmek"
    ]

    e2_secenekler = [
        "Seçiniz...",
        f"Materyal üzerinden sorular sorarak '{surec_kisa}' ilişkisini öğrencinin kendisinin keşfetmesini sağlamak",
        f"'{tema_kisa}' kavramını günlük yaşamdan bir örnekle açıklamasını istemek",
        f"'{kazanim_kod}' hedefini parçalara bölerek farklı bir temsile dönüştürmek",
        f"Birlikte bir model kurup, '{surec_kisa}' için öğrencinin kuralı genellemesini istemek",
        f"'{kazanim_kod}' kuralını/formülünü deftere yazdırıp ezberlemesini istemek",
        f"Zorlanılan kısmı atlayıp işlemi öğrenci yerine tahtada çözmek"
    ]
    return e1_secenekler, e2_secenekler

# ==========================================
# 3. KAPSAMLI AKADEMİK DEĞERLENDİRME MOTORU (TYMM ETKİNLİK RAPORU 5 UYUMLU)
# ==========================================
def kapsamli_ai_degerlendirmesi(eylem1, eylem2, materyal, mat_aciklama, sesli_girdi, ogr_durumlar, kazanim_obj, hoca_rubrik):
    # Eylem Türlerinin Belirlenmesi
    e1_tur = "duyussal" if any(kw in eylem1 for kw in ["kabul ederek", "neyi kaçırdığını", "esneklik sağlamak"]) else "bilissel"
    if any(kw in eylem1 for kw in ["kurallarını hatırlatıp", "devam etmek", "tekrar etmek"]): e1_tur = "disiplin"

    e2_tur = "kesif" if any(kw in eylem2 for kw in ["keşfetmesini", "örnekle açıklamasını", "temsile dönüştürmek", "genellemesini"]) else "ezber"
    if any(kw in eylem2 for kw in ["ezberlemesini", "atlayıp"]): e2_tur = "ezber"
    
    puan = 100
    kriz_yonetimi_puan = 20
    eylem_sirasi_puan = 15
    matematik_surec_puan = 20
    ogrenci_merkezlilik_puan = 15
    materyal_temsil_puan = 25
    ogrenme_kaniti_puan = 5
    
    hatalar_ve_sebepleri = []
    pedagojik_oneriler = []
    materyalsiz = materyal == "Materyal Kullanmadan İlerle"
    profil_durumu = ogr_durumlar[0]

    # 3.1. Kriz Yönetimi, İletişim ve Eylem Sırası
    if e1_tur == "duyussal" and e2_tur == "kesif":
        pedagojik_oneriler.append("✅ Kriz Yönetimi: Öğrencinin zorlanmasını duyuşsal olarak yönettiniz ve ardından bilişsel keşif sürecine geçtiniz. Sıralama pedagojik olarak uygundur.")
    elif e1_tur == "disiplin":
        puan -= 20
        kriz_yonetimi_puan -= 15
        hatalar_ve_sebepleri.append(f"<span class='hata-metni'>Hata (Kriz Yönetimi):</span> Kriz anında doğrudan disipline ve ilerlemeye odaklandınız. <br><b>Akademik Sebep/Olası Etki:</b> {profil_durumu} profiline sahip bir öğrencide bu yaklaşım, güvenliği ve katılımı zedeler, öğrencinin içe kapanmasına veya dersten tamamen kopmasına yol açar.")
        pedagojik_oneriler.append("<span class='oneri-metni'>Öneri:</span> İlk müdahale olarak öğrencinin duygusunu kabul eden, saygılı ve güvenli bir pedagojik alan (bekleme süresi veya sakin bir soru) tanıyın.")
    elif e1_tur == "bilissel" and (e2_tur == "ezber" or e2_tur == "kesif"):
        puan -= 15
        eylem_sirasi_puan -= 10
        hatalar_ve_sebepleri.append(f"<span class='hata-metni'>Hata (Pedagojik Sıralama):</span> Öğrencinin kriz anındaki psikolojik (duyuşsal) ihtiyacını atlayıp doğrudan akademik hedefe yöneldiniz. <br><b>Akademik Sebep/Olası Etki:</b> Duygusal olarak regüle olmamış (sakinleşmemiş) bir beyin yeni bilgiyi işlemleyemez.")
        pedagojik_oneriler.append("<span class='oneri-metni'>Öneri:</span> Bilişsel adımlara geçmeden önce kısa da olsa öğrenciyle empatik bir bağ kurun.")
    
    # 3.2. 2024 TYMM Süreç Bileşenleri Uyumu ve Öğrenci Merkezlilik
    if e2_tur == "ezber":
        puan -= 20
        matematik_surec_puan -= 15
        ogrenci_merkezlilik_puan -= 10
        hatalar_ve_sebepleri.append("<span class='hata-metni'>Hata (TYMM Süreç Uyumu):</span> Öğrenci zorlandığında kavramı doğrudan verip ezberletme veya işlemi onun yerine çözme yolunu seçtiniz. <br><b>Akademik Sebep/Olası Etki:</b> 2024 TYMM beceri ve süreç odaklıdır. Sonuç odaklı ezber veya öğretmenin cevabı doğrudan vermesi, kalıcı öğrenmeyi ve öğrencinin strateji üretmesini engeller.")
        pedagojik_oneriler.append("<span class='oneri-metni'>Öneri:</span> Öğrenciye formülü dikte etmek yerine; yönlendirici sorularla, alt problemlere bölerek veya kavramı farklı bir temsile dönüştürerek kendi keşfini yapmasına (tümevarım) alan bırakın.")

    # 3.3. Materyal/Temsil ve Kapsayıcılık Değerlendirmesi
    mat_raporu = ""
    oneri_mat = kazanim_obj.get("somut_materyal_onerisi", "Uygun somut manipülatifler.")
    
    if materyalsiz:
        if profil_durumu in ["Diskalkuli", "Az Gören", "Disleksi"]:
            puan -= 30
            materyal_temsil_puan -= 25
            hatalar_ve_sebepleri.append(f"<span class='hata-metni'>KRİTİK HATA (Kapsayıcılık ve Temsil):</span> {profil_durumu} profili için tamamen SÖZEL ve SOYUT bir anlatım seçtiniz. <br><b>Akademik Sebep/Olası Etki:</b> Bu profiller zihinsel sembolleştirmeyi materyal olmadan tek başına yapamaz. Materyal/temsil kullanımının reddedilmesi öğrenci için erişim engeli yaratır.")
        else:
            puan -= 20
            materyal_temsil_puan -= 15
            hatalar_ve_sebepleri.append("<span class='hata-metni'>Hata (Somutlaştırma Eksikliği):</span> Soyut matematiksel krizleri sadece konuşarak aşmayı denediniz. <br><b>Akademik Sebep/Olası Etki:</b> Öğrencinin kavramı zihninde canlandırması (modellemesi) için tutunacağı fiziksel veya görsel bir temsil sunulmamıştır.")
        
        mat_raporu = f"Materyal kullanılmadığı için hedef dışı/erişilemez bir durum oluştu.<br><span class='oneri-metni'>Nasıl Kullanılmalıydı?</span> Bu kazanım ve profil için <b>{oneri_mat}</b> kullanılmalıydı. Materyal, kavramı görünür kılacak şekilde öğrencinin doğrudan manipüle edeceği (dokunacağı/etkileşime gireceği) biçimde derse entegre edilmelidir."
    
    elif materyal == "Klasik Çalışma Kâğıdı / Yaprak Test / Formül Özeti":
        puan -= 20
        materyal_temsil_puan -= 15
        hatalar_ve_sebepleri.append(f"<span class='hata-metni'>Hata (Yanlış Temsil/Materyal Seçimi):</span> Seçtiğiniz '{materyal}', {profil_durumu} profili için kriz çözücü değildir. <br><b>Akademik Sebep/Olası Etki:</b> Klasik kağıtlar veya formül özetleri yalnızca sembolik ve soyut tekrardır; kavramın nasıl inşa edildiğini (süreci) göstermez, bu nedenle öğrenme kanıtı oluşturmaz.")
        mat_raporu = f"Seçilen materyal, yapılandırmacı sürece (keşfe) katkı sağlamayan pasif bir araçtır.<br><span class='oneri-metni'>Hangi Materyal Nasıl Kullanılmalıydı?</span> İki boyutlu testler yerine <b>{oneri_mat}</b> tercih edilmelidir. Bu araçlar, öğrencinin parçadan bütüne giderek kuralı kendi kendine keşfetmesini sağlayacak şekilde (örneğin örüntü arayarak) kullanılmalıdır."
        
    else:
        if len(mat_aciklama.strip()) < 40:
            puan -= 10
            materyal_temsil_puan -= 5
            hatalar_ve_sebepleri.append("<span class='hata-metni'>Hata (Yüzeysel Temsil Planlaması):</span> Seçilen materyalin teorik uygunluğuna rağmen, sahada (derste) adım adım nasıl kullanılacağını yeterince detaylandırmadınız. <br><b>Akademik Sebep:</b> Öğretmen adayının materyali ne zaman ve hangi soruyla devreye sokacağı (öğrenme kanıtı alma süreci) belirsizdir.")
            pedagojik_oneriler.append("<span class='oneri-metni'>Öneri:</span> Öğrencinin materyale nasıl dokunacağını, materyal üzerinden ona hangi açık uçlu soruyu soracağınızı ve öğrencinin neyi fark etmesini beklediğinizi adım adım açıklayın.")
            mat_raporu = f"Seçilen '{materyal}' kavramsal bağlantı için doğru bir araçtır ancak eylem planı yüzeysel geçilmiştir."
        else:
            mat_raporu = f"Seçilen '{materyal}', hem öğrencinin gereksinimine hem de TYMM yapısına uygundur. Uygulama planınız, öğrencinin kavramı görünür kılması açısından etkilidir."

    # İletişim ve Hitabet
    if len(sesli_girdi.strip()) < 20 and not materyalsiz:
        puan -= 5
        kriz_yonetimi_puan -= 5
        hatalar_ve_sebepleri.append("<span class='hata-metni'>Hata (İletişim Eksikliği):</span> Öğrenciye doğrudan kurduğunuz sözlü iletişim metni çok yetersiz/yok.")

    # Rapor Metninin İnşası
    rapor_metni = f"**📊 Değerlendirme Sonucu: {max(0, puan)} / 100**\n\n"
    
    if hoca_rubrik:
        rapor_metni += "### 📋 Öğretim Elemanı Rubrik Uyumu\n"
        rapor_metni += "*(Sisteme yüklenen öğretim elemanı rubriği kriterleri dikkate alınarak analiz edilmiştir.)*\n\n"

    rapor_metni += "### ⚠️ Tespit Edilen Eksiklikler, Hatalar ve Akademik Sebepleri\n"
    if hatalar_ve_sebepleri:
        for h in hatalar_ve_sebepleri: rapor_metni += f"- {h}\n\n"
    else:
        rapor_metni += "- Tebrikler. Bağlam uyumu, kriz yönetimi ve eylem sırasına dair pedagojik sürecinizde hata tespit edilmemiştir.\n\n"

    rapor_metni += "### 🛠️ Temsil ve Materyal Kullanım Analizi\n"
    rapor_metni += f"- {mat_raporu}\n\n"

    rapor_metni += "### 💡 İleriye Dönük Pedagojik Öneriler (Gelişim Alanı)\n"
    if pedagojik_oneriler:
        for o in pedagojik_oneriler: rapor_metni += f"- {o}\n\n"
    else:
        rapor_metni += "- 2024 TYMM'nin beceri temelli yapısına, öğrenci merkezliliğe ve kapsayıcılık ilkelerine eksiksiz biçimde uydunuz.\n\n"
        
    rapor_metni += f"*(Puan Dağılımı: Kriz Yön.: {max(0,kriz_yonetimi_puan)}/20 | Eylem Sırası: {max(0,eylem_sirasi_puan)}/15 | Süreç Uyumu: {max(0,matematik_surec_puan)}/20 | Öğr. Merkezlilik: {max(0,ogrenci_merkezlilik_puan)}/15 | Materyal/Temsil: {max(0,materyal_temsil_puan)}/25 | Öğr. Kanıtı: {ogrenme_kaniti_puan}/5)*"

    return puan, rapor_metni

# Dinamik Emojili Tepki Üretimi
def ai_profil_davranisi_uret(ogrenci_adi, sinif, tema, kazanim_kod, kazanim_cikti, surec, temel_kriz, aday_sozu="", eylem_1="", eylem_2="", materyal_etiketi=""):
    profil = ogrenci_profilleri[ogrenci_adi]
    durum = profil["durum"]
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    mudahale_var = bool(aday_sozu.strip() or eylem_1 or materyal_etiketi)
    
    e1_tur = "duyussal" if any(kw in eylem_1 for kw in ["kabul ederek", "neyi kaçırdığını", "esneklik sağlamak"]) else "diger"
    e2_tur = "kesif" if any(kw in eylem_2 for kw in ["keşfetmesini", "örnekle açıklamasını", "temsile dönüştürmek", "genellemesini"]) else "ezber"
    
    d1 = (e1_tur == "duyussal")
    d2 = (e2_tur == "kesif")
    materyalsiz = (materyal_etiketi == "Materyal Kullanmadan İlerle")

    if not mudahale_var:
        return f"😟 **{ogrenci_adi} ({durum}):** `{kazanim_kod}` ({surec_kisa}) adımında {temel_kriz}"

    if materyalsiz and durum in ["Diskalkuli", "Az Gören", "Disleksi"]:
        return f"😭 **{ogrenci_adi} ({durum}):** Öğretmenin sözlerine rağmen ortada somut bir materyal olmadığı için zihinsel olarak konudan tamamen kopar ve kriz derinleşir."
    
    if not (d1 and d2):
        return f"😕 **{ogrenci_adi} ({durum}):** Öğretmenin sözlerine rağmen, '{surec_kisa}' basamağında seçilen yaklaşım ihtiyacına uymadığı için gerginliği sürer ve işlemi ezberlemeye çalışır."

    mat_isim = "yönlendirmeler" if materyalsiz else f"'{materyal_etiketi}'"
    return f"💡 **{ogrenci_adi} ({durum}):** Öğretmenin yaklaşımıyla sakinleşir ve {mat_isim} desteği sayesinde `{kazanim_kod}` ilişkisini kendi kendine yapılandırmaya başlar."

# ==========================================
# 4. 2024 TYMM ORTAOKUL MATEMATİK TAM MÜFREDATI (MATERYAL ÖNERİLERİYLE)
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
                {
                    "kod": "MAT.5.1.1", 
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme", 
                    "surec": ["a) Çok basamaklı sayılar hakkında bilgi toplar.", "b) Ortak özellikleri belirler.", "c) Farklılıkları belirler.", "ç) Örüntüler üzerinden önermelerde bulunur."], 
                    "hook": "Kütüphane arşiv kodlama sistemi veya astronomik uzaklıklar.", 
                    "kriz": "sıfır içeren bölükleri (ör: 100.005) okurken basamakları atlar veya karıştırır.",
                    "somut_materyal_onerisi": "Çok tabanlı bloklar (MAB), basamak değer kartları, renkli pullar ve bölük tabloları."
                },
                {
                    "kod": "MAT.5.1.4", 
                    "cikti": "Kesirlerin farklı gösterimlerini ve sayı doğrusundaki yerlerini ilişkilendirebilme", 
                    "surec": ["a) Basit, bileşik ve tam sayılı kesirleri inceler.", "b) Denk kesirleri modeller ve karşılaştırır."], 
                    "hook": "Mutfak ölçülerinde veya pasta paylaşımlarında çeyrek/yarım ilişkileri.", 
                    "kriz": "payda büyüdükçe (ör: 1/8 < 1/4) kesrin küçüldüğünü zihnen kabullenmekte zorlanır.",
                    "somut_materyal_onerisi": "Kesir takımları, dairesel kesir dilimleri, katlanabilir şeffaf kesir kartları ve Cuisenaire çubukları."
                },
                {
                    "kod": "MAT.5.1.7", 
                    "cikti": "Kesir, ondalık ve yüzde gösterimleri arasındaki ilişkileri yorumlayabilme", 
                    "surec": ["a) Yüzlük kart ve modeller üzerinden eşleştirir.", "b) Farklı gösterimler arasında dönüşüm yapar."], 
                    "hook": "Cep telefonu batarya doluluk yüzdesi veya mağaza indirim etiketleri.", 
                    "kriz": "ondalık kısmı yüzdeye çevirirken basamak değerlerini (ör: 0,2 = %20 yerine %2 yazar) karıştırır.",
                    "somut_materyal_onerisi": "100'lük kare ızgaralar (yüzlük kartlar), onluk taban bloklarının yüzlük düzlemleri."
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.5.2.1", 
                    "cikti": "Temel geometrik çizimler (nokta, doğru, ışın) için araç ve teknolojiden yararlanabilme", 
                    "surec": ["a) Uygun araçlarla çizer.", "b) Özelliklerini ve ilişkilerini açıklar."], 
                    "hook": "Mahalle krokisindeki sokakların kesişimi ve uzanışı.", 
                    "kriz": "ışın ile doğru parçasının uç noktalarındaki sonsuzluk farkını çizimde gösteremez.",
                    "somut_materyal_onerisi": "GeoGebra geometri modülü, ipler, elastik bantlar ve çivili tahta (Geoboard)."
                }
            ],
            "3. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.5.3.2", 
                    "cikti": "Dikdörtgenin çevre uzunluğu ve alanı arasındaki ilişkileri yorumlayabilme", 
                    "surec": ["a) Birim karelerle alan/çevre hesaplar.", "b) Çevreleri eşit dikdörtgenlerin alanlarını karşılaştırır."], 
                    "hook": "Belirli uzunluktaki çit teliyle en geniş bahçe parselini oluşturma tasarımı.", 
                    "kriz": "çevre formülü ile alan hesaplama mantığını birbirine karıştırır.",
                    "somut_materyal_onerisi": "İzometrik kağıt, birim kare plastik küpler ve çevre ipi."
                }
            ],
            "4. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.5.4.1", 
                    "cikti": "Kategorik veriyle çalışabilme ve veriye dayalı karar verebilme", 
                    "surec": ["a) Araştırma sorusu oluşturur ve veri toplar.", "b) Sıklık tablosu ve sütun grafiğiyle görselleştirir.", "c) Veriyi analiz edip yorumlar."], 
                    "hook": "Okul kantininde en çok satılması gereken sağlıklı ürünlerin araştırılması.", 
                    "kriz": "sütun grafiği çizerken eksenleri eşit ölçeklendirmeyi unutur.",
                    "somut_materyal_onerisi": "Renkli yapışkan notlar (post-it) ile tahtada canlı sütun grafiği inşası, Excel grafik araçları."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.5.1", 
                    "cikti": "Herhangi bir olayın olasılığının 0 ile 1 arasında olduğunu yorumlayabilme", 
                    "surec": ["a) İmkânsız, olası ve kesin olayları inceler.", "b) Olayların ihtimalini 0-1 aralığına yerleştirir."], 
                    "hook": "Hava durumu raporlarındaki yağmur ihtimali ve kura çekimi.", 
                    "kriz": "olasılığı 1'den büyük bir tam sayı olarak ifade etmeye çalışır.",
                    "somut_materyal_onerisi": "Torba içine konan renkli toplar, olasılık çarkı (spinner)."
                }
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
                {
                    "kod": "MAT.6.1.1", 
                    "cikti": "Doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme", 
                    "surec": ["a) Varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Modellerle gösterir."], 
                    "hook": "Farklı otobüs hatlarının duraktan aynı anda kalkış saatlerinin tespiti.", 
                    "kriz": "çarpan ile kat kavramlarını zıt algılar; sayıyı büyütmesi gerekirken küçültür.",
                    "somut_materyal_onerisi": "Cuisenaire çubukları ile uzunlukları eşitleme modelleri, çarpım tablosu yüzlük ızgarası."
                },
                {
                    "kod": "MAT.6.1.6", 
                    "cikti": "Tam sayıları ve sayı doğrusunda sıralanışını yorumlayabilme", 
                    "surec": ["a) Yönlü sayıları gerçek yaşamla ilişkilendirir.", "b) Sayı doğrusunda sıralar ve mutlak değeri yorumlar."], 
                    "hook": "Asansör katları (zemin altı) veya kış mevsiminde Erzurum hava sıcaklıkları.", 
                    "kriz": "negatif sayılarda rakamsal değer büyüdükçe (ör: -10) sayının aslında küçüldüğünü algılamakta zorlanır.",
                    "somut_materyal_onerisi": "Dikey ve yatay fiziksel sayı doğruları, termometre modelleri."
                }
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme": [
                {
                    "kod": "MAT.6.2.1", 
                    "cikti": "Nicelikleri cebirsel ifadelerle modelleyebilme", 
                    "surec": ["a) Sabit ve değişkeni belirler.", "b) İlişkiyi tablo/cebirsel temsil eder."], 
                    "hook": "Kumbaradaki başlangıç parasına her hafta eklenen sabit harçlığın formülize edilmesi.", 
                    "kriz": "harf sembolünün (x, y) sadece bir etiket değil, değişebilen herhangi bir sayı olduğunu anlamaz.",
                    "somut_materyal_onerisi": "Cebir karoları (Algebra tiles), kapalı kutu (bilinmeyen) ve misket modellemesi."
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.6.3.1", 
                    "cikti": "Açı çeşitlerini ve iki paralel doğru ile bir kesenin oluşturduğu açıları sınıflandırabilme", 
                    "surec": ["a) Komşu, tümler, bütünler açıları inceler.", "b) Paralel doğru/kesen ile yöndeş, iç/dış ters açıları sınıflandırır."], 
                    "hook": "Tren raylarındaki çapraz makaslar ve köprü direk tasarımları.", 
                    "kriz": "kesen doğru eğik olduğunda veya şekil döndürüldüğünde Z, U kuralını göremez.",
                    "somut_materyal_onerisi": "Hareketli açı çubukları, GeoGebra açı kaydırma modülü, şeffaf asetat kağıtları."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.6.4.1", 
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarına yansıtma yapabilme", 
                    "surec": ["a) Dikdörtgen alan bağıntısından yola çıkar.", "b) Parçalama-birleştirme ile üçgen/paralelkenar alanı çıkarır."], 
                    "hook": "Yamuk veya paralelkenar şeklindeki tarla parsellerinin alanının hesabı.", 
                    "kriz": "üçgenin alanını hesaplarken yüksekliği tabanla çarpıp ikiye bölmeyi unutur.",
                    "somut_materyal_onerisi": "Noktalı kağıt, makasla kesilip dikdörtgene dönüştürülebilen karton paralelkenarlar."
                },
                {
                    "kod": "MAT.6.4.2", 
                    "cikti": "Çemberin uzunluğu ile çapı arasındaki orana (pi) ilişkin çıkarım yapabilme", 
                    "surec": ["a) Farklı çemberlerin çevre ve çaplarını ölçer.", "b) Çevre/çap oranının sabitliğini geneller."], 
                    "hook": "Bisiklet tekerleğinin bir tam tur döndüğünde aldığı mesafenin ölçümü.", 
                    "kriz": "yarıçap (r) ile çap (R) uzunluğunu formülde birbirine karıştırır.",
                    "somut_materyal_onerisi": "Farklı boylarda dairesel kapaklar, ip, cetvel ve esnek mezura."
                }
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {
                    "kod": "MAT.6.5.1", 
                    "cikti": "Veriyle araştırma yapıp merkezî eğilim ve yayılımı yorumlayabilme", 
                    "surec": ["a) Araştırma sorusu oluşturur.", "b) Ortalama, ortanca, tepe değer ve açıklığı hesaplayıp yorumlar."], 
                    "hook": "Sınıfın matematik sınavı puan dağılımlarının incelenmesi.", 
                    "kriz": "açıklığı (ranj) bulurken en küçük değer ile en büyük değer farkı yerine, en küçük değeri sıfır varsayar.",
                    "somut_materyal_onerisi": "Fiziksel boy sırasına girme etkinliği, blok dizilimleriyle ortalama alma (düzleştirme) modelleri."
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1", 
                    "cikti": "Bir olayın olasılığını deneysel gözleme dayalı tahmin edebilme", 
                    "surec": ["a) Deney çıktılarını kaydeder.", "b) Deneme sayısı arttıkça göreli sıklığın kararlılığını yorumlar."], 
                    "hook": "Madeni paranın 10 kez atılması ile 1000 kez atılması sonuçlarının kıyaslanması.", 
                    "kriz": "kısa bir denemede üst üste 3 kez tura gelince, sıradakinin kesin yazı geleceğini sanır (Kumarbaz yanılgısı).",
                    "somut_materyal_onerisi": "Madeni paralar, zar, dijital olasılık simülatörleri."
                }
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
                {
                    "kod": "MAT.7.1.3", 
                    "cikti": "Doğru ve ters orantı durumlarını ayırt etme ve problem çözme", 
                    "surec": ["a) Nicelikler arası orantı türünü belirler.", "b) Orantı sabiti ve denklemle problemi çözer."], 
                    "hook": "İşçi sayısı ile işin bitme süresi ilişkisi.", 
                    "kriz": "ters orantılı çokluklarda değişkenleri çarpmak (k=x.y) yerine, doğru orantıdaki gibi bölmeye çalışır.",
                    "somut_materyal_onerisi": "Denge terazisi, su kapları ve birim küpler, orantı tabloları."
                }
            ],
            "2. Tema: Cebirsel Düşünme": [
                {
                    "kod": "MAT.7.2.1", 
                    "cikti": "Birinci dereceden bir bilinmeyenli denklemleri çözebilme", 
                    "surec": ["a) Cebirsel ifadeyle modeller.", "b) Eşitliğin korunumu ilkesiyle denklemi çözer."], 
                    "hook": "Tahterevalli dengesi veya bilinmeyen ağırlık barındıran terazi durumları.", 
                    "kriz": "eşitliğin karşı tarafına geçen terimin işaretini değiştirmeyi unutur.",
                    "somut_materyal_onerisi": "Fiziksel denklem terazisi, cebir karoları."
                }
            ],
            "3. Tema: Dönüşüm Geometrisi": [
                {
                    "kod": "MAT.7.3.1", 
                    "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerini oluşturma", 
                    "surec": ["a) Yansıma eksenine göre simetriyi inceler.", "b) Görüntüyü oluşturur ve karşılaştırır."], 
                    "hook": "Aynadaki yansımalar, göl yüzeyindeki simetri.", 
                    "kriz": "çapraz simetri eksenlerinde şekli katlamak yerine doğrudan aşağı öteler.",
                    "somut_materyal_onerisi": "Simetri aynası (Mira), şeffaf asetat kağıdı, noktalı kağıt."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.7.4.2", 
                    "cikti": "Dairenin ve daire diliminin alan bağıntılarına çıkarım yapabilme", 
                    "surec": ["a) Merkez açı ile yay/alan orantısını kurar.", "b) Alanı hesaplar."], 
                    "hook": "Pizza diliminin alan hesabı veya döner fıskiye.", 
                    "kriz": "dilim alanı hesaplarken tam daire (360 derece) üzerinden oran kurmayı atlar.",
                    "somut_materyal_onerisi": "Daire dilimleri takımı, iletki, GeoGebra çember modülü."
                }
            ],
            "5. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.7.5.1", 
                    "cikti": "Üçgende kenarortay, açıortay ve yüksekliği çözümleyebilme", 
                    "surec": ["a) Yardımcı elemanları çizer.", "b) Özelliklerini ve kesişimlerini inceler."], 
                    "hook": "Çatı iskeletinin ağırlık merkezi ve taşıyıcı dikmeleri.", 
                    "kriz": "yükseklik ile kenarortay kavramlarını ve çizimlerini birbirine karıştırır.",
                    "somut_materyal_onerisi": "Kağıt katlama (origami) ile açıortay/kenarortay bulma, pergel ve cetvel inşası."
                }
            ],
            "6. Tema: İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.6.1", 
                    "cikti": "Sürekli veri ile çalışıp çizgi grafiği ile analiz edebilme", 
                    "surec": ["a) Sürekli veri toplar.", "b) Çizgi grafiği çizer ve eğilimleri yorumlar."], 
                    "hook": "Bir fidanın aylara göre boy uzama grafiği.", 
                    "kriz": "çizgi grafiğini sürekli olmayan (kategorik) veriler için kullanmaya çalışır.",
                    "somut_materyal_onerisi": "Sensör verileri toplama yazılımları, iplerle duvarda çizgi grafiği ağı örme."
                }
            ],
            "7. Tema: Olasılık": [
                {
                    "kod": "MAT.7.7.1", 
                    "cikti": "Bir olayın ve tümleyeninin olasılığına tümevarımsal akıl yürütebilme", 
                    "surec": ["a) Çıktıları gözlemler.", "b) Olay + Tümleyen = 1 ilişkisini geneller."], 
                    "hook": "Basket atışında topun potaya girmesi ve girmemesi olasılıklarının toplamı.", 
                    "kriz": "tümleyeni bulmak için olayın olasılığını 1'den çıkarmak yerine farklı işlem yapar.",
                    "somut_materyal_onerisi": "İki yüzü farklı renkli pullar, olasılık kutusu."
                }
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
                {
                    "kod": "MAT.8.1.2", 
                    "cikti": "Kareköklü ifadelerin yaklaşık değerini bulma ve işlem yapma", 
                    "surec": ["a) Tam kare ilişkiyi belirler.", "b) Tam kare olmayanların hangi iki sayı arasında olduğunu bulur."], 
                    "hook": "Alanı 50 metrekare olarak bilinen kare biçimindeki odanın bir kenar uzunluğunu tahmin etme.", 
                    "kriz": "karekök bulurken sayıyı ikiye böler (Ör: Kök 36'ya 18 der, Kök 50'ye 25 der).",
                    "somut_materyal_onerisi": "Birim karelerden oluşturulan fiziksel karesel bölgeler, karekök spirali çizimi."
                }
            ],
            "2. Tema: Cebirsel Düşünme": [
                {
                    "kod": "MAT.8.2.2", 
                    "cikti": "Doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme", 
                    "surec": ["a) Tablo, grafik ve denklem geçişlerini yapar.", "b) Eğim (değişim oranı) yorumu yapar."], 
                    "hook": "Taksimetre açılış ücreti ve gidilen kilometreye göre artan fiyat grafiği.", 
                    "kriz": "eğimi hesaplarken dikey değişim / yatay değişim yapmak yerine, yatayı dikeye böler.",
                    "somut_materyal_onerisi": "Fiziksel rampa modelleri ile eğim ölçümü, Desmos Dinamik Grafik Çizici."
                }
            ],
            "3. Tema: Geometrik Şekiller": [
                {
                    "kod": "MAT.8.3.2", 
                    "cikti": "Pisagor bağıntısını (a²+b²=c²) yorumlayıp problem çözebilme", 
                    "surec": ["a) Dik kenarlar ve hipotenüs karelerini inceler.", "b) Bağıntıyı modelleyip uygular."], 
                    "hook": "Duvara dayalı duran bir merdivenin yüksekliği ve taban uzaklığı ilişkisi.", 
                    "kriz": "hipotenüs uzunluğunu bulmak için dik kenarların karelerini almak yerine kenar uzunluklarını toplar.",
                    "somut_materyal_onerisi": "Pisagor su çarkı modeli, kare ve dik üçgen puzzle'ları (Pisagor ispat panoları)."
                }
            ],
            "4. Tema: Geometrik Nicelikler": [
                {
                    "kod": "MAT.8.4.1", 
                    "cikti": "Prizmalar, silindir, piramit ve koni açınımlarını çözümleyebilme", 
                    "surec": ["a) Yüzey şekillerini belirler.", "b) Açınım ile kapalı cisim arasındaki eşleşmeleri kurar."], 
                    "hook": "Fabrikada tasarlanan karton hediye ve ambalaj kutularının açınım planları.", 
                    "kriz": "silindirin yanal yüzeyi açıldığında oluşan dikdörtgenin uzun kenarının, taban dairesinin çevresine eşit olduğunu göremez.",
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
                    "kriz": "sadece aritmetik ortalamaya bakıp karar verir; yayılımı (standart sapmayı/açıklığı) göz ardı eder.",
                    "somut_materyal_onerisi": "İki farklı hedefe atılan dart oklarının dağılım simülasyonu, histogram blokları."
                }
            ],
            "7. Tema: Olasılık": [
                {
                    "kod": "MAT.8.7.1", 
                    "cikti": "Olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı seçebilme", 
                    "surec": ["a) Karara uygun bilgi toplar.", "b) Yaklaşımları kıyaslayıp uygun olanı kullanır."], 
                    "hook": "Penaltı atışında gol olma tahmini (deneysel/öznel) ile zar atışının (teorik) farkı.", 
                    "kriz": "deneysel olasılık (geçmiş veri) kullanılması gereken bir durumda, salt teorik olasılık diyerek kesin hüküm verir.",
                    "somut_materyal_onerisi": "Sporcu istatistik kartları, hileli/ağırlıklı zarlar."
                }
            ]
        }
    }
}
# ==========================================
# 5. UI AKIŞI (KURULUM, 3D SINIF, TRANSKRİPT VE RAPORLAMA)
# ==========================================

# ----------------- ADIM 1 -----------------
if st.session_state.adim == 1:
    st.markdown('<span class="rozet">ADIM 1 / 3</span>', unsafe_allow_html=True)
    st.subheader("📝 2024 TYMM Kurulum Paneli")
    st.info("Bu simülasyon, **İlköğretim Matematik Öğretmenliği adayları** için kriz yönetimi, eylem sırası ve materyal kullanımı becerilerini değerlendirmek üzere tasarlanmıştır.")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">Aday ve Danışman Bilgileri</div>', unsafe_allow_html=True)
        ogretmen_adi = st.text_input("Öğretmen Adayı *", placeholder="Örn: Mislina Taysi")
        okul_numarasi = st.text_input("Okul Numarası *", placeholder="Örn: 20220000000")
        universite_adi = st.text_input("Üniversite Adı *", placeholder="Örn: Kahramanmaraş Sütçü İmam Üniversitesi")
        uygulama_ogretim_elemani = st.text_input("Uygulama Öğretim Elemanı *")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">Öğretim Elemanı Rubriği</div>', unsafe_allow_html=True)
        st.caption("Danışmanınızın özel rubriğini buraya yapıştırabilirsiniz.")
        hoca_rubrik = st.text_area(
            "Rubrik Kriterleri *",
            value="1. Kapsayıcı ve duyuşsal iletişim (20 Puan).\n2. Pedagojik eylem sırası (15 Puan).\n3. Profile ve kazanıma uygun materyal seçimi/kullanımı (25 Puan).\n4. 2024 TYMM keşif odaklı süreç uyumu (20 Puan).\n5. Öğrenme kanıtı (5 Puan)",
            height=100,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 3D Staj Simülasyonunu Başlat", type="primary", use_container_width=True):
        if not all([ogretmen_adi.strip(), okul_numarasi.strip(), universite_adi.strip(), uygulama_ogretim_elemani.strip(), hoca_rubrik.strip()]):
            st.error("❌ Zorunlu (*) alanlar doldurulmadan ilerlenemez.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi.strip()
            st.session_state.okul_numarasi = okul_numarasi.strip()
            st.session_state.universite_adi = universite_adi.strip()
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani.strip()
            st.session_state.hoca_rubrik = hoca_rubrik.strip()
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
                st.caption(f"Mimik: {bilgi['mimik']}")
                st.write(davranis)

    # İpuçsuz Dinamik Eylem Üretimi
    dinamik_eylem_1_list, dinamik_eylem_2_list = dinamik_eylem_secenekleri_uret(secilen_tema, secilen_kazanim_obj["kod"], secilen_surec, secilen_kazanim_obj["kriz"])

    st.markdown('<div class="sade-kart"><div class="baslik-mavi">🎙️ Pedagojik Müdahale Konsolu</div>', unsafe_allow_html=True)
    sesli_girdi = st.text_area("✍️ Öğrenci(ler)e doğrudan söyleyeceğiniz hitabet metni *", placeholder="Örn: Ali'cim şu an kafanın karıştığını görüyorum, bu çok normal. Hadi birlikte şu modeli inceleyelim...", height=85)
        
    eylem_1 = st.selectbox("1. Pedagojik Eylem Sırası *", dinamik_eylem_1_list)
    eylem_2 = st.selectbox("2. Pedagojik Eylem Sırası *", dinamik_eylem_2_list)
    materyal = st.selectbox("Materyal Seçimi (Kapsayıcılık Açısından Kritik) *", MATERYAL_SECENEKLER)
        
    ozgun_tanitim, ozgun_ad = "", ""
    if materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal":
        ozgun_ad = st.text_input("Özgün Materyalinizin Adı *")
        ozgun_tanitim = st.text_area("Materyali Detaylıca Tanıtın *")
        materyal_etiketi = f"{ozgun_ad} (Özgün Materyal)"
    elif materyal == "Materyal Kullanmadan İlerle":
        materyal_etiketi = materyal
    else:
        materyal_etiketi = materyal
            
    mat_label = "Sözel stratejinizi açıklayın *" if materyal == "Materyal Kullanmadan İlerle" else "Materyali nasıl (hangi adımlarla) kullanacaksınız? *"
    mat_aciklama = st.text_area(mat_label, height=85)

    if st.button("📥 Müdahaleyi Onayla ve Değerlendirme Raporuna Geç", type="primary", use_container_width=True):
        eksik_ozgun = materyal == "Kendi Geliştirdiğim / Tasarladığım Materyal" and (not ozgun_ad.strip() or not ozgun_tanitim.strip())
        if not sesli_girdi.strip() or eylem_1 == "Seçiniz..." or eylem_2 == "Seçiniz..." or materyal == "Seçiniz..." or not mat_aciklama.strip() or eksik_ozgun:
            st.error("❌ Tüm zorunlu (*) alanları doldurunuz.")
        else:
            ai_tepkileri = {}
            for ogr_ad in secili_liste:
                ai_tepkileri[ogr_ad] = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, secilen_kazanim_obj["kriz"], sesli_girdi, eylem_1, eylem_2, materyal_etiketi)
                
            durumlar = [ogrenci_profilleri[o]["durum"] for o in secili_liste]
            
            # Geri bildirim burada üretilir ancak 3. Adımda (Tüm cevaplardan sonra) gösterilir
            ai_puan, ai_mesaj = kapsamli_ai_degerlendirmesi(eylem_1, eylem_2, materyal_etiketi, mat_aciklama, sesli_girdi, durumlar, secilen_kazanim_obj, st.session_state.hoca_rubrik)

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

# ----------------- ADIM 3 -----------------
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 2024 TYMM Kapsamlı Akademik Değerlendirme Raporu")
    
    son_kayit = st.session_state.simulasyon_gecmisi[-1]
    
    # 1. SEKME: ÖĞRENCİ TEPKİLERİ VE ADAYIN SEÇİMLERİ (TRANSKRİPT)
    st.markdown("### 1. Öğrenci Tepkileri ve Krizin Son Durumu")
    kart_cols = st.columns(min(len(son_kayit["secili_ogrenciler"]), 3))
    idx = 0
    for ogr, tepki in son_kayit["ai_tepkileri"].items():
        with kart_cols[idx % len(kart_cols)]:
            with st.container(border=True):
                st.write(tepki)
        idx += 1

    st.divider()

    # 2. SEKME: YAPAY ZEKA DEĞERLENDİRME RAPORU
    st.markdown("### 2. Kapsamlı AI Değerlendirme Raporu")
    st.markdown(f"<div class='anlik-bildirim'>{son_kayit['ai_mesaj']}</div>", unsafe_allow_html=True)
    
    st.divider()

    # 3. SEKME: DANIŞMAN HOCA DÖNÜTÜ VE İNDİRME
    tab_trans, tab_hoca = st.tabs(["📝 Sisteme Kayıtlı Ders Transkripti Özeti", "👨‍🏫 Öğretim Elemanı Değerlendirmesi"])
    
    with tab_trans:
        ozg_metin = f"\n- **Özgün Materyal Tanıtımı:** {son_kayit['ozgun_tanitim']}" if son_kayit["ozgun_tanitim"] else ""
        transkript = (
            f"**Oturum Tarihi:** {son_kayit['tarih']} \n**Aday:** {st.session_state.ogretmen_adi} ({st.session_state.universite_adi})\n"
            f"**Kazanım:** {son_kayit['kod']} ({son_kayit['surec']})\n\n"
            f"**1. Eylem (Seçilen):** {son_kayit['eylem_1']}\n**2. Eylem (Seçilen):** {son_kayit['eylem_2']}\n"
            f"**Materyal:** {son_kayit['materyal_etiketi']}{ozg_metin}\n"
            f"**Kullanım Açıklaması:** {son_kayit['mat_aciklama']}\n**Adayın Sözel Hitabeti:** {son_kayit['sesli_girdi']}\n"
        )
        st.markdown(f"<div class='transkript-kutu'>{transkript}</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="⬇️ Yazılı Ders Transkripti ve AI Akademik Raporunu İndir (.txt)",
            data=(son_kayit['ai_mesaj'] + "\n\n=== DERS TRANSKRİPTİ ===\n\n" + transkript).replace("**", "").replace("*", "").replace("`", "").replace("<br>", "\n").replace("<b>", "").replace("</b>", "").replace("<span class='hata-metni'>", "").replace("<span class='oneri-metni'>", "").replace("</span>", ""),
            file_name=f"2024_TYMM_Transkript_Rapor_{st.session_state.get('okul_numarasi', 'aday')}.txt",
            mime="text/plain",
        )

    with tab_hoca:
        st.markdown("### Danışman Öğretim Elemanı Geri Dönütü")
        hoca_notu = st.text_area("Yapay zeka analiz raporunu ve adayın yukarıdaki seçimlerini göz önünde bulundurarak resmî geri dönütünüzü yazın *", height=150)
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
