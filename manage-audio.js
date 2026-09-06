/**
 * Grammar Explorer - Audio Track Manager & Drive Integrator
 * 
 * Scans lesson files across all curriculum directories:
 *   - Grammar Explorer 1/
 *   - Grammar Explorer 2/
 *   - Grammar Explorer 3/
 *   - Grammar-Explorer-book/ (Grammar-Explorer-2 Units 1-16 & sub-lessons)
 * 
 * Inspects Git status and detects changes in Grammar Explorer 1, 2, and 3.
 * Maintains audio-registry.json, converts Google Drive links to direct streaming URLs,
 * and automatically injects or updates audio players into lesson files.
 * 
 * Usage:
 *   node manage-audio.js                 # Interactive menu (Scan, List, Add Link, Apply)
 *   node manage-audio.js --check         # Checks Git status & changes in GE1, GE2, GE3, Book
 *   node manage-audio.js --scan          # Scans files and updates audio-registry.json
 *   node manage-audio.js --list          # Displays all detected tracks and current status
 *   node manage-audio.js --add CD1-02 "<drive_or_mp3_url>" # Sets audio link and injects into files
 *   node manage-audio.js --apply         # Applies all configured links from audio-registry.json
 *   node manage-audio.js --apply --push  # Checks changes, applies audio players and pushes to GitHub
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');

const REPO_DIR = __dirname;
const REGISTRY_PATH = path.join(REPO_DIR, 'audio-registry.json');
const BACKUP_DIR = path.join(REPO_DIR, '_backups');

const CORE_DIRECTORIES = [
  'Grammar Explorer 1',
  'Grammar Explorer 2',
  'Grammar Explorer 3'
];

// CLI Arguments
const args = process.argv.slice(2);
const isScan = args.includes('--scan');
const isList = args.includes('--list');
const isCheck = args.includes('--check') || args.includes('-c');
const isApply = args.includes('--apply');
const isPush = args.includes('--push');
const addIdx = args.findIndex(a => a === '--add' || a === '-a');
const removeIdx = args.findIndex(a => a === '--remove' || a === '-r');

// Terminal colors
const cyan = (s) => `\x1b[36m${s}\x1b[0m`;
const green = (s) => `\x1b[32m${s}\x1b[0m`;
const yellow = (s) => `\x1b[33m${s}\x1b[0m`;
const red = (s) => `\x1b[31m${s}\x1b[0m`;
const bold = (s) => `\x1b[1m${s}\x1b[0m`;
const dim = (s) => `\x1b[2m${s}\x1b[0m`;

function log(msg) { console.log(msg); }

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

  // Also check Book Edition & Registry
  try {
    const bookStatus = execSync('git status --porcelain -- "Grammar-Explorer-book" "audio-registry.json"', {
      cwd: REPO_DIR,
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'ignore']
    }).trim();
    if (bookStatus) {
      const bookLines = bookStatus.split('\n').filter(Boolean);
      log(`  📂 ${bold('Book Edition / Audio Registry')}: ${yellow(`${bookLines.length} change(s) detected`)}`);
    } else {
      log(`  📂 ${bold('Book Edition / Audio Registry')}: ${green('✓ Clean')}`);
    }
  } catch (e) {}

  log(`${bold(cyan('-------------------------------------------------------'))}`);
  return { results, totalChanges };
}

/**
 * Converts any Google Drive link to a direct streaming audio URL.
 */
function convertToDirectAudioUrl(url) {
  if (!url || typeof url !== 'string') return '';
  const trimmed = url.trim();

  // Match /file/d/<ID> or id=<ID>
  const fileIdMatch = trimmed.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) 
    || trimmed.match(/[?&]id=([a-zA-Z0-9_-]+)/);

  if (fileIdMatch && fileIdMatch[1]) {
    return `https://docs.google.com/uc?export=open&id=${fileIdMatch[1]}`;
  }
  return trimmed;
}

/**
 * Creates backup of a file in _backups/ directory.
 */
function backupFile(filePath) {
  if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
  }
  const now = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const timestamp = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
  const baseName = path.basename(filePath);
  const backupPath = path.join(BACKUP_DIR, `${baseName}.backup_${timestamp}`);
  fs.copyFileSync(filePath, backupPath);
  return backupPath;
}

