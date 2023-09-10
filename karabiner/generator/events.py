from dataclasses import dataclass
from typing import List, Generic, TypeVar, Union
from .event_utils import (
    ProducibleKeyEvent,
    ConsumableKeyEvent,
)
from .keys import MODIFIER_KEYS, SPECIFIC_KEYS

KeyEvent = TypeVar(
    "KeyEvent",
    bound=Union[ProducibleKeyEvent, ConsumableKeyEvent],
)


@dataclass
class OsLevelKeymap(Generic[KeyEvent]):
    """These key events are relevant OS wide (vs. just in a specific application)"""

    up: KeyEvent
    down: KeyEvent
    left: KeyEvent
    right: KeyEvent
    esc: KeyEvent
    backspace: KeyEvent
    delete: KeyEvent

    line_start: KeyEvent
    line_end: KeyEvent
    file_start: KeyEvent
    file_end: KeyEvent
    copy: KeyEvent
    paste: KeyEvent
    undo: KeyEvent
    redo: KeyEvent
    find_in_view: KeyEvent
    page_down: KeyEvent
    page_up: KeyEvent
    word_forward: KeyEvent
    word_backward: KeyEvent
    delete_word_backward: KeyEvent
    delete_word_forward: KeyEvent
    select_all: KeyEvent
    save: KeyEvent


@dataclass
class StdIdeKeymap(Generic[KeyEvent]):
    """These key events are relevant to IDEs specifically"""

    action_search: KeyEvent
    rerun: KeyEvent
    format_file: KeyEvent
    find_references: KeyEvent
    go_back: KeyEvent
    find_file: KeyEvent
    find_symbol: KeyEvent
    focus_next_window: KeyEvent
    find_in_files: KeyEvent
    toggle_comment: KeyEvent
    peek_type_defn: KeyEvent
    select_next_match: KeyEvent

    # run_shell_cmd: KeyEvent
    # TODO: Honestly these are used so seldom that are they really worth it?
    #       Can just use the search functionality in the IDEs themselves.
    # split_vertical: KeyEvent
    # split_horizontal: KeyEvent
    # toggle_type_annotations: KeyEvent
    # show_recent_files: KeyEvent
    close_window: List[
        KeyEvent
    ]  # eh, leaving as already had it on hand


@dataclass
class EmacsUtilsKeymap(Generic[KeyEvent]):
    """These key events are used as utilities to implement Emacs keybinds"""

    mode_switch_general_extend: ConsumableKeyEvent
    mode_switch_mode_specific: ConsumableKeyEvent
    select_mode_toggle: ConsumableKeyEvent


@dataclass
class EmacsUniquesKeymap:
    cut: ConsumableKeyEvent


@dataclass
class EmacsKeymap:
    """These key events are relevant to Emacs specifically"""

    os_level_keymap: OsLevelKeymap[ConsumableKeyEvent]
    std_ide_keymap: StdIdeKeymap[ConsumableKeyEvent]
    emacs_utils_keymap: EmacsUtilsKeymap[ConsumableKeyEvent]
    emacs_uniques_keymap: EmacsUniquesKeymap


