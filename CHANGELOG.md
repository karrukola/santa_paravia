## v0.2.0 (2021-12-30)

### Feat

- **paravia.py**: end the game as soon as somebody wins

## v0.1.1 (2021-12-28)

### Fix

- **paravia.py**: include option to buy soldiers in public works phase

## v0.1.0 (2021-12-27)

### Fix

- **paravia.py**: properly declare winner in case more than one player reaches HRH title during turn
- **paravia**: properly evaluate whether all players are dead
- **paravia.py**: properly limit score to change title
- print state purchases as table
- **paravia**: improve user input reading
- **paravia.py**: handle properly user input in state pruchases and adjust taxes phases
- **paravia.py**: set RAND_MAX to 32k
- **paravia.py**: render tables using rich table object
- **paravia.py**: print harvest summary using rich table
- **paravia.py**: do nothing to ensure double precision is used
- **paravia.py**: allow treasury to go below 0

### Refactor

- **__limit10**: avoid using intermediate variable

### Feat

- port game from C reference code
