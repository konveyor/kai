# Demo / Knowledge Share of Agentic Approach in Reactive Code Planning

---

## Introduction to the Agentic Approach in Kai's Reactive Code Planner

- Our agentic approach uses a combination of **concrete tools** and **LLM agents** to:
  - Continuously assess the **state** of the code repository.
  - Split findings into **actionable tasks**.
  - Dynamically **adapt** based on task outcomes.

---

## Core Workflow: Task Prioritization and Resolution

- **Validators**:

  - Concrete tools that assess issues in the repository.
  - Generate tasks based on detected issues.
  - Re-evaluated after each change to the codebase.

- **TaskManager**:

  - Tasks are queued by priority and depth and handed off to TaskRunners depending on their type.
  - The system supports continuous iteration until all tasks are resolved.

- **TaskRunners and Agents**:

  - TaskRunners understand how to handle specific types of errors.
  - They are responsible for orchestrating one or more agents (this is the agentic part) in order to solve the Task.

- **Feedback Loop**:
  - Validators re-assess the codebase after task execution.
  - New tasks may be generated, forming a continuous feedback and action loop.

---

## Visual Workflow

```plaintext
 +------------------+
 |                  |
 |    Codebase      |<-------------------------------------+
 |                  |                                      |
 +---------+--------+                                      |
           |                                               |
           | (1) Validators assess codebase                |
           v                                               |
 +------------------+                             (6) Feedback loop
 |                  |                                      |
 |    Validators    |                                      |
 |                  |                                      |
 +---------+--------+                                      |
           |                                               |
           | (2) Generate tasks based on issues            |
           v                                               |
 +------------------+                                      |
 |                  |                                      |
 |    Task Queue    |                                      |
 |                  |                                      |
 +---------+--------+                                      |
           |                                               |
           | (3) Tasks handed to TaskRunners               |
           v                                               |
 +------------------+                                      |
 |                  |                                      |
 |   TaskRunners    |                                      |
 |                  |                                      |
 +---------+--------+                                      |
           |                                               |
           | (4) TaskRunners orchestrate Agents            |
           v                                               |
 +------------------+                                      |
 |                  |                                      |
 |      Agents      |--------------------------------------+
 |                  | (5) Agents solve tasks
 +------------------+
```

---

## Key Parameters and Their Control Over Behavior

- **Understanding Parameters**:

  - The behavior of the TaskManager is controlled by key parameters:
    - **max_depth**
    - **max_priority**
    - **max_iterations**

- **Symbols and Formatting**:
  - **Symbols Used**:
    - `[X]`: Task deferred or not processed.
    - `[ ]`: Task processed.
    - `├─`, `└─`: Indicate child tasks.
    - `│`: Represents a vertical connection.
  - **Legend**:
    - **Tasks are numbered** to indicate processing order.
    - **Indentation and symbols** represent task hierarchy.

---

## Max Depth

- **Purpose**: Limits how deep the TaskManager will go in resolving issue chains.

- **Application**:

  - Controls the recursion depth when resolving tasks.
  - Tasks beyond **max_depth** are left in the queue for later processing.

- **Example Task Queue (max_depth=1)**:

```plaintext
[1] AnalyzerRuleViolation in Product.java (priority=2, depth=0)
├─ [2] SymbolNotFoundError in Order.java (priority=2, depth=1)
│  ├─ [X] TypeMismatchError in Order.java (priority=2, depth=2)
[3] AnalyzerRuleViolation in Order.java (priority=2, depth=0)
```

- **Explanation**:
  - With `max_depth=1`, the TaskManager processes tasks up to depth 1.
  - Child tasks beyond depth 1 are left in the queue.
  - In this example:
    - Task [1] is processed.
    - Its child [2] is at depth 1 and is processed.
    - Any further children of [2] are beyond **max_depth** and are not processed.

---

## Max Priority

- **Purpose**: Focuses on tasks at or above a specified priority, deferring lower-priority tasks.

- **Application**:

  - Prioritizes critical tasks in the queue.
  - Tasks with priority value less than or equal to **max_priority** are processed.
  - **Child tasks inherit their parent's priority** for queue placement, but their individual priorities sort them among siblings.

- **Example Task Queue (max_priority=1)**:

```plaintext
[1] AnalyzerRuleViolation in SecurityModule.java (priority=1, depth=0)
└─ [2] AnalyzerDependencyRuleViolation in pom.xml: update security dependencies (priority=7, depth=1)
[X] AnalyzerRuleViolation in LoggingModule.java (priority=2, depth=0)
[X] AnalyzerDependencyRuleViolation in pom.xml: replace deprecated logging artifact (priority=3, depth=0)
```

