
# Custom Mod Messages

Credit to [Mango0x45](https://github.com/Mango0x45/retime.mcbe.wtf/blob/master/docs/custom_mod_messages.md) 
for my general plagiarism of his guide.

All of these variables are supported in mod messages. To use a variable, place one of 
the below items in brackets, like this. `Good Morning! Your run was timed to {TT}.`

- `FPS` (Frames per Second)

- `TT` (Total Time)
	- In the format `H:MM:SS.xxx`
	- If the run is less than an hour then hours are not shown (`M:SS.xxx`)
	- Milliseconds use 3 place precision
	- If the run is less than a minute, `0` is shown for the minutes (`0:SS.xxx`)

- `H` (Hours)

- `M` (Minutes)

- `S` (Seconds)

- `MS` (Milliseconds)

- `PM` (Padded Minutes)
	- `5` becomes `05`, `18` remains `18`

- `PS` (Padded Minutes)
	- `5` becomes `05`, `18` remains `18`

- `1MS` (1 Place Precision Milliseconds)
	- `.466` becomes `.5`, `.421` becomes `.4`

- `2MS` (2 Place Precision Milliseconds)
	- `.466` becomes `.47`, `.4` becomes `.40`

- `TS` (Start Time)
	- represented as `ST` except it uses the starting frame.

- `TE` (End Time)
	- represented as `TT` except it uses the ending frame.

- `FS` (Start Frame)

- `FE` (End Frame)

- `FT` (Total Frames)

## Example Usage

Custom mod message:
```
Mod Note: Retimed to {H}h {M}m {S}s {3MS}ms
```

Output:
```
Mod Note: Retimed to 0h 6m 18s 000ms
```

Custom mod message:
```
Retimed! {M}'{PS}"{3MS}
```

Output:
```
Retimed! 5'09"167
```

If you want to be lazy, just use:
```
Mod Note: Retimed to {TT}.
```

Output:
```
Mod Note: Retimed to 1:54:23.233.
```