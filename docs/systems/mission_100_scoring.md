# Mission 100 scoring tables

Extracted from the USA PS2 disc (`SLUS-21678.iso`), `DATA/PZS3US1.AFS`, entry 451 (game file ID 452), screen section 3, BPE-decoded resource section 13. Each row is six little-endian signed 32-bit integers (24 bytes). Bonus names come from resource section 12, text line `32 + bonus ID` (zero-based). The 101 scoring rows match the European English archive `gamedata/pzs3eu1/00454.bin` exactly.

USA archive entry SHA-256: `eca2acc1b949b778123b3bba2e06822e3a405f657868109c1151ce5fad01e3b6`.

## Formula and units

The game adds the health, highest combo hit count, highest combo damage, and earned bonus contributions. Each table value below is an **internal point**. The result screen displays **100 × internal points**. Mission 100 awards **one Z Point per internal point** (subject to the saved-money cap).

For normal inputs, the three base contributions are:

- Health: `10 × floor(remaining team health percentage)`. A positive value below 1% is treated as 1%.
- Combo hits: `min(40 × highest combo hits, 1000)`. The lookup input is capped at 100, but its award already saturates at 25 hits.
- Combo damage: `min(50 × floor(highest combo damage / 1000), 1000)` for the normal covered brackets. The award saturates at 20,000 damage.
- Bonuses: add each earned bonus ID once, using the bonus table. Repeating an action does not multiply that bonus.

Battle duration is recorded but does not contribute to Mission 100 scoring (`UbScore_Fill(1)` uses three base lines). Aborted battles leave an empty score sheet. Wins and losses both populate the sheet; the mission best record is saved only for a win.

**Damage edge case:** the source lookup has a final threshold of **99,989**, while the input is capped at **99,990**. An input of 99,990 matches no threshold and leaves that contribution at zero. The fallback inside the loop is unreachable. This is the behavior of the checked-in decompilation; do not assume the normal formula applies at that edge.

## Maximum base score example

| Component | Input | Internal points / Z Points | Displayed points |
| --- | --- | ---: | ---: |
| Remaining team health | 100% | 1,000 | 100,000 |
| Highest combo | 25 hits or more | 1,000 | 100,000 |
| Highest combo damage | 20,000 (sufficient) | 1,000 | 100,000 |
| **Base total** | Before bonuses | **3,000** | **300,000** |

For example, adding the 100-point Perfect Win bonus produces **310,000 displayed points / 3,100 Z Points**, before any other earned bonuses. This is a worked calculation, not a claim that only that bonus will trigger in such a battle.

A verified achievable overall perfect score requires checking which bonus conditions can coexist. The sum of every listed bonus is only a table total: several slots are not set by the current `BattleResult_CollectEvents` implementation, and conditions may conflict.

## Base lookup table

Health and hits use the row index directly. Damage uses the first row whose threshold is at least the damage value. Row 100 has no corresponding damage bracket (the loop checks rows 0–99 only). The fourth base column in the binary belongs to other modes and is omitted.

