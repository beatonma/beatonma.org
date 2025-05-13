class Installer:
    name: str

    def install(self):
        raise NotImplemented(
            f"{self.__class__.__name__} does not implement install() method"
        )

    def is_installed(self) -> bool:
        raise NotImplemented(
            f"{self.__class__.__name__} does not implement check() method"
        )

    def __call__(self, *args, **kwargs):
        if self.is_installed():
            return

        self.install()
