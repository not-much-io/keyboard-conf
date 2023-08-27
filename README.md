# My personal keyboard configuration

STATUS: Actively iterating
DISCLAIMER: Just for my use, not intended to be generic.

In short:

```text
"go clickidy clack" -consumable_key_events-> karabiner -producible_key_events-> "system go brrr"
```

## Why?

Because I want to used the same keybindings system wide and I wish to use the keybindings of my choice.

### Why not just use "standard keybinds" of your OS/Applications?

Because there is no real wholistic rhyme or reason to them and many actions do not have keybinds attached to them.

However I DO use:

* A standard set of SOURCE keybinds based on emacs standard keybinds or semantic addition that karabiner CONSUMES
  * note: this is the only user facing set I use
* A standard set of TARGET keybind based on MacOS and VSCode standard keybinds or semantic addition that karabiner PRODUCES
  * note: these are just implementation details. The user does not need to know them.

### Why not configure applications with plugins or configuration options?

Because that is a lot of configuration to manage if doing myself and plugins are often implemented incompletely, inconsistently or what they implement does not match my requirements.

Via this project all configuration is in one place and I can easily manage it.

## How?

```text
-emacs_consumable_key_events-> karabiner -std_macos_producible_key_events-> generic_software_actions (e.g. text box actions, tab actions, etc.)
                                         -std_vscode_producible_key_events-> ide_actions (e.g. find references, rerun task, search actions etc.)
                                         -custom_ide_keybinds_key_events-----^
```

### From scratch setup

1. Install karabiner
2. `make karabiner-install`
3. On any editor install a vscode keybind extension (e.g. I used the VSCode keymap extension in Intellij)

At this point most keybinds will work out of the box.

To get full feature set need to add some keybinds outside the standard set in VSCode. See vscode/keybindings.json for those.
And depending on how well the VSCode keymap extension is implemented for any editor may need to add some keybinds there aswell.
