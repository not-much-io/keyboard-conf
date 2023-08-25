from typing import (
    Dict,
    Optional,
    List,
    TypedDict,
    Literal,
    Tuple,
    Union,
    NotRequired,
)
from .keys import MODIFIER_KEYS, KeyCode, Modifier


Modifiers = List[Modifier]

_ModifierKindLit = Literal["mandatory", "optional"]


class KeyEvent(TypedDict):
    key_code: KeyCode


class ProducibleKeyEvent(KeyEvent):
    """This is a key event that karabiner produces.

    NOTE: Karabiner WILL attempt to consume a key event it itself produced.
          This means have to be careful to not produce events that get re-consumed.
    """

    modifiers: NotRequired[List[Modifier]]


class ConsumableKeyEvent(KeyEvent):
    """This is a key event that karabiner consumes."""

    # A consumable key even has the concept of mandatory and optional modifiers.
    # The optional modifier just allows more lenient detection of the key event.
    modifiers: NotRequired[
        Dict[_ModifierKindLit, Modifiers]
    ]


def __init__key_event(
    raw_dict: Union[
        "ProducibleKeyEvent", "ConsumableKeyEvent"
    ]
):
    """TypedDicts have no real logic aside from annotations during runtime, thus we inject our own logic.

    This logic is just a helper function to reduce boilerplate for handling symbols.
    """
    raw_dict["key_code"], modifier = translate_symbols(
        raw_dict["key_code"]
    )
    if modifier:
        assert "modifiers" in raw_dict
        if type(raw_dict["modifiers"]) == list:
            raw_dict["modifiers"].append(modifier)
        elif type(raw_dict["modifiers"]) == dict:
            raw_dict["modifiers"]["mandatory"].append(
                modifier
            )
        else:
            raise Exception("Unknown type for modifiers")
    return raw_dict


ConsumableKeyEvent = __init__key_event  # type: ignore
ProducibleKeyEvent = __init__key_event  # type: ignore


def translate_symbols(
    key: KeyCode,
) -> Tuple[KeyCode, Optional[Modifier]]:
    """Symbols often:
    * are shifted variants of other symbols
    * have names for key codes

    This function translates symbols to their key code and modifiers if required.
    The point is just to reduce pointless boilerplate and use easier to read symbols.
    """
    # TODO: It seems my keyboard specifically pressed left shift for some reason.
    #       Right shift just would not work here.
    if key == "<":
        return "comma", MODIFIER_KEYS.left_shift
    if key == ">":
        return "period", MODIFIER_KEYS.left_shift
    if key == "-":
        return "hyphen", None
    if key == "_":
        return "hyphen", MODIFIER_KEYS.left_shift
    if key == ":":
        return "semicolon", MODIFIER_KEYS.left_shift
    if key == ";":
        return "semicolon", None
    if key == " ":
        return "spacebar", None
    if key == ".":
        return "period", None
    if key == ",":
        return "comma", None

    return key, None
