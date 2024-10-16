# Exploring a Kai Client

## Overview

The goal of this exploration is explore what a client side processing of generating a code suggestion could look like.
The idea is that instead of sending data to the backend server and relying on it to generate a fix we'd move the logic closer to where the entire application's source code reside. This is motivated by the implied need that to address a full modernization at scope of a repository we need to go beyond looking at a single file and we need to consider the full context of a repository...which implies the state of the files on disk may be newer/different than what is committed into a SCM repo.
