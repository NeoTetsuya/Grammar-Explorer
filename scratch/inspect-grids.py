from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html', 'r', encoding='utf-8').read(), 'html.parser')

grids = soup.find_all(class_=lambda c: c and 'grid-cols-12' in c)
print(f"Total 12-col grids: {len(grids)}")
for i, grid in enumerate(grids):
    cards = [c for c in grid.children if c.name and 'reader-card' in c.get('class', [])]
    span_strs = [' '.join([cls for cls in (c.get('class', []) or []) if 'col-span' in cls]) for c in cards]
    card_ids = [c.get('id', 'no-id') for c in cards]
    print(f"Grid {i}: {len(cards)} card(s) -> IDs: {card_ids} -> Spans: {span_strs}")
