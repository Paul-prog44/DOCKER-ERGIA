import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(autouse=True)
def mock_db_singleton():
    """Mock `db_singleton` pour tous les tests."""
    with patch('flaskr.database.db_singleton', new_callable=MagicMock) as mock_db:
        yield mock_db