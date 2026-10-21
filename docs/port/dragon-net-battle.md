# Wii Dragon Net Battle menu in the PC port

With the Wii assets extracted, the PS2 main-menu plate **Dragon Net Battle** opens the Wii mode's top-level choices
in the port's screen mode. Without those assets, it opens the PC online window over the main menu as before.
Nintendo WFC Battle opens its Wii battle menu. Custom Battle opens a matching page with **1 VS 1 Battle**,
**Team Battle**, **10 DP Team Battle**, **15 DP Team Battle**, and **20 DP Team Battle**. Each entry opens
the Wii opponent-search screen with its matching battle rules.
When another player is found, the VS screen shows both player names and "Opponent found!" for about three seconds
before the existing online session launcher starts the battle. Triangle cancels
the search and returns to Custom Battle. Friend Battle keeps its original label and disabled appearance in
the main battle menu; it does not open a screen. The Custom Battle option and all five submenu entries
use their normal, enabled colors. The opponent-search screen alone uses the Custom Battle header.
Normal Battle, Ranking Battle, View Ranking, and Battle Record remain unavailable.
By default, these entries use the existing direct lobby and battle session, with no matchmaking Worker, build
key, or internet connection. The first copy on one computer hosts on UDP port 25443; a second copy on that
computer joins over loopback. For two computers on a LAN, start the host with `BT3_LAN=host` and the other with
`BT3_LAN=join:<host IPv4 address>`, then choose the same entry on both. Allow UDP port 25443 through the host's
firewall. The direct LAN greeting includes the selected battle mode; different entries stay in search instead of
starting a match. Set `BT3_LAN=online` to use the public quick-match queues (S, T, D10, D15, D20); that service may
require an official signed release. Alternatively, test those queues with your own Worker via `BT3_MATCH_URL`; see
[the Worker setup](../../port/matchmaking/README.md).
The separate **Tenkaichi Budokai Online** plate still opens its in-game hub.
Manage Friends and Initialize Wi-Fi Data stay in the menu with a dimmed appearance when unfocused. Both can
receive focus and play the selection sound, but they do not open a screen because their online services are
unavailable in the PC reconstruction. User Settings opens a page with Create Player Name and
Initialize Wi-Fi Data, using the Wii label sheets. Create Player Name reuses the complete Data Center Password Input keyboard movie: backing, glyphs,
selected characters, arrows, delete mark and bottom buttons. Its original selection, release and confirmation
animations run unchanged. The movie is shifted upward by 30 pixels as one unit to meet the name field;
individual keys and captions are not repositioned. The password movie's root entrance is settled on opening,
then the name page moves the entire keyboard with the field during its entrance.
The Wii resource 13 frame, title, underline cursor and typed characters supply the name field above the keyboard.
The name field mirrors the Wii frame's half-width art and shows Giru behind it. Typed characters are vertically
centered inside the field.
Pan remains visible in User Settings and leaves as the keyboard opens. Giru stays beside her on the settings page,
then follows the 30 position samples of the Wii `fl_1` movie into the name field and turns toward it during the
keyboard entrance. The settings page keeps Giru at his home position and original size. The keyboard backing,
glyphs, captions, and text field share the Wii nickname movie's 16-frame entrance.
Returning from User Settings preserves the home positions without replaying their entrance. Both characters keep
their continuous idle movement.
The settings header uses the Wii **User Settings** title from section 0, resource 4, texture 3, with the
existing header animation.
Decide saves the name to `net_name` in `bt3_settings.txt` and updates the
online name used by the port. Initialize Wi-Fi Data remains unavailable. The Wii home screen omits the port's bottom
right Enter and Back hints.

Extract the menu from a Wii disc you own:

```sh
python3 port/tools/extract_wii_online.py roms/RDSPAF.rvz
```

You can also include it in the normal install, with either a European Wii `.iso` or `.rvz` compressed image:

