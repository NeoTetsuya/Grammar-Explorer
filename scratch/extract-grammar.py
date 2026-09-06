import sys
import io
import zipfile
import xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with zipfile.ZipFile('word files/u1.docx') as z:
    tree = ET.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
body = tree.find('w:body', ns)

blocks = []
for child in body:
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        t = ''.join([n.text for n in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if n.text]).strip()
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

print(f"Total blocks: {len(blocks)}")
with open('scratch/u1_docx_blocks.txt', 'w', encoding='utf-8') as f:
    for i, (btype, content) in enumerate(blocks):
        if btype == 'p':
            if content:
                f.write(f"[{i}] P: {content}\n")
        else:
            f.write(f"[{i}] TBL: {content}\n")

print("Wrote scratch/u1_docx_blocks.txt successfully.")
