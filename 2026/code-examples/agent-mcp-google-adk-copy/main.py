import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent


async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="weather_app")
    session = await runner.session_service.create_session(
        app_name="weather_app", user_id="user1"
    )

    query = "What's the weather in San Francisco, and the 5-day forecast for London?"
    content = types.Content(role="user", parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id="user1", session_id=session.id, new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"[{event.author}]: {part.text}")


if __name__ == "__main__":
    asyncio.run(main())
