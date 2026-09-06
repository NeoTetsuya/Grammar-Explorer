import sys
import io
import os
from bs4 import BeautifulSoup

def load_soup(path):
    with open(path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def save_soup(soup, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"[SAVED] {path}")

# Import templates
from card_templates import CARDS_HTML

def make_fullwidth_grid(card_html):
    wrapper_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  <div class="lg:col-span-12">
    {card_html}
  </div>
</div>
'''
    return BeautifulSoup(wrapper_html, 'html.parser').find('div', class_='grid')

def insert_grid_after_card_parent_grid(soup, card_id, new_grid_soup):
    card = soup.find(id=card_id)
    if not card:
        print(f"  [ERROR] Card #{card_id} not found!")
        return False
    # Find the parent grid of this card
    parent_grid = card.find_parent(class_=lambda c: c and 'grid-cols-12' in c)
    if not parent_grid:
        parent_grid = card.parent
    parent_grid.insert_after(new_grid_soup)
    print(f"  + Inserted full-width grid after parent of #{card_id}")
    return True

def run():
    print("==================================================")
    print("BUILDING PERFECT GRID-COMPLIANT PARITY FOR UNIT 1 & UNIT 2")
    print("==================================================")

    # -------------------------------------------------------------
    # UNIT 1 STANDALONE: grammar_explorer_2_unit_1_lesson_1.html
    # -------------------------------------------------------------
    f_u1_l1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_1.html'
    s_u1_l1 = load_soup(f_u1_l1)
    insert_grid_after_card_parent_grid(s_u1_l1, 'ex4-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex5']))
    insert_grid_after_card_parent_grid(s_u1_l1, 'ex6-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex7']))
    insert_grid_after_card_parent_grid(s_u1_l1, 'ex9-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex10']))
    save_soup(s_u1_l1, f_u1_l1)

    # -------------------------------------------------------------
    # UNIT 1 STANDALONE: grammar_explorer_2_unit_1_lesson_2.html
    # -------------------------------------------------------------
    f_u1_l2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_2.html'
    s_u1_l2 = load_soup(f_u1_l2)
    insert_grid_after_card_parent_grid(s_u1_l2, 'ex6-l2-card', make_fullwidth_grid(CARDS_HTML['u1_l2_ex7']))
    save_soup(s_u1_l2, f_u1_l2)

    # -------------------------------------------------------------
    # UNIT 1 STANDALONE: grammar_explorer_2_unit_1_review_writing.html
    # -------------------------------------------------------------
    f_u1_rw = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_review_writing.html'
    s_u1_rw = load_soup(f_u1_rw)
    insert_grid_after_card_parent_grid(s_u1_rw, 'ex3-rev-card', make_fullwidth_grid(CARDS_HTML['u1_rev_ex4']))
    save_soup(s_u1_rw, f_u1_rw)

    # -------------------------------------------------------------
    # UNIT 1 ALL-IN-ONE: GE2 - U1.html
    # -------------------------------------------------------------
    f_u1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html'
    s_u1 = load_soup(f_u1)
    insert_grid_after_card_parent_grid(s_u1, 'ex4-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex5']))
    insert_grid_after_card_parent_grid(s_u1, 'ex6-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex7']))
    insert_grid_after_card_parent_grid(s_u1, 'ex9-card', make_fullwidth_grid(CARDS_HTML['u1_l1_ex10']))
    
    # Ex 14 in Lesson 1
    c14_src = None
    for c in s_u1_l1.select('.reader-card'):
        if 'APPLY (Page 11)' in c.get_text():
            c14_src = c
            break
    if c14_src:
        c14_clean = BeautifulSoup(str(c14_src), 'html.parser').find(class_='reader-card')
        c14_clean['id'] = 'ex14-l1-card'
        c14_clean['class'] = [cls for cls in c14_clean.get('class', []) if not cls.startswith('lg:col-span')]
        insert_grid_after_card_parent_grid(s_u1, 'ex13-card', make_fullwidth_grid(str(c14_clean)))

    # Ex 7 in Lesson 2
    insert_grid_after_card_parent_grid(s_u1, 'ex6-l2-card', make_fullwidth_grid(CARDS_HTML['u1_l2_ex7']))

    # Ex 13 in Lesson 2
    c13_src = None
    for c in s_u1_l2.select('.reader-card'):
        if 'APPLY (Page 19)' in c.get_text():
            c13_src = c
            break
    if c13_src:
        c13_clean = BeautifulSoup(str(c13_src), 'html.parser').find(class_='reader-card')
        c13_clean['id'] = 'ex13-l2-card'
        c13_clean['class'] = [cls for cls in c13_clean.get('class', []) if not cls.startswith('lg:col-span')]
        # target is card 12 Venice Carnival
        target12 = None
        for c in s_u1.select('#tab-lesson2 .reader-card'):
            if 'Venice Carnival' in c.get_text():
                target12 = c
                break
        if target12:
            p_grid = target12.find_parent(class_=lambda c: c and 'grid-cols-12' in c) or target12.parent
            p_grid.insert_after(make_fullwidth_grid(str(c13_clean)))
            print("  + Inserted Ex 13 full-width grid after Venice Carnival in GE2 - U1.html")

    # Ex 4 in Review
    insert_grid_after_card_parent_grid(s_u1, 'ex3-rev-card', make_fullwidth_grid(CARDS_HTML['u1_rev_ex4']))
    save_soup(s_u1, f_u1)

    # -------------------------------------------------------------
    # UNIT 2 STANDALONE: grammar_explorer_2_unit_2_lesson_1.html
    # -------------------------------------------------------------
    f_u2_l1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_1.html'
    s_u2_l1 = load_soup(f_u2_l1)
    insert_grid_after_card_parent_grid(s_u2_l1, 'ex5-l1-card', make_fullwidth_grid(CARDS_HTML['u2_l1_ex6']))
    save_soup(s_u2_l1, f_u2_l1)

    # -------------------------------------------------------------
    # UNIT 2 STANDALONE: grammar_explorer_2_unit_2_lesson_2.html
    # -------------------------------------------------------------
    f_u2_l2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_2.html'
    s_u2_l2 = load_soup(f_u2_l2)
    insert_grid_after_card_parent_grid(s_u2_l2, 'ex6-l2-card', make_fullwidth_grid(CARDS_HTML['u2_l2_ex7']))
    save_soup(s_u2_l2, f_u2_l2)

    # -------------------------------------------------------------
    # UNIT 2 STANDALONE: grammar_explorer_2_unit_2_lesson_3.html
    # -------------------------------------------------------------
    f_u2_l3 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html'
    s_u2_l3 = load_soup(f_u2_l3)
    # in s_u2_l3, ex6-l3-card is inside div.lg:col-span-7.space-y-5
    # Insert ex7-l3-card directly after ex6-l3-card inside that column!
    ex6_tag = s_u2_l3.find(id='ex6-l3-card')
    if ex6_tag and not s_u2_l3.find(id='ex7-l3-card'):
        ex7_tag = BeautifulSoup(CARDS_HTML['u2_l3_ex7'], 'html.parser').find(id='ex7-l3-card')
        ex6_tag.insert_after(ex7_tag)
        print("  + Appended Ex 7 inside right column of Chart 2.6 in Lesson 3 standalone")
    save_soup(s_u2_l3, f_u2_l3)

    # -------------------------------------------------------------
    # UNIT 2 STANDALONE: grammar_explorer_2_unit_2_review_writing.html
    # -------------------------------------------------------------
    f_u2_rw = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_review_writing.html'
    s_u2_rw = load_soup(f_u2_rw)
    # Ex 1 is currently in a 12-col grid with lg:col-span-7. Change to lg:col-span-6 and add Ex 2 with lg:col-span-6
    ex1_card = s_u2_rw.find(id='ex1-rev-card')
    if ex1_card:
        ex1_card['class'] = [cls if cls != 'lg:col-span-7' else 'lg:col-span-6' for cls in ex1_card.get('class', [])]
        ex2_card_html = CARDS_HTML['u2_rev_ex2']
        ex2_tag = BeautifulSoup(ex2_card_html, 'html.parser').find(id='ex2-rev-card')
        ex2_tag['class'] = ['lg:col-span-6'] + [c for c in ex2_tag.get('class', []) if not c.startswith('lg:col-span')]
        ex1_card.insert_after(ex2_tag)
        print("  + Formed balanced 6+6 grid with Ex 1 and Ex 2 in Review standalone")
    
    # Ex 5 after Ex 4
    insert_grid_after_card_parent_grid(s_u2_rw, 'ex4-rev-card', make_fullwidth_grid(CARDS_HTML['u2_rev_ex5']))
    save_soup(s_u2_rw, f_u2_rw)

    # -------------------------------------------------------------
    # UNIT 2 ALL-IN-ONE: GE2 - U2.html
    # -------------------------------------------------------------
    f_u2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html'
    s_u2 = load_soup(f_u2)

    # Tab Lesson 1: Ex 6 SPEAK
    insert_grid_after_card_parent_grid(s_u2, 'ex5-l1-card', make_fullwidth_grid(CARDS_HTML['u2_l1_ex6']))
    
    # Tab Lesson 1: Ex 11 APPLY
    c11_l1 = None
    for c in s_u2_l1.select('.reader-card'):
        if '11' in c.get_text() and 'APPLY' in c.get_text():
            c11_l1 = c
            break
    if c11_l1:
        c11_l1_clean = BeautifulSoup(str(c11_l1), 'html.parser').find(class_='reader-card')
        c11_l1_clean['id'] = 'ex11-l1-card'
        c11_l1_clean['class'] = [cls for cls in c11_l1_clean.get('class', []) if not cls.startswith('lg:col-span')]
        insert_grid_after_card_parent_grid(s_u2, 'ex10-l1-card', make_fullwidth_grid(str(c11_l1_clean)))

    # Tab Lesson 2: Ex 5 WRITE & SPEAK
    c5_l2 = None
    for c in s_u2_l2.select('.reader-card'):
        if '5' in c.get_text() and 'Time Anchors' in c.get_text():
            c5_l2 = c
            break
    if c5_l2:
        c5_l2_clean = BeautifulSoup(str(c5_l2), 'html.parser').find(class_='reader-card')
        c5_l2_clean['id'] = 'ex5-l2-card'
        c5_l2_clean['class'] = [cls for cls in c5_l2_clean.get('class', []) if not cls.startswith('lg:col-span')]
        insert_grid_after_card_parent_grid(s_u2, 'ex4-l2-card', make_fullwidth_grid(str(c5_l2_clean)))

    # Tab Lesson 2: Ex 7 SPEAK
    insert_grid_after_card_parent_grid(s_u2, 'ex6-l2-card', make_fullwidth_grid(CARDS_HTML['u2_l2_ex7']))

    # Tab Lesson 2: Ex 11 APPLY
    c11_l2 = None
    for c in s_u2_l2.select('.reader-card'):
        if '11' in c.get_text() and 'APPLY' in c.get_text():
            c11_l2 = c
            break
    if c11_l2:
        c11_l2_clean = BeautifulSoup(str(c11_l2), 'html.parser').find(class_='reader-card')
        c11_l2_clean['id'] = 'ex11-l2-card'
        c11_l2_clean['class'] = [cls for cls in c11_l2_clean.get('class', []) if not cls.startswith('lg:col-span')]
        insert_grid_after_card_parent_grid(s_u2, 'ex10-l2-card', make_fullwidth_grid(str(c11_l2_clean)))

    # Tab Lesson 3: Chart 2.6 + Ex 5, 6, 7 Grid
    # We take the exact grid from s_u2_l3 (which is Grid 2: Chart 2.6 col-5 + right column col-7 with Ex 5, 6, 7)
    chart2_6_card = None
    for c in s_u2_l3.select('.reader-card'):
        if '2.6' in c.get_text() and 'Events in Sequence' in c.get_text():
            chart2_6_card = c
            break
    ex5_tag = s_u2_l3.find(id='ex5-l3-card')
    ex6_tag = s_u2_l3.find(id='ex6-l3-card')
    ex7_tag = s_u2_l3.find(id='ex7-l3-card')

    if chart2_6_card and ex5_tag and ex6_tag:
        l3_new_grid_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  <div class="lg:col-span-5">
    {str(chart2_6_card)}
  </div>
  <div class="lg:col-span-7 space-y-5">
    {str(ex5_tag)}
    {str(ex6_tag)}
    {str(ex7_tag)}
  </div>
</div>
'''
        l3_new_grid_soup = BeautifulSoup(l3_new_grid_html, 'html.parser').find('div', class_='grid')
        insert_grid_after_card_parent_grid(s_u2, 'ex4-l3-card', l3_new_grid_soup)
        print("  + Inserted full Chart 2.6 + Ex 5, 6, 7 grid in GE2 - U2.html Lesson 3")

    # Tab Lesson 3: Ex 10 Marta's Blog & Ex 11 APPLY in a 6+6 grid
    c10_l3 = None
    c11_l3 = None
    for c in s_u2_l3.select('.reader-card'):
        if 'Marta' in c.get_text() and 'Blog' in c.get_text():
            c10_l3 = c
        elif '11' in c.get_text() and 'Accident Story' in c.get_text():
            c11_l3 = c
    if c10_l3 and c11_l3:
        c10_clean = BeautifulSoup(str(c10_l3), 'html.parser').find(class_='reader-card')
        c10_clean['class'] = ['lg:col-span-6'] + [cls for cls in c10_clean.get('class', []) if not cls.startswith('lg:col-span')]
        c11_clean = BeautifulSoup(str(c11_l3), 'html.parser').find(class_='reader-card')
        c11_clean['class'] = ['lg:col-span-6'] + [cls for cls in c11_clean.get('class', []) if not cls.startswith('lg:col-span')]
        l3_apply_grid_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  {str(c10_clean)}
  {str(c11_clean)}
</div>
'''
        l3_apply_grid_soup = BeautifulSoup(l3_apply_grid_html, 'html.parser').find('div', class_='grid')
        insert_grid_after_card_parent_grid(s_u2, 'ex9-l3-card', l3_apply_grid_soup)
        print("  + Inserted Marta's Blog & Accident Story 6+6 grid in GE2 - U2.html Lesson 3")

    # Tab Lesson 4:
    # Load s_u2_l4
    f_u2_l4 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html'
    s_u2_l4 = load_soup(f_u2_l4)

    # 1. Chart 2.8 + Ex 5 & Ex 6 grid
    chart2_8 = None
    for c in s_u2_l4.select('.reader-card'):
        if '2.8' in c.get_text() and 'Used To: Questions' in c.get_text():
            chart2_8 = c
            break
    ex5_l4 = s_u2_l4.find(id='ex5-l4-card')
    ex6_l4 = None
    for c in s_u2_l4.select('.reader-card'):
        if '6' in c.get_text() and 'Childhood Habits' in c.get_text():
            ex6_l4 = c
            break
    if chart2_8 and ex5_l4 and ex6_l4:
        l4_c28_grid_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  <div class="lg:col-span-5">
    {str(chart2_8)}
  </div>
  <div class="lg:col-span-7 space-y-5">
    {str(ex5_l4)}
    {str(ex6_l4)}
  </div>
</div>
'''
        l4_c28_soup = BeautifulSoup(l4_c28_grid_html, 'html.parser').find('div', class_='grid')
        insert_grid_after_card_parent_grid(s_u2, 'ex4-l4-card', l4_c28_soup)
        print("  + Inserted Chart 2.8 + Ex 5 & Ex 6 grid in GE2 - U2.html Lesson 4")

    # 2. In Lesson 4, Chart 2.9 (Would) was a lonely card in s_u2. Replace its container with Chart 2.9 + Ex 7 grid!
    chart2_9_l4 = None
    for c in s_u2_l4.select('.reader-card'):
        if '2.9' in c.get_text() and 'Would' in c.get_text():
            chart2_9_l4 = c
            break
    ex7_l4 = s_u2_l4.find(id='ex7-l4-card')
    if chart2_9_l4 and ex7_l4:
        # find where chart 2.9 is in s_u2
        c29_in_s_u2 = None
        for c in s_u2.select('#tab-lesson4 .reader-card'):
            if '2.9' in c.get_text() and 'Would' in c.get_text():
                c29_in_s_u2 = c
                break
        if c29_in_s_u2:
            p_grid = c29_in_s_u2.find_parent(class_=lambda c: c and 'grid-cols-12' in c) or c29_in_s_u2.parent
            l4_c29_grid_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  <div class="lg:col-span-5">
    {str(chart2_9_l4)}
  </div>
  <div class="lg:col-span-7">
    {str(ex7_l4)}
  </div>
</div>
'''
            l4_c29_soup = BeautifulSoup(l4_c29_grid_html, 'html.parser').find('div', class_='grid')
            p_grid.replace_with(l4_c29_soup)
            print("  + Replaced Chart 2.9 with Chart 2.9 + Ex 7 grid in GE2 - U2.html Lesson 4")

    # 3. In Lesson 4, add Ex 9 & Ex 10 after Ex 8 in a 6+6 grid
    c9_l4 = None
    c10_l4 = None
    for c in s_u2_l4.select('.reader-card'):
        if '9' in c.get_text() and '5,000 Years Ago' in c.get_text():
            c9_l4 = c
        elif '10' in c.get_text() and 'Personal Life Changes' in c.get_text():
            c10_l4 = c
    if c9_l4 and c10_l4:
        c9_clean = BeautifulSoup(str(c9_l4), 'html.parser').find(class_='reader-card')
        c9_clean['class'] = ['lg:col-span-6'] + [cls for cls in c9_clean.get('class', []) if not cls.startswith('lg:col-span')]
        c10_clean = BeautifulSoup(str(c10_l4), 'html.parser').find(class_='reader-card')
        c10_clean['class'] = ['lg:col-span-6'] + [cls for cls in c10_clean.get('class', []) if not cls.startswith('lg:col-span')]
        l4_apply_grid_html = f'''
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
  {str(c9_clean)}
  {str(c10_clean)}
</div>
'''
        l4_apply_soup = BeautifulSoup(l4_apply_grid_html, 'html.parser').find('div', class_='grid')
        insert_grid_after_card_parent_grid(s_u2, 'ex8-l4-card', l4_apply_soup)
        print("  + Inserted Ex 9 & Ex 10 6+6 grid in GE2 - U2.html Lesson 4")

    # Tab Review in GE2 - U2.html:
    # 1. Ex 1 + Ex 2 in 6+6 grid
    ex1_card_u2 = s_u2.find(id='ex1-rev-card')
    if ex1_card_u2:
        ex1_card_u2['class'] = [cls if cls != 'lg:col-span-7' else 'lg:col-span-6' for cls in ex1_card_u2.get('class', [])]
        ex2_tag = BeautifulSoup(CARDS_HTML['u2_rev_ex2'], 'html.parser').find(id='ex2-rev-card')
        ex2_tag['class'] = ['lg:col-span-6'] + [cls for cls in ex2_tag.get('class', []) if not cls.startswith('lg:col-span')]
        ex1_card_u2.insert_after(ex2_tag)
        print("  + Formed balanced 6+6 grid with Ex 1 and Ex 2 in GE2 - U2.html Review")

    # 2. Ex 5 SPEAK after Ex 4
    insert_grid_after_card_parent_grid(s_u2, 'ex4-rev-card', make_fullwidth_grid(CARDS_HTML['u2_rev_ex5']))
    save_soup(s_u2, f_u2)

    print("\n==================================================")
    print("ALL FILES SUCCESSFULLY RECONSTRUCTED WITH BALANCED GRIDS!")
    print("==================================================")

run()
