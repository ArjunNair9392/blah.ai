import asyncio
from typing import Annotated
import re
import os
import requests
from livekit import agents
import logging

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)


class AssistantFunction(agents.llm.FunctionContext):
    """This class defines functions that the assistant will call."""

    @agents.llm.ai_callable(
        description="Called when a user wants to book an appointment. This function sends a booking link to the "
                    "provided email address and name."
    )
    async def book_appointment(
        self,
        email: Annotated[
            str,
            agents.llm.TypeInfo(
                description="The email address to send the booking link to"
            ),
        ],
        name: Annotated[
            str,
            agents.llm.TypeInfo(
                description="The name of the person booking the appointment"
            ),
        ],
    ):
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "The email address seems incorrect. Please provide a valid one."

        return f"Appointment booking link sent to {email}. Please check your email {name}."

    async def check_appointment_status(
        self,
        email: str,
    ):
        """Check if a user has booked an appointment based on their email."""
        print("calling check function")
        return "The user has not yet booked an appointment. Please offer him help"

