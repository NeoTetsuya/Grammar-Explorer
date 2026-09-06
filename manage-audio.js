/**
 * Grammar Explorer - Audio Track Manager & Drive Integrator
 * 
 * Scans all lesson files for CD audio badges (e.g. CD1-02, CD1-03...), maintains
 * an audio registry (audio-registry.json), converts Google Drive links to direct streaming
 * URLs, and automatically injects or updates audio players into lesson files.
 * 
 * Usage:
 *   node manage-audio.js                 # Interactive menu (Scan, List, Add Link, Apply)
 *   node manage-audio.js --scan          # Scans files and updates audio-registry.json
 *   node manage-audio.js --list          # Displays all detected tracks and current status
 *   node manage-audio.js --add CD1-02 "<drive_or_mp3_url>" # Sets audio link and injects into files
 *   node manage-audio.js --apply         # Applies all configured links from audio-registry.json
 *   node manage-audio.js --apply --push  # Applies audio players and pushes to GitHub
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { execSync } = require('child_process');

const REPO_DIR = __dirname;
const REGISTRY_PATH = path.join(REPO_DIR, 'audio-registry.json');
const BACKUP_DIR = path.join(REPO_DIR, '_backups');

// CLI Arguments
const args = process.argv.slice(2);
const isScan = args.includes('--scan');
const isList = args.includes('--list');
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
  log(`\n${bold('🔍 Scanning lesson files for audio tracks...')}`);
  const bookDir = path.join(REPO_DIR, 'Grammar-Explorer-book');
  const files = getHtmlFiles(bookDir);

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
          // If previous title was generic, short, numeric, or from an overview, and we have a specific heading now, upgrade it
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
  log(`  ${green('✓')} Found & indexed ${bold(sortedKeys.length)} unique audio tracks across lessons.`);
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
 * Uses Google Drive Preview player for Drive files (bypassing browser CORP blocking)
 * and native HTML5 audio for standard MP3 URLs.
 */
function createPlayerHtml(trackId, audioUrl) {
  const fileIdMatch = audioUrl.match(/\/file\/d\/([a-zA-Z0-9_-]+)/) 
    || audioUrl.match(/[?&]id=([a-zA-Z0-9_-]+)/);

  if (fileIdMatch && fileIdMatch[1]) {
    const fileId = fileIdMatch[1];
    return `<!-- Audio Player [${trackId}] -->
<div class="audio-player-widget my-3 p-3 rounded-2xl bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 text-white shadow-md border border-slate-800 space-y-2.5" data-audio-track="${trackId}">
  <div class="flex items-center justify-between px-1">
    <div class="flex items-center gap-2.5">
      <div class="w-7 h-7 rounded-lg bg-amber-400 text-slate-950 flex items-center justify-center font-bold text-xs shadow-sm">
        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"/></svg>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-extrabold tracking-wide text-amber-400 uppercase">Track ${trackId}</span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-[10px] font-medium text-slate-400 uppercase tracking-wider">Lesson Audio</span>
        </div>
      </div>
    </div>
    <a href="https://drive.google.com/file/d/${fileId}/view" target="_blank" rel="noopener noreferrer" class="text-[11px] font-semibold text-slate-300 hover:text-white bg-slate-800/90 hover:bg-slate-700/90 border border-slate-700 px-2.5 py-1 rounded-lg transition flex items-center gap-1.5 shadow-2xs">
      <span>Open Drive</span>
      <svg class="w-3 h-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
    </a>
  </div>
  <div class="rounded-xl overflow-hidden border border-slate-800 shadow-inner bg-black/40">
    <iframe src="https://drive.google.com/file/d/${fileId}/preview" width="100%" height="54" class="w-full block" frameborder="0" allow="autoplay"></iframe>
  </div>
</div>
<!-- End Audio Player [${trackId}] -->`;
  }

  // Fallback to native HTML5 audio for standard direct MP3 URLs
  return `<!-- Audio Player [${trackId}] -->
<div class="audio-player-widget my-3 p-3 rounded-2xl bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 text-white shadow-md border border-slate-800 space-y-2.5" data-audio-track="${trackId}">
  <div class="flex items-center justify-between px-1">
    <div class="flex items-center gap-2.5">
      <div class="w-7 h-7 rounded-lg bg-amber-400 text-slate-950 flex items-center justify-center font-bold text-xs shadow-sm">
        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"/></svg>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-extrabold tracking-wide text-amber-400 uppercase">Track ${trackId}</span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="text-[10px] font-medium text-slate-400 uppercase tracking-wider">Lesson Audio</span>
        </div>
      </div>
    </div>
  </div>
  <audio controls preload="none" class="w-full h-8 accent-amber-500 rounded" src="${audioUrl}">
    Your browser does not support the audio element.
  </audio>
</div>
<!-- End Audio Player [${trackId}] -->`;
}

/**
 * Injects or updates an audio player in target files for a track.
 * Places players in all matching exercise/reading locations, skipping overview index cards.
 */
function injectPlayerIntoFiles(trackId, audioUrl, targetFiles) {
  const playerHtml = createPlayerHtml(trackId, audioUrl);
  let updatedFiles = 0;

  for (const relFile of targetFiles) {
    const fullPath = path.join(REPO_DIR, relFile);
    if (!fs.existsSync(fullPath)) continue;

    let content = fs.readFileSync(fullPath, 'utf8');

    // 1. Strip ALL existing player instances for this track to clean up any misplaced players
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

    // Prefer card-level badges (inside exercise/reading cards) over top tab header banners to avoid duplicate players
    const hasCardBadges = rawMatches.some(b => !b.isTabHeader);
    const matches = hasCardBadges ? rawMatches.filter(b => !b.isTabHeader) : rawMatches;

    if (matches.length > 0) {
      // Sort descending by position so insertions don't alter earlier indexes
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
/**
 * Applies all configured tracks from audio-registry.json to files.
 */
function applyAllConfigured(shouldPush = isPush) {
  if (!fs.existsSync(REGISTRY_PATH)) {
    scanTracks();
  }
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
      const commitMsg = `feat: attach lesson audio players (${totalInjected} files)`;
      try {
        execSync(`git commit -m "${commitMsg}"`, { cwd: REPO_DIR, stdio: 'inherit' });
      } catch (e) { /* ignore if clean */ }
      execSync('git push origin main', { cwd: REPO_DIR, stdio: 'inherit' });
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
    log(`  1. ${bold('Scan Lessons')} (Discover all CD audio tracks in files)`);
    log(`  2. ${bold('List Tracks')} (View all tracks & link status)`);
    log(`  3. ${bold('Add / Update Audio Links')} (Add multiple audio links continuously)`);
    log(`  4. ${bold('Remove Audio Link')} (Remove player from files for a track)`);
    log(`  5. ${bold('Apply All Configured Audio')} (Inject players into lesson files)`);
    log(`  6. ${bold('Apply & Push to GitHub')} (Inject players and push changes)`);
    log(`  7. ${bold('Exit')}`);
    log(`${bold(cyan('========================================================================='))}\n`);

    rl.question('Select an option (1-7): ', (choice) => {
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
        applyAllConfigured(false);
        showMenu();
      } else if (trimmed === '6') {
        applyAllConfigured(true);
        showMenu();
      } else if (trimmed === '7' || trimmed.toLowerCase() === 'exit' || trimmed.toLowerCase() === 'q') {
        log('Exiting Audio Track Manager. Goodbye!\n');
        rl.close();
      } else {
        log(yellow('Invalid option. Please enter a number between 1 and 7.'));
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
        // Prompt for next track immediately so user can add many in a row!
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
if (isScan) {
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
