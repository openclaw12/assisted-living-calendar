# Audit Trail Strategy

- Append-only event store capturing CRUD operations on PHI-related entities.
- Timestamp + user id + IP (where applicable) + request id for correlation.
- Daily export to immutable storage (object store with retention policy).
- Admin dashboard surfacing audit queries with filters (resident, date range, user).
