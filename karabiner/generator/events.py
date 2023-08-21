from .event_utils import ProducibleKeyEvent, ConsumableKeyEvent
from .keys import MODIFIER_KEYS, SPECIFIC_KEYS


class STD_KEYS:
    up = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.up, "modifiers": []})
    down = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.down, "modifiers": []})
    left = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.left, "modifiers": []})
    right = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.right, "modifiers": []})
    esc = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.esc, "modifiers": []})
    backspace = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.backspace, "modifiers": []}
    )
    delete = ProducibleKeyEvent({"key_code": SPECIFIC_KEYS.delete, "modifiers": []})


class STD_MACOS_KEYBIND_EVENTS:
    """There default keybinds are:
    1) Set by default on a fresh MacOS install
    2) Are implemented system wide or at least in most applications
    These are generic keybinds that are not specific to any application.

    NOTE: These are producible key events as we only produce MacOS key events and should never consume them.
    """

    line_start = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.left,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    line_end = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.right,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    file_start = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.up,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    file_end = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.down,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    copy = ProducibleKeyEvent({"key_code": "c", "modifiers": [MODIFIER_KEYS.command]})
    paste = ProducibleKeyEvent({"key_code": "v", "modifiers": [MODIFIER_KEYS.command]})
    undo = ProducibleKeyEvent({"key_code": "z", "modifiers": [MODIFIER_KEYS.command]})
    redo = ProducibleKeyEvent(
        {"key_code": "z", "modifiers": [MODIFIER_KEYS.command, MODIFIER_KEYS.shift]}
    )
    find_in_view = ProducibleKeyEvent(
        {
            "key_code": "f",
            "modifiers": [
                # NOTE: We use the left variant here because we want to use
                #       right_command + F for "Forward Word"
                MODIFIER_KEYS.left_command
            ],
        }
    )
    page_down = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.down, "modifiers": [MODIFIER_KEYS.fn]}
    )
    page_up = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.up, "modifiers": [MODIFIER_KEYS.fn]}
    )
    word_forward = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.right, "modifiers": [MODIFIER_KEYS.option]}
    )
    word_backward = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.left, "modifiers": [MODIFIER_KEYS.option]}
    )
    delete_word_backward = ProducibleKeyEvent(
        {"key_code": SPECIFIC_KEYS.backspace, "modifiers": [MODIFIER_KEYS.option]}
    )
    delete_word_forward = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.delete,
            "modifiers": [MODIFIER_KEYS.option, MODIFIER_KEYS.fn],
        }
    )
    select_all = ProducibleKeyEvent(
        {"key_code": "a", "modifiers": [MODIFIER_KEYS.command]}
    )
    save = ProducibleKeyEvent({"key_code": "s", "modifiers": [MODIFIER_KEYS.command]})


