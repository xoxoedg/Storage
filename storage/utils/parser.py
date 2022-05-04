class ParamParser:

    @staticmethod
    def parse_file(filename):
        params_list = []
        with open(filename, "r") as params_file:
            for line in params_file:
                params_list.append(line.strip().split(","))
        return list(map(lambda x: (x[0], x[1]), params_list))


