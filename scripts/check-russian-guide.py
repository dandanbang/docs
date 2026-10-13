#!/usr/bin/env python3
"""Fail closed on Russian guide omissions and changed technical examples."""
import collections
import hashlib
import json
from pathlib import Path
import re

BLOG_LOCALIZATIONS = {'https://blog.mylifenote.ai/benefits-of-journaling/': 'https://blog.mylifenote.ai/benefits-of-journaling-ru/', 'https://blog.mylifenote.ai/the-vomit-system-a-proven-journaling-framework-by-campbell-walker/': 'https://blog.mylifenote.ai/the-vomit-system-a-proven-journaling-framework-by-campbell-walker-ru/', 'https://blog.mylifenote.ai/your-thoughts-are-safe-how-life-note-protects-your-privacy-with-aes-gcm-encryption/': 'https://blog.mylifenote.ai/your-thoughts-are-safe-how-life-note-protects-your-privacy-with-aes-gcm-encryption-ru/'}
ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'docs.json').read_text())
editorial = json.loads((ROOT / 'docs/russian-guide-editorial-review.json').read_text())
NAVIGATION_NUMBER_CORRECTIONS = {
    'en/advanced/inner-wisdom.mdx': ['6'],
    'en/advanced/your-inner-weather.mdx': ['3', '4'],
}
for source_name, record in editorial['pages'].items():
    snapshot = (ROOT / record['source_snapshot']).read_bytes()
    assert hashlib.sha256(snapshot).hexdigest() == record['sha256'], source_name
    assert snapshot == (ROOT / source_name).read_bytes(), (source_name, 'editorial source drift')
locales = {entry['language']: entry for entry in config['navigation']['languages']}

def pages(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [page for item in value for page in pages(item)]
    if isinstance(value, dict):
        return pages(value.get('pages', [])) + pages(value.get('tabs', []))
    return []

def localized(path):
    return 'ru/faq' if path == 'faq' else path.replace('en/', 'ru/', 1)

def numbers(text):
    text = re.sub(r'```.*?```|https?://\S+|/images/\S+', '', text, flags=re.S)
    return collections.Counter(
        value.replace(',', '').replace(' ', '')
        for value in re.findall(r'\d+(?:[, ]\d{3})*', text)
    )

expected = [localized(path) for path in pages(locales['en'])]
actual = pages(locales['ru'])
assert locales['ru']['navbar']['links'][1]['href'] == 'https://blog.mylifenote.ai/tag/ru/'
assert len(expected) == len(actual) == 21
assert set(expected) == set(actual), 'Russian navigation must cover every English page'
for source_path in pages(locales['en']):
    source = (ROOT / (source_path + '.mdx')).read_text()
    target = ROOT / (localized(source_path) + '.mdx')
    assert target.is_file(), target
    translated = target.read_text()
    for field in ['title', 'description']:
        match = re.search(r'^' + field + r':\s*"(.*?)"$', translated, re.M)
        assert match and re.search('[А-Яа-яЁё]', match[1]), (target, field)
    assert re.findall(r'```.*?```', source, re.S) == re.findall(r'```.*?```', translated, re.S), (target, 'code blocks')
    assert re.findall(r'`[^`\n]+`', source) == re.findall(r'`[^`\n]+`', translated), (target, 'inline code')
    for attribute in ['src', 'img', 'icon', 'className', 'style', 'cols', 'width', 'height']:
        pattern = r'\b' + attribute + r'=("[^"]*"|\{[^\n]*\})'
        assert re.findall(pattern, source) == re.findall(pattern, translated), (target, attribute)
    refs = lambda text: re.findall(r'(?:\]\(|href=")([^\s"\)]+)', text)
    expected_refs = [url.replace('/en/', '/ru/').replace('/faq', '/ru/faq') if url.startswith('/') else BLOG_LOCALIZATIONS.get(url, url) for url in refs(source)]
    expected_refs = ['#заблокировать-само-приложение' if url == '#lock-the-app-itself' else url for url in expected_refs]
    assert collections.Counter(expected_refs) == collections.Counter(refs(translated)), (target, 'links')
    source_numbers = numbers(source)
    # Only stale carousel positions are removed; unlock thresholds, examples,
    # retention periods and all other numeric claims remain protected.
    approved_removals = NAVIGATION_NUMBER_CORRECTIONS.get(source_path + '.mdx', [])
    if approved_removals:
        record = editorial['pages'][source_path + '.mdx']
        assert record['removed_numeric_labels'] == approved_removals
        snapshot = (ROOT / record['source_snapshot']).read_bytes()
        assert hashlib.sha256(snapshot).hexdigest() == record['sha256']
        assert snapshot.decode() == source, (target, 'editorial source drift')
        source_numbers.subtract(approved_removals)
        source_numbers = +source_numbers
    assert source_numbers == numbers(translated), (target, 'numeric claims')
    prose = re.sub(r'```.*?```', '', source, flags=re.S)
    for line in prose.splitlines():
        line = line.strip()
        if (len(line) < 12 or not re.search('[A-Za-z]', line)
            or re.match(r'^(?:<|>|/?>|(?:src|alt|title|caption|style|className|href|icon|img|cols|width|height)=)', line)
            or re.match(r'^(?:title|sidebarTitle|description|icon):', line)):
            continue
        assert line not in translated.splitlines(), (target, 'unchanged English prose', line)
assert '#lock-the-app-itself' not in (ROOT/'ru/start-here/privacy-and-security.mdx').read_text()
assert 'должны иметь возможность расшифровать твою запись' in (ROOT/'ru/start-here/privacy-and-security.mdx').read_text()
assert 'Он **не может** писать' in (ROOT/'ru/developers/lifenote-cli.mdx').read_text()
privacy = (ROOT/'ru/start-here/privacy-and-security.mdx').read_text()
assert 'при чтении и экспорте дневника' in privacy
assert 'внешнему агенту, которого ты явно подключил' in privacy
assert 'как прежнюю схему защиты ключей, так и AWS KMS' in privacy
for unsupported_claim in ['куда у нас нет доступа', 'нельзя извлечь из оборудования',
                          'неопасным событием', 'ни нашей, ни чьей-либо ещё']:
    assert unsupported_claim not in privacy, ('unsupported Russian privacy guarantee', unsupported_claim)
for page in ['ru/advanced/inner-wisdom.mdx', 'ru/advanced/your-inner-weather.mdx',
             'ru/essentials/memory-orb.mdx']:
    assert 'ваш внутренний портрет' not in (ROOT/page).read_text(), (page, 'wrong feature navigation')
inner_world = (ROOT/'ru/advanced/your-inner-world.mdx').read_text()
# Key names are controls, not translatable prose: translating Shift made the
# running instruction impossible to follow even though links/numbers matched.
for key in ['W A S D', 'Shift', 'Space', 'E', 'F', '[', ']', '?']:
    assert f'**{key}**' in inner_world, ('Russian Inner World keyboard control', key)
print('21 Russian pages: navigation, frontmatter, code, media, links, numbers and no English prose fallback passed')
