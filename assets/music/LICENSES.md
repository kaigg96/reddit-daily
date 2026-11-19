# Music in rotation: sources and licences

`video._pick_music` picks at random from every `*.mp3` here, plus the sealed
funk bed (`../funk_bg_lower.mp3.enc`, YouTube Audio Library, unsealed only in
CI), and never the track of the last upload in `upload_log.csv` (E1 T2).

## FreePD.com tracks (CC0 1.0, public domain)

FreePD.com closed in 2025 ("[freepd.com] is now permanently closed", read at
https://freepd.com/ on 2026-11-15). The tracks and the licence statement were
taken from the Internet Archive's copies of the live site.

Licence statement, from https://freepd.com/ as archived at
http://web.archive.org/web/20241231185827/https://freepd.com/ (read 2026-11-15):

> This music is all licensed CC0 1.0 Universal Public Domain Dedication.

and, on the same page:

> 100% Free Music - Free for Commercial Use, Free Of Royalties, Free Of
> Attribution, Creative Commons 0

> Can I buy exclusive rights to any of these tracks? No. The CC0 licensing is
> a one-way trip

CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/. No login,
payment or attribution is needed. All four were listed on FreePD's "Upbeat"
page (http://web.archive.org/web/20250106221458/https://freepd.com/upbeat.php),
which names no composer.

| File | FreePD title | Source (archived download) | Source length | Source sha256 |
|---|---|---|---|---|
| `freepd_advertime.mp3` | Advertime | http://web.archive.org/web/20250107032704id_/https://freepd.com/music/Advertime.mp3 | 2:14 | `6f0d4433cf788304d60add551cc460dd877865e6d84a2ab3fa7d15ba3f55d6ce` |
| `freepd_city_sunshine.mp3` | City Sunshine | http://web.archive.org/web/20250107032552id_/https://freepd.com/music/City%20Sunshine.mp3 | 3:05 | `e05c1bd683174cff77d492b7ac77262ff4617f99f69d82564b66831cf48352d6` |
| `freepd_fresh_focus.mp3` | Fresh Focus | http://web.archive.org/web/20250106221710id_/https://freepd.com/music/Fresh%20Focus.mp3 | 2:04 | `87d70572729712abfb6d444b7de4cc7b0104eafca1f0fcfec1798fd824325c3c` |
| `freepd_funshine.mp3` | Funshine | http://web.archive.org/web/20250107032521id_/https://freepd.com/music/Funshine.mp3 | 2:45 | `b98b226927367a977377fe4f75d1cf59e4366ca2f444c2c7d23d13e7f506f532` |

Processing, the same for each (ffmpeg from `imageio_ffmpeg`): first 60 s, a
3 s fade-out, `loudnorm=I=-20:TP=-2:LRA=11`, metadata and cover art dropped,
128 kbps stereo. At `config.MUSIC_VOLUME_LIBRARY` (0.18, about -15 dB) that
puts them near -36 dBFS mean, beside the funk bed's ~-35.5 at
`MUSIC_VOLUME_FALLBACK`, about 10 dB under the narration (~-25 dBFS).
