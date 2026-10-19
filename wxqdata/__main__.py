"""Offline CLI. No network access or collection command is implemented."""
import argparse
import json
from pathlib import Path

from .cleaning import normalize_private
from .privacy_scan import scan
from .validation import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('validate');check.add_argument('file');check.add_argument('--private', action='store_true')
    clean = sub.add_parser('clean');clean.add_argument('input');clean.add_argument('output')
    audit = sub.add_parser('scan');audit.add_argument('root', nargs='?', default='.');audit.add_argument('--history', action='store_true')
    args = parser.parse_args()
    if args.command == 'scan':
        result = scan(args.root, history=args.history)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'passed' else 1
    if args.command == 'validate':
        validate(json.loads(Path(args.file).read_text(encoding='utf-8')), public=not args.private)
        print('valid_private_draft' if args.private else 'valid_synthetic_public_example')
        return 0
    output = Path(args.output).resolve()
    if '.private' not in output.parts:
        raise ValueError('clean_output_must_stay_in_a_private_directory')
    result = normalize_private(json.loads(Path(args.input).read_text(encoding='utf-8')))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print('private_draft_written_not_approved_for_publication')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
