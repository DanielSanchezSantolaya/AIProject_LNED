import numpy as np
import random
import operator



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
        
    
    def _initialize(self):
        #assign voc_size and create a dictionary with the index position of every word
        #words = np.unique([item for sublist in (d_surround + dc) for item in sublist])
        words = list(set([item for sublist in self.docs for item in sublist]))
        n_docs = len(self.docs)
        self.voc_size = len(words)
        self.idx_w = {}
        for w in words:
            self.idx_w[w] = words.index(w)
        #assign self.num_candidates, create list of regular topics, and index position of every regular index
        self.num_candidates = len(self.d_c)
        self.candidate_topics = [str(i) for i in xrange(self.num_candidates)]
        self.topic_d_c = {}
        for i in xrange(self.num_candidates):
            self.topic_d_c[i] = str(i)
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
        for i in xrange(len(self.docs)):
            for j in xrange(len(self.docs[i])):
                w = self.idx_w[self.docs[i][j]]
                #assign a topic randomly to each word
                z,t = self._get_random_topic(i)
                #update counts
                self._update_counts(1, z, t, w, i)
                #assign the topic
                self.topics[(i, j)] = (z,t)
    
                
    
    def _update_counts(self, value, z, t, w, d):
        if t == 0: #Background topic
            self.n_bg_w[w] += value
            self.n_bg += value
            self.n_bg_d[d] += value
            return #fix
        if t == 1: #Regular topic
            c_idx = self.idx_reg_z[z]
            self.n_reg_d_z[d, c_idx] += value
            self.n_reg_d[d] += value
            self.n_reg_w_z[w, c_idx] += value
            self.n_reg_z[c_idx] += value
            return #fix
        if t == 2: #Mater topic
            self.n_ms_w_d[w, d] += value
            self.n_ms_d[d] += value
            
    def _get_random_topic(self, d):
        #fix
        if d < self.num_candidates: #Only background and candidate topic of that document can be selected
            topics = [self.regular_topics[d]] + ['bg']
        else:
            topics = self.regular_topics + ['bg'] + ['ms']
        z = random.choice(topics)
        t = 1
        if z == 'bg':
            t = 0
        elif z == 'ms':
            t = 2
        return z,t
        
    def sample_topic(self, p_bg, p_reg, p_ms, d):
        """
        Sample from the Multinomial distribution and return the sample index.
        First
        """
        if d < self.num_candidates: #fix
            topics = [self.topic_d_c[d]] + ['bg']
            p = p_reg + [p_bg]
        else:
            topics = self.regular_topics + ['bg'] + ['ms']
            p = p_reg + [p_bg] + [p_ms] 
        # normalize to obtain probabilities
        
        norm_p = [pi/sum(p) for pi in p] #fix
        
        idx = np.random.multinomial(1,norm_p).argmax()
        z = topics[idx]
        t = 1
        if z == 'bg':
            t = 0
        elif z == 'ms':
            t = 2
        return z,t
    
    def run(self, d_surround, d_c, max_iter=100):
        print 'start...'
        self.d_surround = d_surround
        self.d_c = d_c
        self.topic_d_c = {} 
        self.docs = (d_c + d_surround)
        self._initialize()
        for it in xrange(max_iter):
            print 'iteration ' + str(it) + ' of ' + str(max_iter)
            for i in xrange(len(self.docs)):
                for j in xrange(len(self.docs[i])):
                    w = self.idx_w[self.docs[i][j]]
                    #get z for this word and discount 1 to the counts
                    z,t = self.topics[i,j]
                    self._update_counts(-1, z, t, w, i)
                    #get probability distribution p(t,z)
                    p_bg, p_reg, p_ms = self._get_joint_dist_t_z(i, w)
                    #sample form the obtained distribution
                    z,t = self.sample_topic(p_bg, p_reg, p_ms, i)
                    #update counts
                    self._update_counts(1, z, t, w, i)
                    #assign the topic
                    self.topics[(i, j)] = (z,t)
        print 'finished...'
                    
    def _get_joint_dist_t_z(self, d, w):
        
        if d < self.num_candidates: #fix
            #Background topics probability
            p_bg = self._get_p_bg(d, w)
            #Regular topics probability (Only the topic of this candidate for candidate documents)
            c_idx = self.idx_reg_z[self.topic_d_c[d]]
            p_reg = [self._get_p_reg(d, w, c_idx)] #fix
            
            #Master topic probability (0 for candicate documents)
            p_ms = 0.0
        else:
            #Background probability
            p_bg = self._get_p_bg(d, w)
            #Regular probability
            p_reg = []
            for c in self.regular_topics: #regular topics include ud(undefined)
                c_idx = self.idx_reg_z[c]
                p_reg.append(self._get_p_reg(d, w, c_idx))     
            
            #Master probability
            p_ms = self._get_p_ms(d, w)
        return p_bg, p_reg, p_ms
    
    #Get p(t_di = 0, z_di = bg)   #USING SAME FORMULA FOR CANDIDATE AND SURROUND(Mention) Documents
    def _get_p_bg(self, d, w):
        term1 = (self.n_bg_w[w] + self.beta_bg) / (self.n_bg + self.voc_size * self.beta_bg)
        term2 = self.n_bg_d[d] + self.gamma_1
        return term1 * term2
    
    # Get p(t_di=1, z_di=c)
    def _get_p_reg(self, d, w, c):   #WE EXCLUDE THE FIRST TERM IN SURROUND(Mention) Documents, as we don't have undefined topic for them
        term2 = (self.n_reg_w_z[w, c] + self._get_beta(c)) / (self.n_reg_z[c] + self.voc_size * self._get_beta(c)) 
        term3 = (self.n_reg_d[d] + self.gamma_2)
        if d < self.num_candidates: #fix
            return term2 * term3
        else:
            #fix
            term1 = (self.n_reg_d_z[d, c] + self._get_alpha(c)) / (self.n_reg_d[d] + self.num_candidates * self.alpha + self.alpha_ud) 
            return term1 * term2 * term3
    
    #Get p(t_di=2, z_di = e_ms)
    def _get_p_ms(self, d, w):      #ONLY WILL BE USED FOR SURROUND(Mention) Documents
