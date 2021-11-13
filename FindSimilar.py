from PIL import Image
import imagehash
import os
import numpy as np

def find_similar(dirname, location, similarity=80):
        hash_size = 8
        fnames = os.listdir(dirname)
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (hash_size ** 2))
        
        with Image.open(location) as img:
            hash1 = imagehash.average_hash(img, hash_size).hash
        for image in fnames:
            with Image.open(os.path.join(dirname, image)) as img:
                hash2 = imagehash.average_hash(img, hash_size).hash

                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    return [True, image]
        return [False]
                    
                    
                    
                
        
            