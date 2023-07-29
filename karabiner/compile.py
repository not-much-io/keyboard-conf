import json

class Utils:
    clear_emacs_mode = {
        "set_variable": {
            "name": "emacs_mode",
            "value": "none"
        }
    }
    clear_select_mode = {
        "set_variable": {
            "name": "select_mode",
            "value": "none"
        }
    }

    @staticmethod
    def basic_cmd(desc: str,
                  key: str,
                  to: dict) -> dict:
        return {
            "description": desc,
            "manipulators": [
                {
                    "type": "basic",
                    "from": {
                        "modifiers": {
                            "mandatory": [
                                "right_control"
                            ]
                        },
                        "key_code": key
                    },
                    "to": to
                }
            ]
        }

    indent = "                    "

class BasicCommands:
    cancel = Utils.basic_cmd("Cancel", "g", [
        {
            "key_code": "escape"
        },
        Utils.clear_emacs_mode
    ])


with open("karabiner/karabiner.jsonc") as file:
    while line := file.readline():
        if line.strip().startswith("// ::"):
            comment_content = line.replace("// ::", "").strip()
            modification = eval(comment_content)
            modification = json.dumps(modification, indent=4)
            modification = Utils.indent + modification.replace("\n", "\n" + Utils.indent)
            print(modification, end=",\n")
            continue
        if line.strip().startswith("//"):
            continue
        print(line, end="")
