import sys
import io
import zipfile
import xml.etree.ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_exact_text(docx_path, search_terms):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    body = tree.find('w:body', ns)
    
    items = []
    for child in body:
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            t = ''.join([n.text for n in child.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if n.text]).strip()
            if t: items.append(('p', t))
        elif tag == 'tbl':
            rows = []
            for tr in child.findall('w:tr', ns):
                cells = [' '.join(''.join([n.text for n in tc.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if n.text]).split()) for tc in tr.findall('w:tc', ns)]
                rows.append(cells)
            items.append(('tbl', rows))
            
    print(f"=== SEARCH IN {docx_path} ===")
    for idx, term in enumerate(search_terms):
        print(f"\n--- TERM: {term} ---")
        for i, (btype, content) in enumerate(items):
            if term.lower() in str(content).lower():
                print(f"Found around block {i}:")
                for j in range(max(0, i-1), min(len(items), i+6)):
                    bt, c = items[j]
                    print(f"  [{j}] {bt}: {c[:140]}")
                break

search_u1 = [
    "take turns making affirmative or negative",
    "talk about weddings in your own culture",
    "celebrate their birthdays in your culture",
    "change from childhood to adulthood",
    "ask and answer the questions in numbers 1 and 2 in exercise 6",
    "write questions to ask a classmate about what he or she is doing this week",
    "does la tomatina sound like something"
]

search_u2 = [
    "take turns asking and answering the questions from exercise 5",
    "choose an animal from exercise 10",
    "make two of your sentences negative",
    "questions 4, 7, and 8 from exercise 6",
    "write six questions to ask a classmate about what he or she was doing",
    "past time clauses with when: events in sequence",
    "which action or event happened first",
    "when max’s car broke down",
    "when i woke up this morning",
    "used to: questions and answers",
    "did you use to ride",
    "complete each sentence. use would",
    "discuss the ways that life was different 100 years ago",
    "use the simple past, the past progressive, or used to",
    "have you ever been close to a wild animal"
]

extract_exact_text('word files/u1.docx', search_u1)
extract_exact_text('word files/u2.docx', search_u2)
