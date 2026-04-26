import streamlit as st

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #080c14 !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer { display: none !important; }
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Hide default file uploader label */
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] { margin: 0 !important; }

/* File uploader drop zone */
[data-testid="stFileUploadDropzone"] {
    background-color: rgba(13,22,38,0.6) !important;
    border: 2px dashed rgba(59,130,246,0.45) !important;
    border-radius: 12px !important;
    min-height: 120px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(59,130,246,0.85) !important;
    background-color: rgba(59,130,246,0.06) !important;
}

/* Analyze button */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.7rem 2rem !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.35) !important;
    transition: all 0.2s !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #60a5fa) !important;
    box-shadow: 0 6px 28px rgba(59,130,246,0.55) !important;
}

/* Video player — small and contained */
div[data-testid="stVideo"] {
    max-width: 100% !important;
}
div[data-testid="stVideo"] video {
    border-radius: 10px !important;
    max-height: 220px !important;
    width: 100% !important;
    object-fit: cover !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}

[data-testid="stSpinner"] { color: #3b82f6 !important; }

/* ── COMPONENTS ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 3.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    background: rgba(8,12,20,0.97);
}
.nav-logo { display: flex; align-items: center; gap: 10px; }
.nav-logo-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
}
.nav-logo-text { font-size: 17px; font-weight: 700; color: #fff; letter-spacing: -0.02em; }
.nav-links { display: flex; align-items: center; gap: 2rem; }
.nav-link { font-size: 13.5px; color: #64748b; font-weight: 500; }
.nav-badge {
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.28);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #60a5fa;
    font-weight: 600;
}

.hero {
    display: flex;
    align-items: flex-start;
    gap: 3rem;
    padding: 4rem 3.5rem 3rem;
    max-width: 1400px;
    margin: 0 auto;
}
.hero-left { flex: 1; padding-top: 0.5rem; }
.hero-tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 20px; padding: 5px 13px;
    font-size: 11px; color: #60a5fa; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.3rem;
}
.hero-title {
    font-size: 46px; font-weight: 800; color: #fff;
    line-height: 1.1; letter-spacing: -0.03em; margin-bottom: 1.1rem;
}
.hero-title span { color: #3b82f6; }
.hero-desc {
    font-size: 15px; color: #94a3b8; line-height: 1.75;
    margin-bottom: 2rem; max-width: 480px;
}
.features-list { display: flex; flex-direction: column; gap: 11px; }
.feature-item {
    display: flex; align-items: center; gap: 10px;
    font-size: 14px; color: #cbd5e1; font-weight: 500;
}
.feature-dot {
    width: 7px; height: 7px;
    background: #3b82f6; border-radius: 50%; flex-shrink: 0;
}

/* Upload panel on the right */
.upload-panel-wrap { flex: 0 0 460px; }
.upload-panel {
    background: rgba(13,22,38,0.92);
    border: 1px solid rgba(59,130,246,0.18);
    border-radius: 18px;
    padding: 1.6rem 1.6rem 1.2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}
.panel-title {
    font-size: 14px; font-weight: 700; color: #3b82f6;
    text-align: center; margin-bottom: 3px;
}
.panel-sub {
    font-size: 12px; color: #475569;
    text-align: center; margin-bottom: 1rem;
}
.trusted-row {
    display: flex; align-items: center; justify-content: center;
    gap: 1rem; margin-top: 1rem; padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.04); flex-wrap: wrap;
}
.trusted-label { font-size: 11px; color: #334155; font-weight: 600; }
.trusted-item {
    display: flex; align-items: center; gap: 4px;
    font-size: 11px; color: #475569; font-weight: 500;
}
.trusted-check { color: #22c55e; }

/* Result */
.result-wrap { max-width: 1400px; margin: 0 auto; padding: 0 3.5rem 4rem; }
.result-card {
    background: rgba(13,22,38,0.9);
    border: 1px solid rgba(59,130,246,0.14);
    border-radius: 18px; padding: 2rem 2.5rem;
}
.result-header {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 1.4rem;
}
.result-badge {
    display: inline-flex; align-items: center; gap: 10px;
    padding: 10px 22px; border-radius: 50px;
    font-size: 17px; font-weight: 700;
}
.result-conf { font-size: 38px; font-weight: 800; }
.result-conf-label { font-size: 12px; color: #475569; font-weight: 500; text-align: right; }
.divider { height: 1px; background: rgba(255,255,255,0.04); margin: 1.1rem 0; }
.section-label {
    font-size: 10px; font-weight: 700; color: #334155;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;
}
.class-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.class-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px; padding: 13px 15px;
}
.class-card-top {
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 9px;
}
.class-card-name {
    display: flex; align-items: center; gap: 8px;
    font-size: 13px; color: #94a3b8; font-weight: 600;
}
.class-card-dot { width: 8px; height: 8px; border-radius: 50%; }
.class-bar-track {
    height: 6px; background: rgba(255,255,255,0.05);
    border-radius: 3px; overflow: hidden;
}
.class-bar-fill { height: 100%; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


def render_navbar(device_label):
    st.markdown(f"""
<div class="navbar">
  <div class="nav-logo">
    <div class="nav-logo-icon">
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="7.5" stroke="white" stroke-width="1.8"/>
        <circle cx="10" cy="10" r="2.8" fill="white"/>
        <line x1="10" y1="2.5" x2="10" y2="5.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
        <line x1="10" y1="14.5" x2="10" y2="17.5" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
        <line x1="2.5" y1="10" x2="5.5" y2="10" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
        <line x1="14.5" y1="10" x2="17.5" y2="10" stroke="white" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
    </div>
    <span class="nav-logo-text">MMDFD</span>
  </div>
  <div class="nav-links">
    <span class="nav-link">How it works</span>
    <span class="nav-link">About</span>
    <span class="nav-link">Karunya Institute</span>
  </div>
  <div class="nav-badge">◉ &nbsp;{device_label} &nbsp;|&nbsp; B.Sc. Final Year Project</div>
</div>
""", unsafe_allow_html=True)


def render_hero_left():
    st.markdown("""
<div class="hero-left">
  <div class="hero-tag">◈ &nbsp; AI-Powered Detection</div>
  <div class="hero-title">
    Deepfake Detector<br>for <span>Videos &amp; Audio</span>
  </div>
  <div class="hero-desc">
    Detect AI-generated deepfakes, face-swapped videos, and voice-cloned media
    using advanced multimodal deep learning. Analyzes both visual frames
    and audio signals together for accurate source attribution.
  </div>
  <div class="features-list">
    <div class="feature-item"><div class="feature-dot"></div>Multimodal Video + Audio Analysis</div>
    <div class="feature-item"><div class="feature-dot"></div>Real-time Deepfake Source Classification</div>
    <div class="feature-item"><div class="feature-dot"></div>Detects FaceSwap, Wav2Lip &amp; VoiceClone</div>
    <div class="feature-item"><div class="feature-dot"></div>Confidence Score &amp; Class Probabilities</div>
    <div class="feature-item"><div class="feature-dot"></div>Vision Transformer + CNN Audio Encoder</div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_panel_top():
    st.markdown("""
<div class="upload-panel">
  <div class="panel-title">Deepfake Detection Analysis</div>
  <div class="panel-sub">Upload a video to begin multimodal analysis</div>
""", unsafe_allow_html=True)


def render_panel_bottom():
    st.markdown("""
  <div class="trusted-row">
    <span class="trusted-label">Trained on</span>
    <div class="trusted-item"><span class="trusted-check">✓</span>&nbsp;FaceForensics++</div>
    <div class="trusted-item"><span class="trusted-check">✓</span>&nbsp;Wav2Lip Dataset</div>
    <div class="trusted-item"><span class="trusted-check">✓</span>&nbsp;VoiceClone Data</div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_result(result):
    label = result["label"]
    confidence = result["confidence"]
    badge_color = result["badge_color"]
    icon = result["icon"]
    p = result["probs"]

    badge_bg = (
        "rgba(34,197,94,0.12)" if icon == "✓"
        else "rgba(239,68,68,0.12)" if icon == "✗"
        else "rgba(234,179,8,0.12)"
    )

    class_data = [
        ("Real",       p[0], "#22c55e"),
        ("FaceSwap",   p[1], "#a78bfa"),
        ("Wav2Lip",    p[2], "#60a5fa"),
        ("VoiceClone", p[3], "#fb923c"),
    ]

    cards_html = "".join([f"""
    <div class="class-card">
      <div class="class-card-top">
        <div class="class-card-name">
          <div class="class-card-dot" style="background:{c}"></div>{n}
        </div>
        <div style="font-size:15px;font-weight:700;color:{c}">{v*100:.1f}%</div>
      </div>
      <div class="class-bar-track">
        <div class="class-bar-fill" style="width:{v*100:.1f}%;background:{c}"></div>
      </div>
    </div>""" for n, v, c in class_data])

    st.markdown(f"""
<div class="result-wrap">
  <div class="result-card">
    <div class="result-header">
      <div>
        <div class="section-label" style="margin-bottom:10px;">Detection Result</div>
        <div class="result-badge"
             style="background:{badge_bg};color:{badge_color};border:1.5px solid {badge_color}55;">
          <span style="font-size:20px;">{icon}</span> {label}
        </div>
      </div>
      <div style="text-align:right;">
        <div class="result-conf" style="color:{badge_color}">{confidence:.1f}%</div>
        <div class="result-conf-label">Confidence Score</div>
      </div>
    </div>
    <div class="divider"></div>
    <div style="margin-bottom:6px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
        <span style="font-size:13px;color:#475569;font-weight:500;">Overall confidence</span>
        <span style="font-size:13px;font-weight:700;color:#fff;">{confidence:.1f}%</span>
      </div>
      <div style="height:10px;background:rgba(255,255,255,0.04);border-radius:5px;overflow:hidden;">
        <div style="height:100%;width:{confidence:.1f}%;background:{badge_color};border-radius:5px;"></div>
      </div>
    </div>
    <div class="divider"></div>
    <div class="section-label">Class Probabilities</div>
    <div class="class-grid">{cards_html}</div>
  </div>
</div>
""", unsafe_allow_html=True)