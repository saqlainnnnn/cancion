from enum import StrEnum


class Frequency(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ApprovalMode(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"


class Action(StrEnum):
    RENEW = "renew"
    SUBSCRIBE = "subscribe"
    BUY = "buy"
    PAY = "pay"
    CANCEL = "cancel"
