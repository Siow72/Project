# to run this, in terminal "streamlit run application.py"

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Hotel Revenue Management")

# data and bundle loading
@st.cache_resource
def load_assets():
    bundle = joblib.load("application_bundle.pkl")
    df = pd.read_csv("df_streamlit.csv")
    return bundle, df

bundle, df = load_assets()
model_pipe = bundle["pipeline"]
encoders = bundle["label_encoders"]
scaler = bundle["scaler"]
int_cols = bundle["int_cols"]

# kpi section
st.title("Hotel Cancellation Analysis & Prediction")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Bookings", f"{len(df):,}")
with k2:
    st.metric("Avg Price (ADR)", f"${df['adr'].mean():.2f}")
with k3:
    st.metric("Cancellation Rate", f"{(df['is_canceled'].mean()*100):.1f}%")
with k4:
    st.metric("Avg Lead Time", f"{int(df['lead_time'].mean())} days")

st.divider()

# graph/insights section
st.subheader("Business Intelligence")
g1, g2 = st.columns(2)

with g1:
    st.markdown("#### The 'Danger Zone': Lead Time & Price")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df.sample(2000, random_state=42), 
                    x="lead_time", y="adr", hue="is_canceled", 
                    alpha=0.5, ax=ax)
    st.pyplot(fig)

with g2:
    st.markdown("#### Engagement vs. Cancellation")
    req_stats = df.groupby('total_of_special_requests')['is_canceled'].mean() * 100
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=req_stats.index, y=req_stats.values, palette="Reds_r", ax=ax2)
    ax2.set_ylabel("Chance of Cancellation (%)")
    st.pyplot(fig2)

st.divider()

# predictor section
st.subheader("Booking Cancellation Predictor")
col_in, col_out = st.columns([1.2, 1])

with col_in:
    with st.expander("Enter Booking Details", expanded=True):
        lt = st.number_input("Lead Time (Days)", 0, 700, 10)
        adr_val = st.number_input("Price per Night (ADR)", 0.0, 1000.0, 120.0)
        spec = st.slider("Total Special Requests", 0, 5, 0)
        mkt = st.selectbox("Market Segment", options=list(encoders['market_segment'].classes_))
        
        r_col, a_col = st.columns(2)
        with r_col:
            res = st.selectbox("Reserved Room Type", options=list(encoders['reserved_room_type'].classes_))
        with a_col:
            asn = st.selectbox("Assigned Room Type", options=list(encoders['assigned_room_type'].classes_))
            
        with st.expander("Additional Information"):
            prt = st.radio("Is Guest from Portugal?", [1, 0], format_func=lambda x: "Yes" if x==1 else "No")
            park = st.radio("Requires Parking Space?", [0, 1])
            yr = st.number_input("Arrival Year", 2024, 2027, 2026)
            wk = st.number_input("Arrival Week Number", 1, 53, 25)

    predict_btn = st.button("Predict Cancellation Risk", use_container_width=True, type="primary")

with col_out:
    if predict_btn:
        input_data = pd.DataFrame([{
            'lead_time': lt, 'total_of_special_requests': spec, 'is_prt': prt,
            'adr': adr_val, 'assigned_room_type': asn, 'market_segment': mkt,
            'reserved_room_type': res, 'arrival_date_year': yr,
            'arrival_date_week_number': wk, 'required_car_parking_spaces': park
        }])
        
        for c in ['market_segment', 'reserved_room_type', 'assigned_room_type']:
            input_data[c] = encoders[c].transform(input_data[c].astype(str))
        input_data[int_cols] = scaler.transform(input_data[int_cols])
        
        cancel_prob = model_pipe.predict_proba(input_data)[0][1]
        
        st.write("### Prediction Results")
        
        if cancel_prob > 0.70:
            st.error(f"## High Risk: {cancel_prob*100:.1f}%")
            st.write("**Verdict: This guest is very likely to CANCEL.**")
            st.markdown("---")
            st.subheader("Recommended Actions")
            st.warning("**Revenue Protection:** Convert to non-refundable or request deposit.")
            st.warning("**Inventory:** High priority for overbooking.")
            
        elif cancel_prob > 0.35:
            st.warning(f"## Moderate Risk: {cancel_prob*100:.1f}%")
            st.write("**Verdict: Booking is uncertain.**")
            st.markdown("---")
            st.subheader("Recommended Actions")
            st.info("**Engagement:** Send a personalized email with a 'check-in perk'.")
            st.info("**Verification:** Call to confirm details 48 hours prior.")
            
        else:
            # We show the Risk (the small number) so the color matches the text
            st.success(f"## Low Risk: {cancel_prob*100:.1f}%")
            st.write("**Verdict: This guest is likely to SHOW UP.**")
            st.markdown("---")
            st.subheader("Recommended Actions")
            st.success("**Hospitality:** Pre-assign room and prepare for arrival.")
            st.success("**Efficiency:** Expedite check-in.")

    else:
        st.info("Adjust details and click 'Predict' to see the risk analysis and management actions.")