class _Repository:
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return "PyPI"

    @property
    def url(self):
        return None


class CloudRepoRepository(_Repository):
    def __init__(
        self,
        organization: str = "",
        reponame: str = "",
        creds: tuple = (),
        custom_domain: str = None
    ):
        self.creds = creds
        self.organization = organization
        self.reponame = reponame
        self.custom_domain = custom_domain

    @property
    def name(self) -> str:
        e = f"CloudRepo-{self.organization}/{self.reponame}"
        if self.custom_domain is not None:
            e += f" (host {self.custom_domain})"
        return e
