from cancion.api.dependencies import get_intent_parser
from cancion.intent.regex.parser import RegexIntentParser


def test_get_intent_parser_returns_regex_parser():
    parser = get_intent_parser()

    assert isinstance(parser, RegexIntentParser)
