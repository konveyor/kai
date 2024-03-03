repos = {
    "eap-coolstore-monolith": [
        "https://github.com/mathianasj/eap-coolstore-monolith.git",
        "main",
        "quarkus-migration",
    ],
    "kitchensink": [
        "https://github.com/tqvarnst/jboss-eap-quickstarts.git",
        "main",
        "quarkus-3.2",
    ],
    "ticket-monster": ["https://github.com/jmle/monolith.git", "master", "quarkus"],
    "jboss-eap-quickstarts": [
        "https://github.com/jboss-developer/jboss-eap-quickstarts",
        "7.4.x",
        None,
    ],
    "jboss-eap-quickstarts-quarkus": [
        "https://github.com/christophermay07/quarkus-migrations",
        "main",
        "main",
    ],
    "helloworld-mdb": [
        "https://github.com/savitharaghunathan/helloworld-mdb.git",
        "main",
        "quarkus",
    ],
    "bmt": ["https://github.com/konveyor-ecosystem/bmt.git", "main", "quarkus"],
    "cmt": ["https://github.com/konveyor-ecosystem/cmt.git", "main", "quarkus"],
    "tasks-qute": [
        "https://github.com/konveyor-ecosystem/tasks-qute.git",
        "main",
        "quarkus",
    ],
    "greeter": ["https://github.com/konveyor-ecosystem/greeter.git", "main", "quarkus"],
}

sample_source_apps = {
    "eap-coolstore-monolith": "sample_repos/eap-coolstore-monolith",
    "ticket-monster": "sample_repos/ticket-monster",
    "kitchensink": "sample_repos/kitchensink/kitchensink",
    "helloworld-mdb": "sample_repos/helloworld-mdb",
    "bmt": "sample_repos/bmt",
    "cmt": "sample_repos/cmt",
    "ejb-remote": "sample_repos/jboss-eap-quickstarts/ejb-remote",
    "ejb-security": "sample_repos/jboss-eap-quickstarts/ejb-security",
    "tasks-qute": "sample_repos/tasks-qute",
    "greeter": "sample_repos/greeter",
}

sample_target_apps = {
    "eap-coolstore-monolith": "sample_repos/eap-coolstore-monolith",
    "ticket-monster": "sample_repos/ticket-monster",
    "kitchensink": "sample_repos/kitchensink/kitchensink",
    "helloworld-mdb": "sample_repos/helloworld-mdb",
    "bmt": "sample_repos/bmt",
    "cmt": "sample_repos/cmt",
    "ejb-remote": "sample_repos/jboss-eap-quickstarts-quarkus/ejb-remote-to-quarkus-rest",
    "ejb-security": "sample_repos/jboss-eap-quickstarts-quarkus/ejb-security-to-quarkus-basic-elytron",
    "tasks-qute": "sample_repos/tasks-qute",
    "greeter": "sample_repos/greeter",
}
