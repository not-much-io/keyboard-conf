from typing import Dict, Set, Optional


class Utils:
    @staticmethod
    def translate_if_symbol(key: str) -> (str, Optional[str]):
        """ Symbols often:
        * are shifted variants of other symbols
        * have names for key codes

        This function translates symbols to their key code and modifiers if required.
        The point is just to reduce pointless boilerplate.
        """
        if key == "<":
            return "comma", "left_shift"
        if key == ">":
            return "period", "left_shift"
        if key == "-":
            return "hyphen", None
        if key == "_":
            return "hyphen", "left_shift"

        return key, None


class SPECIFIC_KEYS:
    esc = {"key_code": "escape"}

    delete = {"key_code": "delete_or_backspace"}

    up = {"key_code": "up_arrow"}
    down = {"key_code": "down_arrow"}
    left = {"key_code": "left_arrow"}
    right = {"key_code": "right_arrow"}


_registry: Set[str] = set()


def validate_keybinding(
    keybinding: Dict,
    # Some keybindings are the same but in different modes
    # So we we demand intentionally supplying the overlap for:
    # 1. Checking there actually is an overlap
    # 2. Circumventing the check for duplicates
    # That is also to say that it is up to the builder to ensure
    # mode conditions are set on both to avoid conflicts
    intended_overlap: Dict = None,
) -> Dict:
    # just so it is hashable
    keybinding_as_str = str(keybinding)
    intended_overlap_as_str = str(intended_overlap)

    if intended_overlap is not None:
        if intended_overlap_as_str != keybinding_as_str:
            raise ValueError(
                "Intended overlap does not match keybinding supplied:\n"
                + intended_overlap_as_str
                + "\n"
                + keybinding_as_str
                + "\n"
            )

    if intended_overlap is None and keybinding_as_str in _registry:
        raise ValueError("Duplicate keybinding detected: " + keybinding_as_str)

    _registry.add(keybinding_as_str)
    return keybinding


class MODIFIERS:
    fn = "fn"

    # We use the right variants for all modifiers
    # See below note about left variants usage
    command = "right_command"
    control = "right_control"
    option = "right_option"
    shift = "right_shift"

    """
    Some keybinding we want to use are already used by MacOS.

    For example Command + F is used for "Find" in most apps.
    We want to use Command + F for "Forward Word" instead.
    But we also want the OS to still detect Command + F as "Find".

    To work around this we need to distinguish between two cases:
    1. Emacs Command + F is being called
    2. MacOS Command + F is being called
    To achieve this we use the fact that in the virtual keyboard we have two 
    modifier keys for each side of the keyboard.

    On the physical keyboard we only have the right variants - right_command, right_option etc.
    So what we can do is:
    1. right_command + F: Forward Word
    2. left_command  + F: Find

    So these left variants of modifier keys should only ever be used in such cases.
    """
    left_command = "left_command"
    left_control = "left_control"
    left_option = "left_option"
    left_shift = "left_shift"


