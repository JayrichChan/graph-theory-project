# Jayrich Chan
# Shunting Yard Algorithm

def shunt(infix):
    """The Shunting Yard Algorithm for converting infix regular expressions
       to postfix. """

    # Special characters for regular expressions and their precedence.
    specials = {'*': 50, '.': 40, '|': 30, '+': 35}
    
    # Will eventually be the output.
    pofix = ""
    # Operator stack.
    stack = ""
    
    # Loop through the string a character at a time.
    for c in infix:
        # If an open bracket, push to the stack.
        if c == '(':
            stack = stack + c
        # If a closing bracket, pop from stack, push to output until open bracket.
        elif c == ')':
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # If it's an operator, push to stack after popping lower or equal precedence.
        # operators from top of stack into output.
        elif c in specials:
            while stack and specials.get(c, 0) <= specials.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        # Regular characters are pushed immediately to the output.
        else:
            pofix = pofix + c
    # Pop all remaining operators from stack to output.
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix

# Thompson's construction

# Represents a state with two arrows, labelled by label.
# User None for a label representing "e" arrows.
class state:
    label = None
    edge1 = None
    edge2 = None

# An NFA is represented by its initial accept states.
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept

def compile(pofix):
    """Compiles a postfix regular expression into an NFA."""

    nfastack = []
    
    for c in pofix:
        # Since it's a stack, so it's last in first out
        if c == '.':
            # Pop two NFA's off the stack.
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect first NFA's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial
            # Push NFA to the stack
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)
        elif c == '|':
            # Pop two NFA's off the stack.
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Create a new initial state, connect it to initial states
            # of the two NFA's popped from the state.
            initial, accept = state(), state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # Create a new accept state, connecting the accept states
            # of the two NFA's popped from the stack, to the new state.
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # Push new NFA to the stack.
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)
        elif c == '*':
            # Pop a single NFA from the stack.
            nfa1 = nfastack.pop()
            # Create new initial and accept states.
            initial, accept = state(), state()
            # Join the new initial state to nfa's initial state and the new accept state.
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # Join the old accept state to the new accept state and nfa's initial state.
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # Push the new NFA to the stack
            newnfa = nfa(initial,accept)
            nfastack.append(newnfa)
        else:    
            # Create new initial and accept states.
            accept, initial = state(), state()
            # Join the initial state to the accept state using an arrow labelled c.
            initial.label = c
            initial.edge1 = accept
            # Push the new NFA to the stack.
            nfastack.append(nfa(initial, accept))

    # nfastack should only have a single nfa on it at this point.
    return nfastack.pop()
    
def followes(state):
    """Return the set of states that can be reached from state following e arrows."""
    # Create a new set, with state as its only member.
    states = set()
    states.add(state)

    # Check if state has arrows labelled e from it.
    if state.label is None:
        # Check if edge1 is a state.
        if state.edge1 is not None:
            # If there's an edge1, follow it.
            states |= followes(state.edge1)
        # Check if edge2 is a state.
        if state.edge2 is not None:
            # If there's an edge2, follow it.
            states |= followes(state.edge2)

    # Return the set of states.
    return states

def match(infix, string):
    """Matches string to infix regular expression."""

    # Shunt and compile the regular expression.
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The current set of states and the next set of states.
    current = set()
    next = set()

    # Add the initial state to the current list.
    current |= followes(nfa.initial)

    # Loop through each character in the string
    for s in string:
        # Loop through the current set of states.
        for c in current:
            # Check if that state is labelled s.
            if c.label == s:
                # Add the edge1 state to the next set.
                next |= followes(c.edge1)
        # Set current to next, and clear out next.
        current = next
        next = set()

    # Check if the accept state is in the set of current states.
    return (nfa.accept in current)

# A few tests.
infixes = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c", "a.b.c.d+"]
strings = ["", "abc", "abbc", "abad", "abbbc", "abcdd"]

for i in infixes:
    for s in strings:
        print(match(i,s), i, s)