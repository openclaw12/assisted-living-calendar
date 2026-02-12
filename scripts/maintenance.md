# Maintenance SOP

- Nightly backup: run `scripts/export_reports.py` + DB dump to S3.
- Weekly: rotate audit logs into cold storage.
- Monthly: execute `scripts/generate_monthly_plan.py` and review conflicts before publishing.
- Quarterly: review vendor contracts and update cost assumptions in `data/fixtures/vendors.json`.
