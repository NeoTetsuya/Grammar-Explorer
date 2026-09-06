/**
 * Grammar Explorer - Standalone Auto Sorter
 * 
 * Automatically detects, standardizes, and organizes Grammar Explorer lesson files into their
 * respective unit directories (e.g., Grammar-Explorer-book/Grammar-Explorer-2/Unit X/).
 * 
 * Features:
 *   - Auto-detects Series Level (GE1, GE2, GE3, or Full Book Edition)
 *   - Auto-detects Unit number (Units 1–16) and Lesson sequence (Lesson 1–4, Review & Writing, Full Unit)
 *   - Standardizes file locations and names into proper folder hierarchies
 *   - Natural numerical sorting (Units 1..16 instead of alphanumeric 1, 10, 2)
 * 
 * Usage:
 *   node auto-sort.js            # Organizes and standardizes all lesson files
 *   node auto-sort.js --dry-run  # Preview moves and renames without modifying files
 */

const fs = require('fs');
const path = require('path');

const REPO_DIR = __dirname;

// CLI Flags
const args = process.argv.slice(2);
const isDryRun = args.includes('--dry-run');

// Terminal color styling
const cyan = (s) => `\x1b[36m${s}\x1b[0m`;
const green = (s) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s) => `\x1b[33m${s}\x1b[0m`;
const red = (s) => `\x1b[31m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;
const dim = (s) => `\x1b[2m${s}\x1b[0m`;

function log(msg) { console.log(msg); }

/**
 * Natural numerical sort comparator for strings with numbers (e.g., Unit 2 vs Unit 10).
 */
function naturalCompare(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
}

/**
 * Detect unit number (1 to 16) from filename and optional file content.
 */
function detectUnitNumber(filename, content = '') {
  // 1. Filename patterns: 'GE2 - U1', 'unit_1', 'unit-1', 'Unit 1'
  const fnMatch = filename.match(/\bU(?:nit)?[\s_-]*(\d+)\b/i) || filename.match(/unit_(\d+)/i);
  if (fnMatch) return parseInt(fnMatch[1], 10);

  if (!content) return null;

  // 2. HTML Title or header pattern
  const titleMatch = content.match(/<title>[^<]*Unit\s*(\d+)[:\s—–-]/i)
    || content.match(/<h[12][^>]*>[^<]*Unit\s*(\d+)[:\s—–-]/i)
    || content.match(/data-unit=["'](\d+)["']/i);
  if (titleMatch) return parseInt(titleMatch[1], 10);

  return null;
}

/**
 * Detect lesson category/number from filename and content.
 */
function detectLessonType(filename, content = '') {
  const lower = filename.toLowerCase();
  if (lower.includes('review') || lower.includes('writing')) {
    return { type: 'review_writing', label: 'Review & Writing' };
  }
  const lessonMatch = lower.match(/lesson[_-]?(\d+)/i);
  if (lessonMatch) {
    return { type: `lesson_${lessonMatch[1]}`, label: `Lesson ${lessonMatch[1]}` };
  }
  if (/^GE\d+\s*-\s*U\d+/i.test(filename) || lower.includes('full_unit')) {
    return { type: 'full_unit', label: 'Full Unit Book' };
  }
  return { type: 'standalone', label: 'Standalone Exercise' };
}

/**
 * Detect target series level from file or path.
 */
function detectSeriesLevel(filePath, content = '') {
  const normalized = filePath.replace(/\\/g, '/');
  if (normalized.includes('Grammar-Explorer-book/Grammar-Explorer-2') || /GE2\s*-\s*U/i.test(path.basename(filePath))) {
    return 'GE2-Book';
  }
  if (normalized.includes('Grammar-Explorer-book')) {
    return 'Book-Master';
  }
  if (normalized.includes('Grammar Explorer 1') || /ge1/i.test(path.basename(filePath))) {
    return 'GE1';
  }
  if (normalized.includes('Grammar Explorer 2') || /ge2/i.test(path.basename(filePath))) {
    return 'GE2';
  }
  if (normalized.includes('Grammar Explorer 3') || /ge3/i.test(path.basename(filePath))) {
    return 'GE3';
  }
  if (content.includes('Grammar Explorer 2')) return 'GE2';
  if (content.includes('Grammar Explorer 1')) return 'GE1';
  if (content.includes('Grammar Explorer 3')) return 'GE3';
  return 'Unknown';
}

/**
 * Main Auto-Sort execution
 */
function autoSort() {
  log(`\n${bold(cyan('======================================================='))}`);
  log(`  ${bold('Grammar Explorer - Standalone Auto Sorter')}`);
  log(`  Mode: ${isDryRun ? yellow(bold('[DRY RUN - No files will be moved]')) : green(bold('[LIVE EXECUTION]'))}`);
  log(`${bold(cyan('======================================================='))}
`);

  let movedCount = 0;
  let verifiedCount = 0;

  // 1. Check for loose files in root that belong to Grammar-Explorer-book
  const rootFiles = fs.readdirSync(REPO_DIR, { withFileTypes: true })
    .filter(d => !d.isDirectory() && d.name.endsWith('.html') && d.name !== 'index.html');

  for (const fileEnt of rootFiles) {
    const filePath = path.join(REPO_DIR, fileEnt.name);
    const content = fs.readFileSync(filePath, 'utf8').slice(0, 2000);
    const unitNum = detectUnitNumber(fileEnt.name, content);
    const level = detectSeriesLevel(filePath, content);

    if (level === 'GE2-Book' && unitNum) {
      const targetDir = path.join(REPO_DIR, 'Grammar-Explorer-book', 'Grammar-Explorer-2', `Unit ${unitNum}`);
      const targetPath = path.join(targetDir, fileEnt.name);

      log(`  ${cyan('Found loose Book file:')} ${fileEnt.name}`);
      log(`    -> Target folder: ${path.relative(REPO_DIR, targetDir)}`);

      if (!isDryRun) {
        if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });
        fs.renameSync(filePath, targetPath);
      }
      movedCount++;
    }
  }

  // 2. Scan and verify Grammar-Explorer-book/Grammar-Explorer-2 hierarchy
  const bookGe2Dir = path.join(REPO_DIR, 'Grammar-Explorer-book', 'Grammar-Explorer-2');
  if (fs.existsSync(bookGe2Dir)) {
    // Ensure all 16 Unit directories exist
    for (let u = 1; u <= 16; u++) {
      const unitDirName = `Unit ${u}`;
      const unitDirPath = path.join(bookGe2Dir, unitDirName);
      if (!fs.existsSync(unitDirPath)) {
        log(`  ${yellow('Creating missing Unit folder:')} ${path.relative(REPO_DIR, unitDirPath)}`);
        if (!isDryRun) {
          fs.mkdirSync(unitDirPath, { recursive: true });
        }
      }
    }

    // Check if any loose lesson files sit directly in Grammar-Explorer-book/Grammar-Explorer-2/
    const looseGe2Files = fs.readdirSync(bookGe2Dir, { withFileTypes: true })
      .filter(d => !d.isDirectory() && d.name.endsWith('.html') && d.name !== 'index.html');

    for (const fileEnt of looseGe2Files) {
      const filePath = path.join(bookGe2Dir, fileEnt.name);
      const content = fs.readFileSync(filePath, 'utf8').slice(0, 2000);
      const unitNum = detectUnitNumber(fileEnt.name, content);

      if (unitNum) {
        const targetDir = path.join(bookGe2Dir, `Unit ${unitNum}`);
        const targetPath = path.join(targetDir, fileEnt.name);

        log(`  ${cyan('Organizing file into Unit folder:')} ${fileEnt.name}`);
        log(`    -> ${path.relative(REPO_DIR, targetPath)}`);

        if (!isDryRun) {
          fs.renameSync(filePath, targetPath);
        }
        movedCount++;
      }
    }

    // Report active units in Book 2
    const unitDirs = fs.readdirSync(bookGe2Dir, { withFileTypes: true })
      .filter(d => d.isDirectory() && /^Unit\s*\d+$/i.test(d.name))
      .map(d => d.name)
      .sort(naturalCompare);

    log(`\n${bold('Book Edition Structure Check (Grammar Explorer 2):')}`);
    unitDirs.forEach(dirName => {
      const dirPath = path.join(bookGe2Dir, dirName);
      const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.html')).sort(naturalCompare);
      if (files.length > 0) {
        log(`  ${green('✓')} ${bold(dirName)}: ${cyan(files.length + ' file(s)')} [${files.join(', ')}]`);
        verifiedCount += files.length;
      } else {
        log(`  ${dim('○')} ${dim(dirName)}: ${dim('Placeholder (0 files)')}`);
      }
    });
  }

  log(`\n${bold(cyan('-------------------------------------------------------'))}`);
  log(`  ${bold('Summary:')}`);
  log(`  - Files Moved / Reorganized: ${movedCount > 0 ? green(movedCount) : dim('0')}`);
  log(`  - Verified Active Book Files: ${green(verifiedCount)}`);
  log(`${bold(cyan('======================================================='))}
`);
}

autoSort();
