KeyCode = str
Modifier = str


class SPECIFIC_KEYS:
    esc: KeyCode = "escape"

    backspace: KeyCode = "delete_or_backspace"
    delete: KeyCode = "delete"

    up: KeyCode = "up_arrow"
    down: KeyCode = "down_arrow"
    left: KeyCode = "left_arrow"
    right: KeyCode = "right_arrow"


class MODIFIER_KEYS:
    fn: Modifier = "fn"

    # We use the right variants for all modifiers
    # See below note about left variants usage
    command: Modifier = "right_command"
    control: Modifier = "right_control"
    option: Modifier = "right_option"
    shift: Modifier = "right_shift"

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
    left_command: Modifier = "left_command"
    left_control: Modifier = "left_control"
    left_option: Modifier = "left_option"
    left_shift: Modifier = "left_shift"
