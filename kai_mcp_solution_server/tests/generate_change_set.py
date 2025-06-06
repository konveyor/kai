from kai_mcp_solution_server.dao import SolutionChangeSet, SolutionFile

if __name__ == "__main__":
    s = SolutionChangeSet(
        diff="diff --git a/file.txt b/file.txt\nindex 83db48f..f735c8d 100644\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-Hello World\n+Hello Universe\n",
        before=[
            SolutionFile(
                uri="file://file.txt",
                content="Hello World",
            )
        ],
        after=[
            SolutionFile(
                uri="file://file.txt",
                content="Hello Universe",
            )
        ],
    )

    print(s.model_dump_json(indent=2))