# There default keybinds are:
# 1) Set by default on a fresh MacOS install
# 2) Are implemented system wide or at least in most applications
# These are generic keybinds that are not specific to any application.
STDMacOSKeyEvents = OsLevelKeymap[ProducibleKeyEvent](
    up=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.up,
        }
    ),
    down=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.down,
        }
    ),
    left=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.left,
        }
    ),
    right=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.right,
        }
    ),
    esc=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.esc,
        }
    ),
    backspace=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.backspace,
        }
    ),
    delete=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.delete,
        }
    ),
    line_start=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.left,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    line_end=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.right,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    file_start=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.up,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    file_end=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.down,
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    copy=ProducibleKeyEvent(
        {
            "key_code": "c",
            "modifiers": [MODIFIER_KEYS.command],
        }
    ),
    paste=ProducibleKeyEvent(
        {
            "key_code": "v",
            "modifiers": [MODIFIER_KEYS.command],
        }
    ),
    undo=ProducibleKeyEvent(
        {
            "key_code": "z",
            "modifiers": [MODIFIER_KEYS.command],
        }
    ),
    redo=ProducibleKeyEvent(
        {
            "key_code": "z",
            "modifiers": [
                MODIFIER_KEYS.command,
                MODIFIER_KEYS.shift,
            ],
        }
    ),
    find_in_view=ProducibleKeyEvent(
        {
            "key_code": "f",
            "modifiers": [
                # NOTE: We use the left variant here because we want to use
                #       right_command + F for "Forward Word"
                MODIFIER_KEYS.left_command
            ],
        }
    ),
    page_down=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.down,
            "modifiers": [MODIFIER_KEYS.fn],
        }
    ),
    page_up=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.up,
            "modifiers": [MODIFIER_KEYS.fn],
        }
    ),
    word_forward=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.right,
            "modifiers": [MODIFIER_KEYS.option],
        }
    ),
    word_backward=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.left,
            "modifiers": [MODIFIER_KEYS.option],
        }
    ),
    delete_word_backward=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.backspace,
            "modifiers": [MODIFIER_KEYS.option],
        }
    ),
    delete_word_forward=ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.delete,
            "modifiers": [
                MODIFIER_KEYS.option,
                MODIFIER_KEYS.fn,
            ],
        }
    ),
    select_all=ProducibleKeyEvent(
        {
            "key_code": "a",
            "modifiers": [MODIFIER_KEYS.command],
        }
    ),
    save=ProducibleKeyEvent(
        {
            "key_code": "s",
            "modifiers": [MODIFIER_KEYS.command],
        }
    ),
)

