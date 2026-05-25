import pytest
from main import analyze

def test_wrong_path_extension_raises_error():
    with pytest.raises(ValueError):
        analyze("input/not_a_pdf.txt") #the test passes only if ValueError is raised

def test_file_not_found_raises_error():
    with pytest.raises(FileNotFoundError):
        analyze("input/does_not_exist.pdf")       