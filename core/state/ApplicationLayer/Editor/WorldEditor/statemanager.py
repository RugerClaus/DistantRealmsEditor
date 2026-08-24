from systemlogging import log_state_transition
from core.state.ApplicationLayer.Editor.WorldEditor.state import WORLD_EDITOR_STATE
from core.state.basestatemanager import BaseStateManager

class WorldEditorStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            WORLD_EDITOR_STATE.MAP: [WORLD_EDITOR_STATE.WORLD],
            WORLD_EDITOR_STATE.WORLD: [WORLD_EDITOR_STATE.MAP],
        }
        super().__init__(
            initial_state=WORLD_EDITOR_STATE.WORLD,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="WORLD_EDITOR_STATE",
            type="APPLICATION"
        )
