from dataclasses import dataclass
import asyncio

from autogen_core import (
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
    AgentId,
    SingleThreadedAgentRuntime,
)


# ✅ Message types
@dataclass
class TextMessage:
    content: str

@dataclass
class NumberMessage:
    value: int
    retry_count: int = 0


# ✅ Validator Agent
@default_subscription
class ValidatorAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("Validator Agent")
        self.MAX_RETRIES = 3

    @message_handler
    async def handle_text_message(self, message: TextMessage, ctx: MessageContext) -> None:
        try:
            number = int(message.content)
            print(f"{'-'*80}\nValidator:\nValid number: {number}")
            await self.publish_message(NumberMessage(value=number), DefaultTopicId())
        except ValueError:
            print(f"{'-'*80}\nValidator:\nInvalid input. Not a number -> {message.content}")
            await self.publish_message(TextMessage(content="Invalid input: not a number"), DefaultTopicId())

    @message_handler
    async def handle_number_message(self, message: NumberMessage, ctx: MessageContext) -> None:
        if message.retry_count >= self.MAX_RETRIES:
            print(f"{'-'*80}\nValidator:\nMax retries reached. Sending fallback value 3 to PrimeChecker")
            await self.publish_message(NumberMessage(value=3, retry_count=0), DefaultTopicId())
        else:
            print(f"{'-'*80}\nValidator:\nRetry {message.retry_count}/{self.MAX_RETRIES}. Number: {message.value}")
            await self.publish_message(message, DefaultTopicId())


# ✅ Prime Checker Agent
@default_subscription
class PrimeCheckerAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("Prime Checker Agent")

    @staticmethod
    def is_prime(n: int) -> bool:
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @message_handler
    async def handle_message(self, message: NumberMessage, ctx: MessageContext) -> None:
        if self.is_prime(message.value):
            result = f"Got the prime number: {message.value}"
            print(f"{'-'*80}\nPrimeChecker:\n{result}")
            await self.publish_message(TextMessage(content=result), DefaultTopicId())
        else:
            new_value = message.value - 2
            new_retry = message.retry_count + 1
            print(f"{'-'*80}\nPrimeChecker:\n{message.value} is not prime. Sending {new_value} back to Validator (Retry {new_retry})")
            await self.publish_message(NumberMessage(value=new_value, retry_count=new_retry), DefaultTopicId())


# ✅ Logger Agent
@default_subscription
class LoggerAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("Logger Agent")

    @message_handler
    async def handle_message(self, message: TextMessage, ctx: MessageContext) -> None:
        print(f"{'-'*80}\nLogger:\nFinal Message -> {message.content}")


# ✅ Runtime Setup
runtime = SingleThreadedAgentRuntime()


async def main():
    # Register all agents
    await ValidatorAgent.register(runtime, "validator", lambda: ValidatorAgent())
    await PrimeCheckerAgent.register(runtime, "prime_checker", lambda: PrimeCheckerAgent())
    await LoggerAgent.register(runtime, "logger", lambda: LoggerAgent())

    runtime.start()

    # Example inputs
    print("\nSending: '22'")
    await runtime.send_message(TextMessage(content="22"), AgentId("validator", "default"))

    # print("\nSending: 'hello'")
    # await runtime.send_message(TextMessage(content="hello"), AgentId("validator", "default"))

    # print("\nSending: '9'")
    # await runtime.send_message(TextMessage(content="9"), AgentId("validator", "default"))

    # print("\nSending: '17'")
    # await runtime.send_message(TextMessage(content="17"), AgentId("validator", "default"))

    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(main())