| Index | Health % | Health internal | Combo hits | Hits internal | Combo damage bracket | Damage internal |
| ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 0 | 0 | 0 | 0 | 0 | 0–999 | 0 |
| 1 | 1 | 10 | 1 | 40 | 1,000–1,999 | 50 |
| 2 | 2 | 20 | 2 | 80 | 2,000–2,999 | 100 |
| 3 | 3 | 30 | 3 | 120 | 3,000–3,999 | 150 |
| 4 | 4 | 40 | 4 | 160 | 4,000–4,999 | 200 |
| 5 | 5 | 50 | 5 | 200 | 5,000–5,999 | 250 |
| 6 | 6 | 60 | 6 | 240 | 6,000–6,999 | 300 |
| 7 | 7 | 70 | 7 | 280 | 7,000–7,999 | 350 |
| 8 | 8 | 80 | 8 | 320 | 8,000–8,999 | 400 |
| 9 | 9 | 90 | 9 | 360 | 9,000–9,999 | 450 |
| 10 | 10 | 100 | 10 | 400 | 10,000–10,999 | 500 |
| 11 | 11 | 110 | 11 | 440 | 11,000–11,999 | 550 |
| 12 | 12 | 120 | 12 | 480 | 12,000–12,999 | 600 |
| 13 | 13 | 130 | 13 | 520 | 13,000–13,999 | 650 |
| 14 | 14 | 140 | 14 | 560 | 14,000–14,999 | 700 |
| 15 | 15 | 150 | 15 | 600 | 15,000–15,999 | 750 |
| 16 | 16 | 160 | 16 | 640 | 16,000–16,999 | 800 |
| 17 | 17 | 170 | 17 | 680 | 17,000–17,999 | 850 |
| 18 | 18 | 180 | 18 | 720 | 18,000–18,999 | 900 |
| 19 | 19 | 190 | 19 | 760 | 19,000–19,999 | 950 |
| 20 | 20 | 200 | 20 | 800 | 20,000–20,999 | 1,000 |
| 21 | 21 | 210 | 21 | 840 | 21,000–21,999 | 1,000 |
| 22 | 22 | 220 | 22 | 880 | 22,000–22,999 | 1,000 |
| 23 | 23 | 230 | 23 | 920 | 23,000–23,999 | 1,000 |
| 24 | 24 | 240 | 24 | 960 | 24,000–24,999 | 1,000 |
| 25 | 25 | 250 | 25 | 1,000 | 25,000–25,999 | 1,000 |
| 26 | 26 | 260 | 26 | 1,000 | 26,000–26,999 | 1,000 |
| 27 | 27 | 270 | 27 | 1,000 | 27,000–27,999 | 1,000 |
| 28 | 28 | 280 | 28 | 1,000 | 28,000–28,999 | 1,000 |
| 29 | 29 | 290 | 29 | 1,000 | 29,000–29,999 | 1,000 |
| 30 | 30 | 300 | 30 | 1,000 | 30,000–30,999 | 1,000 |
| 31 | 31 | 310 | 31 | 1,000 | 31,000–31,999 | 1,000 |
| 32 | 32 | 320 | 32 | 1,000 | 32,000–32,999 | 1,000 |
| 33 | 33 | 330 | 33 | 1,000 | 33,000–33,999 | 1,000 |
| 34 | 34 | 340 | 34 | 1,000 | 34,000–34,999 | 1,000 |
| 35 | 35 | 350 | 35 | 1,000 | 35,000–35,999 | 1,000 |
| 36 | 36 | 360 | 36 | 1,000 | 36,000–36,999 | 1,000 |
| 37 | 37 | 370 | 37 | 1,000 | 37,000–37,999 | 1,000 |
| 38 | 38 | 380 | 38 | 1,000 | 38,000–38,999 | 1,000 |
| 39 | 39 | 390 | 39 | 1,000 | 39,000–39,999 | 1,000 |
| 40 | 40 | 400 | 40 | 1,000 | 40,000–40,999 | 1,000 |
| 41 | 41 | 410 | 41 | 1,000 | 41,000–41,999 | 1,000 |
| 42 | 42 | 420 | 42 | 1,000 | 42,000–42,999 | 1,000 |
| 43 | 43 | 430 | 43 | 1,000 | 43,000–43,999 | 1,000 |
| 44 | 44 | 440 | 44 | 1,000 | 44,000–44,999 | 1,000 |
| 45 | 45 | 450 | 45 | 1,000 | 45,000–45,999 | 1,000 |
| 46 | 46 | 460 | 46 | 1,000 | 46,000–46,999 | 1,000 |
| 47 | 47 | 470 | 47 | 1,000 | 47,000–47,999 | 1,000 |
| 48 | 48 | 480 | 48 | 1,000 | 48,000–48,999 | 1,000 |
| 49 | 49 | 490 | 49 | 1,000 | 49,000–49,999 | 1,000 |
| 50 | 50 | 500 | 50 | 1,000 | 50,000–50,999 | 1,000 |
| 51 | 51 | 510 | 51 | 1,000 | 51,000–51,999 | 1,000 |
| 52 | 52 | 520 | 52 | 1,000 | 52,000–52,999 | 1,000 |
| 53 | 53 | 530 | 53 | 1,000 | 53,000–53,999 | 1,000 |
| 54 | 54 | 540 | 54 | 1,000 | 54,000–54,999 | 1,000 |
| 55 | 55 | 550 | 55 | 1,000 | 55,000–55,999 | 1,000 |
| 56 | 56 | 560 | 56 | 1,000 | 56,000–56,999 | 1,000 |
| 57 | 57 | 570 | 57 | 1,000 | 57,000–57,999 | 1,000 |
| 58 | 58 | 580 | 58 | 1,000 | 58,000–58,999 | 1,000 |
| 59 | 59 | 590 | 59 | 1,000 | 59,000–59,999 | 1,000 |
| 60 | 60 | 600 | 60 | 1,000 | 60,000–60,999 | 1,000 |
| 61 | 61 | 610 | 61 | 1,000 | 61,000–61,999 | 1,000 |
| 62 | 62 | 620 | 62 | 1,000 | 62,000–62,999 | 1,000 |
| 63 | 63 | 630 | 63 | 1,000 | 63,000–63,999 | 1,000 |
| 64 | 64 | 640 | 64 | 1,000 | 64,000–64,999 | 1,000 |
| 65 | 65 | 650 | 65 | 1,000 | 65,000–65,999 | 1,000 |
| 66 | 66 | 660 | 66 | 1,000 | 66,000–66,999 | 1,000 |
| 67 | 67 | 670 | 67 | 1,000 | 67,000–67,999 | 1,000 |
| 68 | 68 | 680 | 68 | 1,000 | 68,000–68,999 | 1,000 |
| 69 | 69 | 690 | 69 | 1,000 | 69,000–69,999 | 1,000 |
| 70 | 70 | 700 | 70 | 1,000 | 70,000–70,999 | 1,000 |
| 71 | 71 | 710 | 71 | 1,000 | 71,000–71,999 | 1,000 |
| 72 | 72 | 720 | 72 | 1,000 | 72,000–72,999 | 1,000 |
| 73 | 73 | 730 | 73 | 1,000 | 73,000–73,999 | 1,000 |
| 74 | 74 | 740 | 74 | 1,000 | 74,000–74,999 | 1,000 |
| 75 | 75 | 750 | 75 | 1,000 | 75,000–75,999 | 1,000 |
| 76 | 76 | 760 | 76 | 1,000 | 76,000–76,999 | 1,000 |
| 77 | 77 | 770 | 77 | 1,000 | 77,000–77,999 | 1,000 |
| 78 | 78 | 780 | 78 | 1,000 | 78,000–78,999 | 1,000 |
| 79 | 79 | 790 | 79 | 1,000 | 79,000–79,999 | 1,000 |
| 80 | 80 | 800 | 80 | 1,000 | 80,000–80,999 | 1,000 |
| 81 | 81 | 810 | 81 | 1,000 | 81,000–81,999 | 1,000 |
| 82 | 82 | 820 | 82 | 1,000 | 82,000–82,999 | 1,000 |
| 83 | 83 | 830 | 83 | 1,000 | 83,000–83,999 | 1,000 |
| 84 | 84 | 840 | 84 | 1,000 | 84,000–84,999 | 1,000 |
| 85 | 85 | 850 | 85 | 1,000 | 85,000–85,999 | 1,000 |
| 86 | 86 | 860 | 86 | 1,000 | 86,000–86,999 | 1,000 |
| 87 | 87 | 870 | 87 | 1,000 | 87,000–87,999 | 1,000 |
| 88 | 88 | 880 | 88 | 1,000 | 88,000–88,999 | 1,000 |
| 89 | 89 | 890 | 89 | 1,000 | 89,000–89,999 | 1,000 |
| 90 | 90 | 900 | 90 | 1,000 | 90,000–90,999 | 1,000 |
| 91 | 91 | 910 | 91 | 1,000 | 91,000–91,999 | 1,000 |
| 92 | 92 | 920 | 92 | 1,000 | 92,000–92,999 | 1,000 |
| 93 | 93 | 930 | 93 | 1,000 | 93,000–93,999 | 1,000 |
| 94 | 94 | 940 | 94 | 1,000 | 94,000–94,999 | 1,000 |
| 95 | 95 | 950 | 95 | 1,000 | 95,000–95,999 | 1,000 |
| 96 | 96 | 960 | 96 | 1,000 | 96,000–96,999 | 1,000 |
| 97 | 97 | 970 | 97 | 1,000 | 97,000–97,999 | 1,000 |
| 98 | 98 | 980 | 98 | 1,000 | 98,000–98,999 | 1,000 |
| 99 | 99 | 990 | 99 | 1,000 | 99,000–99,989 | 1,000 |
| 100 | 100 | 1,000 | 100 | 1,000 | Unused | 1,000 |

