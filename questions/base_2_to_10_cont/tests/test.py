#! /usr/bin/python3

import cgrader


class QuestionGrader(cgrader.CGrader):
    def tests(self):
        self.test_compile_file(
            "starter_code.c", "starter_code", flags="-Wall -Wextra -pedantic -Werror"
        )
        self.test_run(
            "./starter_code",
            input="10 0000000101\n",
            exp_output=[
                "5"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="4 1101\n",
            exp_output=[
                "13"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="8 00011111\n",
            exp_output=[
                "31"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )


g = QuestionGrader()
g.start()
