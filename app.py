import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TYMM 2026 Tam Müfredat & Rubrik Uyumlu Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
    st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
    st.session_state.adim = 1

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) MASTER ARŞİVİ (5-8)
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı sayılara genelleyebilme",
                    "surec": [
                        "a) Günlük hayattaki bağlamlardan yola çıkarak bilgi toplar.",
                        "b) Sayıların bölümleri ile okunuşları arasındaki ortak özellikleri belirler.",
                        "ç) Örüntüler üzerinden önermelerde bulunur."
                    ],
                    "hook": "Millî Kütüphane'deki 405.020 adet tarihi el yazması kitabın arşiv kodlama sistemi.",
                    "kriz": "Disleksili Kerem tahtada büyük sayıları okurken rakamları ters görür, sınıfta alay başlar."
                },
                {
                    "kod": "MAT.5.1.2",
                    "cikti": "Doğal sayılarla toplama ve çıkarma işlemlerini stratejiler geliştirerek yapabilme",
                    "surec": [
                        "a) İşlem gerektiren günlük yaşam durumlarını inceler.",
                        "b) Zihinden işlem yapma stratejileri geliştirir."
                    ],
                    "hook": "Süpermarket kasasında hızlı para üstü hesaplama.",
                    "kriz": "Öğrenci 'alt alta yazmadan zihinden nasıl yapalım, kafam karıştı' diye isyan eder."
                },
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.5.2.1",
                    "cikti": "Temel geometrik elemanları (nokta, doğru, ışın) modelleyebilme",
                    "surec": [
                        "a) Çevresindeki nesnelerde geometrik formları fark eder.",
                        "b) Nokta, doğru ve ışın kavramlarını somut modellerle temsil eder."
                    ],
                    "hook": "Şehir haritalarındaki cadde ve sokak kesişimleri.",
                    "kriz": "Otizmli Arda tahtaya çizilen çizgilerin kalınlığından rahatsız olup tepki gösterir."
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.5.3.1",
                    "cikti": "Basit kesirlerde anlam oluşturma ve aralarındaki büyüklük ilişkisini kurabilme",
                    "surec": [
                        "a) Bütün, yarım ve çeyrek kavramlarını günlük bağlamlarda yorumlar.",
                        "b) Kesir modelleri oluşturur."
                    ],
                    "hook": "Pizza dilimleme ve paylaşım stratejileri.",
                    "kriz": "Kaygılı Elif 'hocam payda büyüdükçe sayı niye küçülüyor, mantığım almıyor' diye ağlamaya başlar."
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.5.4.1",
                    "cikti": "İstatistiksel bir araştırma için soru oluşturma ve veri toplayabilme",
                    "surec": [
                        "a) Araştırma gerektiren problemleri ve soruları belirler.",
                        "b) Uygun veri toplama araçları seçer."
                    ],
                    "hook": "Sınıfın en çok sevdiği spor dalları anketi.",
                    "kriz": "Üstün yetenekli Can 'bu anket taraflı, sorular yönlendirici' diye tartışma çıkarır."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.5.1",
                    "cikti": "Basit olayların olası durumlarını belirleyebilme",
                    "surec": [
                        "a) Günlük hayattaki olayların sonuçlarını tahmin eder.",
                        "b) Kesin, imkansız ve olası durumları örneklerle açıklar."
                    ],
                    "hook": "Hava durumu raporlarındaki yağmur yağma ihtimali.",
                    "kriz": "Öğrenci 'yarın kesin kar yağacak, okul tatil olacak' diye iddiaya girer."
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1",
                    "cikti": "Doğal sayının çarpan ve katlarına yönelik muhakeme yapabilme",
                    "surec": [
                        "a) Çarpan ve katlarına yönelik varsayımlarda bulunur.",
                        "b) Örnek durumların ilişkilerini inceleyerek genellemeleri belirler."
                    ],
                    "hook": "Otobüs duraklarında iki farklı hattın aynı anda hareket etme saatleri.",
                    "kriz": "Öğrenci 'bu kuralları ezberlemek zorunda mıyız, manavda EKOK mu hesaplayacağız?' diye isyan eder."
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.6.2.1",
                    "cikti": "Üçgen ve paralelkenarın alan bağıntılarını kurabilme",
                    "surec": [
                        "a) Alan ölçme birimleri arasındaki ilişkileri inceler.",
                        "b) Üçgenin alan bağıntısını oluşturur."
                    ],
                    "hook": "Tarım arazilerinin parselasyon ve alan hesabı.",
                    "kriz": "Öğrenci formülü unuttuğunu söyleyip tahtada kilitlenip kalır."
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.6.3.1",
                    "cikti": "Oran kavramını anlamlandırabilme ve yorumlayabilme",
                    "surec": [
                        "a) İki çokluğun birbirine oranını günlük yaşam durumlarıyla ilişkilendirir."
                    ],
                    "hook": "Kek tarifindeki un ve şeker oranları.",
                    "kriz": "Öğrenci oran ile kesir arasındaki fark tam olarak nedir? diye sorar."
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.6.4.1",
                    "cikti": "Aritmetik ortalama ve açıklığı hesaplayıp yorumlayabilme",
                    "surec": [
                        "a) Veri gruplarının merkezî eğilim ölçülerini inceler."
                    ],
                    "hook": "Basketbolcunun maçlarda attığı sayıların ortalaması.",
                    "kriz": "Öğrenci açıklığın verideki uç değerlerden nasıl etkilendiğini anlamakta zorlanır."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.5.1",
                    "cikti": "Bir olayın olasılığını gözleme dayalı tahmin edebilme",
                    "surec": [
                        "a) Olasılık ile deney verisini ilişkilendirir."
                    ],
                    "hook": "Madeni para atma deneylerinde 100 atıştaki değişim.",
                    "kriz": "Öğrenci 'ben 10 kez attım hepsi yazı geldi, teoriniz yanlış' diye isyan eder."
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.1",
                    "cikti": "Rasyonel sayılarla işlemler içeren gerçek yaşam problemlerini çözebilme",
                    "surec": [
                        "a) Sayı ve işlem bileşenlerini belirler.",
                        "b) Stratejiler oluşturup çözer."
                    ],
                    "hook": "Banka kredi faiz kesintileri ve bütçe planlaması.",
                    "kriz": "Negatif rasyonel sayılarda bölme hatası yapan öğrenci masaya vurur."
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.7.2.1",
                    "cikti": "Çember ve dairede açı ve alan bağıntıları kurabilme",
                    "surec": ["a) Çemberin çevre uzunluğu ile çapı arasındaki oran."],
                    "hook": "Pizza dilimlerinin merkez açı hesabı.",
                    "kriz": "Öğrenci pi sayısının nereden geldiğini sorgulayıp derse odaklanmaz."
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.7.3.1",
                    "cikti": "Orantı problemlerini çözebilme ve doğru/ters orantıyı ayırt edebilme",
                    "surec": ["a) Doğru ve ters orantılı nicelikleri fark eder."],
                    "hook": "Musluğun havuzu doldurma süreleri.",
                    "kriz": "Öğrenci ters orantıda neden çarpım yapıldığını anlamaz."
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.4.1",
                    "cikti": "Verileri temsil etmek için uygun grafikleri seçip yorumlayabilme",
                    "surec": ["a) Daire ve çubuk grafiklerini oluşturur."],
                    "hook": "Okul kantini günlük ürün satış grafikleri.",
                    "kriz": "Öğrenci daire grafiğinde açı oranlamasını yaparken hata yapar."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.7.5.1",
                    "cikti": "Bir olayın olma olasılığını hesaplayabilme",
                    "surec": ["a) İstenen durum / tüm olası durumlar oranı."],
                    "hook": "Çekiliş torbalarından top çekme oyunları.",
                    "kriz": "Öğrenci olasılığın kesinlik bildirmediğini görünce şaşırır."
                }
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler",
            "3. Tema: Nicelikler Arasındaki İlişkiler",
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma",
            "5. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.1",
                    "cikti": "Kareköklü ifadeler ile ilgili muhakeme yapabilme",
                    "surec": ["a) Karenin alanı ile kenar uzunluğu ilişkisini belirler."],
                    "hook": "Alanı 50 metrekare olan kare şeklindeki stüdyo dairenin parke hesabı.",
                    "kriz": "Otizmli Arda köklü ifade sesinden rahatsız olup kulaklarını kapatır."
                }
            ],
            "2. Tema: Geometrik Şekiller ve Uzamsal İlişkiler": [
                {
                    "kod": "MAT.8.2.1",
                    "cikti": "Geometrik cisimlerin (silindir, piramit) yüzey alanı ve hacim bağıntıları",
                    "surec": ["a) Silindirin açınımı ve yüzey alanı."],
                    "hook": "Willy Wonka çikolata fabrikası silindir kutu tasarımı.",
                    "kriz": "Öğrenci formülleri ezberlemek istemediğini söyler."
                }
            ],
            "3. Tema: Nicelikler Arasındaki İlişkiler": [
                {
                    "kod": "MAT.8.3.1",
                    "cikti": "Doğrusal denklemler kurabilme ve grafiklerini çizebilme",
                    "surec": ["a) Bağımlı ve bağımsız değişkenleri belirler."],
                    "hook": "Taksi açılış ve kilometre başına ücret tarifesi.",
                    "kriz": "Öğrenci grafikteki eğim açısının ne anlama geldiğini anlamaz."
                }
            ],
            "4. Tema: Veriye Dayalı İstatistiksel Araştırma": [
                {
                    "kod": "MAT.8.4.1",
                    "cikti": "En çok iki kategorik değişken içeren verileri inceleyebilme",
                    "surec": ["a) İki yönlü sıklık tablolarını yorumlar."],
                    "hook": "LGS tercih istatistikleri ve meslek tercihleri.",
                    "kriz": "Kaygılı öğrenci tabloların karmaşık olduğunu söyleyip panikler."
                }
            ],
            "5. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.5.1",
                    "cikti": "Olasılık yaklaşımlarından (öznel, deneysel, teorik) uygun olanı belirleme",
                    "surec": ["a) Karar vermeye yönelik amaç belirler."],
                    "hook": "Futbol teknik direktörlerinin penaltı stratejisi.",
                    "kriz": "Üstün yetenekli Can 'her şey teorik olasılıkla ölçülemez' diye tartışma çıkarır."
                }
            ],
        },
    }
}

