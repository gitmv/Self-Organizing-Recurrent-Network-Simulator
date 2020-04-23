from NetworkBehaviour.Logic.Basics.BasicHomeostasis import *


class Easy_neuron_initialize(Neuron_Behaviour):

    def set_variables(self, neurons):
        self.add_tag('Easy_neuron_initialize')

        #create neuron group variables
        neurons.activity = neurons.get_neuron_vec()
        neurons.output = neurons.get_neuron_vec()
        # equivalent to: np.zeros(neurons.size)

        syn_density = self.get_init_attr('syn_density', 0.1, neurons)
        neurons.syn_norm = self.get_init_attr('syn_norm', 0.8, neurons)

        #create random synapse weights
        for synapse_group in neurons.afferent_synapses['GLUTAMATE']:
            synapse_group.W = synapse_group.get_random_synapse_mat(density=syn_density)
            synapse_group.enabled*=synapse_group.W>0
            #synapse_group.get_synapse_mat() #equivalent to np.zeros(s.get_synapse_mat_dim())

        self.normalize_synapse_attr('W', 'W', neurons.syn_norm, neurons, 'GLUTAMATE')

    def new_iteration(self, neurons):
        neurons.activity *= 0.0


class Easy_neuron_collect_input(Neuron_Behaviour):

    def set_variables(self, neurons):
        self.add_tag('Easy_neuron_collect_input')
        neurons.sensitivity = self.get_init_attr('sensitivity', 1.0, neurons)
        neurons.noise_density = self.get_init_attr('noise_density', 0.01, neurons)
        neurons.noise_strength = self.get_init_attr('noise_strength', 0.1, neurons)

    def new_iteration(self, neurons):
        for s in neurons.afferent_synapses['GLUTAMATE']:
            s.dst.activity += s.W.dot(s.src.output)*neurons.sensitivity

        neurons.activity += neurons.get_random_neuron_vec(density=neurons.noise_density)*neurons.noise_strength


class Easy_neuron_generate_output(Neuron_Behaviour):

    def set_variables(self, neurons):
        self.add_tag('Easy_neuron_generate_output')
        neurons.TH = self.get_init_attr('threshold', 0.5, neurons)

    def new_iteration(self, neurons):
        neurons.output = (neurons.activity > (neurons.TH+neurons.refractory_counter)).astype(np.float64)

class Easy_neuron_Refractory(Neuron_Behaviour):

    def set_variables(self, neurons):
        self.add_tag('Refractory')
        neurons.refractory_counter = neurons.get_neuron_vec()
        self.decay = self.get_init_attr('decay', 0.9, neurons)

    def new_iteration(self, neurons):
        neurons.refractory_counter *= self.decay
        neurons.refractory_counter += neurons.output