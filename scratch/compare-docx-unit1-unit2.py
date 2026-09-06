import sys
import io
import zipfile
import xml.etree.ElementTree as ET
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_paragraphs_and_runs(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = tree.find('w:body', ns)
    
    items = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            p_text = []
            runs = []
            for r in child.findall('w:r', ns):
                t_node = r.find('w:t', ns)
                if t_node is not None and t_node.text:
                    txt = t_node.text
                    b_node = r.find('.//w:b', ns)
                    is_bold = (b_node is not None)
                    runs.append((txt, is_bold))
                    p_text.append(txt)
            full_text = ''.join(p_text).strip()
            if full_text:
                items.append({'type': 'p', 'text': full_text, 'runs': runs})
        elif tag == 'tbl':
            rows = []
            for tr in child.findall('w:tr', ns):
                row = []
                for tc in tr.findall('w:tc', ns):
                    cell_text = []
                    for t in tc.findall('.//w:t', ns):
                        if t.text:
                            cell_text.append(t.text)
                    row.append(' '.join(''.join(cell_text).split()))
                rows.append(row)
            items.append({'type': 'tbl', 'rows': rows})
    return items

def analyze_docx_exercises(docx_path):
    items = extract_paragraphs_and_runs(docx_path)
    print(f"\n=======================================================")
    print(f"ANALYZING: {docx_path}")
    print(f"=======================================================")
    
    lesson = "INTRO"
    for i, it in enumerate(items):
        if it['type'] == 'p':
            t = it['text']
            if 'LESSON 1' in t:
                lesson = "LESSON 1"
                print(f"\n--- {lesson} ---")
            elif 'LESSON 2' in t:
                lesson = "LESSON 2"
                print(f"\n--- {lesson} ---")
            elif 'LESSON 3' in t:
                lesson = "LESSON 3"
                print(f"\n--- {lesson} ---")
            elif 'LESSON 4' in t:
                lesson = "LESSON 4"
                print(f"\n--- {lesson} ---")
            elif 'REVIEW' in t.upper() and 'GRAMMAR' in t.upper():
                lesson = "REVIEW & EXPAND"
                print(f"\n--- {lesson} ---")
            elif 'CONNECT THE GRAMMAR' in t.upper():
                lesson = "WRITING"
                print(f"\n--- {lesson} ---")

            # Detect exercise numbers and titles
            # Often numbered: e.g. "1 READ", "2 CHECK", "3 DISCOVER", "4 COMPLETE", "5 ASK & ANSWER"
            # Or bold runs starting with number
            first_run = it['runs'][0] if it['runs'] else ('', False)
            match_num = re.match(r'^(\d+)\s+([A-Z\s/&,–—\(\)]+)', t)
            
            # Check if line looks like an exercise title or CD track
            if 'CD1-' in t:
                print(f"  [AUDIO] {t}")
            elif match_num:
                num = match_num.group(1)
                heading = match_num.group(2).strip()
                words = heading.split()
                if words and words[0] in ['READ', 'CHECK', 'DISCOVER', 'COMPLETE', 'CHOOSE', 'WRITE', 'EDIT', 'LISTEN', 'TALK', 'PRACTICE', 'ASK', 'EXPAND', 'WORK', 'SPEAK', 'CORRECT', 'MATCH', 'FORM', 'FIND', 'REWRITE', 'TRUE', 'ANSWER', 'APPLY', 'MAKE', 'LOOK']:
                    print(f"  [EXERCISE {num}] {t[:120]}")
            elif t.startswith('EXERCISE') or t.startswith('Exercise'):
                print(f"  [EXERCISE-ALT] {t[:120]}")
            elif any(t.startswith(kw) for kw in ['READ the', 'CHECK.', 'DISCOVER.', 'EDIT.', 'PRACTICE', 'APPLY', 'LISTEN,', 'WRITE']):
                if len(t) < 120:
                    print(f"  [EXERCISE-KW] {t}")

analyze_docx_exercises('word files/u1.docx')
analyze_docx_exercises('word files/u2.docx')
