from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from analysis import REQUIRED,load_csv,summarize,recommend

st.set_page_config(page_title="PaaniSamay",page_icon="💧",layout="wide")
st.markdown("""<style>
.block-container{padding-top:2rem}
.hero{padding:1.3rem 1.5rem;border-radius:16px;background:linear-gradient(115deg,#e0f2fe,#ecfeff);border:1px solid #bae6fd}
.hero h1{margin:0;color:#0c4a6e}.hero p{margin:.4rem 0 0;color:#164e63}
</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>💧 PaaniSamay</h1><p>Smart water collection timing and community water-point insights</p></div>',unsafe_allow_html=True)
st.write("Analyse locally collected queue and waiting-time observations at a shared public water point.")

# Add your genuine site photo as photos/handpump.jpg (or .png/.jpeg).
photo_candidates = [ROOT/"photos/handpump.jpg", ROOT/"photos/handpump.jpeg", ROOT/"photos/handpump.png"]
site_photo = next((p for p in photo_candidates if p.exists()), None)
if site_photo:
    st.image(str(site_photo), caption="Selected water point – add your own field photograph", use_container_width=True)
else:
    st.info("Add your actual handpump/public water-point photograph as photos/handpump.jpg to display it here.")
with st.sidebar:
    st.header("Data settings")
    mode=st.radio("Dataset",["Actual field data","Demo preview (synthetic)"])
    upload=st.file_uploader("Upload CSV (optional)",type=["csv"])
    min_count=st.slider("Minimum records per slot",1,10,3)
    st.caption("Actual mode uses data/data.csv by default.")
source=upload if upload else (ROOT/"demo_data/demo_sample.csv" if mode.startswith("Demo") else ROOT/"data/data.csv")
df,errors,warnings=load_csv(source)
if mode.startswith("Demo"):
    st.warning("DEMO MODE: synthetic examples for interface testing only. Never submit these as fieldwork data.")
else:
    st.success("ACTUAL FIELD DATA MODE: using uploaded CSV or data/data.csv.")
if errors:
    st.error("Fix CSV validation errors:")
    for e in errors: st.write("• "+e)
    st.stop()
for w in warnings: st.warning(w)
if df.empty:
    st.info("Dashboard is ready. Your actual dataset is empty. Enter genuine observations in data/data.csv or upload a completed CSV.")
    st.markdown("### Collection checklist")
    st.write("- Record at least 20 real entries.\\n- Cover different time periods where possible.\\n- Record actual arrival and service-start times.\\n- Calculate waiting time from timestamps.\\n- Use a consistent queue-counting method.")
    st.download_button("Download blank CSV template",pd.DataFrame(columns=REQUIRED).to_csv(index=False).encode(),"paanisamay_template.csv","text/csv")
    st.stop()
if len(df)<20 and not mode.startswith("Demo"):
    st.info(f"{len(df)} valid records loaded. Assignment target: at least 20 genuine entries.")
a,b,c,d=st.columns(4)
a.metric("Observations",len(df))
b.metric("Average wait",f"{df.wait_minutes.mean():.1f} min")
c.metric("Average queue",f"{df.queue_count.mean():.1f} people")
d.metric("Low-flow records",int((df.water_flow=="Low").sum()))
summary=summarize(df)
best,reason=recommend(summary,min_count)
st.markdown("### Less-crowded period analysis")
if best: st.success(f"Lowest observed average waiting time: **{best}**")
else: st.info(reason)
st.caption(reason+" Historical comparison only; not a live forecast or guarantee.")
if not summary.empty:
    st.markdown("### Time-slot comparison")
    st.dataframe(summary.round(2),use_container_width=True,hide_index=True)
    x,y=st.columns(2)
    with x: st.plotly_chart(px.bar(summary,x="time_slot",y="avg_wait",title="Average waiting time",text_auto=".1f"),use_container_width=True)
    with y: st.plotly_chart(px.bar(summary,x="time_slot",y="avg_queue",title="Average queue length",text_auto=".1f"),use_container_width=True)
    flow=df.water_flow.value_counts().rename_axis("Water flow").reset_index(name="Records")
    st.plotly_chart(px.pie(flow,names="Water flow",values="Records",hole=.4,title="Observed water-flow conditions"),use_container_width=True)
st.markdown("### Observation records")
cols=["observation_id","date","arrival_time","queue_count","service_start_time","wait_minutes","water_flow","pump_status","observer"]
st.dataframe(df[cols],use_container_width=True,hide_index=True)
st.download_button("Download validated records",df[cols].to_csv(index=False).encode(),"paanisamay_validated.csv","text/csv")
with st.expander("Method and limitations"):
    st.write("Recommendation is the lowest observed mean wait among slots meeting the minimum sample count. The tool is not live monitoring, does not test water quality and cannot guarantee future queue conditions. Results depend on sample coverage and consistent observations.")
st.caption("PaaniSamay • Local observations • No external data/API")
