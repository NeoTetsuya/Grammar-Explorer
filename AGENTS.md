# Grammar Explorer Development & Maintenance Guidelines

This document is the mandatory standard for all development, file creation, content extraction, grammar updating, and design maintenance across the **Grammar Explorer** repository.
**Always refer to and comply with these rules before performing any actions.**

---

## 1. Safety & Workflow Rules
1. **Always Perform Backups First**:
   - Create a local timestamped backup in `_backups/` for all files being touched (e.g. `filename.backup_YYYYMMDD_HHMMSS`).
   - Create a dedicated Git backup branch before any refactoring or batch script execution:
     ```bash
     git branch backup_before_<task_description>
     ```
2. **Never Edit Placeholder Pages**: Do not add content to pages marked as placeholders until explicitly requested.
3. **Automated Pre/Post Verification**:
   - Always run an automated verification script (using BeautifulSoup) before and after changes to verify:
     - 100% presence of expected charts, rules, and focus sections.
     - Exact count parity of interactive elements (`<input>`, `<select>`, `<button>`).
     - Zero unclosed tags, broken containers, or syntax errors.
4. **Git Author & Remote Push Standard**:
   - Always commit with author:
     ```bash
     git commit -m "<type>(<scope>): <description>" --author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"
     ```
   - Automatically push changes to GitHub (`origin/main`).
   - Use the automated synchronization scripts (`update-and-push.bat` or `node update-index.js --push`) to inspect core directory changes, update catalog entries, and push.

---

## 2. Reading Word Files (`.docx`) & Content Parity Standards

When auditing and extracting source content from textbook `.docx` files (e.g., `word files/u1.docx`, `u2.docx`, `u3.docx`, `u4.docx`):
1. **Systematic XML Parsing**:
   - `.docx` files are zip archives containing `word/document.xml`.
   - Text resides in paragraphs (`<w:p>`) and inside tables (`<w:tbl>/<w:tr>/<w:tc>`).
   - Never rely on simple string searching or regex slicing. Parse all XML nodes systematically.
2. **Grammar Charts Parity**:
   - Extract the complete theoretical content for each grammar chart (`CHART X.Y`):
     - **Full Form & Spelling Tables**: Regular endings (e.g., *-s, -es, -ies, -ves*), irregular categories (vowel changes, irregular endings, invariant forms), time expression tables, and possessive forms.
     - **Structured Categories**: Distinct groups (e.g., Mass/fluids, abstract nouns, subjects of study, measurement containers, units, portions, shapes).
     - **Numbered Rules**: Detailed explanations with all textbook example sentences (contrasting affirmative, negative, question, and edge cases).
     - **Real English Notes**: Conversational usage, spoken reductions, plural-only nouns, dual-meaning count/non-count distinctions, and pronoun substitutions.
     - **Textbook Page Badges**: Retain page reference badge in chart headers:
       ```html
       <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page XX</span>
       ```
3. **Audit for Missing Charts**:
   - Older HTML pages frequently omitted secondary or explanatory charts (e.g., Chart 1.3 *Spelling Rules for -ing*, Chart 2.4 *Time Expressions with Past Tense*, Chart 3.3 *Another and Other*, Chart 3.7 *Measurement Words*).
   - Check the `.docx` chart sequence against existing HTML and insert any missing charts in their designated textbook positions (typically directly before their companion exercise).
4. **Scan Every Exercise & Activity**:
   - Numbered headings: `1 READ`, `2 CHECK`, `3 DISCOVER`, `4 COMPLETE`, `5 ...`, etc.
   - Activity keywords: `EXPLORE`, `CHECK`, `DISCOVER`, `LEARN`, `PRACTICE`, `PRONUNCIATION`, `LISTEN`, `EDIT`, `APPLY`.
   - Ensure classroom speaking drills and pronunciation notes are integrated.
