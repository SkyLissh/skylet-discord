from datetime import datetime
from typing import Any, Union

from discord import ClientUser, Embed, Member
from discord.ext import commands as cmd
from typing_extensions import ParamSpec

from app.models import Game, Stream, User
from app.utils.arguments_help import argument_help
from app.utils.format_number import format_number

P = ParamSpec("P")


def stream_embed(*, stream: Stream, user: User, game: Game) -> Embed:
    embed = Embed(colour=0x6441A4)

    embed.set_author(
        name=f"{stream.user_name} is live on Twitch",
        url=stream.url,
        icon_url=user.profile_image_url,
    )
    embed.title = stream.title

    embed.url = stream.url
    embed.set_image(url=stream.thumbnail_url)
    embed.set_thumbnail(url=game.box_art_url)

    embed.add_field(name=":video_game: Playing", value=stream.game_name)
    embed.add_field(name=":eyes: Viewers", value=stream.viewer_count)

    embed.set_footer(text="SkyLet")
    embed.timestamp = stream.started_at

    return embed


def user_embed(user: User, follows: int) -> Embed:
    followers: str = format_number(follows)

    embed = Embed(colour=0x6441A4)

    embed.title = f"{user.display_name} is on Twitch"
    embed.url = f"https://twitch.tv/{user.login}"

    embed.description = user.description
    embed.set_thumbnail(url=user.profile_image_url)

    embed.add_field(name=":busts_in_silhouette: Followers", value=followers)
    embed.add_field(name=":eyes: Views", value=user.view_count)

    embed.set_footer(text="Created at")
    embed.timestamp = user.created_at

    return embed


def info_embed(message: str) -> Embed:
    embed = Embed(colour=0x6441A4)
    embed.description = f":information_source: Info: {message}"

    return embed


def error_embed(message: str) -> Embed:
    embed = Embed(color=0xF54545)
    embed.description = f":x: Error: {message}"

    return embed


def mute_embed(
    *,
    user: Member,
    moderator: Union[Member, ClientUser],
    reason: str,
) -> Embed:
    embed = Embed(colour=0x6441A4)

    embed.set_author(
        name=f"{user.display_name} has been muted", icon_url=user.display_avatar.url
    )
    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name=":bust_in_silhouette: User",
        value=f"{user.mention} ({user.display_name})",
    )
    embed.add_field(
        name=":name_badge: Moderator",
        value=f"{moderator.mention} ({moderator.display_name})",
    )
    embed.add_field(name=":speech_balloon: Reason", value=reason, inline=False)

    embed.set_footer(text="SkyLet")
    embed.timestamp = datetime.utcnow()

    return embed


def invalid_command_embed(command: cmd.Command[cmd.Cog, P, Any]) -> Embed:
    embed = Embed(colour=0xF54545)
    params = [f"`[{name}]`" for name in command.params.keys()]

    embed.set_author(name="Invalid command usage, try using it like this:")
    embed.description = f"{command.name} {' '.join(params)}"

    embed.add_field(name=":blue_book: Arguments", value=argument_help(command.params))

    return embed
