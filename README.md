# My personal keyboard setup

There are three levels of configuration:

* OS (MacOS)
* Generic Software (Karabiner)
* Specific Software (IDEs and Browsers)

The general philosophy is target emacs keybindings for familiarity and to not need special keys like esc, del and arrows.

There will be three kinds of configurations:

* Just remap emacs keycombo to MacOS/generic standard keycombos/keys
  * ex: control+p to up_arrow
* Reconfigure MacOS keybind and then remap emacs to that
  * ex: cut is command+x by default but that conflicts with emacs so remapping MacOS to something random
    * usually mapping to ctrl+opt+cmd+{letter} (it does not matter, just needs something unused and long)
    * then map control+w to new cut keybinding
* For application specific keybinds use their own conf option
  * ex: In IDE conf map control+. to "go to definition"

## Other Notes

Some emacs keymaps are already standard in MacOS:

* C+k - cut to end of line
