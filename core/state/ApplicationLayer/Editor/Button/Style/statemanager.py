from systemlogging import log_state_transition
from core.state.ApplicationLayer.Editor.Button.Style.state import BUTTON_STYLE_STATE
from core.state.basestatemanager import BaseStateManager

class ButtonStyleStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            BUTTON_STYLE_STATE.IDLE: [BUTTON_STYLE_STATE.HOVER],
            BUTTON_STYLE_STATE.HOVER: [BUTTON_STYLE_STATE.IDLE],

        }
        super().__init__(
            initial_state=BUTTON_STYLE_STATE.IDLE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="BUTTON_STYLE_STATE",
            type="APPLICATION"
        )
