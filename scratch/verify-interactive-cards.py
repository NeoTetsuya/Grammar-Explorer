import sys
import io
import os
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MODIFIED_FILES = [
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_1.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_2.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_review_writing.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_1.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_2.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html',
    'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_review_writing.html'
]

print("=== VERIFYING MODIFIED FILES ===")
total_cards = 0
for fpath in MODIFIED_FILES:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Check body background
    body = soup.find('body')
    bg_cls = body.get('class', []) if body else []
    is_light = any('bg-slate-100' in c for c in bg_cls)
    
    cards = soup.select('.reader-card')
    cloze_inputs = soup.select('input.cloze-input')
    buttons = soup.select('button[onclick]')
    
    print(f"\nFile: {os.path.basename(fpath)}")
    print(f"  Light BG: {'✓' if is_light else '✗ (' + str(bg_cls) + ')'}")
    print(f"  Reader Cards: {len(cards)}")
    print(f"  Cloze Inputs: {len(cloze_inputs)}")
    print(f"  Buttons with onclick: {len(buttons)}")
    
    # Check for empty data-ans
    empty_ans = [inp for inp in cloze_inputs if not inp.get('data-ans')]
    if empty_ans:
        print(f"  [WARN] Found {len(empty_ans)} cloze inputs without data-ans!")
    else:
        print(f"  Cloze data-ans: All {len(cloze_inputs)} have valid answers ✓")
        
    total_cards += len(cards)

print(f"\nTotal reader cards verified across all 10 files: {total_cards}")