# ==========================================
# 2. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
    st.info("ℹ️ Lütfen aşağıdaki adımları sırasıyla takip ederek oturum parametrelerini belirleyin.")
    
    col1, col2 = st.columns(2)
    with col1:
        ogretmen_adi = st.text_input("Öğretmen Adayı Adı Soyadı *", placeholder="Zorunlu Alan")
        okul_numarasi = st.text_input("Okul Numarası *", placeholder="Zorunlu Alan")
        universite_adi = st.text_input("Üniversite Adı *", placeholder="Zorunlu Alan")
        fakulte_bolum = st.text_input("Fakülte ve Bölüm", value="Eğitim Fakültesi - İlköğretim Matematik")
        uygulama_ogretim_elemani = st.text_input("Danışman Hoca *", placeholder="Zorunlu Alan")

    with col2:
        st.markdown("##### 📋 Değerlendirme Rubriği")
        rubrik_metni = st.text_area(
            "Hocanın Rubrik Kriterlerini Buraya Yapıştırın",
            value=(
                "1. 3D sınıf ortamında sesli kriz yönetimi (30 Puan).\n"
                "2. Kapsayıcı hitabet (30 Puan).\n"
                "3. 2026 Maarif Modeli süreç bileşenleri uyumu (20 Puan).\n"
                "4. Sahada aksiyon alma başarısı (20 Puan)."
            ),
            height=130,
        )

    if st.button("🚀 3D Sınıfa Geçiş Yap", type="primary"):
        if not all([ogretmen_adi, okul_numarasi, universite_adi, uygulama_ogretim_elemani]):
            st.error("❌ İlerlemek için lütfen tüm zorunlu alanları (*) eksiksiz doldurun.")
        else:
            st.session_state.ogretmen_adi = ogretmen_adi
            st.session_state.okul_numarasi = okul_numarasi
            st.session_state.universite_adi = universite_adi
            st.session_state.uygulama_ogretim_elemani = uygulama_ogretim_elemani
            st.session_state.rubrik_metni = rubrik_metni
            st.session_state.adim = 2
            st.rerun()
            # ==========================================
