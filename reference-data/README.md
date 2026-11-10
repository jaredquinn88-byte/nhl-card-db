# Reference data

Checklist data scraped from card sites, kept as reference for filling in
team and position details. **None of it is verified.** The card list itself
comes from the image filenames in the set folders (see the main README).

| File | Rows | Covers | Quality |
|---|---|---|---|
| `Universal_NHL_Database.json` | 7,153 | 33 sets: Pro Set 1990–93, MVP 2019–25, Upper Deck Series 1/2 2017–21 | Clean; `position` often `N/A` |
| `MVP_Master_Addon.json` | 2,694 | MVP 2019-20 to 2024-25 | Clean |
| `Series1_Series2_Master.json` | 2,439 | Upper Deck Series 1/2, UD Game Jersey inserts | Clean, has positions |
| `ProSet_Archive_1990_1993.json` | 1,891 | Pro Set 1990-91 to 1992-93, Pro Set Platinum | Clean |
| `TimHortons_Master_Addon.json` | 117 | Tim Hortons 2019-20, 2020-21, 2024-25, 2025-26 | Clean |
| `NHL_Master_List.json` | 2,902 | Unknown, recent Upper Deck | Set name missing on every row |
| `Checklist_V1.json` | 11,217 | Recent Upper Deck base, parallels, inserts | Set name in `Set Name`, not `Set_Name`; mixed columns |
| `hockey_cards_2025-12-24T04-16-47.json` | 2,696 | 2024-25 Upper Deck **CHL** (junior hockey, not NHL) | Messy columns |

Removed during the clean-up (all unusable): the `*_checklist/` CSV and JSON
files in each set folder (scraped website menus, no card rows), plus
`Master_Checklist.csv`, `Comprehensive_NHL_DB_FINAL` and its `backup_progress_*`
copies (non-hockey "set review" pages).
