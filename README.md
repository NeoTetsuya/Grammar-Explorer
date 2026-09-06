# 🧭 Grammar-Explorer — Complete English Grammar Curriculum & Full Book Edition

A structured English grammar mastery platform spanning from Foundation to Advanced. Features interactive visual explanation cards, progressive practice drills, real-world examples, syntax analysis, and the **National Geographic Learning Full Interactive Textbook Series**.

---

## 🌟 Curriculum & Edition Structure

- **Grammar Explorer 1 (Foundation / A2–B1)**: Sentence basics, core tenses (Present, Past, Future), basic modals, nouns, pronouns, and adjectives (26 interactive lessons).
- **Grammar Explorer 2 (Intermediate / B1–B2)**: Perfect tenses, passive voice, relative clauses, conditionals (Types 0, 1, 2), gerunds, infinitives, and reported speech (16 interactive lessons).
- **Grammar Explorer 3 (Advanced / B2–C1)**: Inversion, mixed conditionals, subjunctive mood, cleft sentences, advanced participle clauses, and complex discourse markers (15 interactive lessons).
- **Grammar Explorer Book Edition (National Geographic Learning)**: Complete digital interactive textbooks featuring authentic side-by-side reading passages, embedded CD audio pronunciation drills, and self-evaluating exercises (26 interactive units and sub-lessons).

---

## 📂 Repository Structure

```
Grammar-Explorer/
├── index.html                           # Master Hub & Curriculum Directory (83 Lessons)
├── auto-sort.js / auto-sort.bat         # Automated Sorter & Unit Organizer
├── update-index.js / update-index.bat   # Automated Index & Catalog Synchronizer
├── update-and-push.bat / .ps1          # One-Click Master Catalog Sync & GitHub Push
├── manage-audio.js / manage-audio.bat   # Audio Track Identifier, Git Inspector & Drive Integrator
├── audio-registry.json                  # Centralized Audio Track Registry (49 Tracks)
├── Grammar Explorer 1/                  # Level 1 Foundation Units (26 Lessons)
├── Grammar Explorer 2/                  # Level 2 Intermediate Units (16 Lessons)
├── Grammar Explorer 3/                  # Level 3 Advanced Units (15 Lessons)
├── Grammar-Explorer-book/               # National Geographic Learning Book Edition
│   ├── index.html                       # Master Book Portal
│   └── Grammar-Explorer-2/              # Level 2 Book Edition (Units 1–16)
│       ├── index.html                   # Level 2 Book Directory
│       ├── Unit 1/                      # Unit 1 Full Book & Sub-lessons
│       ├── ...
│       └── Unit 16/
└── README.md                            # Repository Documentation
```

---

## 🛠 Automation Scripts

### 1. Index & Push Pipeline (`update-index.js` & `update-and-push.bat` / `.ps1`)
- **Git Changes Inspection**: Actively inspects and reports uncommitted Git changes in **`Grammar Explorer 1`**, **`Grammar Explorer 2`**, **`Grammar Explorer 3`**, and **`Grammar-Explorer-book`** before updating.
- **Dynamic Filesystem Crawling**: Scans all HTML files on disk, preserving curated metadata while auto-extracting titles, tags, and topics for new lessons to ensure 100% disk-to-catalog parity (83 items total).
- **Automatic Backup**: Creates an automatic timestamped backup in `_backups/` before modifying `index.html`.
- **Author-Compliant Push**: Automatically stages all changes, creates a descriptive commit with the required author (`NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>`), and pushes to GitHub `origin/main`.
- **Commands**:
  - `update-and-push.bat` : Automatically synchronizes index and pushes all changes to GitHub.
  - `node update-index.js --dry-run` : Inspects Git changes and previews catalog without modifying files.
  - `node update-index.js` : Synchronizes `index.html` locally with automatic backup.
  - `node update-index.js --push` : Synchronizes `index.html` and pushes to GitHub.
  - `.\update-and-push.ps1 -Message "your commit message"` : PowerShell runner with custom commit message.

### 2. Audio Track Manager & Google Drive Integrator (`manage-audio.js` & `manage-audio.bat`)
- **Core Directory Git Status**: Inspects Git changes specifically across `Grammar Explorer 1`, `2`, `3`, and `Grammar-Explorer-book`.
- **Multi-Directory Audio Scanning**: Scans all 83 lesson files across all core folders for CD audio badges (`CD1-02`, `CD1-03`, etc.) and registers them in `audio-registry.json`.
- **Direct Stream Conversion**: Converts Google Drive sharing links to direct streaming URLs (`https://docs.google.com/uc?export=open&id=...`).
- **Player Injection & Removal**: Injects responsive HTML5 / Drive audio player widgets directly into lesson files with automatic file backups.
- **Continuous Link Entry**: Interactive menu with continuous prompt loop to quickly attach multiple audio links in sequence.
- **Author-Compliant Push**: Commits changes with the verified author identity and pushes to `origin/main`.
- **Commands**:
  - `manage-audio.bat` : Launches the interactive management menu.
  - `manage-audio.bat --check` or `node manage-audio.js --check` : Inspects Git changes in GE1, GE2, GE3, and Book.
  - `node manage-audio.js --scan` : Scans all 83 lessons across GE1, GE2, GE3, and Book for CD tracks.
  - `node manage-audio.js --list` : Displays all 49 tracks and their current attachment status.
  - `node manage-audio.js --add <TRACK_ID> "<DRIVE_URL>"` : Sets track URL and injects player into files.
  - `node manage-audio.js --remove <TRACK_ID>` : Safely removes player widgets and clears link.
  - `node manage-audio.js --apply` : Bulk injects all configured tracks from `audio-registry.json`.
  - `node manage-audio.js --apply --push` : Inspects changes, injects all players, and pushes to GitHub.

### 3. Standalone Auto Sorter (`auto-sort.js` & `auto-sort.bat`)
- Automatically sorts, standardizes, and organizes unit and sub-lesson files into proper directory structures using natural numerical ordering.
- Supports `--dry-run` to preview moves and renames safely.

---

## 🚀 Getting Started

1. **Direct Web Access (GitHub Pages)**:
   - Visit: `https://neotetsuya.github.io/Grammar-Explorer/`
2. **Local Usage**:
   - Open `index.html` in any modern web browser to access the interactive curriculum hub across all levels.
