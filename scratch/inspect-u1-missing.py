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

print("=== UNIT 1: Blocks 75 - 110 (Around Ex 5, 6, 7) ===")
print_blocks_range('word files/u1.docx', 75, 110)

print("\n=== UNIT 1: Blocks 125 - 145 (Around Ex 9, 10, 11) ===")
print_blocks_range('word files/u1.docx', 125, 145)

print("\n=== UNIT 1: Blocks 155 - 185 (Around Ex 13, 14) ===")
print_blocks_range('word files/u1.docx', 155, 185)

print("\n=== UNIT 1: Blocks 240 - 260 (Around L2 Ex 6, 7, 8) ===")
print_blocks_range('word files/u1.docx', 240, 260)

print("\n=== UNIT 1: Blocks 305 - 325 (Around L2 Ex 12, 13) ===")
print_blocks_range('word files/u1.docx', 305, 325)

print("\n=== UNIT 1: Blocks 355 - 375 (Around Review Ex 3, 4) ===")
print_blocks_range('word files/u1.docx', 355, 375)