/**
 * Recursively retrieves all HTML files in a directory.
 */
function getHtmlFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== '_backups' && entry.name !== '.git') {
      results = results.concat(getHtmlFiles(fullPath));
    } else if (entry.name.endsWith('.html') && entry.name !== 'index.html') {
      results.push(fullPath);
    }
  }
  return results;
}

/**
 * Checks if a badge is an overview/table of contents index card:
 * - Has onclick="switchTab(...)" in parent container
 * - In Unit Sections Index / Unit Lessons Index
 * - Or lists multiple tracks (e.g. "CD1-02, 03, 04", "CD1-05, 06", etc.)
 */
function isOverviewBadge(content, matchIndex, badgeText) {
  if (badgeText.includes(',') || badgeText.includes('&') || /CD\d+-\d+\s*,\s*\d+/i.test(badgeText)) {
    return true;
  }
  const prevChunk = content.slice(Math.max(0, matchIndex - 600), matchIndex);
  if (prevChunk.includes('switchTab(') || prevChunk.includes('Unit Sections Index') || prevChunk.includes('Unit Lessons Index')) {
    const lastSwitchTab = prevChunk.lastIndexOf('switchTab(');
    if (lastSwitchTab !== -1) {
      const afterSwitchTab = prevChunk.slice(lastSwitchTab);
      const openDivs = (afterSwitchTab.match(/<div/gi) || []).length;
      const closeDivs = (afterSwitchTab.match(/<\/div>/gi) || []).length;
      if (openDivs >= closeDivs) return true;
    } else {
      return true;
    }
  }
  return false;
}

/**
 * Scans all lesson files and builds/updates audio-registry.json
 */
function scanTracks() {
  log(`\n${bold('🔍 Scanning lesson files across all curriculum folders for audio tracks...')}`);
  
  const scanDirs = [
    path.join(REPO_DIR, 'Grammar Explorer 1'),
    path.join(REPO_DIR, 'Grammar Explorer 2'),
    path.join(REPO_DIR, 'Grammar Explorer 3'),
    path.join(REPO_DIR, 'Grammar-Explorer-book')
  ];

  let files = [];
  for (const dir of scanDirs) {
    if (fs.existsSync(dir)) {
      files = files.concat(getHtmlFiles(dir));
    }
  }

  // Load existing registry if available
  let registry = {};
  if (fs.existsSync(REGISTRY_PATH)) {
    try {
      registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
    } catch (e) {
      registry = {};
    }
  }

  let foundCount = 0;

  for (const filePath of files) {
    const relPath = path.relative(REPO_DIR, filePath).replace(/\\/g, '/');
    const content = fs.readFileSync(filePath, 'utf8');

    // Regex to match badge-cd spans and divs
    const badgeRegex = /<(?:span|div)[^>]*class="[^"]*badge-cd[^"]*"[^>]*>([\s\S]*?)<\/(?:span|div)>/gi;
    let m;
    while ((m = badgeRegex.exec(content)) !== null) {
      const rawText = m[1].replace(/<[^>]+>/g, '').trim();
      const isOverview = isOverviewBadge(content, m.index, rawText);
      const trackMatch = rawText.match(/CD\d+[\s_-]*\d+/gi);
      if (!trackMatch) continue;

      for (const rawTrack of trackMatch) {
        const trackId = rawTrack.toUpperCase().replace(/\s+/g, '-').replace(/_+/g, '-');

        // Extract surrounding context (e.g. exercise heading)
        const snippetStart = Math.max(0, m.index - 400);
        const snippet = content.slice(snippetStart, m.index);
        const headingMatch = snippet.match(/<h[2-4][^>]*>([\s\S]*?)<\/h[2-4]>/i) 
          || snippet.match(/class="[^"]*(?:font-bold|font-extrabold|font-serif)[^"]*"[^>]*>([\s\S]*?)<\/(?:span|div|h[2-4]|p)>/i);
        let contextTitle = headingMatch ? headingMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : `Exercise Track ${trackId}`;
        if (contextTitle.length < 3) contextTitle = `Exercise Track ${trackId}`;

        if (!registry[trackId]) {
          registry[trackId] = {
            trackId: trackId,
            title: isOverview ? `Exercise Track ${trackId}` : contextTitle,
            driveLink: "",
            directUrl: "",
            files: [relPath],
            hasPlayer: content.includes(`data-audio-track="${trackId}"`)
          };
          foundCount++;
        } else {
          if (!registry[trackId].files.includes(relPath)) {
            registry[trackId].files.push(relPath);
          }
          if (!isOverview && (registry[trackId].title.startsWith('Exercise Track') || registry[trackId].title.startsWith('Lesson ') || registry[trackId].title.length < 5 || /^\d+$/.test(registry[trackId].title))) {
            registry[trackId].title = contextTitle;
          }
          if (content.includes(`data-audio-track="${trackId}"`)) {
            registry[trackId].hasPlayer = true;
          }
        }
      }
    }
  }

  // Sort keys naturally
  const sortedKeys = Object.keys(registry).sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  const sortedRegistry = {};
  for (const k of sortedKeys) {
    sortedRegistry[k] = registry[k];
  }

  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(sortedRegistry, null, 2), 'utf8');
  log(`  ${green('✓')} Found & indexed ${bold(sortedKeys.length)} unique audio tracks across ${files.length} lesson files.`);
  log(`  ${green('✓')} Registry saved to ${bold('audio-registry.json')}\n`);
  return sortedRegistry;
}

