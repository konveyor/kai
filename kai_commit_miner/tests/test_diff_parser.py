"""Tests for unified diff parser."""

from kai_commit_miner.git.diff_parser import parse_unified_diff


def test_parse_simple_diff() -> None:
    diff = """\
diff --git a/src/Foo.java b/src/Foo.java
index abc1234..def5678 100644
--- a/src/Foo.java
+++ b/src/Foo.java
@@ -1,5 +1,5 @@
 package com.example;

-import javax.ejb.Stateless;
+import jakarta.ejb.Stateless;

 @Stateless
"""
    files = parse_unified_diff(diff)
    assert len(files) == 1
    assert files[0].old_path == "src/Foo.java"
    assert files[0].new_path == "src/Foo.java"
    assert len(files[0].hunks) == 1
    hunk = files[0].hunks[0]
    assert hunk.old_start == 1
    assert hunk.old_count == 5
    assert hunk.new_start == 1
    assert hunk.new_count == 5
    assert len(hunk.removed_lines) == 1
    assert len(hunk.added_lines) == 1


def test_parse_new_file() -> None:
    diff = """\
diff --git a/src/New.java b/src/New.java
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/src/New.java
@@ -0,0 +1,3 @@
+package com.example;
+
+public class New {}
"""
    files = parse_unified_diff(diff)
    assert len(files) == 1
    assert files[0].is_new_file is True
    assert files[0].new_path == "src/New.java"
    assert len(files[0].hunks) == 1
    assert len(files[0].hunks[0].added_lines) == 3


def test_parse_deleted_file() -> None:
    diff = """\
diff --git a/src/Old.java b/src/Old.java
deleted file mode 100644
index abc1234..0000000
--- a/src/Old.java
+++ /dev/null
@@ -1,2 +0,0 @@
-package com.example;
-public class Old {}
"""
    files = parse_unified_diff(diff)
    assert len(files) == 1
    assert files[0].is_deleted_file is True
    assert len(files[0].hunks) == 1
    assert len(files[0].hunks[0].removed_lines) == 2


def test_parse_multiple_files() -> None:
    diff = """\
diff --git a/src/A.java b/src/A.java
--- a/src/A.java
+++ b/src/A.java
@@ -1,3 +1,3 @@
 package a;
-import javax.ejb.Stateless;
+import jakarta.ejb.Stateless;
 class A {}
diff --git a/src/B.java b/src/B.java
--- a/src/B.java
+++ b/src/B.java
@@ -1,3 +1,3 @@
 package b;
-import javax.persistence.Entity;
+import jakarta.persistence.Entity;
 class B {}
"""
    files = parse_unified_diff(diff)
    assert len(files) == 2
    assert files[0].old_path == "src/A.java"
    assert files[1].old_path == "src/B.java"


def test_parse_multiple_hunks() -> None:
    diff = """\
diff --git a/src/Foo.java b/src/Foo.java
--- a/src/Foo.java
+++ b/src/Foo.java
@@ -1,3 +1,3 @@
-import javax.ejb.Stateless;
+import jakarta.ejb.Stateless;

 class Foo {
@@ -10,3 +10,3 @@
-    @javax.inject.Inject
+    @jakarta.inject.Inject
     private Service svc;
"""
    files = parse_unified_diff(diff)
    assert len(files) == 1
    assert len(files[0].hunks) == 2
    assert files[0].hunks[0].old_start == 1
    assert files[0].hunks[1].old_start == 10


def test_parse_empty_diff() -> None:
    assert parse_unified_diff("") == []