```sh
python3 install.py --iso /path/to/usa.iso --eu-iso roms/SLES-54945.iso --eu-wii-iso roms/RDSPAF.rvz --rebuild
```

This requires Dolphin's `dolphin-tool`; `--dolphin-tool PATH` selects an executable for either command. The
installer writes the Wii assets to `gamedata/dragon-net-battle/` after the build. An already extracted
`wzs3eu1.afs` or `wzs3us1.afs` can be given instead; pass the matching `wzs3eu2.afs` or `wzs3us2.afs`
with `--voice-afs PATH` to include the dialogue voices. Without it, an AFS input still extracts text and lip tracks.
With an ISO or RVZ input, the script extracts the second archive automatically. The script reads the archive's filename table, decodes
the DragonNe pack's BPE sections, writes native resource binaries and the GX I4/C4/C8 sheets as PNG, and makes
`gamedata/dragon-net-battle/index.html` for inspection. All output is ignored by Git. The GX palettes use split G/R and A/B
planes; the extractor reconstructs RGBA colors and the correct width and height from the texture headers.

The top-level Wii menu uses the extracted color art directly: eight landscape tiles, Pan, Giru, clouds, crest,
title, radar, bars, and both states of the three option labels. The cursor selects the original gold or blue
bar and its matching label. `home-motion.bin` holds keyframes decoded from the Wii FOD movie: the entrance of
the rows, Pan and Giru, Pan's idle movement, the radar pulse, and the lake sparkles. The home screen uses the
500-frame idle span at three-quarter speed. Pan and Giru use a slightly larger cosine bob with
five complete cycles in that span, easing at the top and bottom with no pause or jump at the loop seam. Giru has a different
phase. The title and crest follow the actual main-menu `fl_in` keyframes for `mc_title` and `mc_icon`:
the crest slides into place, then the title expands horizontally from its left edge. The root movie stops at
frame 59, before `fl_out` at frame 60; its icon and title children continue their original 60- and 410-frame
idle loops. The crest bobs gently and the title shifts and changes width while the menu remains open.
The radar appears after the rows finish entering, then switches directly to the selected row. Giru's artwork is
mirrored across its vertical axis with its visible bounds kept in place. The radar pulse animates independently.
These are whole-sprite movements;
the Wii source artwork does not provide articulated body frames for this home pose. A built-in motion fallback keeps them moving
if an older extraction has no `home-motion.bin`; the renderer logs which source it loaded. Selection fades through the
movie's five-frame highlight transition. The European archive has five DragonNe dialogue banks, decoded to
`home-subtitles-{en,es,de,fr,it}.bin` with 44 lines each. It also supplies five sets of headings,
option labels, and Create Player Name artwork, including its button captions, under
`languages/{en,es,de,fr,it}/`.
The port's selected menu language chooses the subtitle bank and matching Wii artwork;
other menu languages fall back to English. Older extractions without localized artwork use the original
English sheets. The landscape, moving clouds, and river sparkles stay visible behind Wii submenus.
Section 0 resource 6 has
separate Japanese and English lip events for each. The matching ADX voices are entries 30787–30830 (Japanese) and
32159–32202 (English) in the Wii voice archive. The extractor pairs them in `home-dialog.bin` and
`voices/{ja,en}/000.adx` through `043.adx`, checking each recording against its own lip track.
The game's Sound Options voice choice selects the matching recording and lip track independently of subtitle language.
Pan's base pose has open eyes; its original closed-eye overlay blinks briefly. After the
first cursor movement she uses the Wii pointing pose with its own eye and mouth sprites. The Wii lip track gates the
mouth animation for either pose: the body texture supplies the widest mouth, the first overlay is half open, and
the second overlay is closed. The recorded lip track chooses speaking or a pause; the two speaking shapes alternate
while it is open. Giru's dim eye is used while idle and his bright eye follows his own lip track.
The home scene speaks Pan's introduction and Giru's reply. Moving the cursor speaks the original description of the
selected option. The other lower Wii menu pages use their original spoken descriptions too. Pan's mouth and Giru's eye
variants come from the same Wii art pack and change on their recorded lip events. The existing game message window
displays the extracted line. A screenshot is useful for comparison but is not loaded by the port. The Nintendo WFC
Battle page uses section 1's clock background, six blue and gold bars, label sheets, title, and Giru pose. It opens
after a fade; Giru enters from the left at the name editor's size, and the title and crest play their header
animation after the fade. Pan does not appear or speak on this page. The battle entries sit below the header and
show neutral descriptions without character dialogue. The other lower Wii menu pages currently use the port's
drawn UI over the decoded landscape.
Focusing Ranking Battle or View Ranking shows the Wii Fighting Point panel on the left with `0000` as a placeholder.
The Custom Battle page uses the extracted Wii title and the battle page's clock, Giru, bars, cursor, and fade.
Its first option starts at the same vertical position as the first option on the preceding battle page.
The opponent-search screen uses section 1 resource 3's blue and red VS panel halves, panel highlights,
1P/2P badges, VS emblem, and battle-record labels and digits. Both panels show Battles, Wins, and Losses
with `0` placeholders. Names sit above the records in the game's native message-window font.
resource 4's Custom Battle title, and the same clock background. Giru enters fully on screen at the lower left after the fade.
The saved player name is centered in the blue panel; the opponent's name appears in the red panel when found.
On both battle pages, each lower option starts 10.5 screen units farther right, following the original Wii menu's
stair-step layout; the radar cursor follows the selected row's horizontal position and shares its text pulse.
The five option labels use the configured Menu font because this extraction has no matching Wii label sheet.
`tbo_sizes.py` measures the first row of the preceding battle page's idle and selected label textures and writes
their bounds into `tbo_sizes.h`. Custom Battle uses the outline's left edge for position and the interior fill's
height for font size; scaling the fill to the full outline height made the text too tall. Focused text
uses the same orange palette as the Versus Duel Menu, and unfocused text uses its purple palette. The Wii bars use
screen coordinates, so the font's page coordinates are converted before drawing to keep the two aligned on wide displays.
# Editable Dragon Net Battle text

