from systemlogging import log_state_transition
from core.state.ApplicationLayer.Editor.Pause.state import PAUSE_STATE
from core.state.basestatemanager import BaseStateManager

class PauseStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            PAUSE_STATE.ACTIVE: [PAUSE_STATE.PAUSED],
            PAUSE_STATE.PAUSED: [PAUSE_STATE.ACTIVE],
        }
        super().__init__(
            initial_state=PAUSE_STATE.ACTIVE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="PAUSE_STATE",
            type="APPLICATION"
        )
