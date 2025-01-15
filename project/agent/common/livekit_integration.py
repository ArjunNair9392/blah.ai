from livekit.plugins import openai, silero


def get_livekit_vad():
    """Return LiveKit Voice Activity Detection instance."""
    return silero.VAD.load()


def get_livekit_stt():
    """Return LiveKit Speech-to-Text instance."""
    return openai.STT()


def get_livekit_tts():
    """Return LiveKit Text-to-Speech instance."""
    return openai.TTS(voice="alloy")


def get_llm():
    """Return LiveKit Text-to-Speech instance."""
    return openai.LLM(model="gpt-4o-mini")
