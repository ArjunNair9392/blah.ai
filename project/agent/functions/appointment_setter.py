import re
import requests
from dotenv import load_dotenv
from livekit import agents
import logging
from typing import Annotated, Optional, List, Tuple
from datetime import datetime

logger = logging.getLogger("temperature-control")
logger.setLevel(logging.INFO)

load_dotenv()


class AppointmentSettingFunction(agents.llm.FunctionContext):
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
        print("book_appointment!!!!!!!!!!!!!!", name, email)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "The email address seems incorrect. Please provide a valid one."

        try:
            return f"Appointment booking link sent to {email}. Please check your email, {name}"
        except requests.RequestException as e:
            print(f"Error booking appointment: {e}")
            return "There was an error booking your appointment. Please try again later."

    @agents.llm.ai_callable(
        description="This function checks for available appointment slots. Provide the service name "
    )
    def check_appointment_availability(
            self,
            service: Annotated[
                str,
                agents.llm.TypeInfo(
                    description="The service name of the service the user wants from this company"
                ),
            ],
    ):
        print("check_appointment_availability", service)
        available_slots = True

        if available_slots:
            return "Yes, we have availability within your requested timeframe."
        else:
            return "No available slots found. Try another time range."

    @agents.llm.ai_callable(
        description="Called when the conversation with the user is complete. This function ends the interaction "
                    "politely."
    )
    async def end_call(self):
        print("End CALL!!!!")
        return ("Thank you for your time. If you need further assistance, feel free to reach out again. Have a great "
                "day!")
