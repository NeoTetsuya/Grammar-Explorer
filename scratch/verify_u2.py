import sys
import io
import re
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

files = [
    ('GE2 - U2.html', ['2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', 'GRAMMAR FOCUS']),
    ('grammar_explorer_2_unit_2_lesson_1.html', ['2.1', '2.2']),
    ('grammar_explorer_2_unit_2_lesson_2.html', ['2.3', '2.4']),
    ('grammar_explorer_2_unit_2_lesson_3.html', ['2.5', '2.6']),
    ('grammar_explorer_2_unit_2_lesson_4.html', ['2.7', '2.8', '2.9']),
    ('grammar_explorer_2_unit_2_review_writing.html', ['GRAMMAR FOCUS', 'WRITING FOCUS'])
]

base_dir = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/'

all_ok = True
for fname, required_elements in files:
    fpath = base_dir + fname
    print(f"\nVerifying {fname}...")
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Check required grammar elements
    for el in required_elements:
        found = False
        for c in soup.select('.reader-card'):
            if el in c.get_text():
                found = True
                break
        if found:
            print(f"  [OK] Found grammar element: {el}")
        else:
            print(f"  [FAIL] Missing grammar element: {el}")
            all_ok = False

    # 2. Check total reader-cards
    cards = soup.select('.reader-card')
    print(f"  Total reader cards: {len(cards)}")

    # 3. Check interactive inputs and check buttons
    inputs = soup.select('input.cloze-input, select.select-check, .tf-row')
    buttons = [b for b in soup.select('button') if 'check' in (b.get('onclick') or '').lower()]
    print(f"  Interactive inputs: {len(inputs)}, Check buttons: {len(buttons)}")

    # 4. Check sub-tab button vs pane parity
    tab_btns = [b.get('data-extab') for b in soup.select('button[data-extab]')]
    tab_panes = [p.get('id') for p in soup.select('.ex-tab-pane')]
    for tb in tab_btns:
        if tb not in tab_panes:
            print(f"  [WARN] Tab button {tb} has no matching pane!")
            all_ok = False
    print(f"  Tab buttons: {len(tab_btns)}, Tab panes: {len(tab_panes)} (Parity check OK)")

if all_ok:
    print("\n>>> ALL UNIT 2 VERIFICATION CHECKS PASSED SUCCESSFULLY! <<<")
else:
    print("\n>>> UNIT 2 VERIFICATION FOUND ISSUES! <<<")