## Bonus lookup table

`Collected` means the checked-in `BattleResult_CollectEvents` contains a condition that sets the bonus bit. A listed price alone does not mean a bonus can currently be earned. Names are the disc labels; they do not fully specify each trigger.

| ID / bit | Disc bonus name | Internal points / Z Points | Displayed points | Collected |
| ---: | --- | ---: | ---: | --- |
| 0 | Ultimate Blast Finish | 70 | 7,000 | Yes |
| 1 | Blast 2 Finish | 50 | 5,000 | Yes |
| 2 | Blast 1 Finish | 30 | 3,000 | Yes |
| 3 | Perfect Win | 100 | 10,000 | Yes |
| 4 | Turnaround | 100 | 10,000 | Yes |
| 5 | Underwater Win | 20 | 2,000 | No |
| 6 | Player Hit More Than Opponent. | 10 | 1,000 | No |
| 7 | Aerial Rush | 15 | 1,500 | No |
| 8 | Blow Opponent In All Directions | 25 | 2,500 | Yes |
| 9 | Pursue downed opponent | 10 | 1,000 | Yes |
| 10 | Guard Crash | 20 | 2,000 | Yes |
| 11 | Lift Opponent Into Air | 10 | 1,000 | No |
| 12 | Knock Opponent Down | 10 | 1,000 | No |
| 13 | Hyper Smash Hits | 30 | 3,000 | Yes |
| 14 | Dragon Heavy Hits | 20 | 2,000 | No |
| 15 | Dragon Smash Hits | 15 | 1,500 | Yes |
| 16 | Burning Attack Hits | 15 | 1,500 | Yes |
| 17 | Burst Meteo Hits | 15 | 1,500 | Yes |
| 18 | Dash Attack Hits | 10 | 1,000 | Yes |
| 19 | Jump Attack Hits | 20 | 2,000 | Yes |
| 20 | Aerial Combos | 15 | 1,500 | No |
| 21 | Blast Combo Hits | 25 | 2,500 | No |
| 22 | Ki Attacks Only | 100 | 10,000 | No |
| 23 | Rushing Ki Attack Hits | 10 | 1,000 | No |
| 24 | Smash Ki Attack Hits | 10 | 1,000 | Yes |
| 25 | Blast 1 Used | 10 | 1,000 | Yes |
| 26 | Blast 2 Used | 10 | 1,000 | Yes |
| 27 | Ultimate Blast Used | 20 | 2,000 | Yes |
| 28 | MAX POWER Mode | 15 | 1,500 | Yes |
| 29 | Blast Attacks Only | 100 | 10,000 | No |
| 30 | Throw Attacks Only | 100 | 10,000 | No |
| 31 | Successful Throws | 10 | 1,000 | Yes |
| 32 | Maximum Speed Evasions | 30 | 3,000 | Yes |
| 33 | Blaster Wave | 10 | 1,000 | Yes |
| 34 | Successful Z Counters | 50 | 5,000 | Yes |
| 35 | Auto-Counter | 20 | 2,000 | Yes |
| 36 | Sonic Sway Evasions | 20 | 2,000 | Yes |
| 37 | Not Knocked Down | 50 | 5,000 | Yes |
| 38 | Successful Guards | 20 | 2,000 | No |
| 39 | Ki Reflected | 10 | 1,000 | Yes |
| 40 | No Switch Victory | 30 | 3,000 | Yes |
| 41 | Taunts | 10 | 1,000 | Yes |
| 42 | First Hit | 30 | 3,000 | Yes |
| 43 | Counter Opponent. | 10 | 1,000 | No |
| 44 | Maximum Blast Stock | 30 | 3,000 | Yes |
| 45 | True Power | 100 | 10,000 | Yes |
| 46 | Crash Battle Victory | 30 | 3,000 | Yes |
| 47 | Fighting Battle Victory | 30 | 3,000 | Yes |

