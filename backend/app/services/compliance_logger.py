class ComplianceLogger:
    def record(self, *, actor: str, action: str, entity: str) -> None:
        print(f"AUDIT: {actor} -> {action} on {entity}")
