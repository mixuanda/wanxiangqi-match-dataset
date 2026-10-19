"""Allowlist a generic research draft. Output stays private and is not anonymous."""
from .validation import PHASES, SUMMARY_KINDS, validate


def number(value):
    if type(value) is int:
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            pass
    return None


def text(value):
    return value if isinstance(value, str) and 0 < len(value) <= 80 else None


def objects(value):
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError('object_list_required_no_silent_record_drops')
    return value


def clean_units(value):
    if value is None:
        return None
    result = []
    for unit in objects(value):
        position = unit.get('position')
        if not isinstance(position, list) or len(position) != 2:
            position = None
        result.append(dict(unit=text(unit.get('unit')), level=number(unit.get('level')),
            quality=number(unit.get('quality')), star=number(unit.get('star')),
            equipment=[text(item) for item in unit.get('equipment', []) if text(item) is not None]
                if isinstance(unit.get('equipment'), list) else None,
            position=[number(x) for x in position] if position is not None else None))
    return result


def normalize_private(document):
    """No source identity, timestamp, free-form metadata or raw payload is copied."""
    if not isinstance(document, dict) or not isinstance(document.get('matches'), list):
        raise ValueError('generic_matches_draft_required_not_a_platform_api_adapter')
    result = dict(schema_version='0.1', origin='private_research', matches=[])
    for match_index, match in enumerate(objects(document['matches'])):
        output = dict(sample_key='local-match-' + str(match_index), mode=text(match.get('mode')),
                      patch=text(match.get('patch')), participants=[])
        for actor_index, actor in enumerate(objects(match.get('participants'))):
            stages = []
            for index, stage in enumerate(objects(actor.get('stages'))):
                summaries = None if stage.get('card_summaries') is None else []
                for summary in objects(stage['card_summaries']) if stage.get('card_summaries') is not None else []:
                    if summary.get('kind') not in SUMMARY_KINDS:
                        raise ValueError('unverified_summary_kind_not_silently_dropped')
                    summaries.append(dict(kind=summary['kind'], card=text(summary.get('card')), count=number(summary.get('count'))))
                source_auction = stage.get('auction')
                auction = None if not isinstance(source_auction, dict) else dict(
                    card=text(source_auction.get('card')), reported_cost_energy=number(source_auction.get('reported_cost_energy')),
                    reported_shared_energy=number(source_auction.get('reported_shared_energy')))
                stages.append(dict(stage_index=index, phase=stage.get('phase') if stage.get('phase') in PHASES else 'unknown',
                    player_level=number(stage.get('player_level')), energy_left=number(stage.get('energy_left')),
                    hero_limit=number(stage.get('hero_limit')), board=clean_units(stage.get('board')),
                    card_summaries=summaries, auction=auction))
            output['participants'].append(dict(actor_key='local-actor-' + str(actor_index),
                selected=actor.get('selected') if type(actor.get('selected')) is bool else None,
                final_rank=number(actor.get('final_rank')), chess_player=text(actor.get('chess_player')),
                final_board=clean_units(actor.get('final_board')), stages=stages))
        result['matches'].append(output)
    validate(result, public=False)
    return result
