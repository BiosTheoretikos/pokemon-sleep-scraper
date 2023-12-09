from enum import Enum


class MainSkillEffect(Enum):
    STRENGTH_FIXED = 1
    STRENGTH_RANDOM = 2
    SHARDS_FIXED = 3
    SHARED_RANDOM = 4
    RECOVERY_SELF = 5
    RECOVERY_RANDOM = 6
    RECOVERY_TEAM = 7
    HELP = 8
    INGREDIENT = 9
    POT_CAPACITY = 10
    METRONOME = 12

    def to_type_str(self) -> str:
        return _MAIN_SKILL_EFFECT_TYPE_STR[self]

    def to_target(self) -> str:
        match self:
            case MainSkillEffect.RECOVERY_SELF:
                return "self"
            case MainSkillEffect.RECOVERY_RANDOM:
                return "random"
            case MainSkillEffect.RECOVERY_TEAM:
                return "team"
            case _:
                raise RuntimeError(f"Main skill effect of {self} does not have target")


_MAIN_SKILL_EFFECT_TYPE_STR: dict[MainSkillEffect, str] = {
    MainSkillEffect.STRENGTH_FIXED: "strength",
    MainSkillEffect.STRENGTH_RANDOM: "strength",
    MainSkillEffect.SHARDS_FIXED: "shards",
    MainSkillEffect.SHARED_RANDOM: "shards",
    MainSkillEffect.RECOVERY_SELF: "stamina",
    MainSkillEffect.RECOVERY_RANDOM: "stamina",
    MainSkillEffect.RECOVERY_TEAM: "stamina",
    MainSkillEffect.HELP: "help",
    MainSkillEffect.INGREDIENT: "cooking",
    MainSkillEffect.POT_CAPACITY: "cooking",
    MainSkillEffect.METRONOME: "random",
}
