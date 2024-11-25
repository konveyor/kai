# Need to make sure that XML tree can use the new parser
import sys

from kai.logging.logging import get_logger, init_logging_from_config
from kai.reactive_codeplanner.agent.reflection_agent import ReflectionAgent

sys.modules['_elementtree'] = None
import pprint

pp = pprint.PrettyPrinter(indent=2)

import tempfile
import shutil
import os
import subprocess

#First we need to download coolstore if it does not exist.

if not os.path.exists("./coolstore"):
    subprocess.run("../../example/fetch.sh")

if not os.path.exists("../../kai_analyzer_rpc/kai_analyzer_rpc"):
    subprocess.run(["go", "build", "-o", "kai_analyzer_rpc", "main.go"], cwd="../../kai_analyzer_rpc")

# NOTE(JonahSussman): Python's default tmp dir gets clobbered somehow on my
# machine, so putting it in local directory for now.
temp_dir = tempfile.TemporaryDirectory(prefix="tmp-")
coolstore_path = os.path.join(temp_dir.name, "coolstore")
shutil.copytree("./coolstore", coolstore_path)

## make the necessary change

print(temp_dir)


from pathlib import Path
from kai.analyzer import AnalyzerLSP
from kai.reactive_codeplanner.task_manager.api import RpcClientConfig
from kai.reactive_codeplanner.task_manager.task_manager import TaskManager
from kai.reactive_codeplanner.task_runner.analyzer_lsp.validator import AnalyzerLSPStep 
from kai.reactive_codeplanner.task_runner.analyzer_lsp.task_runner import AnalyzerTaskRunner
from kai.reactive_codeplanner.task_runner.compiler.maven_validator import MavenCompileStep
from kai.reactive_codeplanner.task_runner.compiler.compiler_task_runner import MavenCompilerTaskRunner
from kai.reactive_codeplanner.task_runner.dependency.task_runner import DependencyTaskRunner
from kai.reactive_codeplanner.agent.dependency_agent.dependency_agent import MavenDependencyAgent
from kai.analyzer_types import Incident, RuleSet, Violation, Category
from kai_solution_server.service.llm_interfacing.model_provider import ModelProvider
from kai.kai_config import KaiConfig
from kai.reactive_codeplanner.vfs.git_vfs import RepoContextManager
import logging
from kai.reactive_codeplanner.task_runner.analyzer_lsp.api import AnalyzerDependencyRuleViolation, AnalyzerRuleViolation

# config = RpcClientConfig(Path(coolstore_path),
#                          "../../kai-analyzer/kai-analyzer",
#                         #  "/Users/shurley/repos/MTA/rulesets/default/generated",
#                         ""
#                          Path("/Users/shurley/repos/kai/jdtls/bin/jdtls"),
#                          Path("./java-bundle/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar"),
#                          "konveyor.io/target=quarkus || konveyor.io/target=jakarta-ee",
#                          None,
#                          None)

config = RpcClientConfig(Path(coolstore_path),
                         Path("../../kai_analyzer_rpc/kai_analyzer_rpc"),
                         Path("/Users/shurley/repos/MTA/rulesets/default/generated"),
                         Path("/Users/shurley/repos/kai/jdtls/bin/jdtls"),
                         Path("./java-bundle/java-analyzer-bundle.core-1.0.0-SNAPSHOT.jar"),
                         "konveyor.io/target=quarkus || konveyor.io/target=jakarta-ee",
                         None,
                         None)
kai_config = KaiConfig.model_validate_filepath("01_config.toml")

init_logging_from_config(kai_config)
modelProvider = ModelProvider(kai_config.models)
reflection_agent = ReflectionAgent(modelProvider.llm)
rcm = RepoContextManager(config.repo_directory, reflection_agent, None)

maven_dependency_agent = MavenDependencyAgent(modelProvider.llm, config.repo_directory)


anayzer_task_runner= AnalyzerTaskRunner(modelProvider.llm)
maven_compiler_task_runner= MavenCompilerTaskRunner(modelProvider.llm)
dependency_task_runner = DependencyTaskRunner(maven_dependency_agent)

# Define the initial task, to prove out the solving of a single incident:

path = os.path.join(coolstore_path, 'src/main/java/com/redhat/coolstore/service/ShippingService.java')
print(path)

