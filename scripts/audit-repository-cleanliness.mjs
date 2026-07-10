import { spawnSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = process.cwd();
const ignoredDirs = new Set(['.git', 'node_modules', '.astro', 'dist']);
const textExtensions = new Set([
  '.astro', '.css', '.csv', '.html', '.js', '.json', '.md', '.mjs', '.py', '.txt', '.xml', '.yml', '.yaml'
]);

const issues = [];
const gitFiles = spawnSync('git', ['ls-files', '--cached', '--others', '--exclude-standard'], {
  cwd: root,
  encoding: 'utf8'
});

if (gitFiles.status !== 0) {
  throw new Error(`Could not list repository files: ${gitFiles.stderr || gitFiles.stdout}`);
}

const addIssue = (type, file, detail = '') => {
  issues.push({ type, file: file ? relative(root, file) : '', detail });
};

const extensionOf = (file) => {
  const match = file.match(/(\.[^.\/]+)$/);
  return match ? match[1].toLowerCase() : '';
};

const walk = (dir, visitor) => {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (ignoredDirs.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      visitor(full, entry);
      walk(full, visitor);
    } else {
      visitor(full, entry);
    }
  }
};

for (const rel of gitFiles.stdout.split(/\r?\n/).filter(Boolean)) {
  const file = join(root, rel);
  if (!existsSync(file) || !statSync(file).isFile()) continue;
  const name = rel.split('/').pop() || rel;
  if (
    name === '.DS_Store' ||
    name.endsWith('~') ||
    name.endsWith('.bak') ||
    name.endsWith('.backup') ||
    name.endsWith('.log')
  ) {
    addIssue('temporary_file', file);
  }

  if (textExtensions.has(extensionOf(name))) {
    const content = readFileSync(file, 'utf8');
    if (/^(<<<<<<<|=======|>>>>>>>)($| )/m.test(content)) {
      addIssue('merge_conflict_marker', file);
    }
    if (/dev\.maatschappijkunde\.nl/i.test(content)) {
      addIssue('dev_origin_reference', file);
    }
  }

  if (rel.startsWith('public/wp-') && !rel.startsWith('public/wp-content/uploads/')) {
    addIssue('unexpected_wordpress_public_path', file);
  }
}

for (const configPath of ['public/.htaccess', 'dist/.htaccess']) {
  const full = join(root, configPath);
  if (existsSync(full)) addIssue('public_htaccess', full);
}

if (existsSync(join(root, 'dist'))) {
  walk(join(root, 'dist'), (file, entry) => {
    const rel = relative(root, file);
    if (entry.isFile() && extensionOf(entry.name) === '.php') {
      addIssue('php_file_in_dist', file);
    }
    if (entry.isFile() && textExtensions.has(extensionOf(entry.name))) {
      const content = readFileSync(file, 'utf8');
      if (/<\?php/i.test(content) || /\.php(?:["'?#/]|$)/i.test(content)) {
        addIssue('php_reference_in_dist', file);
      }
      if (/\[(?:vc_|fusion_|gt_table|shortcode|wpdreams_|uhe_style1)[^\]]*\]/i.test(content)) {
        addIssue('unresolved_wordpress_shortcode_in_dist', file);
      }
      if (/wp-(?:admin|includes|login|config)\b/i.test(content)) {
        addIssue('wordpress_runtime_reference_in_dist', file);
      }
    }
    if (entry.isFile() && rel.startsWith('dist/wp-') && !rel.startsWith('dist/wp-content/uploads/')) {
      addIssue('unexpected_wordpress_dist_path', file);
    }
  });
}

if (existsSync(join(root, 'public', 'wp-content', 'uploads'))) {
  walk(join(root, 'public', 'wp-content', 'uploads'), (file, entry) => {
    if (!entry.isFile()) return;
    const ext = extensionOf(entry.name);
    if (ext === '.php' || statSync(file).isDirectory()) {
      addIssue('unsafe_legacy_upload_asset', file);
    }
  });
}

if (issues.length) {
  console.error(JSON.stringify({ total_issues: issues.length, issues }, null, 2));
  throw new Error(`Repository cleanliness audit found ${issues.length} issue(s).`);
}

console.log('Repository cleanliness ok');
