import sys
import io
import zipfile
import xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_blocks_range(docx_path, start_b, end_b):
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
            
    for i in range(max(0, start_b), min(len(blocks), end_b)):
        btype, content = blocks[i]
        if btype == 'p':
            print(f'[{i}] P: {content}')
        else:
            print(f'[{i}] TBL: {content}')

print("=== UNIT 2: L1 Blocks 75-100 (Ex 5, 6, 7) ===")
print_blocks_range('word files/u2.docx', 75, 100)

print("\n=== UNIT 2: L1 Blocks 125-145 (Ex 10, 11) ===")
print_blocks_range('word files/u2.docx', 125, 145)

print("\n=== UNIT 2: L2 Blocks 200-245 (Ex 4, 5, 6, 7, 8) ===")
print_blocks_range('word files/u2.docx', 200, 245)

print("\n=== UNIT 2: L2 Blocks 255-275 (Ex 10, 11) ===")
print_blocks_range('word files/u2.docx', 255, 275)

print("\n=== UNIT 2: L3 Blocks 335-375 (Ex 4, 5, 6, 7, 8) ===")
print_blocks_range('word files/u2.docx', 335, 375)

print("\n=== UNIT 2: L4 Blocks 430-500 (Ex 4, 5, 6, 7, 8) ===")
print_blocks_range('word files/u2.docx', 430, 500)

print("\n=== UNIT 2: Review Blocks 530-570 (Ex 1, 2, 3, 4, 5) ===")
print_blocks_range('word files/u2.docx', 530, 570)
