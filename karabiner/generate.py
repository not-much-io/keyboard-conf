from typing import List, Optional
from copy import deepcopy
from generator.modification_utils import (
    SetVariable,
    Condition,
    Modification,
    ToDelayedAction,
)
from generator.events import (
    STDEmacsKeyEvents,
    STDMacOSKeyEvents,
    STDIdeKeyEvents,
    MODIFIER_KEYS,
)
import json


modifications: List[Modification] = []


class Utils:
    clear_emacs_mode = SetVariable(
        {
            "set_variable": {
                "name": "emacs_mode",
                "value": "none",
            }
        }
    )
    set_emacs_mode_general_extend = SetVariable(
        {
            "set_variable": {
                "name": "emacs_mode",
                "value": "C-x",
            }
        }
    )
    set_emacs_mode_mode_specific = SetVariable(
        {
            "set_variable": {
                "name": "emacs_mode",
                "value": "C-c",
            }
        }
    )
    is_emacs_mode_general_extend = Condition(
        {
            "type": "variable_if",
            "name": "emacs_mode",
            "value": "C-x",
        }
    )
    is_emacs_mode_mode_specific = Condition(
        {
            "type": "variable_if",
            "name": "emacs_mode",
            "value": "C-c",
        }
    )
    is_emacs_mode_none = Condition(
        {
            "type": "variable_if",
            "name": "emacs_mode",
            "value": "none",
        }
    )
    clear_emacs_mode_after_timeout = {
        "to_delayed_action": ToDelayedAction(
            {
                # If no more keys are pressed within timeout, clear the mode.
                # Can just wait a little after triggering by accident to have it get cleared.
                "to_if_invoked": [
                    SetVariable(
                        {
                            "set_variable": {
                                "name": "emacs_mode",
                                "value": "none",
                            }
                        }
                    )
                ],
                # If another key is pressed before the timeout but after resolving an event clear the mode.
                # This is so each command in mode does not have to clear the mode manually.
                # TODO: This does not seem to work how I expected it to, just doing manually for now.
                # "to_if_canceled": [
                #     SetVariable(
                #         {
                #             "set_variable": {
                #                 "name": "emacs_mode",
                #                 "value": "none",
                #             }
                #         }
                #     )
                # ],
            }
        )
    }

    is_select_mode_on = Condition(
        {
            "type": "variable_if",
            "name": "select_mode",
            "value": "on",
        }
    )
    is_select_mode_off = Condition(
        {
            "type": "variable_if",
            "name": "select_mode",
            "value": "off",
        }
    )
    set_select_mode_on = SetVariable(
        {
            "set_variable": {
                "name": "select_mode",
                "value": "on",
            }
        }
    )
    set_select_mode_off = SetVariable(
        {
            "set_variable": {
                "name": "select_mode",
                "value": "off",
            }
        }
    )

    @staticmethod
    def create_select_mode_variant(
        description: str,
    ) -> Modification:
        # Find the original modification
        original_modification: Optional[Modification] = None
        for modification in modifications:
            if modification["description"] == description:
                if original_modification is not None:
                    raise Exception(
                        "Duplicate modification: "
                        + description
                    )
                original_modification = modification
        if original_modification is None:
            raise Exception(
                "Modification not found: " + description
            )

        # Create the variant modification
        variant_modification = deepcopy(
            original_modification
        )
        variant_modification["description"] = (
            "Select Mode: " + description
        )

        # Add the "select mode" condition to the select variant modification
        assert (
            "conditions"
            in variant_modification["manipulators"][0]
        )
        variant_conditions = variant_modification[
            "manipulators"
        ][0]["conditions"]
        # Expecting the one emacs_mode None condition
        assert variant_conditions is not None
        assert (
            len(variant_conditions) == 1
        ), variant_conditions
        variant_conditions.append(Utils.is_select_mode_on)

        # Add the "shift" modifier to the select variant produced event
        variant_to_events = variant_modification[
            "manipulators"
        ][0]["to"]
        assert (
            len(variant_to_events) == 1
        ), variant_to_events
        variant_to_event_modifiers = variant_to_events[
            0
        ].get("modifiers", [])
        variant_to_event_modifiers.append(
            MODIFIER_KEYS.left_shift
        )
        variant_to_events[0]["modifiers"] = variant_to_event_modifiers  # type: ignore

        # Add the "not select mode" condition to the original modification
        assert (
            len(original_modification["manipulators"]) == 1
        )
        assert (
            "conditions"
            in original_modification["manipulators"][0]
        )
        original_conditions = original_modification[
            "manipulators"
        ][0]["conditions"]
        # Expecting the one emacs_mode None condition
        assert original_conditions is not None
        assert (
            len(original_conditions) == 1
        ), original_conditions

        original_conditions.append(Utils.is_select_mode_off)

        return variant_modification

    INDENT = "                    "


