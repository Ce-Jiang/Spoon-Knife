"""A small, self-contained mock script for testing purposes."""

from dataclasses import dataclass
from unittest.mock import Mock, patch


@dataclass
class Claim:
    claim_id: str
    reserve_amount: float
    status: str = "Open"


class ClaimRepository:
    """Example dependency that would normally access an external system."""

    def get_claim(self, claim_id: str) -> Claim:
        raise NotImplementedError("External data source is not connected.")


class ClaimService:
    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository

    def get_claim_summary(self, claim_id: str) -> str:
        claim = self.repository.get_claim(claim_id)
        return (
            f"Claim {claim.claim_id}: status={claim.status}, "
            f"reserve={claim.reserve_amount:.2f}"
        )


def mock_api_status() -> dict:
    """Return a sample response without making a real API call."""
    return {
        "success": True,
        "environment": "mock",
        "message": "Mock service is available",
    }


def run_mock_demo() -> None:
    repository = Mock(spec=ClaimRepository)
    repository.get_claim.return_value = Claim(
        claim_id="MOCK-001",
        reserve_amount=1_250_000.00,
        status="Open",
    )

    service = ClaimService(repository)
    summary = service.get_claim_summary("MOCK-001")

    repository.get_claim.assert_called_once_with("MOCK-001")
    assert summary == "Claim MOCK-001: status=Open, reserve=1250000.00"

    with patch(__name__ + ".mock_api_status") as mocked_status:
        mocked_status.return_value = {
            "success": True,
            "environment": "patched-mock",
            "message": "Patched response",
        }
        result = mock_api_status()
        assert result["success"] is True
        assert result["environment"] == "patched-mock"

    print(summary)
    print("All mock checks passed.")


if __name__ == "__main__":
    run_mock_demo()
