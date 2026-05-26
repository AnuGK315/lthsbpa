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

Event filters are assigned from Google Calendar metadata first:

- Google color Tomato (`colorId: 11`) -> Meetings
- Google color Tangerine (`colorId: 6`) -> Events
- Google color Sage (`colorId: 2`) -> Conferences
- Google color Peacock (`colorId: 7`) -> Deadlines

If an event has extended properties named `category`, values like `Meetings`, `Events`, `Conferences`, or `Deadlines` override the color. If neither is set, the script falls back to title/description keywords.

For autonomous syncing on GitHub, add a repository secret named `GOOGLE_CALENDAR_API_KEY`. The workflow in `.github/workflows/sync-calendar.yml` refreshes the generated calendar every six hours and can also be run manually from GitHub Actions.
