#!/usr/bin/env python3
"""Generate the transcript pages of the 3b1b entropy field map.

The six source videos all ship HUMAN-written captions (not auto-captions), so
there is nothing to disambiguate: the job is purely mechanical — group the
[mm:ss] blocks into paragraphs, drop the caption-service boilerplate, insert the
YouTube chapter headings as anchors the part pages can link to, and escape HTML.

    tools/build_transcripts.py
"""

import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SRC = "/home/developer/tmp/agent/skill/3b1b-entropy-field-map"

VIDEOS = [
    dict(
        vid="l6DKRf-fAAM",
        slug="part1",
        title="Reinventing Entropy",
        series="Compression is Intelligence, Part 1",
        date="7 June 2026",
        mins=32,
        colour="off",
        box="wb",
        back="../parts/p01.html",
        backlbl="← P1",
    ),
    dict(
        vid="GlYgs6v2YfU",
        slug="part2",
        title="But what is cross-entropy?",
        series="Compression is Intelligence, Part 2",
        date="16 July 2026",
        mins=34,
        colour="def",
        box="bb",
        back="../parts/p07.html",
        backlbl="← P7",
    ),
    dict(
        vid="v68zYyaEmEA",
        slug="wordle",
        title="Solving Wordle using information theory",
        series="Standalone, 2022",
        date="6 February 2022",
        mins=31,
        colour="off",
        box="wb",
        back="../parts/p16.html",
        backlbl="← P16",
    ),
    dict(
        vid="fRed0Xmc2Wg",
        slug="wordle-addendum",
        title="Oh, wait, actually the best Wordle opener is not “crane”…",
        series="Wordle addendum, 2022",
        date="13 February 2022",
        mins=11,
        colour="off",
        box="wb",
        back="../parts/p18.html",
        backlbl="← P18",
    ),
    dict(
        vid="X8jsijhllIA",
        slug="hamming1",
        title="But what are Hamming codes? The origin of error correction",
        series="Hamming codes, part 1",
        date="4 September 2020",
        mins=20,
        colour="def",
        box="bb",
        back="../parts/p19.html",
        backlbl="← P19",
    ),
    dict(
        vid="b3NxrZOu_CE",
        slug="hamming2",
        title="Hamming codes part 2: The one-line implementation",
        series="Hamming codes, part 2",
        date="4 September 2020",
        mins=17,
        colour="def",
        box="bb",
        back="../parts/p20.html",
        backlbl="← P20",
    ),
]

# YouTube leaves an "<Untitled Chapter 1>" placeholder on the two Hamming videos.
CHAPTER_FIX = {
    ("X8jsijhllIA", 0): "Scratched discs and the idea of error correction",
    ("b3NxrZOu_CE", 0): "Recap of part 1",
    ("b3NxrZOu_CE", 1): "Recap of part 1",
}

BOILERPLATE = re.compile(r"\[Submit subtitle corrections at [^\]]*\]\s*")
BLOCK = re.compile(r"^\[(\d+):(\d+)\]\s*(.*)$")

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Transcript · {title_esc} — Entropy, mapped</title>
<meta name="description" content="Timestamped transcript of 3Blue1Brown&#39;s {title_esc}, with every paragraph linking into the video at that moment." />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../paper.css" />
</head>
<body>
<header class="bar"><div class="bar-in">
  <div class="brand"><span class="dot"></span>ENTROPY&nbsp;//&nbsp;FIELD&nbsp;MAP</div>
  <a class="back" href="{back}">{backlbl}</a>
</div></header>
<main>
  <div class="eyebrow"><span class="box {box} mono">TRANSCRIPT</span><span class="mono">3Blue1Brown · {date} · {mins} min</span></div>
  <h1>{title_esc}</h1>
  <div class="authors">{series} · Grant Sanderson&#39;s own published captions, grouped into paragraphs · every timestamp opens the video at that moment</div>
  <div class="paperlink" style="border-left-color:var(--{colour})"><span class="lbl">Video</span><a href="https://youtu.be/{vid}" target="_blank" rel="noopener">{title_esc} — 3Blue1Brown ↗</a></div>
  <p class="mono" style="font-size:12.5px;color:var(--ink-dim)">Back to the <a class="lnk" href="../index.html">field map</a>.</p>
  <div class="transcript">
"""

TAIL = """  </div>
</main>
<footer>Captions published by 3Blue1Brown with the video, regrouped into paragraphs for reading and searching. The lesson is Grant Sanderson&#39;s; this page links to it, it does not replace it.</footer>
</body>
</html>
"""


def load_blocks(vid):
    out = []
    for line in open(f"{SRC}/transcripts/{vid}.md", encoding="utf-8").read().split("\n\n"):
        m = BLOCK.match(line.strip())
        if not m:
            continue
        sec = int(m.group(1)) * 60 + int(m.group(2))
        text = BOILERPLATE.sub("", m.group(3)).strip()
        if text:
            out.append((sec, text))
    return out


def load_chapters(vid):
    raw = json.load(open(f"{SRC}/raw/{vid}.chapters.json", encoding="utf-8")) or []
    chs, seen = [], set()
    for c in raw:
        start = int(c["start_time"])
        title = CHAPTER_FIX.get((vid, start), c["title"])
        if title.startswith("<Untitled"):
            continue
        if title in seen:
            continue
        seen.add(title)
        chs.append((start, title))
    return chs


def build(v):
    vid = v["vid"]
    blocks = load_blocks(vid)
    chapters = load_chapters(vid)
    body, para, ch_i, words = [], [], 0, 0
    h2s = 0

    def flush():
        nonlocal para, words
        if not para:
            return
        sec = para[0][0]
        text = " ".join(html.escape(t) for _, t in para)
        words += sum(len(t.split()) for _, t in para)
        body.append(
            f'    <p><a class="ts" href="https://youtu.be/{vid}?t={sec}" '
            f'target="_blank" rel="noopener">{sec // 60:02d}:{sec % 60:02d}</a> {text}</p>'
        )
        para = []

    for sec, text in blocks:
        while ch_i < len(chapters) and sec >= chapters[ch_i][0]:
            flush()
            cs, ct = chapters[ch_i]
            body.append(f'    <h2 id="s-{cs}">{html.escape(ct)}</h2>')
            h2s += 1
            ch_i += 1
        para.append((sec, text))
        if len(para) >= 3:
            flush()
    flush()
    if body and not body[0].startswith("    <h2"):
        body.insert(0, '    <h2 id="s-0">Opening</h2>')
        h2s += 1

    page = (
        HEAD.format(title_esc=html.escape(v["title"]), **{k: v[k] for k in ("back", "backlbl", "box", "date", "mins", "series", "colour", "vid")})
        + "\n".join(body)
        + "\n"
        + TAIL
    )
    path = f"{SITE}/transcripts/{v['slug']}.html"
    open(path, "w", encoding="utf-8").write(page)
    print(f"{v['slug']:16s} {len(blocks):4d} blocks  {h2s:2d} h2  {words:6d} words -> {path}")


if __name__ == "__main__":
    for v in VIDEOS:
        build(v)
