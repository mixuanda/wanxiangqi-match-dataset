"""Strict field and value allowlists. A source label is not proof of anonymity."""
import re

FIELDS = {
    'dataset': {'schema_version', 'origin', 'matches'},
    'match': {'sample_key', 'mode', 'patch', 'participants'},
    'participant': {'actor_key', 'selected', 'final_rank', 'chess_player', 'final_board', 'stages'},
    'stage': {'stage_index', 'phase', 'player_level', 'energy_left', 'hero_limit', 'board', 'card_summaries', 'auction'},
    'unit': {'unit', 'level', 'quality', 'star', 'equipment', 'position'},
    'summary': {'kind', 'card', 'count'},
    'auction': {'card', 'reported_cost_energy', 'reported_shared_energy'},
}
PHASES = {'combat_snapshot', 'auction_snapshot', 'unknown'}
SUMMARY_KINDS = {'acquired_summary', 'used_summary', 'removed_summary'}
TOY = re.compile(r'toy-[a-z]+(?:-[a-z]+)*\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, kind):
    require(isinstance(value, dict) and set(value) == FIELDS[kind], 'invalid_fields:' + kind)


def integer(value, *, minimum=None):
    require(value is None or type(value) is int, 'integer_or_null_required')
    require(value is None or minimum is None or value >= minimum, 'integer_out_of_range')


def label(value, *, public):
    require(value is None or isinstance(value, str) and 0 < len(value) <= 80, 'bounded_label_or_null_required')
    if public and value is not None:
        require(TOY.fullmatch(value) is not None, 'synthetic_toy_label_required')


def units(value, *, public):
    if value is None:
        return
    require(isinstance(value, list) and len(value) <= 64, 'bounded_unit_list_required')
    for unit in value:
        fields(unit, 'unit')
        label(unit['unit'], public=public)
        for name in ['level', 'quality', 'star']:
            integer(unit[name], minimum=0)
        require(unit['equipment'] is None or isinstance(unit['equipment'], list), 'equipment_list_or_null_required')
        for equipment in unit['equipment'] or []:
            label(equipment, public=public)
        position = unit['position']
        require(position is None or isinstance(position, list) and len(position) == 2, 'position_pair_or_null_required')
        for coordinate in position or []:
            integer(coordinate)


def validate(document, *, public=True):
    fields(document, 'dataset')
    require(document['schema_version'] == '0.1', 'unsupported_schema')
    require(document['origin'] in {'synthetic', 'private_research'}, 'explicit_origin_required')
    if public:
        require(document['origin'] == 'synthetic', 'real_record_publication_disabled')
    require(isinstance(document['matches'], list) and len(document['matches']) <= 5000, 'bounded_match_list_required')
    seen = set()
    for match in document['matches']:
        fields(match, 'match')
        require(isinstance(match['sample_key'], str), 'sample_key_required')
        require(match['sample_key'] not in seen, 'duplicate_sample_key')
        seen.add(match['sample_key'])
        for name in ['sample_key', 'mode', 'patch']:
            label(match[name], public=public)
        if public:
            require(match['patch'] is None, 'synthetic_patch_must_be_unknown')
        require(isinstance(match['participants'], list) and len(match['participants']) <= 16, 'bounded_participant_list_required')
        actors = set()
        for actor in match['participants']:
            fields(actor, 'participant')
            require(isinstance(actor['actor_key'], str) and actor['actor_key'] not in actors, 'unique_local_actor_required')
            actors.add(actor['actor_key'])
            label(actor['actor_key'], public=public)
            label(actor['chess_player'], public=public)
            require(actor['selected'] is None or type(actor['selected']) is bool, 'selection_boolean_or_null_required')
            integer(actor['final_rank'], minimum=1)
            units(actor['final_board'], public=public)
            require(isinstance(actor['stages'], list) and len(actor['stages']) <= 256, 'bounded_stage_list_required')
            previous = -1
            for stage in actor['stages']:
                fields(stage, 'stage')
                require(type(stage['stage_index']) is int and stage['stage_index'] > previous, 'stage_indices_must_increase')
                previous = stage['stage_index']
                require(stage['phase'] in PHASES, 'explicit_phase_required')
                for name in ['player_level', 'hero_limit']:
                    integer(stage[name], minimum=0)
                integer(stage['energy_left'])  # Negative reported values are not silently clipped.
                units(stage['board'], public=public)
                require(stage['card_summaries'] is None or isinstance(stage['card_summaries'], list), 'summary_list_or_null_required')
                for summary in stage['card_summaries'] or []:
                    fields(summary, 'summary')
                    require(summary['kind'] in SUMMARY_KINDS, 'summary_is_not_an_input_action')
                    label(summary['card'], public=public)
                    integer(summary['count'], minimum=0)
                auction = stage['auction']
                if auction is not None:
                    fields(auction, 'auction')
                    label(auction['card'], public=public)
                    integer(auction['reported_cost_energy'])
                    integer(auction['reported_shared_energy'])
    return True
