"""Fail-closed release inventory and text checks, including every reachable Git blob."""
import json
from pathlib import Path
import re
import subprocess

PATTERNS = {
    'long_numeric_identifier': re.compile(r'(?<![0-9])[0-9]{12,}(?![0-9])'),
    'precise_timestamp': re.compile(r'\b[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}'),
    'absolute_user_path': re.compile(r'[A-Za-z]:[\\/](?:Users|Documents)[\\/]|/(?:Users|home)/[A-Za-z]'),
    'library_reference': re.compile(r'libfile_[a-z0-9]+'),
    'github_credential': re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}'),
    'bearer_credential': re.compile(r'Bearer\s+[A-Za-z0-9._~+/-]{16,}'),
    'jwt': re.compile(r'eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}'),
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'source_pseudonym': re.compile(r'\bp_[a-f0-9]{24}\b'),
}
ARCHIVES = {'.zip', '.gz', '.tar', '.7z', '.rar', '.db', '.sqlite', '.sqlite3'}


def inspect_text(text):
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def git(root, *args, check=True):
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=check)


def scan(root, *, history=False):
    root = Path(root).resolve()
    allowed = set(json.loads((root/'PUBLISH_FILES.json').read_text(encoding='utf-8'))['files'])
    findings = []
    count = 0
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if rel == '.git' or rel.startswith('.git/'):
            continue
        if path.is_symlink():
            findings.append(dict(path=rel, kind='symlink_not_allowed'))
            continue
        if not path.is_file():
            continue
        count += 1
        if rel not in allowed:
            findings.append(dict(path=rel, kind='not_in_release_allowlist'))
        if path.suffix.lower() in ARCHIVES:
            findings.append(dict(path=rel, kind='archive_or_database_forbidden'))
        if path.stat().st_size > 512*1024:
            findings.append(dict(path=rel, kind='oversize_file'))
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            findings.append(dict(path=rel, kind='non_utf8_file'))
            continue
        findings.extend(dict(path=rel, kind=kind) for kind in inspect_text(rel+'\n'+text))
    missing = sorted(allowed - {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()})
    findings.extend(dict(path=path, kind='allowlisted_file_missing') for path in missing)
    blob_count = commit_count = 0
    if history:
        head = git(root, 'rev-parse', '--verify', 'HEAD', check=False)
        if head.returncode != 0:
            findings.append(dict(path='git', kind='history_has_no_commit_to_audit'))
        else:
            objects = git(root, 'rev-list', '--objects', '--all').stdout.decode('utf-8').splitlines()
            for line in objects:
                oid, _, rel = line.partition(' ')
                kind = git(root, 'cat-file', '-t', oid).stdout.strip()
                if kind != b'blob':
                    continue
                blob_count += 1
                data = git(root, 'cat-file', 'blob', oid).stdout
                if rel not in allowed or Path(rel).suffix.lower() in ARCHIVES:
                    findings.append(dict(path=rel, kind='history_unapproved_file'))
                try:
                    text = data.decode('utf-8')
                except UnicodeError:
                    findings.append(dict(path=rel, kind='history_binary_blob'))
                    continue
                findings.extend(dict(path=rel, kind='history_'+kind) for kind in inspect_text(rel+'\n'+text))
            log = git(root, 'log', '--all', '--format=%B%n%an <%ae>%n%cn <%ce>').stdout.decode('utf-8')
            findings.extend(dict(path='git_commit_metadata', kind=kind) for kind in inspect_text(log))
            commit_count = len(git(root, 'rev-list', '--all').stdout.splitlines())
    from .validation import validate
    try:
        validate(json.loads((root/'examples'/'synthetic.json').read_text(encoding='utf-8')), public=True)
    except (ValueError, OSError) as error:
        findings.append(dict(path='examples/synthetic.json', kind='public_schema_invalid', detail=type(error).__name__))
    return dict(status='passed' if not findings else 'failed', files_checked=count, history_requested=history,
                reachable_commits=commit_count, reachable_blobs=blob_count, findings=findings,
                limitation='Pattern scans are not proof of anonymity. Real-record publication remains disabled.')
