
def sample_index(p_bg, p_reg, p_ud, p_ms):
    """
    Sample from the Multinomial distribution and return the sample index.
    First
    """
    p = [p_bg] + [p_ms] + [p_ud] + p_reg
    topic = np.random.multinomial(1,p).argmax()
    t = 


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
        #assign voc_size
        #assign self.num_candidates
        #init all counts to 0
        #assign a topic randomly to each word
        #for each doc
            #for each word
                #z = random...
                #update counts
    
    
    def run(self, max_iter=1000):
        for i in xrange(max_iter):
            #for each doc
                #for each word
                    #get z for this word and discount 1 to the counts
                    #TODO
                    #get probability distribution p(t,z)
                    p_bg, p_reg, p_ud, p_ms = self._get_joint_dist_t_z(d, w)
                    #sample form the obtained distribution
                    z,t = sample_index(p_bg, p_reg, p_ud, p_ms)
                    #update counts
                    #TODO
                    
                    
    def _get_joint_dist_t_z(self, d, w):
        p_bg = self._get_p_bg(d, w)
        p_reg = []
        for c in xrange(self.num_candidates):
            p_reg.append(self._get_p_reg(d, w, c))
        p_ud = self._get_p_reg(d, w, "undefined")
        p_ms = self._get_p_ms(d)
        return p_bg, p_reg, p_ud, p_ms
    
    #Get p(t_di = 0, z_di = bg)
    def _get_p_bg(self, d, w):
        term1 = (self.n_bg_w[w] + self.n_beta_bg) / (self.n_bg + self.voc_size * self.beta_bg)
        term2 = self.n_bg_d[d] + self.gamma_1
        return term1 * term2
    
    # Get p(t_di=1, z_di=c)
    def _get_p_reg(self, d, w, c):
        term1 = (self.n_reg_d_z[d][c] + self._get_alpha(c)) / (self.n_reg_d[d] + self.num_candidates * self.alpha + self.alpha_ud)
        term2 = (self.n_reg_w_z[w][c] + self._get_beta(c)) / (self.n_reg_z[c] + self.voc_size * self._get_beta(c)) 
        term3 = (self.n_reg_d[d] + self.gamma_2)
        return term1 * term2 * term3
    
    #Get p(t_di=2, z_di = e_ms)
    def _get_p_ms(self, d):
        term1 = self.n_ms_d[d] + self.beta_ms / self.n_ms_d[d] + self.voc_size * self.beta_ms #numerator good??
        term2 = self.n_ms_d[d] + self.gamma_3
        return term1 * term2
    
    def get_doc_dist(self)
    
    def get_bg_dist(self):
    
    def get_ud_dist(self):
    
    def get_c_dist(self):
    
    def _get_alpha(c):
        return self.alpha_ud if c is "undefined" else self.alpha
        
    def _get_beta(c):
        return self.beta_ud if c is "undefined" else self.beta
        