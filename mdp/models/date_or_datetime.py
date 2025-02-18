import dataclasses

from mdp.models.type_agnostic import BaseProfile
from mdp.primitives import OptionalDateOrDateTime


@dataclasses.dataclass
class DateOrDateTimeProfile(BaseProfile):
    min: OptionalDateOrDateTime
    max: OptionalDateOrDateTime
