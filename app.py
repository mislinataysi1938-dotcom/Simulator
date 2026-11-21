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
# ==========================================
# 6. ADIM 2: 3D SINIF, ÖĞRENCİ SEÇİMİ VE PEDAGOJİK MÜDAHALE
# ==========================================
elif st.session_state.adim == 2:
    st.info("2️⃣ 3D Canlı Sınıf ve Kriz Müdahalesi: Kazanım seçin, öğrenci belirleyin ve pedagojik eylem sıranızı oluşturun.")
    
    with st.expander("📚 Müfredat ve Kazanım Belirleme (Tıklayıp Açınız)", expanded=True):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            secilen_sinif = st.selectbox("Sınıf Düzeyi", list(tyym_master_arsiv.keys()))
        with col_s2:
            secilen_tema = st.selectbox("Tema", tyym_master_arsiv[secilen_sinif]["Temalar"])
        
        kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"].get(secilen_tema, [])
        if kazanim_listesi:
            with col_s3:
                kazanim_secenekleri = [f"{k['kod']}: {k['cikti']}" for k in kazanim_listesi]
                secilen_kazanim_str = st.selectbox("Kazanım Çıktısı", kazanim_secenekleri)
            
            secilen_kazanim_obj = next(k for k in kazanim_listesi if f"{k['kod']}: {k['cikti']}" == secilen_kazanim_str)
            secilen_surec = st.selectbox("Odaklanılacak Süreç Bileşeni:", secilen_kazanim_obj["surec"])
        else:
            st.error("Bu tema için kazanım bulunamadı.")
            st.stop()

    st.markdown("---")
    st.markdown("#### 👥 Sınıftaki Öğrenciler (Müdahale Edeceğiniz Öğrenciyi Seçin)")
    ogrenci_isimleri = list(ogrenciler.keys())
    sekmeler = st.tabs(ogrenci_isimleri)
    secilen_ogrenci_adi = ogrenci_isimleri[0] 
    
    for i, sekme in enumerate(sekmeler):
        with sekme:
            ogr = ogrenciler[ogrenci_isimleri[i]]
            st.markdown(f"**{ogr['ikon']} {ogrenci_isimleri[i]}** - *{ogr['durum']}*")
            st.write(ogr['ozellik'])
            if st.button(f"Sınıfta {ogrenci_isimleri[i]}'i Seç", key=f"btn_{i}"):
                secilen_ogrenci_adi = ogrenci_isimleri[i]
                
    aktif_ogrenci = ogrenciler[secilen_ogrenci_adi]
    dinamik_kriz_metni = f"**{secilen_ogrenci_adi} ({aktif_ogrenci['durum']}):** Öğrenci {aktif_ogrenci['ozellik'].lower()} kaynaklı olarak zorlanmaktadır. Yaşanan Kriz: {secilen_kazanim_obj['kriz']}"

    col_kriz, col_mudahale = st.columns([1, 1.5])
    
    with col_kriz:
        st.warning(f"⚠️ **KRİZ ANI GERÇEKLEŞTİ!**\n\n{dinamik_kriz_metni}")
        st.markdown(f"<div style='text-align:center; font-size:4rem;'>{aktif_ogrenci['ikon']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'><b>{secilen_ogrenci_adi}</b><br><i>Mimik: {aktif_ogrenci['mimik']}</i></div>", unsafe_allow_html=True)

    with col_mudahale:
        st.markdown("##### 🛠️ Pedagojik Eylem Sırası")
        eylem_1 = st.selectbox("1. Adım (İlk Müdahaleniz Ne Olacak?)*", ["Seçiniz...", "Öğrencinin duygusunu kabul edip güvenli alan sunmak (Empati kurmak)", "Sınıf kurallarını hatırlatıp sessiz olmasını istemek", "Durumu görmezden gelip derse devam etmek"])
        eylem_2 = st.selectbox("2. Adım (Akademik Yönlendirmeniz Ne Olacak?)*", ["Seçiniz...", "Doğrudan kuralı/formülü tahtaya yazıp ezberletmek", "Somut materyal üzerinden yönlendirici sorularla keşfettirmek", "Soruyu geçip başka bir konuya odaklanmak"])
        
        st.markdown("##### 🎙️ İletişim (Sadece Kendi Cümleleriniz)")
        sesli_veri = None
        try:
             sesli_veri = st.audio_input("🎤 Sesli Yanıtınızı Kaydedin")
        except AttributeError:
             pass
        yazili_mudahale = st.text_area("✍️ Veya Öğrenciye Ne Söyleyeceğinizi Birebir Yazın *", placeholder="Örn: Derin bir nefes al bakalım...")
        
        st.markdown("##### 🧩 Materyal Kullanımı")
        materyal_kullanimi = st.text_area("Hangi materyali, nasıl bir yönergeyle kullanacaksınız? *", placeholder="Örn: Onluk taban bloklarını masaya koyacağım...")

        if st.button("📥 Müdahaleyi Kaydet & Değerlendirmeye Geç", type="primary", use_container_width=True):
            if not (sesli_veri or yazili_mudahale) or not materyal_kullanimi or eylem_1 == "Seçiniz..." or eylem_2 == "Seçiniz...":
                st.error("❌ Lütfen sesli/yazılı hitabetinizi, eylem sıranızı ve materyal planınızı eksiksiz doldurunuz.")
            else:
                mudahale_ozeti = yazili_mudahale if yazili_mudahale else "Sesli kayıt sisteme işlendi."
                ai_tepki = ai_ogrenci_tepkisi(secilen_tema, secilen_kazanim_obj['cikti'], secilen_surec, secilen_ogrenci_adi, aktif_ogrenci["durum"], eylem_1, eylem_2, mudahale_ozeti)
                hata_donutu = pedagojik_geri_donut_uret(eylem_1, eylem_2)

                st.session_state.simulasyon_gecmisi.append({
                    "sinif": secilen_sinif, "tema": secilen_tema, "kazanim": secilen_kazanim_obj['kod'], "surec": secilen_surec,
                    "ogrenci": secilen_ogrenci_adi, "ogrenci_durum": aktif_ogrenci['durum'], "kriz": dinamik_kriz_metni,
                    "eylem_1": eylem_1, "eylem_2": eylem_2, "mudahale_metni": mudahale_ozeti, "materyal_plan": materyal_kullanimi,
                    "ogrenci_tepkisi": ai_tepki, "geri_donut": hata_donutu
                })
                st.session_state.adim = 3
                st.rerun()

