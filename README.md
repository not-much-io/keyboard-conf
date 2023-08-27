# My personal keyboard configuration

STATUS: Actively iterating

In short:

```text
"I go clickidy clack" -consumable_key_events-> karabiner -producible_key_events-> "system go brrr"
```

## Why?

Because I want to used the same keybindings system wide and I wish to use the keybindings of my choice.

### Why not just use "standard keybinds" of your OS/Applications?

Because there is no real wholistic rhyme or reason to them and many actions do not have keybinds attached to them.

However I DO use:

* Emacs keybindings as SOURCE keybinds that karabiner will consume to produce a standard set of keybinds.
* MacOS and VSCode keybindings as TARGET keybinds that karabiner will produce. Although I need to enhance the standard set to get the functionality I want.

## How?

```text
-emacs_consumable_key_events-> karabiner -std_macos_producible_key_events-> generic_software_actions (e.g. text box actions, tab actions, etc.)
                                         -std_vscode_producible_key_events-> ide_actions (e.g. find references, rerun task, search actions etc.)
                                         -custom_ide_keybinds_key_events-----^
```
