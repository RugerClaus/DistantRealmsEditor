from systemlogging import log_state_transition
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.state.basestatemanager import BaseStateManager

class EditorStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            EDITOR_STATE.NONE: [EDITOR_STATE.FORM,EDITOR_STATE.MENU],
            EDITOR_STATE.FORM: [EDITOR_STATE.NONE],
            EDITOR_STATE.MENU: [EDITOR_STATE.NONE]
        }
        super().__init__(
            initial_state=EDITOR_STATE.NONE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="EDITOR_STATE.NONE",
            type="APPLICATION"
        )
