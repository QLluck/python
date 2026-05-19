## Context

The codebase currently has minimal English comments, making it inaccessible to Chinese-speaking beginners. The code implements complex medical image processing algorithms using OpenCV, including preprocessing (CLAHE, morphology), detection (Otsu thresholding, ROI extraction), and segmentation (region growing, watershed). Without detailed explanations, learners struggle to understand both the code logic and the underlying algorithms.

Existing documentation:
- Minimal English docstrings in code
- README with basic usage
- No concept explanations or tutorials

Target audience:
- Chinese-speaking students learning image processing
- Developers new to OpenCV
- Researchers wanting to understand the algorithms
- Contributors who need to maintain/extend the code

## Goals / Non-Goals

**Goals:**
- Make the codebase accessible to zero-foundation Chinese learners
- Explain both "what" (code does) and "why" (design rationale)
- Provide learning resources (concept dictionary, tutorials, examples)
- Use plain language, analogies, and visual descriptions
- Maintain documentation quality standards

**Non-Goals:**
- Translating existing English comments (we're adding new comprehensive documentation)
- Auto-generating comments (manual, thoughtful documentation is needed)
- Documenting every single line (focus on key concepts and algorithms)
- Creating video tutorials or interactive demos
- Translating external dependencies' documentation

## Decisions

### Decision 1: Comment language and style

**Choice:** Comprehensive Chinese comments using plain language with analogies

**Rationale:**
- Target audience is Chinese-speaking beginners
- Technical jargon creates barriers to entry
- Analogies help relate abstract concepts to everyday experiences
- Examples make concepts concrete

**Alternatives considered:**
- Bilingual comments (Chinese + English): Rejected as too verbose, harder to maintain
- English-only with external Chinese guide: Rejected as requires context switching
- Auto-translated comments: Rejected as quality would be poor

### Decision 2: Documentation structure

**Choice:** Three-level documentation (file → function → inline)

**Rationale:**
- File-level: Provides overview and context
- Function-level: Detailed API documentation
- Inline: Explains algorithm steps and rationale
- Mirrors how developers read code (top-down)

**Alternatives considered:**
- Only function-level: Rejected as lacks context
- Separate documentation files: Rejected as requires context switching
- Wiki-style documentation: Rejected as harder to keep in sync with code

### Decision 3: Documentation templates

**Choice:** Standardized templates for file, function, and inline comments

**Rationale:**
- Ensures consistency across modules
- Provides clear structure for contributors
- Makes documentation easier to navigate
- Reduces decision fatigue when writing

**Alternatives considered:**
- Free-form documentation: Rejected as leads to inconsistency
- Minimal templates: Rejected as doesn't provide enough guidance
- Auto-generated templates: Rejected as too rigid

### Decision 4: Module prioritization

**Choice:** Core algorithms first (preprocess, detect, segment, pipeline), then supporting modules

**Rationale:**
- Core modules are most complex and most important to understand
- Supporting modules are simpler and can reference core concepts
- Allows learners to follow the natural processing pipeline
- Maximizes value early in the process

**Alternatives considered:**
- Alphabetical order: Rejected as doesn't reflect importance
- Bottom-up (utilities first): Rejected as lacks context
- All at once: Rejected as too large a task

### Decision 5: Supporting documentation

**Choice:** Create CONCEPTS.md (concept dictionary), TUTORIAL.md (step-by-step guide), EXAMPLES.md (usage examples)

**Rationale:**
- CONCEPTS.md: Central reference for all technical terms
- TUTORIAL.md: Guided learning path for beginners
- EXAMPLES.md: Practical demonstrations of usage
- Separates reference material from code
- Easier to update and extend

**Alternatives considered:**
- Everything in README: Rejected as would be too long
- Inline-only documentation: Rejected as lacks overview
- External wiki: Rejected as harder to maintain

### Decision 6: Example code style

**Choice:** Runnable, commented examples with input/output descriptions

**Rationale:**
- Runnable code can be tested and verified
- Comments explain each step
- Input/output descriptions set expectations
- Learners can experiment by modifying examples

**Alternatives considered:**
- Pseudo-code: Rejected as not directly usable
- Minimal examples: Rejected as doesn't show full context
- Jupyter notebooks: Rejected as adds dependency

### Decision 7: Quality standards

**Choice:** Accuracy, completeness, consistency, maintainability

**Rationale:**
- Accuracy: Wrong documentation is worse than no documentation
- Completeness: Partial documentation leaves gaps
- Consistency: Makes documentation easier to navigate
- Maintainability: Documentation must evolve with code

**Alternatives considered:**
- "Good enough" approach: Rejected as quality would degrade
- Peer review only: Rejected as needs clear standards
- Automated checks only: Rejected as can't verify quality

## Risks / Trade-offs

**[Risk]** Documentation becomes outdated as code evolves  
→ **Mitigation:** Include documentation updates in code review process; add "last updated" dates

**[Risk]** Inconsistent quality across modules  
→ **Mitigation:** Use templates; review all documentation before merging; maintain quality checklist

**[Risk]** Too verbose, making code harder to read  
→ **Mitigation:** Focus on key concepts; use file/function-level docs for details; keep inline comments concise

**[Risk]** Translation quality issues (technical terms, idioms)  
→ **Mitigation:** Use established Chinese technical terminology; avoid direct translation; have native speakers review

**[Risk]** Maintenance burden increases  
→ **Mitigation:** Documentation is part of code changes; templates reduce effort; benefits outweigh costs

**[Trade-off]** Time investment vs. immediate value  
→ **Accepted:** Documentation is an investment that pays off through easier onboarding and maintenance

**[Trade-off]** Chinese-only vs. bilingual  
→ **Accepted:** Chinese-only is simpler and clearer for target audience; English speakers can use code structure and existing minimal comments

**[Trade-off]** Comprehensive vs. minimal documentation  
→ **Accepted:** Comprehensive documentation for core modules, lighter for utilities; target audience needs detailed explanations

## Migration Plan

Not applicable - this is additive documentation work with no code changes or deployment requirements.

## Open Questions

None - approach is straightforward and well-defined.
