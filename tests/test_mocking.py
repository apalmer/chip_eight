import pytest

class MockSubject():
    
    def mock_method(self):
        return 'a'

def test_mocking(mocker):
    expected = 'a'
    
    subject = MockSubject()
    
    actual = subject.mock_method()
    assert actual == expected

    mocker.patch(__name__ +".MockSubject.mock_method", return_value='b')
    mocked = subject.mock_method()
    assert mocked != expected