5. **Review & Writing Section**:
   - Model Reading passages must include:
     - `GRAMMAR FOCUS (Page XX)`: Highlighting the unit's grammar point in context.
     - `WRITING FOCUS (Page XX)`: Detailing sentence structure, coordination, punctuation, or agreement.

---

## 3. Multi-File Synchronization Architecture

Each unit in `Grammar-Explorer-book/Grammar-Explorer-2/Unit X/` follows a multi-file architecture:
1. **Master Unit File (`GE2 - UX.html`)**:
   - Single-page application containing all lessons, readings, exercises, and the review & writing section, managed via top-level tab buttons (`Lesson 1`, `Lesson 2`, `Lesson 3`, `Review & Writing`).
2. **Standalone Lesson Files**:
   - `grammar_explorer_2_unit_X_lesson_1.html`
   - `grammar_explorer_2_unit_X_lesson_2.html`
   - `grammar_explorer_2_unit_X_lesson_3.html`
3. **Standalone Review & Writing File**:
   - `grammar_explorer_2_unit_X_review_writing.html`

**Mandatory Rule**: Whenever any grammar chart, card, exercise, or audio widget is modified or added, **the change MUST be synchronized in BOTH the master unit file (`GE2 - UX.html`) AND the corresponding standalone file (`lesson_Y.html` or `review_writing.html`)**.

---

## 4. DOM Integrity & File Generation Rules

1. **NEVER Use String Slicing or Regex Chopping on HTML**:
   - Do NOT cut raw HTML between string markers or regex patterns.
   - String slicing truncates parent layout containers (e.g., `<div class="grid grid-cols-1 lg:grid-cols-12...">`), leading to fatal unclosed tags and white-screen DOM collapse.
2. **ALWAYS Use BeautifulSoup for DOM Operations**:
   - Parse using `BeautifulSoup(content, 'html.parser')`.
   - Replace or insert cards cleanly using `.replace_with()`, `.insert_before()`, or `.insert_after()`.
   - Write files out using clean UTF-8 encoding (`open(..., 'w', encoding='utf-8')`).
3. **Card Layout & Grid Standards**:
   - **Standalone / Full-width Cards**:
     ```html
     <div class="max-w-4xl mx-auto space-y-6">
       <!-- Card content -->
     </div>
     ```
   - **Side-by-Side Card Pairs (e.g. Chart + Practice Exercise)**:
     ```html
     <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
       <!-- Left: Chart (lg:col-span-5) -->
       <div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">...</div>
       <!-- Right: Exercise (lg:col-span-7) -->
       <div class="lg:col-span-7 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4">...</div>
     </div>
     ```
4. **Sub-tab Parity**:
   - Every `<button class="ex-tab-btn" data-extab="tab-X" onclick="switchExTab('tab-X')">` must have a matching `<div id="tab-X" class="ex-tab-pane ...">`.

---

## 5. Design System & Aesthetics Standards

1. **Light Background Canvas**:
   - **Body Class**:
     ```html
     <body class="bg-slate-100/70 text-slate-800 font-sans min-h-screen flex flex-col antialiased selection:bg-teal-100 selection:text-teal-900">
     ```
   - **NEVER** apply dark gradient backgrounds (`linear-gradient(135deg, #0b1329...)`) to the `body`. The workspace requires a clean, bright, light slate canvas.
2. **Reader Cards**:
   - White surface: `bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4`
   - Header badge: `w-7 h-7 rounded-lg bg-teal-500 text-white font-bold flex items-center justify-center text-xs shadow-sm`
   - Score badge: `ex-score text-xs font-bold text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-100`
3. **Grammar Chart Interior Styling**:
   - Tables: `border border-slate-200 rounded-xl overflow-hidden shadow-sm`
   - Table Header: `bg-slate-100 px-3 py-1.5 font-bold text-slate-700`
   - Table Rows: `divide-y divide-slate-100`, labels `bg-slate-50/50 w-2/5 font-medium text-slate-600`
   - Form Highlights: Teal (`<strong class="text-teal-700">`), Amber (`<strong class="text-amber-700">`)
   - Callout / Note Boxes: `bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5`
   - Real English Boxes: `bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1`
