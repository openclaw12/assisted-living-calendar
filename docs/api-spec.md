# API Spec (Outline)

## Authentication
- JWT-based session tokens with role claims (resident, staff, admin).
- Optional SSO via OIDC for enterprise customers.

## REST Endpoints
- `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`
- `GET /residents`, `GET /residents/:id`, `PATCH /residents/:id`
- `GET /staff/shifts`, `POST /staff/shifts`
- `GET /polls`, `POST /polls`, `POST /polls/:id/vote`
- `POST /planner/run` triggers the monthly scheduling engine.
- `GET /events`, `POST /events`, `PATCH /events/:id`, `POST /events/:id/rsvp`
- `GET /analytics/engagement`, `GET /analytics/budget`
- `POST /tasks/reminders`, `POST /tasks/reports`

GraphQL layer TBD once REST baseline is stable.
