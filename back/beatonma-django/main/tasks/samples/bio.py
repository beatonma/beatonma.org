import random
from dataclasses import dataclass


@dataclass
class SampleBiography:
    summary: str
    content: str


SAMPLE_BIOGRAPHIES = list(
    map(
        lambda x: SampleBiography(**x),
        [
            {
                "summary": "Designer and artist with a focus on creating visually stunning experiences.",
                "content": "Hello! I'm Sarah, a designer and artist with a passion for creating beautiful and impactful experiences. I specialize in visual design and user experience, and have worked on projects ranging from branding and logos to mobile app interfaces. I love experimenting with different styles and techniques, and am always looking for new inspiration in my surroundings. When I'm not working on design projects, you can find me painting, practicing yoga, or exploring new places.",
            },
            {
                "summary": "Software developer with a passion for creating user-friendly applications.",
                "content": "Hi there! I'm John, a software developer with several years of experience working on projects ranging from mobile apps to web applications. My passion lies in creating software that is both easy to use and aesthetically pleasing. I'm always looking for new challenges and opportunities to learn and grow in my field. When I'm not coding, you can find me hiking, reading, or tinkering with electronics.",
            },
        ],
    )
)


def any_biography():
    return random.choice(SAMPLE_BIOGRAPHIES)
