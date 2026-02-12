# Data Model Notes

## Entities
- **Resident**: profile, care plan tags, mobility aids, dietary notes, contact preferences.
- **StaffShift**: caregiver, role, start/end, certifications, assigned residents.
- **Vendor**: service category, contact info, cost profiles, preferred lead time.
- **Poll**: month, candidate activities, eligibility rules, vote window.
- **Vote**: resident id, poll id, ranking, accessibility flags.
- **Event**: datetime, location, capacity, staff roster, vendor link, cost, compliance notes.
- **EngagementLog**: resident id, event id, status (attended, declined, waitlist), mood notes.

## Relationships
- Residents participate in polls and events; votes influence the scheduling engine.
- Staff shifts must overlap the events they support; optimizer balances workload.
- Vendors tie into events + budget tracker for forecast vs actual spend.
- Engagement logs feed analytics + wellness alerts.
