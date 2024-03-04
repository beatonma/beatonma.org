from basetest.testcase import SimpleTestCase
from common.util.pipeline import apply_pipeline


def append(value: str, suffix: str, prefix: str = "") -> str:
    return f"{prefix}{value}{suffix}"


def a(value: str) -> str:
    return append(value, "a")


def b(value: str) -> str:
    return append(value, "b")


def c(value: str) -> str:
    return append(value, "c")


class PipelineTests(SimpleTestCase):
    def test_pipeline(self):
        self.assertEqual(apply_pipeline("", []), "")
        self.assertEqual(apply_pipeline("", [a]), "a")
        self.assertEqual(apply_pipeline("", [a, b, c]), "abc")
        self.assertEqual(apply_pipeline("", [b, a, c]), "bac")

        self.assertEqual(
            apply_pipeline(
                "abc",
                [
                    (append, ["d"]),
                    (append, ["ef"]),
                ],
            ),
            "abcdef",
        )

        self.assertEqual(
            apply_pipeline(
                "bc",
                [
                    (
                        append,
                        [],
                        {"prefix": "a", "suffix": "d"},
                    )
                ],
            ),
            "abcd",
        )
