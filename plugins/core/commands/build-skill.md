---
description: Build comprehensive Claude Code skills through elicitation-driven development
allowed-tools:
  - Task
  - Read
  - Write
---

# Build Claude Code Skill

Build comprehensive Claude Code skills through elicitation-driven development.

## Instructions

This command orchestrates four specialized agents to create production-ready Claude Code skills from user requirements. Follow this structured workflow:

### Phase 1: Requirements Elicitation

**Agent**: `skill-elicitation-agent`

1. **Activate elicitation agent**
   - Start the skill-elicitation-agent with the Task tool
   - Provide context: "The user wants to create a new Claude Code skill"
   - Include all initial requirements or ideas the user has shared

2. **Elicitation questions**
   - The agent asks 3-5 targeted questions to understand:
     - Purpose and scope of the skill
     - Complexity and structure requirements
     - Required tool permissions
     - Context and references
     - Success criteria

3. **Specification creation**
   - Agent creates a comprehensive skill specification document
   - Includes: metadata, structure, instruction outline, code requirements, examples, dependencies
   - Applies progressive disclosure strategy
   - Validates completeness before proceeding

4. **User approval**
   - Present the specification to the user
   - Confirm understanding and agreement
   - Make adjustments as needed
   - Obtain explicit approval to proceed with generation

### Phase 2: Skill Generation

**Agent**: `skill-generator-agent`

1. **Activate generator agent**
   - Start the skill-generator-agent with the Task tool
   - Pass the approved specification document
   - Specify target location (personal, project, or plugin skill)

2. **Create directory structure**
   - Agent creates the appropriate directory structure:

     ```text
     skill-name/
     ├── SKILL.md (required)
     ├── reference.md (if needed)
     ├── examples.md (if needed)
     ├── scripts/ (if needed)
     └── templates/ (if needed)
     ```

3. **SKILL.md generation**
   - Creates main skill file with correct frontmatter
   - Includes clear instructions and examples
   - Follows progressive disclosure principles
   - Links to supporting files

4. **Generate supporting files**
   - Creates reference documentation
   - Generates example files
   - Writes scripts with proper error handling
   - Creates reusable templates

5. **Dependency documentation**
   - Documents all required packages
   - Provides installation instructions
   - Notes version requirements

6. **Quality checks**
   - Validates YAML frontmatter
   - Checks file structure
   - Verifies code syntax
   - Tests progressive disclosure

### Phase 3: Validation and Testing

**Agent**: `skill-validator-agent`

1. **Activate validator agent**
   - Start the skill-validator-agent with the Task tool
   - Provide path to the generated skill
   - Request comprehensive validation

2. **YAML validation**
   - Check frontmatter syntax
   - Verify required fields
   - Validate optional fields
   - Test YAML parsing

3. **Description analysis**
   - Evaluate discoverability
   - Check trigger keywords
   - Verify clarity and completeness
   - Compare against best practices

4. **Structure validation**
   - Verify file organization
   - Check all references
   - Test script execution
   - Validate permissions

5. **Code testing**
   - Syntax validation
   - Security checks
   - Dependency verification
   - Error handling tests

6. **Integration testing**
   - Test skill loading
   - Verify triggering
   - Check execution flow
   - Validate outputs

7. **Validation report**
   - Generate comprehensive report
   - Score each category
   - List issues by severity
   - Provide actionable fixes

8. **Issue resolution**
   - If issues found, work with generator agent to fix
   - Re-validate after fixes
   - Iterate until validation passes

### Phase 4: Documentation Enhancement

**Agent**: `skill-documenter-agent`

1. **Activate documenter agent**
   - Start the skill-documenter-agent with the Task tool
   - Provide skill path and specification
   - Request comprehensive documentation

2. **SKILL.md enhancement**
   - Refine instructions for clarity
   - Add comprehensive examples
   - Integrate best practices
   - Create troubleshooting section

3. **Reference documentation**
   - Create detailed technical reference (if needed)
   - Document API and configuration
   - Provide advanced patterns
   - Integrate performance tuning tips

4. **Example collection**
   - Generate examples from beginner to advanced
   - Add troubleshooting examples
   - Show integration patterns
   - Provide case studies

5. **README creation**
   - Create skill directory README (if distributable)
   - Document installation
   - Provide quick start
   - Link to full documentation

6. **Documentation quality check**
   - Verify clarity and completeness
   - Test all code examples
   - Check organization
   - Validate accuracy

### Phase 5: Final Delivery

1. **Generate summary**
   - List all created files
   - Document location (personal/project/plugin)
   - Provide usage instructions
   - Include test scenarios

2. **Installation verification**
   - Confirm skill is in the correct location
   - Verify file permissions
   - Check that dependencies are documented
   - Test skill loading

