import csv
import pytest
from solution.main import save_to_csv, CYRILLIC_LETTERS


@pytest.mark.asyncio
async def test_save_to_csv_creates_valid_file(tmp_path):
    test_file = tmp_path / "beasts.csv"
    test_data = [i for i in range(len(CYRILLIC_LETTERS))]

    await save_to_csv(test_data, file=str(test_file))

    assert test_file.exists(), "CSV file was not created."

    with open(test_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["letter", "amount"], "CSV header is incorrect."

    assert len(rows) == len(CYRILLIC_LETTERS) + 1

    for i, row in enumerate(rows[1:]):
        assert row[0] == CYRILLIC_LETTERS[i]
        assert int(row[1]) == i


@pytest.mark.asyncio
async def test_save_to_csv_shorter_data(tmp_path):
    test_file = tmp_path / "beasts.csv"
    test_data = [1] * 10

    await save_to_csv(test_data, file=str(test_file))

    with open(test_file, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))

    assert len(rows) == len(test_data) + 1
