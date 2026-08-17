 # API Reference

`ai-powered-crm` exposes a full JSON API alongside its HTML pages. All API routes are
prefixed with `/api`. Interactive, always-up-to-date documentation is also
available once the app is running:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

This document is a human-readable summary; the interactive docs above are
generated directly from the code and are the source of truth.

---

## Authentication

This project does not include authentication out of the box (see
[`docs/CLAUDE_CODE_WORKFLOW.md`](./CLAUDE_CODE_WORKFLOW.md) for suggested
next steps on adding it). All endpoints are open when running locally.

---

## Conventions

- All request/response bodies are JSON.
- Timestamps are ISO 8601 strings.
- Every resource has a numeric `id`, `created_at`, and `updated_at`.
- `PUT` endpoints accept **partial updates** ” only send the fields you want
 to change.
- Successful `DELETE` requests return `204 No Content`.
- Not-found records return `404` with `{"detail": "..."}`.

---

## Companies ” `/api/companies`

| Method | Path | Description |
|---|---|---|
| GET | `/api/companies?q=` | List companies, optional name filter |
| POST | `/api/companies` | Create a company |
| GET | `/api/companies/{id}` | Get one company |
| PUT | `/api/companies/{id}` | Update a company |
| DELETE | `/api/companies/{id}` | Delete a company |

**Create example:**
```bash
curl -X POST http://127.0.0.1:8000/api/companies \
 -H "Content-Type: application/json" \
 -d '{"name": "Acme Corp", "industry": "Manufacturing", "city": "Springfield"}'
```

## Contacts ” `/api/contacts`

Same CRUD shape as Companies. Fields: `first_name`, `last_name`, `email`,
`phone`, `job_title`, `department`, `notes`, `company_id`.

## Customers ” `/api/customers`

Fields: `name`, `status` (`active` / `inactive` / `at_risk` / `churned`),
`lifetime_value`, `owner`, `notes`, `contact_id`, `company_id`.

## Leads ” `/api/leads`

Fields: `title`, `status` (`new` / `contacted` / `qualified` / `unqualified`
/ `converted`), `source` (`website` / `referral` / `cold_outreach` /
`advertisement` / `social_media` / `event` / `other`), `score` (0-100),
`estimated_value`, `description`, `contact_id`, `company_id`.

Query param: `?status=qualified` to filter.

## Deals ” `/api/deals` (Sales Pipeline)

Fields: `title`, `stage` (`prospecting` / `qualification` / `proposal` /
`negotiation` / `closed_won` / `closed_lost`), `value`, `probability` (0-100),
`expected_close_date`, `notes`, `company_id`, `contact_id`, `customer_id`.

Query param: `?stage=negotiation` to filter.

**Move a deal's stage (used by the Kanban board):**
```
POST /pipeline/{deal_id}/stage
Content-Type: application/json

{"stage": "negotiation"}
```

## Tasks ” `/api/tasks`

Fields: `title`, `description`, `status` (`open` / `in_progress` /
`completed` / `cancelled`), `priority` (`low` / `medium` / `high` /
`urgent`), `due_date`, `assignee`, `related_type`, `related_id`.

`related_type` is one of `company`, `contact`, `customer`, `lead`, `deal`,
`meeting` ” combined with `related_id`, it links the task to any record.

## Notes ” `/api/notes`

Fields: `body`, `author`, `related_type`, `related_id`.

Query params: `?related_type=lead&related_id=5` to list notes for one record.

## Meetings ” `/api/meetings`

Fields: `title`, `starts_at`, `ends_at`, `location`, `attendees`, `agenda`,
`notes`, `status` (`scheduled` / `completed` / `cancelled`), `related_type`,
`related_id`.

---

## AI Endpoints ” `/api/ai`

These power the AI features described in the README. They all return `200`
even when AI is not configured ” check the `ai_enabled` field in the
response to distinguish a real AI result from a fallback message.

### `POST /api/ai/draft-email`
```json
{
 "purpose": "Follow up after our demo call",
 "recipient_name": "Priya",
 "context": "They asked about our enterprise pricing.",
 "tone": "professional",
 "related_type": "lead",
 "related_id": 12
}
```
Response: `{"result": "Subject: ...\n\n...", "ai_enabled": true}`

### `POST /api/ai/followups`
```json
{"related_type": "deal", "related_id": 7, "extra_context": "They went quiet after the proposal."}
```
Response: `{"suggestions": ["...", "...", "..."], "ai_enabled": true}`

### `POST /api/ai/customer-insights/{customer_id}`
No body required. Response: `{"result": "...", "ai_enabled": true}`

### Entity-specific AI actions (HTML form endpoints, redirect back to the detail page)

| Endpoint | Effect |
|---|---|
| `POST /leads/{id}/summarize` | Generates and stores `Lead.ai_summary` |
| `POST /meetings/{id}/summarize` | Generates and stores `Meeting.ai_summary` |
| `POST /pipeline/{id}/recommend` | Generates and stores `Deal.ai_recommendation` |

---

## Health Check

```
GET /health
```
```json
{"status": "ok", "app": "ai-powered-crm", "ai_enabled": true}
```

Useful for monitoring, container health checks, and the startup scripts.
