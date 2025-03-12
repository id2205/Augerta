import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from rooster.services.stock_data import get_stock_symbols
from rooster.integration.myquantServices import MyQuantService

@pytest.fixture
def mock_myquant_service():
    with patch('rooster.services.stock_data.MyQuantService') as mock:
        yield mock

def test_get_stock_symbols_success(mock_myquant_service):
    # Setup mock
    mock_service = MagicMock()
    mock_service.get_symbols.return_value = pd.DataFrame({
        'symbol': ['SH600000', 'SZ000001'],
        'name': ['浦发银行', '平安银行'],
        'exchange': ['SHSE', 'SZSE']
    })
    mock_myquant_service.return_value = mock_service

    # Test with mock API key and disable file saving
    with patch.dict('os.environ', {'MYQUANT_API_KEY': 'test_key'}):
        result = get_stock_symbols(save_to_file=False)
    
    # Verify
    assert not result.empty
    assert len(result) == 2
    assert list(result.columns) == ['symbol', 'name', 'exchange']
    mock_service.get_symbols.assert_called_once_with(exchange='SHSE,SZSE')

def test_get_stock_symbols_failure(mock_myquant_service):
    # Setup mock to raise exception
    mock_service = MagicMock()
    mock_service.get_symbols.side_effect = Exception("API Error")
    mock_myquant_service.return_value = mock_service

    # Test
    result = get_stock_symbols()
    
    # Verify
    assert result.empty

def test_get_stock_symbols_no_api_key(mock_myquant_service):
    # Test without API key
    with patch.dict('os.environ', {}, clear=True):
        result = get_stock_symbols()
        assert result.empty
        mock_myquant_service.assert_not_called()

def test_get_stock_symbols_retry_logic(mock_myquant_service):
    # Setup mock to fail twice then succeed
    mock_service = MagicMock()
    mock_service.get_symbols.side_effect = [
        Exception("First attempt failed"),
        Exception("Second attempt failed"),
        pd.DataFrame({
            'symbol': ['SH600000'],
            'name': ['浦发银行'],
            'exchange': ['SHSE']
        })
    ]
    mock_myquant_service.return_value = mock_service

    # Test with mock API key and disable file saving
    with patch.dict('os.environ', {'MYQUANT_API_KEY': 'test_key'}):
        result = get_stock_symbols(save_to_file=False)
    
    # Verify
    assert not result.empty
    assert mock_service.get_symbols.call_count == 3
