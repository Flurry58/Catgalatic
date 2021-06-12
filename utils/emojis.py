from utils.config import ROLES


def get_emoji_from_reaction(reaction):
    emoji = reaction.emoji
    if reaction.custom_emoji:
        emoji = reaction.emoji.name
    return emoji


def is_clearing_emoji(emoji):
    clearing_emojis = ROLES["clears"].values()
    return emoji in clearing_emojis


def get_all_listed_emojis():
    all_emojis = []
    for group, pair in ROLES.items():
        all_emojis += pair.values()
    return set(all_emojis)


def is_listed_emoji(emoji):
    all_emojis = get_all_listed_emojis()
    return emoji in all_emojis
