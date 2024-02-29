# does Chickasaw have more vowels than this?
def is_vowel(self, c1):
    return c1 in ['a', 'o', 'u', 'i', 'e']

def is_letter(self, c1, c2):
    return c1 == c2

vowels = ['a', 'o', 'u', 'i', 'e']

class Network:
    inputs = []
    outputs = []
    states = []
    nodes = {}

    def __init__(self, is_ISL=True):
        print("--Finite State Transducer--")

        # operations for initial prefixation node
        # should be able to accept functions as well as letters
        prefixation_node = StateNode('λ', is_ISL=True, k=1)
        prefixation_node.add_input_operation(['0'], 'ik', 'START')

        # opertaions for initial node
        initial_node = StateNode('START', is_ISL=True, k=1) # the node first visited after prefixation
        initial_node.add_input_operation(['1'], 'o', 'TERMINATE') # move to state END and suffix an o if it ends
        initial_node.add_input_operation(vowels, 'λ', 'V') # move to state V if there's a vowel
        initial_node.set_defaults(default_output='?',default_next_state='?') # move to ? for all remaining letters

        # default_node
        default_node = StateNode('?', is_ISL=True, k=1)
        default_node.set_defaults(default_output='?',default_next_state='?')
        default_node.add_input_operation(vowels, 'λ', 'V')
        default_node.add_input_operation(['1'], 'o','TERMINATE')

        # V node
        vowel_node = StateNode('V', is_ISL=True, k=1)
        vowel_node.set_defaults(default_output='Vλ', default_next_state='?') # this needs to reference the input, which is why it's k=2
        vowel_node.add_input_operation(['1'], 'o','TERMINATE')
        vowel_node.add_input_operation('V','V','V')

        self.nodes = {
            prefixation_node.state: prefixation_node,
            initial_node.state: initial_node,
            default_node.state: default_node,
            vowel_node.state: vowel_node
        }
        for n in self.nodes.keys():
            print(self.nodes[n].default)
            print(self.nodes[n].functions)

    def run(self, word: str):
        # ASSUME K=1 FOR FIRST IMPLEMENTATION
        # SHOULD TERMINATE WHEN THE NEXT STATE IS NONE
        next_state = 'λ'

        for char in word:
            output, curr_state, next_state = self.nodes[next_state].iterate(char)

            self.inputs.append(char)
            self.outputs.append(output)
            self.states.append(curr_state)

            print(">----")
            print(self.inputs)
            print(self.states)
            print(self.outputs)
            print("Current State: ", curr_state)
            print("Current Char: ", char)
            print("Current Output: ", output)
            print("Next State: ", next_state)
            print("---->")

            if next_state == "TERMINATE":
                break

class StateNode:
    def __init__(self, state, is_ISL=True, k=1):
        self.default = {}
        self.functions = []
        self.k = 1
        self.state = state
        self.set_defaults(None, None)

    # what if there is no next state?
    def add_input_operation(self, letter_input, letter_output, next_state):
        for letter in letter_input:
            self.functions.append([letter, letter_output, next_state])

    def set_defaults(self, default_output, default_next_state):
        self.default['output'] = default_output
        self.default['next_state'] = default_next_state

    def iterate(self, provided_input: str):
        next_state = ""
        for i, o, next_state in self.functions:
            if provided_input == i:
                print(f"Valid match of {provided_input} for output {o} and next state {next_state}")
                return o, self.state, next_state
        print(f"Returning defaults for state {self.state} on input {provided_input}")
        return self.default['output'], self.state, self.default['next_state']

def main():
    network = Network()
    network.run("0lakna1")

if __name__ == "__main__":
    main()
