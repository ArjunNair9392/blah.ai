from livekit import agents
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


class DefaultFunctionClass(agents.llm.FunctionContext):
    @agents.llm.ai_callable(
        description="Called when the conversation with the user is complete. This function ends the interaction "
                    "politely."
    )
    async def end_call(self):
        logger.info("End CALL!!!!")
        return ("Thank you for your time. If you need further assistance, feel free to reach out again. Have a great "
                "day!")

