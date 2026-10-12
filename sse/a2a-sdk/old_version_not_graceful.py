# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "a2a-sdk[http-server]==1.2.1",
#     "uvicorn>=0.54.0",
# ]
# ///
import asyncio

import uvicorn
from a2a.helpers import new_task_from_user_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
    TaskState,
)
from starlette.applications import Starlette


class TickAgent(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.current_task:
            task = context.current_task
        else:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        task_updater = TaskUpdater(event_queue, task.id, task.context_id)
        await task_updater.update_status(state=TaskState.TASK_STATE_WORKING)

        for i in range(1, 11):
            await asyncio.sleep(1)
            await task_updater.add_artifact(
                parts=[new_text_part(text=f"Event {i}", media_type="text/plain")],
                artifact_id="result",
                append=i > 1,
                last_chunk=i == 10,
            )

        await task_updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError


skill = AgentSkill(
    id="tick_bot",
    name="Tick Bot",
    description="An example agent that sends ticks",
    input_modes=["text/plain"],
    output_modes=["text/plain"],
)

public_agent_card = AgentCard(
    name="Tick Agent",
    description="Just a simple agent that sends ticks",
    version="0.0.1",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True, extended_agent_card=False),
    supported_interfaces=[
        AgentInterface(
            protocol_binding="JSONRPC",
            url="http://127.0.0.1:9999",
            protocol_version="1.0",
        )
    ],
    skills=[skill],
)

handler = DefaultRequestHandler(
    agent_executor=TickAgent(),
    task_store=InMemoryTaskStore(),
    agent_card=public_agent_card,
)

app = Starlette(
    routes=create_agent_card_routes(public_agent_card)
    + create_jsonrpc_routes(
        request_handler=handler,
        rpc_url="/",
        # shutdown_grace_period=15.0,  # from 1.2.2
    )
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)
