from .commands import register_commands
from .other import register_other
from .subscribes import register_subscribes
from .filters import register_filters

register_functions = (
    register_commands,
    register_other,
    register_subscribes,
    register_filters
)
