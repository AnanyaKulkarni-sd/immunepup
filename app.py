import streamlit as st
from datetime import date, datetime, timedelta
import calendar

st.set_page_config(page_title="PawCare | Vaccination Planner", page_icon="🐾", layout="wide")

# -------------------- Styling --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');
:root { --purple:#7136d9; --purple2:#8b55ed; --ink:#17152e; --muted:#77748c; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: #f4efff; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px; }
h1,h2,h3 { color:var(--ink); }
.topbar { background:linear-gradient(110deg,#7136d9,#8b50ec); color:white; padding:20px 24px; border-radius:22px; margin-bottom:18px; box-shadow:0 12px 30px #6130bf22; }
.topbar h1 { color:white; font-family:'Playfair Display',serif; font-size:30px; margin:0; }
.topbar p { color:#eee5ff; margin:3px 0 0 0; font-size:13px; }
.panel { background:white; border:1px solid #ece7f6; border-radius:20px; padding:18px; box-shadow:0 8px 24px #34205b0a; }
.panel-title { font-family:'Playfair Display',serif; font-size:21px; color:#19162e; margin-bottom:12px; }
.muted { color:#89859b; font-size:12px; }
.event { border-radius:12px; padding:12px 13px; margin:9px 0; border-left:5px solid; }
.event strong { color:#211b39; font-size:14px; }
.event small { color:#68627b; }
.violet { background:#eee7ff; border-color:#8c62ec; }
.teal { background:#ddf8f6; border-color:#55c9c2; }
.blue { background:#e3f0ff; border-color:#65aef5; }
.peach { background:#fff0dc; border-color:#f2b54f; }
.pink { background:#ffe7eb; border-color:#ec8d9b; }
.metric { background:#fff; border:1px solid #ece7f6; padding:14px 16px; border-radius:16px; }
.metric .num { font-size:26px; font-weight:700; color:#7136d9; }
.metric .lab { font-size:12px; color:#858097; }
.dayhead { background:linear-gradient(120deg,#7136d9,#8c4ee9); color:white; padding:18px 20px; border-radius:16px 16px 0 0; }
.dayhead h2 { color:white; font-family:'Playfair Display',serif; margin:0; }
.dayhead p { color:#eee4ff; margin:4px 0 0 0; font-size:12px; }
.slot { padding:12px 10px; border-bottom:1px solid #eeeaf4; display:flex; gap:14px; align-items:center; }
.slot-time { width:58px; color:#77728c; font-size:12px; }
.slot-card { flex:1; border-radius:11px; padding:11px 13px; }
.detail-row { padding:12px 0; border-bottom:1px solid #eeeaf4; color:#25213b; }
div[data-testid="stButton"] button { border-radius:12px; border:1px solid #e4d9fb; }
div[data-testid="stButton"] button[kind="primary"] { background:#7136d9; border-color:#7136d9; }
div[data-testid="stTextInput"] input, div[data-testid="stDateInput"] input, div[data-testid="stSelectbox"] div { border-radius:10px; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# -------------------- Prototype data --------------------
if "dogs" not in st.session_state:
    st.session_state.dogs = [
        {"id":"PC-001","name":"Bruno","type":"Pet dog","breed":"Labrador Retriever","area":"Indiranagar","age":"2 years","owner":"Ananya"},
        {"id":"PC-002","name":"Milo","type":"Community dog","breed":"Indie","area":"Jayanagar 4th Block","age":"Approx. 3 years","owner":"Community volunteer"},
        {"id":"PC-003","name":"Coco","type":"Pet dog","breed":"Beagle","area":"HSR Layout","age":"1 year","owner":"Rahul"},
    ]
if "records" not in st.session_state:
    today = date.today()
    st.session_state.records = [
        {"dog":"Bruno","vaccine":"Rabies","date":today+timedelta(days=2),"time":"10:30 AM","clinic":"Paws & Care Veterinary Clinic","status":"Upcoming","notes":"Appointment requested. Confirm with clinic.","kind":"peach"},
        {"dog":"Milo","vaccine":"Veterinarian review","date":today+timedelta(days=4),"time":"09:00 AM","clinic":"Community vaccination drive","status":"Planned","notes":"Volunteer has reported Milo's location.","kind":"teal"},
        {"dog":"Coco","vaccine":"Vaccination record check","date":today+timedelta(days=7),"time":"11:00 AM","clinic":"Happy Tails Vet Centre","status":"Upcoming","notes":"Bring previous vaccination card if available.","kind":"blue"},
        {"dog":"Bruno","vaccine":"DHPP record","date":today-timedelta(days=25),"time":"Completed","clinic":"Paws & Care Veterinary Clinic","status":"Completed","notes":"Sample historical record for demonstration.","kind":"violet"},
    ]
if "selected" not in st.session_state:
    st.session_state.selected = 0

dogs = st.session_state.dogs
records = st.session_state.records
today = date.today()
month_name = calendar.month_name[today.month]

# -------------------- Header --------------------
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
    <div><h1>🐾 PawCare</h1><p>Dog vaccination planner · Pet dogs & community dogs</p></div>
    <div style="text-align:right;font-size:12px;color:#f2eaff">PROTOTYPE MODE<br><b>{today.strftime('%A, %d %B %Y')}</b></div>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------- Metrics --------------------
upcoming = [r for r in records if r["status"] != "Completed" and r["date"] >= today]
completed = [r for r in records if r["status"] == "Completed"]
community_count = sum(1 for d in dogs if d["type"] == "Community dog")
m1,m2,m3,m4 = st.columns(4)
for col, num, label in [
    (m1,len(dogs),"Registered dogs"),
    (m2,len(upcoming),"Upcoming activities"),
    (m3,len(completed),"Completed records"),
    (m4,community_count,"Community dogs")
]:
    with col:
        st.markdown(f'<div class="metric"><div class="num">{num}</div><div class="lab">{label}</div></div>',unsafe_allow_html=True)

st.write("")
left, center, right = st.columns([1.02,1.55,1.02], gap="medium")

# -------------------- Left: agenda --------------------
with left:
    st.markdown('<div class="panel-title">Vaccination agenda</div>', unsafe_allow_html=True)
    st.caption("Upcoming and recent records")
    view_filter = st.selectbox("Show", ["All dogs","Pet dogs","Community dogs"], label_visibility="collapsed")
    filtered = records
    if view_filter == "Pet dogs":
        pet_names = [d["name"] for d in dogs if d["type"] == "Pet dog"]
        filtered = [r for r in records if r["dog"] in pet_names]
    elif view_filter == "Community dogs":
        community_names = [d["name"] for d in dogs if d["type"] == "Community dog"]
        filtered = [r for r in records if r["dog"] in community_names]
    for idx, r in enumerate(sorted(filtered, key=lambda x:x["date"])):
        dog = next((d for d in dogs if d["name"] == r["dog"]), None)
        css = r.get("kind","violet")
        status_label = r["status"]
        st.markdown(f"""
        <div class="event {css}">
          <div style="font-size:10px;text-transform:uppercase;letter-spacing:.5px">{r['date'].strftime('%b %d')} · {status_label}</div>
          <strong>{r['vaccine']}</strong><br>
          <small>{r['dog']} · {r['clinic']}</small>
        </div>""", unsafe_allow_html=True)

# -------------------- Center: calendar / timeline --------------------
with center:
    st.markdown(f'<div class="dayhead"><h2>{month_name}</h2><p>Vaccination calendar · Select a record on the right to view details</p></div>', unsafe_allow_html=True)
    cal = calendar.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(today.year,today.month)
    # calendar grid
    st.markdown('<div style="padding:14px 15px 4px 15px">',unsafe_allow_html=True)
    cols = st.columns(7)
    for c, day in zip(cols, ["S","M","T","W","T","F","S"]):
        c.markdown(f"<div style='text-align:center;color:#8c849f;font-size:12px'>{day}</div>",unsafe_allow_html=True)
    for week in weeks:
        cols = st.columns(7)
        for c, day in zip(cols,week):
            if day == 0:
                c.markdown("<div style='height:35px'></div>",unsafe_allow_html=True)
            else:
                is_today = day == today.day
                bg = "#7136d9" if is_today else "#f4efff"
                fg = "white" if is_today else "#3d3655"
                c.markdown(f"<div style='height:32px;width:32px;margin:auto;border-radius:50%;display:flex;align-items:center;justify-content:center;background:{bg};color:{fg};font-size:12px;font-weight:600'>{day}</div>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    st.markdown('<div style="padding:0 18px 12px 18px;font-weight:600;color:#28223e">Activity timeline</div>',unsafe_allow_html=True)
    timeline = sorted(records,key=lambda x:x["date"])
    for r in timeline:
        if r["status"] == "Completed":
            continue
        when = "Today" if r["date"] == today else r["date"].strftime("%a, %d %b")
        css = r.get("kind","violet")
        st.markdown(f"""
        <div class="slot">
          <div class="slot-time">{when}<br>{r['time']}</div>
          <div class="slot-card {css}">
            <b style="font-size:13px">{r['vaccine']} · {r['dog']}</b><br>
            <span style="font-size:11px;color:#69627d">{r['clinic']}</span>
          </div>
        </div>""",unsafe_allow_html=True)

# -------------------- Right: details and add form --------------------
with right:
    st.markdown('<div class="panel-title">Record details</div>', unsafe_allow_html=True)
    record_labels = [f"{r['dog']} · {r['vaccine']} · {r['date'].strftime('%d %b')}" for r in records]
    selected_label = st.selectbox("Choose a record",record_labels,index=min(st.session_state.selected,len(record_labels)-1))
    selected_idx = record_labels.index(selected_label)
    st.session_state.selected = selected_idx
    r = records[selected_idx]
    dog = next((d for d in dogs if d["name"] == r["dog"]), {})
    st.markdown(f"<h3 style='font-family:Playfair Display,serif;font-size:22px;margin:12px 0 4px'>{r['vaccine']}</h3>",unsafe_allow_html=True)
    st.markdown(f"<span style='background:#eee7ff;color:#7136d9;padding:5px 10px;border-radius:20px;font-size:11px'>{r['status']}</span>",unsafe_allow_html=True)
    st.markdown(f"""
    <div class="detail-row">📅 &nbsp; <b>{r['date'].strftime('%A, %d %B %Y')}</b><br><span class="muted">{r['time']}</span></div>
    <div class="detail-row">🐶 &nbsp; <b>{r['dog']}</b><br><span class="muted">{dog.get('type','Dog')} · {dog.get('breed','')}</span></div>
    <div class="detail-row">📍 &nbsp; <b>{r['clinic']}</b></div>
    <div class="detail-row">📝 &nbsp; {r['notes']}</div>
    """,unsafe_allow_html=True)
    st.write("")
    st.markdown("**Quick actions**")
    if r["status"] != "Completed":
        if st.button("Mark as completed (demo)",type="primary",use_container_width=True):
            st.session_state.records[selected_idx]["status"] = "Completed"
            st.success("Marked completed in this demo session.")
            st.rerun()
    else:
        st.info("This sample record is marked completed.")
    st.markdown("</div>",unsafe_allow_html=True)

st.write("")
# -------------------- Add record / dog --------------------
with st.expander("＋ Add a dog or vaccination record", expanded=False):
    tab1,tab2 = st.tabs(["Register a dog","Add vaccination record"])
    with tab1:
        with st.form("dog_form",clear_on_submit=True):
            a,b = st.columns(2)
            name = a.text_input("Dog name")
            dog_type = b.selectbox("Dog category",["Pet dog","Community dog"])
            breed = a.text_input("Breed / type",placeholder="e.g. Indie, Labrador")
            area = b.text_input("Locality",placeholder="e.g. Jayanagar")
            age = a.text_input("Age",placeholder="e.g. 2 years / Unknown")
            owner = b.text_input("Owner / volunteer",placeholder="Optional")
            submitted = st.form_submit_button("Save dog",type="primary")
            if submitted:
                if not name.strip():
                    st.error("Please enter a dog name or temporary identifier.")
                else:
                    st.session_state.dogs.append({"id":f"PC-{len(st.session_state.dogs)+1:03d}","name":name.strip(),"type":dog_type,"breed":breed or "Not specified","area":area or "Not specified","age":age or "Unknown","owner":owner or "Not specified"})
                    st.success(f"{name} added to the prototype.")
                    st.rerun()
    with tab2:
        dog_names = [d["name"] for d in st.session_state.dogs]
        with st.form("record_form",clear_on_submit=True):
            a,b = st.columns(2)
            dog_name = a.selectbox("Select dog",dog_names)
            vaccine = b.text_input("Vaccine / activity",placeholder="Enter vet-confirmed vaccine name")
            vdate = a.date_input("Date",value=date.today()+timedelta(days=7))
            vtime = b.text_input("Time",value="To be confirmed")
            clinic = a.text_input("Clinic / organisation")
            status = b.selectbox("Status",["Upcoming","Planned","Completed"])
            notes = st.text_area("Notes",placeholder="Add details confirmed by the veterinary professional")
            submitted2 = st.form_submit_button("Save record",type="primary")
            if submitted2:
                if not vaccine.strip():
                    st.error("Please enter a vaccine or activity name.")
                else:
                    st.session_state.records.append({"dog":dog_name,"vaccine":vaccine.strip(),"date":vdate,"time":vtime,"clinic":clinic or "Not specified","status":status,"notes":notes or "No additional notes.","kind":"teal" if status=="Planned" else "violet"})
                    st.success("Vaccination record added to the prototype.")
                    st.rerun()

# -------------------- Dog directory --------------------
with st.expander("🐕 Registered dogs / community dog directory"):
    for d in st.session_state.dogs:
        st.markdown(f"**{d['name']}** · {d['type']} · {d['breed']}  \n`{d['id']}` · {d['area']} · Age: {d['age']} · Contact: {d['owner']}")
        st.divider()

st.caption("PawCare is an educational prototype. Sample data is illustrative and stored only in the current Streamlit session. Vaccination decisions and due dates must be confirmed by a qualified veterinarian.")
