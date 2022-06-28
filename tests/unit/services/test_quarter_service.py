from mock import Mock, call
from services import QuarterService


class TestQuarterService:
    def setup(self):
        self.bit_service_mock = Mock()
        self.service = QuarterService(self.bit_service_mock)

    def test_column_round(self):
        self.service.quarter_round = Mock()
        matrix = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ]
        self.service.column_round(matrix)
        self.service.quarter_round.assert_has_calls(
            [
                call(0, 4, 8, 12),
                call(1, 5, 9, 13),
                call(2, 6, 10, 14),
                call(3, 7, 11, 15),

            ]
        )
