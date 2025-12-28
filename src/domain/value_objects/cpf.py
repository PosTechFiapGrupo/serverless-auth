import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CPF:
    """
    CPF Value Object.
    
    Represents a Brazilian CPF document number.
    Immutable and always valid (validates on creation).
    """
    
    value: str
    
    def __post_init__(self):
        """Validate CPF on creation."""
        if not self._is_valid():
            raise ValueError(f"Invalid CPF: {self.value}")
    
    def _clean(self) -> str:
        """Remove non-numeric characters."""
        return "".join(re.findall(r"\d+", self.value))
    
    def _is_valid(self) -> bool:
        """Validate CPF using official algorithm."""
        cpf = self._clean()
        
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False
        
        cpf_numbers = list(map(int, cpf))
        multipliers = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        
        for i in range(9, 11):
            remainder = (
                sum([a * b for a, b in zip(cpf_numbers[:i], multipliers)]) * 10 % 11
            )
            digit = 0 if remainder == 10 else remainder
            if digit != cpf_numbers[i]:
                return False
            multipliers.insert(0, 11)
        
        return True
    
    def clean(self) -> str:
        """Return CPF without formatting."""
        return self._clean()
    
    def format(self) -> str:
        """Return formatted CPF (XXX.XXX.XXX-XX)."""
        cpf = self._clean()
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def __str__(self) -> str:
        """String representation."""
        return self.clean()
