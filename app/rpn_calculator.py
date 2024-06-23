# app/rpn_calculator.py
def evaluate_rpn(expression: str) -> float:
    stack = []
    operators = {'+', '-', '*', '/'}

    for token in expression.split():
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
        else:
            stack.append(float(token))
    return stack.pop()
