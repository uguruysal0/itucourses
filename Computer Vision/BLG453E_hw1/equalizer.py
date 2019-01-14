import numpy as np


"""
This code assumes first channel is red, second channel is green and third channel is green
"""
class HistogramEqualizer():
    def __init__(self, source_image):
        self.source_image = source_image
        self.source_image_histograms_pdfs = self.get_histograms_pdfs(source_image)
        self.source_image_cdfs = [ self.calculate_cdf(i[1]) for i in self.source_image_histograms_pdfs ]
        
    
    def calculate_cdf(self, pdf):
        c = np.zeros(256).astype(np.float)
        c[0] = pdf[0]
        for j in range(1,256):
            c[j] = c[j-1] + pdf[j]
        return c

    def get_histogram_pdf(self, channel):
        histogram = np.array([ np.sum( channel==g ) for g in range(256) ] )
        pdf = histogram / (channel.shape[0]*channel.shape[1])
        return histogram, pdf

    def get_histograms_pdfs(self,Image):
        return [ self.get_histogram_pdf(Image[...,0]),self.get_histogram_pdf(Image[...,1]), self.get_histogram_pdf(Image[...,2]) ]

    def get_data(self, name):
        return {
            "name":name,
            "image":self.source_image,
            "histograms": [ i[0] for i in self.source_image_histograms_pdfs ],
            "cdfs": self.source_image_cdfs }
    
    def get_closest(self,cdf1,cdf2,i):

        for k in range(256):
            if cdf1[k] >= cdf2[i]:
                return k

        return 255        

    def histogram_match(self,source_image, target_image):
        source = source_image["image"]
        target = target_image["image"]

        source_cdfs = source_image["cdfs"]
        target_cdfs = target_image["cdfs"]

        lut =  [ np.array([ self.get_closest(source_cdfs[j], target_cdfs[j], i ) for i in range(256)])  for j in range(3) ]
        
        for c in range(3):
            t = np.zeros( (source.shape[0], source.shape[1]), np.uint8)
            for val in range(255,0,-1):
                y = target[ ...,c ] 
                t[y==val] = lut[c][val]
            target[...,c] = t

        return target.astype(np.uint8)