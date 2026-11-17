# Manual test checklist
1. Empty actual CSV shows a helpful empty state.
2. Missing required header reports an error.
3. Invalid date/time is rejected.
4. Negative queue/wait is rejected.
5. Invalid flow/status category is rejected.
6. Duplicate observation IDs are rejected.
7. Timestamp/wait mismatch shows a warning.
8. Insufficient sample count withholds recommendation.
9. Valid real data produces metrics/charts.
10. Uploading a CSV uses the uploaded data.
