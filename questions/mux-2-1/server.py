from bool import *
from sympy import symbols, And, Or, Not, Xor, sympify
from random import choice
import prairielearn.sympy_utils as psu
from html import escape

VALID_CHARS = {'(', ')', ' ', '+', '*', "'", '1', '0', 'A', 'B'}
A, B = symbols('A, B', Boolean=True)
N = 2

ANSWERS = {
    'AND': { 
        'eval': And(A, B),
        'repr': {
            'I_0': '0',
            'I_1': 'A',
            'S': 'B',
        }
    },
    'OR': { 
        'eval': Or(A, B),
        'repr': {
            'I_0': 'B',
            'I_1': '1',
            'S': 'A',
        }
    },
    'XOR': {
        'eval': Xor(A, B),
        'repr': {
            'I_0': 'B',
            'I_1': "B'",
            'S': 'A',
        }
    },
    'NAND': {
        'eval': Not(And(A, B)),
        'repr': {
            'I_0': "1",
            'I_1': "A'",
            'S': "B",
        }
    },
    'NOR': {
        'eval': Not(Or(A, B)),
        'repr':  {
            'I_0': "B'",
            'I_1': '0',
            'S': 'A',
        }
    },
    'XNOR': {
        'eval': Not(Xor(A, B)),
        'repr': {
            'I_0': "B'",
            'I_1': 'B',
            'S': 'A',
        }
    },
}

EXPRESSIONS = list(ANSWERS.keys())

def generate(data):
    expr_str = choice(EXPRESSIONS)
    
    data['params']['expr'] = expr_str
    
    correct_answers = ANSWERS.get(expr_str)['repr']
    
    data['params']['I_0_ans'] = correct_answers['I_0']
    data['params']['I_1_ans'] = correct_answers['I_1']
    data['params']['S_ans'] = correct_answers['S']



def validate(s: str):
    return parseExprWithErr(s)
    
def parse(data):
    I_0 = data['submitted_answers']['I_0']
    I_1 = data['submitted_answers']['I_1']
    S = data['submitted_answers']['S']
    
    eqs = [(I_0, 'I_0'), (I_1, 'I_1'), (S, 'S')]
    for eqsn in eqs:
        # eq = user input, eqstr = 'I_0'
        eq, eqstr = eqsn
        non_valid_chars = set(eq) - VALID_CHARS
        res = validate(eq)
        
        if len(non_valid_chars) > 0:
            data['format_errors'][eqstr] = f"Using non usable character: {non_valid_chars}"
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
    sympy_locals = {'A': A, 'B': B}
    return sympify(s, locals=sympy_locals)

ANSWER_TABLE = '''
<br>
<table class="table table-striped table-condensed" style="width:300px" summary="Truth table for a Boolean function">
<tbody>
<tr><th>A</th><th>B</th><th style="text-align:center">{0}</th><th style="text-align:center">Your Output</th></tr> 
<tr><td>0</td><td>0</td><td style="text-align:center">{1}</td><td style="text-align:center">{2}</td></tr>
<tr><td>0</td><td>1</td><td style="text-align:center">{3}</td><td style="text-align:center">{4}</td></tr>
<tr><td>1</td><td>0</td><td style="text-align:center">{5}</td><td style="text-align:center">{6}</td></tr>
<tr><td>1</td><td>1</td><td style="text-align:center">{7}</td><td style="text-align:center">{8}</td></tr>
</tbody>
</table>
'''

# Grade all the expressions against the ground truth
def grade(data):
    I_0 = convert_to_sympy(data['submitted_answers']['I_0']) 
    I_1 = convert_to_sympy(data['submitted_answers']['I_1'])
    S = convert_to_sympy(data['submitted_answers']['S'])
    
    student_expr = Or(And(S, I_1), (And(Not(S), I_0)))
    
    expr_str = data['params']['expr']
    true_expr = ANSWERS[expr_str]['eval']
    
    out_table = ['A ' + expr_str + ' B']
    
    # two vars 2 ** 2
    incorrect = 0
    for i in range(2 ** N):
        val_A_int = i & (1 << 1)
        val_B_int = i & 1
        
        sub_dict = {
            A: bool(val_A_int),
            B: bool(val_B_int)
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