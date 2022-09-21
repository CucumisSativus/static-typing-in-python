from typing import Annotated

between_3_and_10 = Annotated[int, ValueRange(3, 10)]