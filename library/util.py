import numpy as np
import scipy

def _cosine_similarity(a, b):
    return np.dot(a,b) / np.linalg.norm(a) *np.linalg.norm(b)

def _quantify_image(image_arr, div=16):
    quantized = image_arr // div * div + div //2
    return quantized


def _find_image_centroid(image_arr, NUM_CLUSTERS = 11):
    arr = image_arr.reshape(scipy.product(image_arr.shape[:2]), image_arr.shape[2]).astype(float) # reshape width and height into 1 dimension
    centroid, dist = scipy.cluster.vq.kmeans(arr, NUM_CLUSTERS)
    vecs, _ = scipy.cluster.vq.vq(arr, centroid)         # assign codes
    counts, _ = scipy.histogram(vecs, len(centroid))    # count occurrences    
    return centroid, counts