from cancion.common import Action

ACTION_PATTERNS: dict[Action, tuple[str, ...]] = {
    Action.RENEW: (
        "renew",
        "continue",
        "keep",
    ),
    Action.SUBSCRIBE: (
        "subscribe",
        "start subscription",
    ),
    Action.BUY: (
        "buy",
        "purchase",
        "order",
    ),
    Action.PAY: (
        "pay",
        "send",
        "transfer",
    ),
    Action.CANCEL: (
        "cancel",
        "stop",
        "terminate",
    ),
}
