import numpy as np
import random




class LNED(object):

    def __init__(self, alpha=0.01, alpha_ud=0.1, beta=0.1, beta_ud=0.1, beta_bg=0.1, beta_ms=0.01, gamma_1=0.01, gamma_2=1, gamma_3=2):
        self.alpha = alpha
        self.alpha_ud = alpha_ud
        self.beta = beta
        self.beta_ud = beta_ud
        self.beta_bg = beta_bg
        self.beta_ms = beta_ms
        self.gamma_1 = gamma_1
        self.gamma_2 = gamma_2
        self.gamma_3 = gamma_3
        
    
    def _initialize(self, d_surround, d_c):
        #NOTE: For the moment working only with d_surround, we have to add dc
        #assign voc_size and create a dictionary with the index position of every word
        #words = np.unique([item for sublist in (d_surround + dc) for item in sublist])
        words = list(set([item for sublist in d_surround for item in sublist]))
        n_docs = len(d_surround)
        self.voc_size = len(words)
        self.idx_w = {}
        for w in words:
            self.idx_w[w] = words.index(w)
        #assign self.num_candidates, create list of regular topics, and index position of every regular index
        self.num_candidates = len(d_c)
        self.candidate_topics = [str(i) for i in xrange(self.num_candidates)]
        self.regular_topics = self.candidate_topics + ['ud'] #undefined topic is added at the end of candidate topics
        self.idx_reg_z = {}
        for z in self.regular_topics:
            self.idx_reg_z[z] = self.regular_topics.index(z)
        #init counts to 0 
        self.n_bg_w = np.zeros(self.voc_size)
        self.n_bg = 0
        self.n_bg_d = np.zeros(n_docs)
        self.n_reg_d_z = np.zeros((n_docs, len(self.regular_topics))) 
        self.n_reg_d = np.zeros(n_docs)
        self.n_reg_w_z = np.zeros((self.voc_size, len(self.regular_topics))) 
        self.n_reg_z = np.zeros(len(self.regular_topics))
        self.n_ms_w_d = np.zeros((self.voc_size, n_docs))
        self.n_ms_d = np.zeros(n_docs)
        self.topics = {} #dictionary for the assignation of every word
        #loop for every doc and word
        for i in xrange(len(d_surround)):
            for j in xrange(len(d_surround[i])):
                w = self.idx_w[d_surround[i][j]]
                #assign a topic randomly to each word
                z,t = self._get_random_topic()
                #update counts
                self._update_counts(1, z, t, w, i)
                #assign the topic
                self.topics[(i, j)] = (z,t)
    
                
    
    def _update_counts(self, value, z, t, w, d):
        if t == 0:
            self.n_bg_w[w] += value
            self.n_bg += value
            self.n_bg_d[d] += value
        if t == 1:
            c_idx = self.idx_reg_z[z]
            self.n_reg_d_z[d, c_idx] += value
            self.n_reg_d[d] += value
            self.n_reg_w_z[w, c_idx] += value
            self.n_reg_z[c_idx] += value
        if t == 2:
            self.n_ms_w_d[w, d] += value
            self.n_ms_d[d] += value
            
    def _get_random_topic(self):
        topics = self.regular_topics + ['bg'] + ['ms']
        z = random.choice(topics)
        t = 1
        if z == 'bg':
            t = 0
        elif z == 'ms':
            t = 2
        return z,t
        
    def sample_topic(self, p_bg, p_reg, p_ms):
        """
        Sample from the Multinomial distribution and return the sample index.
        First
        """
        topics = self.regular_topics + ['bg'] + ['ms']
        p = p_reg + [p_bg] + [p_ms] 
        # normalize to obtain probabilities
        p /= np.sum(p)
        idx = np.random.multinomial(1,p).argmax()
        z = topics[idx]
        t = 1
        if z == 'bg':
            t = 0
        elif z == 'ms':
            t = 2
        return z,t
    
    def run(self, d_surround, d_c, max_iter=100):
        print 'start...'
        self._initialize(d_surround, d_c)
        for it in xrange(max_iter):
            print 'iteration ' + str(it) + ' of ' + str(max_iter)
            for i in xrange(len(d_surround)):
                for j in xrange(len(d_surround[i])):
                    w = self.idx_w[d_surround[i][j]]
                    #get z for this word and discount 1 to the counts
                    z,t = self.topics[i,j]
                    self._update_counts(-1, z, t, w, i)
                    #get probability distribution p(t,z)
                    p_bg, p_reg, p_ms = self._get_joint_dist_t_z(i, w)
                    #sample form the obtained distribution
                    z,t = self.sample_topic(p_bg, p_reg, p_ms)
                    #update counts
                    self._update_counts(1, z, t, w, i)
                    #assign the topic
                    self.topics[(i, j)] = (z,t)
        print 'finish...'
                    
    def _get_joint_dist_t_z(self, d, w):
        p_bg = self._get_p_bg(d, w)
        p_reg = []
        for c in self.regular_topics: #regular topics include ud(undefined)
            c_idx = self.idx_reg_z[c]
            p_reg.append(self._get_p_reg(d, w, c_idx))
        
        p_ms = self._get_p_ms(d, w)
        return p_bg, p_reg, p_ms
    
    #Get p(t_di = 0, z_di = bg)
    def _get_p_bg(self, d, w):
        term1 = (self.n_bg_w[w] + self.beta_bg) / (self.n_bg + self.voc_size * self.beta_bg)
        term2 = self.n_bg_d[d] + self.gamma_1
        return term1 * term2
    
    # Get p(t_di=1, z_di=c)
    def _get_p_reg(self, d, w, c):
        term1 = (self.n_reg_d_z[d, c] + self._get_alpha(c)) / (self.n_reg_d[d] + self.num_candidates * self.alpha + self.alpha_ud)
        term2 = (self.n_reg_w_z[w, c] + self._get_beta(c)) / (self.n_reg_z[c] + self.voc_size * self._get_beta(c)) 
        term3 = (self.n_reg_d[d] + self.gamma_2)
        return term1 * term2 * term3
    
    #Get p(t_di=2, z_di = e_ms)
    def _get_p_ms(self, d, w):
        #term1 = (self.n_ms_d[d] + self.beta_ms) / (self.n_ms_d[d] + self.voc_size * self.beta_ms) #numerator good??
        term1 = (self.n_ms_w_d[w, d] + self.beta_ms) / (self.n_ms_d[d] + self.voc_size * self.beta_ms) #numerator good??
        term2 = self.n_ms_d[d] + self.gamma_3
        return term1 * term2
    
    def get_doc_dist(self):
        pass
    
    def get_bg_dist(self):
        pass
    
    def get_ud_dist(self):
        pass
    
    def get_c_dist(self):
        pass
    
    def _get_alpha(self, c):
        return self.alpha_ud if c is "undefined" else self.alpha
        
    def _get_beta(self, c):
        return self.beta_ud if c is "undefined" else self.beta
        