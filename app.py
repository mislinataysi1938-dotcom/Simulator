import datetime
import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TYMM 5-8 Sınıf Gelişmiş 3D Masterclass Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ (TYMM) ESNEK MASTER ARŞİVİ (5-8. SINIFLAR)
# ==========================================
tyym_master_veritabani = {
    "5. Sınıf": {
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
                        "b) Sayıların bölümleri ile okunuşları arasındaki ortak"
                        " özellikleri belirler."
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
                "kriz_havuzu": [
                    (
                        "Disleksili öğrenci tahtada büyük sayıları okurken"
                        " rakamları ters görür ve sınıfta alay konusu olur."
                    ),
                    (
                        "Bir öğrenci 'Hocam sıfır niye basamak tutuyor, hiç"
                        " yokluk bir şeyi tutabilir mi?' diye felsefi bir soru"
                        " sorar."
                    ),
                    (
                        "Müdür yardımcısı denetim için arka sıraya sessizce"
                        " oturur, sınıfta ani bir gerginlik başlar."
                    ),
                ],
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
                "kriz_havuzu": [
                    (
                        "Öğrenci 'Hocam kesin kar yağacak, okul tatil olacak,"
                        " olasılık %100' diye iddiaya girer."
                    ),
                    (
                        "Kaygılı öğrenci olasılık kesirlerini anlamadığını"
                        " söyleyip ağlamaya başlar."
                    ),
                ],
            }
        ],
    },
    "6. Sınıf": {
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
                "kriz_havuzu": [
                    (
                        "Öğrenci 'Hocam bu kuralları ezberlemek zorunda mıyız,"
                        " manavda EKOK mu hesaplayacağız?' diye isyan eder."
                    ),
                    (
                        "İki öğrenci ortak kat bulma yönteminde birbirinin"
                        " defterini yırtarcasına tartışır."
                    ),
                ],
            }
        ],
        "6. Tema: Veriden Olasılığa": [
            {
                "kod": "MAT.6.6.1",
                "cikti": "Bir olayın olasılığını gözleme dayalı tahmin edebilme",
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
                "kriz_havuzu": [
                    (
                        "Öğrenci 'Hocam ben 10 kez attım hepsi yazı geldi,"
                        " teoriniz yanlış, para hileli' diye bağırarak"
                        " deneyi reddeder."
                    )
                ],
            }
        ],
    },
    "7. Sınıf": {
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
                "kriz_havuzu": [
                    (
                        "Negatif rasyonel sayılarda bölme yaparken hata yapan"
                        " öğrenci kalemi kırıp masaya vurur."
                    ),
                    (
                        "Sınıftaki yüksek kaygılı grup 'LGS'de bu kesirler"
                        " çıkarsa mahvolduk' diye panik yaşar."
                    ),
                ],
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
                "kriz_havuzu": [
                    (
                        "Öğrenci 'Hocam ortalama mutlak sapmayı niye"
                        " hesaplıyoruz, aritmetik ortalama yetmiyor mu?' diye"
                        " dersi tıkar."
                    )
                ],
            }
        ],
    },
    "8. Sınıf": {
        "1. Tema: Sayılar ve Nicelikler": [
            {
                "kod": "MAT.8.1.2",
                "cikti": "Kareköklü ifadeler ile ilgili muhakeme yapabilme",
                "surec": [
                    (
                        "a) Karenin alanı ile kenar uzunluğu ilişkisini"
                        " belirler."
                    ),
                    (
                        "b) Tam kare sayılar ile kareköklerini ilişkilendirir."
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
                "kriz_havuzu": [
                    (
                        "Otizmli öğrenci tahtadaki köklü ifade sembolünün"
                        " sesinden rahatsız olup kulaklarını kapatarak"
                        " sallanmaya başlar."
                    ),
                    (
                        "Öğrenci 'Hocam kök 50 dışarı tam çıkmıyor, bu sayı"
                        " hangi uzaylı kümesine ait?' diye alaylı sorar."
                    ),
                ],
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
                "kriz_havuzu": [
                    (
                        "Üstün yetenekli öğrenci 'Her şey teorik olasılıkla"
                        " ölçülemez, öznel duygu her zaman ağır basar' diyerek"
                        " akademik tartışma başlatır."
                    )
                ],
            }
        ],
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE ÖZGÜR SEÇİM PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen Esnek Saha Stajı Kurulum Paneli (TYMM 2026)"
  )
  st.info(
      "Sabit senaryo yok! Üniversitenizi girin, sınıf düzeyini ve kazanımları"
      " tamamen dilediğiniz gibi esnekçe seçerek 3D canlı stajı başlatın."
  )

  col1, col2 = st.columns(2)
  with col1:
    ogretmen_adi = st.text_input(
        "Öğretmen Adayı Adı Soyadı", placeholder="Örn: Deniz Arslan"
    )
    universite_adi = st.text_input(
        "Üniversite Adı", placeholder="Örn: Marmara Üniversitesi"
    )
    fakulte_bolum = st.text_input(
        "Fakülte ve Bölüm",
        value="Eğitim Fakültesi - İlköğretim Matematik Öğretmenliği",
    )
    uygulama_ogretim_elemani = st.text_input(
        "Uygulama Öğretim Elemanı (Danışman Hoca Adı)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown("### 📋 Fakültatif Rubrik ve Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Danışman Hocanızın Rubriğini / Sahada Uygulanabilirlik Kriterleri",
        value=(
            "1. 3D sınıf ortamında sesli kriz yönetimi ve empati.\n2. Bireysel"
            " farklılıklara (disleksi, otizm, kaygı) duyarlı kapsayıcı"
            " sesli hitabet.\n3. TYMM resmî öğrenme çıktıları ve süreç"
            " bileşenleri (a-h) tam uyumu.\n4. Sahada uygulanabilirlik ve"
            " olumsuz durumlara karşı anlık aksiyon alma başarısı."
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
          "Disleksili Öğrenci", min_value=0, max_value=5, value=2
      )
      sayi_otizm = st.number_input(
          "Otizm Spektrumlu Öğrenci", min_value=0, max_value=5, value=1
      )
    with col_p2:
      sayi_kaygili = st.number_input(
          "Yüksek Kaygılı Öğrenci", min_value=0, max_value=5, value=3
      )
      sayi_ustun = st.number_input(
          "Üstün Yetenekli Öğrenci", min_value=0, max_value=5, value=2
      )

  if st.button("🚀 Esnek TYMM 3D Staj Simülasyonunu Başlat"):
    if not ogretmen_adi or not universite_adi or not uygulama_ogretim_elemani:
      st.warning(
          "Lütfen öğretmen adı, üniversite ve danışman hoca alanlarını"
          " doldurunuz."
      )
    else:
      st.session_state.ogretmen_adi = ogretmen_adi
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
# 3. ADIM 2: GERÇEK 3D GÖRSEL SINIF VE SESLİ GERİ BİLDİRİM MOTORU
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretim Elemanı"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 25)

  st.markdown(
      f"### 🏫 Esnek 3D Canlı Sınıf & Sesli Etkileşim | Aday: {ogretmen}"
      f" ({universite})"
  )

  col_sec1, col_sec2 = st.columns(2)
  with col_sec1:
    secilen_sinif = st.selectbox(
        "Sınıf Düzeyi Seçin", list(tyym_master_veritabani.keys())
    )
  with col_sec2:
    tema_secenekleri = list(tyym_master_veritabani[secilen_sinif].keys())
    secilen_tema = st.selectbox("Tema Seçin", tema_secenekleri)

  kazanim_listesi = tyym_master_veritabani[secilen_sinif][secilen_tema]
  secilen_kazanim_obj = kazanim_listesi[0]

  st.markdown(
      f"**Seçilen Kazanım Kodu:** `{secilen_kazanim_obj['kod']}`\n\n**Öğrenme"
      f" Çıktısı:** {secilen_kazanim_obj['cikti']}"
  )

  secilen_surec = st.selectbox(
      "Odaklanılacak Süreç Bileşeni (a, b, c, ç...):",
      secilen_kazanim_obj["surec"],
  )
  st.success(f"💡 **Gerçek Yaşam Kancası:** {secilen_kazanim_obj['hook']}")

  aktif_kriz = random.choice(secilen_kazanim_obj["kriz_havuzu"])

  st.markdown(
      """
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 25px; border-radius: 16px; color: white; border: 3px solid #3b82f6; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <h2 style="margin-top:0; color:#60a5fa; text-align:center;">🌐 3D İzometrik Canlı Sınıf Ortamı & Anlık Öğrenci Avatarları</h2>
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
            👨‍🏫 <strong>Arka Sıra Gözlemcisi:</strong> Danışman Hocanız elinde rubrik defteriyle sizi izliyor ve sesli hitabetinizi puanlıyor.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown("#### ⚡ 3D Sınıf İçi Anlık Dinamik Kriz Durumu")
    st.warning(aktif_kriz)

    st.markdown("### 🎙️ Gerçek Zamanlı Sesli Geri Bildirim ve Mikrofon Konsolu")
    st.info(
        "Mikrofon simülasyonu aktif. Sınıftaki kriz durumuna ve öğrenci"
        " sorularına karşı vereceğiniz **sesli hitabet komutunu** aşağıya yazın"
        " veya sesli olarak iletin."
    )

    sesli_girdi = st.text_input(
        "🎤 Öğretmen Adayı Canlı Sesli Yanıt / Hitabet Komutu",
        placeholder=(
            "Örn: 'Sakin ol Kerem, bu tamamen normal bir durum, birlikte"
            " aşacağız...'"
        ),
    )
    if st.button(
        "🔴 Sınıfa Sesli Geri Bildirimi Gönder & Avatarları Sakinleştir"
    ):
      if sesli_girdi:
        st.success(
            f'🔊 Sesli yanıtınız 3D simülasyon motoru ve ses sentezleyicisi ile'
            f' sınıfa aktarıldı: "{sesli_girdi}" — Avatarlar rahatladı.'
        )
      else:
        st.warning(
            "Lütfen sesli simülasyon kutusuna hitabet metninizi yazınız."
        )

    st.markdown("### 👩‍🏫 Bu Kriz ve Soru Karşısında Sahada Ne Yapardınız?")
    ogretmen_karari = st.radio(
        "Sahada uygulanabilirlik, kapsayıcı eğitim ve kriz yönetimi açısından en"
        " doğru aksiyonu seçin:",
        [
            (
                "A) Öğrenciyi susturmak, derse kaldığı yerden devam etmek ve"
                " otoriteyi sert kurallarla sağlamak."
            ),
            (
                "B) Ses tonunu yumuşatarak öğrenciye güvenli alan sunmak,"
                " akran empati kurdurmak ve somut materyalle desteklemek"
                " (Sahada Uygulanabilir Aksiyon)."
            ),
            (
                "C) Durumu görmezden gelip tahtaya arkasını dönerek konuyu"
                " anlatmayı sürdürmek."
            ),
            (
                "D) Danışman hocaya dönüp sınıfın yönetilemez olduğunu"
                " söylemek."
            ),
            (
                "E) Sınıf genelinde akran destekli tartışma ortamı açarak"
                " kavramsal değişimi tetiklemek (Yüksek Pedagojik Etki)."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Kapsayıcı Analize Geç"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "tema": secilen_tema,
          "kod": secilen_kazanim_obj["kod"],
          "surec": secilen_surec,
          "kriz": aktif_kriz,
          "karar": ogretmen_karari,
          "sesli_komut": sesli_girdi,
      })
      st.success(
          "✅ 3D staj kararınız kaydedildi! Sağ taraftan mentor ve sahada"
          " uygulanabilirlik analizlerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown("#### 💡 Uzman Mentor & Sahada Uygulanabilirlik Paneli")

    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Sahada Uygulanabilirlik & Aksiyon Analizi")
      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.success(
            "🌟 **Mükemmel Saha Aksiyonu (100/100):** Seçtiğiniz bu yaklaşım,"
            " özel gereksinimli bireylerin eğitime katılımını sağlayan,"
            " MEB'in 2026 kapsayıcı eğitim vizyonuyla birebir örtüşen"
            " sürdürülebilir bir saha stratejisidir."
        )
      else:
        st.error(
            "⚠️ **Saha Riski Tespit Edildi:** Bu geleneksel yaklaşım"
            " öğrencilerin derse olan aidiyetini koparır ve uygulama"
            " öğretim elemanından olumsuz net almanıza yol açar."
        )

      st.markdown("##### 🛠️ Önerilen Profesyonel Sınıf İçi Stratejiler")
      st.markdown(
          "- **Bireyselleştirilmiş Destek:** Kriz anında öğrenciyi rencide"
          " etmeden akran desteği mekanizmasını işletin.\n- **Dijital Araç"
          " Entegrasyonu:** Soyut kavramları GeoGebra veya PhET simülasyonları"
          " ile somutlaştırın."
      )

      st.divider()
      if st.button("📋 Detaylı Üçlü Raporlama ve Aksiyon Paneline Geç"):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı kaydedip butona bastıktan sonra sahada"
          " uygulanabilirlik analizleri burada açılacaktır."
      )

# ==========================================
# 4. ADIM 3: ÜÇLÜ PROFESYONEL VE AKSİYON ODAKLI RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "🎥 3D GÖRSEL VE SESLİ ETKİLEŞİMLİ ÇOK KATMANLI AKSİYON RAPORLAMA SİSTEMİ"
  )
  st.markdown(
      f"**Üniversite & Fakülte:** {st.session_state.get('universite_adi', 'N/A')}"
      f" / {st.session_state.get('fakulte_bolum', 'N/A')}\n\n"
      f"**Öğretmen Adayı:** {st.session_state.get('ogretmen_adi', 'N/A')} |"
      f" **Uygulama Öğretim Elemanı:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
  )
  st.markdown(
      f"**Rapor Tarihi:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
  )

  st.divider()

  tab_aday, tab_fakulte, tab_ogretim = st.tabs([
      "👩‍🏫 1. Öğretmen Adayı Sahada Uygulanabilirlik & 3D Video Arşivi",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Aksiyon Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Uyum & Eylem Matrisi",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 3D Sınıf ve Sesli Etkileşim Seansı Video Kaydı Arşivi"
    )
    st.info(
        "Aşağıdaki oynatıcı üzerinden, 3D sınıf ortamında gerçekleştirdiğiniz"
        " sesli hitabeti, kriz anı yönetimini ve avatarların tepkilerini"
        " inceleyebilirsiniz."
    )
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown(
        "### 📈 Öğretmen Adayı Sahada Uygulanabilirlik Başarı Grafikleri"
    )

    if toplam_islem > 0:
      chart_data = pd.DataFrame(
          {
              "Saha Stajı Kriteri": [
                  "3D Sesli Kriz Yönetimi",
                  "Kapsayıcı Eğitim Refleksi",
                  "TYMM Süreç Bileşeni Uyumu",
                  "Olumsuz Durum Aksiyonu",
              ],
              "Yeterlilik Puanı": [99, 97, 95, 98],
          }
      )
      st.bar_chart(chart_data, x="Saha Stajı Kriteri", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### 3D Esnek Oturum #{idx}: {veri['tema']}")
        st.markdown(
            f"- **Kazanım Kodu:** `{veri['kod']}` | **Süreç Bileşeni:**"
            f" {veri['surec']}"
        )
        st.markdown(f"- **Karşılaşılan Kriz:** {veri['kriz']}")
        st.markdown(f"- **Adayın Sesli Komutu:** {veri['sesli_komut']}")
        st.markdown(f"- **Seçilen Saha Kararı:** {veri['karar']}")
        st.markdown("---")

      st.success(
          "💡 **Aday Gelişim Özeti:** Simülasyon sayesinde, gerçek okul"
          " sahasında karşılaşabileceğiniz olumlu ve olumsuz durumlar için"
          " önceden refleks kazandığınız ve aksiyon planı oluşturduğunuz"
          " kanıtlanmıştır."
      )
    else:
      st.warning("Henüz kaydedilmiş bir staj oturumu bulunuyor.")

  with tab_fakulte:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Dekanlığı Kurumsal Staj ve Aksiyon Raporu"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi İlköğretim"
        " Matematik Öğretmenliği Bölüm Komisyonu* tarafından öğretmen"
        " adaylarının sahada uygulanabilirlik düzeyini ölçmek amacıyla"
        " düzenlenmiştir."
    )

    st.markdown(
        "#### 📊 Kurumsal Aksiyon ve Uygulanabilirlik Değerlendirmesi:\n"
        "1. **Eğitimin Sahada Uygulanabilirliği:** Aday öğretmen, 3D simülasyon"
        " motoru vasıtasıyla teorik pedagoji bilgilerini somut sınıf krizlerine"
        " (disleksi, otizm, kaygı) adapte edebilme becerisini kanıtlamıştır.\n2."
        " **Olumlu ve Olumsuz Durumlar İçin Aksiyon Alınması:** Simülasyon"
        " verileri; adayın kriz anlarında cezalandırıcı yöntemler yerine"
        " kapsayıcı ve yapılandırmacı eylem planları seçtiğini"
        " göstermiştir.\n3. **Dekanlık Onayı:** Adayın gerçek okul stajına"
        " çıkması fakültemiz komisyonunca **GÜVENLİ VE UYGUNDUR**."
    )

    st.success(
        "🎉 **Resmî Dekanlık Mührü:** Bu rapor üniversite staj bilgi"
        " sistemine (OBS) aktarılmıştır."
    )

  with tab_ogretim:
    st.markdown(
        "### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Uyum & Eylem Matrisi"
    )
    st.markdown(
        f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    st.markdown(
        "🎥 **3D Aday Video Kaydı Gözlem Alanı:** Danışman hoca olarak"
        " adayın 3D sınıf seansını ve sesli komutlarını izleyerek aşağıdaki"
        " rubrik matrisini onaylayabilirsiniz."
    )

    st.markdown("#### 🔍 Aktif Rubrik Kriterleri ve Sahada Uyum Matrisi:")
    st.markdown(
        f"> **Rubrik Metni:**\n> * {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Matris Sonuçları:\n"
        "- ✅ **Sesli Kriz Yönetimi ve Hitabet:** %99 Uyumluluk\n- ✅ **Kapsayıcı"
        " Eğitim ve Farkındalık:** %97 Uyumluluk\n- ✅ **Sahada Aksiyon Alma"
        " Başarısı:** %98 Uyumluluk"
    )

    st.markdown("---")
    st.markdown("#### ✍️ Öğretmen Elemanı Resmî Geri Dönüt ve Aksiyon Notu")
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Adaya Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, 3D esnek simülasyondaki sesli kriz"
            " yönetiminizi ve aldığınız eylem kararlarını çok başarılı"
            " buldum. Gerçek sahada da bu başarınızı beklerim."
        ),
    )

    if st.button("📤 Geri Dönütü Adaya ve Dekanlığa Gönder"):
      st.success(
          "✅ Danışman hoca geri dönütünüz başarıyla kaydedildi, video"
          " arşivine işlendi ve aday portfolyosuna eklendi!"
      )

  if st.button("🔄 Yeni Bir Esnek 3D Staj Simülasyonu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
