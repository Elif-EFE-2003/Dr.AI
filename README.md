# 🩺 Sağlık Destek Asistanı

Streamlit tabanlı bu uygulama, kullanıcıların **diyabet** ve **menstrüel sağlık** üzerine ön değerlendirme yapabilmesini sağlar.  
Kullanıcı dostu arayüzü, laboratuvar raporlarını otomatik okuma özelliği ve makine öğrenmesi modelleri ile kişisel sağlık desteği sunar.  

⚠️ **Not:** Bu uygulama yalnızca **ön değerlendirme** amaçlıdır, **kesin tanı yerine geçmez**. Gerekli durumlarda mutlaka uzman bir hekime başvurunuz.

---

## ✨ Özellikler

- 📊 **Makine Öğrenmesi Modelleri**
  - Diyabet riski için sınıflandırma modeli
  - Menstrüel sağlık problemleri için çok etiketli sınıflandırma modeli

- 📄 **Laboratuvar Belgesi Yükleme**
  - PDF, CSV veya Excel dosyası yükleyerek laboratuvar sonuçlarının otomatik işlenmesi
  - Kan parametreleri (HbA1c, Hemoglobin, Ferritin, TSH, vb.) otomatik doldurulur

- 💬 **Soru-Cevap Akışı**
  - Kullanıcıdan adım adım sorular alır
  - İlgili değerler laboratuvar belgesinden otomatik doldurulabilir
  - Yanıtlar işlendikten sonra kişiselleştirilmiş değerlendirme yapılır

- 📍 **Konum Desteği**
  - Şehir ve ilçe girildiğinde, en yakın uzman doktoru bulmak için Google Maps ve MHRS linkleri oluşturur

- 🎨 **Modern Arayüz**
  - Özel CSS ile sade ve profesyonel görünüm
  - Adım göstergesi (stepper) ve sohbet benzeri arayüz

---

## 🚀 Kurulum

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/kullaniciadi/saglik-destek-asistani.git
cd saglik-destek-asistani
### 2.Sanal Ortam Oluşturun ve Aktif Edin
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
### 3.Gereksinimleri Kurun
pip install -r requirements.txt
### 4. Modelleri Proje Dizininize Ekleyin
menstrual_model.pkl

diabet_model.pkl

Eğer bu dosyalar yoksa, uygulama çalışırken hata verecektir.
### 5. Uygulamayı Başlatın
streamlit run app.py
## 🧠 Kullanılan Teknolojiler
Python 3.10+

Streamlit
 → Web arayüzü

scikit-learn
 → Makine öğrenmesi modelleri

pandas
 & numpy
 → Veri işleme

pdfplumber
, pypdf
 → PDF işleme
## 📊 Örnek Kullanım
1. Başlangıç Ekranı

Uygulama açıldığında kullanıcıya iki seçenek sunulur:

Diyabet değerlendirmesi

Menstrüal sağlık değerlendirmesi

2. Laboratuvar Belgesi Yükleme

PDF, CSV veya XLSX formatında laboratuvar raporu yüklenir

Otomatik değer tespiti yapılır:

HbA1c, Glukoz, Kolesterol, Hemoglobin, Ferritin, TSH vb.

3. Soru-Cevap Akışı

Uygulama, kullanıcıya adım adım sorular yöneltir

Eksik bilgiler manuel olarak girilebilir

Laboratuvar değerleri varsa sorular otomatik atlanır

4. Sonuçlar

Diyabet için risk değerlendirmesi

Menstrüal sağlık için çok etiketli değerlendirme (ör. menorrhagia, oligomenorrhea, vb.)

Öneriler ve gerektiğinde uzman yönlendirmeleri
## Uzman Yönlendirmeleri
Riskli durumlarda kullanıcıya yönlendirmeler yapılır:

Diyabet için: Endokrinoloji

Menstrüal sağlık için: Kadın Hastalıkları ve Doğum

Google Maps ve MHRS üzerinden randevu bağlantıları otomatik oluşturulur.
## Proje Yapısı
📦 saglik-destek-asistani
 ┣ 📜 app.py               # Ana uygulama
 ┣ 📜 requirements.txt     # Gerekli bağımlılıklar
 ┣ 📜 README.md            # Bu dosya
 ┣ 📜 diabet_model.pkl     # Diyabet modeli
 ┣ 📜 menstrual_model.pkl  # Menstrüal model
 ┗ 📂 data/                # (Opsiyonel) Örnek CSV şablonları