/**
 * Formats and prints the audio track listing.
 */
function listTracks() {
  if (!fs.existsSync(REGISTRY_PATH)) {
    scanTracks();
  }
  const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  const trackIds = Object.keys(registry);

  log(`\n${bold(cyan('========================================================================='))}`);
  log(`  ${bold('Grammar Explorer Audio Track Registry')} (${trackIds.length} Total Tracks)`);
  log(`${bold(cyan('========================================================================='))}\n`);

  let configuredCount = 0;
  for (const id of trackIds) {
    const item = registry[id];
    const isConfigured = Boolean(item.directUrl || item.driveLink);
    if (isConfigured) configuredCount++;

    const statusBadge = isConfigured 
      ? green('[✓ LINK ATTACHED]') 
      : yellow('[○ PENDING LINK]');
    
    const playerBadge = item.hasPlayer 
      ? cyan('[PLAYER INJECTED]') 
      : dim('[NO PLAYER]');

    log(`  ${bold(id.padEnd(10))} ${statusBadge} ${playerBadge} - ${item.title}`);
    log(`    ${dim('Files:')} ${item.files.map(f => path.basename(f)).join(', ')}`);
    if (item.driveLink) {
      log(`    ${dim('Stream URL:')} ${item.directUrl || item.driveLink}`);
    }
    log('');
  }

  log(`${bold(cyan('-------------------------------------------------------------------------'))}`);
  log(`  ${bold('Summary:')} ${green(configuredCount + ' tracks linked')} | ${yellow((trackIds.length - configuredCount) + ' pending')}`);
  log(`${bold(cyan('========================================================================='))}
`);
}

/**
 * Builds standard HTML player element for a track.
 */
function createPlayerHtml(trackId, audioUrl) {
  const fileIdMatch = audioUrl.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) 
    || audioUrl.match(/[?&]id=([a-zA-Z0-9_-]+)/);

  if (fileIdMatch && fileIdMatch[1]) {
    const fileId = fileIdMatch[1];
    return `<!-- Audio Player [${trackId}] -->
<div class="audio-player-widget my-2 rounded-xl overflow-hidden border border-slate-800 shadow-sm bg-black" data-audio-track="${trackId}">
  <div style="width: calc(100% + 56px); margin-right: -56px;">
    <iframe src="https://drive.google.com/file/d/${fileId}/preview" width="100%" height="54" class="w-full block" frameborder="0" allow="autoplay"></iframe>
  </div>
</div>
<!-- End Audio Player [${trackId}] -->`;
  }

  return `<!-- Audio Player [${trackId}] -->
<div class="audio-player-widget my-2 rounded-xl overflow-hidden border border-slate-800 shadow-sm bg-black p-1.5" data-audio-track="${trackId}">
  <audio controls preload="none" class="w-full h-8 accent-amber-500 rounded" src="${audioUrl}">
    Your browser does not support the audio element.
  </audio>
</div>
<!-- End Audio Player [${trackId}] -->`;
}

