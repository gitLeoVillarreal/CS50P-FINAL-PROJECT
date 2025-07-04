import tempfile
import pytest
from project import compareCitiesWithDifferentCharacters, checkRepeatedCities

def test_compareCitiesWithDifferentCharacters_equal():
    assert compareCitiesWithDifferentCharacters("Merida, Yucatan", "Mérida, Yucatán") is True
    assert compareCitiesWithDifferentCharacters("Zacatecas, Zacatecas", "zacatecas, ZACATECAS") is True
    assert compareCitiesWithDifferentCharacters("Guadalajara, Jalisco", "GUADALAJARA, Jalisco") is True

def test_compareCitiesWithDifferentCharacters_not_equal():
    assert compareCitiesWithDifferentCharacters("Tijuana", "Toluca") is False
    assert compareCitiesWithDifferentCharacters("Puebla", "Merida") is False

def test_checkRepeatedCities_found():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write("Monterrey, Nuevo Leon\n")
        temp.seek(0)
        assert checkRepeatedCities(temp.name, "Monterrey, Nuevo Leon") is True

def test_checkRepeatedCities_not_found():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write("CDMX, CDMX\n")
        temp.seek(0)
        assert checkRepeatedCities(temp.name, "Puebla, Puebla") is False
