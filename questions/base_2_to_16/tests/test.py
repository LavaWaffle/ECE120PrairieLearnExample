#! /usr/bin/python3

import cgrader


class QuestionGrader(cgrader.CGrader):
    def tests(self):
        self.test_compile_file(
            "starter_code.c", "starter_code", flags="-Wall -Wextra -pedantic -Werror"
        )
        self.test_run(
            "./starter_code",
            input="00000101\n",
            exp_output=[
                "05"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="00001101\n",
            exp_output=[
                "0D"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="00111111\n",
            exp_output=[
                "3F"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )
        self.test_run(
            "./starter_code",
            input="11111111\n",
            exp_output=[
                "FF"
            ],
            must_match_all_outputs="all",
            highlight_matches=True
        )


g = QuestionGrader()
g.start()
