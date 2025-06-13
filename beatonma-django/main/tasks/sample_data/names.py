import random

# ChatGPT
NAMES = [
    "Alice Adams",
    "Bob Baker",
    "Charlie Chen",
    "David Davis",
    "Emily Evans",
    "Frank Foster",
    "Grace Gomez",
    "Henry Huang",
    "Isabella Irwin",
    "Jack Johnson",
    "Katherine Kim",
    "Liam Lee",
    "Mia Martinez",
    "Nathan Nguyen",
    "Olivia Ortiz",
    "Patrick Parker",
    "Quinn Quinn",
    "Ryan Ramirez",
    "Sophia Smith",
    "Thomas Taylor",
    "Uma Unger",
    "Victoria Vega",
    "William Wong",
    "Xander Xu",
    "Yara Yu",
    "Zachary Zhang",
]

# ChatGPT
USERNAMES = [
    "cyberspacecowboy",
    "code_ninja",
    "pixel_pirate",
    "tech_guru",
    "web_wizard",
    "digital_nomad",
    "geek_chic",
    "cyber_punk",
    "byte_me",
    "net_surfer",
    "tech_savvy",
    "data_diva",
    "pixel_pusher",
    "digital_dreamer",
    "web_weaver",
    "code_crusader",
    "cyber_hero",
    "tech_titan",
    "nerd_goddess",
    "creative_nomad",
    "travel_junkie",
    "music_lover",
    "bookworm",
    "foodie",
    "fitness_fanatic",
    "outdoor_adventurer",
    "animal_lover",
    "coffee_addict",
    "movie_buff",
    "art_enthusiast",
    "history_nerd",
    "fashionista",
    "beauty_guru",
    "yoga_master",
    "sports_fan",
    "thrill_seeker",
    "plant_parent",
    "home_chef",
    "gardening_guru",
    "DIY_diva",
    "poetry_writer",
    "language_learner",
    "spiritual_seeker",
    "philosophy_buff",
]


def any_name():
    return random.choice(NAMES)


def any_username():
    return random.choice(USERNAMES)
