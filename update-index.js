/**
 * Grammar Explorer - Automatic Index & Catalog Synchronizer
 * 
 * Automatically crawls curriculum directories:
 *   - Grammar Explorer 1/
 *   - Grammar Explorer 2/
 *   - Grammar Explorer 3/
 *   - Grammar-Explorer-book/ (Grammar-Explorer-2 Units 1-16 & sub-lessons)
 * 
 * Extracts titles, topics, and lesson tags from HTML files, generates the masterCatalog,
 * creates an automatic timestamped backup in _backups/, and updates index.html.
 * 
 * Usage:
 *   node update-index.js            # Updates index.html (creates backup first)
 *   node update-index.js --dry-run  # Previews changes without modifying files
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO_DIR = __dirname;
const INDEX_PATH = path.join(REPO_DIR, 'index.html');
const BACKUP_DIR = path.join(REPO_DIR, '_backups');

// CLI Arguments
const args = process.argv.slice(2);
const isDryRun = args.includes('--dry-run');
const isPush = args.includes('--push');
let customMessage = '';
const msgIndex = args.findIndex(a => a === '-m' || a === '--message');
if (msgIndex !== -1 && args[msgIndex + 1]) {
  customMessage = args[msgIndex + 1];
}

// Terminal colors
const cyan = (s) => `\x1b[36m${s}\x1b[0m`;
const green = (s) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s) => `\x1b[33m${s}\x1b[0m`;
const red = (s) => `\x1b[31m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;
const dim = (s) => `\x1b[2m${s}\x1b[0m`;

function log(msg) { console.log(msg); }

// Curated Unit Topics & Metadata Dictionary for Book Units
const BOOK_UNIT_METADATA = {
  1: {
    title: "Unit 1: Customs and Traditions (The Present)",
    topics: ["Customs & Traditions", "Simple Present", "Present Progressive", "Habits", "Authentic Reading", "Audio"],
    subLessons: {
      "grammar_explorer_2_unit_1_lesson_1.html": {
        title: "Unit 1 - Lesson 1: Simple Present",
        tag: "Book U1 L1",
        topics: ["Simple Present", "Habits", "Factual Information"]
      },
      "grammar_explorer_2_unit_1_lesson_2.html": {
        title: "Unit 1 - Lesson 2: Present Progressive & Simple Present",
        tag: "Book U1 L2",
        topics: ["Present Progressive", "Simple vs Progressive", "Temporary Situations"]
      },
      "grammar_explorer_2_unit_1_review_writing.html": {
        title: "Unit 1: Review the Grammar & Connect to Writing",
        tag: "Book U1 Writing",
        topics: ["Unit 1 Review", "Writing Connection", "Editing Practice"]
      }
    }
  },
  2: {
    title: "Unit 2: Survival (The Past)",
    topics: ["Survival", "Simple Past", "Past Progressive", "Used to", "When & While", "Audio Drills"],
    subLessons: {
      "grammar_explorer_2_unit_2_lesson_1.html": {
        title: "Unit 2 - Lesson 1: Simple Past",
        tag: "Book U2 L1",
        topics: ["Simple Past", "Regular/Irregular Verbs", "Survival Stories"]
      },
      "grammar_explorer_2_unit_2_lesson_2.html": {
        title: "Unit 2 - Lesson 2: Past Progressive and Simple Past",
        tag: "Book U2 L2",
        topics: ["Past Progressive", "Interrupted Past Actions", "Background Events"]
      },
      "grammar_explorer_2_unit_2_lesson_3.html": {
        title: "Unit 2 - Lesson 3: Past Time Clauses with When and While",
        tag: "Book U2 L3",
        topics: ["Time Clauses", "When vs While", "Simultaneous Actions"]
      },
      "grammar_explorer_2_unit_2_lesson_4.html": {
        title: "Unit 2 - Lesson 4: Repeated Past Actions: Used To and Would",
        tag: "Book U2 L4",
        topics: ["Used To", "Would", "Past Habits & States"]
      },
      "grammar_explorer_2_unit_2_review_writing.html": {
        title: "Unit 2: Review the Grammar & Connect to Writing",
        tag: "Book U2 Writing",
        topics: ["Unit 2 Review", "Writing Connection", "Narrative Paragraphs"]
      }
    }
  },
  3: {
    title: "Unit 3: Health and Fitness (Nouns)",
    topics: ["Health & Fitness", "Count/Non-count Nouns", "Quantifiers", "Definite/Indefinite Articles"]
  },
  4: {
    title: "Unit 4: Going Places (Pronouns, Prepositions, and Articles)",
    topics: ["Going Places", "Travel", "Object & Indefinite Pronouns", "Prepositions of Place & Movement"]
  },
  5: {
    title: "Unit 5: A Changing World (The Present Perfect)",
    topics: ["A Changing World", "Present Perfect", "For vs Since", "Unspecified Past"]
  },
  6: {
    title: "Unit 6: Appearances and Behavior (Adjectives and Adverbs)",
    topics: ["Appearances & Behavior", "Descriptive Adjectives", "Adjective Order", "Adverbs of Manner"]
  },
  7: {
    title: "Unit 7: Tomorrow and Beyond (The Future)",
    topics: ["Tomorrow and Beyond", "The Future", "Will & Be Going To", "Future Progressive"]
  },
  8: {
    title: "Unit 8: Consumer Society (Comparatives and Superlatives)",
    topics: ["Consumer Society", "Comparatives", "Superlatives", "As...As Comparisons", "Shopping & Economy"]
  },
  9: {
    title: "Unit 9: The Natural World (Conjunctions and Adverb Clauses)",
    topics: ["The Natural World", "Time & Reason Clauses", "Coordinating Conjunctions", "Subordinating Conjunctions"]
  }
};

/**
 * Creates backup file in _backups/ directory.
 */
