# Grammar Explorer Development & Maintenance Guidelines

This document is the mandatory standard for all development, file creation, content extraction, and design maintenance across the **Grammar Explorer** repository.
**Always refer to and comply with these rules before performing any actions.**

---

## 1. Safety & Workflow Rules
1. **Always Perform a Backup First**: Before doing any refactoring, file splitting, or script-based batch modifications, create a backup branch (e.g. `git branch backup_before_<task>`).
2. **Never Edit Placeholder Pages**: Do not add content to pages marked as placeholders until explicitly requested.
3. **Git Author & Push Standard**:
   - Always commit with author: `--author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"`.
   - Automatically push changes to GitHub (`origin/main`).

---

## 2. Reading Word Files (`.docx`) & Content Parity
When reading source `.docx` files (e.g., `word files/u3.docx`):
1. **Inspect Both Paragraphs and Tables**:
   - `.docx` files are zip archives containing `word/document.xml`.
   - Text can be located in paragraphs (`<w:p>`) or inside table cells (`<w:tbl>/<w:tr>/<w:tc>`).
   - Never rely on simple string searching or regex slicing. Parse all XML nodes systematically.
2. **Scan for Every Single Exercise**:
   - Look for numbered headings: `1 READ`, `2 CHECK`, `3 DISCOVER`, `4 COMPLETE`, `5 ...`, `6 ...`, `7 ...`, etc.
   - Look for activity keywords: `EXPLORE`, `CHECK`, `DISCOVER`, `LEARN`, `PRACTICE`, `PRONUNCIATION`, `LISTEN`, `EDIT`, `APPLY`, `WRITING FOCUS`, `BEFORE YOU WRITE`, `WRITE`, `SELF ASSESS`.
   - Account for classroom speaking drills and note whether they should be included or adapted.
3. **Verify Audio Tracks**:
   - Search for all occurrences of `CD1-XX`, `CD2-XX`, `CD3-XX` in the `.docx`.
   - Cross-check against [audio-registry.json](file:///d:/Github%20Repos/Grammar-Explorer/audio-registry.json) to ensure every track is cataloged.

---

## 3. DOM Integrity & File Generation Rules
1. **NEVER Use String Slicing on HTML**:
   - Do NOT cut raw HTML between string markers (e.g. `find_card_start(...)` or regex substring matching).
   - String slicing chops parent containers (such as `<div class="grid grid-cols-1 lg:grid-cols-12...">`) in half, causing fatal unclosed-tag DOM collapse (white screen error).
2. **ALWAYS Use BeautifulSoup (DOM Parser)**:
   - Extract cards as complete Python BeautifulSoup `Tag` objects.
   - When wrapping individual cards:
     - For standalone single cards: wrap in `<div class="max-w-4xl mx-auto space-y-6">` and strip child `lg:col-span-*` classes.
     - For side-by-side card pairs: wrap in `<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">` with balanced columns (`lg:col-span-6`).
3. **Check Sub-tab Button-to-Pane Parity**:
   - Every `<button class="ex-tab-btn" data-extab="tab-X" onclick="switchExTab('tab-X')">` must have an exact matching `<div id="tab-X" class="ex-tab-pane [block|hidden] space-y-6">`.
   - Never leave an empty or truncated tab pane.

---

## 4. Design System & Aesthetics
1. **Light Background Standard**:
   - **Body Class**: `<body class="bg-slate-100/70 text-slate-800 font-sans min-h-screen flex flex-col antialiased selection:bg-teal-100 selection:text-teal-900">`
   - **NEVER** apply dark gradient backgrounds (`linear-gradient(135deg, #0b1329...)`) to the `body`. The workspace requires a clean, bright, light slate canvas.
2. **Reader Cards**:
   - White surface: `bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4`
   - Header badge: `w-7 h-7 rounded-lg bg-teal-500 text-white font-bold flex items-center justify-center text-xs shadow-sm`
   - Score badge: `ex-score text-xs font-bold text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-100`
3. **Typography**:
   - Google Fonts: Plus Jakarta Sans for interface, Playfair Display for readings / literary passages.

---

## 5. Audio System Architecture
1. **CD Badge Placement**:
   - Place `<span class="badge-cd">CDX-XX</span>` in the card header next to the title.
2. **Audio Registry (`audio-registry.json`)**:
   - Structure:
     ```json
     "CD1-16": {
       "trackId": "CD1-16",
       "title": "Sangomas of Southern Africa",
       "driveLink": "https://drive.google.com/open?id=...&usp=drive_fs",
       "directUrl": "https://docs.google.com/uc?export=open&id=...",
       "files": [
         "Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/GE2 - U3.html",
         "Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/grammar_explorer_2_unit_3_lesson_1.html"
       ],
       "hasPlayer": true
     }
     ```
3. **Synchronization**:
   - Run `node manage-audio.js --apply` after every page creation or track update.

---

## 6. Interactivity & Form Checking Standards
Each interactive card must include client-side instant validation:
1. **Fill-in Cloze**:
   - Inputs: `<input class="cloze-input input-clean..." data-ans="expected,alt1,alt2" />`
   - Check function: `checkClozeCard('card-id')`
2. **Dropdown Selects**:
   - Selects: `<select class="select-check input-clean..." data-ans="expected">`
   - Check function: `checkSelectCard('card-id')`
3. **True / False**:
   - Row: `<div class="tf-row..." data-correct="T">`
   - Buttons: `<button class="tf-btn..." onclick="selectTF(this, 'T')">T</button>`
   - Check function: `checkTFCard('card-id')`
4. **Multiple Choice (MCQ)**:
   - Items: `<div class="mcq-item..." data-correct="...">`
   - Inputs: `<input type="radio" name="..." value="..." />`
   - Check function: `checkMCQCard('card-id')`
5. **Editing / Error Correction**:
   - Use `.edit-pill` containers with `<input class="cloze-input input-clean" data-ans="..." />`
6. **Reset**:
   - Provide `resetCurrentLesson()` in top navigation to reset all inputs and remove badges.
