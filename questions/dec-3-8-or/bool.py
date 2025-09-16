from random import randrange, randint, sample, shuffle
from functools import reduce
import pyparsing as pp
import subprocess

OR = 0
AND = 1
NOT = -1
ZERO = {OR:()}
ONE = {AND:()}

def parity(x):
	r = 0
	while x != 0:
		r ^= (x & 1)
		x >>= 1
	return r

def mkOr(terms):
	return {OR:tuple(terms)}

def orExpr(*terms):
	return mkOr(terms)

def mkAnd(terms):
	return {AND:tuple(terms)}

def andExpr(*terms):
	return mkAnd(terms)

def mkNot(arg):
	return {-1: arg}

def notExpr(arg):
	return mkNot(arg)

def mkNand(terms):
	return {-1:{AND:tuple(terms)}}

def nandExpr(*terms):
	return mkNand(terms)

def mkNor(terms):
	return {-1:{OR:tuple(terms)}}

def norExpr(*terms):
	return mkNor(terms)

def mkXor(inputTerms):
	n = len(inputTerms)
	orTerms = list()
	for i in range(2**n):
		if parity(i) == 1:
			andTerms = list()
			for j in range(n):
				if (i >> j) & 1:
					andTerms.append(inputTerms[j])					
				else:
					andTerms.append(mkNot(inputTerms[j]))
			orTerms.append(mkAnd(andTerms))
	return mkOr(orTerms)
	
def xorExpr(*terms):
	return mkXor(terms)

def mkXnor(inputTerms):
	n = len(inputTerms)
	orTerms = list()
	for i in range(2**n):
		if parity(i) == 0:
			andTerms = list()
			for j in range(n):
				if (i >> j) & 1:
					andTerms.append(mkNot(inputTerms[j]))
				else:
					andTerms.append(inputTerms[j])
			orTerms.append(mkAnd(andTerms))
	return mkOr(orTerms)
	
def xnorExpr(*terms):
	return mkXnor(terms)

#	def ttUnpack(ttcode, nvars):
#		return [(ttcode >> i) & 1 for i in range(2**nvars)]
#	
#	def ttPack(tt):
#		ttcode = 0
#		for i in range(len(tt)):
#			ttcode |= (tt[i] << i)
#		return ttcode

def _negVal(v):
	return 1-v if type(v) is int else None

def _ttRev(tt, nvars = None):
	def revBits(x, n):
		y = 0
		for i in range(n):
			y <<= 1
			y |= x & 1
			x >>= 1
		return y

	if nvars is None:
		nvars = ttNumVars(tt)
	return tuple([tt[revBits(pt,nvars)] for pt in range(2**nvars)])

def ttParse(s):
	def ttParseVal(c):
		if c == '0':
			return 0
		if c == '1':
			return 1
		return None
	
	return _ttRev(list(map(ttParseVal, s)))

def ttStr(tt):
	def ttValStr(v):
		if type(v) is int:
			return str(v)
		return 'X'
	
	return ''.join(_ttRev(list(map(ttValStr, tt))))

def ttNumVars(tt):
	nvals = len(tt)
	nvars = 0
	while nvals > 1:
		nvals >>= 1
		nvars += 1
	return nvars

def espForTab(tt, nvars = None):
	if nvars is None:
		nvars = ttNumVars(tt)

	lines = list()

	lines.append(".i {:d}".format(nvars))
	lines.append(".o 1")

	ilbstr = ".ilb"
	for i in range(nvars):
		ilbstr += " " + chr(ord('A') + i)
	lines.append(ilbstr)
	lines.append(".ob F")
	lines.append(".type fr")

	ttr = _ttRev(tt)
	for i in range(2**nvars):
		if ttr[i] is not None:
			lines.append(("{:0" + str(nvars) + "b} {:b}").format(i, ttr[i]))
	
	lines.append(".e")
	return lines

#	def espExpr(espStr, nvars):
#		expr = list()
#		for i in range(len(espStr) // nvars):
#			prodTerms = list()
#			for j in range(nvars):
#				if espStr[nvars*i+j] == '0':
#					prodTerms.append(notExpr(j))
#				elif espStr[nvars*i+j] == '1':
#					prodTerms.append(j)
#			expr.append(mkAnd(prodTerms))
#		return mkOr(expr)