/**
 * Injects or updates an audio player in target files for a track.
 */
function injectPlayerIntoFiles(trackId, audioUrl, targetFiles) {
  const playerHtml = createPlayerHtml(trackId, audioUrl);
  let updatedFiles = 0;

  for (const relFile of targetFiles) {
    const fullPath = path.join(REPO_DIR, relFile);
    if (!fs.existsSync(fullPath)) continue;

    let content = fs.readFileSync(fullPath, 'utf8');

    // 1. Strip ALL existing player instances for this track
    const existingPlayerRegex = new RegExp(`<!-- Audio Player \\[${trackId}\\] -->[\\s\\S]*?<!-- End Audio Player \\[${trackId}\\] -->\\n?`, 'gi');
    content = content.replace(existingPlayerRegex, '');

    // 2. Find all valid target badge-cd occurrences for this track
    const escapedTrack = trackId.replace(/[-]/g, '[-_\\s]*');
    const badgeRegex = /<(?:span|div)[^>]*class="[^"]*badge-cd[^"]*"[^>]*>([\s\S]*?)<\/(?:span|div)>/gi;
    
    const rawMatches = [];
    let m;
    while ((m = badgeRegex.exec(content)) !== null) {
      const badgeText = m[1].replace(/<[^>]+>/g, '').trim();
      const trackPattern = new RegExp(`^Track\\s+${escapedTrack}$|^${escapedTrack}$`, 'i');
      const hasTrack = trackPattern.test(badgeText) || badgeText.toUpperCase().includes(trackId);
      if (!hasTrack) continue;
      if (isOverviewBadge(content, m.index, badgeText)) continue;

      const snippet = content.slice(Math.max(0, m.index - 500), m.index);
      const isTabHeader = snippet.includes('<h2') && !snippet.includes('<h3') && !snippet.includes('<h4');

      const badgeEnd = m.index + m[0].length;
      const nextDivEnd = content.indexOf('</div>', badgeEnd);
      const insertPos = (nextDivEnd !== -1) ? (nextDivEnd + '</div>'.length) : badgeEnd;
      rawMatches.push({ pos: insertPos, text: badgeText, isTabHeader });
    }

    const hasCardBadges = rawMatches.some(b => !b.isTabHeader);
    const matches = hasCardBadges ? rawMatches.filter(b => !b.isTabHeader) : rawMatches;

    if (matches.length > 0) {
      matches.sort((a, b) => b.pos - a.pos);

      for (const item of matches) {
        content = content.slice(0, item.pos) + '\n' + playerHtml + content.slice(item.pos);
      }

      backupFile(fullPath);
      fs.writeFileSync(fullPath, content, 'utf8');
      log(`    ${green('✓')} Injected audio player at ${bold(matches.length)} place(s) in: ${path.basename(fullPath)}`);
      updatedFiles++;
    } else {
      log(`    ${yellow('!')} Could not locate target badge for ${trackId} in ${path.basename(fullPath)}`);
    }
  }

  return updatedFiles;
}

/**
 * Add or update audio link for a specific track.
 */
function setTrackAudio(trackId, rawUrl) {
  const normalizedId = trackId.toUpperCase().replace(/\s+/g, '-').replace(/_+/g, '-');
  if (!fs.existsSync(REGISTRY_PATH)) {
    scanTracks();
  }

  const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  if (!registry[normalizedId]) {
    log(`${red('Error:')} Track "${normalizedId}" was not found in registry.`);
    return;
  }

  const directUrl = convertToDirectAudioUrl(rawUrl);
  registry[normalizedId].driveLink = rawUrl;
  registry[normalizedId].directUrl = directUrl;

  log(`\n${bold('🎵 Configuring Audio Track:')} ${cyan(normalizedId)}`);
  log(`  ${dim('Provided Link:')} ${rawUrl}`);
  log(`  ${dim('Streaming URL:')} ${directUrl}`);

  const modified = injectPlayerIntoFiles(normalizedId, directUrl, registry[normalizedId].files);
  registry[normalizedId].hasPlayer = modified > 0;

  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');
  log(`\n  ${green('✓')} Successfully attached audio to ${bold(modified)} file(s)!`);
}

