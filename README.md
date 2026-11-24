# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b84-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b84-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up **Monday 23 November 2026** in a single image: 31 stories across 6 regions.

## The day

- **AI rout hits Asia** — Kospi −3.3% to 4,708.54, sheds 161 pts (intraday −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — at the Bridgetown summit, 150 delegates back a risk framework.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China 73.6, gap 5.3, narrowest since 2018; India third at 40.5.

Below the heroes: 10 more stories, a world map with numbered pins, 18 more in "Also on Monday", and a red DATE CHECK box separating what is *not* 23 November (Dems 258, Sparta II fire, El Chapo, EU–Indonesia, Nigeria boat, ICJ Myanmar) from the day's news.

## How to render

```sh
python3 draw.py            # regenerates entry.png (1024x1024)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` is stdlib-only: it validates the PNG header and chunk CRCs itself (no PIL), and never writes next to itself.

## Sources

Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026). Scenes are drawn illustrations, not photographs. All times UTC.