# 3. ADIM 2: 3D GÖRSEL SINIF VE SESLİ GERİ BİLDİRİM MOTORU
# ==========================================
elif st.session_state.adim == 2:
    st.info("ℹ️ Sınıf düzeyini ve ilgili öğretim kazanımlarını belirleyerek kriz senaryosunu başlatın.")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        secilen_sinif = st.selectbox("1️⃣ Sınıf Düzeyi", list(tyym_master_arsiv.keys()))
    with col_s2:
        secilen_tema = st.selectbox("2️⃣ Tema Seçin", tyym_master_arsiv[secilen_sinif]["Temalar"])
    
    kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"].get(secilen_tema, [])
    
    if kazanim_listesi:
        with col_s3:
            kazanim_secenekleri = [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
            secilen_kazanim_str = st.selectbox("3️⃣ Kazanım Seçin", kazanim_secenekleri)
            
        secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str)
        secilen_surec = st.selectbox("4️⃣ Odaklanılacak Süreç Bileşeni:", secilen_kazanim_obj["surec"])
        
        st.info(f"💡 **2026 Maarif Modeli Yaşam Kancası:** {secilen_kazanim_obj['hook']}")
        
        # KRİZ DURUMU (Sarı Uyarı)
        aktif_kriz = secilen_kazanim_obj["kriz"]
        st.warning(f"⚠️ **KRİZ DURUMU:** {aktif_kriz}")

        # 3D İZOMETRİK SINIF VE AVATARLAR (Emojili)
        st.markdown("---")
        st.markdown("#### 🌐 Aktif Öğrenci Avatarları")
        
        col_av1, col_av2, col_av3, col_av4 = st.columns(4)
        with col_av1:
            st.info("👦 😟 **Kerem**\n\n*Durum: Disleksili*\n\nMimik: Alnını ovuşturuyor")
        with col_av2:
            st.info("👦 🎧 **Arda**\n\n*Durum: Otizm Spektrumlu*\n\nMimik: Sallanıyor")
        with col_av3:
            st.info("👦 🙋‍♂️ **Can**\n\n*Durum: Üstün Yetenekli*\n\nMimik: Sabırsız")
        with col_av4:
            st.info("👧 😔 **Elif**\n\n*Durum: Yüksek Kaygılı*\n\nMimik: Başını öne eğmiş")

        st.markdown("---")
        col_sol, col_sag = st.columns([1, 1], gap="large")
        with col_sol:
            st.markdown("#### 🎙️ Kriz Karar ve Sesli Hitabet Konsolu")
            sesli_secenek = st.selectbox(
                "🎤 Hazır Sesli Hitabet Komutu Seçin:",
                [
                    "Sakin ol Kerem, rakamların yeri değişse de değerini birlikte bulacağız...",
                    "Harika bir soru Arda, kulaklığını rahatça kullanabilirsin...",
                    "Haklısın Can, teorik olasılığın yanına öznel bakış açını da ekleyelim!",
                    "Elif derin bir nefes al, formülü birlikte adım adım çözeceğiz."
                ],
            )
            sesli_girdi_manuel = st.text_input("⌨️ Veya Kendi Sesli Hitabet Metninizi Yazın", placeholder="Örn: 'Sakin ol, birlikte aşacağız...'")

            ogretmen_karari = st.radio(
                "👩‍🏫 Pedagojik Aksiyonu Seçin:",
                [
                    "A) Disiplin kurallarıyla dersi bölmeden devam etmek.",
                    "B) Ses tonunu yumuşatarak güvenli alan sunmak, somut materyalle desteklemek.",
                    "C) Durumu görmezden gelmek.",
                    "D) Sınıf genelinde akran destekli tartışma ortamı açarak kavramsal değişimi tetiklemek."
                ],
            )

            if st.button("📥 Staj Kararını Kaydet & Raporlamaya Geç", type="primary"):
                kayit_metni = sesli_girdi_manuel if sesli_girdi_manuel else sesli_secenek
                st.session_state.simulasyon_gecmisi.append({
                    "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "sinif": secilen_sinif,
                    "tema": secilen_tema,
                    "kod": secilen_kazanim_obj["kod"],
                    "kriz": aktif_kriz,
                    "karar": ogretmen_karari,
                    "sesli_komut": kayit_metni,
                })
                st.session_state.adim = 3
                st.rerun()
                
        with col_sag:
            st.info("ℹ️ Kararınızı kaydettikten sonra sistem pedagojik analizinizi sağdaki sekmede detaylı raporlayacaktır.")
    else:
        st.error("Bu tema altında henüz bir kazanım bulunmamaktadır.")

