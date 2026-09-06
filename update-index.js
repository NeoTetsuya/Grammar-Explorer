/**
 * Grammar Explorer - Automatic Index & Catalog Synchronizer
 * 
 * Automatically crawls curriculum directories:
 *   - Grammar Explorer 1/
 *   - Grammar Explorer 2/
 *   - Grammar Explorer 3/
 *   - Grammar-Explorer-book/ (Grammar-Explorer-2 Units 1-16 & sub-lessons)
 * 
 * Inspects Git status and detects changes in Grammar Explorer 1, 2, and 3.
 * Dynamically scans the filesystem for all lesson files, extracts titles,
 * topics, and tags, generates the masterCatalog, creates an automatic
 * timestamped backup in _backups/, and updates index.html.
 * 
 * Usage:
 *   node update-index.js            # Updates index.html (creates backup first)
 *   node update-index.js --dry-run  # Previews changes and git status without modifying files
 *   node update-index.js --push     # Stages, commits, and pushes all changes to GitHub
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO_DIR = __dirname;
const INDEX_PATH = path.join(REPO_DIR, 'index.html');
const BACKUP_DIR = path.join(REPO_DIR, '_backups');

const CORE_DIRECTORIES = [
  'Grammar Explorer 1',
  'Grammar Explorer 2',
  'Grammar Explorer 3'
];

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
const magenta = (s) => `\x1b[35m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;
const dim = (s) => `\x1b[2m${s}\x1b[0m`;

function log(msg) { console.log(msg); }

// Curated Topics & Metadata Dictionary for Standard Lessons
const STANDARD_CURATED_METADATA = {
  // Grammar Explorer 1 additional/alternate files
  "Grammar Explorer 1/unit12_comparatives_superlatives.html": {
    title: "Unit 12: Comparatives, Superlatives & Possessives",
    tag: "Unit 12",
    topics: ["Comparatives", "Superlatives", "Possessives", "-er / more"]
  },
  "Grammar Explorer 1/units_11_13_modals_and_conjunctions.html": {
    title: "Units 11 & 13: Modals & Conjunctions",
    tag: "Units 11 & 13",
    topics: ["Modals", "Conjunctions", "Can / Should", "Connecting Clauses"]
  },
  "Grammar Explorer 1/units_3_4_simple_present_daily_life.html": {
    title: "Units 3 & 4: Simple Present & Daily Life",
    tag: "Units 3 & 4",
    topics: ["Simple Present", "Daily Routines", "Frequency Adverbs"]
  },
  "Grammar Explorer 1/units_8_9_the_past.html": {
    title: "Units 8 & 9: The Past (Parts 1 & 2)",
    tag: "Units 8 & 9",
    topics: ["Was / Were", "Simple Past", "Irregular Verbs"]
  },
  "Grammar Explorer 1/unit_11_action_vs_non_action_verbs.html": {
    title: "Unit 11: Action vs Non-Action Verbs",
    tag: "Unit 11",
    topics: ["Stative Verbs", "Dynamic Verbs", "Action vs Non-Action"]
  },
  "Grammar Explorer 1/unit_12_simple_present_vs_present_progressive.html": {
    title: "Unit 12: Simple Present vs. Present Progressive",
    tag: "Unit 12",
    topics: ["Simple vs Progressive", "Habits vs Now", "Signal Words"]
  },
  "Grammar Explorer 1/unit_13_simple_past_past_progressive.html": {
    title: "Unit 13: Simple Past & Past Progressive",
    tag: "Unit 13",
    topics: ["When & While", "Interrupted Past Actions", "Simultaneous Actions"]
  },
  "Grammar Explorer 1/unit_14_count_and_non_count_nouns.html": {
    title: "Unit 14: Count and Non-Count Nouns",
    tag: "Unit 14",
    topics: ["Count Nouns", "Non-Count Nouns", "Partitives", "Some / Any"]
  },
  "Grammar Explorer 1/unit_15_there_is_there_are_and_it.html": {
    title: "Unit 15: There Is / There Are & It",
    tag: "Unit 15",
    topics: ["There is/are", "It as Subject", "Existence", "Weather/Time"]
  }
};

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
    topics: ["Health & Fitness", "Count/Non-count Nouns", "Quantifiers", "Definite/Indefinite Articles"],
    subLessons: {
      "grammar_explorer_2_unit_3_lesson_1.html": {
        title: "Unit 3 - Lesson 1: Plural and Possessive Nouns; Another and Other",
        tag: "Book U3 L1",
        topics: ["Plural Nouns", "Possessive Nouns", "Another vs Other", "Spelling Rules"]
      },
      "grammar_explorer_2_unit_3_lesson_2.html": {
        title: "Unit 3 - Lesson 2: Count and Non-Count Nouns",
        tag: "Book U3 L2",
        topics: ["Count Nouns", "Non-Count Nouns", "Categories of Nouns", "Superfoods"]
      },
      "grammar_explorer_2_unit_3_lesson_3.html": {
        title: "Unit 3 - Lesson 3: Quantity and Measurement Words",
        tag: "Book U3 L3",
        topics: ["Quantity Words", "Measurement Units", "Sports Science", "Nutrition"]
      },
      "grammar_explorer_2_unit_3_review_writing.html": {
        title: "Unit 3: Review the Grammar & Connect to Writing",
        tag: "Book U3 Writing",
        topics: ["Unit 3 Review", "Subject-Verb Agreement", "Opinion Paragraphs", "Staying Fit"]
      }
    }
  },
  4: {
    title: "Unit 4: Going Places (Pronouns, Prepositions, and Articles)",
    topics: ["Going Places", "Travel", "Personal & Reflexive Pronouns", "Prepositions of Time/Place/Direction", "Articles"],
    subLessons: {
      "grammar_explorer_2_unit_4_lesson_1.html": {
        title: "Unit 4 - Lesson 1: Personal Pronouns, Possessives & Reflexives",
        tag: "Book U4 L1",
        topics: ["Subject & Object Pronouns", "Possessive Forms", "Reflexive Pronouns", "Getting Around"]
      },
      "grammar_explorer_2_unit_4_lesson_2.html": {
        title: "Unit 4 - Lesson 2: Prepositions of Time, Place, and Direction",
        tag: "Book U4 L2",
        topics: ["Prepositions of Time", "Prepositions of Place", "Direction Prepositions", "Travel Websites"]
      },
      "grammar_explorer_2_unit_4_lesson_3.html": {
        title: "Unit 4 - Lesson 3: Articles: Indefinite and Definite Articles; Generalizations",
        tag: "Book U4 L3",
        topics: ["Indefinite Articles", "Definite Article", "Generalizations", "Wilderness Expeditions"]
      },
      "grammar_explorer_2_unit_4_lesson_4.html": {
        title: "Unit 4 - Lesson 4: Articles with Place Names",
        tag: "Book U4 L4",
        topics: ["Geographic Names", "Hotels & Buildings", "Streets & Parks", "Travel Blogs"]
      },
      "grammar_explorer_2_unit_4_review_writing.html": {
        title: "Unit 4: Review the Grammar & Connect to Writing",
        tag: "Book U4 Writing",
        topics: ["Unit 4 Review", "Misplaced Prepositional Phrases", "Descriptive Paragraphs", "Favorite Places"]
      }
    }
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
 * Check Git Status & Changes specifically in Core Directories
 */
