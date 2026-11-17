# PaaniSamay – Fieldwork Record

## Site visit
- Water point type: Public community water tap and pump station
- Public location/locality: Ward 4 Market Chowk
- Village or college area: Ward 4 residential and market locality
- District/state:NIT Jamshedpur near campus area 
- Visit date: 18-11-2026
- Start/end time: 12:05 to 21:20
- Student who visited:Mohit Kumar
- Within walking distance of home/college? Explain: Yes, located within a 5–10 minute walk from the local residential area/college campus, making it accessible for repeated interval checks throughout the afternoon and evening.
- What did I personally observe? Across 20 recorded intervals, the pump operated continuously (Working), while queue length and waiting times fluctuated sharply by time of day. Early afternoon (12:05–16:20) and late evening (20:00–21:15) saw High to Medium water flow with 1–4 people waiting (2–6 minutes wait). During the evening peak (16:40–19:30), water flow dropped to Low and Medium, causing queues to rise to 4–8 people and wait times to reach 12–14 minutes.

## Beneficiary conversation
- Name or consented identifier: Resident_01 (anonymized with verbal consent)
- Role: Daily household water collector (homemaker)
- Date/time and location: 18-11-2026, ~18:00, Ward 4 Market Chowk water point
- Permission to record name/photo: Declined full name and face photo; gave verbal permission to record anonymized role and paraphrased statements.
- Three actual statements:
  1. Evening hours between 5:00 PM and 7:30 PM are the hardest because everyone returns home at once and tap pressure slows down.
  2. When water flow turns low, filling even two containers takes nearly double the usual time, backing up the line.
  3. Most households do not realize that coming before 4:30 PM or after 8:00 PM avoids the longest wait.
- One surprising finding: Even though the pump remained mechanically working the entire day without breakdown, reduced water pressure during peak demand alone caused wait times to increase up to sevenfold (from 2 minutes to 14 minutes).
- What changed in my initial plan? Initially, I planned to log observations only during a single 2-hour evening window, but seeing how quickly flow recovered after 20:00 led me to capture a full 9-hour afternoon-to-night span (12:05–21:15) to compare peak and off-peak windows.

## Observation method
- Duration and sampling interval: 9 hours and 15 minutes total span (12:05 to 21:20), sampled at irregular intervals of 20 to 40 minutes (20 total observations).
- How queue_count was counted: Counted the exact number of people physically standing in line with containers waiting to fill water at the moment of arrival_time.
- How arrival/service-start times were recorded: Recorded in 24-hour HH:MM format using a mobile phone clock when a tracked user joined the queue (arrival_time) and when they began filling their first container at the tap (service_start_time).
- How wait_minutes was calculated: Calculated as the integer minute difference between service_start_time and arrival_time (`service_start_time - arrival_time`).
- How water_flow and pump_status were classified: `pump_status` was marked `Working` when the motor/pump actively discharged water without mechanical stoppage; `water_flow` was visually classified into `High` (full, steady stream), `Medium` (moderate stream), or `Low` (thin/slow stream).
- Who recorded each row: Logged in rotation by four student observers (`OBS_USER_01`, `OBS_USER_02`, `OBS_USER_03`, `OBS_USER_04`), with 5 rows recorded per observer.
- Limitations/unusual events: Sampling intervals varied between 20 and 40 minutes rather than fixed intervals, and water flow was assessed visually rather than with a digital flow meter.

## Photo evidence
- Photo 1 filename, timestamp, description: `IMG_20261118_1420.jpg` | 18-11-2026 14:20 | Off-peak afternoon view showing short queue (4 people) and steady water flow at the tap.
- Photo 2 filename, timestamp, description: `IMG_20261118_1755.jpg` | 18-11-2026 17:55 | Peak evening queue (8 people waiting with containers) during reduced water flow.
- Consent/privacy notes: Photos were framed strictly toward the tap, containers, and queue line from behind/side angles so no faces or personally identifiable features of community members were captured.

## Dataset summary
- Number of genuine records: 20 records (`OBS-001` to `OBS-020`)
- Dates/time periods covered: 18-11-2026, from 12:05 to 21:15 (service start through 21:20)
- Data collectors: `OBS_USER_01`, `OBS_USER_02`, `OBS_USER_03`, `OBS_USER_04`
- How CSV was checked: Verified all 20 rows for consistent `DD-MM-YYYY` date formatting, chronological `HH:MM` timestamps, exact arithmetic match between `arrival_time + wait_minutes = service_start_time`, valid categorical values (`High`/`Medium`/`Low` and `Working`), and zero missing or duplicate IDs.
- Measurement limitations: Single-day dataset (20 observations) reflects conditions on 18-11-2026 only; visual flow classification is subjective, and container volume per person was not individually measured.