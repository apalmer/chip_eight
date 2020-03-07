import chip_eight

def test_execute(capsys):
    chip_eight.execute()
    captured = capsys.readouterr()
    assert captured.out == "Executing...\n"