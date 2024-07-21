from .start import start_router
from .report import report_router
from .help import help_router
from .next import next_router
from .end import end_router
from .stop import stop_router
from .setting import setting_router
from .admin import admin_router
from .echo import echo_router
from .reopen import reopen_router


routers_list =[
    start_router,
    report_router,
    next_router,
    end_router,
    stop_router,
    help_router,
    setting_router,
    admin_router,
    reopen_router,
    echo_router
]