# These keybinds are:
# 1) Set by default on a fresh emacs install
#   OR
# 2) Are often used in emacs modes and plugins
#   OR
# 3) Are just set to something semantically sensible
STDEmacsKeyEvents = EmacsKeymap(
    os_level_keymap=OsLevelKeymap[ConsumableKeyEvent](
        up=ConsumableKeyEvent(
            {
                "key_code": "p",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        down=ConsumableKeyEvent(
            {
                "key_code": "n",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        left=ConsumableKeyEvent(
            {
                "key_code": "b",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        right=ConsumableKeyEvent(
            {
                "key_code": "f",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        word_forward=ConsumableKeyEvent(
            {
                "key_code": "f",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        word_backward=ConsumableKeyEvent(
            {
                "key_code": "b",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        line_start=ConsumableKeyEvent(
            {
                "key_code": "a",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        line_end=ConsumableKeyEvent(
            {
                "key_code": "e",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        page_up=ConsumableKeyEvent(
            {
                "key_code": "v",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        page_down=ConsumableKeyEvent(
            {
                "key_code": "v",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        file_start=ConsumableKeyEvent(
            {
                "key_code": "<",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        file_end=ConsumableKeyEvent(
            {
                "key_code": ">",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        # We do not really use
        copy=ConsumableKeyEvent(
            {
                "key_code": "w",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        paste=ConsumableKeyEvent(
            {
                "key_code": "y",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        undo=ConsumableKeyEvent(
            {
                "key_code": "_",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        redo=ConsumableKeyEvent(
            {
                "key_code": "-",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        delete=ConsumableKeyEvent(
            {
                "key_code": "d",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        delete_word_backward=ConsumableKeyEvent(
            {
                "key_code": SPECIFIC_KEYS.backspace,
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        delete_word_forward=ConsumableKeyEvent(
            {
                "key_code": "d",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.command]
                },
            }
        ),
        backspace=ConsumableKeyEvent(
            {
                "key_code": "h",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        esc=ConsumableKeyEvent(
            {
                "key_code": "g",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        find_in_view=ConsumableKeyEvent(
            {
                "key_code": "s",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        select_all=ConsumableKeyEvent(
            {
                "key_code": "h",
            }
        ),
        save=ConsumableKeyEvent(
            {
                "key_code": "s",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
    ),
    std_ide_keymap=StdIdeKeymap[ConsumableKeyEvent](
        action_search=ConsumableKeyEvent(
            {
                "key_code": "x",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.command,
                    ]
                },
            }
        ),
        rerun=ConsumableKeyEvent(
            {
                "key_code": "c",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        format_file=ConsumableKeyEvent(
            {
                "key_code": "f",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        find_references=ConsumableKeyEvent(
            {
                "key_code": ".",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        go_back=ConsumableKeyEvent(
            {
                "key_code": ",",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        find_file=ConsumableKeyEvent(
            {
                "key_code": "f",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        find_symbol=ConsumableKeyEvent(
            {
                "key_code": ".",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        focus_next_window=ConsumableKeyEvent(
            {
                "key_code": "o",
            }
        ),
        close_window=[
            ConsumableKeyEvent(
                {
                    "key_code": "0",
                }
            )
        ],
        find_in_files=ConsumableKeyEvent(
            {
                "key_code": "s",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        toggle_comment=ConsumableKeyEvent(
            {
                "key_code": ";",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.command,
                    ]
                },
            }
        ),
        peek_type_defn=ConsumableKeyEvent(
            {
                "key_code": "t",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
        select_next_match=ConsumableKeyEvent(
            {
                "key_code": "m",
                "modifiers": {
                    "mandatory": [
                        MODIFIER_KEYS.control,
                    ]
                },
            }
        ),
    ),
    emacs_utils_keymap=EmacsUtilsKeymap[ConsumableKeyEvent](
        mode_switch_general_extend=ConsumableKeyEvent(
            {
                "key_code": "x",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        mode_switch_mode_specific=ConsumableKeyEvent(
            {
                "key_code": "c",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
        select_mode_toggle=ConsumableKeyEvent(
            {
                "key_code": "spacebar",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
    ),
    emacs_uniques_keymap=EmacsUniquesKeymap(
        cut=ConsumableKeyEvent(
            {
                "key_code": "w",
                "modifiers": {
                    "mandatory": [MODIFIER_KEYS.control]
                },
            }
        ),
    ),
)

# Based on VSCode keymaps with holes in default keymap filled in with sensible defaults.
# It does not matter what this is really, the only consideration are:
# 1) The keybinds do not conflict with key events we try to consume (to avoid produce-consume loops)
# 2) The keybinds are sensibly complete for the StdIdeKeymap
# 3) The keybinds are much used - meaning there is probably a keymap plugin for it in mainstream IDEs
# Also considered IntelliJ keymap as default but it has a few more holes and is probably less supported by plugins.
STDIdeKeyEvents = StdIdeKeymap[ProducibleKeyEvent](
    action_search=ProducibleKeyEvent(
        {
            "key_code": "p",
            "modifiers": [
                MODIFIER_KEYS.command,
                MODIFIER_KEYS.shift,
            ],
        }
    ),
    rerun=ProducibleKeyEvent(
        {
            "key_code": "f1",
        }
    ),
    format_file=ProducibleKeyEvent(
        {
            "key_code": "f",
            "modifiers": [
                MODIFIER_KEYS.option,
                MODIFIER_KEYS.shift,
            ],
        }
    ),
    find_references=ProducibleKeyEvent(
        {
            "key_code": "f12",
        }
    ),
    go_back=ProducibleKeyEvent(
        {
            "key_code": "-",
            "modifiers": [
                MODIFIER_KEYS.control,
            ],
        }
    ),
    find_file=ProducibleKeyEvent(
        {
            "key_code": "p",
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    find_symbol=ProducibleKeyEvent(
        {
            "key_code": "t",
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    focus_next_window=ProducibleKeyEvent(
        {
            "key_code": "f2",
        }
    ),
    find_in_files=ProducibleKeyEvent(
        {
            "key_code": "f3",
        }
    ),
    toggle_comment=ProducibleKeyEvent(
        {
            "key_code": "/",
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    ),
    peek_type_defn=ProducibleKeyEvent(
        {
            "key_code": "f4",
        }
    ),
    close_window=[
        ProducibleKeyEvent(
            {
                "key_code": "k",
                "modifiers": [
                    MODIFIER_KEYS.command,
                ],
            }
        ),
        ProducibleKeyEvent(
            {
                "key_code": "w",
            }
        ),
    ],
    select_next_match=ProducibleKeyEvent(
        {
            "key_code": "d",
            "modifiers": [
                # Left variant to avoid conflict with delete word forward
                MODIFIER_KEYS.left_command,
            ],
        }
    ),
)


class STD_WINDOW_MANAGER_KEYBIND_EVENTS:
    """TODO: Of secondary importance right now"""

    window_next = None
    window_prev = None
    window_fit_left = None
    window_fit_right = None
    window_throw_next = None