## Rank thresholds

Mission 100 selects the first inclusive threshold in `{1599, 2199, 2799, 9999}` using the internal total. These are numeric rank IDs; the displayed letter is selected from a texture.

| Internal total | Displayed total | Rank ID |
| --- | --- | ---: |
| 0–1,599 | 0–159,900 | 1 |
| 1,600–2,199 | 160,000–219,900 | 2 |
| 2,200–2,799 | 220,000–279,900 | 3 |
| 2,800–9,999 | 280,000–999,900 | 4 |

## Code references

- [Result initialization and table loading](../../src/menu/menu_p_b.c): `MisResult_Init`, resource sections 12 and 13; calls `UbScore_Fill(1)`, `UbScore_CalcPoints`, and `UbScore_CalcRank(1)`.
- [Scoring and lookup thresholds](../../src/menu/menu_p_d.c): `UbScore_Fill`, `UbScore_CalcPoints`, `UbScore_CalcRank`.
- [Display and payout](../../src/menu/menu_p_b.c): `MisResult_Draw` displays points multiplied by 100; the money state restores `score.convert = score.saved` before transferring it to saved money. The generic 0.1 conversion animation does not determine the final Mission 100 payout.
- [Bonus bit construction](../../src/battle/battle_load.c): `BattleResult_CollectEvents`.
- [Battle statistics](../../src/battle/btl_char_mgr.c): maximum combo statistics and remaining team health are copied into the battle result.
- [Table layout](../../include/menu/menu_p.h): `UbScorePrice`.