- **Explanation**:
  - With `max_priority=1`, only tasks with priority 1 or lower (higher actual priority) are processed.
  - Task [1] is processed.
  - Its child [2] is processed because it inherits the parent's priority for queue placement.
  - Tasks marked with `[X]` have lower priority (higher numerical value) and are deferred.

---

## Max Iterations

- **Purpose**: Sets a cap on attempts to solve each issue in one run.

- **Application**:

  - Useful for avoiding excessive retry loops.
  - Tasks exceeding `max_iterations` remain unresolved and may require manual intervention.

- **Example Task Queue (max_iterations=2)**:

```plaintext
[1] AnalyzerRuleViolation in PaymentService.java: update currency formatter (priority=2, depth=0)
├─ [2] AnalyzerDependencyRuleViolation in pom.xml: replace javax.activation with jakarta.activation (priority=2, depth=1)
│  ├─ [X] SymbolNotFoundError in Billing.java: unresolved symbol (priority=2, depth=2)
│  ├─ [X] PackageDoesNotExistError in Invoice.java: missing java.util.stream (priority=1, depth=3)
│  └─ [X] PackageDoesNotExistError in Receipt.java: missing javax.print (priority=1, depth=3)
└─ [X] SymbolNotFoundError in SummaryReport.java: unresolved identifier (priority=2, depth=1)
```

- **Explanation**:
  - With `max_iterations=2`, only two tasks will be pulled off the queue.
  - Tasks marked with `[X]` have exceeded the maximum iterations.
  - They remain unresolved and may be solved in future runs.

---

## Implementation Strategies and Their Impact on Task Resolution

---

## Example: Depth-First vs. Breadth-First Processing

- **Understanding Processing Strategies**:
  - The **TaskManager** can be configured for different processing strategies using **max_depth**.
  - **Depth-First**: Fully resolves each issue before moving to the next.
  - **Breadth-First**: Processes high-level issues across the codebase incrementally.

---

## Depth-First Processing

- **Configuration**: Set **max_depth** to a high value or unrestricted.

- **Example**:

```plaintext
[1] AnalyzerRuleViolation in CartController.java (priority=2, depth=0)
├─ [2] AnalyzerDependencyRuleViolation in pom.xml: move to Jakarta EE artifacts (priority=2, depth=1)
│  ├─ [3] AnalyzerRuleViolation in Inventory.java: deprecated method usage (priority=2, depth=2)
│  ├─ [4] SymbolNotFoundError in PaymentGateway.java: missing dependency (priority=2, depth=3)
│  └─ [5] PackageDoesNotExistError in UserProfile.java: missing javax.security package (priority=1, depth=3)
[6] AnalyzerRuleViolation in CheckoutController.java (priority=2, depth=0)
```

- **Explanation**:
  - The TaskManager processes each task and its children fully before moving to the next top-level task.
  - Deeply nested issues are resolved immediately.

---

## Breadth-First Processing

- **Configuration**: Incrementally increase **max_depth**.

- **Example**:

### At `max_depth=0`

```plaintext
[1] AnalyzerRuleViolation in CartController.java (priority=2, depth=0)
├─ [X] AnalyzerDependencyRuleViolation in pom.xml (priority=2, depth=1)
[2] AnalyzerRuleViolation in CheckoutController.java (priority=2, depth=0)
├─ [X] AnalyzerDependencyRuleViolation in pom.xml (priority=2, depth=1)
```

### At `max_depth=1`

```plaintext
[1] AnalyzerRuleViolation in CartController.java (priority=2, depth=0)
├─ [3] AnalyzerDependencyRuleViolation in pom.xml (priority=2, depth=1)
│  ├─ [X] SymbolNotFoundError in PaymentGateway.java: missing dependency (priority=2, depth=3)
[2] AnalyzerRuleViolation in CheckoutController.java (priority=2, depth=0)
├─ [4] AnalyzerDependencyRuleViolation in pom.xml (priority=2, depth=1)
│  └─ [X] PackageDoesNotExistError in UserProfile.java: missing javax.security package (priority=1, depth=3)
```

- **Explanation**:
  - The TaskManager processes tasks level by level.
  - At each increment of **max_depth**, it delves one level deeper into dependencies.

---

## Priority Seeding

- **Benefit**: Ensures essential tasks are prioritized.

  - Ideal for integrating with external tools (e.g., IDEs) to drive the loop.
  - Ensures user-prioritized issues are processed first.

- **Application**:
  - High-priority tasks can be added to the queue to influence processing order.

---

## Closing: Flexibility and Control in Problem-Solving

- **Key Takeaways**:

  - **Concrete tools** help agents stay grounded and focused on relevant tasks.
  - The **agentic approach** transforms static analysis results directly into targeted code changes.
  - The **task hierarchy** tracks changes and their effects across the codebase.
  - **Customizable parameters** allow for precise control over task prioritization and resolution order.

- **Questions and Discussion**:
  - Open invitation for questions.
