# app.py
import streamlit as st
import pandas as pd
from db_utils import init_db, save_result, fetch_results  # ✅ db_utils integrated

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Automated Resume Relevance Check System",
    page_icon="📄",
    layout="wide",
)

# ==============================
# INITIALIZE DATABASE
# ==============================
init_db()  # Creates results.db and table if not exists

# ==============================
# SIDEBAR THEME & LOGIN/SIGNUP PLACEHOLDERS
# ==============================
st.sidebar.title("👤 User Access (Placeholder)")
st.sidebar.button("Login")   # placeholder
st.sidebar.button("Signup")  # placeholder

# Dark/Light mode toggle
theme = st.sidebar.radio("Theme", ["Light", "Dark"])

# ==============================
# COLORS & STYLING
# ==============================
if theme == "Dark":
    page_bg = "#1A1A2E"
    text_color = "#EAEAEA"
    card_color = "#16213E"
    shadow_color = "rgba(255,255,255,0.05)"
    border_color = "#0F3460"
    front_bg_color = "#1F4068"
    front_text_color = "#EAEAEA"
else:
    page_bg = "#F2F2F2"
    text_color = "black"
    card_color = "#FFFFFF"
    shadow_color = "rgba(0,0,0,0.1)"
    border_color = "#CCC"
    front_bg_color = "#A8DADC"
    front_text_color = "#1A1A1A"

