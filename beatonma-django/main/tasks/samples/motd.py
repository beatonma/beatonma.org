import random
from dataclasses import dataclass
from typing import Optional

TITLES = [
    "Embrace Positivity",
    "Practice Gratitude",
    "Embrace Change",
    "Kindness Matters",
    "Set Meaningful Goals",
    "Take Care of Yourself",
    "Face Challenges Boldly",
    "Spread Love and Joy",
    "Embrace Failure as Learning",
    "Stay Curious",
] + ([None] * 10)

CONTENTS = [
    "Start your day with a positive mindset and watch how it transforms your experiences.",
    "Take a moment to appreciate the little things in life that bring you joy and fulfillment.",
    "Change is the only constant. Embrace it as an opportunity for growth and learning.",
    "A small act of kindness can brighten someone's day and create a ripple of positivity.",
    "Define clear and achievable goals that give your life purpose and direction.",
    "Self-care is essential for your well-being. Remember to rest, recharge, and prioritize yourself.",
    "Challenges are opportunities in disguise. Face them with courage and determination.",
    "Share love and joy with others, as these emotions have the power to create a harmonious world.",
    "Failure is not the end; it's a stepping stone on the path to success. Learn from it.",
    "Curiosity fuels intellectual and personal growth. Keep asking questions and seeking knowledge.",
]


@dataclass
class SampleMotd:
    title: Optional[str]
    content: str


def any_title() -> Optional[str]:
    return random.choice(TITLES)


def any_content() -> str:
    return random.choice(CONTENTS)


def any_motd() -> SampleMotd:
    return SampleMotd(title=any_title(), content=any_content())