#        if d < self.num_candidates:
#            raise Exception('Called _get_p_ms() for a candidate document')
        #term1 = (self.n_ms_d[d] + self.beta_ms) / (self.n_ms_d[d] + self.voc_size * self.beta_ms) #numerator good??
        term1 = (self.n_ms_w_d[w, d] + self.beta_ms) / (self.n_ms_d[d] + self.voc_size * self.beta_ms) #numerator good??
        term2 = self.n_ms_d[d] + self.gamma_3
        return term1 * term2
    
    def get_doc_dist(self):
        self.probs_d_c = {}
        for d in xrange(len(self.docs)):
            probs = {}
            for c in self.regular_topics:
                idx_c = self.idx_reg_z[c]
                probs[c] = (self.n_reg_d_z[d, idx_c] + self._get_alpha(c)) / (self.n_reg_d[d] + self.num_candidates * self.alpha + self.alpha_ud)
            self.probs_d_c[d] = sorted(probs.items(), key=operator.itemgetter(1))
    
    def get_bg_dist(self):
        self.probs_bg = {}
        for w in self.idx_w:
            idx_w = self.idx_w[w]
            self.probs_bg[w] = (self.n_bg_w[idx_w] + self.beta_bg)/(self.n_bg + self.voc_size * self.beta_bg)
        self.probs_bg = sorted(self.probs_bg.items(), key=operator.itemgetter(1))
    
    def get_ud_dist(self):
        self.probs_ud = {}
        idx_c = self.idx_reg_z['ud']
        for w in self.idx_w:
            idx_w = self.idx_w[w]
            self.probs_ud[w] = (self.n_reg_w_z[idx_w, idx_c] + self.beta_ud) / (self.n_reg_z[idx_c] + self.voc_size * self.beta_ud)
        self.probs_ud = sorted(self.probs_ud.items(), key=operator.itemgetter(1))

    
    def get_c_dist(self):
        self.probs_c = {}
        for c in self.candidate_topics:
            probs_c = {}
            idx_c = self.idx_reg_z[c]
            for w in self.idx_w:
                idx_w = self.idx_w[w]
                probs_c[w] = (self.n_reg_w_z[idx_w, idx_c] + self.beta) / (self.n_reg_z[idx_c] + self.voc_size * self.beta)
            #sort by prob
            self.probs_c[c] = sorted(probs_c.items(), key=operator.itemgetter(1))
            
    
    def _get_alpha(self, c):
        return self.alpha_ud if c is 'ud' else self.alpha
        
    def _get_beta(self, c):
        return self.beta_ud if c is 'ud' else self.beta
        
    def _is_cand_doc(self, d):
        return d < self.num_candidates #fix
        
    def run_doc_query(self, d_query, max_iter = 80):
        self._initialize_doc_query(d_query)
        for it in xrange(max_iter):
            for j in xrange(len(d_query)):
                if d_query[j] in self.idx_w:
                    w = self.idx_w[d_query[j]]
                    #get z for this word and discount 1 to the counts
                    z,t = self.topics_d_query[j]
                    #update counts
                    self._update_counts_doc_query(-1, w, z, t)
                    #get probability distribution p(t,z)
                    p_bg, p_reg, p_ms = self._get_joint_dist_t_z_doc_query(w)
                    #sample form the obtained distribution
                    z,t = self.sample_topic(p_bg, p_reg, p_ms, len(self.docs))
                    #update counts
                    self._update_counts_doc_query(1, w, z, t)
                    #assign the topic
                    self.topics_d_query[j] = (z,t)
                else: #if word is not in vocabulary, assign to undefined?
                    z,t = ('ud', 1)
                    self.topics_d_query[j] = (z,t)
        #print d_query
        #print self.topics_d_query
                    
    def _initialize_doc_query(self, d_query):
        self.topics_d_query = {}
        self.n_bg_dquery = 0
        self.n_reg_dquery_z = np.zeros(len(self.regular_topics))
        self.n_reg_dquery = 0
        self.n_ms_w_dquery = np.zeros(self.voc_size)
        self.n_ms_dquery = 0
        #loop for every doc and word
        for j in xrange(len(d_query)):
            if d_query[j] in self.idx_w:
                w = self.idx_w[d_query[j]]
                #assign a topic randomly to each word
                z,t = self._get_random_topic(len(self.docs))
                #update counts
                self._update_counts_doc_query(1, w, z, t)
                #assign the topic
                self.topics_d_query[j] = (z,t)
            else:
                z,t = ('ud', 1)
                self.topics_d_query[j] = (z,t)
        
    def _update_counts_doc_query(self, value, w, z, t):
        if t == 0: #Background topic
            self.n_bg_w[w] += value
            self.n_bg += value
            self.n_bg_dquery += value
        if t == 1: #Regular topic
            c_idx = self.idx_reg_z[z]
            self.n_reg_dquery_z[c_idx] += value
            self.n_reg_dquery += value
            self.n_reg_w_z[w, c_idx] += value
            self.n_reg_z[c_idx] += value
        if t == 2: #Mater topic
            self.n_ms_w_dquery[w] += value
            self.n_ms_dquery += value
            
    def _get_joint_dist_t_z_doc_query(self, w):
        #background
        term1 = (self.n_bg_w[w] + self.beta_bg) / (self.n_bg + self.voc_size * self.beta_bg)
        term2 = self.n_bg_dquery + self.gamma_1
        p_bg = term1 * term2
        #regular topics
        p_reg = []
        for c in self.regular_topics: #regular topics include ud(undefined)
            c_idx = self.idx_reg_z[c]
            term1 = (self.n_reg_dquery_z[c_idx] + self._get_alpha(c_idx)) / (self.n_reg_dquery + self.num_candidates * self.alpha + self.alpha_ud)
            term2 = (self.n_reg_w_z[w, c_idx] + self._get_beta(c_idx)) / (self.n_reg_z[c_idx] + self.voc_size * self._get_beta(c_idx))                 
            term3 = (self.n_reg_dquery + self.gamma_2)   
            p_reg.append(term1 * term2 * term3)  
        #Undefined
        term1 = (self.n_ms_w_dquery[w] + self.beta_ms) / (self.n_ms_dquery + self.voc_size * self.beta_ms) #numerator good??
        term2 = self.n_ms_dquery + self.gamma_3
        p_ms = term1 * term2
        return p_bg, p_reg, p_ms
    
    def get_doc_query_dist(self):
        self.probs_dquery_c = {}
        for c in self.regular_topics:
            idx_c = self.idx_reg_z[c]
            self.probs_dquery_c[c] = (self.n_reg_dquery_z[idx_c] + self._get_alpha(c)) / (self.n_reg_dquery + self.num_candidates * self.alpha + self.alpha_ud)
        #self.probs_dquery_c = sorted(self.probs_dquery_c.items(), key=operator.itemgetter(1))
        
    def get_max_topic_doc_query(self):
        self.get_doc_dist()
        return max(self.probs_dquery_c.iteritems(), key=operator.itemgetter(1))[0]
        
    def get_candidate_ranking_doc_query(self):
        ranking = sorted(self.probs_dquery_c.items(), key=operator.itemgetter(1), reverse = True)
        ranking = [topic for topic, prob in ranking if topic != 'ud']
        return ranking
        