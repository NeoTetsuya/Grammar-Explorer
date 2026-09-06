from bs4 import BeautifulSoup

s_u2 = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html', 'r', encoding='utf-8').read(), 'html.parser')
s_u2_l4 = BeautifulSoup(open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html', 'r', encoding='utf-8').read(), 'html.parser')

ex8 = s_u2_l4.find(id='ex8-l4-card')
c9_l4 = None
c10_l4 = None
for c in s_u2_l4.select('.reader-card'):
    if '5,000 Years Ago' in c.get_text():
        c9_l4 = c
    elif 'Personal Life Changes' in c.get_text():
        c10_l4 = c

ex7 = s_u2.find(id='ex7-l4-card')
p_grid = ex7.find_parent(class_=lambda c: c and 'grid-cols-12' in c)

if ex8 and not s_u2.find(id='ex8-l4-card'):
    ex8_clean = BeautifulSoup(str(ex8), 'html.parser').find(class_='reader-card')
    ex8_clean['class'] = [cls for cls in ex8_clean.get('class', []) if not cls.startswith('lg:col-span')]
    grid8_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  <div class="lg:col-span-12">
    {str(ex8_clean)}
  </div>
</div>
'''
    grid8_soup = BeautifulSoup(grid8_html, 'html.parser').find('div', class_='grid')
    p_grid.insert_after(grid8_soup)
    print('Inserted Ex 8 full-width into Lesson 4')
    p_grid = grid8_soup

if c9_l4 and c10_l4 and not any('5,000 Years Ago' in c.get_text() for c in s_u2.select('#tab-lesson4 .reader-card')):
    c9_clean = BeautifulSoup(str(c9_l4), 'html.parser').find(class_='reader-card')
    c9_clean['class'] = ['lg:col-span-6'] + [cls for cls in c9_clean.get('class', []) if not cls.startswith('lg:col-span')]
    c10_clean = BeautifulSoup(str(c10_l4), 'html.parser').find(class_='reader-card')
    c10_clean['class'] = ['lg:col-span-6'] + [cls for cls in c10_clean.get('class', []) if not cls.startswith('lg:col-span')]
    grid9_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  {str(c9_clean)}
  {str(c10_clean)}
</div>
'''
    grid9_soup = BeautifulSoup(grid9_html, 'html.parser').find('div', class_='grid')
    p_grid.insert_after(grid9_soup)
    print('Inserted Ex 9 & Ex 10 6+6 grid into Lesson 4')

with open('Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html', 'w', encoding='utf-8') as f:
    f.write(str(s_u2))
print('Saved GE2 - U2.html')
