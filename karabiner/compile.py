from typing import List, Dict, Optional
from collections import OrderedDict
from copy import deepcopy
import json
import keys


class Utils:
    complex_mods_registry = OrderedDict()

    clear_emacs_mode = {
        "set_variable": {
            "name": "emacs_mode",
            "value": "none"
        }
    }
    set_emacs_mode_general_extend = {
        "set_variable": {
            "name": "emacs_mode",
            "value": "C-x"
        }
    }
    is_emacs_mode_general_extend = {
        "type": "variable_if",
        "name": "emacs_mode",
        "value": "C-x"
    }
    is_emacs_mode_none = {
        "type": "variable_if",
        "name": "emacs_mode",
        "value": "none"
    }
    clear_emacs_mode_after_timeout = {
        "to_delayed_action": {
            # If no more keys are pressed within timeout, clear the mode.
            # Can just wait a little after triggering by accident to have it get cleared.
            "to_if_invoked": [
                {
                    "set_variable": {
                        "name": "emacs_mode",
                        "value": "none"
                    }
                }
            ]
            # If another key is pressed before the timeout but after resolving an event clear the mode.
            # This is so each command in mode does not have to clear the mode manually.
            # TODO: This does not seem to work how I expected it to, just doing manually for now.
            # "to_if_canceled": [
            #     {
            #         "set_variable": {
            #             "name": "emacs_mode",
            #             "value": "none"
            #         }
            #     }
            # ]
        }
    }

    is_select_mode_on = {
        "type": "variable_if",
        "name": "select_mode",
        "value": 1
    }
    is_select_mode_off = {
        "type": "variable_if",
        "name": "select_mode",
        "value": 0
    }
    set_select_mode_on = {
        "set_variable": {
            "name": "select_mode",
            "value": 1
        }
    }
    set_select_mode_off = {
        "set_variable": {
            "name": "select_mode",
            "value": 0
        }
    }

    @staticmethod
    def new_cmd(
        desc: str,
        from_: Dict,
        to: List[Dict],
        conditions: List[Dict] = [],
        # This is only relevant for emacs mode switching
        to_delayed_action: Optional[Dict] = None,
    ) -> Dict:
        """ NOTE: Every command should finally be created through this function.
        """
        modification = {
            "description": desc,
            "conditions": conditions,
            "manipulators": [
                {
                    "type": "basic",
                    "from": from_,
                    "to": to
                }
            ]
        }

        if to_delayed_action:
            modification["manipulators"][0]["to_delayed_action"] = to_delayed_action

        if desc in Utils.complex_mods_registry:
            raise RuntimeError(f"Duplicate description: {desc}")
        # deepcopy avoids any accidental mutation
        Utils.complex_mods_registry[desc] = deepcopy(modification)

        return modification

    @staticmethod
    def new_basic_cmd(
        desc: str,
        from_: Dict,
        to: List[Dict],
        # Aside from a few exceptions, most basic commands are only
        # relevant in none emacs mode
        # e.g. Cancel/Escape is relevant in any mode
        conditions: List[Dict] = [is_emacs_mode_none]
    ) -> Dict:
        return Utils.new_cmd(
            desc,
            from_,
            to,
            conditions
        )

    @staticmethod
    def new_switch_emacs_mode_cmd(
        desc: str,
        from_: List[Dict],
        to: List[Dict],
    ) -> Dict:
        return Utils.new_cmd(
            desc,
            from_,
            to,
            # TODO: Probably something more advanced will be needed here
            #       as we want to be able to switch modes from any mode
            conditions=[Utils.is_emacs_mode_none],
            to_delayed_action=Utils.clear_emacs_mode_after_timeout
        )

    @staticmethod
    def new_general_extend_command(
        desc: str,
        from_: List[Dict],
        to: List[Dict],
    ) -> Dict:
        # Must always be present - a bit implicit but it's fine
        # Might even be removed if can get to_delayed_action working fully
        to.append(Utils.clear_emacs_mode)
        return Utils.new_cmd(
            desc,
            from_,
            to,
            conditions=[Utils.is_emacs_mode_general_extend],
        )

    @staticmethod
    def new_select_mode_movements_variant(desc: str):
        """ Finds the command with the given description and creates a variant that will:
        1) only be active when select mode is on
        2) that adds shift to the target modifier
        So movements become shift + movement

        To stop the originals from getting triggered when select mode is on we also
        add a condition to the originals. This is a bit "random mutation" but it's fine for now.

        This condition based logic is probably better than depending on ordering in the list which 
        is the other option to achieve the same thing.
        """
        original = Utils.complex_mods_registry[desc]
        
        new_desc = f"{desc} (Select Mode)"
        new_cond = deepcopy(original["conditions"])
        new_cond.append(Utils.is_select_mode_on)
        new_to_mods = deepcopy(original["manipulators"][0]["to"][0].get(
            "modifiers",
            []
        ))
        new_to_mods.append(keys.MODIFIERS.shift)
        new_to = deepcopy(original["manipulators"][0]["to"])
        new_to[0]["modifiers"] = new_to_mods
        new_from = deepcopy(original["manipulators"][0]["from"])

        Utils.new_cmd(
            desc=new_desc,
            from_=new_from,
            to=new_to,
            conditions=new_cond,
        )
        
        original["conditions"].append(Utils.is_select_mode_off)

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

    indent = "                    "