class STD_MACOS_KEYBINDS:
    line_start = validate_keybinding(
        {
            "modifiers": [
                MODIFIERS.control,
            ]
        } | SPECIFIC_KEYS.left
    )
    line_end = validate_keybinding(
        {
            "modifiers": [
                MODIFIERS.control,
            ]
        } | SPECIFIC_KEYS.right
    )
    file_start = validate_keybinding(
        {
            "modifiers": [
                MODIFIERS.command,
            ]
        } | SPECIFIC_KEYS.up
    )
    file_end = validate_keybinding(
        {
            "modifiers": [
                MODIFIERS.command,
            ]
        } | SPECIFIC_KEYS.down
    )
    copy = validate_keybinding(
        {
            "key_code": "c",
            "modifiers": [
                MODIFIERS.command
            ]
        }
    )
    paste = validate_keybinding(
        {
            "key_code": "v",
            "modifiers": [
                MODIFIERS.command
            ]
        }
    )
    undo = validate_keybinding(
        {
            "key_code": "z",
            "modifiers": [
                MODIFIERS.command
            ]
        }
    )
    redo = validate_keybinding(
        {
            "key_code": "z",
            "modifiers": [
                MODIFIERS.command,
                MODIFIERS.shift
            ]
        }
    )
    find_in_view = validate_keybinding(
        {
            "key_code": "f",
            "modifiers": [
                # NOTE: We use the left variant here because we want to use
                #       right_command + F for "Forward Word"
                MODIFIERS.left_command
            ]
        }
    )
    page_down = validate_keybinding(
        {
            "key_code": "down_arrow",
            "modifiers": [
                MODIFIERS.fn
            ]
        }
    )
    page_up = validate_keybinding(
        {
            "key_code": "up_arrow",
            "modifiers": [
                MODIFIERS.fn
            ]
        }
    )
    word_forward = validate_keybinding(
        {
            "key_code": "right_arrow",
            "modifiers": [
                MODIFIERS.option
            ]
        }
    )
    word_backward = validate_keybinding(
        {
            "key_code": "left_arrow",
            "modifiers": [
                MODIFIERS.option
            ]
        }
    )
    delete_word_backward = validate_keybinding(
        {
            "key_code": "delete_or_backspace",
            "modifiers": [
                MODIFIERS.option,
            ]
        }
    )
    delete_word_forward = validate_keybinding(
        {
            "key_code": "delete_or_backspace",
            "modifiers": [
                MODIFIERS.option,
                MODIFIERS.fn
            ]
        }
    )
    # TODO: Does this always work?
    select_all = validate_keybinding(
        {
            "key_code": "a",
            "modifiers": [
                MODIFIERS.command
            ]
        }
    )
    save = validate_keybinding(
        {
            "key_code": "s",
            "modifiers": [
                MODIFIERS.command
            ]
        }
    )


class STD_EMACS_KEYBINDS:
    @staticmethod
    def new_keybind(
        # Just a key, e.g. letter "g" or a symbol like "<"
        key: str,
        # Most cmds use control as modifier but there are some that use Command
        # e.g. "Control + v" for page down vs "Command + v" for page up.
        modifier_key: str = MODIFIERS.control,
    ) -> Dict:
        modifiers = []
        if modifier_key is not None:
            modifiers.append(modifier_key)

        key, modifier = Utils.translate_if_symbol(key)
        if modifier is not None:
            modifiers.append(modifier)

        new_keybind = {
            "modifiers": {
                "mandatory": modifiers
            },
            "key_code": key
        }

        if new_keybind["modifiers"]["mandatory"] == []:
            del new_keybind["modifiers"]

        return new_keybind

    up = validate_keybinding(
        new_keybind("p")
    )
    down = validate_keybinding(
        new_keybind("n")
    )
    left = validate_keybinding(
        new_keybind("b")
    )
    right = validate_keybinding(
        new_keybind("f")
    )

    word_forward = validate_keybinding(
        new_keybind("f", MODIFIERS.command)
    )
    word_backward = validate_keybinding(
        new_keybind("b", MODIFIERS.command)
    )

    line_start = validate_keybinding(
        new_keybind("a")
    )
    line_end = validate_keybinding(
        new_keybind("e")
    )

    page_up = validate_keybinding(
        new_keybind("v", MODIFIERS.command)
    )
    page_down = validate_keybinding(
        new_keybind("v")
    )

    file_start = validate_keybinding(
        new_keybind("<")
    )
    file_end = validate_keybinding(
        new_keybind(">")
    )

    wipe = validate_keybinding(
        new_keybind("w")
    )
    yank = validate_keybinding(
        new_keybind("y")
    )

    undo = validate_keybinding(
        new_keybind("_")
    )
    redo = validate_keybinding(
        new_keybind("-")
    )

    delete = validate_keybinding(
        new_keybind("d")
    )
    delete_word_backward = validate_keybinding(
        new_keybind("delete_or_backspace", MODIFIERS.command)
    )
    delete_word_forward = validate_keybinding(
        new_keybind("d", MODIFIERS.command)
    )

    cancel = validate_keybinding(
        new_keybind("g")
    )

    find_in_view = validate_keybinding(
        new_keybind("s")
    )

    mode_switch_general_extend = validate_keybinding(
        new_keybind("x")
    )
    select_all = validate_keybinding(
        new_keybind("h", modifier_key=None)
    )
    save = validate_keybinding(
        new_keybind("s"),
        intended_overlap=find_in_view
    )

    select_mode_toggle = validate_keybinding(
        new_keybind("spacebar")
    )
