def appearance(intervals: dict[str, list[int]]) -> int:
    """
    I actually consider the code in the docstring below a much better version of this function.
    Yet, due to some *really* weird data that was included in the tests
    (like intervals starting at 2789 and apparently never ending - for almost five years now),
    it's impossible to use it with the given dataset.

    Still, I'm gonna leave it here. Just in case…

    The code currently in use abruptly ignores any uncomfortable intervals by just skipping them
    (and assuming that the order in which they come really matters).
    However, since this bruteforce solution actually worked, I’ve decided that this is
    the chosen one - the only one that deserves the leading role in this little tragicomedy.

    Oh right, this was supposed to be a docstring, not an essay about me looking for excuses, so...

    The function takes a dictionary of intervals and returns the length of overlap
    between all three: lesson, pupil, and tutor.

    The logic is pretty straightforward (and not exactly elegant):
        - For each list of intervals, expand them into a flat set of individual seconds.
        - Intersect the sets for lesson, pupil, and tutor.
        - Return the size of the intersection - that’s how long they were all in sync.

    nodes = [(intervals[entity][i], 'exit' if i % 2 else 'enter')
             for entity in ['pupil', 'tutor'] for i in range(len(intervals[entity]))]
    nodes += [(intervals['lesson'][0], 'enter'), (intervals['lesson'][1], 'exit')]
    nodes.sort(key=lambda node: node[0])

    ecount, delta = 0, 0

    for node in nodes:
        ecount += 1 if node[1] == 'enter' else -1
        delta += node[0] if delta < 0 and ecount != 3 else -node[0] if delta >= 0 and ecount == 3 else 0

    return delta
    """
    def overlaps(timerange):
        return set(j for i in range(0, len(timerange), 2) for j in range(timerange[i], timerange[i + 1]))

    return len(overlaps(intervals['lesson']) & overlaps(intervals['pupil']) & overlaps(intervals['tutor']))


# flake8: noqa
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
