---
description: Mandatory rules for reading docx, generating lesson files, maintaining HTML structure, design system, and audio in Grammar-Explorer
globs: "**/*"
always_on: true
---

# Grammar Explorer Development Guidelines

Always strictly follow these rules when working in this repository:

1. **Perform Backup First**: Before any major changes or code generation, create a backup branch (`git branch backup_...`).
2. **Reading `.docx` Files**:
   - Parse both paragraphs (`<w:p>`) and tables (`<w:tbl>`) using `zipfile` and XML parsing.
   - Extract all exercise numbers (`1 READ`, `2 CHECK`, `3 DISCOVER`, `4 COMPLETE`, etc.) and activity labels.
   - Scan for all CD audio mentions (`CD1-XX`, `CD2-XX`, `CD3-XX`) and verify parity against `audio-registry.json`.
3. **HTML Generation & DOM Integrity**:
   - **NEVER use string slicing or regex chopping** on HTML.
   - **ALWAYS use BeautifulSoup** to parse and extract complete DOM nodes to prevent broken tags and white-screen bugs.
   - Wrap single cards in `<div class="max-w-4xl mx-auto space-y-6">` and pairs in `<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">`.
   - Ensure every `<button data-extab="tab-X">` matches `<div id="tab-X" class="ex-tab-pane">`.
4. **Design Aesthetics**:
   - **Light Background Standard**: Always use `<body class="bg-slate-100/70 text-slate-800 font-sans min-h-screen flex flex-col antialiased selection:bg-teal-100 selection:text-teal-900">`.
   - Never add dark gradient backgrounds to `body`.
   - Style cards with `bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-4`.
5. **Audio Pipeline**:
   - Add `<span class="badge-cd">CDX-XX</span>` to card headers.
   - Register tracks in `audio-registry.json`.
   - Run `node manage-audio.js --apply` after updating HTML files.
6. **Git Version Control**:
   - Never edit placeholder pages.
   - Commit author: `--author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"`.
   - Always push changes to GitHub `origin/main`.
