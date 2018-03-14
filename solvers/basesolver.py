from score import Score


class BaseSolver(object):
    def __init__(self):
        pass

    def get_solution(self, rides_list, rows, columns, vehicles, rides, bonus, steps, args):
        """
        :param rides_list: rides_list[rid] == (x1, y1, x2, y2, step_start, step_end)
        :param rows: as specified by input file
        :param columns: as specified by input file
        :param vehicles: as specified by input file
        :param rides: as specified by input file
        :param bonus: as specified by input file
        :param steps: as specified by input file
        :param args:
        :return: rides_solution, score
        """
        rides_solution = [[]] * vehicles  # no rides
        score = Score()
        score.unassigned = rides
        return rides_solution, score