class STD_EMACS_KEYBIND_EVENTS:
    """These keybinds are directly std emacs keybinds and are both application agnostic and not.

    NOTE: These are consumable key events as we only consume Emacs key events and should never produce them.
    """

    ###
    # Generally application agnostic
    ###
    master_search = ConsumableKeyEvent(
        {"key_code": "x", "modifiers": {"mandatory": [MODIFIER_KEYS.command]}}
    )

    up = ConsumableKeyEvent(
        {"key_code": "p", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    down = ConsumableKeyEvent(
        {"key_code": "n", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    left = ConsumableKeyEvent(
        {"key_code": "b", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    right = ConsumableKeyEvent(
        {"key_code": "f", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    word_forward = ConsumableKeyEvent(
        {"key_code": "f", "modifiers": {"mandatory": [MODIFIER_KEYS.command]}}
    )
    word_backward = ConsumableKeyEvent(
        {"key_code": "b", "modifiers": {"mandatory": [MODIFIER_KEYS.command]}}
    )
    line_start = ConsumableKeyEvent(
        {"key_code": "a", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    line_end = ConsumableKeyEvent(
        {"key_code": "e", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    page_up = ConsumableKeyEvent(
        {"key_code": "v", "modifiers": {"mandatory": [MODIFIER_KEYS.command]}}
    )
    page_down = ConsumableKeyEvent(
        {
            "key_code": "v",
            "modifiers": {
                "mandatory": [
                    MODIFIER_KEYS.control,
                ]
            },
        }
    )
    file_start = ConsumableKeyEvent(
        {"key_code": "<", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    file_end = ConsumableKeyEvent(
        {"key_code": ">", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    wipe = ConsumableKeyEvent(
        {"key_code": "w", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    yank = ConsumableKeyEvent(
        {"key_code": "y", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    undo = ConsumableKeyEvent(
        {"key_code": "_", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    redo = ConsumableKeyEvent(
        {
            "key_code": "-",
            "modifiers": {
                "mandatory": [
                    MODIFIER_KEYS.control,
                ]
            },
        }
    )
    delete = ConsumableKeyEvent(
        {"key_code": "d", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    delete_word_backward = ConsumableKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.backspace,
            "modifiers": {"mandatory": [MODIFIER_KEYS.command]},
        }
    )
    delete_word_forward = ConsumableKeyEvent(
        {"key_code": "d", "modifiers": {"mandatory": [MODIFIER_KEYS.command]}}
    )
    cancel = ConsumableKeyEvent(
        {"key_code": "g", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    find_in_view = ConsumableKeyEvent(
        {"key_code": "s", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    mode_switch_general_extend = ConsumableKeyEvent(
        {"key_code": "x", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    select_all = ConsumableKeyEvent(
        {
            "key_code": "h",
        }
    )
    save = ConsumableKeyEvent(
        {"key_code": "s", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    select_mode_toggle = ConsumableKeyEvent(
        {"key_code": "spacebar", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )

    ###
    # Generally application specific
    ###
    find_usages = ConsumableKeyEvent(
        {"key_code": ".", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    go_back = ConsumableKeyEvent(
        {"key_code": ",", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )
    toggle_comment = ConsumableKeyEvent(
        {"key_code": ";", "modifiers": {"mandatory": [MODIFIER_KEYS.control]}}
    )

    show_type_hint = None
    toggle_type_annotations = None
    format_file = None
    rerun = None
    run_shell_cmd = None

    find_file = None
    find_in_files = None
    show_recent_files = None

    pane_split_vertical = None
    pane_split_horizontal = None
    pane_next = None
    pane_close = None


class STD_WINDOW_MANAGER_KEYBIND_EVENTS:
    """TODO: Of secondary importance right now"""

    window_next = None
    window_prev = None
    window_fit_left = None
    window_fit_right = None
    window_throw_next = None


class STD_TABULAR_APPLICATION_KEYBIND_EVENTS:
    """Every application that has tabs should already have these keybinds.

    This class is just to document their existence.
    """

    # TODO
    tab_new = None
    tab_next = None
    tap_prev = None
    tab_close = None


class STD_VSCODE_KEYBIND_EVENTS:
    """We use VSCode as our default editor target keymap because:
    1. It is very widely used so there is a plugin for VSCode keybind in IntelliJ by IntelliJ themselves
    2. We cannot nicely use Emacs keybinds themselves as the target keybinds as karabiner would pick up its own generated keybinds
      2.1. Also emacs keybind plugins tend to be a bit buggy or incomplete
    3. VSCode is Electron based which means some keybinds will work in Browser also for free (like Navigate Back and Forward)
    """

    find_usages = None
    go_back = None
    toggle_comment = None
    show_type_hint = None
    toggle_type_annotations = None
    format_file = None
    rerun = None
    run_shell_cmd = None

    find_file = None
    find_in_files = None
    show_recent_files = None

    pane_split_vertical = None
    pane_split_horizontal = None
    pane_next = None
    pane_close = None


STD_EDITOR_KEYBINDS = STD_VSCODE_KEYBIND_EVENTS
