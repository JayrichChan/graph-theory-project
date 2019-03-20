# Thompson's construction
# Jayrich Chan

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
            accept = state()
            initial = state()
            # Join the initial state to the accept state using an arrow labelled c.
            initial.label = c
            initial.edge1 = accept
            # Push the new NFA to the stack.
            nfastack.append(nfa(initial, accept))

    # nfastack should only have a single nfa on it at this point.
    return nfastack.pop()
    
print(compile("ab.cd.|"))
print(compile("aa.*"))

