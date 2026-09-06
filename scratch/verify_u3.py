import os
from bs4 import BeautifulSoup

UNIT3_DIR = r"d:\Github Repos\Grammar-Explorer\Grammar-Explorer-book\Grammar-Explorer-2\Unit 3"
files = [
    "GE2 - U3.html",
    "grammar_explorer_2_unit_3_lesson_1.html",
    "grammar_explorer_2_unit_3_lesson_2.html",
    "grammar_explorer_2_unit_3_lesson_3.html",
    "grammar_explorer_2_unit_3_review_writing.html"
]

print("Verifying Unit 3 HTML files...")

for fname in files:
    fpath = os.path.join(UNIT3_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    
    print(f"\n--- Checking {fname} (Size: {len(content):,} bytes) ---")
    
    # Check charts
    checks = {
        "Chart 3.1": "3.1 Spelling Rules for Plural Nouns" in text,
        "Chart 3.2": "3.2 Possessive Nouns" in text,
        "Chart 3.3": "3.3 Another and Other" in text,
        "Chart 3.4": "3.4 Count and Non-Count Nouns" in text,
        "Chart 3.5": "3.5 Categories of Non-Count Nouns" in text,
        "Chart 3.6": "3.6 Some, Any, A Few, Many, A Little, Much, A Lot Of" in text,
        "Chart 3.7": "3.7 Measurement Words with Non-Count Nouns" in text,
        "Grammar Focus": "GRAMMAR FOCUS" in text,
        "Writing Focus": "WRITING FOCUS: Subject-Verb Agreement" in text,
    }
    
    if fname == "GE2 - U3.html":
        expected = checks.keys()
    elif fname == "grammar_explorer_2_unit_3_lesson_1.html":
        expected = ["Chart 3.1", "Chart 3.2", "Chart 3.3"]
    elif fname == "grammar_explorer_2_unit_3_lesson_2.html":
        expected = ["Chart 3.4", "Chart 3.5"]
    elif fname == "grammar_explorer_2_unit_3_lesson_3.html":
        expected = ["Chart 3.6", "Chart 3.7"]
    elif fname == "grammar_explorer_2_unit_3_review_writing.html":
        expected = ["Grammar Focus", "Writing Focus"]
        
    all_ok = True
    for exp in expected:
        if checks[exp]:
            print(f"  ✓ Found {exp}")
        else:
            print(f"  ✗ MISSING {exp}!")
            all_ok = False
            
    # Check form elements count
    inputs = len(soup.find_all("input"))
    selects = len(soup.find_all("select"))
    buttons = len(soup.find_all("button"))
    print(f"  Interactive elements: inputs={inputs}, selects={selects}, buttons={buttons}")
    
    if not all_ok:
        print(f"  [ERROR] Verification failed for {fname}!")
    else:
        print(f"  [OK] All expected grammar sections confirmed in {fname}!")

print("\nAll verifications complete!")