def ttMinSOP(tt, espCmd = './espresso', numVars = None):
	if numVars is None:
		numVars = ttNumVars(tt)
	
	espInput = '\n'.join(espForTab(tt, numVars))
	
	espProc = subprocess.Popen (
		[espCmd,'-Dopo'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	
	espOutput, _ = espProc.communicate(espInput)
	espLines = espOutput.split('\n')
	
	terms = list()
	for espLine in espLines:
		espLine = espLine.strip()
		if espLine.startswith(('.','#')) or len(espLine) == 0:
			continue

		assert (espLine[numVars] == ' ')
		assert (espLine[:numVars].strip('01-') == '')
	
		lits = list()
		for i in range(numVars):
			if espLine[i] == '0':
				lits.append(notExpr(i))
			elif espLine[i] == '1':
				lits.append(i)
		
		terms.append(mkAnd(lits))
	
	return mkOr(terms) if len(terms) != 1 else terms[0]

def ttMinPOS(tt, espCmd = './espresso', numVars = None):
	return exprNeg(ttMinSOP(ttNeg(tt), espCmd, numVars))
	
def ttSOP(tt, nvars = None):
	if nvars is None:
		nvars = ttNumVars(tt)
	
	terms = list()
	for i in range(2**nvars):
		if tt[i] == 1:
			term = list()
			for j in range(nvars):
				if (i >> j) & 1:
					term.append(j)
				else:
					term.append(notExpr(j))
			terms.append(mkAnd(term))
	return mkOr(terms)

def ttPOS(tt, nvars = None):
	if nvars is None:
		nvars = ttNumVars(tt)
	
	terms = list()
	for i in range(2**nvars):
		if tt[i] == 0:
			term = list()
			for j in range(nvars):
				if (i >> j) & 1:
					term.append(notExpr(j))
				else:
					term.append(j)
			terms.append(mkOr(term))
	return mkAnd(terms)

def exprDual(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return mkNot(exprDual(arg))
		elif op == OR:
			return mkAnd(map(exprDual, arg))
		elif op == AND:
			return mkOr(map(exprDual, arg))
		else:
			return None
	else:
		return expr

def exprNeg(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return arg
		elif op == OR:
			return mkAnd(map(exprNeg, arg))
		elif op == AND:
			return mkOr(map(exprNeg, arg))
		else:
			return None
	elif type(expr) is int:
		return mkNot(expr)
	else:
		return None

def ttDual(tt):
	mask = len(tt) - 1
	return tuple([_negVal(tt[~i & mask]) for i in range(len(tt))])

def ttNeg(tt):
	return tuple(map(_negVal, tt))

def exprVars(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return exprVars(arg)
		elif op == OR:
			return reduce(lambda x,y: set.union(x,exprVars(y)), arg, set())
		elif op == AND:
			return reduce(lambda x,y: set.union(x,exprVars(y)), arg, set())
		else:
			return None
	elif type(expr) is int:
		return {expr}
	else:
		return None

def exprPerm(expr, o):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return {-1:exprPerm(arg, o)}
		elif op == OR:
			return {0: tuple(map(lambda e: exprPerm(e,o), arg))}
		elif op == AND:
			return {1: tuple(map(lambda e: exprPerm(e,o), arg))}
		else:
			return None
	else:
		return o[expr]
	

def exprEval(expr, valBits):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return 1 - exprEval(arg, valBits)
		elif op == OR:
			return reduce(lambda x,y: x | exprEval(y, valBits), arg, 0)
		elif op == AND:
			return reduce(lambda x,y: x & exprEval(y, valBits), arg, 1)
		else:
			return None
	elif type(expr) is int:
		if type(valBits) is int:
			return (valBits >> expr) & 1
	else:
		return None

def exprTab(expr, numVars):
	return tuple(map(lambda i: exprEval(expr,i), range(2**numVars)))

def exprIsVar(expr):
	return type(expr) is int

def exprIsLit(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT and type(arg) is int:
			return True
	elif type(expr) is int:
		return True
	return False

def exprIsLitProd(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return type(arg) is int
		elif op == AND:
			return reduce(lambda b,t: b and exprIsLit(t), arg, True)
	elif type(expr) is int:
		return True
	return False

def exprIsLitSum(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return type(arg) is int
		elif op == OR:
			return reduce(lambda b,t: b and exprIsLit(t), arg, True)
	elif type(expr) is int:
		return True
	return False

def exprIsSOP(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return type(arg) is int
		elif op == OR:
			return reduce(lambda b,t: b and exprIsLitProd(t), arg, True)
		elif op == AND:
			return reduce(lambda b,t: b and exprIsLit(t), arg, True)
	elif type(expr) is int:
		return True
	return False

def exprIsPOS(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return type(arg) is int
		elif op == AND:
			return reduce(lambda b,t: b and exprIsLitSum(t), arg, True)
		elif op == OR:
			return reduce(lambda b,t: b and exprIsLit(t), arg, True)
	elif type(expr) is int:
		return True
	return False

def exprStr(expr, syms=dict(), par=0):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			resultStr = negStr(arg, syms)
		elif op == OR:
			resultStr = sumStr(arg, syms, par)
		elif op == AND:
			resultStr = prodStr(arg, syms, par)
		else:
			return None
	elif type(expr) is int:
		resultStr = litStr(expr, syms)
	else:
		return None
	
	return syms.get('{','') + resultStr + syms.get('}','')

def litStr(arg, syms=dict()):
	varName = chr(ord('A')+arg)
	return syms.get(varName, varName)

def negStr(arg, syms=dict()):
	if type(arg) is int:
		varName = chr(ord('A')+arg)
		varStr = syms.get(varName, varName)
		return syms.get('!' + varName, syms.get('!','!') + varStr)
	else:
		return syms.get('!','!') + exprStr(arg, syms, 2)

def sumStr(terms, syms=dict(), par=0):
	if len(terms) == 0:
		return syms.get('0','0')
	elif len(terms) == 1:
		return exprStr(terms[0], syms, par)
	else:
		termStrs = map(lambda term: exprStr(term, syms, 0), terms)
		termsStr = syms.get('+','+').join(termStrs)
		if par > 0:
			return syms.get('(','(') + termsStr + syms.get(')',')')
		else:
			return termsStr

def prodStr(terms, syms=dict(), par=0):
	if len(terms) == 0:
		return syms.get('1','1')
	elif len(terms) == 1:
		return exprStr(terms[0], syms)
	else:
		termStrs = map(lambda term: exprStr(term, syms, 1), terms)
		termsStr = syms.get('*','').join(termStrs)
		if par > 1:
			return syms.get('(','(') + termsStr + syms.get(')',')')
		else:
			return termsStr


LATEX_SYMS = {
	'A': r'{\rm A}', 'B': r'{\rm B}', 'C': r'{\rm C}', 'D': r'{\rm D}',
	'!A': r'\hspace{0.125em}\rule[2ex]{0.45em}{0.75pt}\kern-0.575em{\rm A}',
	'!B': r'\hspace{0.1em}\rule[2ex]{0.45em}{0.75pt}\kern-0.55em{\rm B}',
	'!C': r'\hspace{0.15em}\rule[2ex]{0.45em}{0.75pt}\kern-0.6em{\rm C}',
	'!D': r'\hspace{0.1em}\rule[2ex]{0.45em}{0.75pt}\kern-0.55em{\rm D}',
	'+': r'\hspace{0.25em}\raisebox{0.2ex}{+}\hspace{0.25em}',
	'(': r'{\raisebox{0.2ex}{(}', ')': r'\raisebox{0.2ex}{)}}',
	'*': '',
	'!': r'\overline',
	'{': '{', '}': '}',
}

MATHJAX_SYMS = {
	'A': r'\mathrm{A}', 'B': r'\mathrm{B}',
	'C': r'\mathrm{C}', 'D': r'\mathrm{D}',
	'!A': r'\hspace{0.125em}\rule[2ex]{0.45em}{0.75pt}\kern-0.575em{\mathrm{A}}',
	'!B': r'\hspace{0.1em}\rule[2ex]{0.45em}{0.75pt}\kern-0.55em{\mathrm{B}}',
	'!C': r'\hspace{0.15em}\rule[2ex]{0.45em}{0.75pt}\kern-0.6em{\mathrm{C}}',
	'!D': r'\hspace{0.1em}\rule[2ex]{0.45em}{0.75pt}\kern-0.55em{\mathrm{D}}',
	'+': r'\hspace{0.25em}\raise{0.2ex}{+}\hspace{0.25em}',
	'(': r'{\raise{0.2ex}{(}', ')': r'\raise{0.2ex}{)}}',
	'*': '',
	'!': r'\neg'
}

def exprMathJaxStr(expr):
	return exprStr(expr, MATHJAX_SYMS)

def exprLatexStr(expr):
	return exprStr(expr, LATEX_SYMS)
	
SYMPY_SYMS = {
    '+': ' | ',  # Use | for OR
    '*': ' & ',  # Use & for AND (the default '' is implicit, which SymPy won't parse)
    '!': '~',    # Use ~ for NOT
    '(': '(',    # Parentheses are the same
    ')': ')',
    '0': '0',    # Constants are the same
    '1': '1'
}

def exprSympyStr(expr):
    """
    A wrapper for exprStr that outputs a SymPy-parseable string.
    
    It calls the original exprStr but provides the SYMPY_SYMS
    dictionary to override the default output format.
    """
    return exprStr(expr, syms=SYMPY_SYMS)

def exprShuffled(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return notExpr(exprShuffle(arg))
		elif op == 0 or op == AND:
			return {op: tuple(map(exprShuffle, sample(arg, len(arg))))}
		else:
			return expr
	else:
		return expr

def exprSortKey(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return exprSortKey(arg)+1
		elif op == OR or op == AND:
			return 32*len(arg)+reduce(lambda x, y: x+exprSortKey(y), arg, 0)
		else:
			return None
	elif type(expr) is int:
		return 32*expr
	else:
		return None
		

def exprSorted(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return mkNot(exprSorted(arg))
		elif op == OR or op == AND:
			return {op: tuple(sorted(map(exprSorted, arg), key=exprSortKey))}
		else:
			return expr
	else:
		return expr

def randNumTerms(numDice, dieSides, addConst = 0):
	result = addConst
	for i in range(numDice):
		result += 1 + randrange(dieSides)
	return max(0,result)

def randNeg(expr):
	if randrange(2):
		return mkNot(expr)
	else:
		return expr

def randLit(numVars):
	return randNeg(randrange(numVars))

def randExpr(numVars, minDepth = 2, maxDepth = 2, params = dict()):
	return randOpExpr(randrange(2), numVars, minDepth, maxDepth, params)

def randOpExpr(op, numVars, minDepth, maxDepth, params):
	numTerms = params.get('numTerms',numVars)
	numSubs = params.get('numSubs',numVars)
	numBlanks = params.get('numBlanks',1)
	
	if type(numTerms) is tuple:
		numTerms = randNumTerms(*numTerms)
		
	preTerms = list()
	
	if maxDepth == 0:
		return randLit(numVars)
	
	if maxDepth == 1:
		protoTerms = list(range(numVars)) + [None] * numBlanks
	elif minDepth > 0:
		protoTerms = [()] * numTerms	
	else:
		protoTerms = list(range(numVars)) + [None] * numBlanks + [()] * numSubs
		
	numTerms = min(numTerms, len(protoTerms))
	protoTerms = sample(protoTerms, numTerms)
	
	terms = list()
	
	for protoTerm in protoTerms:
		if type(protoTerm) is tuple:
			expr = randOpExpr(1 - op, numVars, minDepth - 1, maxDepth - 1, params)
			terms.append(expr)
		elif type(protoTerm) is int:
			expr = randNeg(protoTerm)
			terms.append(expr)
	
	if len(terms) != 1:
		return {op:tuple(terms)}
	else:
		return terms[0]

# Idea: Have arguments min0s, max0s, min1s, max1s, minXs, maxXs, which may be
# None, and then choose uniformly at random among all satisfying configurations.

def randTab(numVars, min1s = 1, max1s = -1, minXs = 0, maxXs = 0):
	numRows = 2**numVars
	
	if min1s < 0:
		min1s = numRows + min1s
	if max1s < 0:
		max1s = numRows + max1s
	max1s = min(max1s, numRows)
	if max1s < min1s:
		return None
	
	if minXs < 0:
		minXs = numRows + minXs
	if maxXs < 0:
		maxXs = numRows + maxXs
	maxXs = min(maxXs, numRows)
	if maxXs < minXs:
		return None
	
	if numRows < min1s + minXs:
		return None
	
	act1s = randint(min1s, max1s)
	
	maxXs = min(maxXs, numRows - act1s)
	minXs = min(minXs, maxXs)
	actXs = randint(minXs, maxXs)
	
	act0s = numRows - act1s - actXs
	
	tt = [0] * act0s + [1] * act1s + [None] * actXs
	shuffle(tt)
	
	return tuple(tt)

def exprArea(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return 1 + exprArea(arg) if type(arg) is dict else 1
		elif op == OR or op == AND:
			return 1 + reduce(lambda x,t: x+exprArea(t), arg, 0)
		else:
			return None
	elif type(expr) is int:
		return 1

def exprDelay(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			return 1 + exprDelay(arg) if type(arg) is dict else 0
		elif op == OR or op == AND:
			return 1 + reduce(lambda x,t: max(x,exprDelay(t)), arg, 0)
		else:
			return None
	elif type(expr) is int:
		return 0

def exprSimplify(expr):
	if type(expr) is dict:
		op, arg = list(expr.items())[0]
		if op == NOT:
			# Apply DeMorgan's Law
			return exprNeg(arg)
		
		elif op == OR or op == AND:
			terms = map(exprSimplify, arg)
			
			# First pass: merge sub-expressions of same type. Note that this
			# also automatically applies the identities A+0=A and A*1=A
			
			newTerms = list()
			for term in terms:
				if type(term) is dict:
					subOp, subArg = list(term.items())[0]
					if op == subOp:
						newTerms += subArg
						continue
				newTerms.append(term)
			
			terms = newTerms
			
			if len(terms) == 1:
				return terms[0]
			
			# Second pass: find first occurrence of each literal and apply
			# A*0 and A+1 identity rules.

			posVars = set() # positive variables seen
			negVars = set() # negative variables seen
			extras = set() # Redundant terms to remove
			
			for i in range(len(terms)):
				term = terms[i]
				if type(term) is dict:
					subOp, subArg = list(term.items())[0]
					if subOp == NOT and type(subArg) is int:
						if subArg not in negVars:
							negVars.add(subArg)
						else:
							extras.add(i)
					# Short-circuit A*0=0
					elif op == AND and subOp == OR and len(subArg) == 0:
						return ZERO
					# Short-circuit A+1=1
					elif op == OR and subOp == AND and len(subArg) == 0:
						return ONE
				elif type(term) is int:
					if term not in posVars:
						posVars.add(term)
					else:
						extras.add(i)
			
			# Apply B+!B = 1 and B*!B = 0 identities
			if not posVars.isdisjoint(negVars):
				return ONE if op == OR else ZERO
			
			# Third pass: Remove redundant terms (applies A+A=A and A*A=A)
			terms = [terms[i] for i in range(len(terms)) if i not in extras]
			
			return {op:tuple(terms)}
				
	return expr

# BOOLEAN EXPRESSION PARSING

# We use pyparsing (as pp) to parse Boolean expressions. Variables are
# single letters. The syntax is fairly permissive, and allows any mix of
# the following:
# 
# 1. Negation may be written as !A or A'
# 2. Conjunction may be written as AB, A*B, or A&B
# 3. Disjunction may be written as A+B or A|B
# 

ppExpr = pp.Forward()
ppPar = '(' + ppExpr + ')'
ppVar = pp.Char(pp.alphas)
ppConst = pp.Char("01")
ppAtom = ppPar | ppConst | ppVar
ppNeg = pp.ZeroOrMore('!') + ppAtom + pp.ZeroOrMore("'")
ppProd = ppNeg + pp.ZeroOrMore(ppNeg | (pp.Char("*&") + ppNeg))
ppExpr <<= ppProd + pp.ZeroOrMore(pp.Char("+|") + ppProd)

def ppVarAction(toks):
	c = toks[0]
	if 'A' <= c and c <= 'Z':
		return ord(c) - ord('A')
	elif 'a' <= c and c <= 'z':
		return ord(c) - ord('a')
	else:
		return None

def ppConstAction(toks):
	return {int(toks[0]):()}

def ppParAction(toks):
	return toks[1]

def ppNegAction(toks):
	expr = list(filter(lambda t: type(t) is not str, toks))[0]
	for i in range(len(toks)-1):
		expr = notExpr(expr)
	return expr

def ppProdAction(toks):
	if len(toks) != 1:
		return mkAnd(filter(lambda t: t != '*', toks))
	else:
		return toks[0]

def ppExprAction(toks):
	if len(toks) != 1:
		return mkOr(filter(lambda t: t != '+', toks))
	else:
		return toks[0]

ppPar.setParseAction(ppParAction)
ppVar.setParseAction(ppVarAction)
ppConst.setParseAction(ppConstAction)
ppNeg.setParseAction(ppNegAction)
ppProd.setParseAction(ppProdAction)
ppExpr.setParseAction(ppExprAction)

def parseExpr(s):
	return ppExpr.parseString(s, parseAll=True)[0]

def parseExprWithErr(s):
	try:
		return parseExpr(s)
	except pp.ParseException as e:
		prefix = s[:e.column-1]
		badch = s[e.column-1:e.column]
		suffix = s[e.column:]
		return (prefix,badch,suffix)