/**
 * Removes audio player for a specific track from files and clears registry link.
 */
function removeTrackAudio(trackId) {
  const normalizedId = trackId.toUpperCase().replace(/\s+/g, '-').replace(/_+/g, '-');
  if (!fs.existsSync(REGISTRY_PATH)) return;

  const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  if (!registry[normalizedId]) {
    log(`${red('Error:')} Track "${normalizedId}" was not found in registry.`);
    return;
  }

  log(`\n${bold('🗑 Removing Audio Player:')} ${cyan(normalizedId)}`);
  let removedCount = 0;

  for (const relFile of registry[normalizedId].files) {
    const fullPath = path.join(REPO_DIR, relFile);
    if (!fs.existsSync(fullPath)) continue;

    let content = fs.readFileSync(fullPath, 'utf8');
    const existingPlayerRegex = new RegExp(`<!-- Audio Player \\[${normalizedId}\\] -->[\\s\\S]*?<!-- End Audio Player \\[${normalizedId}\\] -->\\n?`, 'i');

    if (existingPlayerRegex.test(content)) {
      backupFile(fullPath);
      content = content.replace(existingPlayerRegex, '');
      fs.writeFileSync(fullPath, content, 'utf8');
      log(`    ${green('✓')} Removed audio player from: ${path.basename(fullPath)}`);
      removedCount++;
    }
  }

  registry[normalizedId].driveLink = "";
  registry[normalizedId].directUrl = "";
  registry[normalizedId].hasPlayer = false;

  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');
  log(`\n  ${green('✓')} Successfully removed audio player from ${bold(removedCount)} file(s)!`);
}

/**
 * Applies all configured tracks from audio-registry.json to files.
 */
function applyAllConfigured(shouldPush = isPush) {
  if (!fs.existsSync(REGISTRY_PATH)) {
    scanTracks();
  }

  // Check Git status across core directories
  checkDirectoryGitChanges();

  const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
  const trackIds = Object.keys(registry);

  log(`\n${bold('⚡ Applying all configured audio tracks to lesson files...')}`);
  let totalInjected = 0;

  for (const id of trackIds) {
    const item = registry[id];
    if (item.directUrl || item.driveLink) {
      const url = item.directUrl || convertToDirectAudioUrl(item.driveLink);
      log(`  Applying ${cyan(id)}...`);
      const count = injectPlayerIntoFiles(id, url, item.files);
      if (count > 0) {
        item.hasPlayer = true;
        totalInjected += count;
      }
    }
  }

  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');
  log(`\n  ${green('✓')} Finished applying audio players (${bold(totalInjected)} file updates).`);

  if (shouldPush) {
    log(`\n${bold('📦 Committing & Pushing to GitHub...')}`);
    try {
      execSync('git add -A', { cwd: REPO_DIR, stdio: 'inherit' });
      const stagedStatus = execSync('git diff --cached --name-status', { cwd: REPO_DIR, encoding: 'utf8' }).trim();
      
      if (!stagedStatus) {
        log(`  ${yellow('Note: Working tree is clean, no newly staged changes to commit.')}`);
      } else {
        const commitMsg = `feat: attach lesson audio players (${totalInjected} files)`;
        execSync(`git commit -m "${commitMsg}" --author="NeoTetsuya <35198449+NeoTetsuya@users.noreply.github.com>"`, { cwd: REPO_DIR, stdio: 'inherit' });
        log(`  ${green('✓ Commit created:')} "${commitMsg}"`);
      }

      log(`  ${cyan('Pushing to GitHub (origin main)...')}`);
      execSync('git push -u origin main', { cwd: REPO_DIR, stdio: 'inherit' });
      log(`  ${green('✓ Successfully pushed to GitHub!')}`);
    } catch (err) {
      console.error(red(`Git push failed: ${err.message}`));
    }
  }
}

