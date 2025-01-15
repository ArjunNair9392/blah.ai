import asyncio
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, cli, JobProcess
from livekit.agents.llm import ChatContext, ChatMessage
from livekit.agents.voice_assistant import VoiceAssistant
from common.livekit_integration import get_livekit_vad, get_livekit_tts, get_livekit_stt, get_llm
from common.prompts import appointment_setter_prompt
from functions.appointment_setter import AppointmentSettingFunction
from livekit.plugins import silero
from livekit import agents
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


def prewarm_fnc(proc: JobProcess):
    proc.userdata["vad"] = get_livekit_vad()


async def entrypoint(ctx: JobContext):
    await ctx.connect()
    print(f"Connected to room: {ctx.room.name}")
    vad: silero.VAD = ctx.proc.userdata["vad"]
    fnc_str: str = ctx.proc.userdata["fnc_str"]

    # Initialize the chat context
    chat_context = ChatContext(messages=[
        ChatMessage(role="system",
                    content=appointment_setter_prompt)
    ])

    assistant = VoiceAssistant(
        vad=vad,
        stt=get_livekit_stt(),
        tts=get_livekit_tts(),
        llm=get_llm(),
        fnc_ctx=AppointmentSettingFunction(),
        chat_ctx=chat_context,
    )

    async def _process_query(text: str):
        if not text or not isinstance(text, str):
            logger.error("Invalid input text provided to `_process_query`.")
            return

        logger.info(f"Processing query: {text}")
        chat_context.messages.append(ChatMessage(role="user", content=text))

        try:
            stream = get_llm().chat(chat_ctx=chat_context)
            await assistant.say(stream, allow_interruptions=True)
        except Exception as e:
            logger.error(f"Error during LLM chat or TTS: {e}")

    @assistant.on("user_message")
    def handle_user_message_sync(text: str):
        """Handle user messages."""
        asyncio.create_task(_process_query(text))

    assistant.start(ctx.room)

    await assistant.say("Hello! Welcome to XYZ Company. How can I assist you today?", allow_interruptions=True)

    # Keep the room connection alive
    while ctx.room.connection_state == rtc.ConnectionState.CONN_CONNECTED:
        await asyncio.sleep(1)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm_fnc))
