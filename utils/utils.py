from utils.config import HOST_CHANNEL

def is_mod_or_admin(author):
    perms = author.server_permissions
    return perms.manage_roles or perms.administrator

def should_ignore(client, channel, user):
    if user == client.user:
        return True

    if channel.name != HOST_CHANNEL:
        return True
    
    return False
