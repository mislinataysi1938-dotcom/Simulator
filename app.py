import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="2024 TYMM - Akademik Staj ve Gelişim Simülatörü",
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
    .uyari-bildirim {
        background-color: #FEF2F2; border-left: 4px solid #DC2626; padding: 15px; margin-bottom: 15px; border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

if "simulasyon_gecmisi" not in st.session_state: st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state: st.session_state.adim = 1
if "secili_ogrenciler" not in st.session_state: st.session_state.secili_ogrenciler = []
if "otur_seed" not in st.session_state: st.session_state.otur_seed = random.randint(1, 1000)
if "telafi_senaryosu" not in st.session_state: st.session_state.telafi_senaryosu = None

UNIVERSITELER = [
    "Seçiniz...", "Kahramanmaraş Sütçü İmam Üniversitesi", "Ankara Üniversitesi", "Gazi Üniversitesi", 
    "Hacettepe Üniversitesi", "Marmara Üniversitesi", "Boğaziçi Üniversitesi", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 
    "Yıldız Teknik Üniversitesi", "Ege Üniversitesi", "Dokuz Eylül Üniversitesi", "Çukurova Üniversitesi", "Diğer"
]

# ==========================================
# 1. 10 ÖĞRENCİ PROFİLİ VE BİLİŞSEL DETAYLARI
# ==========================================
ogrenci_profilleri = {
    "Kerem": {"durum": "Disleksi", "ikon": "👦", "mimik": "Basamaklara ve harflere odaklanmakta zorlanıyor, gözlerini kısıyor", "ozellik": "Rakamları, sembolleri ve harfleri ters algılayabilir; görsel-dokunsal ayrıştırmaya ihtiyaç duyar."},
    "Arda": {"durum": "Otizm Spektrumu", "ikon": "👦", "mimik": "Kulaklık takılı, hafifçe ileri geri sallanıyor", "ozellik": "Ani seslere ve belirsiz yönergelere aşırı hassastır; soyut metaforlar yerine net, ardışık yönergeler bekler."},
    "Can": {"durum": "Üstün Yetenekli", "ikon": "👦", "mimik": "Sabırsızca parmak kaldırıyor, ofluyor", "ozellik": "Rutin tekrardan ve ezberden anında kopar; kavramın felsefi nedenini, genellemesini sorgular."},
    "Elif": {"durum": "Yüksek Kaygılı", "ikon": "👧", "mimik": "Başını öne eğmiş, elleriyle sırayı sıkıyor", "ozellik": "Hata yapmaktan aşırı çekinir; akademik baskı hissederse donup kalır, önce yargısız bir güven alanı ister."},
    "Zeynep": {"durum": "DEHB", "ikon": "👧", "mimik": "Sürekli etrafa bakınıyor, kalemiyle ritim tutuyor", "ozellik": "Sürdürülebilir dikkati kısadır; uzun sözel anlatımlarda kopar. Harekete dayalı, aktif katılımlı görevlere ihtiyaç duyar."},
    "Mehmet": {"durum": "İşitme Yetersizliği", "ikon": "👦", "mimik": "Konuşanın dudaklarına ve mimiklerine odaklanmış", "ozellik": "Sadece işitsel olan yönergeleri kaçırır; tahtadaki yazılı pekiştireçlere ve görsel ipuçlarına dayanır."},
    "Ayşe": {"durum": "Az Gören", "ikon": "👧", "mimik": "Materyale çok yakından bakıyor, kağıda eğilmiş", "ozellik": "Küçük puntolu, karmaşık görsellerde kaybolur; yüksek kontrastlı, dokunarak hissedilebilen materyaller bekler."},
    "Ali": {"durum": "Diskalkuli", "ikon": "👦", "mimik": "Parmaklarıyla gizlice saymaya çalışıyor, kaşları çatık", "ozellik": "Sayıların büyüklük (nicelik) ilişkisini ve işlemsel akıl yürütmeyi zihinde kuramaz; somut manipülatiflerle kavramı inşa etmesi gerekir."},
    "Merve": {"durum": "Bedensel Yetersizlik", "ikon": "👧", "mimik": "Elleri sırasında, bedensel hareketleri kısıtlı ama gözleri odaklı", "ozellik": "Bilişsel hiçbir engeli yoktur ancak yoğun çizim veya ince motor beceri gerektiren adımlarda erişilebilirlik desteği şarttır."},
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
# 2. İPUÇSUZ DİNAMİK YAPAY ZEKA ŞIK ÜRETİCİSİ
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
# 3. KAPSAMLI AKADEMİK DEĞERLENDİRME MOTORU
# ==========================================
def kapsamli_ai_degerlendirmesi(eylem1, eylem2, materyal, mat_aciklama, sesli_girdi, ogr_durumlar, kazanim_obj, hoca_rubrik):
    e1_tur = "duyussal" if any(kw in eylem1 for kw in ["kabul ederek", "neyi kaçırdığını", "esneklik sağlamak"]) else "bilissel"
    if any(kw in eylem1 for kw in ["kurallarını hatırlatıp", "devam etmek", "tekrar etmek"]): e1_tur = "disiplin"

    e2_tur = "kesif" if any(kw in eylem2 for kw in ["keşfetmesini", "örnekle açıklamasını", "temsile dönüştürmek", "genellemesini"]) else "ezber"
    if any(kw in eylem2 for kw in ["ezberlemesini", "atlayıp", "çözmek"]): e2_tur = "ezber"
    
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

    if e1_tur == "duyussal" and e2_tur == "kesif":
        pedagojik_oneriler.append("✅ Kriz Yönetimi: Öğrencinin zorlanmasını duyuşsal olarak yönettiniz ve ardından bilişsel keşif sürecine geçtiniz. Sıralama pedagojik olarak uygundur.")
    elif e1_tur == "disiplin":
        puan -= 20
        kriz_yonetimi_puan -= 15
        hatalar_ve_sebepleri.append(f"❌ **Hata (Kriz Yönetimi):** Kriz anında doğrudan disipline ve ilerlemeye odaklandınız. \n*Akademik Sebep/Olası Etki:* {profil_durumu} profiline sahip bir öğrencide bu yaklaşım, güvenliği zedeler, öğrencinin içe kapanmasına veya dersten tamamen kopmasına yol açar.")
        pedagojik_oneriler.append("💡 **Öneri:** İlk müdahale olarak öğrencinin duygusunu kabul eden, saygılı ve güvenli bir pedagojik alan tanıyın.")
    elif e1_tur == "bilissel" and (e2_tur == "ezber" or e2_tur == "kesif"):
        puan -= 15
        eylem_sirasi_puan -= 10
        hatalar_ve_sebepleri.append(f"❌ **Hata (Pedagojik Sıralama):** Öğrencinin kriz anındaki psikolojik (duyuşsal) ihtiyacını atlayıp doğrudan akademik hedefe yöneldiniz. \n*Akademik Sebep/Olası Etki:* Duygusal olarak regüle olmamış (sakinleşmemiş) bir beyin yeni bilgiyi işlemleyemez.")
        pedagojik_oneriler.append("💡 **Öneri:** Bilişsel adımlara geçmeden önce kısa da olsa öğrenciyle empatik bir bağ kurun.")
    
    if e2_tur == "ezber":
        puan -= 20
        matematik_surec_puan -= 15
        ogrenci_merkezlilik_puan -= 10
        hatalar_ve_sebepleri.append("❌ **Hata (TYMM Süreç Uyumu):** Öğrenci zorlandığında kavramı doğrudan verip ezberletme veya işlemi onun yerine çözme yolunu seçtiniz. \n*Akademik Sebep/Olası Etki:* 2024 TYMM beceri ve süreç odaklıdır. Sonuç odaklı ezber, kalıcı öğrenmeyi ve öğrencinin strateji üretmesini engeller.")
        pedagojik_oneriler.append("💡 **Öneri:** Öğrenciye formülü dikte etmek yerine; yönlendirici sorularla, alt problemlere bölerek veya kavramı farklı bir temsile dönüştürerek kendi keşfini yapmasına alan bırakın.")

    mat_raporu = ""
    oneri_mat = kazanim_obj.get("somut_materyal_onerisi", "Uygun somut manipülatifler.")
    
    if materyalsiz:
        if profil_durumu in ["Diskalkuli", "Az Gören", "Disleksi"]:
            puan -= 30
            materyal_temsil_puan -= 25
            hatalar_ve_sebepleri.append(f"❌ **KRİTİK HATA (Kapsayıcılık ve Temsil):** {profil_durumu} profili için tamamen SÖZEL ve SOYUT bir anlatım seçerek materyal kullanmayı reddettiniz. \n*Akademik Sebep/Olası Etki:* Bu profiller zihinsel sembolleştirmeyi materyal olmadan tek başına yapamaz. Bu durum kesin bir erişim engeli (bilişsel çöküş) yaratır.")
        else:
            puan -= 20
            materyal_temsil_puan -= 15
            hatalar_ve_sebepleri.append("❌ **Hata (Somutlaştırma Eksikliği):** Soyut matematiksel krizleri sadece konuşarak aşmayı denediniz. \n*Akademik Sebep/Olası Etki:* Ortaokul dönemi somuttan soyuta geçiş evresidir. Öğrencinin kavramı zihninde canlandırması (modellemesi) için tutunacağı fiziksel bir model sunulmamıştır.")
        
        mat_raporu = f"Materyal kullanılmadığı için hedef dışı/erişilemez bir durum oluştu.\n\n**Hangi Materyal Nasıl Kullanılmalıydı?** \nBu kazanım ve {profil_durumu} profili için **{oneri_mat}** kullanılmalıydı. Materyal, kavramı görünür kılacak şekilde öğrencinin doğrudan manipüle edeceği (dokunacağı/etkileşime gireceği) biçimde derse entegre edilmelidir."
    
    elif materyal == "Klasik Çalışma Kâğıdı / Yaprak Test / Formül Özeti":
        puan -= 20
        materyal_temsil_puan -= 15
        hatalar_ve_sebepleri.append(f"❌ **Hata (Yanlış Temsil/Materyal Seçimi):** Seçtiğiniz '{materyal}', {profil_durumu} profili için kriz çözücü değildir. \n*Akademik Sebep/Olası Etki:* Klasik kağıtlar yalnızca sembolik ve soyut tekrardır; kavramın nasıl inşa edildiğini göstermez, bu nedenle anlamlı bir öğrenme kanıtı oluşturmaz.")
        mat_raporu = f"Seçilen materyal, yapılandırmacı sürece (keşfe) katkı sağlamayan pasif bir araçtır.\n\n**Hangi Materyal Nasıl Kullanılmalıydı?** \nİki boyutlu testler yerine **{oneri_mat}** tercih edilmelidir. Bu araçlar, öğrencinin parçadan bütüne giderek kuralı kendi kendine keşfetmesini sağlayacak şekilde (örneğin örüntü arayarak) kullanılmalıdır."
        
    else:
        if len(mat_aciklama.strip()) < 40:
            puan -= 10
            materyal_temsil_puan -= 5
            hatalar_ve_sebepleri.append("❌ **Hata (Yüzeysel Temsil Planlaması):** Seçilen materyalin teorik uygunluğuna rağmen, sahada (derste) adım adım nasıl kullanılacağını yeterince detaylandırmadınız. \n*Akademik Sebep:* Öğretmen adayının materyali ne zaman ve hangi soruyla devreye sokacağı (öğrenme kanıtı alma süreci) belirsizdir.")
            pedagojik_oneriler.append("💡 **Öneri:** Öğrencinin materyale nasıl dokunacağını, materyal üzerinden ona hangi açık uçlu soruyu soracağınızı adım adım açıklayın.")
            mat_raporu = f"Seçilen '{materyal}' kavramsal bağlantı için doğru bir araçtır ancak eylem planı yüzeysel geçilmiştir."
        else:
            mat_raporu = f"Seçilen '{materyal}', hem öğrencinin gereksinimine hem de TYMM yapısına uygundur. Uygulama planınız, öğrencinin kavramı görünür kılması açısından etkilidir."

    if len(sesli_girdi.strip()) < 20 and not materyalsiz:
        puan -= 5
        kriz_yonetimi_puan -= 5
        ogrenme_kaniti_puan -= 5
        hatalar_ve_sebepleri.append("❌ **Hata (İletişim Eksikliği):** Öğrenciye doğrudan kurduğunuz sözlü iletişim metni çok yetersiz/yok. Öğrencinin duygusunu geçerli kılacak (validasyon) bir dil kullanılmamış.")

    kriz_yonetimi_puan = max(0, kriz_yonetimi_puan)
    eylem_sirasi_puan = max(0, eylem_sirasi_puan)
    matematik_surec_puan = max(0, matematik_surec_puan)
    ogrenci_merkezlilik_puan = max(0, ogrenci_merkezlilik_puan)
    materyal_temsil_puan = max(0, materyal_temsil_puan)
    ogrenme_kaniti_puan = max(0, ogrenme_kaniti_puan)
    puan = max(0, puan)

    alt_puanlar_dict = {
        "Kriz Yönetimi (20)": kriz_yonetimi_puan,
        "Eylem Sırası (15)": eylem_sirasi_puan,
        "Süreç Uyumu (20)": matematik_surec_puan,
        "Öğr. Merkezlilik (15)": ogrenci_merkezlilik_puan,
        "Materyal/Temsil (25)": materyal_temsil_puan,
        "Öğrenme Kanıtı (5)": ogrenme_kaniti_puan,
        "Toplam": puan
    }

    rapor_metni = f"**📊 Değerlendirme Sonucu: {puan} / 100**\n\n"
    if hoca_rubrik:
        rapor_metni += "### 📋 Öğretim Elemanı Rubrik Uyumu\n*(Sisteme yüklenen öğretim elemanı rubriği kriterleri dikkate alınarak analiz edilmiştir.)*\n\n"
    rapor_metni += "### ⚠️ Tespit Edilen Eksiklikler, Hatalar ve Akademik Sebepleri\n"
    if hatalar_ve_sebepleri:
        for h in hatalar_ve_sebepleri: rapor_metni += f"- {h}\n\n"
    else:
        rapor_metni += "- Tebrikler. Bağlam uyumu, kriz yönetimi ve eylem sırasına dair pedagojik sürecinizde hata tespit edilmemiştir.\n\n"
    rapor_metni += f"### 🛠️ Temsil ve Materyal Kullanım Analizi\n- {mat_raporu}\n\n"
    rapor_metni += "### 💡 İleriye Dönük Pedagojik Öneriler (Gelişim Alanı)\n"
    if pedagojik_oneriler:
        for o in pedagojik_oneriler: rapor_metni += f"- {o}\n\n"
    else:
        rapor_metni += "- 2024 TYMM'nin beceri temelli yapısına, öğrenci merkezliliğe ve kapsayıcılık ilkelerine eksiksiz biçimde uydunuz.\n\n"

    return puan, rapor_metni, alt_puanlar_dict

def profil_ve_kazanima_ozel_kriz_uret(durum, kazanim_cikti, surec_kisa):
    if durum == "Disleksi": return f"'{surec_kisa}' sürecinde ekrandaki/tahtadaki sembollerin ve rakamların sırasını karıştırıp okuyamadığı için işleme başlayamaz."
    elif durum == "Otizm Spektrumu": return f"'{surec_kisa}' adımında soyut bir açıklama yapıldığı ve adımlar belirli olmadığı için ne yapacağını bilemez, elleriyle kulaklarını kapatır."
    elif durum == "Üstün Yetenekli": return f"'{surec_kisa}' adımındaki kuralın 'neden' öyle olduğunu sorgular, sadece formül verilirse oflayarak işlemi yapmayı reddeder."
    elif durum == "Yüksek Kaygılı": return f"'{surec_kisa}' kısmında 'Ya yanlış yaparsam?' korkusuyla tahtaya/kağıda boş boş bakar, baskı hissederse tamamen içine kapanır."
    elif durum == "DEHB": return f"'{surec_kisa}' işlemi uzadığı veya çok sözel kaldığı için dikkatini kaybeder, kalemiyle oynayıp yanındakiyle konuşmaya başlar."
    elif durum == "İşitme Yetersizliği": return f"'{surec_kisa}' anlatılırken öğretmen yüzünü tahtaya döndüğü için dudak okuyamaz ve sürecin kritik yönergesini kaçırır."
    elif durum == "Az Gören": return f"'{surec_kisa}' adımındaki görsel/şekil çok küçük veya karmaşık olduğu için detayı seçemez, eğilip baksa da parçaları birleştiremez."
    elif durum == "Diskalkuli": return f"'{surec_kisa}' sürecindeki sayılar ve oranlar arasındaki niceliksel büyüklük ilişkisini zihninde kurgulayamaz, parmaklarıyla saymaya çalışır ama yapamaz."
    elif durum == "Bedensel Yetersizlik": return f"'{surec_kisa}' adımını zihnen anlasa da, bu adım çok ince motor beceri (hızlı çizim/kesme) gerektirdiği için fiziksel olarak geride kalır ve üzülür."
    elif durum == "Düşük Motivasyon": return f"'{surec_kisa}' adımının gerçekte ne işe yarayacağını anlamadığı için 'Bunu bilmek benim ne işime yarayacak?' diyerek soruyu çözmeyi reddeder."
    return f"'{surec_kisa}' adımında genel bir matematiksel güçlük yaşar."

def ai_profil_tepkisi_uret(ogrenci_adi, durum, kazanim_kod, surec, eylem_1, eylem_2, materyal_etiketi):
    surec_kisa = surec.split(")", 1)[1].strip() if ")" in surec else surec
    e1_tur = "duyussal" if any(kw in eylem_1 for kw in ["kabul ederek", "neyi kaçırdığını", "esneklik sağlamak"]) else "diger"
    e2_tur = "kesif" if any(kw in eylem_2 for kw in ["keşfetmesini", "örnekle açıklamasını", "temsile dönüştürmek", "genellemesini"]) else "ezber"
    d1 = (e1_tur == "duyussal")
    d2 = (e2_tur == "kesif")
    materyalsiz = (materyal_etiketi == "Materyal Kullanmadan İlerle")
    mat_isim = "sözel yönergeler" if materyalsiz else f"'{materyal_etiketi}'"

    if durum == "Disleksi":
        if materyalsiz: return f"😭 **{ogrenci_adi} ({durum}):** Öğretmenin sözlerine rağmen ortada görsel/dokunsal bir materyal olmadığı için rakamlar beynimde daha çok karıştı, tamamen pes ettim."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Öğretmenin yaklaşımı bana anlamlı gelmedi, {mat_isim} olsa da formülü ezberlemem imkansız."
        return f"💡 **{ogrenci_adi} ({durum}):** Öğretmenimin yargılamayan sesi beni rahatlattı. {mat_isim} sayesinde sembollerin yönünü ve sırasını dokunarak ayırabiliyorum!"
    elif durum == "Otizm Spektrumu":
        if materyalsiz: return f"😭 **{ogrenci_adi} ({durum}):** Açıklamalar çok soyut. {mat_isim} olmadan adımları öngöremediğim için sallanmam hızlandı, kulaklarımı kapattım."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Kuralları veya ezberi dayatması bende kriz yarattı, dış dünyayla iletişimimi kestim."
        return f"💡 **{ogrenci_adi} ({durum}):** Adımların {mat_isim} ile net ve öngörülebilir şekilde sunulması beni sakinleştirdi. Şimdi ne yapacağımı tam biliyorum."
    elif durum == "Üstün Yetenekli":
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Bana sadece kuralı ezberletmeye çalışıyor. Bu çok sıkıcı ve mantıksız, oflayarak dersi dinlemeyi bıraktım."
        return f"💡 **{ogrenci_adi} ({durum}):** İşte bu! Öğretmenin sorduğu açık uçlu soru ve {mat_isim} ile kavramın asıl örüntüsünü kendi başıma formülize edebilirim."
    elif durum == "Yüksek Kaygılı":
        if e1_tur != "duyussal": return f"😭 **{ogrenci_adi} ({durum}):** Akademik süreci (kuralları) doğrudan hatırlatması beni daha çok strese soktu. Donup kaldım, hiçbir şey düşünemiyorum."
        if not d2: return f"😕 **{ogrenci_adi} ({durum}):** Öğretmen güven verdi ama benden doğrudan işlemi (ezberi) istiyor. Yanlış yapmaktan hala korkuyorum."
        return f"💡 **{ogrenci_adi} ({durum}):** Yargılamayan güvenli yaklaşımı beni rahatlattı. {mat_isim} ile hata yapma korkusu olmadan küçük bir adım atabilirim."
    elif durum == "DEHB":
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Uzun ve pasif açıklamalar çok sıkıcı. Ne dediğini takip edemedim, kalemimle ritim tutmaya devam ediyorum."
        return f"💡 **{ogrenci_adi} ({durum}):** Doğrudan {mat_isim} ile aktif bir şeyler (dokunmak/hareket ettirmek) yapmak dikkatimi tam olarak konuya çekti!"
    elif durum == "İşitme Yetersizliği":
        if materyalsiz: return f"😭 **{ogrenci_adi} ({durum}):** Öğretmen sadece konuşarak anlattığı ({mat_isim}) ve görsel destek olmadığı için hiçbir şeyi anlayamadım, boş bakıyorum."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** {mat_isim} var ama yönergeler açıklayıcı değildi. Neyi ezberlemem gerektiğini anlamadım."
        return f"💡 **{ogrenci_adi} ({durum}):** Bana dönük net ifadeler ve {mat_isim} sayesinde görsel ipuçlarını yakaladım. Artık adımları takip edebiliyorum!"
    elif durum == "Az Gören":
        if materyalsiz: return f"😭 **{ogrenci_adi} ({durum}):** Göremediğim şeyleri sadece sesle anlatması zihnimde canlanmıyor, tamamen kayboldum."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** {mat_isim} sunuldu ancak ezbere ve küçük detaylara odaklandığı için detayları seçemiyorum."
        return f"💡 **{ogrenci_adi} ({durum}):** Net, betimleyici ses tonu ve {mat_isim} sayesinde kavramı ellerimle/yakından hissederek algıladım, sürece dahil oldum!"
    elif durum == "Diskalkuli":
        if materyalsiz: return f"😭 **{ogrenci_adi} ({durum}):** {mat_isim} (somutluk) olmadan sayılar beynimde hiçbir şey ifade etmiyor, sadece havada uçuşan anlamsız kelimeler..."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Öğretmen benden zihinden ezber bekliyor. İşlemi ve oranları yine kurgulayamadım."
        return f"💡 **{ogrenci_adi} ({durum}):** Sayıların ve oranların gerçekte ne kadar büyük/küçük olduğunu {mat_isim} (somut model) sayesinde ellerimle gördüm. Mantığı şimdi oturdu!"
    elif durum == "Bedensel Yetersizlik":
        if materyalsiz: return f"😕 **{ogrenci_adi} ({durum}):** Zihinsel olarak anlasam da, {mat_isim} ve erişilebilirliğim sağlanmadığı için işleme aktif katılamıyorum."
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** {mat_isim} masaya konsa da süreç hızlı veya benim katılımıma kapalı tasarlandığı için izleyici kalıyorum."
        return f"💡 **{ogrenci_adi} ({durum}):** Zihinsel olarak katılabilmem için erişilebilir {mat_isim} ve uygun alternatif yanıt yöntemi sunuldu. Kendimi dahil hissettim!"
    elif durum == "Düşük Motivasyon":
        if not (d1 and d2): return f"😕 **{ogrenci_adi} ({durum}):** Bana yine sadece kuralı ezberletip sınav için çözmemi istiyor, hiç umurumda değil."
        return f"💡 **{ogrenci_adi} ({durum}):** Kavramın günlük yaşam bağlamıyla sunulması ve {mat_isim} ilgimi çekti. Ne işe yaradığını gördüğüm için işlemi deneyeceğim."
    return f"💡 **{ogrenci_adi} ({durum}):** Öğretmenin yaklaşımıyla sakinleşir ve {mat_isim} desteği sayesinde işlemi kavramaya başlar."
     # ==========================================
# 5. 2024 TYMM ORTAOKUL MATEMATİK TAM MÜFREDATI
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler (1)", "1. Tema: Sayılar ve Nicelikler (2)", "2. Tema: İşlemlerle Cebirsel Düşünme", "3. Tema: Geometrik Şekiller", "4. Tema: Geometrik Nicelikler", "5. Tema: İstatistiksel Araştırma Süreci", "6. Tema: Veriden Olasılığa"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {"kod": "MAT.5.1.1", "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme", "surec": ["a) Çok basamaklı sayılar hakkında bilgi toplar.", "b) Ortak özellikleri belirler.", "c) Farklılıkları belirler.", "ç) Örüntüler üzerinden önermelerde bulunur."], "hook": "Kütüphane arşiv kodlama sistemi veya astronomik uzaklıklar.", "somut_materyal_onerisi": "Çok tabanlı bloklar (MAB), basamak değer kartları, renkli pullar ve bölük tabloları."},
                {"kod": "MAT.5.1.2", "cikti": "Doğal sayılar ve işlemler içeren gerçek yaşam problemlerini çözebilme", "surec": ["a) Sayı ve işlem bileşenlerini belirler.", "b) İşlemler arasındaki ilişkiyi belirler.", "c) Uygun temsillere dönüştürür.", "ç) Kendi ifadeleri ile açıklar.", "d) Stratejiler geliştirir.", "e) Çözüm için uygular.", "f) Stratejiyi değiştirir.", "g) Kısa yolları değerlendirir.", "ğ) Farklı problemlere geneller.", "h) Örneklerle değerlendir."], "hook": "Okul gezisi bütçesi hesaplamaları.", "somut_materyal_onerisi": "Gerçek paralar, şemalar, kavram haritaları."}
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {"kod": "MAT.5.1.3", "cikti": "Gerçek yaşam durumlarına karşılık gelen kesirleri farklı biçimlerde temsil edebilme", "surec": ["a) Kesirlerin farklı gösterimlerinin kullanımını anlar.", "b) Farklı modelleri seçer.", "c) Seçilen modelleri kullanır.", "ç) Modelleri farklı gösterimlerle yorumlar.", "d) Modelleri karşılaştırır.", "e) Kullanışlılığa karar verir."], "hook": "Mutfak ölçülerinde veya pasta paylaşımlarında çeyrek/yarım ilişkileri.", "somut_materyal_onerisi": "Yüzlük kartlar, sayı doğruları, kesir takımları."},
                {"kod": "MAT.5.1.4", "cikti": "Farklı gösterimlerle ifade edilen kesirlerin karşılaştırılmasına yönelik çıkarım yapabilme", "surec": ["a) Karşılaştırmaya yönelik varsayımda bulunur.", "b) Genellemeleri belirler.", "c) Varsayımını modeller üzerinde gösterir.", "ç) Matematiksel önermeleri sunar.", "d) Önermelerin katkısını açıklar."], "hook": "Market indirim oranlarının veya cihaz şarj yüzdelerinin karşılaştırılması.", "somut_materyal_onerisi": "Şeffaf kesir kartları, onluk taban blokları, 100'lük ızgaralar."}
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme": [
                {"kod": "MAT.5.2.1", "cikti": "Eşitliğin korunumuna ve işlem özelliklerine yönelik çıkarım yapabilme", "surec": ["a) Eşitliğin korunumuna yönelik varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Örnekler üzerinden sınar.", "ç) Önermeyi sözel ve sembolik sunar.", "d) Önermenin katkısına gerekçe sunar."], "hook": "Eşit kollu terazi ile denge durumu oluşturma.", "somut_materyal_onerisi": "Eşit kollu terazi (denklem terazisi), birim küpler."},
                {"kod": "MAT.5.2.2", "cikti": "Karşılaştığı günlük hayat ya da matematiksel durumlarda işlem önceliğini yorumlayabilme", "surec": ["a) İşlem önceliğini inceler.", "b) İşlem önceliğini uygular.", "c) İşlem önceliğini açıklar."], "hook": "Fatura hesaplamaları veya çoklu indirim uygulamaları.", "somut_materyal_onerisi": "İşlem ağaçları, parantez blokları (renkli kartonlar)."},
                {"kod": "MAT.5.2.3", "cikti": "Sayı ve şekil örüntülerinin kuralına ilişkin muhakeme yapabilme", "surec": ["a) Örüntülerdeki ilişkilere yönelik varsayımda bulunur.", "b) Genellemeleri belirler.", "c) Varsayımını sınar.", "ç) Önermeyi sunar.", "d) Gerekçeler sunar.", "e) Kapsayıcı örnekler verir.", "f) Benzer önermelere uygulanıp uygulanamayacağını değerlendirir."], "hook": "Kibrit çöpleriyle veya birim küplerle yapı inşası.", "somut_materyal_onerisi": "Kibrit çöpleri, örüntü blokları, birim kareler."},
                {"kod": "MAT.5.2.4", "cikti": "Temel aritmetik işlem içeren durumlardaki algoritmaları yorumlayabilme", "surec": ["a) Algoritmik yapıyı inceler.", "b) Algoritmik yapıyı dönüştürür.", "c) Matematiksel ilişkileri sözlü olarak ifade eder."], "hook": "Aşama aşama yemek tarifi veya basit bilgisayar komutları.", "somut_materyal_onerisi": "Akış şeması kartları, adım kartları."}
            ],
            "3. Tema: Geometrik Şekiller": [
                {"kod": "MAT.5.3.1", "cikti": "Temel geometrik çizimler için matematiksel araç ve teknolojiden yararlanabilme", "surec": ["a) Gerekli araç ve teknolojileri tanır.", "b) Uygun olanları belirler.", "c) Uygun araç ve teknolojileri kullanır."], "hook": "Pusula ve harita üzerinde yön/konum belirleme.", "somut_materyal_onerisi": "GeoGebra, pergel, gönye, iletki."},
                {"kod": "MAT.5.3.2", "cikti": "Temel geometrik çizimlere dayalı deneyimlerini yansıtabilme", "surec": ["a) Deneyimlerini gözden geçirir.", "b) Özelliklere yönelik çıkarım yapar.", "c) Çıkarımını değerlendirir."], "hook": "Mimari bir yapının çizimlerini analiz etme.", "somut_materyal_onerisi": "Aydınger kağıdı (katlama), dinamik geometri yazılımları."},
                {"kod": "MAT.5.3.3", "cikti": "Açıları ölçmek için matematiksel araç ve teknolojiden yararlanabilme", "surec": ["a) Araç ve teknolojiyi tanır.", "b) Uygun aracı belirler.", "c) Uygun aracı kullanır."], "hook": "Kapı açıklığı veya çatı eğimi ölçümleri.", "somut_materyal_onerisi": "Büyük boy iletki (açıölçer), GeoGebra."},
                {"kod": "MAT.5.3.4", "cikti": "Düzlemde iki veya üç doğrunun birbirine göre durumuna bağlı olarak oluşabilecek açılara dair çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Açıları belirleyerek listeler.", "c) Varsayımlarıyla karşılaştırır.", "ç) Önerme sunar.", "d) Gerekçe sunar."], "hook": "Kavşaklardaki yolların kesişimi.", "somut_materyal_onerisi": "Hareketli çubuklar, şeffaf asetatlar, GeoGebra."},
                {"kod": "MAT.5.3.5", "cikti": "Çokgenleri düzlemde ardışık olarak kesişen doğruların oluşturduğu kapalı şekiller olarak yorumlayabilme", "surec": ["a) Durumları inceler.", "b) Çokgenler oluşturur.", "c) Çokgenlerin meydana geldiğini ifade eder."], "hook": "Esnemiş lastikle çivili tahta üzerinde şekiller oluşturma.", "somut_materyal_onerisi": "Çivili tahta (Geoboard) ve renkli lastikler."},
                {"kod": "MAT.5.3.6", "cikti": "Çokgenlerin özellikleri ile ilgili edindiği deneyimleri yansıtabilme", "surec": ["a) Deneyimlerini gözden geçirir.", "b) Kenar ve açı özelliklerine dair çıkarım yapar.", "c) Değerlendirir."], "hook": "Trafik levhalarının şekil özellikleri.", "somut_materyal_onerisi": "Tangram, örüntü blokları."},
                {"kod": "MAT.5.3.7", "cikti": "Matematiksel araç ve teknoloji yardımıyla düzlemde iki noktada kesişen çember çiftinin merkezleri ve kesişim noktalarından biri ile inşa edilen üçgenlerin kenar özelliklerine yönelik çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Üçgenleri belirler.", "c) Varsayımları ile karşılaştırır.", "ç) Önermeler şeklinde ifade eder.", "d) Katkısını değerlendir."], "hook": "Radar kesişim alanları veya pusula çizimleri.", "somut_materyal_onerisi": "Pergel, GeoGebra çember modülü."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.5.4.1", "cikti": "Kenar uzunlukları doğal sayı olan bir dikdörtgenin çevre uzunluğu verildiğinde kenar uzunluklarını yorumlayabilme", "surec": ["a) Kenar uzunluklarını inceler.", "b) Dikdörtgen oluşturur.", "c) Aynı çevre uzunluğuna sahip olabileceğini açıklar."], "hook": "Farklı boyutlardaki resim çerçevelerinin kenar uzunlukları.", "somut_materyal_onerisi": "İzometrik kağıt, esnek çevre ipleri."},
                {"kod": "MAT.5.4.2", "cikti": "Birim karelerden yola çıkarak dikdörtgenin alanını değerlendirebilme", "surec": ["a) Ölçüt olarak belirler.", "b) Alanını ölçer.", "c) Kenar uzunluğu ile ilişkisini inceler.", "ç) Yargıda bulunur."], "hook": "Odanın tabanına fayans döşeme.", "somut_materyal_onerisi": "Plastik birim kareler, yüzlük ızgaralar."},
                {"kod": "MAT.5.4.3", "cikti": "Kenar uzunlukları doğal sayı olan bir dikdörtgenin alanının ölçüsü verildiğinde çevre uzunluğunu, çevre uzunluğu verildiğinde alanını yorumlayabilme", "surec": ["a) Çevre ve alanı inceler.", "b) Farklı dikdörtgenlerin özelliklerini belirler.", "c) Çevre ve alanın farklı olabileceğini ifade eder."], "hook": "Aynı alana sahip farklı arsa parselleri tasarlama.", "somut_materyal_onerisi": "Birim küpler (Alan-Çevre ilişkisi için)."},
                {"kod": "MAT.5.4.4", "cikti": "Dikdörtgenin çevre uzunluğu ve alanı ile ilgili problemleri çözebilme", "surec": ["a) Matematiksel bileşenleri belirler.", "b) İlişkileri belirler.", "c) Temsillere dönüştürür.", "ç) İfadeleri ile açıklar.", "d) Tahminde bulunur ve stratejiler geliştirir.", "e) Çözüm için uygular.", "f) Stratejiyi değiştirir.", "g) Çözüm yollarını değerlendirir.", "ğ) Geneller.", "h) Matematiksel örneklerle değerlendirir."], "hook": "Halı veya parke siparişi için maliyet hesaplama.", "somut_materyal_onerisi": "Kroki çizimleri, kareli kağıt, minyatür halı/parke modelleri."}
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {"kod": "MAT.5.5.1", "cikti": "Kategorik veri ile çalışabilme ve veriye dayalı karar verebilme", "surec": ["a) Araştırma gerektiren durumları fark eder.", "b) Araştırma soruları oluşturur.", "c) Plan yapar.", "ç) Veri toplar.", "d) Görselleştirme aracını seçme gerekçelerini belirtir.", "e) Analiz eder.", "f) Gerekçeler sunar.", "g) Yeniden planlar."], "hook": "Okulda en sevilen derslerin anketini yapma.", "somut_materyal_onerisi": "Post-it notlar, grafik kağıtları, Excel."},
                {"kod": "MAT.5.5.2", "cikti": "Başkaları tarafından oluşturulan kategorik veriye dayalı istatistiksel sonuç veya yorumları tartışabilme", "surec": ["a) İstatistiksel temellendirme yapar.", "b) Hataları ya da yanlılıkları tespit eder.", "c) Çürütür ya da kabul eder."], "hook": "Haberlerdeki veya reklamlardaki grafiklerin doğruluğunu sorgulama.", "somut_materyal_onerisi": "Yanıltıcı gazete grafikleri örnekleri, tartışma kartları."}
            ],
            "6. Tema: Veriden Olasılığa": [
                {"kod": "MAT.5.6.1", "cikti": "Herhangi bir olayın olasılığının 0 (imkânsız) ile 1 (kesin) arasında (0 ve 1 dâhil) olduğunu (olasılık spektrumu) yorumlayabilme", "surec": ["a) Olayları inceler.", "b) Tahminlerini sayı temsillerine dönüştürür.", "c) 0 ile 1 arasında olduğunu ifade eder."], "hook": "Bir zar atıldığında 7 gelme veya 6'dan küçük gelme olasılığı.", "somut_materyal_onerisi": "Zarlar, olasılık çubuğu (0'dan 1'e spektrum modeli)."},
                {"kod": "MAT.5.6.2", "cikti": "Olayları az ya da çok olasılıklı şeklinde yapılandırabilme", "surec": ["a) İlişkiler ortaya koyar.", "b) Az veya çok olasılıklı şeklinde ortaya koyar."], "hook": "Renkli topların bulunduğu torbadan istenen rengi çekme ihtimali.", "somut_materyal_onerisi": "Şeffaf torbalar ve farklı sayılarda renkli toplar."}
            ]
        }
    },
    "6. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler (1)", "1. Tema: Sayılar ve Nicelikler (2)", "2. Tema: İşlemlerle Cebirsel Düşünme Ve Değişimler", "3. Tema: Geometrik Şekiller", "4. Tema: Geometrik Nicelikler", "5. Tema: İstatistiksel Araştırma Süreci", "6. Tema: Veriden Olasılığa"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {"kod": "MAT.6.1.1", "cikti": "Karşılaştığı problem durumlarında bir doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Modellerle gösterir.", "ç) Sözel ya da sembolik temsil ile sunar.", "d) Gerekçelerini sunar.", "e) Kapsayıcı örnekler verir.", "f) Benzer önermelere uygulanıp uygulanamayacağını değerlendirir."], "hook": "Farklı vardiyalarla çalışan işçilerin nöbet denk gelme günleri.", "somut_materyal_onerisi": "Cuisenaire çubukları, çarpım tablosu."},
                {"kod": "MAT.6.1.2", "cikti": "Bir doğal sayının 2, 3, 4, 5, 6, 9 ve 10 ile tam bölünebilme kriterlerine ilişkin çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Genellemeleri belirler.", "c) Örnekler ile sinar.", "ç) Önerme sunar.", "d) Kullanışlılığını değerlendirir."], "hook": "Grup etkinliklerinde öğrencileri artansız gruplara ayırma.", "somut_materyal_onerisi": "Yüzlük ızgarada bölünebilme örüntülerini boyama."},
                {"kod": "MAT.6.1.3", "cikti": "Bir doğal sayının asal olma durumunu ve asal çarpanlarını çözümleyebilme", "surec": ["a) Asal olup olmadığını ve asal çarpanlarını belirler.", "b) Özelliklerini ve ilişkileri belirler."], "hook": "Şifreleme algoritmaları veya Eratosthenes kalburu.", "somut_materyal_onerisi": "Asal çarpan ağacı panosu, Eratosthenes kalburu kağıdı."},
                {"kod": "MAT.6.1.4", "cikti": "Günlük hayat problemleri ya da matematiksel durumlar üzerinden ortak kat ve ortak böleni yorumlayabilme", "surec": ["a) Ortak katlarını ve ortak bölenlerini inceler.", "b) Matematiksel temsillerle ifade eder.", "c) Açıklar."], "hook": "Kumaş parçalarını eşit boylara bölme (EBOB).", "somut_materyal_onerisi": "Eşit uzunlukta kağıt şeritler, Venn şeması."}
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {"kod": "MAT.6.1.5", "cikti": "Gerçek yaşam durumlarında ondalık gösterimlerin basamak değerlerini kesirlerden yararlanarak yorumlayabilme", "surec": ["a) Basamak değerlerini inceler.", "b) Yeniden ifade eder.", "c) Açıklar."], "hook": "Market alışverişi fişlerindeki kuruş hesaplamaları.", "somut_materyal_onerisi": "Ondalık sayı kartları, ondalık modelleme blokları."},
                {"kod": "MAT.6.1.6", "cikti": "Kesir ve bölme işlemi arasındaki ilişkiye yönelik tümevarımsal akıl yürütebilme", "surec": ["a) Gözlem yapar.", "b) Örüntüleri belirler.", "c) İlişkileri geneller."], "hook": "Bütün bir pastayı eşit bölüşme problemleri.", "somut_materyal_onerisi": "Kesir takımları, dairesel dilimler."},
                {"kod": "MAT.6.1.7", "cikti": "Gerçek yaşam durumlarında karşılaşılan kesir, ondalık ve yüzde gösterimleri ile ilgili dört işlem gerektiren problemleri çözebilme", "surec": ["a) Bileşenleri belirler.", "b) İlişkiyi belirler.", "c) Uygun temsilleri kullanır.", "ç) Açıklar.", "d) Stratejiler geliştirir.", "e) Problemleri çözer.", "f) Kontrol eder.", "g) Kısa yolları değerlendirir.", "ğ) Farklı problemlere geneller.", "h) Geçerliliğini değerlendirir."], "hook": "İndirim hesaplamaları veya vergi ekleme.", "somut_materyal_onerisi": "Alışveriş oyun paraları, yüzde hesaplama çarkları."},
                {"kod": "MAT.6.1.8", "cikti": "Karşılaştığı günlük hayat ya da matematiksel durumlarda standart uzunluk ölçme birimlerini değerlendirebilme", "surec": ["a) Metreyi ölçüt olarak belirler.", "b) Ölçme yapar.", "c) Karşılaştırır.", "ç) Yargıda bulunur."], "hook": "Farklı mesafeleri (şehirlerarası vs. karınca boyu) uygun birimle ifade etme.", "somut_materyal_onerisi": "Farklı uzunluklarda (mm, cm, m) cetveller ve mezuralar."}
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme Ve Değişimler": [
                {"kod": "MAT.6.2.1", "cikti": "Gerçek yaşam durumlarında bilinen niceliklerden bilinmeyen niceliklere ilişkin muhakeme yapabilme", "surec": ["a) Nicelikleri belirler.", "b) Tablo temsili kullanarak belirler.", "c) Cebirsel olarak ifade eder.", "ç) Anlamını açıklar.", "d) Varsayımda bulunur.", "e) Genellemeleri belirler.", "f) Sınır.", "g) Yeniden ifade eder.", "ğ) Katkısını ifade eder."], "hook": "Taksi ücreti (sabit açılış + kilometre başı ücret) hesaplama.", "somut_materyal_onerisi": "Cebir karoları, fonksiyon makinesi çizimleri."},
                {"kod": "MAT.6.2.2", "cikti": "Sayı ve şekil örüntülerini yorumlayabilme", "surec": ["a) İlişkileri inceler.", "b) İfade eder.", "c) Cebirsel olarak ifade eder."], "hook": "Fayans döşeme desenleri.", "somut_materyal_onerisi": "Geometrik şekiller seti, renkli bloklar."},
                {"kod": "MAT.6.2.3", "cikti": "Cebirsel ifadeler içeren durumlardaki algoritmaları yorumlayabilme", "surec": ["a) Algoritmik yapıyı inceler.", "b) Dönüştürür.", "c) Sözlü olarak ifade eder."], "hook": "Basit bilgisayar programlama mantığı (Girdi -> İşlem -> Çıktı).", "somut_materyal_onerisi": "Akış şeması kartları."}
            ],
            "3. Tema: Geometrik Şekiller": [
                {"kod": "MAT.6.3.1", "cikti": "Düzlemde iki paralel doğru ve bir kesen ile oluşan açıları sınıflandırabilme", "surec": ["a) Açıları belirler.", "b) Ayrıştırır.", "c) Tasnif eder.", "ç) Adlandırır."], "hook": "Köprü veya inşaat iskelelerindeki çapraz bağlantılar.", "somut_materyal_onerisi": "Renkli şeffaf açılar, GeoGebra açı kaydırma."},
                {"kod": "MAT.6.3.2", "cikti": "Matematiksel araç ve teknolojiden yararlanarak iki paralel doğrunun iki kesenle oluşturduğu şekillerin özelliklerine dair çıkarım yapabilme", "surec": ["a) Varsayımda bulunur.", "b) Listeler.", "c) Karşılaştırır.", "ç) Önermeler sunar.", "d) Değerlendirir."], "hook": "Paralel yollar arasında kalan üçgen veya dörtgen şeklindeki parklar.", "somut_materyal_onerisi": "Hareketli doğru çubukları, GeoGebra."},
                {"kod": "MAT.6.3.3", "cikti": "Matematiksel araç ve teknolojiden yararlanarak birbirlerini ortalayan doğru parçalarını köşegen kabul eden dörtgenlere yönelik çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Oluşturur ve listeler.", "c) Karşılaştırır.", "ç) Önermeler sunar.", "d) Değerlendirir."], "hook": "Uçurtma yapımı (köşegenlerin ortalanması/dik kesişmesi).", "somut_materyal_onerisi": "Geoboard (Çivili tahta), köşegen şeritleri."},
                {"kod": "MAT.6.3.4", "cikti": "Üçgen, yamuk, paralelkenar, eşkenar dörtgen, dikdörtgen ve karenin açıları ile ilgili problemleri çözebilme", "surec": ["a) Bileşenleri belirler.", "b) İlişkiyi belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Stratejiler geliştirir.", "e) Uygular.", "f) Kontrol eder.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Farklı şekillerdeki bahçelerin sınır açılarını hesaplama.", "somut_materyal_onerisi": "Açı ölçer, çokgen birleştirme/parçalama setleri."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.6.4.1", "cikti": "Uzunluk ve alan ölçme birimleri arasındaki ilişkilerle ilgili analojik akıl yürütebilme", "surec": ["a) Gözlemler.", "b) Tespit eder.", "c) Çıkarım yapar."], "hook": "Ev planında metrekare ile kenar metre uzunluğu ilişkisi.", "somut_materyal_onerisi": "Birim karelerden oluşan 10x10 levhalar."},
                {"kod": "MAT.6.4.2", "cikti": "Dikdörtgenin alan bağıntısına yönelik deneyimlerini paralelkenar ve üçgenin alan bağıntılarına yansıtabilme", "surec": ["a) Gözden geçirir.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "Üçgen şeklindeki bayrakların veya yelkenlerin kumaş miktarını hesaplama.", "somut_materyal_onerisi": "Karton dikdörtgeni kesip üçgene/paralelkenara dönüştürme materyali."},
                {"kod": "MAT.6.4.3", "cikti": "Geometrik şekillerin alanları ile modellenen gerçek yaşam durumlarına yönelik problem çözebilme", "surec": ["a) Bileşenleri belirler.", "b) İlişkiyi belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Stratejiler geliştirir.", "e) Uygular.", "f) Kontrol eder.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Farklı şekillerden oluşan bir tarlanın toplam alanını bulma.", "somut_materyal_onerisi": "Tangram veya farklı geometrik şekillerden oluşan yapbozlar."},
                {"kod": "MAT.6.4.4", "cikti": "Çemberin uzunluğu ile çap uzunluğu arasındaki ilişkiye yönelik çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Listeler.", "c) Karşılaştırır.", "ç) Önermeler sunar.", "d) Değerlendirmeler yapar."], "hook": "Bisiklet tekerleğinin çevresi ile çapı arasındaki oran (Pi).", "somut_materyal_onerisi": "Farklı boylarda dairesel cisimler, ip, esnek mezura."},
                {"kod": "MAT.6.4.5", "cikti": "Çap veya yarıçap uzunluğu verilen bir çemberin uzunluğu ile ilgili problemleri çözebilme", "surec": ["a) Bileşenleri belirler.", "b) İlişkiyi belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Stratejiler geliştirir.", "e) Uygular.", "f) Kontrol eder.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Dönme dolap veya saat yelkovanının çizdiği yol.", "somut_materyal_onerisi": "Telden çember modelleri."},
                {"kod": "MAT.6.4.6", "cikti": "Çemberde merkez açının ölçüsü ile gördüğü yayın uzunluğu arasındaki ilişkiye dair tümevarımsal akıl yürütebilme", "surec": ["a) Gözlem yapar.", "b) Örüntü bulur.", "c) Genelleme yapar."], "hook": "Pizza veya yaş pasta dilimlerinin yay uzunluğu.", "somut_materyal_onerisi": "GeoGebra dinamik yay aracı, dairesel kesir takımları."}
            ],
            "5. Tema: İstatistiksel Araştırma Süreci": [
                {"kod": "MAT.6.5.1", "cikti": "Kategorik veya nicel (kesikli) veri ile çalışabilme ve veriye dayalı karar verebilme", "surec": ["a) Fark eder.", "b) Araştırma soruları oluşturur.", "c) Plan yapar.", "ç) Veri toplar.", "d) Gerekçelerini belirtir.", "e) Analiz eder.", "f) Gerekçeler sunar.", "g) Yeniden planlar."], "hook": "Okul başkanlığı seçimi anket sonuçları.", "somut_materyal_onerisi": "Fiziksel anket formları, grafik çizim kağıtları."},
                {"kod": "MAT.6.5.2", "cikti": "Başkaları tarafından oluşturulan kategorik veya nicel (kesikli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme", "surec": ["a) İstatistiksel temellendirme yapar.", "b) Hataları ya da yanlılıkları tespit eder.", "c) Çürütür ya da kabul eder."], "hook": "Reklamlardaki abartılı istatistiksel iddiaların analizi.", "somut_materyal_onerisi": "Yanıltıcı gazete grafikleri örnekleri, tartışma kartları."}
            ],
            "6. Tema: Veriden Olasılığa": [
                {"kod": "MAT.6.6.1", "cikti": "Bir olayın olasılığını gözleme dayalı tahmin edebilme", "surec": ["a) İlişkilendirir.", "b) Çıkarım yapar.", "c) Yargıda bulunur."], "hook": "Spor müsabakalarında veya zar atışında tahminde bulunma.", "somut_materyal_onerisi": "Zarlar, madeni paralar, dijital olasılık simülatörü."}
            ]
        }
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler (1)",
            "1. Tema: Sayılar ve Nicelikler (2)",
            "2. Tema: İşlemlerle Cebirsel Düşünme Ve Değişimler",
            "3. Tema: Dönüşüm",
            "4. Tema: Geometrik Nicelikler (1)",
            "4. Tema: Geometrik Nicelikler (2)",
            "5. Tema: Geometrik Şekiller",
            "6. Tema: İstatistiksel Araştırma",
            "7. Tema: Veriden Olasılığa"
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler (1)": [
                {"kod": "MAT.7.1.1", "cikti": "Gerçek yaşam ya da matematiksel durumlarda doğal sayı, tam sayı ve rasyonel sayıları yorumlayabilme", "surec": ["a) İnceleyer.", "b) Genişletir ve açıklar.", "c) Açıklar."], "hook": "Asansör katları (tam sayılar) veya pizza dilimi (rasyonel).", "somut_materyal_onerisi": "Sayı doğrusu şeritleri."},
                {"kod": "MAT.7.1.2", "cikti": "Gerçek yaşam durumlarında rasyonel sayıların ondalık gösterimlerini yansıtabilme", "surec": ["a) İnceleyer.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "Bölüşülemeyen miras veya bitmeyen hesaplamalar (devirli ondalık).", "somut_materyal_onerisi": "Hesap makinesi, uzun bölme kağıtları."},
                {"kod": "MAT.7.1.3", "cikti": "Rasyonel sayıların karşılaştırma ve sıralama ilişkilerini yorumlayabilme", "surec": ["a) İnceleyer.", "b) İfade eder.", "c) Açıklar."], "hook": "Farklı uzunluklardaki vidaların veya kumaşların sıralanması.", "somut_materyal_onerisi": "Kesir çubukları, dikey/yatay sayı doğrusu."},
                {"kod": "MAT.7.1.4", "cikti": "Rasyonel sayılar ve işlemler içeren gerçek yaşam problemlerini çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Stratejiler oluşturur.", "e) Çözer.", "f) Kontrol eder.", "g) İnceleyer.", "ğ) Genellemeler yapar.", "h) Değerlendirir."], "hook": "Hisse senedi değişimleri, bütçe yönetimi.", "somut_materyal_onerisi": "Gerçek fişler, kesir takımları."}
            ],
            "1. Tema: Sayılar ve Nicelikler (2)": [
                {"kod": "MAT.7.1.5", "cikti": "Gerçek yaşam durumları üzerinden oran ilişkileri hakkında muhakeme yapabilme", "surec": ["a) Ayırt eder.", "b) Belirler.", "c) İfade eder.", "ç) Açıklar.", "d) Varsayımlarda bulunur.", "e) Genellemeleri belirler.", "f) Sınır.", "g) Sunar.", "ğ) Gerekçeler sunar."], "hook": "Tariflerdeki malzemelerin orantılı artırılması veya harita ölçekleri.", "somut_materyal_onerisi": "Renkli sıvı ölçekleri, oran tabloları."},
                {"kod": "MAT.7.1.6", "cikti": "Gerçek yaşam durumları üzerinden orantılı durumları yorumlayabilme", "surec": ["a) İnceleyer.", "b) İfade eder.", "c) Yeniden açıklar."], "hook": "Araç hızı ile varış süresi arasındaki ilişki.", "somut_materyal_onerisi": "Grafik kağıdı, doğru orantı modelleri."},
                {"kod": "MAT.7.1.7", "cikti": "Gerçek yaşam durumları üzerinden doğru orantılı durumlara ilişkin problemleri çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) Dönüştürür.", "ç) İfade eder.", "d) Stratejiler oluşturur.", "e) Kullanır.", "f) Doğrular.", "g) İnceleyer.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Döviz çevirme, KDV hesaplama.", "somut_materyal_onerisi": "Orantı çarkları, denge terazisi."}
            ],
            "2. Tema: İşlemlerle Cebirsel Düşünme Ve Değişimler": [
                {"kod": "MAT.7.2.1", "cikti": "Gerçek yaşam durumları ya da matematiksel durumlar üzerinden cebirsel ifadelerle toplama, çıkarma ve bir rasyonel sayıyla çarpma işlemlerini yorumlayabilme", "surec": ["a) İnceleyer.", "b) Kullanır.", "c) Açıklar."], "hook": "Maaş artış oranının formülize edilmesi.", "somut_materyal_onerisi": "Cebir karoları (Algebra tiles)."},
                {"kod": "MAT.7.2.2", "cikti": "Birinci dereceden bir bilinmeyenli denklem ve birinci dereceden bir bilinmeyenli eşitsizlik içeren gerçek yaşam problemlerini çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) İfade eder.", "ç) İfade eder.", "d) Strateji oluşturur.", "e) Uygular.", "f) Değiştirir.", "g) İnceleyer.", "ğ) Yapar.", "h) Değerlendirir."], "hook": "Limit hesaplamaları, yaş problemleri.", "somut_materyal_onerisi": "Fiziksel denklem terazisi, sayı doğrusu."},
                {"kod": "MAT.7.2.3", "cikti": "Sayılar ve özelliklerini içeren ispatlara ilişkin matematiksel muhakeme yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Listeler.", "c) Sınır.", "ç) İfade eder.", "d) Gerekçeler sunar.", "e) Koşar.", "f) Uyarlar."], "hook": "Sihirli kareler, ardışık sayı toplamları.", "somut_materyal_onerisi": "Sayı örüntüsü blokları."},
                {"kod": "MAT.7.2.4", "cikti": "Temel aritmetik ve cebirsel ifadelerle işlem içeren durumlardaki süreci algoritma ifade yöntemlerini kullanarak yapılandırabilme", "surec": ["a) Açıklar.", "b) Oluşturur."], "hook": "Basit bilgisayar programlaması, kodlama adımları.", "somut_materyal_onerisi": "Akış şeması tahtası, kod blokları."}
            ],
            "3. Tema: Dönüşüm": [
                {"kod": "MAT.7.3.1", "cikti": "Şekillerin yansıma dönüşümü altındaki görüntülerinin oluşturulmasına dair çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Oluşturur.", "c) Karşılaştırmalar yapar.", "ç) Önermeler sunar.", "d) Değerlendirir."], "hook": "Aynadaki yansımalar, kelebek kanadındaki simetri.", "somut_materyal_onerisi": "Simetri aynası (Mira), şeffaf asetat kağıdı (katlama), noktalı kağıt."},
                {"kod": "MAT.7.3.2", "cikti": "Yansıma dönüşümündeki deneyimlerini orta dikme ve açıortay inşasına yansıtabilme", "surec": ["a) Gözden geçirir.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "İki şehre eşit uzaklıktaki buluşma noktasının (orta dikme) belirlenmesi.", "somut_materyal_onerisi": "Pergel, gönye, dinamik geometri yazılımı (GeoGebra)."}
            ],
            "4. Tema: Geometrik Nicelikler (1)": [
                {"kod": "MAT.7.4.1", "cikti": "Eş küplerle oluşturulan yapılar ile görünümleri arasındaki ilişkiyi çözümleyebilme", "surec": ["a) Çizer ve oluşturur.", "b) Belirler."], "hook": "Mimari bir maketin (önden/üstten/yandan) plan çizimi.", "somut_materyal_onerisi": "Birim küpler, izometrik kağıt."},
                {"kod": "MAT.7.4.2", "cikti": "Dikdörtgenler prizmasının yüzey alanını yorumlayabilme", "surec": ["a) İnceleyer.", "b) İfade eder.", "c) Hesaplar."], "hook": "Hediye paketini kaplamak için gereken ambalaj kağıdı miktarının hesaplanması.", "somut_materyal_onerisi": "Prizma açınımı (karton), yüzey alanı kaplama yapışkanları."},
                {"kod": "MAT.7.4.3", "cikti": "Dikdörtgenler prizmasının hacmini eş nesneler aracılığıyla yorumlayabilme", "surec": ["a) İnceleyer.", "b) Oluşturur.", "c) İfade eder."], "hook": "Depoya eş büyüklükteki kolilerin yerleştirilmesi.", "somut_materyal_onerisi": "Şeffaf prizma kutusu, doldurmak için birim küpler."},
                {"kod": "MAT.7.4.4", "cikti": "Dikdörtgenler prizmasının hacim bağıntısını değerlendirebilme", "surec": ["a) Belirler.", "b) Sayar.", "c) Karşılaştırır.", "ç) İfade eder."], "hook": "Akvaryumun alabileceği su miktarı.", "somut_materyal_onerisi": "Katman katman dizilebilen bloklar."},
                {"kod": "MAT.7.4.5", "cikti": "Hacim ölçme birimleri arasındaki ilişkileri değerlendirebilme", "surec": ["a) Belirler.", "b) Yapar.", "c) Karşılaştırır.", "ç) Yargıda bulunur."], "hook": "İlaç dozları (ml) veya barajdaki su miktarı (m3).", "somut_materyal_onerisi": "Dereceli silindirler, sıvı hacim seti."},
                {"kod": "MAT.7.4.6", "cikti": "Günlük hayat durumlarında dikdörtgenler prizmaları ile modellenen cisimlerin yüzey alanı ve hacmine yönelik problem çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Geliştirir.", "e) Uygular.", "f) Değiştirir.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Kutu tasarımında malzeme israfını önleme problemi.", "somut_materyal_onerisi": "Karton ambalaj projeleri."}
            ],
            "4. Tema: Geometrik Nicelikler (2)": [
                {"kod": "MAT.7.4.7", "cikti": "Dikdörtgenin, paralelkenarın alanına ve çemberin uzunluğuna İlişkin deneyimlerini dairenin alan bağıntısına yansıtabilme", "surec": ["a) Gözden geçirir.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "Dairesel bir masanın yüzeyini kumaşla kaplama.", "somut_materyal_onerisi": "Daireyi dilimleyip paralelkenara benzeten yapboz."},
                {"kod": "MAT.7.4.8", "cikti": "Çemberde merkez açı ve gördüğü yay uzunluğu arasındaki İlişkiden yola çıkarak daire ve daire diliminin alanları arasındaki ilişkiye yönelik analojik akıl yürütebilme", "surec": ["a) Gözlemler.", "b) Tespit eder.", "c) Çıkarım yapar."], "hook": "Pasta diliminin veya sileceklerin süpürdüğü cam alanı.", "somut_materyal_onerisi": "Daire dilimi (fraksiyon) takımı."},
                {"kod": "MAT.7.4.9", "cikti": "Eşkenar dörtgen ve yamuğun alan bağıntılarına dair çıkarım yapabilme", "surec": ["a) Varsayımda bulunur.", "b) Belirler.", "c) Karşılaştırır.", "ç) Önermeler sunar.", "d) Değerlendirir."], "hook": "Yamuk şeklindeki çatı yüzeyi hesabı.", "somut_materyal_onerisi": "Yamuğu dikdörtgene tamamlayan karton parçalar."},
                {"kod": "MAT.7.4.10", "cikti": "Günlük hayat durumlarında daire, daire dilimi, eşkenar dörtgen ve yamuğun alanına ilişkin problem çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Geliştirir.", "e) Uygular.", "f) Değiştirir.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Pencere veya parkelerin alanını bulup fiyat çıkarma.", "somut_materyal_onerisi": "Gerçek ev planı krokileri."}
            ],
            "5. Tema: Geometrik Şekiller": [
                {"kod": "MAT.7.5.1", "cikti": "Matematiksel araç ve teknolojiden yararlanarak üçgende kenarortayı, açıortayı ve yüksekliği çözümleyebilme", "surec": ["a) Belirler.", "b) Belirler."], "hook": "Çatı direkleri veya denge noktası bulma.", "somut_materyal_onerisi": "Origami (kağıt katlama) üçgenleri, GeoGebra."},
                {"kod": "MAT.7.5.2", "cikti": "Orta dikme inşasına yönelik deneyimlerini üçgende kenarortay inşasına yansıtabilme", "surec": ["a) Gözden geçirir.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "Adil bölüşüm için orta nokta bulma.", "somut_materyal_onerisi": "Pergel, gönye, dinamik yazılım."}
            ],
            "6. Tema: İstatistiksel Araştırma": [
                {"kod": "MAT.7.6.1", "cikti": "Kategorik veya nicel (sürekli) veri ile çalışabilme ve veriye dayalı karar verebilme", "surec": ["a) Fark eder.", "b) Oluşturur.", "c) Plan yapar.", "ç) Toplar.", "d) Belirtir.", "e) Analiz eder.", "f) Sunar.", "g) Yeniden planlar."], "hook": "Nüfus artış hızı veya borsa grafiği analizi.", "somut_materyal_onerisi": "Grafik panoları, Excel, iplerle canlı grafik oluşturma."},
                {"kod": "MAT.7.6.2", "cikti": "Başkaları tarafından oluşturulan kategorik veya nicel (sürekli) veriye dayalı istatistiksel sonuç veya yorumları tartışabilme", "surec": ["a) Yapar.", "b) Tespit eder.", "c) Çürütür ya da kabul eder."], "hook": "Haber spikerinin sunduğu grafik iddialarını inceleme.", "somut_materyal_onerisi": "Gazete kupürleri, yanıltıcı grafik örnekleri."}
            ],
            "7. Tema: Veriden Olasılığa": [
                {"kod": "MAT.7.7.1", "cikti": "Bir olayın ve tümleyeninin olasılığına ilişkin tümevarımsal akıl yürütebilme", "surec": ["a) Gözlemler.", "b) Bulur.", "c) Genelleme yapar."], "hook": "Kura çekilişinde kazanma ve kaybetme olasılıklarının bütünü.", "somut_materyal_onerisi": "Olasılık çarkı, renkli toplar (bütün-parça modeli)."},
                {"kod": "MAT.7.7.2", "cikti": "Aynı deneye ait olayların eşit olasılıklı olma durumlarını değerlendirebilme", "surec": ["a) Belirler.", "b) Yapar.", "c) Karşılaştırır.", "ç) Yargıda bulunur."], "hook": "Zar veya para atışı oyunlarının adaleti.", "somut_materyal_onerisi": "Oyun pulları, hileli ve normal zarlar."},
                {"kod": "MAT.7.7.3", "cikti": "Olayları ayrık olma ve ayrık olmama durumlarına göre sınıflandırabilme", "surec": ["a) Belirler.", "b) Ayrıştırır.", "c) Tasnif eder.", "ç) Etiketler."], "hook": "Kart çekme (Ör: Hem Kupa hem de As çekme).", "somut_materyal_onerisi": "Oyun kağıdı (İskambil) destesi veya çok özellikli nesneler, Venn şeması."}
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
                {"kod": "MAT.8.1.1", "cikti": "Farklı bağlamlardaki üslü ifadelere, özelliklerine ve üslü ifadelerle yapılan işlemlere ilişkin çıkarım yapabilme", "surec": ["a) Varsayımlarda bulunur.", "b) Belirler.", "c) Sınır.", "ç) İfade eder.", "d) Açıklar."], "hook": "Hücre bölünmesi veya kağıt katlama (2'nin kuvvetleri).", "somut_materyal_onerisi": "Kağıt katlama etkinliği (geometrik dizi büyümesi)."},
                {"kod": "MAT.8.1.2", "cikti": "Kareköklü ifadelerin yaklaşık değerini bulma ve işlem yapma", "surec": ["a) Belirler.", "b) İlişkilendirir.", "c) İfade eder.", "ç) Açıklar."], "hook": "Alanı 50 metrekare olarak bilinen kare odanın bir kenarını bulma.", "somut_materyal_onerisi": "Birim karelerden oluşturulan fiziksel karesel bölgeler, karekök spirali çizimi."},
                {"kod": "MAT.8.1.3", "cikti": "Sayıların rasyonel ya da irrasyonelliğini değerlendirebilme", "surec": ["a) Belirler.", "b) Elde eder.", "c) Karşılaştırır.", "ç) Yargıda bulunur."], "hook": "Pi sayısının veya altın oranın sırrı.", "somut_materyal_onerisi": "Sayı kümeleri (iç içe geçmiş kutular - Venn şeması) ve hesap makinesi deneyleri."},
                {"kod": "MAT.8.1.4", "cikti": "Gerçek sayıları ve aralıklarını sayı doğrusunda yorumlayabilme", "surec": ["a) İnceleyer.", "b) Yerleştirir.", "c) Açıklar."], "hook": "Güvenlik limitleri, hız sınırları (aralık kavramı).", "somut_materyal_onerisi": "İp üzerinde mandallı sayı doğrusu."}
            ],
            "2. Tema: Cebirsel Düşünme": [
                {"kod": "MAT.8.2.1", "cikti": "Gerçek yaşam durumları üzerinden dik koordinat sistemini çözümleyebilme", "surec": ["a) Belirler.", "b) Belirler."], "hook": "Sinemada koltuk bulma (satır, sütun) veya amiral battı oyunu.", "somut_materyal_onerisi": "Izgara panosu, koordinat düzlemi oyunu (Amiral Battı)."},
                {"kod": "MAT.8.2.2", "cikti": "Doğrusal ilişkileri doğrusal fonksiyonlarla temsil edebilme", "surec": ["a) Tanır.", "b) Belirler.", "c) Kullanır.", "ç) Değerlendirir.", "d) Karşılaştırır.", "e) Karar verir."], "hook": "Taksimetre açılış ücreti ve gidilen kilometreye göre artan fiyat grafiği.", "somut_materyal_onerisi": "Fiziksel rampa modelleri ile eğim ölçümü, Desmos Dinamik Grafik Çizici."},
                {"kod": "MAT.8.2.3", "cikti": "Dik koordinat sisteminde iki doğrusal fonksiyonun birbirine göre durumuna ilişkin çıkarım yapabilme", "surec": ["a) Oluşturur.", "b) Yapar.", "c) Karşılaştırır.", "ç) Sunar.", "d) Değerlendirir."], "hook": "İki farklı telefon operatörünün ücretlendirme grafiklerinin kesişimi (avantaj noktası).", "somut_materyal_onerisi": "Renkli iplerle grafik panosu (Geoboard)."},
                {"kod": "MAT.8.2.4", "cikti": "Doğrusal fonksiyonlara ilişkin problemlerin çözümlerini algoritma ifade yöntemlerini kullanarak yapılandırabilme", "surec": ["a) Açıklar.", "b) Oluşturur."], "hook": "Basit bir maliyet hesaplama yazılımı algoritması.", "somut_materyal_onerisi": "Fonksiyon makinesi kutusu (girdi-çıktı)."}
            ],
            "3. Tema: Geometrik Şekiller": [
                {"kod": "MAT.8.3.1", "cikti": "Matematiksel araç ve teknoloji yardımıyla üçgenin kenarları ve açıları arasındaki ilişkiyi yorumlayabilme", "surec": ["a) İnceleyer.", "b) Sıralar.", "c) İfade eder."], "hook": "Kapı menteşesinin açılması ile kapı ucunun mesafesinin artması ilişkisi.", "somut_materyal_onerisi": "Hareketli açı kolları (Mekano seti) ve lastik."},
                {"kod": "MAT.8.3.2", "cikti": "Matematiksel araç ve teknoloji yardımıyla üçgenin kenar uzunlukları arasındaki ilişkiye yönelik çıkarım yapabilme", "surec": ["a) Bulunur.", "b) Listeler.", "c) Karşılaştırır.", "ç) Sunar.", "d) Sunar."], "hook": "Rastgele seçilen üç çubuğun neden her zaman üçgen oluşturamayacağı.", "somut_materyal_onerisi": "Makarna veya çubuklarla (farklı uzunluklarda) üçgen yapma kiti."},
                {"kod": "MAT.8.3.3", "cikti": "Bir üçgene eş üçgen oluşturmak için üçgenle ilgili bilinmesi yeterli olan elemanlara dair çıkarım yapabilme", "surec": ["a) Bulunur.", "b) Oluşturur.", "c) Karşılaştırır.", "ç) Sunar.", "d) Değerlendirir."], "hook": "Matbaada basılan şablonların eşliği.", "somut_materyal_onerisi": "Aydınger kağıdı, dinamik geometri yazılımı (GeoGebra)."},
                {"kod": "MAT.8.3.4", "cikti": "Bir üçgene benzer üçgen oluşturmak için üçgenle ilgili bilinmesi yeterli olan elemanlara dair çıkarım yapabilme", "surec": ["a) Bulunur.", "b) Oluşturur.", "c) Karşılaştırır.", "ç) Sunar.", "d) Değerlendirir."], "hook": "Maket uçaklar veya harita ölçeklendirmesi.", "somut_materyal_onerisi": "Pantograf aracı, milimetrik kağıt üzerinde büyütme/küçültme."},
                {"kod": "MAT.8.3.5", "cikti": "Kenar uzunlukları a² + b² = c² eşitliğini sağlayan üçgenleri oluşturarak dik üçgen olduklarını; dik üçgenlerde dik kenar uzunluklarının kareleri toplamının hipotenüs uzunluğunun karesine eşit olduğunu yorumlayabilme", "surec": ["a) İnceleyer.", "b) Belirler.", "c) İfade eder."], "hook": "Duvara dayalı merdiven uzunluğu, kestirme yol hesaplaması.", "somut_materyal_onerisi": "Pisagor su çarkı, birim karelerden oluşan 3-4-5 puzzle takımı."},
                {"kod": "MAT.8.3.6", "cikti": "Üçgende açı-kenar ilişkisi, üçgen eşitsizliği ve Pisagor bağıntısını içeren problemleri çözebilme", "surec": ["a) Belirler.", "b) Belirler.", "c) Dönüştürür.", "ç) Açıklar.", "d) Geliştirir.", "e) Uygular.", "f) Değiştirir.", "g) Değerlendirir.", "ğ) Geneller.", "h) Değerlendirir."], "hook": "Mimari çatı eğimi hesaplamaları.", "somut_materyal_onerisi": "3D mimari model kitleri, gönye."}
            ],
            "4. Tema: Geometrik Nicelikler": [
                {"kod": "MAT.8.4.1", "cikti": "Dik prizmalar, silindir, piramit ve koni açınımlarını çözümleyebilme", "surec": ["a) Belirler.", "b) Belirler."], "hook": "Ambalaj ve hediye kutularının karton üretimi.", "somut_materyal_onerisi": "Mıknatıslı açınım setleri, kağıt prizma maketleri."},
                {"kod": "MAT.8.4.2", "cikti": "Dik dairesel silindirin yüzey açınımına ilişkin deneyimlerini dik dairesel silindirin yüzey alanına yansıtabilme", "surec": ["a) Gözden geçirir.", "b) Çıkarım yapar.", "c) Değerlendirir."], "hook": "Konserve kutusunun kağıt etiketi ve metal kapaklarının alanını bulma.", "somut_materyal_onerisi": "Konserve kutusu ve onu tam saran bir A4 kağıdı (soyutlama modeli)."},
                {"kod": "MAT.8.4.3", "cikti": "Dairenin alan bağıntısının oluşturulma sürecinden hareketle dik dairesel silindirin hacim bağıntısına yönelik analojik akıl yürütebilme", "surec": ["a) Gözden geçirir.", "b) Belirler.", "c) Çıkarım yapar."], "hook": "Bardağın alabileceği su miktarı, silindirik su deposu kapasitesi.", "somut_materyal_onerisi": "Üst üste dizilen CD'ler (alan-hacim analojisi), hacim sıvı aktarma kapları."}
            ],
            "5. Tema: Dönüşüm Geometrisi": [
                {"kod": "MAT.8.5.1", "cikti": "Dik koordinat sisteminde öteleme ve yansıma dönüşümlerini yapabilme", "surec": ["a) Koordinat değişimlerine dair kuralı bulur.", "b) Ardışık dönüşümler uygular."], "hook": "Oyun karakterinin eksenlere göre hareketi.", "somut_materyal_onerisi": "Koordinat düzlemi çizili manyetik tahta ve mıknatıslı çokgen şekilleri."}
            ],
            "6. Tema: İstatistik": [
                {"kod": "MAT.8.6.1", "cikti": "Farklı veri setlerini ve grafikleri karşılaştırıp karar verebilme", "surec": ["a) Veri toplar.", "b) Uygun grafiği seçip yayılım/merkez analizi yapar."], "hook": "İki şubenin deneme sınavı başarı analizi.", "somut_materyal_onerisi": "İki farklı hedefe atılan dart oklarının dağılım simülasyonu, histogram blokları."}
            ],
            "7. Tema: Olasılık": [
                {"kod": "MAT.8.7.1", "cikti": "Olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı seçebilme", "surec": ["a) Karara uygun bilgi toplar.", "b) Yaklaşımları kıyaslayıp uygun olanı kullanır."], "hook": "Penaltı atışında gol olma tahmini (deneysel/öznel) ile zar atışının (teorik) farkı.", "somut_materyal_onerisi": "Sporcu istatistik kartları, hileli/ağırlıklı zarlar."}
            ]
        }
    }
}
# ==========================================
# 6. UI AKIŞI (KURULUM, TELAFI MODU, 3D SINIF, DASHBOARD VE ÇIKIŞ BİLETİ)
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
        st.markdown('<div class="sade-kart"><div class="baslik-mavi">Öğretim Elemanı Rubriği & Yansıtma Notu</div>', unsafe_allow_html=True)
        hoca_rubrik = st.text_area(
            "Rubrik Kriterleri *",
            value="1. Kapsayıcı ve duyuşsal iletişim (20 Puan).\n2. Pedagojik eylem sırası (15 Puan).\n3. Profile ve kazanıma uygun materyal seçimi/kullanımı (25 Puan).\n4. 2024 TYMM keşif odaklı süreç uyumu (20 Puan).\n5. Öğrenme kanıtı (5 Puan)",
            height=100,
        )
        onceki_rapor = st.text_area(
            "Önceki Dersteki Hata/Hedefleriniz (Gelişim Takibi İçin):",
            placeholder="Örn: Bir önceki stajımda kriz anında öğrenciyi dinlemeden doğrudan tahtada kuralı vermiştim...",
            height=60,
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
            st.session_state.onceki_rapor = onceki_rapor.strip() if onceki_rapor else ""
            st.session_state.adim = 2
            st.rerun()

# ----------------- ADIM 2 -----------------
elif st.session_state.adim == 2:
    st.markdown('<span class="rozet">ADIM 2 / 3</span>', unsafe_allow_html=True)
    st.markdown(f"### 🏫 3D Canlı Sınıf | Aday: {st.session_state.ogretmen_adi} - {st.session_state.universite_adi}")

    # TELAFİ MODU SEÇENEĞİ
    st.markdown("<div class='sade-kart'><div class='baslik-mavi'>⚙️ Mod Seçimi</div>", unsafe_allow_html=True)
    telafi_modu = st.toggle("🤖 **Telafi Modu Aktif:** Yapay Zeka Kasten Sınamak İçin Rastgele Zorlu Senaryo (Sınıf, Kazanım ve Özel Profil) Üretsin")
    st.markdown("</div>", unsafe_allow_html=True)

    if telafi_modu:
        if st.session_state.telafi_senaryosu is None:
            # AI Rastgele Zorlu Senaryo Üretir
            r_sinif = random.choice(list(tyym_master_arsiv.keys()))
            r_tema = random.choice(tyym_master_arsiv[r_sinif]["Temalar"])
            r_kazanim_list = tyym_master_arsiv[r_sinif]["Kazanimlar"][r_tema]
            r_kazanim_obj = random.choice(r_kazanim_list)
            r_surec = random.choice(r_kazanim_obj["surec"])
            # Özel gereksinimli zorlu profillerden rastgele 2 tanesini seçer
            zorlu_profiller = ["Kerem", "Arda", "Elif", "Zeynep", "Ayşe", "Ali", "Mehmet"]
            r_ogrenciler = random.sample(zorlu_profiller, 2)
            
            st.session_state.telafi_senaryosu = {
                "sinif": r_sinif, "tema": r_tema, "kazanim_obj": r_kazanim_obj,
                "surec": r_surec, "secili_ogrenciler": r_ogrenciler
            }

        secilen_sinif = st.session_state.telafi_senaryosu["sinif"]
        secilen_tema = st.session_state.telafi_senaryosu["tema"]
        secilen_kazanim_obj = st.session_state.telafi_senaryosu["kazanim_obj"]
        secilen_surec = st.session_state.telafi_senaryosu["surec"]
        secili_liste = st.session_state.telafi_senaryosu["secili_ogrenciler"]

        st.info("🤖 **Yapay Zeka Telafi Modu devrede.** Bu modda kazanımı ve kriz yaşayacak öğrencileri sistem sizin için seçti. Lütfen doğrudan müdahale konsoluna geçiniz.")
        st.success(f"**Atanan Kazanım:** {secilen_kazanim_obj['kod']} - {secilen_kazanim_obj['cikti']}\n\n**Süreç Bileşeni:** {secilen_surec}\n\n**Bağlam:** {secilen_kazanim_obj['hook']}")

    else:
        st.session_state.telafi_senaryosu = None
        with st.expander("📚 2024 TYMM Detaylı Müfredat Seçimi (Manuel)", expanded=True):
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

        st.markdown('<div class="sade-kart"><div class="baslik-mavi">👥 Öğrenci Seçimi (Manuel) *</div>', unsafe_allow_html=True)
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
        dinamik_kriz = profil_ve_kazanima_ozel_kriz_uret(bilgi['durum'], secilen_kazanim_obj["cikti"], secilen_surec)
        davranis = ai_profil_davranisi_uret(ogr_ad, secilen_sinif, secilen_tema, secilen_kazanim_obj["kod"], secilen_kazanim_obj["cikti"], secilen_surec, dinamik_kriz)
        with kart_cols[idx % len(kart_cols)]:
            with st.container(border=True):
                st.markdown(f"**{ogr_ad} ({bilgi['durum']})**")
                st.caption(f"Mimik: {bilgi['mimik']}")
                st.write(davranis)

    dinamik_eylem_1_list, dinamik_eylem_2_list = dinamik_eylem_secenekleri_uret(secilen_tema, secilen_kazanim_obj["kod"], secilen_surec, dinamik_kriz)

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
                durum = ogrenci_profilleri[ogr_ad]["durum"]
                ai_tepkileri[ogr_ad] = ai_profil_tepkisi_uret(ogr_ad, durum, secilen_kazanim_obj["kod"], secilen_surec, eylem_1, eylem_2, materyal_etiketi)
                
            durumlar = [ogrenci_profilleri[o]["durum"] for o in secili_liste]
            
            ai_puan, ai_mesaj, alt_puanlar_dict = kapsamli_ai_degerlendirmesi(eylem_1, eylem_2, materyal_etiketi, mat_aciklama, sesli_girdi, durumlar, st.session_state.onceki_rapor, secilen_kazanim_obj, st.session_state.hoca_rubrik)

            st.session_state.simulasyon_gecmisi.append({
                "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sinif": secilen_sinif, "tema": secilen_tema, "kod": secilen_kazanim_obj["kod"], "cikti": secilen_kazanim_obj["cikti"],
                "surec": secilen_surec, "secili_ogrenciler": secili_liste, "eylem_1": eylem_1, "eylem_2": eylem_2,
                "materyal_etiketi": materyal_etiketi, "ozgun_tanitim": ozgun_tanitim, "mat_aciklama": mat_aciklama,
                "sesli_girdi": sesli_girdi, "ai_tepkileri": ai_tepkileri, "ai_puan": ai_puan, "ai_mesaj": ai_mesaj,
                "alt_puanlar": alt_puanlar_dict
            })
            st.session_state.telafi_senaryosu = None
            st.session_state.adim = 3
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- ADIM 3 -----------------
elif st.session_state.adim == 3:
    st.markdown('<span class="rozet">ADIM 3 / 3</span>', unsafe_allow_html=True)
    st.subheader("📊 2024 TYMM Kapsamlı Akademik Değerlendirme Raporu")
    
    son_kayit = st.session_state.simulasyon_gecmisi[-1]
    
    # 1. SEKME: ÖĞRENCİ TEPKİLERİ VE ADAYIN SEÇİMLERİ (TRANSKRİPT)
    st.markdown("### 1. Seçimlerinize Göre Öğrenci Tepkileri ve Krizin Son Durumu")
    kart_cols = st.columns(min(len(son_kayit["secili_ogrenciler"]), 3))
    idx = 0
    for ogr, tepki in son_kayit["ai_tepkileri"].items():
        with kart_cols[idx % len(kart_cols)]:
            with st.container(border=True):
                st.write(tepki)
        idx += 1

    st.divider()

    # 2. SEKME: YAPAY ZEKA DEĞERLENDİRME RAPORU VE GELİŞİM GRAFİĞİ
    tab_rapor, tab_gelisim, tab_hoca = st.tabs(["🤖 Yapay Zeka Analiz Raporu", "📈 Beceri Bazlı Gelişim Grafiği (Dashboard)", "👨‍🏫 Öğretim Elemanı Kararı"])
    
    with tab_rapor:
        st.markdown(f"<div class='anlik-bildirim'>{son_kayit['ai_mesaj']}</div>", unsafe_allow_html=True)
        ozg_metin = f"\n- **Özgün Materyal Tanıtımı:** {son_kayit['ozgun_tanitim']}" if son_kayit["ozgun_tanitim"] else ""
        
        transkript = (
            f"**Oturum Tarihi:** {son_kayit['tarih']} \n**Aday:** {st.session_state.ogretmen_adi} ({st.session_state.universite_adi})\n"
            f"**Kazanım:** {son_kayit['kod']} ({son_kayit['surec']})\n\n"
            f"**1. Eylem (Seçilen):** {son_kayit['eylem_1']}\n**2. Eylem (Seçilen):** {son_kayit['eylem_2']}\n"
            f"**Materyal:** {son_kayit['materyal_etiketi']}{ozg_metin}\n"
            f"**Kullanım Açıklaması:** {son_kayit['mat_aciklama']}\n**Adayın Sözel Hitabeti:** {son_kayit['sesli_girdi']}\n"
        )
        st.markdown("#### 📝 Sisteme Kayıtlı Ders Transkripti Özeti")
        st.markdown(f"<div class='transkript-kutu'>{transkript}</div>", unsafe_allow_html=True)
        
        st.download_button(
            label="⬇️ Yazılı Ders Transkripti ve AI Akademik Raporunu İndir (.txt)",
            data=(son_kayit['ai_mesaj'] + "\n\n=== DERS TRANSKRİPTİ ===\n\n" + transkript).replace("**", "").replace("*", "").replace("`", "").replace("<br>", "\n").replace("<b>", "").replace("</b>", "").replace("<span class='hata-metni'>", "").replace("<span class='oneri-metni'>", "").replace("</span>", ""),
            file_name=f"2024_TYMM_Transkript_Rapor_{st.session_state.get('okul_numarasi', 'aday')}.txt",
            mime="text/plain",
        )

    with tab_gelisim:
        st.markdown("#### 📈 Denemeler Arası Beceri Gelişimi")
        st.info("Bu grafik, oturum boyunca yaptığınız tüm simülasyon denemelerinde (Telafi dahil) hangi pedagojik beceride ne kadar ilerlediğinizi gösterir.")
        
        if len(st.session_state.simulasyon_gecmisi) > 0:
            df_puanlar = pd.DataFrame([k["alt_puanlar"] for k in st.session_state.simulasyon_gecmisi])
            df_puanlar.index = [f"Deneme {i+1}" for i in range(len(df_puanlar))]
            st.line_chart(df_puanlar)
        else:
            st.write("Yeterli veri bulunmamaktadır.")

    with tab_hoca:
        st.markdown("### Danışman Öğretim Elemanı Geri Dönütü")
        hoca_notu = st.text_area("Yapay zeka analiz raporunu ve adayın seçimlerini göz önünde bulundurarak resmî geri dönütünüzü yazın *", height=150)
        if st.button("📤 Dönütü Sisteme Kaydet", type="primary"):
            if hoca_notu.strip(): st.success("✅ Öğretim elemanı akademik geri dönütü başarıyla sisteme kaydedildi.")
            else: st.error("❌ Geri dönüt alanı boş bırakılamaz.")
                
    st.divider()

    # ÇIKIŞ BİLETİ (ZORUNLU YANSITMA)
    st.markdown('<div class="sade-kart"><div class="baslik-mavi">🎫 Bilişsel Çıkış Bileti (Zorunlu Yansıtma)</div>', unsafe_allow_html=True)
    st.warning("⚠️ Ezber/deneme-yanılma (Trial-and-Error) yöntemini önlemek amacıyla doğrudan yeni simülasyona geçemezsiniz. Lütfen yukarıdaki raporda tespit edilen hatalarınızdan ne öğrendiğinizi kısaca ifade ediniz.")
    
    cikis_bileti = st.text_area("Bu kriz senaryosundaki hatalarımdan şunu öğrendim ve bir sonraki derste şunu farklı yapacağım:", height=80)
    if st.button("🔄 Yansıtmayı Kaydet ve Yeni Simülasyon Başlat"):
        if not cikis_bileti.strip() or len(cikis_bileti.strip()) < 15:
            st.error("❌ Lütfen hatalarınızdan ne öğrendiğinizi anlamlı bir şekilde (en az 15 karakter) ifade ediniz.")
        else:
            # Sadece eski raporu bu çıkış bileti ile güncelleyip 1. Adıma dönüyoruz.
            st.session_state.onceki_rapor = cikis_bileti.strip()
            st.session_state.secili_ogrenciler = []
            st.session_state.otur_seed = random.randint(1, 1000)
            st.session_state.adim = 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
