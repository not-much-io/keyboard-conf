# Docs

## Application generic

NOTE: some mappings are done just for better compatibility. For example ctrl+f is standard MacOS forward. But some application still use arrow key so using that aswell for better compatibility in different contexts. Also for stuff like navigating non text guis like they were text based (dropdowns up/down)

```text
C : basic command prefix
  // karabiner: to arrows
  b : back char
  f : forward char
  p : previous line
  n : next line

  // karabiner: to command arrow
  a : line start
  e : line ending    
  > : end of file
  < : start of file

  // karabiner: to fn arrow
  v : page down

  // karabiner: to del
  d : delete char forward
  
  // karabiner to MacOS Menu Items:
  // * Edit->Find
  //   * ex. VSCode
  // * Edit->Find->Find..
  //   * ex. Browsers
  s : search file
  
  // karabiner: to command z and command shift z
  _ : undo
  - : redo
  
  // karabiner to MacOS Menu Items:
  // * Edit->Cut
  //   * ex. VSCode, browsers
  // BUG: in IntelliJ the keymap cut seems to overwrite the menu item? Manually added the menu item combo as cut in keymap.
  w : wipe

  // karabiner: to command v
  y : yank

  // default already matches
  k : kill

  // karabiner: to esc  
  g : cancel
  
  // karabiner: shift held navigation mode
  C-spc : start/end selection

M- : basic command variants
  // karabiner to MacOS Menu Items
  // * Go->Back
  // * History->Back
  // * Navigate->Back
  , : go back

  // karabiner: to alt arrow
  b : back word
  f : forward word

  // karabiner: to fn arrow
  v : page down
  
  // karabiner: to alt del and fn alt del
  d : delete word forward
  backspace : delete word backwards

C-x : general extend command
  // karabiner: to command a
  h : select whole file
  // karabiner: to command s
  C-s : save
```

## Application Specific

TODO: define stable keymap that we target from karabiner instead of real keymap

```python

mods1 = [
  "right_command",
  "right_option",
  "right_control",
  "left_shift"
]

def stdFindFile():
  return {
###       "key_code": "1",
      "modifiers": mods1
  }

def stdNextPane():
  return {
      "key_code": "n",
      "modifiers": mods1
  }

def stdNextPane():
  return {
      "key_code": "r",
      "modifiers": mods1
  }

def stdReRun():
  return {
      "key_code": "r",
      "modifiers": mods1
  }
```

```
M- : basic command variants
  // ide-s : find usages
  // browser : navigate forward
  . : go to
  // ide-s : find action
  // browser : select address bar
  x : master search

C-x : general extend command
  ; : toggle comment
  b : switch to "open recent file"
  f : find file
  2 : split view horizontally
  3 : split view vertically
  0 : close view
  O : next view

// application specific for vscode and jetbrains
C-c C- : mode specific extend command
  t : show type info
  c : run/re-run
  f : format
  s : search in files
  r : run shell cmd
  a : toggle type annotations
```
