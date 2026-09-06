from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html', 'r', encoding='utf-8').read(), 'html.parser')

grids = soup.find_all(class_=lambda c: c and 'grid-cols-12' in c)
print(f"Grids in unit 2 lesson 3 standalone: {len(grids)}")
for i, g in enumerate(grids):
    cards = [c for c in g.children if c.name and 'reader-card' in c.get('class', [])]
    spans = [' '.join([cls for cls in c.get('class', []) if 'col-span' in cls]) for c in cards]
    ids = [c.get('id', 'no-id') for c in cards]
    print(f"Grid {i}: IDs: {ids} -> Spans: {spans}")
