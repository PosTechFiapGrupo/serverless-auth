"""Unit tests for CPF Value Object."""

import pytest
from src.domain.value_objects import CPF


class TestCPF:
    """Test suite for CPF value object."""

    def test_create_valid_cpf(self):
        """Test creating a valid CPF."""
        cpf = CPF("111.444.777-35")
        assert cpf.value == "111.444.777-35"

    def test_create_valid_cpf_without_formatting(self):
        """Test creating a valid CPF without formatting."""
        cpf = CPF("11144477735")
        assert cpf.value == "11144477735"

    def test_clean_cpf(self):
        """Test cleaning CPF (removing formatting)."""
        cpf = CPF("111.444.777-35")
        assert cpf.clean() == "11144477735"

    def test_format_cpf(self):
        """Test formatting CPF."""
        cpf = CPF("11144477735")
        assert cpf.format() == "111.444.777-35"

    def test_cpf_string_representation(self):
        """Test CPF string representation."""
        cpf = CPF("111.444.777-35")
        assert str(cpf) == "11144477735"

    def test_invalid_cpf_raises_error(self):
        """Test that invalid CPF raises ValueError."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("00000000000")

    def test_invalid_cpf_all_same_digits(self):
        """Test that CPF with all same digits is invalid."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("11111111111")

    def test_invalid_cpf_wrong_length(self):
        """Test that CPF with wrong length is invalid."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("123456789")

    def test_invalid_cpf_wrong_checksum(self):
        """Test that CPF with wrong checksum is invalid."""
        with pytest.raises(ValueError, match="Invalid CPF"):
            CPF("11144477736")  # Último dígito errado

    def test_cpf_is_immutable(self):
        """Test that CPF is immutable."""
        cpf = CPF("11144477735")
        with pytest.raises(AttributeError):
            cpf.value = "52998224725"

    def test_cpf_with_special_characters(self):
        """Test CPF with special characters."""
        cpf = CPF("111.444.777-35")
        assert cpf.clean() == "11144477735"

    def test_valid_cpf_examples(self):
        """Test various valid CPF examples."""
        valid_cpfs = ["11144477735", "52998224725", "84434916041"]
        for cpf_str in valid_cpfs:
            cpf = CPF(cpf_str)
            assert cpf.clean() == cpf_str.replace(".", "").replace("-", "")
