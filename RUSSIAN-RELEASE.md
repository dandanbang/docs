# Russian guide release

This branch adds all 20 published English guide pages plus a Russian version of the shared free/subscription FAQ: 21 Russian navigation destinations. The unlisted starter snippet is excluded. English and Traditional Chinese navigation remain in place.

The source revision is `e067fca`. Russian prose was drafted locally with an offline EN→RU model; page titles, navigation, product controls, privacy/security disclosures, import/deletion instructions and other selected passages were manually reviewed. No journal data or credentials were involved. Shared image and video references remain unchanged; screenshots within those assets currently show the source UI language.

Two outdated source facts were corrected in English and Russian under the CEO's existing approved behavior, with no product change:

- Inner Wisdom opens after 4 entries: `spiritualhuman/server/utils/unlock_thresholds.py`, `INNER_WISDOM_UNLOCK_ENTRIES = 4` (CEO curve, 2026-08-20).
- Paid voice quota is 300 recordings/month, free quota remains 10/week: `spiritualhuman/server/journal/voice_limits.py`, `PREMIUM_USER_MONTHLY_VOICE_LIMIT = 300` (approved 200→300, 2026-08-25).

## Verification

- `python3 scripts/check-russian-guide.py` checks all 21 navigation destinations, Russian frontmatter, unchanged code examples and technical MDX attributes, original media, localized internal links, numeric claims and absent English prose fallbacks.
- `npx mint broken-links` passed.
- `npx mint dev --port 3017` compiled the site locally. The Russian welcome page rendered with Russian locale selector, search, sidebar and article. Language-specific navbar labels are Russian; the website footer targets `/ru/`.
- The self-contained audit passes on this branch and fails without the Russian page/navigation additions.

The follow-up copy pass corrected malformed Russian wording and instructions across 16 pages. Keyboard controls remain literal key names; the regression guard fails the earlier draft that translated Shift. The Russian privacy page now describes server-side decryption for reading, export, AI replies and explicitly authorized external agents. It does not promise universal KMS deployment, company-inaccessible keys, harmless database leaks or control over external providers. Stale carousel/Inner Portrait instructions now identify the actual home sections. Immutable English source snapshots and SHA-256 records document these deliberate editorial differences; unlock thresholds and other numeric facts remain protected.

Focused browser previews of Inner World controls and the decryption disclosure were captured and inspected; local previews were stopped. These are agent source/language checks, not a claim of an exhaustive human editorial audit.

## Publication order

1. Complete normal PR review and obtain publication authorization for the guide and separately prepared Ghost drafts. Source-aware language and owned privacy/navigation corrections are completed and recorded in `docs/russian-guide-editorial-review.json`; structural checks do not themselves authorize publication.
2. Publish and verify the approved Russian Ghost post corpus and `/tag/ru/` index first. This branch prepares the three linked articles at `benefits-of-journaling-ru`, `the-vomit-system-a-proven-journaling-framework-by-campbell-walker-ru` and `your-thoughts-are-safe-how-life-note-protects-your-privacy-with-aes-gcm-encryption-ru`. Each must resolve to its reviewed Russian body before the guide merges.
3. The CEO merges the approved guide PR. The documented Mintlify integration deploys default-branch changes automatically. This agent must not merge or push to `main`.
4. Verify all 21 Russian navigation URLs on `https://guide.mylifenote.ai`, the Russian language switcher/pagination, and the localized blog links. A GitHub merge alone does not prove publication.
5. Only then approve/merge the main application's Russian rollout, including `/ru/start-here/welcome-to-life-note` links for landing and signed-in web. Ship mobile/store localization through its separately approved build/listing path.

Until these gates pass, the guide and application PRs stay drafts/off production. No external content or store metadata was published during preparation.
