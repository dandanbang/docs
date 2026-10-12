#!/usr/bin/env python3
"""Fail closed on Russian guide omissions and changed technical examples."""
import collections
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'docs.json').read_text())
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
    expected_refs = [url.replace('/en/', '/ru/').replace('/faq', '/ru/faq') if url.startswith('/') else url for url in refs(source)]
    expected_refs = ['#заблокировать-само-приложение' if url == '#lock-the-app-itself' else url for url in expected_refs]
    assert collections.Counter(expected_refs) == collections.Counter(refs(translated)), (target, 'links')
    assert numbers(source) == numbers(translated), (target, 'numeric claims')
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
print('21 Russian pages: navigation, frontmatter, code, media, links, numbers and no English prose fallback passed')
