import pytest
import os
from src.task import count_dna


def test_count_dna_valid_file():
    """Test counting DNA in a valid file."""
    filepath = os.path.join(os.path.dirname(__file__), "files", "sample_dna.txt")
    result = count_dna(filepath)

    assert result["status"] == "success"
    assert result["counts"]["A"] == 15
    assert result["counts"]["T"] == 15
    assert result["counts"]["C"] == 15
    assert result["counts"]["G"] == 15


def test_count_dna_mixed_case():
    """Test counting DNA with mixed case."""
    filepath = os.path.join(os.path.dirname(__file__), "files", "mixed_case_dna.txt")
    result = count_dna(filepath)

    assert result["status"] == "success"
    assert result["counts"]["A"] == 4
    assert result["counts"]["T"] == 4
    assert result["counts"]["C"] == 4
    assert result["counts"]["G"] == 4


def test_count_dna_invalid_chars():
    """Test counting DNA with invalid characters."""
    filepath = os.path.join(os.path.dirname(__file__), "files", "invalid_dna.txt")
    result = count_dna(filepath)

    assert result["status"] == "success"
    assert result["counts"]["A"] == 1
    assert result["counts"]["T"] == 1
    assert result["counts"]["C"] == 1
    assert result["counts"]["G"] == 1


def test_count_dna_nonexistent_file():
    """Test handling of nonexistent file."""
    result = count_dna("/nonexistent/file.txt")

    assert result["status"] == "error"
    assert "No such file or directory" in result["message"]


def test_count_dna_empty_file(tmp_path):
    """Test counting in an empty file."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    result = count_dna(str(empty_file))

    assert result["status"] == "success"
    assert result["counts"]["A"] == 0
    assert result["counts"]["T"] == 0
    assert result["counts"]["C"] == 0
    assert result["counts"]["G"] == 0