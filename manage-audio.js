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

    // Regex to match badge-cd spans
    const badgeRegex = /class="badge-cd"[^>]*>([^<]+)<\/span>/gi;
    let m;
    while ((m = badgeRegex.exec(content)) !== null) {
      const rawText = m[1].trim();
      const trackMatch = rawText.match(/CD\d+[\s_-]*\d+/gi);
      if (!trackMatch) continue;

      for (const rawTrack of trackMatch) {
        const trackId = rawTrack.toUpperCase().replace(/\s+/g, '-').replace(/_+/g, '-');

        // Extract surrounding context (e.g. exercise heading)
        const snippetStart = Math.max(0, m.index - 300);
        const snippet = content.slice(snippetStart, m.index);
        const headingMatch = snippet.match(/<h[34][^>]*>([^<]+)<\/h[34]>/i) 
          || snippet.match(/<span[^>]*class="[^"]*(?:font-bold|text-xs)[^"]*"[^>]*>([^<]+)<\/span>/i);
        const contextTitle = headingMatch ? headingMatch[1].trim() : `Exercise Track ${trackId}`;

        if (!registry[trackId]) {
          registry[trackId] = {
            trackId: trackId,
            title: contextTitle,
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
 */
function createPlayerHtml(trackId, audioUrl) {
  return `<!-- Audio Player [${trackId}] -->
<div class="audio-player-widget mt-3 mb-3 p-2.5 rounded-2xl bg-amber-500/10 dark:bg-slate-800/80 border border-amber-500/30 flex items-center gap-3 shadow-xs" data-audio-track="${trackId}">
  <div class="w-8 h-8 rounded-xl bg-amber-500 text-slate-900 flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"/></svg>
  </div>
  <div class="flex-grow min-w-0">
    <div class="text-[10px] font-bold text-amber-900 dark:text-amber-300 uppercase tracking-wider mb-1">Audio Track • ${trackId}</div>
    <audio controls preload="none" class="w-full h-8 accent-amber-500 rounded" src="${audioUrl}">
      Your browser does not support the audio element.
    </audio>
  </div>
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

    // 1. If player already exists for this track, update its src
    if (content.includes(`data-audio-track="${trackId}"`)) {
      const existingPlayerRegex = new RegExp(`<!-- Audio Player \\[${trackId}\\] -->[\\s\\S]*?<!-- End Audio Player \\[${trackId}\\] -->\\n?`, 'i');
      if (existingPlayerRegex.test(content)) {
        content = content.replace(existingPlayerRegex, playerHtml);
        backupFile(fullPath);
        fs.writeFileSync(fullPath, content, 'utf8');
        log(`    ${green('✓')} Updated existing player in: ${path.basename(fullPath)}`);
        updatedFiles++;
        continue;
      }
    }

    // 2. Find the badge-cd occurrence for this track and insert player right after its container
    // Search for: <span class="badge-cd">...CDX-XX...</span>
    const escapedTrack = trackId.replace(/[-]/g, '[-_\\s]*');
    const badgeSearchRegex = new RegExp(`(<(?:span|div)[^>]*class="[^"]*badge-cd[^"]*"[^>]*>[^<]*${escapedTrack}[^<]*<\\/(?:span|div)>)`, 'i');
    const match = badgeSearchRegex.exec(content);

    if (match) {
      // Find the closing parent </div> after this badge
      const afterIndex = match.index + match[0].length;
      const nextDivEnd = content.indexOf('</div>', afterIndex);

      if (nextDivEnd !== -1) {
        const insertPos = nextDivEnd + '</div>'.length;
        const newContent = content.slice(0, insertPos) + '\n' + playerHtml + content.slice(insertPos);
        backupFile(fullPath);
        fs.writeFileSync(fullPath, newContent, 'utf8');
        log(`    ${green('✓')} Injected audio player into: ${path.basename(fullPath)}`);
        updatedFiles++;
      } else {
        // Fallback: insert directly after badge
        const insertPos = afterIndex;
        const newContent = content.slice(0, insertPos) + '\n' + playerHtml + content.slice(insertPos);
        backupFile(fullPath);
        fs.writeFileSync(fullPath, newContent, 'utf8');
        log(`    ${green('✓')} Injected audio player after badge in: ${path.basename(fullPath)}`);
        updatedFiles++;
      }
    } else {
      log(`    ${yellow('!')} Could not locate badge for ${trackId} in ${path.basename(fullPath)}`);
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
function applyAllConfigured() {
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

  if (isPush) {
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
 * Interactive Command Line Menu
 */
function interactiveMenu() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  log(`\n${bold(cyan('========================================================================='))}`);
  log(`  ${bold('Grammar Explorer - Audio Track Manager & Drive Integrator')}`);
  log(`${bold(cyan('========================================================================='))}`);
  log(`  1. ${bold('Scan Lessons')} (Discover all CD audio tracks in files)`);
  log(`  2. ${bold('List Tracks')} (View all tracks & link status)`);
  log(`  3. ${bold('Add / Update Audio Link')} (Paste Google Drive or MP3 link for a track)`);
  log(`  4. ${bold('Remove Audio Link')} (Remove player from files for a track)`);
  log(`  5. ${bold('Apply All Configured Audio')} (Inject players into lesson files)`);
  log(`  6. ${bold('Exit')}`);
  log(`${bold(cyan('========================================================================='))}\n`);

  rl.question('Select an option (1-6): ', (choice) => {
    const trimmed = choice.trim();
    if (trimmed === '1') {
      scanTracks();
      rl.close();
    } else if (trimmed === '2') {
      listTracks();
      rl.close();
    } else if (trimmed === '3') {
      rl.question('\nEnter Track ID (e.g. CD1-02, CD1-03): ', (trackId) => {
        rl.question('Paste Google Drive sharing link (or direct MP3 URL): ', (link) => {
          if (trackId && link) {
            setTrackAudio(trackId, link);
          } else {
            log(yellow('Cancelled: Track ID and URL are required.'));
          }
          rl.close();
        });
      });
    } else if (trimmed === '4') {
      rl.question('\nEnter Track ID to remove: ', (trackId) => {
        if (trackId) {
          removeTrackAudio(trackId);
        }
        rl.close();
      });
    } else if (trimmed === '5') {
      applyAllConfigured();
      rl.close();
    } else {
      log('Exiting.');
      rl.close();
    }
  });
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
