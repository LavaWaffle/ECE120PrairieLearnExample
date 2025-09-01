#! /usr/bin/python3

import cgrader


class QuestionGrader(cgrader.CPPGrader):
    def tests(self):
        self.test_compile_file(
            "starter_code.cpp", "starter_code", flags="-Wall -Wextra -pedantic -Werror"
        )
        self.test_run(
            "./starter_code",
            input="5 4\n",
            exp_output=[
                "Enter the length: \n",
                "Enter the width: \n",
                "The perimeter of the rectangle is: 18\n",
            ],
            must_match_all_outputs="partial",
        )
        self.test_run(
            "./starter_code",
            input="3 3\n",
            exp_output=[
                "Enter the length: \n",
                "Enter the width: \n",
                "The perimeter of the rectangle is: 12\n",
            ],
            must_match_all_outputs="partial",
        )


g = QuestionGrader()
g.start()
