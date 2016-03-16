# Write a C program to do the following:
# Input: A regular expression on the alphabet {a,b...}.
# Output: The minimal DFA for the regular expression
# In addition, you must write a program to simulate the DFA on any possible input.
import re

print "Input: A regular expression on the alphabet {a,b...}.\n e implies 'epsilon'"
print "Supported (, ), |, *, .\n"
re_input = raw_input()

state_list = []
for i in range(50, 0, -1):
    state_list.append(i)


class Node:
    def __init__(self, initdata):
        self.state = initdata
        self.list = []
        self.start_state = False
        self.accept_state = False

    def get_state(self):
        return self.state

    def get_list(self):
        return self.list

    def get_start_state(self):
        return self.start_state

    def get_accept_state(self):
        return self.accept_state

    def get_connecting_alphabet(self, state):
        output = []
        for i in self.list:
            if i[0] == state.get_state():
                output.append(i[1])
        return output

    def get_connecting_state_num(self, alphabet):
        output = []
        for i in self.list:
            if i[1] == alphabet:
                output.append(i[0])
        return output

    def set_state(self, new_data):
        self.state = new_data

    def set_start_state(self, new_data):
        self.start_state = new_data

    def set_accept_state(self, new_data):
        self.accept_state = new_data

    def display(self):
        print "State : " + str(self.state)
        print "Connection list : " + str(self.list)
        if self.start_state:
            print "Start state"
        if self.accept_state:
            print "Accept state"

    def add_link(self, next_state, alphabet):
        for i in self.list:
            if i == (next_state, alphabet):
                return
        self.list.append((next_state, alphabet))

    def rmv_link(self, state, alphabet):
        self.list.remove((state, alphabet))


list_of_states = []

start_state = Node(state_list.pop())
start_state.set_start_state(True)
list_of_states.append(start_state)
accept_state = Node(state_list.pop())
accept_state.set_accept_state(True)
list_of_states.append(accept_state)


