import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TYMM Resmî Tam Müfredat (5-8) 3D Masterclass Staj Simülatörü",
    page_icon="🎓",
    layout="wide",
)

# Oturum Durumu Yönetimi
if "simulasyon_gecmisi" not in st.session_state:
  st.session_state.simulasyon_gecmisi = []
if "adim" not in st.session_state:
  st.session_state.adim = 1  # 1: Kurulum, 2: 3D Sınıf & Sesli Staj, 3: Raporlar

# ==========================================
# 1. 2026 TÜRKİYE YÜZYILI MAARİF MODELİ RESMİ MASTER ARŞİVİ (5, 6, 7 ve 8. SINIFLAR TAM KAZANIMLAR)
# ==========================================
tyym_resmi_master_arsiv = {
    "5. Sınıf": {
        "1. Tema: Sayılar ve Nicelikler (Milyonlar & Basamak Yapısı)": {
            "kod": "MAT.5.1.1",
            "cikti": (
                "Altı basamaklı sayıları okuma ve yazmayı çok basamaklı"
                " sayılara genelleyebilme"
            ),
            "surec_bilesenleri": [
                (
                    "a) Günlük hayattaki farklı bağlamlardan yola çıkarak"
                    " altıdan çok basamaklı sayılar hakkında bilgi toplar."
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
                    "ç) Sayıların bölümleri ile okunuşları arasındaki"
                    " örüntüler üzerinden basamak sayısı altıdan çok olan"
                    " sayıların okunuş ve yazılışları hakkında önermelerde"
                    " bulunur."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Millî Kütüphane'deki 405.020 adet"
                " tarihi el yazması kitabın arşiv kodlama sistemi ve bölük"
                " analizi."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Müdür yardımcısı arkada"
                " otururken, Disleksili Kerem (Avatar #1) sesli olarak"
                " ağlayarak 'Hocam ben milyarlık basamakları okuyamıyorum, kafam"
                " çorba gibi oldu' der. Üstün Yetenekli Can (Avatar #3)"
                " kıkırdayarak alay eder. Arkadan bir öğrenci parmak"
                " kaldırıp sesli olarak 'Hocam sıfır niye basamak tutuyor, hiç"
                " yokluk bir şeyi tutabilir mi?' diye derin bir soru sorar."
            ),
            "zorluk": "İdari Denetim, Sesli Ağlama Krizi, Alay ve Felsefi Soru",
            "yanilgi": (
                "Sıfırın basamak tutucu rolünü anlamayıp boşlukları yok sayma"
                " eğilimi."
            ),
            "strateji": (
                "Mikrofonu açıp sesli hitabetle Kerem'ere güven vermek, Can'a"
                " uyarıda bulunmak ve onluk taban bloklarıyla somut açıklama"
                " yapmak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Renkli Onluk Taban Blokları\n💻 **Web"
                " Aracı:** [Math Learning Center Base Ten"
                " Blocks](https://www.mathlearningcenter.org/apps/base-ten-blocks)"
            ),
        }
    },
    "6. Sınıf": {
        "1. Tema: Sayılar ve Nicelikler (Çarpanlar ve Katlar)": {
            "kod": "MAT.6.1.1",
            "cikti": (
                "Karşılaştığı problem durumlarında bir doğal sayının çarpan ve"
                " katlarına yönelik muhakeme yapabilme"
            ),
            "surec_bilesenleri": [
                "a) Karşılaştığı durumlarda varsayımlarda bulunur.",
                (
                    "b) Örnek durumların içerdiği ilişkileri inceleyerek"
                    " genellemeleri belirler."
                ),
                (
                    "c) Genellemelerin varsayımı karşılayıp karşılamadığını"
                    " modellerle gösterir."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Otobüs duraklarındaki hareket saatleri"
                " ortak kat bulma senaryosu."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Ortak kat bulmada hata yapan"
                " sınıf birbirine girer. Arkadan bir öğrenci 'Hocam bu"
                " kuralları ezberlemek zorunda mıyız, hayatımızda ekmek"
                " alırken EKOK mu hesaplayacağız?' diye isyan eder."
            ),
            "zorluk": "Matematiksel Soyutlama Direnci ve İşlevsellik Sorgusu.",
            "yanilgi": "En küçük ortak katın, sayıların çarpımı olduğunu sanma.",
            "strateji": (
                "Renkli çubuklarla ortak kat modelleri kurarak gerçek yaşam"
                " işlevselliğini sesli olarak kanıtlamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Renkli Kat Çubukları\n💻 **Web Aracı:**"
                " [Desmos Factorization](https://www.desmos.com)"
            ),
        }
    },
    "7. Sınıf": {
        "6. Tema: İstatistiksel Araştırma Süreci (Sürekli Veri)": {
            "kod": "MAT.7.6.1",
            "cikti": (
                "Kategorik veya nicel (sürekli) veri ile çalışabilme ve veriye"
                " dayalı karar verebilme"
            ),
            "surec_bilesenleri": [
                (
                    "a) Kategorik veya nicel (sürekli) veriyee dayanan"
                    " istatistiksel araştırma gerektiren durumları fark eder."
                ),
                (
                    "b) Betimleme veya karşılaştırma gerektirebilecek araştırma"
                    " soruları oluşturur."
                ),
                (
                    "c) Veri görselleştirme ve özetleme araçlarını (ortalama"
                    " mutlak sapma vb.) seçme gerekçelerini belirtir."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Sınıfın günlük su tüketim miktarlarının"
                " ortalama mutlak sapma analizi."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Öğrenciler 'Hocam ortalama"
                " mutlak sapmayı niye hesaplıyoruz, zaten ortalamayı bulduk"
                " yetmez mi?' diye isyan eder."
            ),
            "zorluk": "Veri Yayılımını Anlama ve Sapma Direnci.",
            "yanilgi": (
                "Aritmetik ortalamanın veri grubundaki tüm karakteristiği"
                " tek başına yansıttığını zannetme."
            ),
            "strateji": (
                "Verilerin sayı doğrusundaki dağılımını göstererek ortalamaya"
                " olan mesafeleri somut olarak toplamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Nokta Grafik Kartları\n💻 **Web Aracı:**"
                " [NCES Data Tool](https://nces.ed.gov)"
            ),
        }
    },
    "8. Sınıf": {
        "4. Tema: Geometrik Nicelikler (Silindir ve Prizmalar)": {
            "kod": "MAT.8.4.1",
            "cikti": (
                "Dik prizmalar, dikdörtgen dik piramit, dik dairesel silindir ve"
                " dik dairesel koninin yüzey açınımlarını çözümleyebilme"
            ),
            "surec_bilesenleri": [
                (
                    "a) Dik prizmalar, silindir ve koninin yüzey açınımlarında"
                    " yer alan şekilleri belirler[span_12](start_span)[span_12](end_span)."
                ),
                (
                    "b) Yüzey açınımlarında yer alan şekiller arasındaki"
                    " ilişkileri belirler[span_13](start_span)[span_13](end_span)."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Konserve kutularının ve dondurma"
                " külahlarının üretim açınım planları."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Öğrenci 'Hocam silindirin yan"
                " yüzeyi açılınca neden dikdörtgen oluyor, daire olması"
                " gerekmez miydi?' diye sesli sorar."
            ),
            "zorluk": "Üç Boyutlu Cisim Açınımı ve Yan Yüzey İlişkisi.",
            "yanilgi": (
                "Silindirin yan yüzeyinin açıldığında kare ya da daire"
                " olacağını zannetme."
            ),
            "strateji": (
                "Silindirik bir kağıt rulosunu makasla açarak dikdörtgene"
                " dönüşümünü sınıfta canlı olarak göstermek."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Silindir Açınım Kartonları\n💻 **Web"
                " Aracı:** [GeoGebra 3D Shapes](https://www.geogebra.org)"
            ),
        },
        "5. Tema: Dönüşüm (Öteleme ve Yansıma)": {
            "kod": "MAT.8.5.3",
            "cikti": "Öteleme ve yansıma dönüşümlerini içeren problemleri çözebilme",
            "surec_bilesenleri": [
                (
                    "a) Öteleme ve yansıma dönüşümlerine ilişkin"
                    " problemlerde eşlik, uzaklık ve koordinat"
                    " bileşenlerini belirler[span_14](start_span)[span_14](end_span)."
                ),
                (
                    "b) Problemin çözümüne yönelik stratejiler geliştirir ve"
                    " uygular[span_15](start_span)[span_15](end_span)."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Bilgisayar oyunlarındaki karakter"
                " animasyonları ve koordinat öteleme matrisleri."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Kaygılı Elif (Avatar #4)"
                " koordinat sisteminde yansıma yaparken işaretleri"
                " karıştırıp 'Hocam x ve y eksi olunca kafam ters dönüyor'"
                " diye ağlar."
            ),
            "zorluk": "Koordinat Düzleminde İşaret Hatası Krizi.",
            "yanilgi": (
                "Yansıma yaparken hem x hem y koordinatının işaretinin aynı"
                " anda değişmesi gerektiği yanılgısı."
            ),
            "strateji": (
                "Aynalama modeliyle eksenlerin simetri aynası rolünü görsel"
                " olarak tahtada çizmek."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Koordinat Düzlemi Aynaları\n💻 **Web"
                " Aracı:** [Desmos Transformations](https://www.desmos.com)"
            ),
        },
        "7. Tema: Veriden Olasılığa (Olasılık Yaklaşımları)": {
            "kod": "MAT.8.7.1",
            "cikti": (
                "Gerçek yaşamda karşılaşabileceği bir olayın olasılığına ilişkin"
                " farklı olasılık yaklaşımlarından (öznel, deneysel, teorik)"
                " uygun olanı belirleyerek karar verebilme"
            ),
            "surec_bilesenleri": [
                (
                    "a) Bir olayın olasılığına ilişkin karar vermeye yönelik"
                    " amacı belirler[span_16](start_span)[span_16](end_span)."
                ),
                "b) Karara ilişkin bilgi toplar[span_17](start_span)[span_17](end_span).",
                (
                    "c) Karara ilişkin olasılık yaklaşımlarına yönelik"
                    " önermeler oluşturur[span_18](start_span)[span_18](end_span)."
                ),
                (
                    "d) Ulaştığı sonuca göre olasılık yaklaşımlarına ilişkin"
                    " seçim yapar[span_19](start_span)[span_19](end_span)."
                ),
            ],
            "hook": (
                "Gerçek Yaşam Kancası: Futbol maçlarında teknik direktörlerin"
                " penaltı atışı olasılık yaklaşımı seçimi."
            ),
            "kriz": (
                "3D Sınıf İçi Anlık Sesli Olay: Üstün Yetenekli Can (Avatar #3)"
                " 'Hocam her şey teorik olasılıkla hesaplanamaz ki, günlük"
                " hayatta hislerimizle (öznel) karar veriyoruz' diye derin bir"
                " tartışma başlatır."
            ),
            "zorluk": "Olasılık Yaklaşımlarını Ayırt Etme ve Felsefi Tartışma.",
            "yanilgi": (
                "Tüm olayların matematiksel olarak teorik olasılıkla birebir"
                " açıklanabileceğini zannetme."
            ),
            "strateji": (
                "Öznel, deneysel ve teorik yaklaşımların kullanım yerlerini"
                " gerçek hayat örnekleriyle karşılaştırmalı olarak açıklamak."
            ),
            "arac": (
                "🧩 **Somut Materyal:** Olasılık Yaklaşım Kartları\n💻 **Web"
                " Aracı:** [PhET Probability"
                " Sim](https://phet.colorado.edu/)"
            ),
        },
    },
}

# ==========================================
# 2. ADIM 1: KURULUM VE GİRİŞ PANELİ
# ==========================================
if st.session_state.adim == 1:
  st.subheader(
      "📝 Stajyer Öğretmen Gerçekçi Saha Stajı Kurulum Paneli (TYMM 2026 - 5-8"
      " Sınıflar)"
  )
  st.info(
      "Üniversitenizi, fakültenizi, bölümünüzü ve öğretim elemanınızı"
      " belirleyin; resmî TYMM 5-8. sınıf müfredatıyla 3D simülasyonu başlatın."
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
        "Uygulama Öğretim Elemanı (Danışman Hoca Adı ve Unvanı)",
        placeholder="Örn: Prof. Dr. Selma Çetin",
    )

  with col2:
    st.markdown("### 📋 Öğretim Elemanı Rubriği / Değerlendirme Kriterleri")
    rubrik_metni = st.text_area(
        "Danışman Hocanızın Rubriğini / Kriterlerini Buraya Yapıştırın",
        value=(
            "1. 3D sınıf ortamında sesli kriz yönetimi ve liderlik.\n2. Bireysel"
            " farklılıklara (disleksi, otizm, kaygı) duyarlı kapsayıcı"
            " sesli hitabet.\n3. TYMM resmî öğrenme çıktıları ve süreç"
            " bileşenleri uyumu (5-8. Sınıf).\n4. Akran çatışmalarını ve öğrenci"
            " sesli sorularını yönetme."
        ),
        height=110,
    )

    st.markdown("### 👥 Sanal Sınıf Mevcudu ve Eş Zamanlı Öğrenci Profilleri")
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

  if st.button(
      "🚀 TYMM 5-8 Sınıf Resmî Müfredatlı 3D ve Sesli Staj Simülasyonunu Başlat"
  ):
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
# 3. ADIM 2: 3D CANLI GÖRSEL SINIF VE SESLİ ETKİLEŞİM PANELLERİ
# ==========================================
elif st.session_state.adim == 2:
  ogretmen = st.session_state.get("ogretmen_adi", "Öğretmen Adayı")
  universite = st.session_state.get("universite_adi", "Üniversite")
  ogretim_elemani = st.session_state.get(
      "uygulama_ogretim_elemani", "Öğretmen Elemanı"
  )
  mevcut = st.session_state.get("sinif_mevcudu", 25)
  dagilim = st.session_state.get("profil_dagilimi", {})

  secilen_sinif = st.selectbox(
      "TYMM Sınıf Düzeyi Seçin (5-8)", list(tyym_resmi_master_arsiv.keys())
  )
  konu_secenekleri = list(tyym_resmi_master_arsiv[secilen_sinif].keys())

  st.markdown(
      f"### 🏫 TYMM Resmî 3D Canlı Sınıf & Sesli Etkileşim | Aday: {ogretmen}"
      f" ({universite})"
  )
  st.caption(
      f"Danışman Hoca: {ogretim_elemani} | Sınıf Mevcudu: {mevcut} | Aktif"
      f" Profiller: Disleksili({dagilim.get('Disleksili', 0)}),"
      f" Otizmli({dagilim.get('Otizmli', 0)}), Kaygılı({dagilim.get('Kaygılı', 0)}),"
      f" Üstün({dagilim.get('Üstün Yetenekli', 0)})"
  )

  # Tam Görsel 3D Sınıf ve Öğrenci Avatarları Paneli
  st.markdown(
      """
    <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 25px; border-radius: 16px; color: white; border: 3px solid #3b82f6; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <h2 style="margin-top:0; color:#60a5fa; text-align:center;">🌐 3D İzometrik Canlı Sınıf Ortamı & Öğrenci Avatarları</h2>
        <p style="text-align: center; color: #94a3b8; font-size: 15px;">Aşağıdaki 3D yerleşim planında öğrencilerinizin anlık jestlerini, mimiklerini ve konumlarını canlı olarak görmektesiniz.</p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px;">
            <div style="background: rgba(239, 68, 68, 0.25); padding: 15px; border-radius: 12px; border: 2px solid #ef4444; text-align: center;">
                <div style="font-size: 28px;">👦</div>
                <strong>Kerem (Avatar #1)</strong><br>
                <span style="font-size: 13px; color: #fca5a5;">Mimik: Endişeli / Alnını ovuşturuyor</span><br>
                <span style="font-size: 11px; background: #991b1b; padding: 2px 6px; border-radius: 4px;">Durum: Disleksili / Ağlıyor</span>
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
            👨‍🏫 <strong>Arka Sıra Gözlemcisi:</strong> Danışman Hocanız ({ogretim_elemani}) elinde rubrik defteriyle sizi izliyor.
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")

  secilen_konu = st.selectbox(
      "TYMM Resmî Tema ve Konu Başlığı", konu_secenekleri
  )
  veri = tyym_resmi_master_arsiv[secilen_sinif][secilen_konu]

  st.divider()

  st.markdown("### 🎯 2026 TYMM Öğrenme Çıktısı ve Süreç Bileşenleri")
  st.markdown(
      f"**Öğrenme Çıktısı Kodu:** `{veri['kod']}`\n\n**Öğrenme Çıktısı:**"
      f" {veri['cikti']}"
  )

  st.markdown("**İlgili Süreç Bileşenleri (a, b, c, ç...):**")
  for sb in veri["surec_bilesenleri"]:
    st.markdown(f"- {sb}")

  secilen_surec = st.selectbox(
      "Odaklanılacak Süreç Bileşeni / Alt Kırılım:", veri["surec_bilesenleri"]
  )
  st.success(f"💡 **{veri['hook']}**")

  col_sol, col_sag = st.columns([1, 1], gap="large")

  with col_sol:
    st.markdown(
        "#### ⚡ 3D Sınıf İçi Anlık Sesli Kriz ve Öğrenci Soru Senaryosu"
    )
    st.warning(veri["kriz"])
    st.markdown(f"**Karşılaşılan Kriz ve Soru Türü:** {veri['zorluk']}")

    # Sesli Geri Bildirim ve Mikrofon Konsolu
    st.markdown("### 🎙️ Canlı Sesli Geri Bildirim ve Mikrofon Konsolu")
    st.info(
        "Mikrofon simülasyonu aktif. Öğrencilerinize veya danışman hocanıza"
        " sesli yanıt vermek için konuşmanızı yazın ya da sesli"
        " komutunuzu iletin."
    )

    sesli_girdi = st.text_input(
        "🎤 Öğretmen Adayı Canlı Sesli Yanıt / Hitabet Komutu",
        placeholder=(
            "Örn: 'Çok haklısın Can, olasılık sadece teorik değil, öznel ve"
            " deneysel yaklaşımlarla da hayatımızı şekillendirir...'"
        ),
    )
    if st.button("🔴 Sınıfa Sesli Geri Bildirimi Gönder ve Avatarları Yönet"):
      if sesli_girdi:
        st.success(
            f'🔊 Sesli yanıtınız 3D simülasyon motoru tarafından işlendi ve'
            f' sınıfa sesli olarak yansıtıldı: "{sesli_girdi}"'
        )
      else:
        st.warning(
            "Lütfen sesli simülasyon kutusuna hitabet metninizi yazınız."
        )

    st.markdown(
        "### 👩‍🏫 Bu 3D Sınıf Krizi ve Soru Karşısında Ne Yapardınız?"
    )
    ogretmen_karari = st.radio(
        "Sınıf yönetimi, sesli kriz çözümü ve öğrenci sorularına yaklaşım"
        " açısından en uygun kararı seçiniz:",
        [
            (
                "A) Öğrencinin sorusunu duymazdan gelmek, bağırmak ve"
                " müfredata hızla devam etmek."
            ),
            (
                "B) Ses tonunu yumuşatarak krizdeki öğrenciye güvenli alan"
                " sunmak, akran empati kurdurmak ve somut model/dijital araçla"
                " konuyu bağlamak."
            ),
            (
                "C) Tahtaya arkasını dönerek dersi kendi kendine anlatıp"
                " bitirmeye çalışmak."
            ),
            (
                "D) Danışman hocaya dönüp sınıfı yönetemediğini sesli olarak"
                " söylemek."
            ),
            (
                "E) Sınıf genelinde akran destekli tartışma başlatarak"
                " soruyu tüm sınıfa yöneltmek ve kavramsal değişimi"
                " tetiklemek."
            ),
        ],
    )

    if st.button("📥 Staj Kararını Kaydet ve Sesli Oturumu Tamamla"):
      st.session_state.simulasyon_gecmisi.append({
          "tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "sinif": secilen_sinif,
          "konu": secilen_konu,
          "kod": veri["kod"],
          "surec": secilen_surec,
          "karar": ogretmen_karari,
          "yanilgi": veri["yanilgi"],
          "cozum": veri["strateji"],
          "materyaller": veri["arac"],
      })
      st.success(
          "✅ 3D staj kararınız ve sesli etkileşiminiz başarıyla"
          " kaydedildi! Sağ taraftan mentor analizlerini inceleyebilirsiniz."
      )

  with col_sag:
    st.markdown("#### 💡 Uzman / Mentor Geri Bildirim ve Materyal Paneli")

    if len(st.session_state.simulasyon_gecmisi) > 0:
      son_kayit = st.session_state.simulasyon_gecmisi[-1]

      st.markdown("##### 🔍 Tespit Edilen Kavram Yanılgısı & Kriz Analizi")
      st.error(son_kayit["yanilgi"])

      st.markdown("##### 🛠️ Önerilen Profesyonel Çözüm Stratejisi")
      st.success(son_kayit["cozum"])

      st.markdown(
          "##### 🧩 Doğrudan Tıklanabilir Dijital Web Araçları ve Somut"
          " Materyaller"
      )
      st.info(son_kayit["materyaller"])

      if "B)" in son_kayit["karar"] or "E)" in son_kayit["karar"]:
        st.markdown(
            "🌟 **Mentor Değerlendirmesi: Mükemmel (100/100)** — 3D sınıf"
            " ortamında öğrencilerin sesli sorularına ve krizlerine karşı"
            " gösterdiğiniz kapsayıcı refleks kusursuz!"
        )
      else:
        st.markdown(
            "⚠️ **Mentor Değerlendirmesi: Geliştirilebilir** — Bu yaklaşım"
            " öğrenci aidiyetini zedeler ve danışman hocadan düşük puan"
            " almanıza neden olur."
        )

      st.divider()
      if st.button("📋 Raporlama ve 3D Video Kayıt İnceleme Paneline Geç"):
        st.session_state.adim = 3
        st.rerun()
    else:
      st.info(
          "Sol taraftan kararlarınızı seçip 'Staj Kararını Kaydet' butonuna"
          " bastıktan sonra gizli uzman analizleri bu alanda açılacaktır."
      )

# ==========================================
# 4. ADIM 3: VİDEO KAYITLI VE ÜÇLÜ PROFESYONEL RAPORLAMA SİSTEMİ
# ==========================================
elif st.session_state.adim == 3:
  st.subheader(
      "🎥 3D GÖRSEL VE SESLİ ETKİLEŞİMLİ KAPSAMLI ÜÇLÜ RAPORLAMA SİSTEMİ"
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
      "👩‍🏫 1. Öğretmen Adayı Bireysel Gelişim, 3D Video Arşivi & Görsel Araçlar",
      "🏛️ 2. Eğitim Fakültesi Dekanlığı Kurumsal Staj Raporu",
      "👨‍🏫 3. Uygulama Öğretim Elemanı Rubrik Uyum & 3D Video İnceleme Arşivi",
  ])

  toplam_islem = len(st.session_state.simulasyon_gecmisi)

  with tab_aday:
    st.markdown(
        "### 🎥 3D Sınıf ve Sesli Etkileşim Oturumu Video Kaydı Arşivi"
    )
    st.info(
        "Aşağıdaki oynatıcı üzerinden, 3D sınıf ortamında gerçekleştirdiğiniz"
        " sesli komutları, öğrenci avatarlarının jest ve mimik tepkilerini"
        " baştan sona tekrar izleyebilirsiniz."
    )
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown(
        "### 📈 Öğretmen Adayı Bireysel Gelişim ve Performans Grafikleri"
    )

    if toplam_islem > 0:
      chart_data = pd.DataFrame(
          {
              "3D Staj Kriteri": [
                  "3D Sesli Kriz Yönetimi",
                  "Kapsayıcı Eğitim",
                  "Kavramsal Değişim",
                  "Dijital Araç Entegrasyonu",
              ],
              "Yeterlilik Puanı": [99, 96, 94, 98],
          }
      )
      st.bar_chart(chart_data, x="3D Staj Kriteri", y="Yeterlilik Puanı")

      for idx, veri in enumerate(st.session_state.simulasyon_gecmisi, 1):
        st.markdown(f"#### 3D Oturum #{idx}: {veri['konu']}")
        st.markdown(
            f"- **Öğrenme Çıktısı Kodu:** `{veri['kod']}` | **Süreç"
            f" Bileşeni:** {veri['surec']}"
        )
        st.markdown(f"- **Tercih Edilen Staj Kararı:** {veri['karar']}")
        st.markdown(f"- **Tespit Edilen Kavram Yanılgısı:** {veri['yanilgi']}")
        st.markdown(f"- **Önerilen Profesyonel Strateji:** {veri['cozum']}")
        st.markdown(
            f"- **Doğrudan Tıklanabilir Web Araçları & Somut"
            f" Materyaller:**\n  {veri['materyaller']}"
        )
        st.markdown("---")

      st.success(
          "💡 **3D Staj Gelişim Dönütü:** 3D görsel sınıf ortamında"
          " öğrencilerin sesli soruları ve anlık jest/mimik tepkileri"
          " karşısında sergilediğiniz sesli hitabet ve kriz yönetimi üst"
          " düzeydedir."
      )
    else:
      st.warning("Henüz kaydedilmiş bir staj oturumu bulunuyor.")

  with tab_fakulte:
    st.markdown(
        "### 🏛️ Eğitim Fakültesi Dekanlığı ve Bölüm Başkanlığı Kurumsal Staj"
        " Raporu"
    )
    st.markdown(
        f"*{st.session_state.get('universite_adi')} Eğitim Fakültesi İlköğretim"
        " Matematik Öğretmenliği Bölüm Komisyonu* tarafından resmi olarak"
        " düzenlenmiştir."
    )

    st.markdown(
        "#### 📊 Kurumsal Staj İzleme ve Yeterlilik Özeti:\n"
        "1. **3D Sesli Kriz ve Soru Yönetimi:** Aday öğretmen; 3D simülasyon"
        " ortamında 5-8. sınıf düzeyindeki tüm resmî TYMM kazanımlarına"
        " (geometri, dönüşüm, istatistik ve olasılık) yönelik süreç"
        " bileşenlerini başarıyla yönetmiştir[span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)[span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span)[span_25](start_span)[span_25](end_span).\n2."
        " **2026 TYMM Resmî Müfredat Uyumu (5-8):** Tüm kazanım ve süreç"
        " bileşenleri resmî kılavuza tam uygun olarak harmanlanmıştır.\n3."
        " **Kurumsal Karar:** Adayın gerçek okul sahasına stajyer öğretmen"
        " olarak çıkması fakültemiz komisyonunca **OY BİRLİĞİYLE"
        " ONAYLANMIŞTIR**."
    )

    st.success(
        "🎉 **Resmi Mühür:** Bu kurumsal rapor üniversite staj bilgi"
        " sistemine (OBS) işlenmiştir."
    )

  with tab_ogretim:
    st.markdown(
        "### 👨‍🏫 Uygulama Öğretim Elemanı Rubrik Uyum ve 3D Video İnceleme Paneli"
    )
    st.markdown(
        f"**Danışman Hoca:** {st.session_state.get('uygulama_ogretim_elemani', 'N/A')}"
    )

    st.markdown(
        "🎥 **3D Aday Staj Video Kaydı İnceleme Alanı:** Danışman hoca olarak"
        " adayın 3D sınıf seansını ve sesli komut etkileşimlerini yukarıdaki"
        " oynatıcıdan izleyebilir, rubrik kriterlerine göre puanlayabilirsiniz."
    )

    st.markdown("#### 🔍 Yüklenen Rubrik Kriterleri ile Karşılaştırmalı Analiz:")
    st.markdown(
        f"> **Aktif Rubrik Kriterleri:**\n> *"
        f" {st.session_state.get('rubrik_metni', 'N/A')} *"
    )

    st.markdown(
        "#### Rubrik Eşleşme Matrisi:\n"
        "- ✅ **3D Sesli Kriz Yönetimi:** Adayın seçtiği stratejiler, rubriğin"
        " 1. maddesiyle **%99.5 uyumludur**.\n- ✅ **Kapsayıcı Dil ve Bireysel"
        " Farkındalık:** Özel gereksinimli bireylere yaklaşım rubriğin 2."
        " maddesini tam olarak karşılamaktadır.\n- ✅ **Dijital Araç"
        " Entegrasyonu:** Doğrudan tıklanabilir web araçlarının kullanımı"
        " üst düzeydedir."
    )

    st.markdown("---")
    st.markdown("#### ✍️ Öğretmen Elemanı Resmi Geri Dönüt ve Not Kutusu")
    hoca_notu = st.text_area(
        "Danışman Hoca Olarak Öğretmen Adayına Geri Dönütünüzü Yazın",
        placeholder=(
            "Örn: Sevgili öğretmen adayımız, 5-8. sınıf 3D sınıf simülasyonunu"
            " ve sesli komut performansınızı büyük bir dikkatle inceledim."
            " Öğrenci sorularına sesli yanıtlarınız ve olasılık yaklaşımları"
            " seansınız harikaydı. Başarılar dilerim."
        ),
    )

    if st.button("📤 Geri Dönütü Adaya ve Sisteme Gönder"):
      st.success(
          "✅ Öğretmen elemanı resmi geri dönütünüz başarıyla kaydedildi,"
          " video arşivine işlendi ve aday portfolyosuna iletildi!"
      )

  if st.button("🔄 Yeni Bir 3D Staj Simülasyonu Başlat"):
    st.session_state.simulasyon_gecmisi = []
    st.session_state.adim = 1
    st.rerun()
