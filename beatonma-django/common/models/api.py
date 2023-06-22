class ApiModel:
    def to_json(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement to_json()"
        )
