import logging


def parse_input(file_in):
    """
    Parse input file
    :param file_in: input file name
    :return: rides_list, rows, columns, vehicles, rides, bonus, steps
    """
    logging.info("opening {}".format(file_in))
    with open(file_in, 'r') as f:
        first_line = f.readline()
        rows, columns, vehicles, rides, bonus, steps = tuple([int(x) for x in first_line.split(' ')])
        logging.debug("{} {} {} {} {} {}".format(rows, columns, vehicles, rides, bonus, steps))
        rides_list = []
        for rid, line in enumerate(f.readlines()):
            ride = tuple([int(x) for x in line.split(' ')])  # x1, y1, x2, y2, step_start, step_end
            rides_list.append(ride)
    logging.debug("parsing rides done")
    return rides_list, rows, columns, vehicles, rides, bonus, steps


def dump_rides(rides, output):
    """
    Dump rides to output file.
    :param rides: rides assigned to vehicles, i.e. rides[i] = ride ids assigned to vehicle i
    :param output: output file name
    :return: None
    """
    logging.info("dumping rides to {}".format(output))
    data = ""
    for rids in rides:
        data += str(len(rids))
        if rids:
            data += ' '
            data += ' '.join([str(r) for r in rids])
        data += '\n'
    with open(output, 'w+') as f:
        f.write(data)  # only one write statement -> much quicker
    logging.debug("dumping rides: done")
