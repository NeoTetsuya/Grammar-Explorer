from bs4 import BeautifulSoup

def check_all_new_cards(fpath, card_ids):
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

check_all_new_cards('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html', [
    'ex5-l1-card', 'ex7-l1-card', 'ex10-l1-card', 'ex14-l1-card', 'ex7-l2-card', 'ex13-l2-card', 'ex4-rev-card'
])

check_all_new_cards('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html', [
    'ex6-l1-card', 'ex11-l1-card', 'ex5-l2-card', 'ex7-l2-card', 'ex11-l2-card',
    'ex5-l3-card', 'ex6-l3-card', 'ex7-l3-card', 'ex5-l4-card', 'ex7-l4-card',
    'ex8-l4-card', 'ex2-rev-card', 'ex5-rev-card'
])
