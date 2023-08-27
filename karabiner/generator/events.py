from dataclasses import dataclass
from typing import List, Generic, TypeVar, Union
from .event_utils import (
    ProducibleKeyEvent,
    ConsumableKeyEvent,
)
from .keys import MODIFIER_KEYS, SPECIFIC_KEYS


class STD_KEYS:
    up = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.up,
        }
    )
    down = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.down,
        }
    )
    left = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.left,
        }
    )
    right = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.right,
        }
    )
    esc = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.esc,
        }
    )
    backspace = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.backspace,
        }
    )
    delete = ProducibleKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.delete,
        }
    )


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

    select_next_match: KeyEvent

    run_shell_cmd: KeyEvent
    show_recent_files: KeyEvent
    toggle_type_annotations: KeyEvent
    master_search: KeyEvent

    peek_type_defn: KeyEvent
    rerun: KeyEvent
    pane_split_vertical: KeyEvent
    pane_split_horizontal: KeyEvent
    pane_next: KeyEvent
    pane_close: KeyEvent

    find_usages: KeyEvent
    go_back: KeyEvent
    toggle_comment: KeyEvent
    format_file: KeyEvent
    find_file: KeyEvent
    find_in_files: KeyEvent


@dataclass
class EmacsUtilsKeymap(Generic[KeyEvent]):
    """These key events are used as utilities to implement Emacs keybinds"""

    mode_switch_general_extend: ConsumableKeyEvent
    select_mode_toggle: ConsumableKeyEvent


@dataclass
class EmacsUniquesKeymap:
    cut: ConsumableKeyEvent
    
@dataclass
class EmacsKeymap(
    OsLevelKeymap[ConsumableKeyEvent],
    # StdIdeKeymap[ConsumableKeyEvent],
    EmacsUtilsKeymap[ConsumableKeyEvent],
    EmacsUniquesKeymap,
):
    """These key events are relevant to Emacs specifically"""

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


