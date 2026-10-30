import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title=(
        "TYMM 2026 Resmî Müfredat & Rubrik Uyumlu 3D Sesli Staj Simülatörü"
    ),
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) ESNEK MASTER ARŞİVİ (5-8)
# ==========================================
tyym_master_arsiv = {
    "5. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "6. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.5.1.1",
                    "cikti": (
                        "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı"
                        " sayılara genelleyebilme"
                    ),
                    "surec": [
                        (
                            "a) Günlük hayattaki bağlamlardan yola çıkarak çok"
                            " basamaklı sayılar hakkında bilgi toplar."
                        ),
                        (
                            "b) Sayıların bölümleri ile okunuşları arasındaki"
                            " ortak özellikleri belirler."
                        ),
                        (
                            "c) Sayıların bölümleri ile okunuşları arasındaki"
                            " farklılıkları belirler."
                        ),
                        (
                            "ç) Örüntüler üzerinden basamak sayısı çok olan"
                            " sayıların okunuş/yazılışları hakkında önermelerde"
                            " bulunur."
                        ),
                    ],
                    "hook": (
                        "Millî Kütüphane'deki 405.020 adet tarihi el yazması"
                        " kitabın arşiv kodlama sistemi."
                    ),
                    "kriz": (
                        "Disleksili Kerem tahtada büyük sayıları okurken"
                        " rakamları ters görür, sınıfta alay başlar."
                    ),
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.5.6.1",
                    "cikti": (
                        "Herhangi bir olayın olasılığının 0 ile 1 arasında"
                        " olduğunu yorumlayabilme"
                    ),
                    "surec": [
                        "a) Olayları ve olası durumları inceler.",
                        (
                            "b) Olasılığa dair tahminlerini farklı sayı"
                            " temsillerine dönüştürür."
                        ),
                        (
                            "c) 0 ile 1 arasında olduğunu kendi ifadeleriyle"
                            " açıklar."
                        ),
                    ],
                    "hook": (
                        "Hava durumu raporlarındaki yağmur yağma yüzdesi tahmin"
                        " grafikleri."
                    ),
                    "kriz": (
                        "Öğrenci 'Hocam kesin kar yağacak, okul tatil olacak,"
                        " olasılık %100' diye iddiaya girer."
                    ),
                }
            ],
        },
    },
    "6. Sınıf": {
        "Temalar": ["1. Tema: Sayılar ve Nicelikler", "6. Tema: Veriden Olasılığa"],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.6.1.1",
                    "cikti": (
                        "Doğal sayının çarpan ve katlarına yönelik muhakeme"
                        " yapabilme"
                    ),
                    "surec": [
                        "a) Çarpan ve katlarına yönelik varsayımlarda bulunur.",
                        (
                            "b) Örnek durumların ilişkilerini inceleyerek"
                            " genellemeleri belirler."
                        ),
                        (
                            "c) Genellemelerin varsayımı karşılayıp"
                            " karşılamadığını modellerle gösterir."
                        ),
                    ],
                    "hook": (
                        "Otobüs duraklarında iki farklı hattın aynı anda hareket"
                        " etme saatleri."
                    ),
                    "kriz": (
                        "Öğrenci 'Hocam bu kuralları ezberlemek zorunda mıyız,"
                        " manavda EKOK mu hesaplayacağız?' diye isyan eder."
                    ),
                }
            ],
            "6. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.6.6.1",
                    "cikti": (
                        "Bir olayın olasılığını gözleme dayalı tahmin edebilme"
                    ),
                    "surec": [
                        "a) Olasılık ile deney verisini ilişkilendirir.",
                        (
                            "b) Tekrar sayısı ile göreli sıklık ilişkisini çıkarım"
                            " yapar."
                        ),
                        (
                            "c) Göreli sıklığın kullanımına yönelik yargıda"
                            " bulunur."
                        ),
                    ],
                    "hook": "Madeni para atma deneylerinde 100 atıştaki değişim.",
                    "kriz": (
                        "Öğrenci 'Hocam ben 10 kez attım hepsi yazı geldi,"
                        " teoriniz yanlış, para hileli' diye bağırarak"
                        " deneyi reddeder."
                    ),
                }
            ],
        },
    },
    "7. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "6. Tema: İstatistiksel Araştırma",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.7.1.4",
                    "cikti": (
                        "Rasyonel sayılar ve işlemler içeren gerçek yaşam"
                        " problemlerini çözebilme"
                    ),
                    "surec": [
                        "a) Sayı ve işlem bileşenlerini belirler.",
                        (
                            "b) İstenenler ile seçilen işlemler arasındaki ilişkiyi"
                            " belirler."
                        ),
                        "c) Problemi uygun temsillere dönüştürür.",
                        "d) Stratejiler oluşturup çözer.",
                    ],
                    "hook": "Banka kredi faiz kesintileri ve bütçe planlaması.",
                    "kriz": (
                        "Negatif rasyonel sayılarda bölme yaparken hata yapan"
                        " öğrenci kalemi kırıp masaya vurur."
                    ),
                }
            ],
            "6. Tema: İstatistiksel Araştırma": [
                {
                    "kod": "MAT.7.6.1",
                    "cikti": (
                        "Kategorik veya nicel veri ile çalışabilme ve karar"
                        " verebilme"
                    ),
                    "surec": [
                        (
                            "a) İstatistiksel araştırma gerektiren durumları fark"
                            " eder."
                        ),
                        "b) Araştırma soruları oluşturur.",
                        (
                            "c) Ortalama mutlak sapma ve özetleme araçlarını seçme"
                            " gerekçesini belirtir."
                        ),
                    ],
                    "hook": (
                        "Okul kantininin günlük su satış miktarlarının yayılım"
                        " analizi."
                    ),
                    "kriz": (
                        "Öğrenci 'Hocam ortalama mutlak sapmayı niye"
                        " hesaplıyoruz, aritmetik ortalama yetmiyor mu?' diye"
                        " dersi tıkar."
                    ),
                }
            ],
        },
    },
    "8. Sınıf": {
        "Temalar": [
            "1. Tema: Sayılar ve Nicelikler",
            "7. Tema: Veriden Olasılığa",
        ],
        "Kazanimlar": {
            "1. Tema: Sayılar ve Nicelikler": [
                {
                    "kod": "MAT.8.1.2",
                    "cikti": (
                        "Kareköklü ifadeler ile ilgili muhakeme yapabilme"
                    ),
                    "surec": [
                        (
                            "a) Karenin alanı ile kenar uzunluğu ilişkisini"
                            " belirler."
                        ),
                        (
                            "b) Tam kare sayılar ile kareköklerini"
                            " ilişkilendirir."
                        ),
                        (
                            "c) Tam kare olmayanların hangi iki sayı arasında"
                            " olduğunu bulur."
                        ),
                    ],
                    "hook": (
                        "Alanı 50 metrekare olan kare şeklindeki stüdyo dairenin"
                        " parke hesabı."
                    ),
                    "kriz": (
                        "Otizmli Arda tahtadaki köklü ifade sesinden rahatsız"
                        " olup kulaklarını kapatarak sallanmaya başlar."
                    ),
                }
            ],
            "7. Tema: Veriden Olasılığa": [
                {
                    "kod": "MAT.8.7.1",
                    "cikti": (
                        "Olasılık yaklaşımlarından (öznel, deneysel, teorik)"
                        " uygun olanı belirleyerek karar verebilme"
                    ),
                    "surec": [
                        "a) Karar vermeye yönelik amacı belirler.",
                        "b) Karara ilişkin bilgi toplar.",
                        "c) Olasılık yaklaşımlarına yönelik önermeler oluşturur.",
                    ],
                    "hook": (
                        "Futbol teknik direktörlerinin penaltı atışı stratejisi"
                        " seçimi."
                    ),
                    "kriz": (
                        "Üstün yetenekli Can 'Her şey teorik olasılıkla"
                        " ölçülemez, öznel duygu her zaman ağır basar' diyerek"
                        " tartışma çıkarır."
                    ),
                }
            ],
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE RUBRİK YÜKLEME PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen 2026 Maarif Modeli Kurulum ve Rubrik Yükleme Paneli"
  )
  st.info(
      "Okul numaranızı, bilgilerinizi girin ve uygulama öğretim elemanının"
      " rubriğini sisteme yükleyerek 3D canlı stajı başlatın."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Deniz Arslan"
    )
    okul_numarasi = st.text_input(
        "Okul Numarası", placeholder="Örn: 20210504012"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Marmara Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )
    uygulama_ogretim_elemani = st.text_input(
        "Uygulama Öğretim Elemanı (Danışman Hoca)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown(
        "### 📋 Uygulama Öğretim Elemanı Rubriği (Sisteme Yükleme / Yapıştırma)"
    )
    rubrik_dosya = st.file_uploader(
        "Hocanın Rubrik Dosyasını Yükle (PDF, Word veya Metin)",
        type=["pdf", "docx", "txt"],
    )

    rubrik_metni = st.text_area(
        "Veya Hocanın Rubrik Kriterlerini Buraya Yapıştırın",
        value=(
            "1. 3D sınıf ortamında sesli kriz yönetimi ve empati (30 Puan).\n2."
            " Bireysel farklılıklara (disleksi, otizm, kaygı) duyarlı kapsayıcı"
            " sesli hitabet (30 Puan).\n3. 2026 Maarif Modeli kazanım ve süreç"
            " bileşenleri tam uyumu (20 Puan).\n4. Sahada uygulanabilirlik ve"
            " olumsuz durumlara karşı aksiyon alma başarısı (20 Puan)."
        ),
        height=100,
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

  if st.button("🚀 2026 Maarif Modeli 3D Staj Simülasyonunu Başlat"):
    if (
        not ogretmen_adi
        or not okul_numarasi
        or not universite_adi
        or not uygulama_ogretim_elemani
    ):
      st.warning(
          "Lütfen öğretmen adı, okul numarası, üniversite ve danışman hoca"
          " alanlarını doldurunuz."
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
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretim Elemanı"
  )

  st.markdown(
      f"### 🏫 3D Canlı Sınıf & Sesli Etkileşim | Aday: {ogretmen} (No:"
      f" {okul_no}) - {universite}"
  )

  col_s1, col_s2 = st.columns(2)
  with col_s1:
    secilen_sinif = st.selectbox(
        "1️⃣ Sınıf Düzeyi Seçin", list(tyym_master_arsiv.keys())
    )
  with col_s2:
    secilen_tema = st.selectbox(
        "2️⃣ Tema Seçin", tyym_master_arsiv[secilen_sinif]["Temalar"]
    )

  kazanim_listesi = tyym_master_arsiv[secilen_sinif]["Kazanimlar"][secilen_tema]
  secilen_kazanim_obj = kazanim_listesi[0]

  st.markdown(
      f"**3️⃣ Seçilen Resmî Kazanım Kodu:** `{secilen_kazanim_obj['kod']}`"
  )
  st.markdown(
      f"**4️⃣ Öğrenme Çıktısı:** {secilen_kazanim_obj['cikti']}"
  )

  secilen_surec = st.selectbox(
      "5️⃣ Odaklanılacak Süreç Bileşeni (a, b, c, ç...):",
      secilen_kazanim_obj["surec"],
  )
  st.success(
      f"💡 **2026 Maarif Modeli Gerçek Yaşam Kancası:**"
      f" {secilen_kazanim_obj['hook']}"
  )

  aktif_kriz = secilen_kazanim_obj["kriz"]

  st.markdown(
      """
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 25px; border-radius: 16px; color: white; border: 3px solid #3b82f6; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <h2 style="margin-top:0; color:#60a5fa; text-align:center;">🌐 3D İzometrik Canlı Sınıf Ortamı & Aktif Öğrenci Avatarları</h2>
        <p style="text-align: center; color: #94a3b8; font-size: 15px;">Aşağıdaki 3D sınıf haritasında öğrencilerinizin anlık jest, mimik ve duyusal kriz durumları canlı olarak simüle edilmektedir.</p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px;">
            <div style="background: rgba(239, 68, 68, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #ef4444; text-align: center;">
                <div style="font-size: 28px;">👦</div>
                <strong>Kerem (Avatar #1)</strong><br>
                <span style="font-size: 13px; color: #fca5a5;">Mimik: Endişeli / Alnını ovuşturuyor</span><br>
                <span style="font-size: 11px; background: #991b1b; padding: 2px 6px; border-radius: 4px;">Durum: Disleksili</span>
            </div>
            
            <div style="background: rgba(16, 185, 129, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #10b981; text-align: center;">
                <div style="font-size: 28px;">👧</div>
                <strong>Arda (Avatar #2)</strong><br>
                <span style="font-size: 13px; color: #6ee7b7;">Mimik: Kulaklık takılı / Sallanıyor</span><br>
                <span style="font-size: 11px; background: #065f46; padding: 2px 6px; border-radius: 4px;">Durum: Otizm Spektrumlu</span>
            </div>
            
            <div style="background: rgba(245, 158, 11, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #f59e0b; text-align: center;">
                <div style="font-size: 28px;">👦</div>
                <strong>Can (Avatar #3)</strong><br>
                <span style="font-size: 13px; color: #fde68a;">Mimik: Sabırsız / Parmağı havada</span><br>
                <span style="font-size: 11px; background: #78350f; padding: 2px 6px; border-radius: 4px;">Durum: Üstün Yetenekli</span>
            </div>
            
            <div style="background: rgba(168, 85, 247, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #a855f7; text-align: center;">
                <div style="font-size: 28px;">👧</div>
                <strong>Elif (Avatar #4)</strong><br>
                <span style="font-size: 13px; color: #d8b4fe;">Mimik: Başını öne eğmiş / Kaygılı</span><br>
                <span style="font-size: 11px; background: #581c87; padding: 2px 6px; border-radius: 4px;">Durum: Yüksek Kaygılı</span>
            </div>
        </div>
        
        <div style="margin-top: 15px; background: rgba(59, 130, 246, 0.2); padding: 12px; border-radius: 8px; border: 1px solid #3b82f6; text-align: center;">
            👨‍🏫 <strong>Arka Sıra Gözlemcisi:</strong> Danışman Hocanız yüklediğiniz rubrik kriterleriyle sizi izliyor.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### ⚡ 3D Sınıf İçi Anlık Kriz Durumu")
    st.warning(aktif_kriz)

    st.markdown("### 🎙️ Gerçek Mikrofon & Sesli Hitabet Konsolu")
    st.info(
        "Mikrofon simülasyonu aktif. Sınıftaki kriz durumuna karşı sesli"
        " konuşun."
    )

    mic_html = """
        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 2px dashed #3b82f6; text-align: center;">
            <p style="color: #93c5fd; margin-bottom: 10px;">🎤 Mikrofonu Açmak İçin Aşağıdaki Butona Tıklayın:</p>
            <button onclick="startListening()" style="background: #ef4444; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold;">🔴 Mikrofonu Aç / Konuş</button>
            <p id="transcript" style="margin-top: 15px; color: #4ade80; font-style: italic; font-size: 15px;">Sesli Komut Bekleniyor...</p>
        </div>
        <script>
            function startListening() {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert("Tarayıcınız ses tanımayı desteklemiyor.");
                    return;
                }
                const recognition = new SpeechRecognition();
                recognition.lang = 'tr-TR';
                recognition.interimResults = false;
                document.getElementById('transcript').innerText = "Dinleniyor...";
                recognition.onresult = function(event) {
                    const text = event.results[0][0].transcript;
                    document.getElementById('transcript').innerText = "Algılanan: " + text;
                };
                recognition.start();
            }
        </script>
        """
    st.components.v1.html(mic_html, height=150)

    sesli_girdi_manuel = st.text_input(
        "⌨️ Sesli Sinyal Notu / Alternatif Girdi",
        placeholder=(
            "Örn: 'Sakin ol Kerem, birlikte aşacağız...' "
        ),
    )

    st.markdown(
        "### 👩‍🏫 Bu Kriz Durumunda 2026 Maarif Modeli'ne Göre Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sahada uygulanabilirlik ve rubrik kriterleri açısından doğru aksiyonu"
        " seçin:",
        [
            (
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve"
                " sınıf disiplinini sert kurallarla korumak."
            ),
            (
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak,"
                " akran destekli empati kurdurmak ve somut materyalle desteklemek"
                " (2026 Maarif Modeli Örnek Aksiyonu)."
            ),
            (
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu"
                " anlatmaya devam etmek."
            ),
            (
                "D) Danışman hocaya dönüp sınıfın yönetilemez olduğunu"
                " bildirmek."
            ),
            (
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak"
                " kavramsal değişimi tetiklemek (Yüksek Pedagojik Etki)."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Detaylı Raporlamaya Geç"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "tema": secilen_tema,
          "kod": secilen_kazanim_obj["kod"],
          "surec": secilen_surec,
          "kriz": aktif_kriz,
          "karar": ogretmen_karari,
          "sesli_komut": sesli_girdi_manuel,
      })
      st.success(
          "✅ 3D staj kararınız ve sesli kayıtlarınız sisteme işlendi! Sağ"
          " taraftan 2026 Maarif ve rubrik uyum analizlerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown(
        "#### 💡 2026 Maarif Modeli & Yüklenen Rubrik Uyum Analizi Paneli"
    )

    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Rubrik Kriterleri Kapsamında Saha Analizi")
      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.success(
            "🌟 **Mükemmel Rubrik ve Maarif Uyumu (100/100):** Seçtiğiniz bu"
            " yaklaşım; yüklediğiniz rubriğin kapsayıcı eğitim ve kriz"
            " yönetimi maddeleriyle ve 2026 Türkiye Yüzyılı Maarif Modeli"
            " felsefesiyle birebir örtüşmektedir."
        )
      else:
        st.error(
            "⚠️ **Rubrik Uyarı Uyarısı:** Bu geleneksel yaklaşım, yüklediğiniz"
            " rubriğin kapsayıcı eğitim ilkelerini ihlal eder ve danışman"
            " hocadan düşük puan almanıza neden olur."
        )

      st.markdown(
          "##### 🛠️ Öğretmen Adayı İçin Net Ne Yapmalı / Nasıl Davranmalı Eylem"
          " Planı"
      )
      st.markdown(
          "- **Adım 1 (Güvenli Alan):** Öğrenciyi asla akranlarının önünde"
          " eleştirmeyin; 'Birlikte bakalım, bu harika bir keşif fırsatı'"
          " diyerek hitap edin.\n- **Adım 2 (Somutlaştırma):** Soyut kavramları"
          " onluk taban blokları veya dijital araçlarla destekleyin.\n- **Adım"
          " 3 (Rubrik Eşleme):** Yüklediğiniz rubriğin duyarlılık kriterini"
          " birebir uygulayın."
      )

      st.divider()
      if st.button("📋 Çok Katmanlı Detaylı Raporlama Paneline Geç"):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı kaydedip butona bastıktan sonra rubrik"
          " ve Maarif modeline uygunluk analizleri burada açılacaktır."
      )

# ==========================================
# 4. ADIM 3: ÇOK KATMANLI, GRAFİKLİ VE DETAYLI RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "🎥 2026 MAARİF MODELİ & RUBRİK UYUMLU ÇOK KATMANLI DETAYLI RAPORLAMA"
      " SİSTEMİ"
  )
  st.markdown(
      f"**Üniversite & Fakülte:** {st.session_state.get('universite_adi', 'N/A')}"
      f" / {st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
      f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} |"
      f" **Okul No:** {st.session_state.get('okul_numarasi', 'N/A')} |"
      f" **Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
  )
  st.markdown(
      f"**Rapor Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
  )

  st.divider()

  tab_aday, tab_fakulte, tab_ogretim = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Gelişim, 3D Video & Eylem Planı",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Puan Matrisi & Geri Dönüt",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 3D Sınıf ve
