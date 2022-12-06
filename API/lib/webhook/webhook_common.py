def determine_webhook_source(request):
    gitlab_header = request.headers.get("X-Gitlab-Event", None)
    if gitlab_header and gitlab_header == "Push Hook":
        return "GITLAB"

    github_header = request.headers.get("X-Github-Event", None)
    if github_header:
        return "GITHUB"

    # Unsupported webhook source
    return None

def get_host_domain_from_url(git_url):
        path = git_url.split("://")[1]
        components = path.split("/")
        host_domain = components[0]
        return host_domain
