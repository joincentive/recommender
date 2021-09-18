from github import Github
import math

from embeddings import getVector, similarity


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


OMITTED_LANGS = {"HTML", "CSS"}
def gen_top(langs, total, scaling = 1):
    total_lines = sum(langs.values())
    for lang, lines in langs.items():
        if lang not in OMITTED_LANGS:
            if lang in total:
                total[lang] += (lines / total_lines) * scaling
            else:
                total[lang] = (lines / total_lines) * scaling


def fmt_repo(repo):
    return {
        "name": repo.full_name,
        "description": repo.description,
        "topics": repo.get_topics(),
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
    }


def get_recs(token, looking_for=""):
    g = Github(token)
    user = g.get_user()

    # get last 5 created repos
    weighted_langs = {}
    created = user.get_repos(sort="updated", direction="desc")
    for repo in created[:5]:
        langs = repo.get_languages()
        gen_top(langs, weighted_langs, 1)

    # get 5 starred repos (weight 1/5)
    starred = user.get_starred()
    for repo in starred[:5]:
        langs = repo.get_languages()
        gen_top(langs, weighted_langs, 0.2)

    # calculate top 4 languages
    top = sorted(weighted_langs.items(), key=lambda item: item[1], reverse=True)[:4]
    recs = []

    lf_vec = getVector(looking_for)
    for (lang, freq) in top:
        # for each language, search for 1-2 projects
        repositories = g.search_repositories(query=f'language:{lang} good-first-issues:3..50')
        bound = math.floor(1 + sigmoid(freq) * 1.5)
        for repo in repositories[:bound]:
            desc_vec = getVector(repo.description + " " + " ".join(repo.get_topics()))
            mult = similarity(lf_vec, desc_vec)
            repo = fmt_repo(repo)
            repo["relevance"] = freq + (mult * 10)
            recs.append(repo)

    return sorted(recs, key=lambda item: item["relevance"], reverse=True)


def similar(token, repo):
    g = Github(token)

    repo = g.get_repo(repo)
    topics = repo.get_topics()
    recs = []
    for topic in topics:
        repositories = g.search_repositories(query=f'topic:{topic}')
        for repo in repositories[:2]:
            repo = fmt_repo(repo)
            recs.append(repo)
    return recs