The Dragon Net Battle screens read their entries and headers from
`gamedata/game-text/translations/port/en.json`. Edit the `text` value of an ID
beginning with `dragon-net/`, leaving its `original` and ID unchanged. This
includes the home, battle, custom battle, friends, settings, and ranking
headers and entries. The battle help lines are editable there too. The
Create Player Name keyboard title always uses its Wii artwork.
Fighting Point always uses its Wii artwork. Restart the game to load changes.

With **Menu font: Original**, unchanged labels use the extracted Wii artwork;
edited labels use the Menu font. Selecting any other Menu font renders all
entries and headers through the same row renderer and Evolution Z menu styles,
including unchanged English text. The Wii rows keep their screen
positions and the headers keep their entrance animation. Longer wording is
fitted to its available width. The screen reader uses the edited entries and
headers as well, while the keyboard title remains artwork.
Disabled font labels use the same dim tint as their Wii bars.
Font labels use Evolution Z's 19-pixel plate-caption letter height in both
states. Their focused layer replaces the idle layer during the four-frame
selection change, then continues a looping vertical stretch while focused.
The extracted texture labels on the home, battle, and settings pages use the
same focused-layer fade and vertical stretch. Their size now uses Evolution Z's
measured 19-pixel letter fill: the Wii home, battle, and settings sheets measure
17, 19, and 21 pixels, so they draw at 19/17, 19/19, and 19/21 of source size.
Both texture layers keep the original left edge and vertical center.
The Custom Battle text and fallback submenu entries use the same 19-pixel
letter height.
Evolution Z's heading has a 21-pixel letter height. Dragon Net Battle's Wii
title artwork and selected Menu font headings already match it; edited-title
fallback text now uses that measured height through the same title animation.
Text follows each bar's entrance motion. The first focused entry begins the
effect after the page's rows finish entering.
