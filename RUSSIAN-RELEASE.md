# Russian guide release

This branch adds all 20 published English guide pages plus a Russian version of the shared free/subscription FAQ: 21 Russian navigation destinations. The unlisted starter snippet is excluded. English and Traditional Chinese navigation remain in place.

The source revision is `e067fca`. Russian prose was drafted locally with an offline EN→RU model; page titles, navigation, product controls, privacy/security disclosures, import/deletion instructions and other selected passages were manually reviewed. No journal data or credentials were involved. Native-speaker review is still required before publication. Shared image and video references remain unchanged; screenshots within those assets currently show the source UI language.

Two outdated source facts were corrected in English and Russian under the CEO's existing approved behavior, with no product change:

- Inner Wisdom opens after 4 entries: `spiritualhuman/server/utils/unlock_thresholds.py`, `INNER_WISDOM_UNLOCK_ENTRIES = 4` (CEO curve, 2026-08-20).
- Paid voice quota is 300 recordings/month, free quota remains 10/week: `spiritualhuman/server/journal/voice_limits.py`, `PREMIUM_USER_MONTHLY_VOICE_LIMIT = 300` (approved 200→300, 2026-08-25).

## Verification

- `python3 scripts/check-russian-guide.py` checks all 21 navigation destinations, Russian frontmatter, unchanged code examples and technical MDX attributes, original media, localized internal links, numeric claims and absent English prose fallbacks.
- `npx mint broken-links` passed.
- `npx mint dev --port 3017` compiled the site locally. The Russian welcome page rendered with Russian locale selector, search, sidebar and article. Language-specific navbar labels are Russian; the website footer targets `/ru/`.
- The self-contained audit passes on this branch and fails without the Russian page/navigation additions.

## Publication order

1. Complete native-speaker/content review and approve this guide PR. Review existing source claims as well as translation; publication is not authorized by a passing structural audit.
2. The CEO merges the approved guide PR. The repository's documented Mintlify integration deploys default-branch changes automatically. This agent must not merge or push to `main`.
3. Verify every URL named by Russian navigation on `https://guide.mylifenote.ai`, plus the Russian language switcher and pagination. A GitHub merge alone does not prove publication.
4. Publish and verify the Russian Ghost post corpus and Russian index/tag destinations from the separately prepared drafts. Blog links in this guide include the privacy/encryption article, `benefits-of-journaling` and the Campbell Walker VOMIT article; they remain at existing live originals in this draft until those Russian destinations are published and an approved link update is made.
5. Only then approve/merge the main application's Russian rollout, which includes explicit `/ru/start-here/welcome-to-life-note` links for landing and signed-in web. Ship the mobile/store localization via its separately approved build/listing path.

Until these gates pass, the guide and application PRs stay drafts/off production. No external content or store metadata was published during preparation.