def compose(state1, re_str, state2):
    re_string = re_str
    depth = 0
    count = 0
    starts_with_braces = False
    # check for external braces
    for component in re_string:
        count += 1
        if component == "(":
            depth += 1
        if component == ")":
            depth -= 1

        if component == "(" and count == 1:
            starts_with_braces = True
        if component == ")" and starts_with_braces and count == len(re_string):
            re_string = re_str.split("(")[1].split(")")[0]

    depth = 0
    count = 0
    # check existence of |
    for component in re_string:
        count += 1
        if component == "(":
            depth += 1
        if component == ")":
            depth -= 1
        if component == "|" and depth == 0:
            x = re_string[:count - 1]
            y = re_string[count:]

            new_state1 = Node(state_list.pop())
            state1.add_link(new_state1.get_state(), "e")
            new_state2 = Node(state_list.pop())
            new_state2.add_link(state2.get_state(), "e")
            compose(new_state1, x, new_state2)

            new_state3 = Node(state_list.pop())
            state1.add_link(new_state3.get_state(), "e")
            new_state4 = Node(state_list.pop())
            new_state4.add_link(state2.get_state(), "e")
            compose(new_state3, y, new_state4)

            list_of_states.append(new_state1)
            list_of_states.append(new_state2)
            list_of_states.append(new_state3)
            list_of_states.append(new_state4)
            return 1

    # split braces
    depth = 0
    count = 0
    starts_with_braces = False
    for component in re_string:
        count += 1
        # abc...(ijk...)...
        if component == "(" and count > 1 and depth == 0:
            depth += 1
            x = re_string[:count - 1]
            y = re_string[count - 1:]

            new_state = Node(state_list.pop())
            compose(state1, x, new_state)
            compose(new_state, y, state2)
            list_of_states.append(new_state)
            return 1
        # (abc...
        elif component == "(" and count == 1:
            depth += 1
            starts_with_braces = True

        # (abc...xyz)
        if component == ")" and starts_with_braces and depth == 1 and count == len(re_string):
            depth -= 1
            compose(state1, re_string.split("(")[1].split(")")[0], state2)
            return 1
        # (abc..ijk)*
        elif component == ")" and starts_with_braces and depth == 1 and re_string[count] == '*' and count + 1 == len(
                re_string):
            depth -= 1
            state1.add_link(state2.get_state(), 'e')
            new_state1 = Node(state_list.pop())
            new_state2 = Node(state_list.pop())
            compose(new_state1, re_string.split("(")[1].split(")*")[0], new_state2)
            state1.add_link(new_state1.get_state(), "e")
            new_state2.add_link(state2.get_state(), "e")
            new_state2.add_link(new_state1.get_state(), "e")

            list_of_states.append(new_state1)
            list_of_states.append(new_state2)
            return 1
        # (abc..ijk)*lmn...xyz
        elif component == ")" and starts_with_braces and depth == 1 and re_string[count] == '*' and count != len(
                re_string):
            depth -= 1
            x = re_string[:count + 1]
            y = re_string[count + 1:]
            new_state = Node(state_list.pop())
            compose(state1, x, new_state)
            compose(new_state, y, state2)
            list_of_states.append(new_state)
            return 1
        # (abc..ijk)lmn...xyz
        elif component == ")" and starts_with_braces and depth == 1 and count != len(re_string):
            depth -= 1
            x = re_string[:count]
            y = re_string[count:]
            new_state = Node(state_list.pop())
            compose(state1, x, new_state)
            compose(new_state, y, state2)
            list_of_states.append(new_state)
            return 1
        # abc...(i...z)
        elif component == ")" and not starts_with_braces:
            depth -= 1

    # split concatenations
    # empty string
    if len(re_string) == 0:
        state1.add_link(state2.get_state(), "e")
        return 1
    # a
    elif len(re_string) == 1:
        state1.add_link(state2.get_state(), re_string)
        return 1
    # ab....
    elif len(re_string) > 1 and re.match(r'^\w\w', re_string):
        x = re_string[:1]
        y = re_string[1:]
        new_state = Node(state_list.pop())
        compose(state1, x, new_state)
        compose(new_state, y, state2)
        list_of_states.append(new_state)
        return 1
    # a*
    elif len(re_string) == 2 and re.match(r'^\w\*$', re_string):
        state1.add_link(state2.get_state(), 'e')
        new_state1 = Node(state_list.pop())
        new_state2 = Node(state_list.pop())
        new_state1.add_link(new_state2.get_state(), re_string[:1])
        state1.add_link(new_state1.get_state(), "e")
        new_state2.add_link(state2.get_state(), "e")
        new_state2.add_link(new_state1.get_state(), "e")

        list_of_states.append(new_state1)
        list_of_states.append(new_state2)
        return 1
    # a*....
    elif len(re_string) >= 2 and re.match(r'^\w\*', re_string):
        new_state3 = Node(state_list.pop())
        state1.add_link(new_state3.get_state(), 'e')
        new_state1 = Node(state_list.pop())
        new_state2 = Node(state_list.pop())
        new_state1.add_link(new_state2.get_state(), re_string[:1])
        state1.add_link(new_state1.get_state(), "e")
        new_state2.add_link(new_state3.get_state(), "e")
        new_state2.add_link(new_state1.get_state(), "e")
        compose(new_state3, re_string[2:], state2)

        list_of_states.append(new_state1)
        list_of_states.append(new_state2)
        list_of_states.append(new_state3)
        return 1

    return 1


compose(start_state, re_input, accept_state)
print "\n E NFA :"
for i in list_of_states:
    i.display()


# enfa -> nfa
def modify_start_state(state):
    global start_state
    start_state = state


def modify_accept_state(state):
    global accept_state
    accept_state = state


# state1 and state2 is merged and state2 is removed
def join_states(state1, state2):
    s1 = state1.get_state()
    s2 = state2.get_state()
    # connecting between two states is merged
    for alphabet in state2.get_connecting_alphabet(state1):
        state1.add_link(s1, alphabet)
        state2.rmv_link(s1, alphabet)
    for alphabet in state1.get_connecting_alphabet(state2):
        state1.rmv_link(s2, alphabet)
        state1.add_link(s1, alphabet)
    for alphabet in state2.get_connecting_alphabet(state2):
        state1.add_link(s1, alphabet)
        state2.rmv_link(s2, alphabet)
    # connection incoming to and outgoing from state2 is managed
    for link in state2.get_list():
        state1.add_link(link[0], link[1])
        state2.rmv_link(link[0], link[1])
    for state in list_of_states:
        for alphabet in state.get_connecting_alphabet(state2):
            state.rmv_link(s2, alphabet)
            state.add_link(s1, alphabet)

    # check start and accept state of state2
    if state2.get_start_state():
        state1.set_start_state(True)
        modify_start_state(state1)
    if state2.get_accept_state():
        state1.set_accept_state(True)
        modify_accept_state(state1)

    # debug adjustment for a|b|c
    for link in state2.get_list():
        print link
        state1.add_link(link[0], link[1])
        state2.rmv_link(link[0], link[1])
    # delete state2
    state_list.append(state2.get_state())
    state_list.sort(reverse=True)
    list_of_states.remove(state2)

    # check for an epsilon self-loop
    for link in state1.get_list():
        if link[0] == state1.get_state() and link[1] == 'e':
            state1.rmv_link(link[0], link[1])

    return 1


