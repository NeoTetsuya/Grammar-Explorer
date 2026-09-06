from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html', 'r', encoding='utf-8').read(), 'html.parser')

tab_l1 = soup.find('section', id='tab-lesson1')
for i, child in enumerate(tab_l1.children):
    if child.name:
        cards = child.select('.reader-card')
        classes = ' '.join(child.get('class', []))
        print(f"Child {i}: <{child.name} class='{classes}'> with {len(cards)} card(s)")
        for c in cards:
            c_cls = ' '.join(c.get('class', []))
            cid = c.get('id', 'no-id')
            print(f"    - Card #{cid} (class='{c_cls[:40]}...')")