# ==========================================
# 7. ADIM 3: DİJİTAL REPLAY VE AKADEMİK GERİ DÖNÜT
# ==========================================
elif st.session_state.adim == 3:
    st.info("3️⃣ Raporlama Paneli: Oturum tamamlandı. Aşağıdan hatalarınızı inceleyebilir ve hoca değerlendirmesine geçebilirsiniz.")
    st.markdown(f"**Aday:** {st.session_state.ogretmen_adi} | **No:** {st.session_state.okul_numarasi}")
    st.divider()

    tab_rapor, tab_degerlendirme = st.tabs(["📄 Oturum Özeti ve Hata Dönütleri", "👨‍🏫 Öğretim Elemanı Paneli"])
    son_oturum = st.session_state.simulasyon_gecmisi[-1]
    
    with tab_rapor:
        with st.container(border=True):
            st.markdown("#### ⚙️ Eğitim Sistemi Geri Dönütü (Hata Analizi)")
            if "Tebrikler" in son_oturum["geri_donut"]:
                st.success(son_oturum["geri_donut"])
            else:
                st.error(son_oturum["geri_donut"])
                
            st.divider()
            st.markdown("#### 🤖 Öğrencinin (Yapay Zeka) Tepkisi")
            if "Tebrikler" in son_oturum["geri_donut"]:
                st.success(f"**{son_oturum['ogrenci']}:** {son_oturum['ogrenci_tepkisi']}")
            else:
                st.error(f"**{son_oturum['ogrenci']}:** {son_oturum['ogrenci_tepkisi']}")

            st.divider()
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.write(f"- **Kazanım:** {son_oturum['kazanim']}")
                st.write(f"- **1. Adım:** {son_oturum['eylem_1']}")
                st.write(f"- **2. Adım:** {son_oturum['eylem_2']}")
            with col_r2:
                st.info(f"**İletişim:** {son_oturum['mudahale_metni']}")
                st.info(f"**Materyal:** {son_oturum['materyal_plan']}")

    with tab_degerlendirme:
        with st.container(border=True):
            st.markdown(f"### 👨‍🏫 Sayın {st.session_state.hoca_adi},")
            st.write("Adayın pedagojik eylem sırasını, materyal planını ve sistemin hata analizini inceleyerek geri dönütünüzü yazınız.")
            st.warning(f"**Rubrik Kriterleriniz:**\n\n{st.session_state.rubrik}")
            
            hoca_donutu = st.text_area("Değerlendirme Notunuz:", height=150)
            
            if st.button("📤 Geri Dönütü Adaya İlet ve Oturumu Kapat", type="primary"):
                if hoca_donutu:
                    st.success("✅ Öğretim elemanı değerlendirmesi aday portfolyosuna başarıyla eklendi.")
                    st.balloons()
                else:
                    st.error("❌ Lütfen değerlendirme notunuzu yazınız.")

    st.markdown("---")
    if st.button("🔄 Yeni Bir Simülasyon Başlat"):
        st.session_state.simulasyon_gecmisi = []
        st.session_state.adim = 1
        st.rerun()