# Define the standard modifications
modifications += [
    Modification(
        description="Up",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.up,
                "to": [STDMacOSKeyEvents.up],
            },
        ],
    ),
    Modification(
        description="Down",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.down,
                "to": [STDMacOSKeyEvents.down],
            },
        ],
    ),
    Modification(
        description="Left",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.left,
                "to": [STDMacOSKeyEvents.left],
            },
        ],
    ),
    Modification(
        description="Right",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.right,
                "to": [STDMacOSKeyEvents.right],
            },
        ],
    ),
    Modification(
        description="Forward Word",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.word_forward,
                "to": [STDMacOSKeyEvents.word_forward],
            },
        ],
    ),
    Modification(
        description="Backward Word",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.word_backward,
                "to": [STDMacOSKeyEvents.word_backward],
            },
        ],
    ),
    Modification(
        description="Line Start",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.line_start,
                "to": [STDMacOSKeyEvents.line_start],
            },
        ],
    ),
    Modification(
        description="Line End",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.line_end,
                "to": [STDMacOSKeyEvents.line_end],
            },
        ],
    ),
    Modification(
        description="Page Down",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.page_down,
                "to": [STDMacOSKeyEvents.page_down],
            },
        ],
    ),
    Modification(
        description="Page Up",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.page_up,
                "to": [STDMacOSKeyEvents.page_up],
            },
        ],
    ),
    Modification(
        description="File Start",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.file_start,
                "to": [STDMacOSKeyEvents.file_start],
            },
        ],
    ),
    Modification(
        description="File End",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.file_end,
                "to": [STDMacOSKeyEvents.file_end],
            },
        ],
    ),
    Modification(
        description="Wipe",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.emacs_uniques_keymap.cut,
                "to": [
                    # Emulating cut as real cut through Command + X will be taken by Emacs "action search"
                    STDMacOSKeyEvents.copy,
                    STDMacOSKeyEvents.backspace,
                    # Very often used together with select mode, so clearing select mode here also
                    Utils.set_select_mode_off,
                ],
            },
        ],
    ),
    Modification(
        description="Yank",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.os_level_keymap.paste,
                "to": [STDMacOSKeyEvents.paste],
            },
        ],
    ),
    # NOTE: kill is already standard in all apps on MacOS as "Command + k"
    Modification(
        description="Undo",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.os_level_keymap.undo,
                "to": [STDMacOSKeyEvents.undo],
            },
        ],
    ),
    Modification(
        description="Redo",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.os_level_keymap.redo,
                "to": [STDMacOSKeyEvents.redo],
            },
        ],
    ),
    # NOTE: Using normal backspace instead of Control + h as used to that.
    #       Might be worth changing in the future?
    Modification(
        description="Delete Word Backward",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.delete_word_backward,
                "to": [
                    STDMacOSKeyEvents.delete_word_backward
                ],
            },
        ],
    ),
    Modification(
        description="Delete",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.delete,
                "to": [STDMacOSKeyEvents.delete],
            },
        ],
    ),
    Modification(
        description="Delete Word Forward",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.delete_word_forward,
                "to": [
                    STDMacOSKeyEvents.delete_word_forward
                ],
            },
        ],
    ),
    Modification(
        description="Cancel",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.os_level_keymap.esc,
                "to": [
                    STDMacOSKeyEvents.esc,
                    Utils.clear_emacs_mode,
                    Utils.set_select_mode_off,
                ],
            },
        ],
    ),
    Modification(
        description="Search",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.os_level_keymap.find_in_view,
                "to": [
                    STDMacOSKeyEvents.find_in_view,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Action search",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.std_ide_keymap.action_search,
                "to": [
                    # If already going for action search, no mode has any relevance
                    Utils.clear_emacs_mode,
                    Utils.set_select_mode_off,
                    STDIdeKeyEvents.action_search,
                ],
            },
        ],
    ),
    Modification(
        description="Find references",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.std_ide_keymap.find_references,
                "to": [
                    STDIdeKeyEvents.find_references,
                ],
            },
        ],
    ),
    Modification(
        description="Go back",
        manipulators=[
            {
                "type": "basic",
                "from": STDEmacsKeyEvents.std_ide_keymap.go_back,
                "to": [
                    STDIdeKeyEvents.go_back,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: General Extend",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.emacs_utils_keymap.mode_switch_general_extend,
                "to": [
                    Utils.set_emacs_mode_general_extend,
                ],
                **Utils.clear_emacs_mode_after_timeout,
            },
        ],  # type: ignore
    ),
    Modification(
        description="Emacs Mode: General Extend: Select all",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_general_extend
                ],
                "from": STDEmacsKeyEvents.os_level_keymap.select_all,
                "to": [
                    STDMacOSKeyEvents.select_all,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: General Extend: Save",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_general_extend
                ],
                "from": STDEmacsKeyEvents.os_level_keymap.save,
                "to": [
                    STDMacOSKeyEvents.save,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: General Extend: Focus Next Window",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_general_extend
                ],
                "from": STDEmacsKeyEvents.std_ide_keymap.focus_next_window,
                "to": [
                    STDIdeKeyEvents.focus_next_window,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Find File",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_general_extend
                ],
                "from": STDEmacsKeyEvents.std_ide_keymap.find_file,
                "to": [
                    STDIdeKeyEvents.find_file,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: Mode Specific",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STDEmacsKeyEvents.emacs_utils_keymap.mode_switch_mode_specific,
                "to": [
                    Utils.set_emacs_mode_mode_specific,
                ],
                **Utils.clear_emacs_mode_after_timeout,
            },
        ],  # type: ignore
    ),
    Modification(
        description="Emacs Mode: Mode Specific: Rerun",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_mode_specific
                ],
                "from": STDEmacsKeyEvents.std_ide_keymap.rerun,
                "to": [
                    STDIdeKeyEvents.rerun,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: Mode Specific: Format",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_mode_specific
                ],
                "from": STDEmacsKeyEvents.std_ide_keymap.format_file,
                "to": [
                    STDIdeKeyEvents.format_file,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
    Modification(
        description="Emacs Mode: Mode Specific: Find in Files",
        manipulators=[
            {
                "type": "basic",
                "conditions": [
                    Utils.is_emacs_mode_mode_specific
                ],
                "from": STDEmacsKeyEvents.std_ide_keymap.find_in_files,
                "to": [
                    STDIdeKeyEvents.find_in_files,
                    Utils.clear_emacs_mode,
                ],
            },
        ],
    ),
]