4. **Typography**:
   - Google Fonts: *Plus Jakarta Sans* for UI, labels, charts, and instructions; *Lora* or *Playfair Display* for reading passages and literary texts.

---

## 6. Audio System Architecture

1. **CD Badge Placement**:
   - Card headers: `<span class="badge-cd">CDX-XX</span>` next to the exercise title.
2. **Centralized Registry (`audio-registry.json`)**:
   - Every audio track referenced in curriculum files must be registered with its `trackId`, `title`, Google Drive link, direct streaming URL, and target files.
3. **Multi-Directory Scanning**:
   - `node manage-audio.js --scan` discovers CD badges across all curriculum directories:
     - `Grammar Explorer 1`
     - `Grammar Explorer 2`
     - `Grammar Explorer 3`
     - `Grammar-Explorer-book`
4. **Syncing & Injecting Audio**:
   - Run `node manage-audio.js --apply` to inject or update audio players in lesson files.
   - Run `node manage-audio.js --apply --push` to inspect Git status in core directories, inject audio players, and push to GitHub.
5. **Git Status Inspection**:
   - Run `manage-audio.bat --check` or `node manage-audio.js --check` to audit uncommitted files in `Grammar Explorer 1`, `2`, `3`, and Book Edition.

---

## 7. Interactivity & Form Checking Standards

Each practice card provides instant client-side evaluation:
1. **Fill-in Cloze**:
   - `<input class="cloze-input input-clean..." data-ans="expected,alt1,alt2" />`
   - Evaluation: `checkClozeCard('card-id')`
2. **Dropdown Selects**:
   - `<select class="select-check input-clean..." data-ans="expected">`
   - Evaluation: `checkSelectCard('card-id')`
3. **True / False**:
   - `<div class="tf-row..." data-correct="T">`
   - Buttons: `<button class="tf-btn..." onclick="selectTF(this, 'T')">T</button>`
   - Evaluation: `checkTFCard('card-id')`
4. **Multiple Choice (MCQ)**:
   - Items: `<div class="mcq-item..." data-correct="...">`
   - Inputs: `<input type="radio" name="..." value="..." />`
   - Evaluation: `checkMCQCard('card-id')`
5. **Editing / Error Correction**:
   - Sentence container with `.edit-pill` and embedded cloze input.
6. **Reset Controls**:
   - `resetCurrentLesson()` in top navigation cleans inputs, clears score badges, and restores default states.

---

## 8. Indexing, Master Catalog & Push Pipeline

1. **Core Directories Git Inspection**:
   - Both `update-index.js` and `manage-audio.js` actively inspect Git changes in:
     - `Grammar Explorer 1`
     - `Grammar Explorer 2`
     - `Grammar Explorer 3`
     - `Grammar-Explorer-book`
   - Statuses (`[MODIFIED]`, `[ADDED]`, `[DELETED]`, `[RENAMED]`, `[UNTRACKED]`, or `Clean`) are displayed before executing operations.
2. **Dynamic Filesystem Crawling**:
   - `update-index.js` dynamically crawls all lesson files on disk in `Grammar Explorer 1`, `2`, and `3`, ensuring 100% disk-to-catalog parity (currently 83 lessons across the hub).
   - Preserves curated titles, tags, and topics while automatically parsing new/unmapped files.
3. **One-Click Push Automation**:
   - Use `update-and-push.bat` (or `node update-index.js --push`) to:
     1. Inspect Git status in core directories.
     2. Scan the filesystem and update `masterCatalog` in `index.html`.
     3. Create an automatic backup in `_backups/`.
     4. Stage all files (`git add -A`).
     5. Commit using author `NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>`.
     6. Push to `origin/main`.
