from bs4 import BeautifulSoup

def check_standalone(fpath, card_ids):
    soup = BeautifulSoup(open(fpath, 'r', encoding='utf-8').read(), 'html.parser')
    print(f"\nChecking {fpath}:")
    for cid in card_ids:
        c = soup.find(id=cid)
        if not c:
            print(f"  [MISSING] #{cid}")
        else:
            p = c.parent
            p2 = p.parent if p else None
            p_cls = ' '.join(p.get('class', [])) if p else ''
            p2_cls = ' '.join(p2.get('class', [])) if p2 else ''
            print(f"  [OK] #{cid} | Parent: <{p.name} class='{p_cls}'> | Grandparent: <{p2.name} class='{p2_cls}'>")

check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_1.html', ['ex5-l1-card', 'ex7-l1-card', 'ex10-l1-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_2.html', ['ex7-l2-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_review_writing.html', ['ex4-rev-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_1.html', ['ex6-l1-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_2.html', ['ex7-l2-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html', ['ex5-l3-card', 'ex6-l3-card', 'ex7-l3-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html', ['ex5-l4-card', 'ex7-l4-card', 'ex8-l4-card'])
check_standalone('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_review_writing.html', ['ex2-rev-card', 'ex5-rev-card'])
