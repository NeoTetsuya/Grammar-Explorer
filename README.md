# 🧭 Grammar-Explorer — Complete English Grammar Curriculum & Full Book Edition

A structured English grammar mastery platform spanning from Foundation to Advanced. Features interactive visual explanation cards, progressive practice drills, real-world examples, syntax analysis, and the **National Geographic Learning Full Interactive Textbook Series**.

---

## 🌟 Curriculum & Edition Structure

- **Grammar Explorer 1 (Foundation / A2–B1)**: Sentence basics, core tenses (Present, Past, Future), basic modals, nouns, pronouns, and adjectives.
- **Grammar Explorer 2 (Intermediate / B1–B2)**: Perfect tenses, passive voice, relative clauses, conditionals (Types 0, 1, 2), gerunds, infinitives, and reported speech.
- **Grammar Explorer 3 (Advanced / B2–C1)**: Inversion, mixed conditionals, subjunctive mood, cleft sentences, advanced participle clauses, and complex discourse markers.
- **Grammar Explorer Book Edition (National Geographic Learning)**: Complete digital interactive textbooks featuring authentic side-by-side reading passages, embedded CD audio pronunciation drills, and self-evaluating exercises.

---

## 📂 Repository Structure

```
Grammar-Explorer/
├── index.html                      # Master Hub & Curriculum Directory
├── auto-sort.js / auto-sort.bat    # Automated Sorter & Unit Organizer
├── update-index.js / update-index.bat # Automated Index & Catalog Synchronizer
├── Grammar Explorer 1/             # Level 1 Foundation Units
├── Grammar Explorer 2/             # Level 2 Intermediate Units
├── Grammar Explorer 3/             # Level 3 Advanced Units
├── Grammar-Explorer-book/          # National Geographic Learning Book Edition
│   ├── index.html                  # Master Book Portal
│   └── Grammar-Explorer-2/         # Level 2 Book Edition (Units 1–16)
│       ├── index.html              # Level 2 Book Directory
│       ├── Unit 1/                 # Unit 1 Full Book & Sub-lessons
│       ├── ...
│       └── Unit 16/
└── README.md                       # Repository Documentation
```

---

## 🛠 Automation Scripts

- **Auto Sorter**:
  - `auto-sort.bat` or `node auto-sort.js`
  - Automatically sorts, standardizes, and organizes unit and sub-lesson files into proper directory structures using natural numerical ordering.
  - Supports `--dry-run` to preview changes safely.

- **Index & Catalog Synchronizer**:
  - `update-index.bat` or `node update-index.js`
  - Crawls all curriculum directories, extracts lesson titles, tags, and topics, creates an automated pre-execution backup in `_backups/`, and synchronizes the searchable `masterCatalog` in `index.html`.
  - Supports `--dry-run` to preview catalog items.

---

## 🚀 Getting Started

1. **Direct Web Access (GitHub Pages)**:
   - Visit: `https://neotetsuya.github.io/Grammar-Explorer/`
2. **Local Usage**:
   - Open `index.html` in any web browser to select your desired grammar level or explore the Full Book Edition.
