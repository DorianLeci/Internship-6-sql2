from enum import Enum
class MatchType(Enum):
    GROUP_STAGE="group_stage"
    ROUND_OF_32="round_of_32"
    ROUND_OF_16="round_of_16"
    QUARTERFINAL="quarterfinal"
    SEMIFINAL="semifinal"
    FINAL="final"
    THIRD_PLACE="third_place"

def generate_match_type(num_of_teams,include_group_stage=True,include_third_place_match=True):

    KNOCKOUT_ORDER = [
    MatchType.GROUP_STAGE,
    MatchType.ROUND_OF_32,
    MatchType.ROUND_OF_16,
    MatchType.QUARTERFINAL,
    MatchType.SEMIFINAL,
    MatchType.FINAL
    ]

    phase_list=[]

    num_teams_after_group_stage=num_of_teams

    if(include_group_stage):
        phase_list.append(MatchType.GROUP_STAGE)
        num_teams_after_group_stage=num_teams_after_group_stage/2

    if num_teams_after_group_stage==32:
        start_phase=(MatchType.ROUND_OF_32)
    
    if num_teams_after_group_stage==16:
        start_phase=(MatchType.ROUND_OF_16)

    if num_teams_after_group_stage==8:
        start_phase=(MatchType.QUARTERFINAL)

    if num_teams_after_group_stage==4:
        start_phase=(MatchType.SEMIFINAL)

    index=KNOCKOUT_ORDER.index(start_phase)
    phase_list.extend(KNOCKOUT_ORDER[index:])

    if (include_third_place_match):
        final_index = phase_list.index(MatchType.FINAL)
        phase_list.insert(final_index,MatchType.THIRD_PLACE)

    return phase_list



    