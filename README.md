## Dataset Curation

This dataset was created to examine publication trends in robotic-manipulation task planning, with particular emphasis on world models, natural-language instructions, long-horizon tasks, and planning methods.

The initial paper search, download, and text preprocessing were performed through a combination of **human review and Python-based code**. The relevant preprocessing and analysis workflows are documented in the Jupyter notebooks available in the `notebooks/` directory.

Final paper annotation was performed by loading the preprocessed papers into **OpenAI GPT-5.6 Thinking** in batches. Each paper was classified using a consistent schema covering publication metadata, task domain, world-model use, planning approach, language conditioning, evaluation setting, robot platform, and related methodological details. Definition-sensitive decisions, such as distinguishing world models from direct policies and planning from closed-loop action prediction, were recorded with supporting evidence and review notes.

After curation, the consolidated dataset was analyzed again to generate summary statistics and visualizations.

### Limitations

* The corpus is targeted rather than exhaustive and may omit relevant publications.
* Paper selection reflects the chosen emphasis on manipulation, planning, world models, and language conditioning.
* Several recent entries are preprints whose details may change.
* Some labels require interpretation because terms such as *world model*, *planning*, and *long horizon* are used inconsistently in the literature.
* LLM-generated annotations may contain errors and were not validated through full experimental reproduction.
* Reported percentages describe this curated dataset only and should not be interpreted as estimates for the entire robotics literature.


## Summary Results (Numerical Overview)
## Metric Definitions

The percentages below use the **47 method papers** as the denominator. These categories are not mutually exclusive, so a single paper may be counted under several metrics.

| Metric                            | Meaning in this dataset                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **World-model methods**           | Methods containing a learned model that predicts how the environment evolves. Predictions may be future images, latent states, object states, rewards, or other task-relevant states. Direct action-only policies, frozen visual encoders used only for representation, ordinary history-conditioned policies, knowledge graphs without learned transitions, and analytical simulators were excluded. |
| **Explicit-planning methods**     | Methods that explicitly search for, optimize, select, or structurally construct behavior. Examples include MPC, CEM, MCTS, A*, Bayesian optimization, task-and-motion planning, symbolic planning, and learned high-level subgoal planning. Direct policies that simply output an action or action chunk were not counted.                                                                            |
| **Long-horizon methods**          | Methods evaluated on temporally extended tasks involving multiple stages, subgoals, skills, or prolonged interaction. This refers to the **task horizon**, not necessarily the numerical prediction or planning horizon.                                                                                                                                                                              |
| **Language-conditioned methods**  | Methods where natural language is an actual input used to specify the task, goal, subtask, reward, plan, or desired behavior. Papers that only discuss language without conditioning the method were not counted.                                                                                                                                                                                     |
| **Hierarchical-planning methods** | Methods containing at least two distinct planning or control levels, such as an LLM task planner above a skill controller, a symbolic planner above motion planning, or a latent high-level planner above a low-level policy.                                                                                        |
| **Online-replanning methods**     | Methods that update their plan, subgoal, action sequence, or action chunk using new observations during execution. This includes explicit receding-horizon planners and direct closed-loop policies that regenerate actions from feedback.                                                                                                                                                            |
| **Real-robot methods**            | Methods evaluated or deployed on physical robot hardware. Training only on previously collected real-robot data was not normally counted unless the proposed method was physically executed or evaluated.                                                                                                                                                                                             |
| **Simulation methods**            | Methods evaluated in a simulator or simulated benchmark, including physics-based manipulation or control environments. Papers evaluated in both simulation and the real world are counted in both categories.                                                                                                                                                                            |

## Important Classification Distinctions

* **World model vs. planner:** A method may predict future states without using those predictions to search for or optimize actions. Therefore, not every world-model method is an explicit-planning method.

* **Long horizon vs. planning horizon:** A method can solve a long, multi-stage task while only predicting or planning a short action chunk at each step. `long_horizon` describes the task, while `planning_horizon` describes how far the planner explicitly reasons ahead.

* **Hierarchical architecture vs. hierarchical planning:** A system containing several neural modules is not automatically hierarchical planning. The method must contain distinct decision-making levels, such as task planning, skill selection, and low-level control.

* **Online replanning vs. explicit planning:** Online replanning is broader than search-based planning. A direct policy that regenerates action chunks from new observations may count as online replanning even when `uses_planning = No`.

* **Real-robot data vs. real-robot evaluation:** Using a dataset collected from physical robots does not necessarily mean the proposed method was evaluated on hardware. `real_robot = Yes` generally requires physical execution or deployment of the method.

* **Simulation and real-robot evaluation:** These categories overlap. A paper tested in both simulation and on physical hardware is included in both counts.

| Metric                        | Count | Percentage |
| ----------------------------- | ----: | ---------: |
| Papers analyzed               |    47 |     100.0% |
| World-model methods           |    26 |      55.3% |
| Explicit-planning methods     |    30 |      63.8% |
| Long-horizon methods          |    24 |      51.1% |
| Language-conditioned methods  |    24 |      51.1% |
| Hierarchical-planning methods |    20 |      42.6% |
| Online-replanning methods     |    36 |      76.6% |
| Real-robot methods            |    33 |      70.2% |
| Simulation methods            |    37 |      78.7% |
