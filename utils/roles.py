import discord
from utils.config import ROLES, INACCESSIBLE_ROLES
from discord.utils import get
from utils.emojis import get_emoji_from_reaction


def get_role_from_reaction(reaction):
    """ Return role paired with reaction """

    emoji = get_emoji_from_reaction(reaction);

    for subgroup in ROLES.values():
        for r, e in subgroup.items():
            if e == emoji:
                return r
    return None


def user_has_role(user, role):
    for r in user.roles:
        if r.name == role or r == role:
            return True
    return False


def user_has_single_use_category(user, *categories):
    """ Check if user already has a role in
        categories where they can only have one
    """

    for category in categories:
        for role_name in category:
            if user_has_role(user, role_name):
                return True
        return False


def is_valid_role(user, role):
    """ Check if role exists and is a server role """

    for r in user.server.roles:
        if r.name == role:
            return True
    return False


def is_accessible_role(role):
    """ Check if role is accessible """

    return role not in INACCESSIBLE_ROLES


async def add_role(client, user, role):
    """ Add a role to a user and sends message notification
        Allows for only one seniority role
    """

    seniority_roles = ROLES["seniorities"].keys()
    if not is_valid_role(user, role) or user_has_role(user, role) \
            or (user_has_single_use_category(user, seniority_roles)
                and role in seniority_roles):
        return

    try:
        role_to_add = get(user.server.roles, name=role)
        await client.add_roles(user, role_to_add)
        await client.send_message(user, "Added **{}** to active roles in _CS Career Hackers_".format(role_to_add))
    except discord.Forbidden:
        await client.send_message(user, "Please give bot `Manage Role` permissions or notify an admin")
        return


async def remove_role(bot, user, role):
    """ Removes a role from a user """

    if not is_valid_role(user, role) or not user_has_role(user, role):
        return

    all_user_roles = user.roles
    for r in all_user_roles:
        if r.name == role:
            try:
                await client.remove_roles(user, r)
                await client.send_message(user, "Removed **{}** from active roles in _CS Career Hackers_".format(r))
            except discord.Forbidden:
                await client.send_message(user, "Please give bot Manage Role permissions or notify an admin")
                return


async def remove_all_roles(bot, user):
    """ Removes all self-assignable roles from user """

    all_user_roles = user.roles
    roles_to_remove = []
    for r in all_user_roles:
        if is_accessible_role(r.name):
            roles_to_remove.append(r)
    await client.remove_roles(user, *roles_to_remove)
