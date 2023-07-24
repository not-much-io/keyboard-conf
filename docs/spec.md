# Keyboard keybind specification

```text

// Special cases
// Per application - ex. IDE action search or browser search bar
M-x : master search
// Special case - can this be made global?
C-spc : start/end selection

// The expectation is that these are configured globally and relevant in each application
C : basic command prefix
  // Char related
  b : back char
  f : forward char
  d : delete char forward
  // Line related
  p : previous line
  n : next line
  a : line start
  e : line ending
  // File related
  s : search file
  > : end of file
  < : start of file
  // Actions
  _ : undo
  - : redo
  w : wipe
  k : kill
  y : yank
  , : go back // mirrors IDE go to defn though is generic
  g : cancel (like esc)
M- : basic command variants
  // Word related
  b : back word
  f : forward word
  d : delete word forward
  backspace : delete word backwards

// These are application "category" specific - aka IDE functionality
C-x : general extend command
  // File related
  b : switch to "open recent file"
  f : find file
  s : save file  
  h : select whole file
  // Code related
  . : go to defn
  ; : toggle comment
  t : show type info
  c : run/re-run
  f : format
  r : run shell cmd
  // Window related
  2 : split view horizontally
  3 : split view vertically
  0 : close view
  O : next view

// TODO: for completely application unique keybindings if needed for something
C-x C-
```
