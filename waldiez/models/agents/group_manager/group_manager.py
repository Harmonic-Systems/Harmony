"""Group chat manager agent."""

from typing import List, Literal

from pydantic import Field
from typing_extensions import Annotated

from ..agent import HarmonyAgent
from .group_manager_data import HarmonyGroupManagerData
from .speakers import HarmonyGroupManagerSpeakers


class HarmonyGroupManager(HarmonyAgent):
    """Group chat manager agent.

    A `HarmonyAgent` with agent_type `manager`, `human_input_mode`: `"NEVER"`
    and chat group related config for the agent.
    Also see `HarmonyAgent`, `HarmonyGroupManagerData`, `HarmonyAgentData`

    Attributes
    ----------
    agent_type : Literal["manager"]
        The agent type: 'manager' for a group manager agent
    data : HarmonyGroupManagerData
        The group manager agent's data.

    Functions
    ---------
    validate_transitions(agent_ids: List[str])
        Validate the transitions.
    """

    agent_type: Annotated[
        Literal["manager"],
        Field(
            "manager",
            title="Agent type",
            description="The agent type: 'manager' for a group manager agent",
            alias="agentType",
        ),
    ]
    data: Annotated[
        HarmonyGroupManagerData,
        Field(
            title="Data",
            description="The group manager agent's data",
            default_factory=HarmonyGroupManagerData,
        ),
    ]

    def validate_transitions(self, agent_ids: List[str]) -> None:
        """Validate the transitions.

        If the selection mode is `transition`:

        - if `allow_repeat` is a list of agent_ids,
                make sure these ids exist.
        - make sure the `allowed_or_disallowed_transitions` mapping
                has valid agent ids.

        Parameters
        ----------
        agent_ids : List[str]
            The list of agent IDs.

        Raises
        ------
        ValueError
            If the transitions are invalid.
        """
        speakers: HarmonyGroupManagerSpeakers = self.data.speakers
        if speakers.selection_mode != "transition":
            return
        allow_repeat = speakers.allow_repeat
        if isinstance(allow_repeat, list):
            for agent_id in allow_repeat:
                if agent_id not in agent_ids:
                    raise ValueError(f"Invalid agent id: {agent_id}")
        for (
            agent_id,
            transitions,
        ) in speakers.allowed_or_disallowed_transitions.items():
            if agent_id not in agent_ids:
                raise ValueError(f"Invalid agent id: {agent_id}")
            for agent_id in transitions:
                if agent_id not in agent_ids:
                    raise ValueError(f"Invalid agent id: {agent_id}")
