from typing import TypedDict, List, Literal, Union, NotRequired
from .event_utils import ProducibleKeyEvent, ConsumableKeyEvent


class Condition(TypedDict):
    type: Literal["variable_if"]
    name: str
    value: str


class SetVariableContent(TypedDict):
    name: str
    value: str


class SetVariable(TypedDict):
    set_variable: SetVariableContent


class ToDelayedAction(TypedDict):
    to_if_invoked: NotRequired[List[SetVariable]]
    to_if_canceled: NotRequired[List[SetVariable]]


# from is a reserved keyword so using this workaround
FromWorkaround = TypedDict("From", {"from": ConsumableKeyEvent})


class Manipulation(FromWorkaround):
    type: Literal["basic"]
    conditions: NotRequired[List[Condition]]
    # See FromWorkaround, there is this field here
    # from: List[ConsumableKeyEvent]
    to: List[Union[ProducibleKeyEvent, SetVariable]]
    to_delayed_action: NotRequired[ToDelayedAction]


class Modification(TypedDict):
    description: str
    manipulators: List[Manipulation]
