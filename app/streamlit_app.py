from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json, pandas as pd, streamlit as st
from src.nids.predict import load_artifacts,predict_frame
st.set_page_config(page_title="Network Intrusion Detection",page_icon="🛡️",layout="wide")
st.title("🛡️ Network Intrusion Detection & Anomaly Scoring")
page=st.sidebar.radio("Page",["Overview","Model Performance","Anomaly Detection","Risk Scoring","PCA Visualization"])
def read_report(name):
    p=Path("reports")/name
    return json.loads(p.read_text()) if p.exists() else None
if page=="Overview":
    st.header("Dataset and training overview")
    r=read_report("training_summary.json")
    if r: st.metric("Flows loaded",f'{r["rows"]:,}'); st.json(r)
    else: st.warning("Training report unavailable. Install CIC-IDS2017 and run python -m src.nids.train.")
elif page=="Model Performance":
    st.header("Held-out test performance")
    r=read_report("metrics.json")
    st.json(r) if r else st.info("Run python -m src.nids.evaluate after training.")
elif page=="Anomaly Detection":
    st.header("Upload and score network flows")
    up=st.file_uploader("CIC-IDS2017-compatible flow CSV",type="csv")
    if up:
        try:
            result=predict_frame(pd.read_csv(up),load_artifacts())
            st.dataframe(result,use_container_width=True)
            st.download_button("Download scored CSV",result.to_csv(index=False),"scored_flows.csv","text/csv")
        except Exception as e: st.error(str(e))
elif page=="Risk Scoring":
    st.header("Risk policy")
    st.write("LOW: Allow and monitor | MEDIUM: Log for investigation | HIGH: Flag for security review | CRITICAL: Prioritize investigation")
    st.caption("Risk bands are score-based policy labels, not calibrated attack probabilities.")
elif page=="PCA Visualization":
    p=Path("models/pca_reconstruction.joblib")
    if p.exists():
        import joblib
        model=joblib.load(p); st.metric("Retained components",model.pca_.n_components_)
        st.bar_chart(model.pca_.explained_variance_ratio_)
        st.line_chart(pd.Series(model.pca_.explained_variance_ratio_).cumsum())
    else: st.info("PCA artifact appears after genuine dataset training.")
