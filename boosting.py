import numpy as np

class Boosting():
    
    def __init(self, training_set):
        self.training_set = training_set
        self.N = len(self.training_set)
        self.weights = np.ones(self.N)/self.N
        self.RULES = np.array([])
        self.ALPHA = np.array([])


    def weakClassify(self,):
        # call Naive Bayes classifier
        # get result = np.array([[x,y, h_x],]) for all tuples
        # return result 


    def boost(self,):
        """
        """

        for t in range(10):
            # get all (x,y,h_x) tuples
            hAndY = self.weakClassify()

            # calculate error 
            errors = np.array(i[1] != i[2] for i in self.training_set)
            error_t = (errors * self.weights).sum()
            # print(error_t,)

            # set alpha
            alpha_t = 0.5 * np.log((1 - error_t) / error_t)
            self.ALPHA.append(alpha_t)

            self.RULES.append(hAndY)

            #update weights
            z_tdas = self.weights * np.exp(-hAndY[:, 1] * alpha_t * hAndY[:, 2] )
            z_t = s_tdas.sum()

            self.weights = s_tdas / z_t


    def strongClassify(self,):
        # get alphas and rules(hypothesis)
        # for all tuples in training set, multiply alpha and h_x
        # sum the products above
        # return np.sign(sum)

    