/**
 * Interactive Command Line Menu (loops continuously until user exits)
 */
function interactiveMenu() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  function showMenu() {
    log(`\n${bold(cyan('========================================================================='))}`);
    log(`  ${bold('Grammar Explorer - Audio Track Manager & Drive Integrator')}`);
    log(`${bold(cyan('========================================================================='))}`);
    log(`  1. ${bold('Scan Lessons')} (Discover all CD audio tracks across GE1, GE2, GE3 & Book)`);
    log(`  2. ${bold('List Tracks')} (View all tracks & link status)`);
    log(`  3. ${bold('Add / Update Audio Links')} (Add multiple audio links continuously)`);
    log(`  4. ${bold('Remove Audio Link')} (Remove player from files for a track)`);
    log(`  5. ${bold('Check Git Changes in GE1, GE2, GE3 & Book')} (Inspect uncommitted files)`);
    log(`  6. ${bold('Apply All Configured Audio')} (Inject players into lesson files)`);
    log(`  7. ${bold('Apply & Push to GitHub')} (Inspect changes, inject players, and push)`);
    log(`  8. ${bold('Exit')}`);
    log(`${bold(cyan('========================================================================='))}\n`);

    rl.question('Select an option (1-8): ', (choice) => {
      const trimmed = choice.trim();
      if (trimmed === '1') {
        scanTracks();
        showMenu();
      } else if (trimmed === '2') {
        listTracks();
        showMenu();
      } else if (trimmed === '3') {
        promptAddTrack();
      } else if (trimmed === '4') {
        promptRemoveTrack();
      } else if (trimmed === '5') {
        checkDirectoryGitChanges();
        showMenu();
      } else if (trimmed === '6') {
        applyAllConfigured(false);
        showMenu();
      } else if (trimmed === '7') {
        applyAllConfigured(true);
        showMenu();
      } else if (trimmed === '8' || trimmed.toLowerCase() === 'exit' || trimmed.toLowerCase() === 'q') {
        log('Exiting Audio Track Manager. Goodbye!\n');
        rl.close();
      } else {
        log(yellow('Invalid option. Please enter a number between 1 and 8.'));
        showMenu();
      }
    });
  }

  function promptAddTrack() {
    log(`\n${bold(cyan('--- Add / Update Audio Link ---'))}`);
    log(`${dim('Tip: Press Enter with an empty Track ID anytime to return to the main menu.')}`);
    rl.question('Enter Track ID (e.g. CD1-05, CD2-02): ', (trackId) => {
      const cleanId = trackId.trim();
      if (!cleanId) {
        showMenu();
        return;
      }
      rl.question(`Paste Google Drive sharing link (or direct MP3 URL) for [${cleanId}]: `, (link) => {
        const cleanLink = link.trim();
        if (cleanLink) {
          setTrackAudio(cleanId, cleanLink);
        } else {
          log(yellow('Cancelled: Track URL was empty.'));
        }
        promptAddTrack();
      });
    });
  }

  function promptRemoveTrack() {
    log(`\n${bold(cyan('--- Remove Audio Link ---'))}`);
    log(`${dim('Tip: Press Enter with an empty Track ID to return to the main menu.')}`);
    rl.question('Enter Track ID to remove: ', (trackId) => {
      const cleanId = trackId.trim();
      if (!cleanId) {
        showMenu();
        return;
      }
      removeTrackAudio(cleanId);
      showMenu();
    });
  }

  showMenu();
}

// Main CLI Router
if (isCheck) {
  checkDirectoryGitChanges();
} else if (isScan) {
  scanTracks();
} else if (isList) {
  listTracks();
} else if (addIdx !== -1 && args[addIdx + 1] && args[addIdx + 2]) {
  setTrackAudio(args[addIdx + 1], args[addIdx + 2]);
} else if (removeIdx !== -1 && args[removeIdx + 1]) {
  removeTrackAudio(args[removeIdx + 1]);
} else if (isApply) {
  applyAllConfigured();
} else {
  interactiveMenu();
}
