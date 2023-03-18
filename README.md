# ![Logo](https://media.discordapp.net/attachments/902396118976061461/1042515141658419200/32.png) Jerrin's Retiming Tool

A program made to help speedrun moderators retime runs that have multiple splits.

![Screenshot of the program](https://cdn.discordapp.com/attachments/682750811008139305/1079190212346916935/image.png)

## Features:
**Save your progress!**
Closing the window does not delete your progress.

**Add Infinitely many rows of splits!**
When they go off the window, a scrollbar will appear.
    
**Custom FPS**  
Defaulted on 30fps. Allows 0 to 999.

**Copy Mod Message**  
Allows for easy mod messages when verifying runs.

**+ | – Splits**  
Click the + or – button to toggle between a row counting as addition or subtraction.
When

**Easy timing!**  
- The textboxes support numbers in these syntax's:
    - youtube debug info
    - 0
    - 0.123
    - 1:10:42.222
    - -5 😳

**Auto Updates!**  
Whenever I publish a new version, an update button will appear on the menu bar.

**Compact Mode**  
![Screenshot of compact mode](https://media.discordapp.net/attachments/682750811008139305/1079197542451003392/image.png)

This can be used when you don't need the full window.  
Closing it will re-open the main window, or by clicking its open keybind again.

## Settings
**Window Style**  
Pick from different styles your OS offers!

**Theme Color**  
After changing, requires a restart to show. Choose from Yellow, Green, Cyan and Purple!

**Show Paste Buttons**  
Toggles the Paste Button's visibility.

**Show Sub-load Textboxes**  
Toggles sub-loads / the modifier text box's visibility.

**Show Text Hints**  
Toggles whether or not "Start...", "End...", and "Total..." are visible.


## Templates
The program has a template feature, allowing you to save and open saved template files.

## Custom Mod Messages
You can customize mod messages with this feature.
Check out MOD_FORMAT.md for more information.

## Menu Bar

### 1. File
- **Open Folder** - Brings you to the Documents/ folder it's data resides in.
- **Single Row Mode** - Opens a smaller, less versatile window, only has one start and one end time.
- **Settings** - The place to fiddle with things.

### 2. Edit
- **Copy Rows as Text** - Copies rows as text.
- **Clear Rows** - Clears all rows.
- **Clear Times** - Clears all times.

### 2. Templates
- **Open Template** - Open saved template files.
- **Save Template** - Save Current Rows as a template file.

### 3. Websites
- **Moderation Hub** - Easy link to SR.C. Mod Hub!
- **Edit Pages** - [TBD] :)

### 4. About
- **GitHub** - Brings you to the GitHub page, obviously
- **How to Use** - Will bring the user to a YouTube video going over all the features.
- **Credits** -

# Developing

If you wish to develop this you will need python 3 and virtualenv.

To set up the environment run the following commands

```sh
virtualenv venv
# append .fish/.csh/.nu/.ps1 depending on your shell
source venv/bin/activate
python -m pip install -r requirements/base.txt
```

To start the program run 

```sh
python src/main/python/main.py
```

