
class Constants():
    global CTS
    CTS = {
        "PIB": (22400000000, 'Syria'),
        "CONVERSION": (50.0, "CR to $")
    }

    def __init__(self) -> None:
        pass

    def getter(self):
        return CTS