def find_state(state_id):
    for state in list_of_states:
        if state.get_state() == state_id:
            return state
    return None


def epsilon_connections(state):
    output = 0
    for link in state.get_list():
        if link[1] == "e":
            output += 1
    return output


def join_satisfying_states(state1, state2):
    list1 = state1.get_list()
    for link1 in list1:
        if link1[0] == state2.get_state():
            list1.remove(link1)
    for link2 in state2.get_list():
        for link1 in list1:
            if link1 == link2:
                list1.remove(link2)
    if not list1:
        return True
    else:
        return False


def epsilon_state_join(state):
    if state.get_start_state():
        while epsilon_connections(state) > 0:
            for link in state.get_list():
                if link[1] == "e":
                    print "Joining states " + str(state.get_state()) + "  " + str(
                        find_state(link[0]).get_state()) + "\n"
                    join_states(state, find_state(link[0]))
    else:
        while epsilon_connections(state) > 0:
            for link in state.get_list():
                if link[1] == "e":
                    if join_satisfying_states(state, find_state(link[0])):
                        print "Joining states " + str(state.get_state()) + "  " + str(
                            find_state(link[0]).get_state()) + "\n"
                        join_states(state, find_state(link[0]))
                    else:
                        print "Removing link " + str(state.get_state()) + " on alphabet " + str(link[1]) + " -> " + str(
                            link[0])
                        # state.rmv_link(link[0], link[1])
                        join_states(state, find_state(link[0]))


def e_closure_of_state(state):
    output = [state]
    for link in state.get_list():
        if link[1] == 'e':
            output.append(find_state(link[0]))
            for i in e_closure_of_state(find_state(link[0])):
                output.append(i)
    return output


class SuperNode:
    def __init__(self, initdata):
        self.node_num = initdata
        self.node_list = []
        self.node_super_links = []
        self.node_links = []
        self.start_state = False
        self.accept_state = False

    def get_node_num(self):
        return self.node_num

    def get_node_list(self):
        return self.node_list

    def get_node_super_link(self):
        return self.node_super_links

    def get_node_link(self):
        return self.node_links

    def get_next_states_on_alphabet_e(self, alphabet):
        output = []
        output2 = []
        for link in self.node_links:
            if link[2] == alphabet:
                output.append(link[1])
        for i in output:
            for state in e_closure_of_state(find_state(i)):
                output2.append(state.get_state())
        output = output + output2
        return output

    def display(self):
        print "Nfa state : " + str(self.node_num)
        print "e-nfa states : " + str(self.node_list)
        print "Links : " + str(self.node_super_links)
        if self.start_state:
            print "Start state"
        if self.accept_state:
            print "Accept state"

    def add_node_super_link(self, state, alphabet):
        self.node_super_links.append((state, alphabet))

    def add_node(self, node):
        for i in self.get_node_list():
            if i == node.get_state():
                return 0
        self.node_list.append(node.get_state())
        if node.get_start_state():
            self.start_state = True
        if node.get_accept_state():
            self.accept_state = True
        for link in node.get_list():
            self.node_links.append((node.get_state(), link[0], link[1]))


list_of_nfa_states = []

start_nfa_state = SuperNode(state_list.pop())
list_of_nfa_states.append(start_nfa_state)

death_nfa_state = SuperNode(state_list.pop())
list_of_nfa_states.append(death_nfa_state)


for state in e_closure_of_state(start_state):
    start_nfa_state.add_node(state)

# display nfa
print "\n\nNFA :"
for i in list_of_nfa_states:
    i.display()
print start_nfa_state.get_next_states_on_alphabet_e('a')
