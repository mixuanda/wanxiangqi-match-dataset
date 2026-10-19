import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from wxqdata.cleaning import normalize_private
from wxqdata.privacy_scan import inspect_text, scan
from wxqdata.validation import validate

ROOT = Path(__file__).resolve().parents[1]


class DataContracts(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ROOT/'examples'/'synthetic.json').read_text(encoding='utf-8'))

    def test_synthetic_public_example(self):
        self.assertTrue(validate(self.document))

    def test_private_normalization_forces_private_origin(self):
        result = normalize_private(self.document)
        self.assertEqual(result['origin'], 'private_research')
        with self.assertRaisesRegex(ValueError, 'publication_disabled'):
            validate(result)

    def test_identity_and_free_text_removed_at_all_levels(self):
        document = copy.deepcopy(self.document)
        match = document['matches'][0];actor = match['participants'][0]
        document['token'] = 'private-placeholder'
        match.update(source_match_id='private-placeholder', timestamp='private-placeholder', url='private-placeholder')
        actor.update(account_id='private-placeholder', nickname='private-placeholder', avatar='private-placeholder')
        actor['stages'][0]['raw_payload'] = {'account_id':'private-placeholder'}
        result = normalize_private(document)
        self.assertNotIn('private-placeholder', json.dumps(result))
        self.assertEqual(result['matches'][0]['sample_key'], 'local-match-0')

    def test_nested_unknown_field_public_rejected(self):
        self.document['matches'][0]['participants'][0]['stages'][0]['board'][0]['note'] = 'extra'
        with self.assertRaisesRegex(ValueError, 'invalid_fields:unit'):
            validate(self.document)

    def test_missing_star_not_derived_from_level(self):
        unit = self.document['matches'][0]['participants'][0]['final_board'][0]
        unit.pop('star');unit['level'] = 250
        result = normalize_private(self.document)
        self.assertIsNone(result['matches'][0]['participants'][0]['final_board'][0]['star'])

    def test_unknown_board_is_not_empty_board(self):
        self.document['matches'][0]['participants'][0]['stages'][0]['board'] = None
        result = normalize_private(self.document)
        self.assertIsNone(result['matches'][0]['participants'][0]['stages'][0]['board'])

    def test_negative_energy_preserved(self):
        self.document['matches'][0]['participants'][0]['stages'][0]['energy_left'] = -2
        result = normalize_private(self.document)
        self.assertEqual(result['matches'][0]['participants'][0]['stages'][0]['energy_left'], -2)

    def test_acquisition_not_relabelled_as_purchase(self):
        result = normalize_private(self.document)
        event = result['matches'][0]['participants'][0]['stages'][0]['card_summaries'][0]
        self.assertEqual(event['kind'], 'acquired_summary')
        self.assertNotIn('cost', event)
        self.assertNotIn('timestamp', event)

    def test_timestamps_and_real_labels_not_public(self):
        self.document['matches'][0]['mode'] = 'real-record-placeholder'
        with self.assertRaisesRegex(ValueError, 'synthetic_toy_label'):
            validate(self.document)

    def test_malformed_records_do_not_disappear_silently(self):
        self.document['matches'].append('not an object')
        with self.assertRaisesRegex(ValueError, 'no_silent_record_drops'):
            normalize_private(self.document)

    def test_boolean_is_not_integer_count(self):
        self.document['matches'][0]['participants'][0]['stages'][0]['card_summaries'][0]['count'] = True
        with self.assertRaisesRegex(ValueError, 'integer_or_null'):
            validate(self.document)

    def test_unverified_action_kind_not_silently_dropped(self):
        self.document['matches'][0]['participants'][0]['stages'][0]['card_summaries'][0]['kind'] = 'purchase'
        with self.assertRaisesRegex(ValueError, 'unverified_summary_kind'):
            normalize_private(self.document)


class ReleaseChecks(unittest.TestCase):
    def test_credential_pattern(self):
        fake = 'ghp_' + 'A' * 36
        self.assertIn('github_credential', inspect_text(fake))

    def test_history_checks_removed_secret_and_unapproved_archive(self):
        with tempfile.TemporaryDirectory(prefix='.synthetic-test-', dir=ROOT/'tests') as directory:
            root = Path(directory).resolve()
            self.assertEqual(root.parent, (ROOT/'tests').resolve())
            self.assertTrue(root.name.startswith('.synthetic-test-'))
            (root/'examples').mkdir()
            (root/'examples'/'synthetic.json').write_text((ROOT/'examples'/'synthetic.json').read_text(), encoding='utf-8')
            (root/'PUBLISH_FILES.json').write_text(json.dumps({'files':['PUBLISH_FILES.json','examples/synthetic.json']}), encoding='utf-8')
            def git(*args):
                subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            git('init','-b','main')
            git('config','user.name','Dataset Research Contributors')
            git('config','user.email','contributors@users.noreply.github.com')
            (root/'removed.txt').write_text('ghp_' + 'A' * 36, encoding='utf-8')
            git('add','.');git('commit','-m','Synthetic rejection fixture')
            (root/'removed.txt').unlink()
            git('add','-u');git('commit','-m','Remove fixture')
            (root/'blocked.zip').write_bytes(b'not a real archive')
            result = scan(root, history=True)
            kinds = {finding['kind'] for finding in result['findings']}
            self.assertIn('history_github_credential', kinds)
            self.assertIn('archive_or_database_forbidden', kinds)
            self.assertEqual(result['reachable_commits'], 2)


if __name__ == '__main__':
    unittest.main()
