import zipfile
import xml.etree.ElementTree as ET
import re

def extract_docx_elements(path):
    with zipfile.ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = tree.find('w:body', ns)
    
    elements = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            texts = [node.text for node in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            t = ''.join(texts).strip()
            if t:
                elements.append(('p', t))
        elif tag == 'tbl':
            rows = []
            for row in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr'):
                cells = []
                for cell in row.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc'):
                    cell_texts = [node.text for node in cell.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                    cells.append(' '.join(''.join(cell_texts).split()))
                rows.append(cells)
            elements.append(('tbl', rows))
    return elements

def analyze_unit(docx_path):
    print(f"==================================================")
    print(f"ANALYZING DOCX: {docx_path}")
    print(f"==================================================")
    elements = extract_docx_elements(docx_path)
    
    current_section = "START"
    for idx, (el_type, content) in enumerate(elements):
        if el_type == 'p':
            t = content
            # check section headers
            if re.match(r'^(LESSON\s+\d+|Review and Expand|UNIT\s+\d+\s+REVIEW|CONNECT THE GRAMMAR)', t, re.IGNORECASE):
                current_section = t
                print(f"\n--- SECTION: {current_section} ---")
            
            # check exercise headers
            # Pattern: e.g. "1 READ", "2 CHECK", "EXERCISE 3", "3 DISCOVER", "4 COMPLETE", "5 ASK & ANSWER"
            m = re.match(r'^(\d+)\s+([A-Z\s/&,–—\(\)]+)', t)
            if m and len(t) < 80:
                first_word = m.group(2).strip().split()[0] if m.group(2).strip() else ''
                if first_word in ['READ', 'CHECK', 'DISCOVER', 'COMPLETE', 'CHOOSE', 'WRITE', 'EDIT', 'LISTEN', 'TALK', 'PRACTICE', 'ASK', 'EXPAND', 'WORK', 'SPEAK', 'CORRECT', 'MATCH', 'FORM', 'FIND', 'REWRITE', 'TRUE', 'ANSWER']:
                    print(f"  [Ex {m.group(1)}] {t}")
            elif 'EXERCISE' in t.upper() and len(t) < 80:
                print(f"  [Exercise line] {t}")
            elif 'CD1-' in t:
                print(f"  [Audio] {t}")

print("UNIT 1:")
analyze_unit('word files/u1.docx')

print("\n\nUNIT 2:")
analyze_unit('word files/u2.docx')