function checkDirectoryGitChanges(dirs = CORE_DIRECTORIES) {
  log(`\n${bold(cyan('-------------------------------------------------------'))}`);
  log(`  ${bold('🔍 Inspecting Git Status & Changes in Core Directories')}`);
  log(`${bold(cyan('-------------------------------------------------------'))}`);

  const results = {};
  let totalChanges = 0;

  for (const dir of dirs) {
    const dirPath = path.join(REPO_DIR, dir);
    if (!fs.existsSync(dirPath)) {
      results[dir] = { exists: false, changes: [] };
      continue;
    }

    try {
      const output = execSync(`git status --porcelain -- "${dir}"`, {
        cwd: REPO_DIR,
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();

      const lines = output ? output.split('\n').map(l => l.trimEnd()).filter(Boolean) : [];
      const changes = lines.map(line => {
        const code = line.slice(0, 2).trim();
        const relFile = line.slice(3).trim().replace(/^"|"$/g, '');
        let status = 'MODIFIED';
        let colorFn = yellow;
        if (code === '??') {
          status = 'UNTRACKED';
          colorFn = green;
        } else if (code.includes('A')) {
          status = 'ADDED';
          colorFn = green;
        } else if (code.includes('D')) {
          status = 'DELETED';
          colorFn = red;
        } else if (code.includes('R')) {
          status = 'RENAMED';
          colorFn = cyan;
        }
        return { code, status, file: relFile, filename: path.basename(relFile), colorFn };
      });

      results[dir] = { exists: true, changes };
      totalChanges += changes.length;

      if (changes.length === 0) {
        log(`  📂 ${bold(dir)}: ${green('✓ Clean (No uncommitted changes)')}`);
      } else {
        log(`  📂 ${bold(dir)}: ${yellow(bold(`${changes.length} change(s) detected:`))}`);
        changes.forEach(c => {
          log(`     • ${c.colorFn(`[${c.status}]`)} ${c.filename} ${dim(`(${c.file})`)}`);
        });
      }
    } catch (e) {
      log(`  📂 ${bold(dir)}: ${red(`Error checking status: ${e.message}`)}`);
      results[dir] = { exists: true, changes: [], error: e.message };
    }
  }

  // Also check Book Edition & Hub Index
  try {
    const bookStatus = execSync('git status --porcelain -- "Grammar-Explorer-book" "index.html"', {
      cwd: REPO_DIR,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).trim();
    if (bookStatus) {
      const bookLines = bookStatus.split('\n').filter(Boolean);
      log(`  📂 ${bold('Book Edition / Hub Index')}: ${yellow(`${bookLines.length} change(s) detected`)}`);
    } else {
      log(`  📂 ${bold('Book Edition / Hub Index')}: ${green('✓ Clean')}`);
    }
  } catch (e) {}

  log(`${bold(cyan('-------------------------------------------------------'))}`);
  return { results, totalChanges };
}

/**
 * Scan existing standard curriculum lessons from index.html to preserve custom mappings.
 */
function extractExistingStandardCatalog(html) {
  const match = html.match(/const\s+masterCatalog\s*=\s*\[([\s\S]*?)\];/);
  if (!match) return [];

  const rawCode = match[1];
  const items = [];
  const itemRegex = /{\s*id:\s*["']([^"']+)["'],\s*level:\s*["']([^"']+)["'],\s*folder:\s*["']([^"']+)["'],\s*file:\s*["']([^"']+)["'],\s*title:\s*["']([^"']+)["'],\s*tag:\s*["']([^"']+)["'],\s*topics:\s*(\[[^\]]*\])\s*}/g;
  let m;
  while ((m = itemRegex.exec(rawCode)) !== null) {
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
 * Dynamically scan a standard directory on disk, preserving known metadata and
 * auto-extracting info for newly detected lesson files.
 */
function scanStandardDirectory(folderName, levelCode, existingCatalogMap) {
  const dirPath = path.join(REPO_DIR, folderName);
  if (!fs.existsSync(dirPath)) return { items: [], newCount: 0, totalDisk: 0 };

  const files = fs.readdirSync(dirPath)
    .filter(f => f.endsWith('.html') && f.toLowerCase() !== 'index.html');

  // Natural numerical sorting for unit and lesson names
  files.sort((a, b) => {
    const numA = (a.match(/\d+/) || [999])[0];
    const numB = (b.match(/\d+/) || [999])[0];
    const diff = parseInt(numA, 10) - parseInt(numB, 10);
    if (diff !== 0) return diff;
    return a.localeCompare(b, undefined, { numeric: true });
  });

  const items = [];
  let newCount = 0;

  for (const filename of files) {
    const relFile = `${folderName}/${filename}`;
    const existing = existingCatalogMap[relFile];

    if (existing) {
      items.push(existing);
      continue;
    }

    // Check curated metadata dictionary
    const curated = STANDARD_CURATED_METADATA[relFile];
    if (curated) {
      const baseId = filename.replace(/\.html$/i, '').replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
      items.push({
        id: `${levelCode.toLowerCase()}_${baseId}`,
        level: levelCode,
        folder: folderName,
        file: relFile,
        title: curated.title,
        tag: curated.tag,
        topics: curated.topics
      });
      newCount++;
      continue;
    }

    // Auto-extract metadata from HTML file content
    let fileContent = '';
    try {
      fileContent = fs.readFileSync(path.join(dirPath, filename), 'utf8');
    } catch (e) {
      fileContent = '';
    }

    let title = '';
    const titleMatch = fileContent.match(/<title>([^<]+)<\/title>/i);
    if (titleMatch) {
      title = titleMatch[1]
        .replace(/\s*\|\s*Grammar\s*Explorer.*$/i, '')
        .replace(/\s*-\s*Grammar\s*Explorer.*$/i, '')
        .trim();
    }
    if (!title) {
      const cleanName = filename.replace(/\.html$/i, '').replace(/[_-]+/g, ' ');
      title = cleanName.charAt(0).toUpperCase() + cleanName.slice(1);
    }

    let tag = '';
    const unitMatch = filename.match(/units?_?(\d+(?:_\d+)?)/i) || title.match(/Units?\s*(\d+(?:\s*(?:&|and)\s*\d+)?)/i);
    if (unitMatch) {
      const uStr = unitMatch[1].replace('_', ' & ');
      tag = uStr.includes('&') ? `Units ${uStr}` : `Unit ${uStr}`;
    } else if (/wh_question/i.test(filename)) {
      tag = 'Masterclass';
    } else {
      tag = 'Lesson';
    }

    let topics = [];
    const metaKwMatch = fileContent.match(/<meta\s+name=["']keywords["']\s+content=["']([^"']+)["']/i);
    if (metaKwMatch) {
      topics = metaKwMatch[1].split(',').map(s => s.trim()).filter(Boolean).slice(0, 5);
    }
    if (topics.length === 0) {
      const cleaned = title.replace(/Unit\s*\d+(\s*&amp;|\s*&|\s*and\s*\d+)?:?/i, '').trim();
      topics = cleaned.split(/[,:;()\/]+/).map(s => s.trim()).filter(s => s.length > 2).slice(0, 4);
      if (topics.length === 0) {
        topics = [tag, levelCode];
      }
    }

    const baseId = filename.replace(/\.html$/i, '').replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
    items.push({
      id: `${levelCode.toLowerCase()}_${baseId}`,
      level: levelCode,
      folder: folderName,
      file: relFile,
      title,
      tag,
      topics
    });
    newCount++;
  }

  return { items, newCount, totalDisk: files.length };
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

  // 1. Inspect Git Changes in Core Directories
  const gitAudit = checkDirectoryGitChanges(CORE_DIRECTORIES);

  const indexHtml = fs.readFileSync(INDEX_PATH, 'utf8');

  // 2. Extract existing standard catalog into lookup map
  const existingStandard = extractExistingStandardCatalog(indexHtml);
  const existingMap = {};
  existingStandard.forEach(item => {
    existingMap[item.file] = item;
  });

  log(`\n${bold(cyan('-------------------------------------------------------'))}`);
  log(`  ${bold('📁 Scanning Filesystem Across Core Curriculum Folders')}`);
  log(`${bold(cyan('-------------------------------------------------------'))}`);

  // 3. Scan directories on disk
  const ge1Scan = scanStandardDirectory('Grammar Explorer 1', 'GE1', existingMap);
  const ge2Scan = scanStandardDirectory('Grammar Explorer 2', 'GE2', existingMap);
  const ge3Scan = scanStandardDirectory('Grammar Explorer 3', 'GE3', existingMap);

  log(`  • ${bold('Grammar Explorer 1')}: ${cyan(ge1Scan.totalDisk)} files on disk ${ge1Scan.newCount > 0 ? green(`(+${ge1Scan.newCount} newly indexed)`) : dim('(up to date)')}`);
  log(`  • ${bold('Grammar Explorer 2')}: ${cyan(ge2Scan.totalDisk)} files on disk ${ge2Scan.newCount > 0 ? green(`(+${ge2Scan.newCount} newly indexed)`) : dim('(up to date)')}`);
  log(`  • ${bold('Grammar Explorer 3')}: ${cyan(ge3Scan.totalDisk)} files on disk ${ge3Scan.newCount > 0 ? green(`(+${ge3Scan.newCount} newly indexed)`) : dim('(up to date)')}`);

  const ge1Items = ge1Scan.items;
  const ge2Items = ge2Scan.items;
  const ge3Items = ge3Scan.items;
  const standardCount = ge1Items.length + ge2Items.length + ge3Items.length;

  // 4. Generate Book catalog
  const bookItems = generateBookCatalog();
  log(`  • ${bold('GE2-Book Edition')}:   ${cyan(bookItems.length)} interactive units/lessons scanned`);
  log(`${bold(cyan('-------------------------------------------------------'))}`);

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

  // 5. Replace in index.html
  const catalogRegex = /\/\/\s*Master Catalog[\s\S]*?const\s+masterCatalog\s*=\s*\[[\s\S]*?\];/;
  if (!catalogRegex.test(indexHtml)) {
    log(`${red('Error:')} Could not locate masterCatalog block in index.html`);
    process.exit(1);
  }

  const updatedHtml = indexHtml.replace(catalogRegex, fullCatalogCode);
  const totalCatalogEntries = ge1Items.length + ge2Items.length + ge3Items.length + bookItems.length;

  if (isDryRun) {
    log(`\n  ${yellow(bold('DRY RUN Summary:'))}`);
    log(`  - Standard GE1: ${ge1Items.length} lessons (Disk: ${ge1Scan.totalDisk})`);
    log(`  - Standard GE2: ${ge2Items.length} lessons (Disk: ${ge2Scan.totalDisk})`);
    log(`  - Standard GE3: ${ge3Items.length} lessons (Disk: ${ge3Scan.totalDisk})`);
    log(`  - Full Book GE2: ${bookItems.length} interactive units/lessons`);
    log(`  - Total Master Catalog Entries: ${bold(green(totalCatalogEntries))} items`);
    log(`  - Git Changes in Core Folders: ${gitAudit.totalChanges > 0 ? yellow(`${gitAudit.totalChanges} uncommitted change(s)`) : green('0 (Clean)')}`);
    log(`\n${bold(cyan('======================================================='))}
`);
    return;
  }

  // Live execution: Create backup first
  createBackup();

  fs.writeFileSync(INDEX_PATH, updatedHtml, 'utf8');
  log(`  ${green('✓')} Successfully updated ${bold('index.html')} with ${bold(green(totalCatalogEntries))} catalog entries!`);

  // Git Push Automation
  if (isPush) {
    log(`\n${bold(cyan('======================================================='))}`);
    log(`  ${bold('📦 Committing & Pushing to GitHub...')}`);
    log(`${bold(cyan('======================================================='))}`);
    try {
      log(`  ${dim('Staging all files across workspace...')}`);
      execSync('git add -A', { cwd: REPO_DIR, stdio: 'inherit' });

      // Check if any staged changes exist
      const stagedStatus = execSync('git diff --cached --name-status', { cwd: REPO_DIR, encoding: 'utf8' }).trim();

      if (!stagedStatus) {
        log(`  ${yellow('Note: Working tree is clean, no newly staged changes to commit.')}`);
      } else {
        const stagedLines = stagedStatus.split('\n').filter(Boolean);
        log(`  ${green('✓ Staged changes:')} ${stagedLines.length} file(s) ready to commit.`);

        const commitMsg = customMessage || `feat: sync catalog and update changes across GE1, GE2, GE3, Book (${totalCatalogEntries} items)`;
        execSync(`git commit -m "${commitMsg.replace(/"/g, '\\"')}" --author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"`, { cwd: REPO_DIR, stdio: 'inherit' });
        log(`  ${green('✓ Commit created:')} "${commitMsg}"`);
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
    log(`    or run: ${cyan('.\\update-and-push.bat')}`);
  }

  log(`\n${bold(cyan('======================================================='))}
`);
}

updateIndex();
