import spacy
from scipy import spatial
model = spacy.load('en_core_web_md')


def getVector(label):
    vec = model(label.replace('-', ' ')).vector
    return vec


def similarity(vec1, vec2):
    return 1 - spatial.distance.cosine(vec1, vec2)


if __name__ == "__main__":
    pl = getVector("model-infrastructure")
    py = getVector("model-management")
    m = getVector("python")

    print(similarity(pl, py))
    print(similarity(pl, m))