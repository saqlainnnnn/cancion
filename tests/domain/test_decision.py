from cancion.domain.decision import Decision, DecisionOutcome


def test_decision() -> None:
    decision = Decision(
        outcome=DecisionOutcome.APPROVE,
        reasons=[],
    )

    assert decision.outcome is DecisionOutcome.APPROVE
    assert decision.reasons == []
