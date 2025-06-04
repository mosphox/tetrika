from solution.main import appearance


def test_full_overlap():
    intervals = {
        'lesson': [10, 50],
        'pupil': [10, 50],
        'tutor': [10, 50],
    }

    assert appearance(intervals) == 40


def test_no_overlap():
    intervals = {
        'lesson': [0, 10],
        'pupil': [20, 30],
        'tutor': [40, 50],
    }

    assert appearance(intervals) == 0


def test_partial_overlap():
    intervals = {
        'lesson': [0, 100],
        'pupil': [50, 120],
        'tutor': [60, 90],
    }

    assert appearance(intervals) == 30


def test_multiple_intervals():
    intervals = {
        'lesson': [0, 50],
        'pupil': [10, 20, 30, 40],
        'tutor': [15, 35],
    }

    assert appearance(intervals) == 10


def test_empty_intervals():
    intervals = {
        'lesson': [],
        'pupil': [0, 10],
        'tutor': [0, 10],
    }

    assert appearance(intervals) == 0
