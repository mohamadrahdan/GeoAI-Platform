# GeoAI Platform – Workflow Rules
This document defines the working principles for developing and maintaining the GeoAI Platform as a long-term, single-developer project.
The goal of these rules is to keep the project structured, understandable, and sustainable over time.

## General Principles
1. Work in small and clear steps.
   Each task should have a clear purpose and a visible outcome.
2. Focus on one task at a time.
   Avoid working on multiple unfinished features in parallel.
3. Prefer clarity over complexity.
   Simple and readable solutions are more valuable than complex ones.
4. Accept imperfect early versions.
   Version 0.x is for learning, testing, and improving.

## Project Structure and Architecture
5. Keep shared logic inside the `core` directory.
   Code that is used by more than one plugin must not be duplicated.
6. Treat each use-case as a plugin.
   New ideas should be implemented as independent plugins whenever possible.
7. Keep plugins loosely coupled.
   Plugins should not depend directly on each other.
8. Update documentation when architecture changes.
   Structure and documentation should always match.

## Git and Version Control
9. Use small and meaningful commits.
   Each commit should represent one logical change.
10. Write clear commit messages.
    Messages should describe what was changed and why.
11. Push changes regularly.
    Code and documentation should not remain only on the local machine.
12. Keep the main branch stable.
    Experimental work should be done carefully and step by step.

## Daily Work Habits
13. Work consistently, even with limited time.
    Short daily progress is better than long inactive periods.
14. Review the project structure frequently.
    Small adjustments are easier than large refactoring later.
15. Think long-term.
    Code and decisions should remain understandable after several months.