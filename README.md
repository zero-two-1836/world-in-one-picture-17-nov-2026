[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/zero-two-1836/world-in-one-picture-17-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/zero-two-1836/world-in-one-picture-17-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261117)

# The World in One Picture — 17 November 2026

Entry for the make.fun bounty **"Sum up 17 November's world news in one
image"** ($250, ends Thu 19 Nov 2026 07:00 WIB).

## What it is

One image that sums up Tuesday 17 November 2026: a newspaper front page
with **12 stories from 6 continents** plus a numbers strip.

- **Lead:** U.S. and Iran trade fire across the Gulf — U.S. jets struck a
  missile site on Qeshm Island after Iran fired drones at a U.S. radar
  base in Bahrain, Tehran's third attack there in five days.
- **War / Ukraine:** a section of the Kerch Bridge to Crimea falls into
  the strait after a second day of Ukrainian drone strikes.
- **Diplomacy / Asia:** Trump flies to Manila, then on to Shenzhen for
  APEC talks with China's Xi and Russia's Putin.
- **Plus:** Nvidia's record $115bn quarter (Huang not reinstated), Ebola
  passing 11,000 cases in DR Congo, the West urging Israel to open Gaza
  crossings, a 1,000-for-1,000 POW swap, Houthi drones on Saudi's
  East-West pipeline, the U.S. losing measles-free status, Voyager 1
  reaching one light-day out, and 146,000 marching across France.

## How to run

```sh
python3 main.py        # writes entry.png to /output (or ./output)
```

Requirements: Python 3.13, standard library only, no network. The program
copies the bundled image (`assets/entry.png`, 1024×1024 PNG, ~139 KB) to
`/output/entry.png`. Running it twice produces byte-identical output.

## How the image was made

`build_image.py` renders the front page with Pillow from the verified
story list in `NEWS.md`. It is kept in the repo so the image is fully
reproducible; the submitted program itself (`main.py`) needs no
third-party packages.

## Sources

See `NEWS.md`. Headlines were verified on 18 Nov 2026 against BBC,
Reuters/AP wires, Al Jazeera, NPR and One Turn News summaries of
17 November 2026.

## License

MIT — see `LICENSE`.
