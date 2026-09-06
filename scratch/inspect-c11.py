from bs4 import BeautifulSoup

soup = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html', 'r', encoding='utf-8').read(), 'html.parser')
tab_l1 = soup.find('section', id='tab-lesson1')

for div in tab_l1.find_all('div', recursive=False):
    for child in div.children:
        if child.name:
            cards = child.select('.reader-card')
            classes = ' '.join(child.get('class', []))
            print(f"<{child.name} class='{classes}'> : {len(cards)} card(s)")
            for c in child.find_all(class_='reader-card', recursive=False):
                print(f"   Direct card #{c.get('id')} classes: {c.get('class')}")
