# 

import asyncio


class QABaseEventLoop(asyncio.AbstractEventLoop):
    def __init__(self):
        pass

    @property
    def qa_loop(self):
        try:
            self.get_task_factory