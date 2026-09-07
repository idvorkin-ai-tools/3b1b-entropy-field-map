# Entropy, mapped

A field map of 3Blue1Brown's **Compression is Intelligence** series — Grant
Sanderson's videos on entropy and cross-entropy — plus the videos on either
side of it that carry the same argument.

Live: <https://idvorkin-ai-tools.github.io/3b1b-entropy-field-map/>

## What is here

Twenty explainer pages in four arcs, each written from the video but in its own
words, with every claim timestamped into the source:

| Arc | Pages | Source |
| --- | --- | --- |
| Reinventing entropy | P1–P6 | [Reinventing Entropy](https://youtu.be/l6DKRf-fAAM) — Part 1, Jun 2026 |
| Cross-entropy, and where the loss function comes from | P7–P15 | [But what is cross-entropy?](https://youtu.be/GlYgs6v2YfU) — Part 2, Jul 2026 |
| Entropy in action: Wordle | P16–P18 | [Solving Wordle using information theory](https://youtu.be/v68zYyaEmEA) + [the addendum](https://youtu.be/fRed0Xmc2Wg), 2022 |
| The other direction: redundancy on purpose | P19–P20 | [Hamming codes](https://youtu.be/X8jsijhllIA) [part 2](https://youtu.be/b3NxrZOu_CE), 2020 |

Plus a [concept index](concepts.html) and six timestamped transcripts under
`transcripts/`.

## The spine

surprise → optimal codes → entropy → cross-entropy → KL divergence → the
training objective of every language model.

## Building

`tools/build_transcripts.py` regenerates the transcript pages from the captions
pulled with `yt-dlp`. The pages themselves are hand-written HTML over a single
`paper.css`; there is no build step and no JavaScript beyond a progress
checkbox on the index.

## Credit

The lessons, animations and framings are Grant Sanderson's
([3blue1brown.com](https://www.3blue1brown.com)). This map explains them in its
own words and links back at every timestamp; it is not a substitute for
watching the videos.
