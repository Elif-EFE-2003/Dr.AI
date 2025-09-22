# Dr.AI – AI Destekli Sağlık Simülasyonu

#🩺 Sağlık Destek Asistanı

Sağlık Destek Asistanı, bireylerin temel sağlık verilerini girerek veya laboratuvar belgelerini yükleyerek ön değerlendirme yapmasını sağlayan, yapay zekâ destekli bir Streamlit web uygulamasıdır.
Bu sistem, özellikle Diyabet ve Menstrüal Sağlık konularında farkındalık yaratmayı amaçlar.
⚠️ Tıbbi teşhis yerine geçmez. Sadece eğitim ve yönlendirme amacı taşır.

#📖 İçindekiler

Özellikler

Mimari ve Çalışma Prensibi

Proje Yapısı

Kurulum ve Çalıştırma

Kullanım Senaryosu

Laboratuvar Dosyası İşleme

Örnek Çıktılar

Teknolojiler

Geliştirme ve Katkı

Uyarı

#✨ Özellikler

Çoklu Konu Desteği

🔹 Diyabet değerlendirmesi: Kan şekeri, HbA1c, kolesterol, BMI, hipertansiyon, sigara öyküsü vb.

🔹 Menstrüal sağlık değerlendirmesi: Döngü uzunluğu, kanama miktarı, ağrı düzeyi, hormon değerleri vb.

Laboratuvar Belgesi Yükleme

PDF, CSV veya XLSX formatlarını destekler

Belgelerden değerleri otomatik çıkarır (ör. Hemoglobin, Ferritin, HbA1c, TSH, vb.)

Uygulamadaki soruları otomatik doldurur ve hızlandırır

Sohbet Tabanlı Arayüz

Sorular asistan tarafından sırayla yöneltilir

Kullanıcı cevap verir, sistem ilerlemeyi stepper ile gösterir

Sohbet geçmişi kullanıcıya şeffaf şekilde yansıtılır

Model Tabanlı Tahmin

diabet_model.pkl ve menstrual_model.pkl dosyaları ile scikit-learn tabanlı tahmin

Diyabet için risk sınıflandırması (var/yok)

Menstrüal sağlık için çoklu etiketli sınıflandırma (ör. Oligomenore, Menorrhagia vb.)

Kişisel Öneriler & Yönlendirme

Risk bulunduğunda → yaşam tarzı önerileri + ilgili uzman (Endokrinoloji, Kadın Doğum)

Google Maps ve MHRS entegrasyonu ile yakındaki doktor/klinik arama desteği

Modern Arayüz

Inter fontu

Responsive CSS düzeni

Kurumsal ve profesyonel görünüm

#🏗 Mimari ve Çalışma Prensibi

Kullanıcı Etkileşimi

Başlangıçta konu seçimi: Diyabet veya Menstrüal

Sorular, sohbet ekranında adım adım sorulur

Kullanıcı cevaplar girer veya laboratuvar dosyası yükler

Veri Ön İşleme (Preprocessing)

Cevaplar numeric/categorical forma dönüştürülür

Modelin beklediği kolon isimleri ile DataFrame oluşturulur

Model Tahmini

İlgili pickle modeli (joblib.load) çağrılır

.predict() çalıştırılır → risk sınıfları elde edilir

#Sonuç & Öneriler

Menstrüal: Çoklu etiket raporu (ör. “Polymenorrhea: Var → hormonal dengesizlik olabilir”)

Diyabet: Risk var/yok, öneriler listesi

Uzman yönlendirmesi: Google Maps + MHRS linkleri

Kayıtlı Sohbet

Mesajlar st.session_state.messages listesinde saklanır

Kullanıcı geçmişi ekranın altında gösterilir

#📂 Proje Yapısı
.
├── app.py                # Ana Streamlit uygulaması
├── requirements.txt      # Bağımlılıklar
├── diabet_model.pkl      # Diyabet modeli
├── menstrual_model.pkl   # Menstrüal sağlık modeli
├── lab_sablon.csv        # Örnek CSV şablonu
└── README.md             # Bu dosya

#⚙️ Kurulum ve Çalıştırma
1) Depoyu klonla
git clone <repo-url>
cd saglik-destek-asistani

2) Sanal ortam oluştur
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

3) Bağımlılıkları yükle
pip install -r requirements.txt

4) Uygulamayı çalıştır
streamlit run app.py

5) Tarayıcıda aç

👉 http://localhost:8501

#🧪 Kullanım Senaryosu

Kullanıcı uygulamayı açar → “Diyabet” veya “Menstrüal” seçer

Sorular sohbet ekranında sırasıyla gelir

Kullanıcı cevap girer veya PDF/CSV/XLSX laboratuvar raporunu yükler

Sistem otomatik doldurulan sorularla ilerler

Model tahmini yapılır → risk raporu hazırlanır

Kullanıcıya yaşam tarzı önerileri + uzman yönlendirme linkleri verilir

#📄 Laboratuvar Dosyası İşleme

Desteklenen formatlar: PDF, CSV, XLSX

Otomatik çıkarılan parametreler:

Hemoglobin, Ferritin, TSH, Prolaktin, FSH/LH

Random Glucose, HbA1c, Kolesterol

Kan şekeri (açlık/tokluk)

Örnek CSV şablonu:

Parameter	Value
Hemoglobin	13.8
Ferritin	22
TSH	1.9
Prolactin	12
FSH/LH	1.6
Random Glucose	98
HbA1c	5.6
Cholesterol	180
#📊 Örnek Çıktılar
Diyabet Değerlendirmesi
- Model, verdiğiniz değerlere göre diyabet açısından anlamlı risk olabileceğini gösteriyor.
- Rafine karbonhidratı azaltın, düzenli egzersiz yapın.
- Endokrinoloji uzmanına başvurun.

Menstrüal Sağlık Değerlendirmesi
- Oligomenorrhea: Var → PCOS veya kilo değişiklikleri ile ilişkili olabilir.
- Menorrhagia: Yok
- Amenorrhea: Yok
...
Öneri: Kadın Doğum uzmanına başvurun.

#🛠 Teknolojiler

Python 3.10+

Streamlit
 → Web arayüzü

scikit-learn
 → ML modelleri

pandas
 → Veri işleme

numpy
 → Matematiksel işlemler

pdfplumber
 & pypdf
 → PDF işleme

#👩‍💻 Geliştirme ve Katkı

Yeni sağlık alanları eklenebilir (ör. Hipertansiyon, Anemi vb.)

UI/UX geliştirmeleri yapılabilir (mobil uyum, temalar)

Docker veya Hugging Face Spaces ile deploy seçenekleri eklenebilir

Katkıda bulunmak isteyenler:

Fork edin

Branch oluşturun (feature/xyz)

Commit + PR gönderin

#🔒 Uyarı

Bu uygulama:

✅ Eğitim ve farkındalık amacı taşır

❌ Kesin tıbbi teşhis koymaz

⚠️ Belirtileriniz varsa mutlaka doktora başvurun

📌 Sağlık bir yolculuktur. Bu uygulama sadece yol göstericidir.

---

© 2025 – DreamCoders