STDEmacsKeyEvents = EmacsKeymap(
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
    cut=ConsumableKeyEvent(
        {
            "key_code": "w",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
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
    mode_switch_general_extend=ConsumableKeyEvent(
        {
            "key_code": "x",
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
    select_mode_toggle=ConsumableKeyEvent(
        {
            "key_code": "spacebar",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    ),


    # ###
    # # Generally application specific
    # ###
    # find_usages=ConsumableKeyEvent(
    #     {
    #         "key_code": ".",
    #         "modifiers": {
    #             "mandatory": [MODIFIER_KEYS.control]
    #         },
    #     }
    # ),
    # go_back=ConsumableKeyEvent(
    #     {
    #         "key_code": ",",
    #         "modifiers": {
    #             "mandatory": [MODIFIER_KEYS.control]
    #         },
    #     }
    # ),
    # toggle_comment=ConsumableKeyEvent(
    #     {
    #         "key_code": ";",
    #         "modifiers": {
    #             "mandatory": [MODIFIER_KEYS.control]
    #         },
    #     }
    # ),
)

STD_EMACS_KEYBIND_EVENTS = STDEmacsKeyEvents

class _STD_EMACS_KEYBIND_EVENTS:
    """These keybinds are directly std emacs keybinds and are both application agnostic and not.

    NOTE: These are consumable key events as we only consume Emacs key events and should never produce them.
    """

    ###
    # Generally application agnostic
    ###
    master_search = ConsumableKeyEvent(
        {
            "key_code": "x",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
    )

    up = ConsumableKeyEvent(
        {
            "key_code": "p",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    down = ConsumableKeyEvent(
        {
            "key_code": "n",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    left = ConsumableKeyEvent(
        {
            "key_code": "b",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    right = ConsumableKeyEvent(
        {
            "key_code": "f",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    word_forward = ConsumableKeyEvent(
        {
            "key_code": "f",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
    )
    word_backward = ConsumableKeyEvent(
        {
            "key_code": "b",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
    )
    line_start = ConsumableKeyEvent(
        {
            "key_code": "a",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    line_end = ConsumableKeyEvent(
        {
            "key_code": "e",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    page_up = ConsumableKeyEvent(
        {
            "key_code": "v",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
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
        {
            "key_code": "<",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    file_end = ConsumableKeyEvent(
        {
            "key_code": ">",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    wipe = ConsumableKeyEvent(
        {
            "key_code": "w",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    yank = ConsumableKeyEvent(
        {
            "key_code": "y",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    undo = ConsumableKeyEvent(
        {
            "key_code": "_",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
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
        {
            "key_code": "d",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    delete_word_backward = ConsumableKeyEvent(
        {
            "key_code": SPECIFIC_KEYS.backspace,
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
    )
    delete_word_forward = ConsumableKeyEvent(
        {
            "key_code": "d",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.command]
            },
        }
    )
    cancel = ConsumableKeyEvent(
        {
            "key_code": "g",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    find_in_view = ConsumableKeyEvent(
        {
            "key_code": "s",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    mode_switch_general_extend = ConsumableKeyEvent(
        {
            "key_code": "x",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    select_all = ConsumableKeyEvent(
        {
            "key_code": "h",
        }
    )
    save = ConsumableKeyEvent(
        {
            "key_code": "s",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    select_mode_toggle = ConsumableKeyEvent(
        {
            "key_code": "spacebar",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )

    ###
    # Generally application specific
    ###
    find_usages = ConsumableKeyEvent(
        {
            "key_code": ".",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    go_back = ConsumableKeyEvent(
        {
            "key_code": ",",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
    )
    toggle_comment = ConsumableKeyEvent(
        {
            "key_code": ";",
            "modifiers": {
                "mandatory": [MODIFIER_KEYS.control]
            },
        }
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


@dataclass
class NMIO_STD_EDITOR_KEYMAP(Generic[KeyEvent]):
    select_next_match: KeyEvent

    run_shell_cmd: KeyEvent
    show_recent_files: KeyEvent
    toggle_type_annotations: KeyEvent
    master_search: KeyEvent

    peek_type_defn: KeyEvent
    rerun: KeyEvent
    pane_split_vertical: KeyEvent
    pane_split_horizontal: KeyEvent
    pane_next: KeyEvent
    pane_close: KeyEvent

    find_usages: KeyEvent
    go_back: KeyEvent
    toggle_comment: KeyEvent
    format_file: KeyEvent
    find_file: KeyEvent
    find_in_files: KeyEvent


# VsCodeKeymap = NMIO_STD_EDITOR_KEYMAP[ProducibleKeyEvent]()


class STD_VSCODE_KEYBIND_EVENTS:
    """We use VSCode as our default editor target keymap because:
    1. It is very widely used so there is a plugin for VSCode keybind in IntelliJ by IntelliJ themselves
    2. We cannot nicely use Emacs keybinds themselves as the target keybinds as karabiner would pick up its own generated keybinds
      2.1. Also emacs keybind plugins tend to be a bit buggy or incomplete
    3. VSCode is Electron based which means some keybinds will work in Browser also for free (like Navigate Back and Forward)

    ref: https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf
    """

    # TODO: Probably worth implementing eventually?
    run_shell_cmd = None
    show_recent_files = None
    toggle_type_annotations = None

    master_search = ProducibleKeyEvent(
        {
            "key_code": "p",
            "modifiers": [
                MODIFIER_KEYS.command,
                MODIFIER_KEYS.shift,
            ],
        }
    )

    @staticmethod
    def _search(term: str) -> List[ProducibleKeyEvent]:
        """This is just a hack when no keybind exists for a specific action.

        In VSCode search will work so fast as to be unnoticeable.
        In IntelliJ search will be slow enough to actually break sometimes.
        """
        events = [
            STD_VSCODE_KEYBIND_EVENTS.master_search,
        ]
        for c in term:
            events.append(
                ProducibleKeyEvent(
                    {
                        "key_code": c,
                    }
                )
            )
        for _ in range(30 - len(term)):
            events.append(
                ProducibleKeyEvent(
                    {
                        "key_code": "spacebar",
                    }
                )
            )
        events.append(
            ProducibleKeyEvent(
                {
                    "key_code": SPECIFIC_KEYS.enter,
                }
            )
        )
        return events

    # These are hacks as VSCode does not come with default keymaps for these..
    # peek_type_defn = _search("peek type definition")
    # rerun = _search("rerun")
    # pane_split_vertical = _search("split editor left")
    # pane_split_horizontal = _search("split editor down")
    # pane_next = _search("focus next editor group")
    # pane_close = _search("close all editors in group")

    find_usages = ProducibleKeyEvent(
        {
            "key_code": "f12",
            "modifiers": [
                MODIFIER_KEYS.shift,
            ],
        }
    )
    go_back = ProducibleKeyEvent(
        {
            "key_code": "-",
            "modifiers": [
                MODIFIER_KEYS.control,
            ],
        }
    )
    toggle_comment = ProducibleKeyEvent(
        {
            "key_code": "/",
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    format_file = ProducibleKeyEvent(
        {
            "key_code": "f",
            "modifiers": [
                MODIFIER_KEYS.option,
                MODIFIER_KEYS.shift,
            ],
        }
    )
    find_file = ProducibleKeyEvent(
        {
            "key_code": "p",
            "modifiers": [
                MODIFIER_KEYS.command,
            ],
        }
    )
    find_in_files = ProducibleKeyEvent(
        {
            "key_code": "f",
            "modifiers": [
                MODIFIER_KEYS.command,
                MODIFIER_KEYS.shift,
            ],
        }
    )


STD_EDITOR_KEYBINDS = STD_VSCODE_KEYBIND_EVENTS
