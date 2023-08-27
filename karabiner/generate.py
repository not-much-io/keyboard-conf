from typing import List, Optional
from copy import deepcopy
from generator.modification_utils import (
    SetVariable,
    Condition,
    Modification,
    ToDelayedAction,
)
from generator.events import (
    STD_EMACS_KEYBIND_EVENTS,
    STDMacOSKeyEvents,
    STD_KEYS,
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
    is_emacs_mode_general_extend = Condition(
        {
            "type": "variable_if",
            "name": "emacs_mode",
            "value": "C-x",
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
                "to_if_canceled": [
                    SetVariable(
                        {
                            "set_variable": {
                                "name": "emacs_mode",
                                "value": "none",
                            }
                        }
                    )
                ],
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
                "from": STD_EMACS_KEYBIND_EVENTS.up,
                "to": [STD_KEYS.up],
            },
        ],
    ),
    Modification(
        description="Down",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.down,
                "to": [STD_KEYS.down],
            },
        ],
    ),
    Modification(
        description="Left",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.left,
                "to": [STD_KEYS.left],
            },
        ],
    ),
    Modification(
        description="Right",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.right,
                "to": [STD_KEYS.right],
            },
        ],
    ),
    Modification(
        description="Forward Word",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.word_forward,
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
                "from": STD_EMACS_KEYBIND_EVENTS.word_backward,
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
                "from": STD_EMACS_KEYBIND_EVENTS.line_start,
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
                "from": STD_EMACS_KEYBIND_EVENTS.line_end,
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
                "from": STD_EMACS_KEYBIND_EVENTS.page_down,
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
                "from": STD_EMACS_KEYBIND_EVENTS.page_up,
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
                "from": STD_EMACS_KEYBIND_EVENTS.file_start,
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
                "from": STD_EMACS_KEYBIND_EVENTS.file_end,
                "to": [STDMacOSKeyEvents.file_end],
            },
        ],
    ),
    Modification(
        description="Wipe",
        manipulators=[
            {
                "type": "basic",
                "from": STD_EMACS_KEYBIND_EVENTS.cut,
                "to": [
                    # Emulating cut as real cut through Command + X will be taken by Emacs "action search"
                    STDMacOSKeyEvents.copy,
                    STD_KEYS.backspace,
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
                "from": STD_EMACS_KEYBIND_EVENTS.paste,
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
                "from": STD_EMACS_KEYBIND_EVENTS.undo,
                "to": [STDMacOSKeyEvents.undo],
            },
        ],
    ),
    Modification(
        description="Redo",
        manipulators=[
            {
                "type": "basic",
                "from": STD_EMACS_KEYBIND_EVENTS.redo,
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
                "from": STD_EMACS_KEYBIND_EVENTS.delete_word_backward,
                "to": [STDMacOSKeyEvents.delete_word_backward],
            },
        ],
    ),
    Modification(
        description="Delete",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.delete,
                "to": [STD_KEYS.delete],
            },
        ],
    ),
    Modification(
        description="Delete Word Forward",
        manipulators=[
            {
                "type": "basic",
                "conditions": [Utils.is_emacs_mode_none],
                "from": STD_EMACS_KEYBIND_EVENTS.delete_word_forward,
                "to": [STDMacOSKeyEvents.delete_word_forward],
            },
        ],
    ),
    Modification(
        description="Cancel",
        manipulators=[
            {
                "type": "basic",
                "from": STD_EMACS_KEYBIND_EVENTS.esc,
                "to": [
                    STD_KEYS.esc,
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
                "from": STD_EMACS_KEYBIND_EVENTS.find_in_view,
                "to": [
                    STDMacOSKeyEvents.find_in_view,
                    Utils.clear_emacs_mode,
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
                "from": STD_EMACS_KEYBIND_EVENTS.mode_switch_general_extend,
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
                "from": STD_EMACS_KEYBIND_EVENTS.select_all,
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
                "from": STD_EMACS_KEYBIND_EVENTS.save,
                "to": [
                    STDMacOSKeyEvents.save,
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
                "from": STD_EMACS_KEYBIND_EVENTS.select_mode_toggle,
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
                "from": STD_EMACS_KEYBIND_EVENTS.select_mode_toggle,
                "to": [
                    Utils.set_select_mode_off,
                    # clearing whatever is currently selected if any
                    STD_KEYS.esc,
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
            for modification in modifications:
                modification = json.dumps(
                    modification, indent=4
                )
                modification = (
                    Utils.INDENT
                    + modification.replace(
                        "\n", "\n" + Utils.INDENT
                    )
                )
                print(modification, end=",\n")
            continue
        if line.strip().startswith("//"):
            continue
        print(line, end="")
