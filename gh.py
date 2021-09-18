from github import Github
import math


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


def get_recs(token):
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
    for (lang, freq) in top:
        # for each language, search for 1-2 projects
        repositories = g.search_repositories(query=f'language:{lang} good-first-issues:>3')
        bound = math.floor(1 + sigmoid(freq))
        for repo in repositories[:bound]:
            recs.append({
                "name": repo.full_name,
                "topics": repo.get_topics(),
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "relevance": freq
            })

    return recs

if __name__ == "__main__":
    print(get_recs("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"))