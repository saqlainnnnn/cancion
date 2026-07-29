from cancion.api.schemas.evaluation import EvaluationResponse
from cancion.domain.decision import Decision


def to_evaluation_response(
    decision: Decision,
) -> EvaluationResponse:
    """Convert a domain decision into an API response."""

    return EvaluationResponse(
        outcome=decision.outcome,
        reasons=decision.reasons,
    )
