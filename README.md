# PaaniSamay – Smart Water Collection Timing & Monitoring
PaaniSamay analyses locally collected queue and waiting-time observations at a shared public water point. It compares time periods and identifies the period with the lowest average wait when enough records are available.

## Data integrity
- `data/data.csv` is the blank default field-data file.
- `demo_data/demo_sample.csv` is synthetic and only previews the interface.
- Demo records are labelled in the app and must never be submitted as fieldwork evidence.
- Use actual observations and document the actual data collector(s).

## Features
CSV upload/local loading, validation, timestamp/wait consistency warnings, queue and wait metrics, time-slot charts, water-flow chart, minimum-sample recommendation and CSV download.

## Stack
Python, Pandas, Streamlit, Plotly.

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run src/main.py
```
Actual field data mode is the default. With the blank CSV, the app displays a ready empty state. Select Demo preview (synthetic) only to test charts.

## CSV columns
`observation_id,date,arrival_time,queue_count,service_start_time,wait_minutes,water_flow,pump_status,observer`
- ID unique per row.
- Date: YYYY-MM-DD.
- Times: 24-hour HH:MM.
- Queue: non-negative whole number waiting at observation time.
- Wait: minutes from observed person's arrival until service starts.
- Flow: High, Medium, Low, Unknown.
- Pump: Working, Not Working, Unknown.
- Observer: actual collector name or agreed identifier.

 

## Actual field result (complete after visit)
- Site:Basti Near NIT Jamshedpur
- Beneficiary role/name (with permission):Ramesh Kumar
- Visit date(s):18/11/2026
- Genuine record count:20
- Data collector(s):20
- Actual finding:20
- What changed after conversation:

## Limitations
Not live monitoring; no water-quality testing; small or uneven samples may not generalize; recommendation is historical comparison, not a guarantee.


