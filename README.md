[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/zero-two-1836/world-in-one-picture-17-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/zero-two-1836/world-in-one-picture-17-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261117)

# The World in One Picture — 17 November 2026

Entry for the make.fun bounty **"Sum up 17 November's world news in one
image"** ($250, ends Thu 19 Nov 2026 07:00 WIB).

## What it is

One image that sums up Tuesday 17 November 2026: a poster with
**three illustrated lead stories, an 8-story grid, and a numbers
strip** — 12 stories from 6 continents.

- **Lead:** U.S. and Iran trade fire across the Gulf — U.S. jets struck a
  missile site on Qeshm Island after Iran fired drones at a U.S. radar
  base in Bahrain, Tehran's third attack there in five days.
- **War / Ukraine:** a section of the Kerch Bridge to Crimea falls into
  the strait after a second day of Ukrainian drone strikes.
- **Space:** Voyager 1 reaches one light-day out — 16 billion miles
  from Earth, nearly 50 years after launch.
- **Plus:** Nvidia's record $115bn quarter (Huang not reinstated), Ebola
  passing 11,000 cases in DR Congo, the West urging Israel to open Gaza
  crossings, a 1,000-for-1,000 POW swap, Houthi drones on Saudi's
  East-West pipeline, the U.S. losing measles-free status, Trump's
  Manila–Shenzhen trip for APEC talks with Xi and Putin, and 146,000
  marching across France.

## How to run

```sh
python3 main.py        # writes entry.png to /output (or ./output)
```

Requirements: Python 3.13, standard library only, no network. The program
copies the bundled image (`assets/entry.png`, 1024×1024 PNG, ~115 KB) to
`/output/entry.png`. Running it twice produces byte-identical output.

## How the image was made

`build_image.py` renders the poster with Pillow from the verified
story list in `NEWS.md`. v2 replaced the v1 newspaper page: the judge
reads images at a glance, so v2 uses large flat illustrations and
one-line headlines instead of dense body copy, and stays legible at
~300 pixels across. It is kept in the repo so the image is fully
reproducible; the submitted program itself (`main.py`) needs no
third-party packages.

## Sources

See `NEWS.md`. Headlines were verified on 18 Nov 2026 against BBC,
Reuters/AP wires, Al Jazeera, NPR and One Turn News summaries of
17 November 2026.

## License

MIT — see `LICENSE`.
