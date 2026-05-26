# lthsbpa
Lebanon Trail High School BPA Website

## Calendar sync

The homepage calendar is static HTML generated from the chapter Google Calendar. It does not use browser JavaScript.

To refresh it locally:

```powershell
$env:GOOGLE_CALENDAR_API_KEY="your-api-key"
python scripts\sync_calendar.py
```

The script rewrites only the generated calendar and milestone blocks in `index.html`.
