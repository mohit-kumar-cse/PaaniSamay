from datetime import datetime
import pandas as pd

REQUIRED = ["observation_id","date","arrival_time","queue_count","service_start_time","wait_minutes","water_flow","pump_status","observer"]
SLOTS = ["Early morning (05:00–08:59)","Late morning (09:00–10:59)","Afternoon (11:00–15:59)","Evening (16:00–20:59)","Night (21:00–04:59)"]

def slot_for_hour(h):
    if 5 <= h < 9: return SLOTS[0]
    if 9 <= h < 11: return SLOTS[1]
    if 11 <= h < 16: return SLOTS[2]
    if 16 <= h < 21: return SLOTS[3]
    return SLOTS[4]

def validate(raw):
    errors, warnings = [], []
    missing = [c for c in REQUIRED if c not in raw.columns]
    if missing: return pd.DataFrame(), [f"Missing columns: {', '.join(missing)}"], []
    df = raw[REQUIRED].copy().dropna(how="all")
    if df.empty or all(str(x).strip()=="" for x in df.to_numpy().flatten()):
        return pd.DataFrame(), [], ["No observations entered yet."]
    df = df.fillna("").astype(str)
    for c in REQUIRED: df[c] = df[c].str.strip()
    seen = set()
    for n, (_, r) in enumerate(df.iterrows(), 2):
        missing_values = [c for c in REQUIRED if not r[c]]
        if missing_values:
            errors.append(f"Row {n}: empty values in {', '.join(missing_values)}."); continue
        if r.observation_id in seen: errors.append(f"Row {n}: duplicate observation_id.")
        seen.add(r.observation_id)
        try: datetime.strptime(r.date, "%Y-%m-%d")
        except ValueError: errors.append(f"Row {n}: date must be YYYY-MM-DD.")
        for c in ["arrival_time","service_start_time"]:
            try: datetime.strptime(r[c], "%H:%M")
            except ValueError: errors.append(f"Row {n}: {c} must be 24-hour HH:MM.")
        try:
            if int(r.queue_count)<0: raise ValueError
        except ValueError: errors.append(f"Row {n}: queue_count must be a non-negative integer.")
        try:
            if float(r.wait_minutes)<0: raise ValueError
        except ValueError: errors.append(f"Row {n}: wait_minutes must be non-negative.")
        if r.water_flow.lower() not in {"high","medium","low","unknown"}:
            errors.append(f"Row {n}: invalid water_flow.")
        if r.pump_status.lower() not in {"working","not working","unknown"}:
            errors.append(f"Row {n}: invalid pump_status.")
        try:
            a=datetime.strptime(r.arrival_time,"%H:%M"); s=datetime.strptime(r.service_start_time,"%H:%M")
            delta=(s-a).total_seconds()/60
            if delta>=0 and abs(delta-float(r.wait_minutes))>1:
                warnings.append(f"Row {n}: wait_minutes differs from timestamp difference ({delta:.0f} min).")
            elif delta<0: warnings.append(f"Row {n}: service time precedes arrival; check overnight case.")
        except ValueError: pass
    if errors: return pd.DataFrame(), errors, warnings
    df["date"]=pd.to_datetime(df.date,format="%Y-%m-%d")
    df["queue_count"]=pd.to_numeric(df.queue_count).astype(int)
    df["wait_minutes"]=pd.to_numeric(df.wait_minutes).astype(float)
    df["arrival_hour"]=df.arrival_time.str[:2].astype(int)
    df["time_slot"]=df.arrival_hour.map(slot_for_hour)
    df["water_flow"]=df.water_flow.str.title()
    df["pump_status"]=df.pump_status.str.title()
    return df, [], warnings

def load_csv(source):
    try: raw=pd.read_csv(source,dtype="string",keep_default_na=False)
    except Exception as e: return pd.DataFrame(), [f"Could not read CSV: {e}"], []
    return validate(raw)

def summarize(df):
    if df.empty: return pd.DataFrame()
    out=df.groupby("time_slot",observed=False).agg(
        observations=("observation_id","count"),
        avg_wait=("wait_minutes","mean"),
        median_wait=("wait_minutes","median"),
        avg_queue=("queue_count","mean"),
        low_flow=("water_flow",lambda x:(x=="Low").sum()),
        pump_down=("pump_status",lambda x:(x=="Not Working").sum())
    ).reset_index()
    out["time_slot"]=pd.Categorical(out.time_slot,categories=SLOTS,ordered=True)
    return out.sort_values("time_slot").reset_index(drop=True)

def recommend(summary, min_count=3):
    if summary.empty: return None,"No observations are available."
    eligible=summary[summary.observations>=min_count].copy()
    if eligible.empty: return None,f"No slot has {min_count} records yet. Collect more data."
    eligible=eligible.sort_values(["avg_wait","avg_queue"],ascending=True)
    r=eligible.iloc[0]
    return str(r.time_slot),f"Lowest observed average wait: {r.avg_wait:.1f} minutes across {int(r.observations)} records."
