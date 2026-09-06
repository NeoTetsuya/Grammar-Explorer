import sys
import io
import zipfile
import xml.etree.ElementTree as ET
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_doc_blocks(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = tree.find('w:body', ns)
    
    blocks = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            t = ''.join([node.text for node in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]).strip()
            if t:
                blocks.append(('p', t))
        elif tag == 'tbl':
            rows = []
            for tr in child.findall('w:tr', ns):
                cells = []
                for tc in tr.findall('w:tc', ns):
                    c_text = ' '.join(''.join([node.text for node in tc.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]).split())
                    cells.append(c_text)
                rows.append(cells)
            blocks.append(('tbl', rows))
    return blocks

def parse_unit(docx_path, unit_name):
    print(f"\n==================================================================")
    print(f"COMPLETE AUDIT OF {unit_name}: {docx_path}")
    print(f"==================================================================")
    blocks = extract_doc_blocks(docx_path)
    
    current_sec = "INTRO"
    for i, (btype, content) in enumerate(blocks):
        if btype == 'p':
            t = content
            # check section
            if any(k in t.upper() for k in ['LESSON 1', 'LESSON 2', 'LESSON 3', 'LESSON 4', 'REVIEW THE GRAMMAR', 'CONNECT THE GRAMMAR']):
                if len(t) < 80:
                    current_sec = t
                    print(f"\n>>> SECTION: {current_sec}")
            
            # Check for exercise markers like:
            # "1 READ", "2 CHECK", "3 DISCOVER", "4 COMPLETE", "5 SPEAK", "6 WRITE", "PRACTICE", "EDIT", "APPLY", "LISTEN"
            # Or table containing exercise
            is_ex = False
            m = re.match(r'^(\d+)\s+([A-Z\s/&,–—\(\)\.\?]+)', t)
            if m and len(t) < 100:
                first_w = m.group(2).strip().split()[0] if m.group(2).strip() else ''
                if first_w in ['READ', 'CHECK', 'DISCOVER', 'COMPLETE', 'CHOOSE', 'WRITE', 'EDIT', 'LISTEN', 'TALK', 'PRACTICE', 'ASK', 'EXPAND', 'WORK', 'SPEAK', 'CORRECT', 'MATCH', 'FORM', 'FIND', 'REWRITE', 'TRUE', 'ANSWER', 'APPLY', 'LOOK', 'BEFORE', 'SELF']:
                    print(f"  [Block {i}] EXERCISE {m.group(1)}: {t}")
                    is_ex = True
            if not is_ex:
                if any(t.startswith(kw) for kw in ['READ the', 'CHECK.', 'DISCOVER.', 'EDIT.', 'PRACTICE', 'APPLY.', 'LISTEN,', 'WRITE &', 'SPEAK.', 'BEFORE YOU WRITE', 'SELF ASSESS']):
                    print(f"  [Block {i}] ACTIVITY: {t[:100]}")
                elif 'CD1-' in t:
                    print(f"  [Block {i}] AUDIO: {t}")

parse_unit('word files/u1.docx', 'UNIT 1')
parse_unit('word files/u2.docx', 'UNIT 2')
