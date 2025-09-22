import streamlit as st
import joblib
import numpy as np
import time
import pandas as pd
import re

# --- PDF bağımlılıklarını esnek yükleme ---
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from pypdf import PdfReader  # yeni paket
except ImportError:
    try:
        from PyPDF2 import PdfReader  # eski paket
    except ImportError:
        PdfReader = None  # hiçbiri yoksa None

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Sağlık Destek Asistanı",
    page_icon="🩺",
    layout="wide"
)

# =========================
# GLOBAL CSS (Kurumsal/Profesyonel)
# =========================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root{
  --bg: #f7fafc;
  --panel: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --border: #e5e7eb;
}
html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }

/* Header */
.header{
  padding: 24px 24px 16px 24px;
  border-radius: 20px;
  background: linear-gradient(180deg,#ecfeff 0%, #f9fbfb 100%);
  border: 1px solid #d7f3f1;
}
.header h1{
  margin: 0;
  font-size: 1.9rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #065f5b;
}
.header p{ margin: 6px 0 0 0; color: var(--muted); }

/* Panel */
.panel{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
}

/* Stepper */
.stepper{ display:flex; align-items:center; gap:10px; flex-wrap: wrap; }
.step{
  display:flex; align-items:center; gap:8px;
  color: var(--muted); font-weight: 600;
}
.step .dot{
  width: 22px; height: 22px; border-radius: 999px;
  display:flex; align-items:center; justify-content:center;
  border:1px solid var(--border);
  background:#fff; font-size:12px; color:#4b5563;
}
.step.active{ color:#075e5a; }
.step.active .dot{ border-color:#9fe1df; background:#ecfffd; color:#075e5a; font-weight:800; }
.step.done{ color:#065f5b; }
.step.done .dot{ background:#0ea5a3; color:white; border-color:#0ea5a3; }

/* Chat */
.chat-wrap{ max-width: 880px; margin: 0 auto; }
.msg{
  border:1px solid var(--border); border-radius: 14px;
  padding: 12px 14px; margin: 6px 0; background: #fff;
}
.assistant .tag{ color:#075e5a; font-weight:700; }
.user .tag{ color:#0b4b49; font-weight:700; }

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown(
    """
    <div class="header">
      <h1>🩺 Sağlık Destek Asistanı</h1>
      <p>Bu uygulama ön değerlendirme amaçlıdır; tıbbi teşhis yerine geçmez. Şüphedeysen mutlaka hekime danış.</p>
    </div>
    """, unsafe_allow_html=True
)

# =========================
# Models
# =========================
@st.cache_resource
def load_models():
    models = {}
    try:
        with open('menstrual_model.pkl', 'rb') as f:
            models['menstrual'] = joblib.load(f)
        with open('diabet_model.pkl', 'rb') as f:
            models['diabet'] = joblib.load(f)
    except FileNotFoundError as e:
        st.error(f"Model dosyası bulunamadı: {e}. Lütfen 'menstrual_model.pkl' ve 'diabet_model.pkl' mevcut olsun.")
        return None
    except Exception as e:
        st.error(f"Model yüklenirken bir hata oluştu: {e}")
        return None
    return models

models = load_models()
if models is None:
    st.stop()

# =========================
# Questions & State
# =========================
QUESTIONS = {
    'diabet': [
        "Kan şekeri seviyeniz kaç mg/dL?",
        "HbA1c seviyeniz kaç? (Ör: 6.5)",
        "Kolesterol seviyeniz kaç mg/dL?",
        "Yaşınız kaç?",
        "Vücut Kitle İndeksiniz (BMI) kaç? (Ör: 25.4)",
        "Hipertansiyonunuz (yüksek tansiyon) var mı? ('evet' veya 'hayır')",
        "Kalp hastalığınız var mı? ('evet' veya 'hayır')",
        "Hemoglobin (hgb) seviyeniz kaç g/dL? (Ör: 14.2)",
        "Cinsiyetiniz nedir? ('erkek' veya 'kadın')",
        "Sigara kullanıyor musunuz? ('evet' veya 'hayır')"
    ],
    'menstrual': [
        "Yaşınız kaç?",
        "Vücut Kitle İndeksiniz (BMI) kaç?",
        "Hangi yaşam evresindesiniz? (Ergen, üreme, menopoz öncesi gibi)",
        "Adet dönemlerinizdeki ağrıyı 1-10 arası bir puanla değerlendirin. (1: yok, 10: çok şiddetli)",
        "Ortalama adet döngü uzunluğunuz kaç gün?",
        "Döngü uzunluğunuzda ne kadar varyasyon oluyor? (Örn: +/- 2 gün)",
        "Ortalama kanama gün sayınız kaç?",
        "Kanama miktarınızı 1-5 arası bir puanla değerlendirin. (1: az, 5: çok fazla)",
        "İki adet dönemi arasında lekelenme veya kanama oluyor mu? ('evet' veya 'hayır')",
        "Döngü varyasyon katsayınız kaç? (Eğer biliyorsanız, yoksa 0 girin)",
        "Adet döngünüzdeki düzensizlik veya bozulma puanınız kaç? (1-10 arası)",
        "Ailenizde kalıtsal bir hastalık geçmişi var mı? ('evet' veya 'hayır')",
        "Kişisel alkol kullanımınız var mı? ('evet' veya 'hayır')",
        "Uyku kalitenizi 1-5 arası bir puanla değerlendirin. (1: çok kötü, 5: çok iyi)",
        "Hemoglobin seviyeniz kaç g/dL?",
        "Ferritin seviyeniz kaç ng/mL?",
        "TSH seviyeniz kaç μIU/mL?",
        "Prolaktin seviyeniz kaç ng/mL?",
        "FSH/LH oranınız kaç?",
        "Rastgele kan glikoz seviyeniz kaç mg/dL?"
    ]
}

# Session state vars
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hangi konuda bilgi almak istersiniz? (Diabet, Menstrüal)"}]
if 'stage' not in st.session_state:
    st.session_state.stage = "select_topic"
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'lab_values' not in st.session_state:
    st.session_state.lab_values = {}
if "city" not in st.session_state:
    st.session_state.city = ""
if "district" not in st.session_state:
    st.session_state.district = ""
if 'last_prompted_index' not in st.session_state:
    st.session_state.last_prompted_index = -1

# =========================
# Lab Upload & Parsing
# =========================
LAB_FIELD_ALIASES = {
    # Menstrual & genel
    "hemoglobin g/dl": "hemoglobin_level",
    "hemoglobin": "hemoglobin_level",
    "hgb": "hemoglobin_level",
    "ferritin": "ferritin_level",
    "tsh": "tsh_level",
    "prolaktin": "prolactin_level", "prolactin": "prolactin_level",
    "fsh/lh": "fsh_lh_ratio", "fsh-lh": "fsh_lh_ratio", "fsh lh": "fsh_lh_ratio",
    "random glucose": "random_glucose", "glucose random": "random_glucose", "rastgele glikoz": "random_glucose",

    # Diabet (kan şekeri)
    "glukoz (açlık kan şekeri)": "blood_glucose_level",
    "glukoz (aclik kan sekeri)": "blood_glucose_level",
    "glukoz açlık": "blood_glucose_level",
    "glukoz aclik": "blood_glucose_level",
    "glukoz sekeri": "blood_glucose_level",
    "glukoz": "blood_glucose_level",
    "fasting plasma glucose": "blood_glucose_level",
    "açlık kan şekeri": "blood_glucose_level",
    "aclik kan sekeri": "blood_glucose_level",
    "akş": "blood_glucose_level", "aks": "blood_glucose_level",
    "fpg": "blood_glucose_level",
    "fasting blood glucose": "blood_glucose_level",
    "fasting blood sugar": "blood_glucose_level",
    "fasting glucose": "blood_glucose_level",
    "fbg": "blood_glucose_level", "fbs": "blood_glucose_level",
    "blood glucose": "blood_glucose_level",
    "kan şekeri": "blood_glucose_level", "kan sekeri": "blood_glucose_level",
    "glucose": "blood_glucose_level",

    # Kolesterol & HbA1c
    "cholesterol mg/dl": "cholesterol_mg_dL",
    "cholesterol": "cholesterol_mg_dL", "kolesterol": "cholesterol_mg_dL",
    "hba1c": "HbA1c_level", "hb a1c": "HbA1c_level",
}

NUM_REGEX = r"([-+]?\d+(?:[.,]\d+)?)"

def normalize_key(label: str) -> str:
    s = str(label).strip().lower()
    s = s.replace(":", " ").replace("=", " ").replace("(", " ").replace(")", " ")
    s = re.sub(r"\s+", " ", s)
    for k in sorted(LAB_FIELD_ALIASES.keys(), key=len, reverse=True):
        if k in s:
            return LAB_FIELD_ALIASES[k]
    if "glukoz" in s:
        return "blood_glucose_level"
    return ""

def normalize_num(x):
    if x is None:
        return None
    if not isinstance(x, str):
        try:
            return float(x)
        except Exception:
            return None
    s = x.strip().lower().replace(",", ".")
    m = re.search(NUM_REGEX, s)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None

def extract_text_from_pdf(file) -> str:
    if pdfplumber is not None:
        try:
            with pdfplumber.open(file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception:
            pass
    if PdfReader is not None:
        try:
            reader = PdfReader(file)
            text = ""
            for page in getattr(reader, "pages", []):
                text += page.extract_text() or ""
            return text
        except Exception:
            pass
    return ""

def extract_values_from_text(text: str) -> dict:
    vals = {}
    lower = text.lower()

    # Genel sayısal
    patterns = {
        "hemoglobin_level": r"(hemoglobin|hgb)[^\d\-+]*" + NUM_REGEX,
        "ferritin_level": r"(ferritin)[^\d\-+]*" + NUM_REGEX,
        "tsh_level": r"(tsh)[^\d\-+]*" + NUM_REGEX,
        "prolactin_level": r"(prolaktin|prolactin)[^\d\-+]*" + NUM_REGEX,
        "fsh_lh_ratio": r"(fsh\s*[/\-]?\s*lh)[^\d\-+]*" + NUM_REGEX,
        "random_glucose": r"(random\s+glucose|glucose\s+random|rastgele\s+glikoz)[^\d\-+]*" + NUM_REGEX,
        "HbA1c_level": r"(hba1c|hb\s*a1c)[^\d\-+]*" + NUM_REGEX,
        "blood_glucose_level": (
            r"(?:glucose|blood\s+glucose|kan\s+şekeri|kan\s+sekeri|"
            r"açlık\s+kan\s+şekeri|aclik\s+kan\s+sekeri|"
            r"fasting\s+(?:plasma\s+)?(?:blood\s+)?glucose|fasting\s+blood\s+sugar|"
            r"fbg|fbs|fpg|akş|aks|"
            r"glukoz(?:\s*açlık|\s*aclik)?|glukoz\s+kan\s+şekeri|glukoz\s+kan\s+sekeri)"
            r"[^\d\-+]*" + NUM_REGEX
        ),
        "cholesterol_mg_dL": r"(cholesterol|kolesterol)[^\d\-+]*" + NUM_REGEX,
    }
    for key, pat in patterns.items():
        m = re.search(pat, lower, re.IGNORECASE)
        if m:
            num = normalize_num(m.group(len(m.groups())))
            if num is not None:
                vals[key] = num

    return vals

# =========================
# Sidebar yardımcı: Değerleri yazdır
# =========================
def _render_detected_values(vals: dict):
    display_names = {
        "hemoglobin_level": "Hemoglobin (g/dL)",
        "ferritin_level": "Ferritin (ng/mL)",
        "tsh_level": "TSH (μIU/mL)",
        "prolactin_level": "Prolaktin (ng/mL)",
        "fsh_lh_ratio": "FSH/LH Oranı",
        "random_glucose": "Rastgele Glikoz (mg/dL)",
        "HbA1c_level": "HbA1c (%)",
        "blood_glucose_level": "Kan Şekeri (mg/dL)",
        "cholesterol_mg_dL": "Kolesterol (mg/dL)",
    }
    if not vals:
        return
    st.markdown("**Tespit edilen değerler:**")
    for k, v in vals.items():
        st.write(f"- {display_names.get(k, k)}: {v}")

# =========================
# Sidebar: Upload, Konum & Template
# =========================
with st.sidebar:
    st.markdown("### 📄 Laboratuvar Belgesi (opsiyonel)")
    uploaded = st.file_uploader("PDF, CSV veya XLSX yükleyin", type=["pdf", "csv", "xlsx"], accept_multiple_files=False)
    if uploaded is not None:
        try:
            ext = uploaded.name.lower().split(".")[-1]
            if ext == "csv":
                df = pd.read_csv(uploaded)
                # Beklenen iki kolon: Parameter, Value
                mapping = {}
                if df.shape[1] >= 2:
                    for lab, val in zip(df.iloc[:,0], df.iloc[:,1]):
                        key = normalize_key(lab)
                        if key:
                            mapping[key] = val
                st.session_state.lab_values = mapping
            elif ext == "xlsx":
                df = pd.read_excel(uploaded)
                mapping = {}
                if df.shape[1] >= 2:
                    for lab, val in zip(df.iloc[:,0], df.iloc[:,1]):
                        key = normalize_key(lab)
                        if key:
                            mapping[key] = val
                st.session_state.lab_values = mapping
            elif ext == "pdf":
                text = extract_text_from_pdf(uploaded)
                st.session_state.lab_values = extract_values_from_text(text)
            st.success("Belge işlendi ve değerler tespit edildi.")
        except Exception as e:
            st.error(f"Belge işlenirken hata: {e}")

    # Tespit edilen değerler
    if st.session_state.lab_values:
        _render_detected_values(st.session_state.lab_values)
    else:
        st.caption("Yüklü/ayrıştırılmış değer yok.")

    # Örnek CSV şablonu indir (yalnızca genel/kan parametreleri)
    template = pd.DataFrame({
        "Parameter": ["Hemoglobin", "Ferritin", "TSH", "Prolactin", "FSH/LH", "Random Glucose", "HbA1c", "Cholesterol"],
        "Value":     ["13.8",       "22",        "1.9",  "12",        "1.6",     "98",             "5.6",    "180"]
    })
    st.download_button("Örnek CSV Şablonu İndir", data=template.to_csv(index=False).encode("utf-8"),
                       file_name="lab_sablon.csv", mime="text/csv")

    # --- Konum ---
    st.markdown("### 📍 Konum")
    st.session_state.city = st.text_input("Şehir", value=st.session_state.city, placeholder="Örn: İstanbul")
    st.session_state.district = st.text_input("İlçe (opsiyonel)", value=st.session_state.district, placeholder="Örn: Kadıköy")

# =========================
# Helpers (preprocess + stepper + location)
# =========================
def preprocess_answers(answers, topic):
    if topic == 'diabet':
        processed = []
        for i in range(10):
            answer = answers[i]
            if i in [5, 6]:
                processed.append(1 if str(answer).lower().strip() in ['evet', 'evet.'] else 0)
            elif i == 8:  # gender
                processed.append(str(answer).lower().strip())
            elif i == 9:  # smoking
                processed.append('current' if str(answer).lower().strip() in ['evet', 'evet.'] else 'no')
            else:
                try:
                    processed.append(float(answer))
                except ValueError:
                    st.warning(f"'{answer}' anlaşılamadı, 0 kabul edildi.")
                    processed.append(0)
        column_names = [
            'blood_glucose_level', 'HbA1c_level', 'cholesterol_mg_dL', 'age', 'bmi',
            'hypertension', 'heart_disease', 'hemoglobin_g_dL', 'gender', 'smoking_history'
        ]
        return pd.DataFrame([processed], columns=column_names)

    elif topic == 'menstrual':
        column_names = [
            'age','bmi','life_stage','pain_score','avg_cycle_length','cycle_length_variation',
            'avg_bleeding_days','bleeding_volume_score','intermenstrual_episodes','cycle_variation_coeff',
            'pattern_disruption_score','family_history','alcohol_use','sleep_quality','hemoglobin_level',
            'ferritin_level','tsh_level','prolactin_level','fsh_lh_ratio','random_glucose'
        ]
        processed_answers = []
        for i, answer in enumerate(answers):
            a = str(answer).lower().strip()
            if i in [8, 11, 12]:  # yes/no fields
                processed_answers.append(1 if a in ['evet', 'evet.'] else 0)
            else:
                try:
                    processed_answers.append(float(answer))
                except ValueError:
                    if i == 2:  # life_stage text
                        processed_answers.append(str(answer).strip())
                    else:
                        st.warning(f"'{answer}' anlaşılamadı, 0 kabul edildi.")
                        processed_answers.append(0)
        return pd.DataFrame([processed_answers], columns=column_names)

    else:
        processed = []
        for answer in answers:
            a = str(answer).lower().strip()
            if a in ['evet','evet.','evet!']:
                processed.append(1)
            elif a in ['hayır','hayır.','hayır!','hayir','hayir.']:
                processed.append(0)
            else:
                try:
                    processed.append(float(answer))
                except ValueError:
                    st.warning(f"'{answer}' anlaşılamadı, 0 kabul edildi.")
                    processed.append(0)
        return np.array(processed).reshape(1, -1)

def stepper_ui(topic, index):
    if topic is None:
        return
    total = len(QUESTIONS[topic])
    items = []
    for i in range(total):
        cls = "step"
        if i < index: cls += " done"
        elif i == index: cls += " active"
        items.append(f'<div class="{cls}"><div class="dot">{i+1}</div><div>{topic.title()}</div></div>')
    html = f'<div class="panel"><div class="stepper">{"".join(items)}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

def build_location_query():
    city = (st.session_state.city or "").strip()
    district = (st.session_state.district or "").strip()
    if city and district:
        return f"{district} {city}"
    return city

def specialist_links(specialty_tr: str):
    loc = build_location_query()
    q = f"{specialty_tr} {loc}" if loc else specialty_tr
    maps_url = f"https://www.google.com/maps/search/{q.replace(' ', '+')}"
    mhrs_url = "https://www.mhrs.gov.tr/vatandas/#/"
    return maps_url, mhrs_url

# =========================
# Prefill/Skip from lab_values
# =========================
def prefill_or_skip(q_idx, topic):
    if topic == "menstrual":
        mapping = {
            14: "hemoglobin_level",
            15: "ferritin_level",
            16: "tsh_level",
            17: "prolactin_level",
            18: "fsh_lh_ratio",
            19: "random_glucose",
        }
    elif topic == "diabet":
        mapping = {
            0: "blood_glucose_level",
            1: "HbA1c_level",
            2: "cholesterol_mg_dL",
            7: ["hemoglobin_g_dL", "hemoglobin_level"],
        }
    else:
        mapping = {}

    if q_idx in mapping:
        keys = mapping[q_idx] if isinstance(mapping[q_idx], list) else [mapping[q_idx]]
        for key in keys:
            if key in st.session_state.lab_values:
                val = st.session_state.lab_values[key]
                st.session_state.answers.append(str(val))
                st.session_state.question_index += 1
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Otomatik tespit: **{key} = {val}** (soru atlandı)"
                })
                return True
    return False

def auto_advance_from_lab():
    topic = st.session_state.current_topic
    if topic is None:
        return False
    qlist = QUESTIONS[topic]
    while st.session_state.question_index < len(qlist):
        if not prefill_or_skip(st.session_state.question_index, topic):
            break
    return st.session_state.question_index >= len(qlist)

# =========================
# Sidebar: Status & Tips
# =========================
with st.sidebar:
    st.markdown("### 🔧 Sistem Durumu")
    loaded_list = []
    for k in ['diabet', 'menstrual']:
        if k in models:
            loaded_list.append(f"• {k.title()}")
    st.markdown(f"""<div class="panel"><div>🧠 Yüklü Modeller</div>
    <div style="margin-top:6px; font-weight:700; color:#065f5b;">{'<br>'.join(loaded_list) if loaded_list else '—'}</div></div>""", unsafe_allow_html=True)
    st.markdown("### 💡 İpuçları")
    st.markdown("- Laboratuvar belgesi yüklersen ilgili sorular **otomatik doldurulur**.\n- Sonuçlar **ön değerlendirme** niteliğindedir.\n- Gerekirse doktorunuza başvurun.")

# =========================
# Quick Start Buttons (Konu seçimi)
# =========================
st.markdown('<div class="panel">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1])
with c1:
    if st.button("🧪 Diabet", use_container_width=True):
        st.session_state.current_topic = "diabet"
        st.session_state.stage = "ask_questions"
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.last_prompted_index = -1
        all_prefilled = auto_advance_from_lab()
        if all_prefilled:
            st.session_state.messages.append({"role":"assistant","content":"Tüm ilgili değerler lab belgesinden alındı. Değerlendiriyorum…"})
        else:
            st.session_state.messages.append({"role":"assistant","content":"Harika, **Diabet** ile başlayalım."})

with c2:
    if st.button("🩸 Menstrüal", use_container_width=True):
        st.session_state.current_topic = "menstrual"
        st.session_state.stage = "ask_questions"
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.last_prompted_index = -1
        all_prefilled = auto_advance_from_lab()
        if all_prefilled:
            st.session_state.messages.append({"role":"assistant","content":"Tüm ilgili değerler lab belgesinden alındı. Değerlendiriyorum…"})
        else:
            st.session_state.messages.append({"role":"assistant","content":"Harika, **Menstrüal** ile başlayalım."})
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Stepper + Progress (yalnızca konu seçildiyse)
# =========================
def stepper_ui(topic, index):
    if topic is None:
        return
    total = len(QUESTIONS[topic])
    items = []
    for i in range(total):
        cls = "step"
        if i < index: cls += " done"
        elif i == index: cls += " active"
        items.append(f'<div class="{cls}"><div class="dot">{i+1}</div><div>{topic.title()}</div></div>')
    html = f'<div class="panel"><div class="stepper">{"".join(items)}</div></div>'
    st.markdown(html, unsafe_allow_html=True)

if st.session_state.current_topic is not None:
    stepper_ui(st.session_state.current_topic, st.session_state.question_index)
    total_q = len(QUESTIONS[st.session_state.current_topic])
    st.progress((st.session_state.question_index / total_q) if total_q else 0.0)

# ====================================================
# CHAT INPUT: SADECE SORU AŞAMASINDA
# ====================================================
prompt = None
if st.session_state.stage == "ask_questions":
    if not auto_advance_from_lab():
        prompt = st.chat_input("Cevabınızı yazın…")

# ====================================================
# LOGIC
# ====================================================
# 1) Kullanıcı cevabı işlensin
if prompt and st.session_state.stage == "ask_questions":
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.answers.append(prompt)
    st.session_state.question_index += 1

# 2) Sıradaki soru / sonuç
if st.session_state.stage == "ask_questions":
    topic = st.session_state.current_topic
    qlist = QUESTIONS[topic]
    auto_advance_from_lab()

    if st.session_state.question_index < len(qlist) and st.session_state.last_prompted_index != st.session_state.question_index:
        next_q = qlist[st.session_state.question_index]
        st.session_state.messages.append({
            "role":"assistant",
            "content": f"{st.session_state.question_index + 1}. {next_q}"
        })
        st.session_state.last_prompted_index = st.session_state.question_index

    elif st.session_state.question_index >= len(qlist):
        st.session_state.messages.append({"role":"assistant","content": "Teşekkür ederim. Cevaplarınızı değerlendiriyorum…"})
        try:
            model = models.get(topic)
            if model is None:
                raise RuntimeError("Seçilen konu için model yüklü değil.")
            processed = preprocess_answers(st.session_state.answers, topic)
            time.sleep(0.2)
            prediction = model.predict(processed)[0]

            if topic == 'menstrual':
                target_pairs = [
                    ('duration_abnormality_flag', "Adet süresinde düzensizlik",
                     "Adet süresi normalden kısa/uzun olabilir. Hormonal değişiklikler, tiroid bozuklukları veya stres etkili olabilir."),
                    ('oligomenorrhea', "Oligomenorrhea (seyrek adet)",
                     "Döngüler 35 günden uzun aralıklarla gelebilir. PCOS veya kilo değişiklikleriyle ilişkili olabilir."),
                    ('polymenorrhea', "Polymenorrhea (sık adet)",
                     "Döngüler 21 günden kısa aralıklarla gelebilir. Ovulasyon problemleri veya hormonal dengesizlik görülebilir."),
                    ('menorrhagia', "Menorrhagia (aşırı kanama)",
                     "Ped/tampon değişim ihtiyacı artar, pıhtı olabilir. Demir eksikliği riski doğurabilir."),
                    ('amenorrhea', "Amenorrhea (adet görememe)",
                     "3+ ay adet olmaması durumudur. Gebelik, kilo/stres, tiroid veya prolaktin değişiklikleriyle ilişkili olabilir."),
                    ('intermenstrual', "İntermenstrüel kanama (ara kanama)",
                     "Dönemler arasında lekelenme/kanama görülebilir. Hormonal nedenler veya rahim ağzı kaynaklı durumlar incelenmelidir.")
                ]
                results_text = "**Menstrüal Sağlık Değerlendirmesi:**\n\n"
                is_risky = False
                for i, (key, label, expl) in enumerate(target_pairs):
                    flag = int(prediction[i]) == 1
                    results_text += f"- **{label}:** {'Var' if flag else 'Yok'}"
                    if flag:
                        results_text += f" → {expl}"
                        is_risky = True
                    results_text += "\n"

                if is_risky:
                    final_response = (
                        f"{results_text}\n"
                        f"**Ne yapabilirim?**\n"
                        f"- Semptom günlüğü tutun (tarih, şiddet, kanama miktarı).\n"
                        f"- Demir eksikliği açısından hemogram/ferritin takibi yaptırın.\n"
                        f"- Uygun bir **Kadın Hastalıkları ve Doğum** uzmanına değerlendirme için başvurun.\n"
                        f"_Bu değerlendirme ön bilgi amaçlıdır, kesin tanı değildir._"
                    )
                else:
                    final_response = (
                        f"{results_text}\n"
                        f"**Genel öneriler:**\n"
                        f"- Düzenli takip yapın; önemli değişiklik olursa hekime danışın.\n"
                        f"- Stres, uyku ve beslenme düzeni döngüyü etkileyebilir.\n"
                        f"_Bu değerlendirme ön bilgi amaçlıdır, kesin tanı değildir._"
                    )

            elif topic == 'diabet':
                risky = (int(prediction) == 1)
                if risky:
                    final_response = (
                        "**Diyabet Değerlendirmesi:**\n\n"
                        "- Model, verdiğiniz değerlere göre **diyabet açısından anlamlı risk** olabileceğini gösteriyor.\n"
                        "- Bu; kan şekeri regülasyonunda bozulma, insülin direnci veya diyabetle uyumlu bir tabloya işaret edebilir.\n"
                        "- Tek başına tanı koymaz; doğrulama için **açlık/tokluk glukoz** ve **HbA1c** gibi testlerinizi hekiminizle gözden geçirin.\n\n"
                        "**Ne yapabilirim?**\n"
                        "- Rafine karbonhidratı azaltın, lif ve protein dengesini artırın.\n"
                        "- Haftalık orta yoğunlukta egzersiz (150 dk) hedefleyin.\n"
                        "- Kilo yönetimi ve düzenli uykuyu gözden geçirin.\n"
                        "- Bir **Endokrinoloji** uzmanıyla görüşün.\n"
                        "_Bu değerlendirme ön bilgi amaçlıdır, kesin tanı değildir._"
                    )
                else:
                    final_response = (
                        "**Diyabet Değerlendirmesi:**\n\n"
                        "- Mevcut yanıtlara göre **acil risk bulgusu yok**.\n"
                        "- Yine de semptomlarınız olursa (aşırı susama, sık idrara çıkma, kilo değişimi vb.) testlerinizi tekrarlayın.\n\n"
                        "**Genel öneriler:**\n"
                        "- Dengeli beslenme ve düzenli fiziksel aktiviteyi sürdürün.\n"
                        "- Yıllık kontrol ve gerektiğinde HbA1c ölçümü yaptırın.\n"
                        "_Bu değerlendirme ön bilgi amaçlıdır, kesin tanı değildir._"
                    )
            else:
                final_response = "Değerlendirme tamamlandı."

            # --- konuma bağlı uzman linkleri ---
            show_links = False
            spec_tr = None
            if topic == 'menstrual':
                if 'is_risky' in locals() and is_risky:
                    spec_tr = "Kadın Hastalıkları ve Doğum"; show_links = True
            elif topic == 'diabet':
                if (int(prediction) == 1):
                    spec_tr = "Endokrinoloji"; show_links = True

            if show_links:
                maps_url, mhrs_url = specialist_links(spec_tr)
                loc_hint = "" if build_location_query() else (
                    "\n\n> 🔎 **İpucu:** Sidebar’daki **Şehir** ve **İlçe** alanlarını doldurursanız, harita araması doğrudan bölgenize göre açılır."
                )
                final_response += (
                    f"\n\n---\n"
                    f"### 📍 Yakınında **{spec_tr}** bul\n"
                    f"- [Google Haritalar’da ara]({maps_url})\n"
                    f"- [MHRS’den randevu al]({mhrs_url})"
                    f"{loc_hint}"
                )

            st.session_state.messages.append({"role":"assistant","content": final_response})
            st.session_state.messages.append({"role":"assistant","content": "Başka bir konuda yardımcı olabilir miyim? (Diabet, Menstrüal)"})

            # Flow reset
            st.session_state.stage = "select_topic"
            st.session_state.current_topic = None
            st.session_state.question_index = 0
            st.session_state.answers = []

        except Exception as e:
            st.session_state.messages.append({"role":"assistant","content": f"Tahmin yapılırken bir hata oluştu: {e}"})
            st.session_state.stage = "select_topic"

# ====================================================
# MESAJ GEÇMİŞİ
# ====================================================
st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    role = message["role"]; content = message["content"]
    css_class = "assistant" if role == "assistant" else "user"
    st.markdown(
        f"""
        <div class="msg {css_class}">
          <div class="tag">{'Asistan' if role=='assistant' else 'Siz'}</div>
          <div style="margin-top:6px;">{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)