function createBackup() {
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const timestamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
  const backupFile = path.join(BACKUP_DIR, `index.html.backup_${timestamp}`);
  fs.copyFileSync(INDEX_PATH, backupFile);
  log(`  ${green('✓')} Backup created: ${path.relative(REPO_DIR, backupFile)}`);
  return backupFile;
}

/**
 * Scan existing standard curriculum lessons from index.html to preserve custom mappings.
 */
function extractExistingStandardCatalog(html) {
  const match = html.match(/const\s+masterCatalog\s*=\s*\[([\s\S]*?)\];/);
  if (!match) return [];

  const rawCode = match[1];
  // Parse existing GE1, GE2, GE3 items
  const items = [];
  const itemRegex = /{\s*id:\s*["']([^"']+)["'],\s*level:\s*["']([^"']+)["'],\s*folder:\s*["']([^"']+)["'],\s*file:\s*["']([^"']+)["'],\s*title:\s*["']([^"']+)["'],\s*tag:\s*["']([^"']+)["'],\s*topics:\s*(\[[^\]]*\])\s*}/g;
  let m;
  while ((m = itemRegex.exec(rawCode)) !== null) {
    // Only collect standard GE1, GE2, GE3 (skip existing Book items to regenerate cleanly)
    if (!m[2].includes('Book')) {
      let topics = [];
      try {
        topics = JSON.parse(m[7].replace(/'/g, '"'));
      } catch (e) {
        topics = m[7].replace(/[\[\]"']/g, '').split(',').map(s => s.trim()).filter(Boolean);
      }
      items.push({
        id: m[1],
        level: m[2],
        folder: m[3],
        file: m[4],
        title: m[5],
        tag: m[6],
        topics: topics
      });
    }
  }
  return items;
}

/**
 * Build Full Book Edition Catalog Items
 */
function generateBookCatalog() {
  const bookItems = [];
  const ge2BookBase = 'Grammar-Explorer-book/Grammar-Explorer-2';
  const ge2BookDir = path.join(REPO_DIR, 'Grammar-Explorer-book', 'Grammar-Explorer-2');

  if (!fs.existsSync(ge2BookDir)) return bookItems;

  for (let u = 1; u <= 16; u++) {
    const unitFolder = `Unit ${u}`;
    const unitDir = path.join(ge2BookDir, unitFolder);
    if (!fs.existsSync(unitDir)) continue;

    const files = fs.readdirSync(unitDir).filter(f => f.endsWith('.html'));
    if (files.length === 0) continue;

    const meta = BOOK_UNIT_METADATA[u] || {
      title: `Unit ${u}: Interactive Textbook`,
      topics: [`Unit ${u}`, "Interactive Textbook", "Full Book Edition"]
    };

    // 1. Full unit main file: GE2 - UX.html
    const fullUnitFile = files.find(f => /^GE2\s*-\s*U\d+/i.test(f));
    if (fullUnitFile) {
      bookItems.push({
        id: `ge2_book_u${u}`,
        level: "GE2-Book",
        folder: `${ge2BookBase}/${unitFolder}`,
        file: `${ge2BookBase}/${unitFolder}/${fullUnitFile}`,
        title: `${meta.title} (Full Textbook Edition)`,
        tag: `Book Unit ${u}`,
        topics: meta.topics
      });
    }

    // 2. Sub-lessons (Lesson 1, Lesson 2, Review & Writing)
    const subLessonFiles = files.filter(f => !/^GE2\s*-\s*U\d+/i.test(f)).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
    for (const subFile of subLessonFiles) {
      let subMeta = (meta.subLessons && meta.subLessons[subFile]) ? meta.subLessons[subFile] : null;
      if (!subMeta) {
        // Auto-generate metadata if not in dictionary
        const cleanName = path.basename(subFile, '.html')
          .replace(/grammar_explorer_\d+_unit_\d+_/i, '')
          .replace(/[_-]+/g, ' ');
        subMeta = {
          title: `Unit ${u} - ${cleanName.charAt(0).toUpperCase() + cleanName.slice(1)}`,
          tag: `Book U${u}`,
          topics: [`Unit ${u}`, cleanName]
        };
      }

      const lessonId = subFile.replace(/grammar_explorer_2_unit_\d+_/i, '').replace(/[^a-zA-Z0-9]/g, '_');
      bookItems.push({
        id: `ge2_book_u${u}_${lessonId}`,
        level: "GE2-Book",
        folder: `${ge2BookBase}/${unitFolder}`,
        file: `${ge2BookBase}/${unitFolder}/${subFile}`,
        title: subMeta.title,
        tag: subMeta.tag,
        topics: subMeta.topics
      });
    }
  }

  return bookItems;
}

/**
 * Format catalog item to clean JavaScript object code
 */
function formatCatalogItem(item) {
  const topicsJson = JSON.stringify(item.topics);
  return `            { id: "${item.id}", level: "${item.level}", folder: "${item.folder}", file: "${item.file}", title: "${item.title.replace(/"/g, '\\"')}", tag: "${item.tag}", topics: ${topicsJson} },`;
}

/**
 * Main execution function
 */
function updateIndex() {
  log(`\n${bold(cyan('======================================================='))}`);
  log(`  ${bold('Grammar Explorer - Master Index & Catalog Synchronizer')}`);
  log(`  Mode: ${isDryRun ? yellow(bold('[DRY RUN - No files will be modified]')) : green(bold('[LIVE UPDATE]'))}`);
  log(`${bold(cyan('======================================================='))}
`);

  if (!fs.existsSync(INDEX_PATH)) {
    log(`${red('Error:')} index.html not found at ${INDEX_PATH}`);
    process.exit(1);
  }

  const indexHtml = fs.readFileSync(INDEX_PATH, 'utf8');

  // 1. Extract standard catalog
  const standardItems = extractExistingStandardCatalog(indexHtml);
  log(`  ${green('✓')} Found ${cyan(standardItems.length)} standard lessons in catalog (GE1, GE2, GE3).`);

  // 2. Generate Book catalog
  const bookItems = generateBookCatalog();
  log(`  ${green('✓')} Generated ${cyan(bookItems.length)} Full Book items (GE2 Units 1–9 & Sub-lessons).`);

  const ge1Items = standardItems.filter(i => i.level === 'GE1');
  const ge2Items = standardItems.filter(i => i.level === 'GE2');
  const ge3Items = standardItems.filter(i => i.level === 'GE3');

  const fullCatalogCode = [
    `        // Master Catalog across GE1, GE2, GE3, and Grammar-Explorer-book`,
    `        const masterCatalog = [`,
    `            // ==========================================`,
    `            // GE1 - Grammar Explorer 1 (${ge1Items.length} Lessons)`,
    `            // ==========================================`,
    ...ge1Items.map(formatCatalogItem),
    ``,
    `            // ==========================================`,
    `            // GE2 - Grammar Explorer 2 Standard (${ge2Items.length} Lessons)`,
    `            // ==========================================`,
    ...ge2Items.map(formatCatalogItem),
    ``,
    `            // ==========================================`,
    `            // GE3 - Grammar Explorer 3 (${ge3Items.length} Lessons)`,
    `            // ==========================================`,
    ...ge3Items.map(formatCatalogItem),
    ``,
    `            // ==========================================`,
    `            // GE2-Book - National Geographic Full Textbook Series (${bookItems.length} Interactive Lessons/Units)`,
    `            // ==========================================`,
    ...bookItems.map(formatCatalogItem),
    `        ];`
  ].join('\n');

  // 3. Replace in index.html
  const catalogRegex = /\/\/\s*Master Catalog[\s\S]*?const\s+masterCatalog\s*=\s*\[[\s\S]*?\];/;
  if (!catalogRegex.test(indexHtml)) {
    log(`${red('Error:')} Could not locate masterCatalog block in index.html`);
    process.exit(1);
  }

  const updatedHtml = indexHtml.replace(catalogRegex, fullCatalogCode);

  if (isDryRun) {
    log(`\n  ${yellow('DRY RUN Summary:')}`);
    log(`  - Standard GE1: ${ge1Items.length} lessons`);
    log(`  - Standard GE2: ${ge2Items.length} lessons`);
    log(`  - Standard GE3: ${ge3Items.length} lessons`);
    log(`  - Full Book GE2: ${bookItems.length} interactive units/lessons`);
    log(`  - Total Catalog Entries: ${bold(standardItems.length + bookItems.length)} items`);
    log(`\n${bold(cyan('======================================================='))}
`);
    return;
  }

  // Live execution: Create backup first
  createBackup();

  fs.writeFileSync(INDEX_PATH, updatedHtml, 'utf8');
  log(`  ${green('✓')} Successfully updated ${bold('index.html')} with ${bold(standardItems.length + bookItems.length)} catalog entries!`);

  // Git Push Automation
  if (isPush) {
    log(`\n${bold('📦 Committing & Pushing to GitHub...')}`);
    try {
      execSync('git add -A', { cwd: REPO_DIR, stdio: 'inherit' });
      const commitMsg = customMessage || `feat: integrate full book edition, add auto-sorter and update catalog (${standardItems.length + bookItems.length} items)`;
      try {
        execSync(`git commit -m "${commitMsg.replace(/"/g, '\\"')}"`, { cwd: REPO_DIR, stdio: 'inherit' });
        log(`  ${green('✓ Commit created:')} "${commitMsg}"`);
      } catch (commitErr) {
        log(yellow('  Note: No new changes to commit.'));
      }
      log(`  ${cyan('Pushing to GitHub (origin main)...')}`);
      execSync('git push -u origin main', { cwd: REPO_DIR, stdio: 'inherit' });
      log(`\n${green(bold('🎉 All changes successfully updated and pushed to GitHub!'))}`);
    } catch (gitErr) {
      console.error(red(`\nGit operation failed: ${gitErr.message}`));
      process.exit(1);
    }
  } else {
    log(`\n  ${yellow('Tip:')} Run with ${bold('--push')} to automatically commit and push to GitHub:`);
    log(`    ${cyan('node update-index.js --push')}`);
  }

  log(`\n${bold(cyan('======================================================='))}
`);
}

updateIndex();
