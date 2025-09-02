#! /usr/bin/python3

import cgrader


class QuestionGrader(cgrader.CGrader):
    def tests(self):
        self.compile_file(
            "starter_code.c", "starter_code", flags="-Wall -Wextra -pedantic -Werror -Wno-implicit-function-declaration"
        )
        self.test_run(
            "./starter_code",
            exp_output=[
                ".1        : 0 01111111011 1001100110011001100110011001100110011001100110011010",
                ".2        : 0 01111111100 1001100110011001100110011001100110011001100110011010",
                ".1 + .2:  : 0 01111111101 0011001100110011001100110011001100110011001100110100",
                ".3        : 0 01111111101 0011001100110011001100110011001100110011001100110011"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )


g = QuestionGrader()
g.start()
