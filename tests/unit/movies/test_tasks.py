from unittest import mock
from movies.tasks import process_heavy_task


@mock.patch("movies.tasks.logger")
def test_process_heavy_task_mocked_logger(mock_logger):
    result = process_heavy_task(max_count=10)
    assert result == 10

    mock_logger.info.assert_called()
