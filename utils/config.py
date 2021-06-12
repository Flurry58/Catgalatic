HOST_CHANNEL = "roles"

# INACCESSIBLE_ROLES = [role_name, role_name, ...]

INACCESSIBLE_ROLES = {"the whats role role", "Admin", "Mods", "Interviewers",
                      "Recruiter", "Hiring Manager", "Bot Creation", "Website Mod", 
                      "Channel Mod", "Dory Team", "Temporary Mute"}

# ROLES = { role_group: { role_name: emote_name, ... }, ... }
# alphabetically order groups to keep correct order

ROLES = {
    'Test': {
      
    },
    'Gender': {
        'Male': '♂️',
        'Female': '♀️',
        'Non-Binary': '⚲',
        'Gender Fluid': '☿️',
        'Trans Gender': '⚧️'
    },
    'seniorities': {
        'Student': '🎓',
        'Intern': '🤓',
        'Junior Developer': '💼',
        'Mid-level Developer': '👔',
        'Senior Developer': '👴'
    },
    'volunteering':{
        # Fixes index out of range due to commands.py call 'role_group = sorted(ROLES.keys())[i]'
    },
    'xtra': {
        'Notifications': '💡',
        'Interview Notifications': '🔔',
        'Military Veteran': 'vet'
    }
}

# EMBEDS = [(title, description), (title, description), ...]

EMBEDS = [
    ("React for Roles with Rolley!",
     ("Add a reaction on the below messages to add a role, remove a reaction to remove the role. "
      "If you already have the role, clicking a reaction will not do anything. "
      "However, if you have the role and react then unreact, your role will be removed. "
      "Click any react on this message to clear all of your self-assignable roles. "
      "If it is unclear what emojis are which, hover over the emoji to see its name.")),
    ("Gender", "Select your gender** Possible roles: {}."
        .format(', '.join(sorted(ROLES['Gender'].keys())))),
    ("Seniority Roles",
     "You are only allowed one seniority role that best reflects where you\'re at in your career. Student = :mortar_board:, Intern = :nerd:, Junior Developer = :briefcase:, "
     "Mid-level Developer = :necktie:, Senior Developer = :older_man:."),
     ("Volunteering",
     "We're always looking for volunteer **Interviewers** to help give mock-interviews. We also have roles reserved for "
     "**Recruiters** and **Hiring Managers**. CSCH is a 501c3 non-profit organization so if you work for a company that has a matching program for volunteer "
     "hours, you'll be able to submit those hours. Please pm a Mod or Admin if you'd like to have these roles assigned."),
    ("Miscellaneous", "These are utility roles, mostly. :bulb: to opt-in to **Global Notifications**, "
     ":bell: to opt-in to **Interview Notifications**, ""**Military Veteran**: for veterans.") 
]