def create_keybinds():
    ###
    # Movement
    ###

    # Basic arrow keys
    # These keybindings actually work in a lot of contexts already however arrow keys are more
    # widely applicable and give a more consistent experience.
    # e.g. in dropdowns the "emacs" keybindings don't work but arrow keys do
    Utils.new_basic_cmd(
        "Up",
        from_=keys.STD_EMACS_KEYBINDS.up,
        to=[keys.SPECIFIC_KEYS.up],
    )
    Utils.new_basic_cmd(
        "Down",
        from_=keys.STD_EMACS_KEYBINDS.down,
        to=[keys.SPECIFIC_KEYS.down],
    )
    Utils.new_basic_cmd(
        "Left",
        from_=keys.STD_EMACS_KEYBINDS.left,
        to=[keys.SPECIFIC_KEYS.left],
    )
    Utils.new_basic_cmd(
        "Right",
        from_=keys.STD_EMACS_KEYBINDS.right,
        to=[keys.SPECIFIC_KEYS.right],
    )

    # Word forward/backward
    Utils.new_basic_cmd(
        "Forward Word",
        from_=keys.STD_EMACS_KEYBINDS.word_forward,
        to=[keys.STD_MACOS_KEYBINDS.word_forward],
    )
    Utils.new_basic_cmd(
        "Backward Word",
        from_=keys.STD_EMACS_KEYBINDS.word_backward,
        to=[keys.STD_MACOS_KEYBINDS.word_backward],
    )

    # Line start/end
    Utils.new_basic_cmd(
        "Line Start",
        from_=keys.STD_EMACS_KEYBINDS.line_start,
        to=[keys.STD_MACOS_KEYBINDS.line_start],
    )
    Utils.new_basic_cmd(
        "Line End",
        from_=keys.STD_EMACS_KEYBINDS.line_end,
        to=[keys.STD_MACOS_KEYBINDS.line_end],
    )

    # Page up/down
    Utils.new_basic_cmd(
        "Page Down",
        from_=keys.STD_EMACS_KEYBINDS.page_down,
        to=[keys.STD_MACOS_KEYBINDS.page_down],
    )
    Utils.new_basic_cmd(
        "Page Up",
        from_=keys.STD_EMACS_KEYBINDS.page_up,
        to=[keys.STD_MACOS_KEYBINDS.page_up],
    )

    # File start/end
    Utils.new_basic_cmd(
        "File Start",
        from_=keys.STD_EMACS_KEYBINDS.file_start,
        to=[keys.STD_MACOS_KEYBINDS.file_start],
    )
    Utils.new_basic_cmd(
        "File End",
        from_=keys.STD_EMACS_KEYBINDS.file_end,
        to=[keys.STD_MACOS_KEYBINDS.file_end],
    )

    ###
    # Copy, Paste related
    ###
    Utils.new_basic_cmd(
        "Wipe",
        from_=keys.STD_EMACS_KEYBINDS.wipe,
        to=[
            # Emulating cut as real cut through Command + X will be taken by Emacs "action search"
            keys.STD_MACOS_KEYBINDS.copy,
            keys.SPECIFIC_KEYS.delete,
        ],
    )
    Utils.new_basic_cmd(
        "Yank",
        from_=keys.STD_EMACS_KEYBINDS.yank,
        to=[keys.STD_MACOS_KEYBINDS.paste],
    )
    # NOTE: kill is already standard in all apps on MacOS as "Command + k"

    ###
    # Undo, Redo
    ###
    Utils.new_basic_cmd(
        "Undo",
        from_=keys.STD_EMACS_KEYBINDS.undo,
        to=[keys.STD_MACOS_KEYBINDS.undo],
        conditions=None,  # relevant in any mode
    )
    Utils.new_basic_cmd(
        "Redo",
        from_=keys.STD_EMACS_KEYBINDS.redo,
        to=[keys.STD_MACOS_KEYBINDS.redo],
        conditions=None,  # relevant in any mode
    )

    ###
    # Delete
    ###
    # NOTE: Using normal backspace instead of Control + h as used to that.
    #       Might be worth changing in the future?
    Utils.new_basic_cmd(
        "Delete Word Backward",
        from_=keys.STD_EMACS_KEYBINDS.delete_word_backward,
        to=[keys.STD_MACOS_KEYBINDS.delete_word_backward],
    )
    Utils.new_basic_cmd(
        "Delete",
        from_=keys.STD_EMACS_KEYBINDS.delete,
        to=[keys.SPECIFIC_KEYS.delete],
    )
    Utils.new_basic_cmd(
        "Delete Word Forward",
        from_=keys.STD_EMACS_KEYBINDS.delete_word_forward,
        to=[keys.STD_MACOS_KEYBINDS.delete_word_forward],
    )

    ###
    # Other specific key remaps
    ###
    Utils.new_basic_cmd(
        "Cancel",
        from_=keys.STD_EMACS_KEYBINDS.cancel,
        to=[
            keys.SPECIFIC_KEYS.esc,
            Utils.clear_emacs_mode,
        ],
        conditions=None,  # relevant in any mode
    )

    ###
    # Search
    ###
    Utils.new_basic_cmd(
        "Search",
        from_=keys.STD_EMACS_KEYBINDS.find_in_view,
        to=[
            keys.STD_MACOS_KEYBINDS.find_in_view,
            Utils.clear_emacs_mode,
        ],
    )

    ###
    # Emacs Mode General Extend
    ###
    Utils.new_switch_emacs_mode_cmd(
        "Emacs Mode: General Extend",
        from_=keys.STD_EMACS_KEYBINDS.mode_switch_general_extend,
        to=[
            Utils.set_emacs_mode_general_extend
        ]
    )
    Utils.new_general_extend_command(
        "select all",
        from_=keys.STD_EMACS_KEYBINDS.select_all,
        to=[keys.STD_MACOS_KEYBINDS.select_all]
    )
    Utils.new_general_extend_command(
        "save",
        from_=keys.STD_EMACS_KEYBINDS.save,
        to=[keys.STD_MACOS_KEYBINDS.save]
    )

    ###
    # Select Mode
    ###
    Utils.new_cmd(
        "Select Mode: On",
        from_=keys.STD_EMACS_KEYBINDS.select_mode_toggle,
        to=[Utils.set_select_mode_on],
        conditions=[Utils.is_select_mode_off]
    )
    Utils.new_cmd(
        "Select Mode: Off",
        from_=keys.STD_EMACS_KEYBINDS.select_mode_toggle,
        to=[
            Utils.set_select_mode_off,
            # clearing whatever is currently selected if any
            keys.SPECIFIC_KEYS.esc,
        ],
        conditions=[Utils.is_select_mode_on]
    )
    
    Utils.new_select_mode_movements_variant("Up")
    Utils.new_select_mode_movements_variant("Down")
    Utils.new_select_mode_movements_variant("Left")
    Utils.new_select_mode_movements_variant("Right")
    Utils.new_select_mode_movements_variant("Forward Word")
    Utils.new_select_mode_movements_variant("Backward Word")
    Utils.new_select_mode_movements_variant("Line Start")
    Utils.new_select_mode_movements_variant("Line End")
    Utils.new_select_mode_movements_variant("Page Down")
    Utils.new_select_mode_movements_variant("Page Up")
    # Will these work or will it not register the same keybind with the extra shift?
    Utils.new_select_mode_movements_variant("File Start")
    Utils.new_select_mode_movements_variant("File End")

create_keybinds()

with open("karabiner/karabiner.jsonc") as file:
    while line := file.readline():
        if line.strip().startswith("// ::commands"):
            for modification in Utils.complex_mods_registry.values():
                modification = json.dumps(modification, indent=4)
                modification = Utils.indent + \
                    modification.replace("\n", "\n" + Utils.indent)
                print(modification, end=",\n")
            continue
        if line.strip().startswith("//"):
            continue
        print(line, end="")
