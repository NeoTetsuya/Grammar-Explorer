from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html', 'r', encoding='utf-8').read(), 'html.parser')
grids = soup.find_all(class_=lambda c: c and 'grid-cols-12' in c)
g1 = grids[1]
g2 = grids[2]

curr = g1.next_sibling
while curr and curr != g2:
    if getattr(curr, 'name', None):
        print(f"<{curr.name} class='{curr.get('class')}'>")
        for c in curr.select('.reader-card'):
            print(f"   Card #{c.get('id')} span: {[cls for cls in c.get('class', []) if 'col-span' in cls]}")
    curr = curr.next_sibling