# ==========================================
# 4. ADIM 3: DİJİTAL REPLAY VE RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
    st.subheader("📊 2026 Maarif Modeli Çok Katmanlı Simülasyon Raporu")
    
    tab_aday, tab_fakulte, tab_ogretim = st.tabs([
        "👩‍🏫 Öğretmen Adayı Gelişim & Replay",
        "🏛️ Kurumsal Aksiyon Raporu",
        "👨‍🏫 Danışman Hoca Rubrik Matrisi",
    ])

    son_kayit = st.session_state.simulasyon_gecmisi[-1]

    with tab_aday:
        st.info("🔄 **Dijital Oturum Replay Paneli**")
        st.markdown(f"**Oturum:** #{random.randint(1000, 9999)} | **Sınıf:** {son_kayit['sinif']} | **Kazanım:** `{son_kayit['kod']}`")
        st.markdown(f"**Kriz:** {son_kayit['kriz']}")
        st.markdown(f"**Adayın Sesli Yanıtı:** *\"{son_kayit['sesli_komut']}\"*")
        
        if "B)" in son_kayit["karar"] or "D)" in son_kayit["karar"]:
            st.success("🌟 **Mükemmel Maarif Uyumu:** Seçilen kapsayıcı yaklaşım 2026 felsefesiyle birebir örtüşüyor.")
        else:
            st.error("❌ **Rubrik Uyarısı:** Geleneksel/Sert yaklaşım kapsayıcı eğitim ilkelerini ihlal etmektedir.")
        
        st.markdown("---")
        st.markdown("#### 📝 Aday Öz-Değerlendirme Modülü")
        aday_geri_bildirimi = st.text_area("Bu simülasyonun pedagojik kriz yönetimine katkısını değerlendirin:")
        if st.button("📤 Geri Bildirimi Kaydet"):
            if aday_geri_bildirimi:
                st.success("✅ Yansıtma notunuz portfolyoya eklendi.")
            else:
                st.error("❌ Lütfen metin alanını doldurun.")

        chart_data = pd.DataFrame({
            "Kriterler": ["Kriz Yönetimi", "Kapsayıcı Eğitim", "Süreç Uyumu", "Saha Aksiyonu"],
            "Puan": [95, 90, 85, 92]
        })
        st.bar_chart(chart_data, x="Kriterler", y="Puan")

    with tab_fakulte:
        st.markdown("### 🏛️ Eğitim Fakültesi Dekanlık Kararı")
        st.info(f"**Aday:** {st.session_state.get('ogretmen_adi', 'N/A')} | **Okul No:** {st.session_state.get('okul_numarasi', 'N/A')}")
        st.markdown(
            "1. **Maarif Uyumu:** Aday teorik bilgiyi sahaya aktarabileceğini kanıtlamıştır.\n"
            "2. **Değerlendirme:** Yüklenen rubrikle yüksek başarı sergilenmiştir.\n"
            "3. **Karar:** Gerçek okul stajına çıkması **UYGUN BULUNMUŞTUR**."
        )

    with tab_ogretim:
        st.markdown("### 👨‍🏫 Uygulama Öğretim Elemanı Geri Dönütü")
        st.info(f"**Yüklenen Rubrik:**\n{st.session_state.get('rubrik_metni', 'N/A')}")
        hoca_notu = st.text_area("Danışman Hoca Geri Dönütü:", placeholder="Örn: Sesli hitabeti oldukça kapsayıcıydı...")
        if st.button("📤 Dönütü Onayla"):
            st.success("✅ Onaylandı.")

    st.markdown("---")
    if st.button("🔄 Yeni Bir Simülasyon Başlat", type="primary"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.adim = 1
        st.rerun()
