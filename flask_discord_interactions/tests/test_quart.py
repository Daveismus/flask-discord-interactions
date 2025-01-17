import asyncio

import pytest

@pytest.fixture()
def quart_discord():
    import sys
    if "flask" in sys.modules:
        del sys.modules["flask"]

    from quart import Quart
    import quart.flask_patch


    from flask_discord_interactions import DiscordInteractions, Client


    app = Quart(__name__)
    discord = DiscordInteractions(app)
    return discord, Client(discord)


@pytest.mark.asyncio
async def test_async_ping(quart_discord):
    discord, client = quart_discord

    @discord.command()
    async def ping(ctx, pong: str = "pong"):
        "Respond with a friendly 'pong'!"
        return f"Pong {pong}!"

    assert (await client.run("ping")).content == "Pong pong!"


@pytest.mark.asyncio
async def test_await_in_command(quart_discord):
    discord, client = quart_discord

    @discord.command()
    async def wait(ctx):
        await asyncio.sleep(0.01)
        return "Hi!"

    assert (await client.run("wait")).content == "Hi!"

@pytest.mark.asyncio
async def test_mixed_commands(quart_discord):
    discord, client = quart_discord

    @discord.command()
    async def async_command(ctx):
        return "Async"

    @discord.command()
    def not_async_command(ctx):
        return "Not Async"

    assert (await client.run("async_command")).content == "Async"
    assert client.run("not_async_command").content == "Not Async"
