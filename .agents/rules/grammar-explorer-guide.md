---
description: Mandatory rules for reading docx, grammar chart parity, generating lesson files, multi-file sync, DOM structure, design system, audio, and git push in Grammar-Explorer
globs: "**/*"
always_on: true
---

# Grammar Explorer Development & Maintenance Guidelines

Always strictly follow these rules when working in this repository:

1. **Perform Backups First**:
   - Create a local timestamped backup in `_backups/` for all target files (`*.backup_YYYYMMDD_HHMMSS`).
   - Create a dedicated Git backup branch before any refactoring or batch script execution (`git branch backup_before_<task>`).

2. **Reading `.docx` Files & Grammar Chart Parity**:
   - Systematically parse paragraphs (`<w:p>`) and tables (`<w:tbl>`) using `zipfile` and XML parsing.
   - **Grammar Chart Parity**: Ensure 100% fidelity to the textbook `.docx`:
     - Extract full regular and irregular spelling/form tables (e.g. *-s, -es, -ies, -ves*, vowel changes, irregular forms).
     - Include structured category lists (mass/fluids, abstract nouns, subjects of study, containers, units, portions, shapes).
     - Include all numbered rules with authentic example sentences.
     - Include all "Real English" callout boxes (`bg-amber-50/70 border border-amber-200 text-amber-950`).
     - Audit for missing charts (e.g., Chart 1.3, Chart 2.4, Chart 3.3, Chart 3.7) and insert them before companion exercises.
   - **Review & Writing**: Ensure Model Reading cards include both `GRAMMAR FOCUS (Page XX)` and `WRITING FOCUS (Page XX)`.
   - Scan for all CD audio mentions (`CD1-XX`, `CD2-XX`, `CD3-XX`) and verify against `audio-registry.json`.

3. **Multi-File Synchronization**:
   - For every unit, keep the master SPA file (`GE2 - UX.html`) in 100% sync with the standalone files:
     - `grammar_explorer_2_unit_X_lesson_1.html`
     - `grammar_explorer_2_unit_X_lesson_2.html`
     - `grammar_explorer_2_unit_X_lesson_3.html`
     - `grammar_explorer_2_unit_X_review_writing.html`
   - Any chart or exercise added/updated in the master file **must** also be updated in its standalone lesson file, and vice-versa.

4. **HTML Generation & DOM Integrity**:
   - **NEVER use string slicing or regex chopping** on HTML. It causes unclosed parent grids and fatal white-screen bugs.
   - **ALWAYS use BeautifulSoup** to parse, inspect, replace (`.replace_with()`), or insert DOM nodes cleanly.
   - Standalone cards: wrap in `<div class="max-w-4xl mx-auto space-y-6">`.
   - Card pairs: wrap in `<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">` with balanced columns (`lg:col-span-5` / `lg:col-span-7`).
   - Ensure every `<button data-extab="tab-X">` matches `<div id="tab-X" class="ex-tab-pane">`.

5. **Design Aesthetics & Typography**:
   - **Light Background Standard**: Always use `<body class="bg-slate-100/70 text-slate-800 font-sans min-h-screen flex flex-col antialiased selection:bg-teal-100 selection:text-teal-900">`.
   - Never add dark gradient backgrounds to `body`.
   - Cards: `bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4`.
   - Chart Tables: `border border-slate-200 rounded-xl overflow-hidden shadow-sm`, header `bg-slate-100 px-3 py-1.5 font-bold text-slate-700`.
   - Highlights: Teal (`text-teal-700`) and Amber (`text-amber-700`).

6. **Audio Pipeline & Multi-Directory Management**:
   - Add `<span class="badge-cd">CDX-XX</span>` to card headers.
   - Register tracks in `audio-registry.json`.
   - Run `node manage-audio.js --scan` to discover audio tracks across all curriculum directories (`Grammar Explorer 1`, `2`, `3`, and Book Edition).
   - Run `manage-audio.bat --check` or `node manage-audio.js --check` to audit uncommitted changes in core folders.
   - Run `node manage-audio.js --apply` to inject audio players, or `node manage-audio.js --apply --push` to push to GitHub.

7. **Git Version Control, Dynamic Indexing & Push**:
   - Never edit placeholder pages.
   - **Core Directories Inspection**: Always check uncommitted changes in `Grammar Explorer 1`, `Grammar Explorer 2`, and `Grammar Explorer 3` before pushing.
   - **Dynamic Indexing**: Run `update-and-push.bat` (or `node update-index.js --push`) to crawl all lessons on disk, sync `masterCatalog` in `index.html` (83 lessons total), and automatically commit and push.
   - Commit author: `--author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"`.
   - Always push changes to GitHub `origin/main`.