# Define the select mode modifications
modifications += [
    Modification(
        description="Select Mode: On",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_select_mode_off],
                "from": STDEmacsKeyEvents.emacs_utils_keymap.select_mode_toggle,
                "to": [Utils.set_select_mode_on],
            },
        ],
    ),
    Modification(
        description="Select Mode: Off",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_select_mode_on],
                "from": STDEmacsKeyEvents.emacs_utils_keymap.select_mode_toggle,
                "to": [
                    Utils.set_select_mode_off,
                    # clearing whatever is currently selected if any
                    STDMacOSKeyEvents.esc,
                ],
            },
        ],
    ),
    Utils.create_select_mode_variant("Up"),
    Utils.create_select_mode_variant("Down"),
    Utils.create_select_mode_variant("Left"),
    Utils.create_select_mode_variant("Right"),
    Utils.create_select_mode_variant("Forward Word"),
    Utils.create_select_mode_variant("Backward Word"),
    Utils.create_select_mode_variant("Line Start"),
    Utils.create_select_mode_variant("Line End"),
    Utils.create_select_mode_variant("Page Down"),
    Utils.create_select_mode_variant("Page Up"),
    Utils.create_select_mode_variant("File Start"),
    Utils.create_select_mode_variant("File End"),
]

with open("karabiner/karabiner.jsonc") as file:
    while line := file.readline():
        if line.strip().startswith("// ::commands"):
            for i, modification in enumerate(modifications):
                modification = json.dumps(
                    modification, indent=4
                )
                modification = (
                    Utils.INDENT
                    + modification.replace(
                        "\n", "\n" + Utils.INDENT
                    )
                )

                if i == len(modifications) - 1:
                    print(modification, end="\n")
                else:
                    print(modification, end=",\n")
            continue
        if line.strip().startswith("//"):
            continue
        print(line, end="")
