from cancion.api.mappers.evaluation import (
    to_evaluation_response,
)
from cancion.domain.decision import (
    Decision,
    DecisionOutcome,
)


def test_to_evaluation_response():
    decision = Decision(
        outcome=DecisionOutcome.APPROVE,
        reasons=["Within contract limit"],
    )

    response = to_evaluation_response(decision)

    assert response.outcome == DecisionOutcome.APPROVE
    assert response.reasons == [
        "Within contract limit",
    ]
