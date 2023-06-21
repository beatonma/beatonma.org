"""Generated by ChatGPT.

Prompt:
    Now can I get a list of 10 names that might be suitable for an app, browser
    extension, backend library, or python utility
"""
import random
from dataclasses import dataclass

APP_NAMES = [
    "CodeCompanion",
    "QuickLink",
    "DataDash",
    "Streamlined",
    "PyBoost",
    "Backstacker",
    "InfraMind",
    "DevSuite",
    "CodeVault",
    "RapidRunner",
]


@dataclass
class SampleChangelog:
    app_name: str
    version_name: str
    summary: str
    content: str


"""Generated by ChatGPT.

Prompt:
    ok, now can i get 3 examples of changelogs for those apps. they should be JSON formatted with fields for:
        - app_name
        - version_name
        - summary
        - content (~1 paragraph text)
"""
CHANGELOGS = list(
    map(
        lambda x: SampleChangelog(**x),
        [
            {
                "app_name": "CodeCompanion",
                "version_name": "1.1",
                "summary": "Improved code suggestions and performance optimizations.",
                "content": "In this update, we've made several improvements to the code suggestion feature to provide more accurate and relevant suggestions based on your code. We've also optimized the performance of the app to make it faster and more responsive when working with large codebases. Thank you for using CodeCompanion!",
            },
            {
                "app_name": "QuickLink",
                "version_name": "2.0",
                "summary": "New features and bug fixes.",
                "content": "We're excited to introduce several new features in this update, including the ability to customize the appearance of your links, improved link sharing options, and support for more link types. We've also fixed several bugs and made performance improvements to the app. Thanks for using QuickLink!",
            },
            {
                "app_name": "DataDash",
                "version_name": "3.2",
                "summary": "New data visualization tools and improved data import/export.",
                "content": "In this update, we've added several new data visualization tools to help you better understand your data, including scatter plots, heat maps, and more. We've also improved the data import/export functionality to make it easier to work with data from different sources. Thank you for using DataDash!",
            },
        ],
    )
)


APP_TYPES = [
    "Android",
    "Arduino",
    "Browser extension",
    "Python utility",
    "Web backend",
    "Webapp",
]

LANGUAGES = [
    "Python",
    "Kotlin",
    "Java",
    "Typescript",
    "Bash",
    "Powershell",
    "Javascript",
]


def any_app_name():
    return random.choice(APP_NAMES)


def any_app_type():
    return random.choice(APP_TYPES)


def any_changelog():
    return random.choice(CHANGELOGS)


def any_language():
    return random.choice(LANGUAGES)
