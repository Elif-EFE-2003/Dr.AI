# 🩺 Sağlık Destek Asistanı
Streamlit tabanlı bu uygulama, kullanıcıların diyabet ve menstrüel sağlık üzerine ön değerlendirme yapabilmesini sağlar. Kullanıcı dostu arayüzü, laboratuvar raporlarını otomatik okuma özelliği ve makine öğrenmesi modelleri ile kişisel sağlık desteği sunar.

⚠️ Not: Bu uygulama yalnızca ön değerlendirme amaçlıdır, kesin tanı yerine geçmez. Gerekli durumlarda mutlaka uzman bir hekime başvurunuz.

## ✨ Özellikler
Makine Öğrenmesi Modelleri

Diyabet riski için sınıflandırma modeli

Menstrüel sağlık problemleri için çok etiketli sınıflandırma modeli

Laboratuvar Belgesi Yükleme

PDF, CSV veya Excel dosyası yükleyerek laboratuvar sonuçlarının otomatik işlenmesi

Kan parametreleri (HbA1c, Hemoglobin, Ferritin, TSH, vb.) otomatik doldurulur

Soru-Cevap Akışı

Kullanıcıdan adım adım sorular alır

İlgili değerler laboratuvar belgesinden otomatik doldurulabilir

Yanıtlar işlendikten sonra kişiselleştirilmiş değerlendirme yapılır

Konum Desteği

Şehir ve ilçe girildiğinde, en yakın uzman doktoru bulmak için Google Maps ve MHRS linkleri oluşturur

Modern Arayüz

Özel CSS ile sade ve profesyonel görünüm

Adım göstergesi (stepper) ve sohbet benzeri arayüz

## 🚀 Kurulum
### 1. Depoyu Klonlayın
Bash

git clone https://github.com/kullaniciadi/saglik-destek-asistani.git
cd saglik-destek-asistani
### 2. Sanal Ortam Oluşturun ve Aktif Edin
Bash

python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate
### 3. Gereksinimleri Kurun
Bash

pip install -r requirements.txt
### 4. Modelleri Proje Dizinine Ekleyin
menstrual_model.pkl ve diabet_model.pkl dosyalarını proje ana dizinine yerleştirin. Eğer bu dosyalar yoksa, uygulama çalışırken hata verecektir.

### 5. Uygulamayı Başlatın
Bash

streamlit run app.py
## 🧠 Kullanılan Teknolojiler
Python 3.10+

Streamlit: Web arayüzü

scikit-learn: Makine öğrenmesi modelleri

pandas & numpy: Veri işleme

pdfplumber, pypdf: PDF işleme

## 📊 Örnek Kullanım
Başlangıç Ekranı: Uygulama açıldığında kullanıcıya iki seçenek sunulur: Diyabet veya Menstrüel Sağlık değerlendirmesi.

Laboratuvar Belgesi Yükleme: PDF, CSV veya XLSX formatında laboratuvar raporu yüklenerek otomatik değer tespiti yapılır: HbA1c, Glukoz, Kolesterol, Hemoglobin, Ferritin, TSH vb.

Soru-Cevap Akışı: Uygulama, kullanıcıya adım adım sorular yöneltir. Eksik bilgiler manuel olarak girilebilir. Laboratuvar değerleri varsa sorular otomatik atlanır.

Sonuçlar: Diyabet için risk değerlendirmesi ve menstrüel sağlık için çok etiketli değerlendirme (örn. menorrhagia, oligomenorrhea, vb.) sunulur.

## Uzman Yönlendirmeleri
Riskli durumlarda kullanıcıya yönlendirmeler yapılır:

Diyabet için: Endokrinoloji

Menstrüel sağlık için: Kadın Hastalıkları ve Doğum

Google Maps ve MHRS üzerinden randevu bağlantıları otomatik oluşturulur.

## Proje Yapısı
# 📦 saglik-destek-asistani
 ┣ 📜 app.py                # Ana uygulama
 ┣ 📜 requirements.txt      # Gerekli bağımlılıklar
 ┣ 📜 README.md             # Bu dosya
 ┣ 📜 diabet_model.pkl      # Diyabet modeli
 ┣ 📜 menstrual_model.pkl   # Menstrüal model
 ┗ 📂 data/                 # (Opsiyonel) Örnek CSV şablonları
