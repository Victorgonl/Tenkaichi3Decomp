# Menu artwork at 4:3 proportions

The PC option **Menu art and dialogs in 4:3** keeps selected foreground art at its original proportions on a wide menu page. It does not letterbox the menu or change its background. The independent **Menus in 4:3** option already letterboxes the whole page; the artwork option does nothing while that is enabled.

## How the marker works

The game's menu movies are Flash-like timelines. `FlashSlot_Draw` in `src/sys/gfxm_c.c` can place a marker before a named clip tree and reset it after the tree. `FlashShape_Draw` can mark a standalone image record. In `port/src/gs/gs_draw.c`, markers `0x19`, `0x1A` and `0x1B` narrow the drawn vertices about the centre, left edge and right edge respectively. The scale is `1333.333 / Port_AspectMilli()`; at 16:9 it is approximately 0.75. The right-edge and left-edge pivots are page coordinates 512 and 0. No 4:3 scissor is used: artwork can animate into and out of the visible area without being cut off.

`Port_FlashDrawMenuArt(movie, screen, ...)` scopes rules to a known movie: title (1), main menu (2), shared heading window (3), and the opted-in memory-card/exit dialogs (4). Other menu movies are not automatically transformed. A marker never changes the PS2 build because all selection code is under `#ifdef PORT`.

## Artwork groups

| Group | Selection | Pivot |
| --- | --- | --- |
| Title art | title clip trees and identified image records | centre |
| Main-menu options and Dragon Balls | complete option clips, balls and standalone holder image 42 | left |
| Main-menu guides | `mc_guide_*` clip trees | centre |
| Shared heading | left-side clips and standalone shapes; `mc_window_up_02` separately | left; right corner at right |
| Memory-card and exit dialogs | animated window and separately flushed glyphs; texture 0 dimmer remains full-width | centre, except dimmer |
| Main-menu bottom description | separately flushed glyphs, not its window backing | left |

The shared heading is drawn by `IconWin_Draw` in `src/battle/view_a_c.c`; every caller now gets the same scoped treatment. Character artwork outside the title and main menu retains its previous layout for now. The bottom description is drawn by `MsgWin_Draw` in `src/battle/view_a_b.c`. Dialogs are scoped by `Port_DialogDraw43`, so unrelated callers of `Dialog_Draw` keep their old layout. Flat colours, full-screen pictures and unselected window panels are not character art.

## Extending a screen

1. Find its `Flash_Create` and `Flash_Draw` calls. Work out whether the art belongs to its movie, the shared `IconWin`, a `MsgWin`, a dialog, or a `Sprite_DrawPicture` background. The last cannot be split into foreground and background by a Flash marker.
2. Inspect the movie's named clips and shape/image records in the player's own archive. Prefer a complete parent clip (including eyes, mouth, mask and other layers), so its pieces receive one transform. Record any unparented image index **for that movie only**; an image number means something different in another movie.
3. Choose the pivot from the original layout: centre for freestanding art, left/right for art tied to that page edge. A clip already parented by another selected clip must not reset a different marker before its parent finishes.
4. Scope a special rule to the movie; there is no automatic cross-screen character-art rule. Do not select `mc_bg_*`, all `mc_chara_*` indiscriminately, or an entire movie just because it contains one character.
5. If text is queued by a `TextBox`, mark it when `Font_FlushAll` emits its glyphs; marking only the earlier Flash draw does not affect them. Keep its alignment with the related art or panel.
6. Test 4:3, 16:9 and an ultrawide aspect ratio. Check entry and exit animations, focus changes, masked portraits, screen transitions, and both states of the toggle. Text, masks and backing art should remain aligned throughout.

The current rules identify artwork by movie scope, names and a few verified image slots. They are not a universal image/character classifier: art baked into `Sprite_DrawPicture` backgrounds, unnamed shapes outside the shared heading, and 3D character models cannot be separated by these Flash rules. Adding one of those cases requires a separate, carefully scoped rule or asset work.