incident = Incident(
    uri='file://'+path,
    message='Remote EJBs are not supported in Quarkus, and therefore its use must be removed and replaced with REST functionality. In order to do this:\n 1. Replace the `@Remote` annotation on the class with a `@jakarta.ws.rs.Path("<endpoint>")` annotation. An endpoint must be added to the annotation in place of `<endpoint>` to specify the actual path to the REST service.\n 2. Remove `@Stateless` annotations if present. Given that REST services are stateless by nature, it makes it unnecessary.\n 3. For every public method on the EJB being converted, do the following:\n - In case the method has no input parameters, annotate the method with `@jakarta.ws.rs.GET`; otherwise annotate it with `@jakarta.ws.rs.POST` instead.\n - Annotate the method with `@jakarta.ws.rs.Path("<endpoint>")` and give it a proper endpoint path. As a rule of thumb, the method name can be used as endpoint, for instance:\n ```\n @Path("/increment")\n public void increment() \n ```\n - Add `@jakarta.ws.rs.QueryParam("<param-name>")` to any method parameters if needed, where `<param-name>` is a name for the parameter.',
    code_snip=' 2  \n 3  import java.math.BigDecimal;\n 4  import java.math.RoundingMode;\n 5  \n 6  import javax.ejb.Remote;\n 7  import javax.ejb.Stateless;\n 8  \n 9  import com.redhat.coolstore.model.ShoppingCart;\n10  \n11  @Stateless\n12  @Remote\n13  public class ShippingService implements ShippingServiceRemote {\n14  \n15      @Override\n16      public double calculateShipping(ShoppingCart sc) {\n17  \n18          if (sc != null) {\n19  \n20              if (sc.getCartItemTotal() >= 0 && sc.getCartItemTotal() < 25) {\n21  \n22                  return 2.99;',
    line_number=12,
    variables={'file': 'file:///private/var/folders/vt/5bfp7vyd1h79_7k5ygr0fttr0000gn/T/tmpthgg63up/coolstore/src/main/java/com/redhat/coolstore/service/ShippingService.java', 'kind': 'Class', 'name': 'Stateless', 'package': 'com.redhat.coolstore.service'},
)

ruleset = RuleSet(
    name='quarkus/springboot',
    description='This ruleset gives hints to migrate from SpringBoot devtools to Quarkus',
    tags=None,
    violations={},
    errors=None,
    unmatched=None,
    skipped=None,
)

violation = Violation(
    description='Remote EJBs are not supported in Quarkus',
    category=Category.MANDATORY,
    labels=['konveyor.io/source=java-ee', 'konveyor.io/source=jakarta-ee', 'konveyor.io/target=quarkus'],
)

seed_task = AnalyzerRuleViolation(
    file=path,
    line=incident.line_number,
    column=0,
    message=incident.message,
    incident=incident,
    violation=violation,
    ruleset=ruleset,
)

analyzer =  AnalyzerLSP(
    analyzer_lsp_server_binary=config.analyzer_lsp_server_binary,
    repo_directory=config.repo_directory,
    rules_directory=config.rules_directory,
    analyzer_lsp_path=config.analyzer_lsp_path,
    analyzer_java_bundle_path=config.analyzer_java_bundle_path,
    dep_open_source_labels_path=config.dep_open_source_labels_path
    or Path(),
)

# TODO: Use seed_tasks argument to supply initial task to the task_manager
task_manager = TaskManager(
        config,
        rcm,
        [seed_task],
        # TODO: Set up with maven as well?
        validators=[AnalyzerLSPStep(config=config, analyzer=analyzer), MavenCompileStep(config)],
        # Agents are really task_runners
        task_runners=[anayzer_task_runner, maven_compiler_task_runner, dependency_task_runner],
    )


# TODO: Make this get_next_task(max_priority=0) to only grab seeded tasks
# Can also do: 
#   initial_task = task_manager.get_next_task(max_priority=0)
#   ...
#   task_manager.supply_result(task_manager.execute_task(initial_task)
#   follow_up_task = task_manager.get_next_task(max_priority=0)
#   # do whatever to show what followup is
#   task_manager.supply_result(task_manager.execute_task(follow_up_task)
# etc ...
# can  introspect the stack using task_manager.task_stacks
# priority 0 tasks will be accessible with task_manager.task_stacks.get(0)
# So can see all the new tasks that are spawned and how that stack changes as we progress
# as well as showing all the tasks in the stack if we want to show all the work that's been detected in general
# Can do that with task_manager.task_stacks.values() -> list of lists of tasks associated with each priority level

i = 0
for task in task_manager.get_next_task(max_priority=0):
    if i > 1:
        break
    print(f"main loop: got task: {task}")
    result = task_manager.execute_task(task)
    print(f"main loop: got result: {result}")
    task_manager.supply_result(result)
    i += 1

#verify that the java file has been updated.

import filecmp

diff = rcm.snapshot.diff(rcm.first_snapshot)

print(diff[1])

r = filecmp.cmp(coolstore_path+"/pom.xml", "./test-data/pom.xml")
print(r)


temp_dir.cleanup()