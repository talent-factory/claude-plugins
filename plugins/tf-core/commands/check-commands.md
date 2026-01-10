# Check Commands

Validate Claude Code command files for correctness and best practices.

## Context

You are helping validate command files to ensure they follow Claude Code best practices and will work correctly.

## Validation Checklist

### 1. File Format
- [ ] File has `.md` extension
- [ ] File uses Markdown syntax
- [ ] File is UTF-8 encoded
- [ ] No special characters in filename

### 2. Structure
- [ ] Has clear title/heading
- [ ] Includes context section
- [ ] Provides clear instructions
- [ ] Has examples when appropriate

### 3. Content Quality
- [ ] Instructions are clear and specific
- [ ] Examples are correct and helpful
- [ ] No ambiguous language
- [ ] Appropriate level of detail

### 4. Best Practices
- [ ] Follows progressive disclosure pattern
- [ ] Uses appropriate formatting
- [ ] Includes error handling guidance
- [ ] Has interactive mode if applicable

## Validation Process

### Step 1: File Existence
```bash
# Check if command file exists
ls -la commands/*.md
```

### Step 2: Syntax Check
```bash
# Validate markdown syntax
# Using a markdown linter
mdl commands/*.md
```

### Step 3: Content Review

Read each command file and check:

1. **Title Section**
   - Clear, descriptive title
   - Brief purpose statement

2. **Context Section**
   - Explains the command's role
   - Provides necessary background

3. **Instructions Section**
   - Step-by-step guidance
   - Clear expectations
   - Error handling

4. **Examples Section**
   - Working examples
   - Common use cases
   - Expected outputs

### Step 4: Test Execution

Try using the command:
```bash
# Load the command in Claude Code
claude --plugin-dir ./plugins/[plugin-name]

# Test the command
/command-name
```

## Common Issues

### Issue 1: Missing Context
**Problem:** Command doesn't explain its purpose
**Fix:** Add context section at the top

### Issue 2: Unclear Instructions
**Problem:** Steps are vague or confusing
**Fix:** Use numbered lists, be specific

### Issue 3: No Examples
**Problem:** Users don't know how to use it
**Fix:** Add practical examples

### Issue 4: Too Complex
**Problem:** Command tries to do too much
**Fix:** Split into multiple commands

## Quality Criteria

### Good Command Characteristics

1. **Single Purpose**
   - Does one thing well
   - Clear, focused scope
   - Easy to understand

2. **Clear Instructions**
   - Step-by-step guidance
   - Unambiguous language
   - Appropriate detail level

3. **Helpful Examples**
   - Show common use cases
   - Include expected output
   - Cover edge cases

4. **Error Handling**
   - Anticipate problems
   - Provide solutions
   - Guide recovery

### Command Template

```markdown
# [Command Name]

Brief description of what this command does.

## Context

Explain when and why to use this command.

## Instructions

1. First step
2. Second step
3. Third step

## Examples

### Example 1: [Use Case]
\`\`\`
[Code or command]
\`\`\`

Expected result: [Description]

### Example 2: [Another Use Case]
\`\`\`
[Code or command]
\`\`\`

Expected result: [Description]

## Tips

- Tip 1
- Tip 2

## Troubleshooting

**Issue:** [Problem]
**Solution:** [Fix]
```

## Automated Checks

Create a validation script:

```bash
#!/bin/bash

# Check all command files
for file in commands/*.md; do
    echo "Checking $file..."
    
    # Check file exists and is readable
    if [ ! -r "$file" ]; then
        echo "❌ Cannot read $file"
        continue
    fi
    
    # Check for title
    if ! grep -q "^# " "$file"; then
        echo "❌ No title found in $file"
    else
        echo "✅ Title found"
    fi
    
    # Check for context
    if ! grep -qi "context" "$file"; then
        echo "⚠️  No context section in $file"
    else
        echo "✅ Context section found"
    fi
    
    # Check for examples
    if ! grep -q "```" "$file"; then
        echo "⚠️  No code examples in $file"
    else
        echo "✅ Code examples found"
    fi
    
    echo ""
done
```

## Report Format

After validation, generate a report:

```markdown
## Command Validation Report

Date: [Date]
Plugin: [Plugin Name]
Commands Checked: [Number]

### Summary
- ✅ Passed: [Number]
- ⚠️  Warnings: [Number]
- ❌ Failed: [Number]

### Details

#### commands/commit.md
- ✅ Valid file format
- ✅ Has title
- ✅ Has context
- ✅ Has examples
- ⚠️  Consider adding error handling section

#### commands/create-pr.md
- ✅ Valid file format
- ✅ Has title
- ✅ Has context
- ✅ Has examples
- ✅ Complete

### Recommendations
1. Add error handling to commit.md
2. Consider splitting large commands
3. All other commands are good to go
```

## Interactive Mode

Ask the user:
1. Which plugin to validate?
2. Validate all commands or specific ones?
3. Generate detailed report?
4. Fix issues automatically where possible?

Then perform validation and present results.

## Next Steps

After validation:
1. Fix any critical issues
2. Address warnings
3. Update documentation
4. Test commands in real use
5. Get peer review
