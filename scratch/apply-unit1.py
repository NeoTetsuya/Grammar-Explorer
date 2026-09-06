import sys
import io
import os
from bs4 import BeautifulSoup

# sys.stdout utf-8

# Import templates
from card_templates import CARDS_HTML

def load_soup(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def save_soup(soup, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"[SAVED] {filepath}")

def insert_after_card(soup, target_id, new_card_html, new_id=None):
    if new_id and soup.find(id=new_id):
        print(f"  - Card {new_id} already exists in soup, skipping.")
        return False
    target = soup.find(id=target_id)
    if not target:
        print(f"  [WARN] Target #{target_id} not found!")
        return False
    new_tag = BeautifulSoup(new_card_html, 'html.parser').find(class_=lambda c: c and 'reader-card' in c)
    if not new_tag:
        new_tag = BeautifulSoup(new_card_html, 'html.parser')
    target.insert_after(new_tag)
    print(f"  + Inserted {new_id or 'new card'} after #{target_id}")
    return True

def apply_unit1():
    print("\n=======================================================")
    print("UPDATING UNIT 1 FILES")
    print("=======================================================")
    
    # 1. Update standalone grammar_explorer_2_unit_1_lesson_1.html
    f_l1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_1.html'
    s_l1 = load_soup(f_l1)
    insert_after_card(s_l1, 'ex4-card', CARDS_HTML['u1_l1_ex5'], 'ex5-l1-card')
    insert_after_card(s_l1, 'ex6-card', CARDS_HTML['u1_l1_ex7'], 'ex7-l1-card')
    insert_after_card(s_l1, 'ex9-card', CARDS_HTML['u1_l1_ex10'], 'ex10-l1-card')
    save_soup(s_l1, f_l1)
    
    # 2. Update standalone grammar_explorer_2_unit_1_lesson_2.html
    f_l2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_2.html'
    s_l2 = load_soup(f_l2)
    insert_after_card(s_l2, 'ex6-l2-card', CARDS_HTML['u1_l2_ex7'], 'ex7-l2-card')
    save_soup(s_l2, f_l2)
    
    # 3. Update standalone grammar_explorer_2_unit_1_review_writing.html
    f_rw = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_review_writing.html'
    s_rw = load_soup(f_rw)
    insert_after_card(s_rw, 'ex3-rev-card', CARDS_HTML['u1_rev_ex4'], 'ex4-rev-card')
    save_soup(s_rw, f_rw)
    
    # 4. Update GE2 - U1.html (All-in-one)
    f_u1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html'
    s_u1 = load_soup(f_u1)
    
    # tab-lesson1:
    insert_after_card(s_u1, 'ex4-card', CARDS_HTML['u1_l1_ex5'], 'ex5-l1-card')
    insert_after_card(s_u1, 'ex6-card', CARDS_HTML['u1_l1_ex7'], 'ex7-l1-card')
    insert_after_card(s_u1, 'ex9-card', CARDS_HTML['u1_l1_ex10'], 'ex10-l1-card')
    
    # Add Ex 14 from s_l1 if not present
    if not any('14' in c.get_text() and 'APPLY' in c.get_text() for c in s_u1.select('#tab-lesson1 .reader-card')):
        card14 = None
        for c in s_l1.select('.reader-card'):
            if '14' in c.get_text() and 'APPLY' in c.get_text():
                card14 = c
                break
        if card14:
            target13 = s_u1.find(id='ex13-card')
            if target13:
                c14_copy = BeautifulSoup(str(card14), 'html.parser').find(class_='reader-card')
                target13.insert_after(c14_copy)
                print("  + Copied Ex 14 APPLY to GE2 - U1.html Lesson 1")

    # tab-lesson2:
    insert_after_card(s_u1, 'ex6-l2-card', CARDS_HTML['u1_l2_ex7'], 'ex7-l2-card')
    
    # Add Ex 13 from s_l2 if not present
    if not any('13' in c.get_text() and 'APPLY' in c.get_text() for c in s_u1.select('#tab-lesson2 .reader-card')):
        card13 = None
        for c in s_l2.select('.reader-card'):
            if '13' in c.get_text() and 'APPLY' in c.get_text():
                card13 = c
                break
        if card13:
            # target is card 12 Venice Carnival
            target12 = None
            for c in s_u1.select('#tab-lesson2 .reader-card'):
                if '12' in c.get_text() and 'Venice Carnival' in c.get_text():
                    target12 = c
                    break
            if target12:
                c13_copy = BeautifulSoup(str(card13), 'html.parser').find(class_='reader-card')
                target12.insert_after(c13_copy)
                print("  + Copied Ex 13 APPLY to GE2 - U1.html Lesson 2")

    # tab-review:
    insert_after_card(s_u1, 'ex3-rev-card', CARDS_HTML['u1_rev_ex4'], 'ex4-rev-card')

    save_soup(s_u1, f_u1)

apply_unit1()