# Page-wide CSS
st.markdown(
    f"""
    <style>
    body {{
        background-color: {page_bg};
        color: {text_color};
        transition: background-color 0.5s, color 0.5s;
    }}
    .stButton>button {{
        background-color: {card_color};
        color:{text_color};
        border:1px solid {border_color};
    }}
    .stTextInput>div>div>input {{
        background-color: {card_color};
        color:{text_color};
        border:1px solid {border_color};
    }}
    h1 {{font-family: 'Times New Roman', serif;}}
    h3 {{font-style: italic;}}
    p {{font-style: italic;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================
# FRONT PAGE / HEADER
# ==============================
st.markdown(
    f"""
    <div style="background-color:{front_bg_color}; padding:40px; border-radius:15px; text-align:center;">
        <h1 style="color:{front_text_color}; font-family: 'Times New Roman', serif;">📄 <b>Automated Resume Relevance Check System</b></h1>
        <h3 style="color:{front_text_color}; font-style: italic;">✨ AI-powered Resume Screening & Job Matching ✨</h3>
        <p style="color:{front_text_color}; font-size:18px; font-style: italic;">
            👋 Welcome! Upload a Job Description & one or more Resumes below, then click <b>Analyze</b> to see how well they match.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ==============================
# UPLOAD SECTION (TWO COLUMNS)
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Upload Job Description (JD)")
    jd_file = st.file_uploader("Choose a JD file (PDF/TXT/DOCX)", type=["pdf", "txt", "docx"], key="jd_upload")

with col2:
    st.subheader("📌 Upload Resume(s)")
    resume_files = st.file_uploader(
        "Choose one or more Resume files (PDF/DOCX)",
        type=["pdf", "docx"],
        key="resume_upload",
        accept_multiple_files=True,
    )

st.write("")  # spacing

# ==============================
# ANALYZE BUTTON
# ==============================
analyze_btn = st.button("🚀 Analyze", use_container_width=True)

if analyze_btn:
    if jd_file and resume_files:
        high_score_exists = False  # flag for balloons
        for resume_file in resume_files:
            # Placeholder scoring (replace with backend integration)
            score = 85.0
            verdict = "High"
            missing_skills = ["Tableau", "Power BI"]

            verdict_color = {"High": "green", "Medium": "orange", "Low": "red"}.get(verdict, text_color)

            # ✅ Save result to DB using db_utils
            save_result(
                resume_file.name,
                jd_file.name,
                "Sample Role",
                score,
                verdict,
                missing_skills,
                location="Hyderabad"
            )

            # Mark if score > 65
            if score > 65:
                high_score_exists = True

            # Results Card
            st.markdown(
                f"""
                <div style="background-color:{card_color}; padding:20px; border-radius:15px;
                            box-shadow:2px 2px 10px {shadow_color}; margin-top:20px; color:{text_color};">
                    <h4 style="color:#2E86C1;"><b>🎯 Analysis Results</b></h4>
                    <b>Resume:</b> {resume_file.name}<br>
                    <b>Job Description:</b> {jd_file.name}<br>
                    <b>Role:</b> Sample Role<br>
                    <b>Score:</b> {score:.2f}%<br>
                    <b>Verdict:</b> <span style="color:{verdict_color};"><b>{verdict}</b></span><br>
                    <b>Missing Skills:</b> {", ".join(missing_skills) if missing_skills else "None"}<br>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Summary Box
            st.markdown(
                f"""
                <div style="background-color:{card_color}; padding:20px; border-radius:12px;
                            margin-top:20px; border-left:6px solid #4CAF50; color:{text_color};">
                    <h4 style="color:#27AE60;">📝 <b>Summary & Suggestions</b></h4>
                    ✅ Your resume matches well with the JD.<br>
                    📊 Overall Relevance Score: <b>{score:.2f}%</b> → 
                    <span style="color:{verdict_color};"><b>{verdict} Fit</b></span><br>
                    ⚡ Focus on improving by adding these skills: 
                    <b>{", ".join(missing_skills) if missing_skills else "No major gaps detected"}</b><br>
                    🚀 Next Step: Strengthen your profile with projects/certifications in these areas.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 🎉 Trigger balloons only once, after all resumes are analyzed
        if high_score_exists:
            st.balloons()
    else:
        st.error("⚠️ Please upload both a JD and at least one Resume before analyzing.")

# ==============================
# DASHBOARD SECTION (Table View)
# ==============================
st.divider()
st.subheader("📊 Dashboard - Search & Filter Results")

# Fetch all results from DB
all_results = fetch_results({})
df_all = pd.DataFrame(all_results, columns=[
    "ID", "Resume", "JD", "Role", "Score", "Verdict", "Missing Skills", "Location"
]) if all_results else pd.DataFrame()

# Dropdown filters
roles = df_all['Role'].unique().tolist() if not df_all.empty else []
locations = df_all['Location'].unique().tolist() if not df_all.empty else []

role_filter = st.selectbox("🔎 Filter by Role Title", ["All"] + roles)
location_filter = st.selectbox("📍 Filter by Location", ["All"] + locations)
min_score, max_score = st.slider("📈 Score Range", 0, 100, (0, 100))

# Apply filters
df_filtered = df_all.copy()
if role_filter != "All":
    df_filtered = df_filtered[df_filtered["Role"] == role_filter]
if location_filter != "All":
    df_filtered = df_filtered[df_filtered["Location"] == location_filter]
df_filtered = df_filtered[(df_filtered["Score"] >= min_score) & (df_filtered["Score"] <= max_score)]

# Dashboard metrics
col1, col2, col3 = st.columns(3)
col1.metric("📝 Total Resumes", len(df_filtered))
col2.metric("📊 Average Score", f"{df_filtered['Score'].mean():.2f}%" if not df_filtered.empty else "0%")
high_count = df_filtered[df_filtered["Verdict"] == "High"].shape[0] if not df_filtered.empty else 0
col3.metric("🎯 High Matches", high_count)

# Show results in table with color-coded verdict
if not df_filtered.empty:
    def color_verdict(val):
        if val == "High":
            return 'color: green; font-weight:bold'
        elif val == "Medium":
            return 'color: orange; font-weight:bold'
        elif val == "Low":
            return 'color: red; font-weight:bold'
        else:
            return ''

    st.dataframe(df_filtered.style.applymap(color_verdict, subset=["Verdict"]), use_container_width=True)

    # Download filtered results
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Results as CSV",
        data=csv,
        file_name="filtered_resume_results.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info("ℹ️ No results match the selected filters.")
