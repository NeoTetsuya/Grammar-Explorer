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
        # maybe multiple tags or outer tag
        new_tag = BeautifulSoup(new_card_html, 'html.parser')
    target.insert_after(new_tag)
    print(f"  + Inserted {new_id or 'new card'} after #{target_id}")
    return True

def apply_unit2():
    print("\n=======================================================")
    print("UPDATING UNIT 2 FILES")
    print("=======================================================")
    
    # 1. Update standalone grammar_explorer_2_unit_2_lesson_1.html
    f_l1 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_1.html'
    s_l1 = load_soup(f_l1)
    insert_after_card(s_l1, 'ex5-l1-card', CARDS_HTML['u2_l1_ex6'], 'ex6-l1-card')
    save_soup(s_l1, f_l1)
    
    # 2. Update standalone grammar_explorer_2_unit_2_lesson_2.html
    f_l2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_2.html'
    s_l2 = load_soup(f_l2)
    insert_after_card(s_l2, 'ex6-l2-card', CARDS_HTML['u2_l2_ex7'], 'ex7-l2-card')
    save_soup(s_l2, f_l2)
    
    # 3. Update standalone grammar_explorer_2_unit_2_lesson_3.html
    f_l3 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_3.html'
    s_l3 = load_soup(f_l3)
    insert_after_card(s_l3, 'ex6-l3-card', CARDS_HTML['u2_l3_ex7'], 'ex7-l3-card')
    save_soup(s_l3, f_l3)
    
    # 4. Update standalone grammar_explorer_2_unit_2_review_writing.html
    f_rw = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_review_writing.html'
    s_rw = load_soup(f_rw)
    insert_after_card(s_rw, 'ex1-rev-card', CARDS_HTML['u2_rev_ex2'], 'ex2-rev-card')
    insert_after_card(s_rw, 'ex4-rev-card', CARDS_HTML['u2_rev_ex5'], 'ex5-rev-card')
    save_soup(s_rw, f_rw)
    
    # 5. Now update GE2 - U2.html (All-in-one)
    f_u2 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/GE2 - U2.html'
    s_u2 = load_soup(f_u2)
    
    # tab-lesson1:
    insert_after_card(s_u2, 'ex5-l1-card', CARDS_HTML['u2_l1_ex6'], 'ex6-l1-card')
    # Add Ex 11 from s_l1
    if not s_u2.find(id='ex11-l1-card') and not any('APPLY (Page 32)' in c.get_text() for c in s_u2.select('.reader-card')):
        card11 = None
        for c in s_l1.select('.reader-card'):
            if '11' in c.get_text() and 'APPLY' in c.get_text():
                card11 = c
                break
        if card11:
            target10 = s_u2.find(id='ex10-l1-card')
            if target10:
                card11_copy = BeautifulSoup(str(card11), 'html.parser').find(class_='reader-card')
                target10.insert_after(card11_copy)
                print("  + Copied Ex 11 APPLY to GE2 - U2.html Lesson 1")

    # tab-lesson2:
    # Add Ex 5 from s_l2
    if not any('Time Anchors (Page 36)' in c.get_text() for c in s_u2.select('.reader-card')):
        card5_l2 = None
        for c in s_l2.select('.reader-card'):
            if '5' in c.get_text() and 'Time Anchors' in c.get_text():
                card5_l2 = c
                break
        if card5_l2:
            target4_l2 = s_u2.find(id='ex4-l2-card')
            if target4_l2:
                c5_copy = BeautifulSoup(str(card5_l2), 'html.parser').find(class_='reader-card')
                target4_l2.insert_after(c5_copy)
                print("  + Copied Ex 5 WRITE & SPEAK to GE2 - U2.html Lesson 2")
    
    insert_after_card(s_u2, 'ex6-l2-card', CARDS_HTML['u2_l2_ex7'], 'ex7-l2-card')
    
    # Add Ex 11 from s_l2
    if not any('APPLY (Page 38)' in c.get_text() for c in s_u2.select('.reader-card')):
        card11_l2 = None
        for c in s_l2.select('.reader-card'):
            if '11' in c.get_text() and 'APPLY' in c.get_text():
                card11_l2 = c
                break
        if card11_l2:
            target10_l2 = s_u2.find(id='ex10-l2-card')
            if target10_l2:
                c11_copy = BeautifulSoup(str(card11_l2), 'html.parser').find(class_='reader-card')
                target10_l2.insert_after(c11_copy)
                print("  + Copied Ex 11 APPLY to GE2 - U2.html Lesson 2")

    # tab-lesson3:
    # Need Chart 2.6, Ex 5, Ex 6, Ex 7, Ex 10, Ex 11
    target4_l3 = s_u2.find(id='ex4-l3-card')
    if target4_l3 and not s_u2.find(id='ex5-l3-card'):
        # Copy Chart 2.6 and Ex 5 & Ex 6 from s_l3
        chart2_6 = None
        for c in s_l3.select('.reader-card'):
            if '2.6' in c.get_text() and 'Events in Sequence' in c.get_text():
                chart2_6 = c
                break
        ex5_tag = s_l3.find(id='ex5-l3-card')
        ex6_tag = s_l3.find(id='ex6-l3-card')
        
        curr = target4_l3
        if chart2_6:
            c26_copy = BeautifulSoup(str(chart2_6), 'html.parser').find(class_='reader-card')
            curr.insert_after(c26_copy)
            curr = c26_copy
            print("  + Inserted Chart 2.6 into GE2 - U2.html Lesson 3")
        if ex5_tag:
            ex5_copy = BeautifulSoup(str(ex5_tag), 'html.parser').find(id='ex5-l3-card')
            curr.insert_after(ex5_copy)
            curr = ex5_copy
            print("  + Inserted Ex 5 into GE2 - U2.html Lesson 3")
        if ex6_tag:
            ex6_copy = BeautifulSoup(str(ex6_tag), 'html.parser').find(id='ex6-l3-card')
            curr.insert_after(ex6_copy)
            curr = ex6_copy
            print("  + Inserted Ex 6 into GE2 - U2.html Lesson 3")
        
        # Now insert Ex 7
        ex7_tag = BeautifulSoup(CARDS_HTML['u2_l3_ex7'], 'html.parser').find(id='ex7-l3-card')
        curr.insert_after(ex7_tag)
        print("  + Inserted Ex 7 into GE2 - U2.html Lesson 3")
    
    # Also add Ex 10 & 11 in Lesson 3
    target9_l3 = s_u2.find(id='ex9-l3-card')
    if target9_l3 and not any('Marta’s Blog' in c.get_text() or "Marta's Blog" in c.get_text() for c in s_u2.select('.reader-card')):
        c10_l3 = None
        c11_l3 = None
        for c in s_l3.select('.reader-card'):
            if 'Marta' in c.get_text() and 'Blog' in c.get_text():
                c10_l3 = c
            elif '11' in c.get_text() and 'Accident Story' in c.get_text():
                c11_l3 = c
        curr = target9_l3
        if c10_l3:
            c10_copy = BeautifulSoup(str(c10_l3), 'html.parser').find(class_='reader-card')
            curr.insert_after(c10_copy)
            curr = c10_copy
            print("  + Inserted Marta's Blog (Ex 10) into GE2 - U2.html Lesson 3")
        if c11_l3:
            c11_copy = BeautifulSoup(str(c11_l3), 'html.parser').find(class_='reader-card')
            curr.insert_after(c11_copy)
            print("  + Inserted Accident Story (Ex 11 APPLY) into GE2 - U2.html Lesson 3")

    # tab-lesson4:
    # Need Chart 2.8, Ex 5, Ex 6, Ex 7, Ex 9, Ex 10
    f_l4 = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 2/grammar_explorer_2_unit_2_lesson_4.html'
    s_l4 = load_soup(f_l4)
    target4_l4 = s_u2.find(id='ex4-l4-card')
    if target4_l4 and not s_u2.find(id='ex5-l4-card'):
        chart2_8 = None
        for c in s_l4.select('.reader-card'):
            if '2.8' in c.get_text() and 'Used To: Questions' in c.get_text():
                chart2_8 = c
                break
        ex5_l4 = s_l4.find(id='ex5-l4-card')
        ex6_l4 = None
        for c in s_l4.select('.reader-card'):
            if '6' in c.get_text() and 'Childhood Habits' in c.get_text():
                ex6_l4 = c
                break
        curr = target4_l4
        if chart2_8:
            c28_copy = BeautifulSoup(str(chart2_8), 'html.parser').find(class_='reader-card')
            curr.insert_after(c28_copy)
            curr = c28_copy
            print("  + Inserted Chart 2.8 into GE2 - U2.html Lesson 4")
        if ex5_l4:
            ex5_copy = BeautifulSoup(str(ex5_l4), 'html.parser').find(id='ex5-l4-card')
            curr.insert_after(ex5_copy)
            curr = ex5_copy
            print("  + Inserted Ex 5 into GE2 - U2.html Lesson 4")
        if ex6_l4:
            ex6_copy = BeautifulSoup(str(ex6_l4), 'html.parser').find(class_='reader-card')
            curr.insert_after(ex6_copy)
            print("  + Inserted Ex 6 into GE2 - U2.html Lesson 4")

    # In Lesson 4, also insert Ex 7 after Chart 2.9 (if not present)
    if not s_u2.find(id='ex7-l4-card'):
        chart2_9 = None
        for c in s_u2.select('#tab-lesson4 .reader-card'):
            if '2.9' in c.get_text() and 'Would' in c.get_text():
                chart2_9 = c
                break
        ex7_l4 = s_l4.find(id='ex7-l4-card')
        if chart2_9 and ex7_l4:
            ex7_copy = BeautifulSoup(str(ex7_l4), 'html.parser').find(id='ex7-l4-card')
            chart2_9.insert_after(ex7_copy)
            print("  + Inserted Ex 7 into GE2 - U2.html Lesson 4")

    # In Lesson 4, also insert Ex 9 & 10 after Ex 8
    target8_l4 = s_u2.find(id='ex8-l4-card')
    if target8_l4 and not any('5,000 Years Ago vs. People Today' in c.get_text() for c in s_u2.select('.reader-card')):
        c9_l4 = None
        c10_l4 = None
        for c in s_l4.select('.reader-card'):
            if '9' in c.get_text() and '5,000 Years Ago' in c.get_text():
                c9_l4 = c
            elif '10' in c.get_text() and 'Personal Life Changes' in c.get_text():
                c10_l4 = c
        curr = target8_l4
        if c9_l4:
            c9_copy = BeautifulSoup(str(c9_l4), 'html.parser').find(class_='reader-card')
            curr.insert_after(c9_copy)
            curr = c9_copy
            print("  + Inserted Ex 9 into GE2 - U2.html Lesson 4")
        if c10_l4:
            c10_copy = BeautifulSoup(str(c10_l4), 'html.parser').find(class_='reader-card')
            curr.insert_after(c10_copy)
            print("  + Inserted Ex 10 APPLY into GE2 - U2.html Lesson 4")

    # tab-review:
    insert_after_card(s_u2, 'ex1-rev-card', CARDS_HTML['u2_rev_ex2'], 'ex2-rev-card')
    insert_after_card(s_u2, 'ex4-rev-card', CARDS_HTML['u2_rev_ex5'], 'ex5-rev-card')

    save_soup(s_u2, f_u2)

apply_unit2()
