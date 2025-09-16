from bool import *
from sympy import symbols, And, Or, Not, Xor, sympify
from random import choice
import prairielearn.sympy_utils as psu
from html import escape

VALID_CHARS = {'(', ')', ' ', "'", '+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
I_2, I_1, I_0, S = symbols('I_2, I_1, I_0, S', Boolean=True)
A = And(Not(I_2), Not(I_1), Not(I_0))
B = And(Not(I_2), Not(I_1), I_0)
C = And(Not(I_2), I_1, Not(I_0))
D = And(Not(I_2), I_1, I_0)
E = And(I_2, Not(I_1), Not(I_0))
F = And(I_2, Not(I_1), I_0)
G = And(I_2, I_1, Not(I_0))
H = And(I_2, I_1, I_0)
N = 3

# 3 - 8 dec I to A
ANSWERS = {
    "(I_2*I_1)' + I_0'*I_1'*I_2'": {
        'eval': Or(Not(And(I_2, I_1)), And(Not(I_0), Not(I_1), Not(I_2))),
        'repr': "(G+H)'"
    },
    "(I_1*I_0)' + I_2'*I_1*I_0'": {
        'eval': Or(Not(And(I_1, I_0)), And(Not(I_2), I_1, Not(I_0))),
        'repr': "(D+H)'"
    },
    "(I_2*I_0)' + I_1'*I_0'*I_2'": {
        'eval': Or(Not(And(I_2, I_0)), And(Not(I_1), Not(I_0), Not(I_2))),
        'repr': "(F+H)'"
    }
}

EXPRESSIONS = list(ANSWERS.keys())

def generate(data):
    expr_str = choice(EXPRESSIONS)
    
    data['params']['expr'] = expr_str
    
    correct_answer = ANSWERS.get(expr_str)['repr']
    
    data['params']['F'] = correct_answer



def validate(s: str):
    return parseExprWithErr(s)
    
def parse(data):
    F = data['submitted_answers']['F']
    
    eqs = [(F, 'F')]
    for eqsn in eqs:
        # eq = user input, eqstr = 'I_0'
        eq, eqstr = eqsn
        non_valid_chars = set(eq) - VALID_CHARS
        res = validate(eq)
        
        if len(non_valid_chars) > 0:
            data['format_errors'][eqstr] = f"Using non usable character: {non_valid_chars}"
        elif eq.count("'") != 1:
            data['format_errors'][eqstr] = f"Must use exactly 1 not (')"
        elif type(res) is tuple:
            prefix, badch, suffix = res
            eqOut = "<p>Malformed Boolean expression:</p>\n"
            eqOut += "<p><code>" + escape(prefix) + "</code>"
            if len(badch) != 0:
                eqOut += "<code style=\"background-color:red\">" + escape(badch) + "</code>"
            if len(suffix) != 0:
                eqOut += "<code>" + escape(suffix) + "</code></p>\n"
            data['submitted_answers'][eqstr] = eqOut
            data['format_errors'][eqstr] = "Malformed Boolean expression"



def convert_to_sympy(s: str):
    s = parseExpr(s)
    s = exprSympyStr(s)
    sympy_locals = {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G, 'H': H}
    return sympify(s, locals=sympy_locals)

ANSWER_TABLE = '''
<br>
<table class="table table-striped table-condensed" style="width:400px" summary="Truth table for a Boolean function">
<tbody>
<tr><th>$I_2$</th><th>$I_1$</th><th>$I_0$</th><th style="text-align:center">{0}</th><th style="text-align:center">Your Output</th></tr> 
<tr><td>0</td><td>0</td><td>0</td><td style="text-align:center">{1}</td><td style="text-align:center">{2}</td></tr>
<tr><td>0</td><td>0</td><td>1</td><td style="text-align:center">{3}</td><td style="text-align:center">{4}</td></tr>
<tr><td>0</td><td>1</td><td>0</td><td style="text-align:center">{5}</td><td style="text-align:center">{6}</td></tr>
<tr><td>0</td><td>1</td><td>1</td><td style="text-align:center">{7}</td><td style="text-align:center">{8}</td></tr>
<tr><td>1</td><td>0</td><td>0</td><td style="text-align:center">{9}</td><td style="text-align:center">{10}</td></tr>
<tr><td>1</td><td>0</td><td>1</td><td style="text-align:center">{11}</td><td style="text-align:center">{12}</td></tr>
<tr><td>1</td><td>1</td><td>0</td><td style="text-align:center">{13}</td><td style="text-align:center">{14}</td></tr>
<tr><td>1</td><td>1</td><td>1</td><td style="text-align:center">{15}</td><td style="text-align:center">{16}</td></tr>
</tbody>
</table>
'''

# Grade all the expressions against the ground truth
def grade(data):
    F = convert_to_sympy(data['submitted_answers']['F'])
    
    student_expr = F
    
    expr_str = data['params']['expr']
    true_expr = ANSWERS[expr_str]['eval']
    
    out_table = [f"F = ${expr_str}$"]
    
    incorrect = 0
    for i in range(2 ** N):
        val_I_2_int = i & (1 << 2)
        val_I_1_int = i & (1 << 1)
        val_I_0_int = i & 1
        
        A = And(Not(bool(val_I_2_int)), Not(bool(val_I_1_int)), Not(bool(val_I_0_int)))
        B = And(Not(bool(val_I_2_int)), Not(bool(val_I_1_int)), bool(val_I_0_int))
        C = And(Not(bool(val_I_2_int)), bool(val_I_1_int), Not(bool(val_I_0_int)))
        D = And(Not(bool(val_I_2_int)), bool(val_I_1_int), bool(val_I_0_int))
        E = And(bool(val_I_2_int), Not(bool(val_I_1_int)), Not(bool(val_I_0_int)))
        F = And(bool(val_I_2_int), Not(bool(val_I_1_int)), bool(val_I_0_int))
        G = And(bool(val_I_2_int), bool(val_I_1_int), Not(bool(val_I_0_int)))
        H = And(bool(val_I_2_int), bool(val_I_1_int), bool(val_I_0_int))

        sub_dict = {
            I_2: bool(val_I_2_int),
            I_1: bool(val_I_1_int),
            I_0: bool(val_I_0_int),
            A: A,
            B: B,
            C: C,
            D: D,
            E: E,
            F: F,
            G: G,
            H: H,
        }
        
        student_result = student_expr.subs(sub_dict)
        true_result = true_expr.subs(sub_dict)
        
        stu_int = 1 if student_result else 0
        true_int = 1 if true_result else 0
        
        out_table.append(true_int)
        if stu_int != true_int:
            incorrect += 1
            out_table.append("<b style=\"color:red\">" + str(stu_int) + "</b>")
        else:
            # correct
            out_table.append(stu_int)
    
    correct = 2 ** N - incorrect

    score = max(0, correct / ( 2 ** N))
    data['score'] = score
    
    # prepare submitted_answer data
    data['submitted_answers']['table'] = ANSWER_TABLE.format(*out_table)