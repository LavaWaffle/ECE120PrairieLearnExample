#! /usr/bin/python3

import cgrader


class QuestionGrader(cgrader.CGrader):
    def tests(self):
        self.test_compile_file(
            "starter_code.c", "starter_code", flags="-Wall -Wextra -pedantic -Werror"
        )
        self.test_run(
            "./starter_code",
            input="5\n",
            exp_output=[
                "000101"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="10\n",
            exp_output=[
                "001010"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="32\n",
            exp_output=[
                "100000"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="63\n",
            exp_output=[
                "111111"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )


g = QuestionGrader()
g.start()
