import sys
import io
import zipfile
import xml.etree.ElementTree as ET
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_all_text_blocks(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = tree.find('w:body', ns)
    
    blocks = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            t = ''.join([n.text for n in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if n.text]).strip()
            if t:
                blocks.append(('p', t))
        elif tag == 'tbl':
            rows = []
            for tr in child.findall('w:tr', ns):
                cells = []
                for tc in tr.findall('w:tc', ns):
                    c = ' '.join(''.join([n.text for n in tc.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if n.text]).split())
                    cells.append(c)
                rows.append(cells)
            blocks.append(('tbl', rows))
    return blocks

def audit_doc(docx_path, u_name):
    blocks = extract_all_text_blocks(docx_path)
    print(f"\n=======================================================")
    print(f"AUDIT FOR {u_name}")
    print(f"=======================================================")
    
    # We want to trace each lesson and find all exercises
    for i, (btype, content) in enumerate(blocks):
        if btype == 'p':
            t = content
            # detect keywords indicating start of an exercise
            is_start = False
            # Check for pattern e.g. "Complete each...", "Read the...", "Work with a partner...", "Rewrite...", "Circle the...", "EDIT.", "APPLY."
            prefixes = [
                'READ the', 'CHECK.', 'DISCOVER.', 'Complete each', 'Complete the',
                'Rewrite each', 'Circle the', 'EDIT.', 'SPEAK.', 'WRITE &', 'APPLY.',
                'LISTEN', 'BEFORE YOU WRITE', 'SELF ASSESS', 'Look at the photo', 'Work with a partner',
                'Choose the correct', 'In your notebook', 'Use the words to make'
            ]
            for pfx in prefixes:
                if t.startswith(pfx):
                    is_start = True
                    break
            if is_start and len(t) < 160:
                print(f"[{i:03d}] {t}")

print("--- UNIT 1 ---")
audit_doc('word files/u1.docx', 'UNIT 1')

print("\n--- UNIT 2 ---")
audit_doc('word files/u2.docx', 'UNIT 2')