3. **Usage guide**
   - Explain how to trigger the skill
   - Provide example prompts
   - Show expected behavior
   - Link to documentation

4. **Next steps**
   - Suggest testing approach
   - Recommend improvements
   - Explain maintenance
   - Note future extensions

## Agent Coordination

### Sequential Flow

```text
User request
    |
skill-elicitation-agent (requirements)
    |
User approval
    |
skill-generator-agent (creation)
    |
skill-validator-agent (testing)
    |
Fixes if needed (back to generator)
    |
skill-documenter-agent (enhancement)
    |
Final delivery
```

### Agent Communication

**Between agents**:

- Elicitation -> Generator: Pass specification document
- Generator -> Validator: Pass skill location and files
- Validator -> Generator: Pass validation issues (if any)
- Generator -> Documenter: Pass skill for enhancement
- Documenter -> User: Final documentation

**With user**:

- Obtain approval after elicitation
- Confirm location preference (personal/project)
- Review validation results
- Approve final result

## Best Practices

1. **Always begin with elicitation**
   - Do not skip the questioning phase
   - Understand deeply before building
   - Obtain user approval for the specification

2. **Use all four agents**
   - Each has specialized expertise
   - Complete flow ensures quality
   - Do not shortcut the process

3. **Iterate based on validation**
   - Fix issues immediately
   - Re-validate after changes
   - Do not proceed with errors

4. **Test comprehensively**
   - Manual trigger testing
   - Script execution tests
   - Integration tests
   - Real-world scenario tests

5. **Document thoroughly**
   - Clear instructions
   - Comprehensive examples
   - Troubleshooting guides
   - Best practices

## Location Options

### Personal Skills (`~/.claude/skills/`)

Use for:

- Individual workflows
- Experimental skills
- Personal preferences
- Private tools

### Project Skills (`.claude/skills/`)

Use for:

- Team-shared workflows
- Project-specific expertise
- Version-controlled skills
- Collaborative tools

### Plugin Skills (plugin directory structure)

Use for:

- Distributable skills
- Marketplace deployment
- Public sharing
- Bundled capabilities

## Output Format

Provide the user with a comprehensive summary:

```text
Skill created successfully!

Skill: [Skill Name]
Location: [Path]
Type: [simple/multi-file/tool-restricted/code-execution]

Files created:
- SKILL.md - Main skill instructions
- reference.md - Technical reference (if created)
- examples.md - Comprehensive examples (if created)
- scripts/[name].py - Helper scripts (if created)
- README.md - Installation guide (if created)

Validation: PASSED (Score: X/10)

Dependencies:
[List if any, or "None"]

Usage:
Trigger this skill by:
- "[Example trigger 1]"
- "[Example trigger 2]"

Or explicitly: "Use [skill-name] for [task]"

Test with:
[Specific test scenario]

Documentation:
- See SKILL.md for instructions
- See examples.md for comprehensive examples
- See reference.md for technical details

Next steps:
1. Test the skill with provided scenarios
2. Refine based on usage
3. Share with team (if project skill)
4. Consider adding more examples
```

## Troubleshooting

**Agent not found**: Ensure `.claude/agents/skill-builder/` exists with all agent files

**Permission errors**: Check file permissions with `chmod +x scripts/*.py`

**YAML errors**: Validator will catch and report these

**Agent confusion**: Use explicit agent names: "Start skill-elicitation-agent"

## Examples

### Example 1: Simple Instruction-Only Skill

**Request**: "Create a skill for writing Conventional Commit messages"

**Flow**:

1. Elicitation asks about commit style, projects, examples
2. Generates simple single SKILL.md
3. Validates structure and description
4. Documents with examples and best practices

### Example 2: Multi-File Skill with Scripts

**Request**: "Create a skill for filling PDF forms"

**Flow**:

1. Elicitation asks about PDF types, operations, dependencies
2. Generates SKILL.md + scripts/fill_form.py + FORMS.md
3. Validates code execution and file structure
4. Documents with comprehensive examples and API reference

### Example 3: Tool-Restricted Read-Only Skill

**Request**: "Create a skill for security code analysis"

**Flow**:

1. Elicitation determines read-only requirement
2. Generates SKILL.md with allowed-tools: Read, Grep, Glob
3. Validates tool restrictions
4. Documents security patterns and analysis techniques

## Remember

- **Quality over speed** - Take time for thorough elicitation
- **User involvement** - Obtain approval at key stages
- **Comprehensive validation** - Test everything
- **Excellent documentation** - Make skills easy to use
- **Iterative improvement** - Skills can evolve over time

This command ensures every skill is production-ready, well-documented, and follows Claude Code best practices!
