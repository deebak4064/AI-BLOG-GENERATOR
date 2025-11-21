# Contributing to AI Blog Generator

Thank you for your interest in contributing to the AI Blog Generator! 

## ⚠️ Attribution Policy & Enforcement

**This project uses the MIT License with a strong attribution requirement and built-in enforcement.**

### What's Required

If you contribute, fork, or modify this project, you **MUST**:

1. **Retain the original copyright notice** - Keep Deebak Kumar's copyright in all files
2. **Include the LICENSE file** - Always include the LICENSE file in distributions
3. **Credit the original author** - Link back to [https://github.com/deebak4064/AI-BLOG-GENERATOR](https://github.com/deebak4064/AI-BLOG-GENERATOR)
4. **Document changes** - Clearly mark any modifications you make to the original code

### Built-in Enforcement

The application includes an **attribution tracking system** that:

- ✅ **Checks compliance on startup** - Verifies proper attribution when the app starts
- 📋 **Logs deployment instances** - Records every deployment (whether attributed or not)
- ⚠️ **Shows warnings** - Displays prominent warnings if attribution is missing
- 📊 **Generates compliance reports** - Available at `/api/attribution-check`
- 🚨 **Tracks non-compliance** - Maintains historical log of unattributed instances

### What Happens If Attribution Is Missing?

When the app starts, it checks for:
- ✓ LICENSE file exists
- ✓ CITATION.cff file exists
- ✓ README mentions original author
- ✓ Code headers contain attribution

**If any are missing**, you'll see:
```
╔════════════════════════════════════════════════════════════════╗
║                   ⚠️  ATTRIBUTION WARNING  ⚠️                   ║
║ MISSING ATTRIBUTION for: [license, citation, readme_attribution]║
║ Please ensure proper attribution is included...                ║
╚════════════════════════════════════════════════════════════════╝
```

### Compliance Report API

Access `/api/attribution-check` to get a compliance report:
```json
{
  "status": "COMPLIANT|NON-COMPLIANT",
  "attribution_check": {
    "licensed": true,
    "missing_items": []
  },
  "deployment_history": [...],
  "total_instances": 42
}
```

## How to Contribute

### Reporting Issues
- Use the GitHub Issues tab to report bugs
- Provide clear, detailed descriptions
- Include reproduction steps if applicable

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add attribution headers if modifying core files
5. Commit with clear messages
6. Push to your fork
7. Submit a Pull Request with a description

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable/function names
- Add comments for complex logic
- Include docstrings for functions

## Using Modified Versions

If you create a derivative work:
1. Clearly state it's based on AI Blog Generator
2. Link to the original repository
3. List all significant modifications
4. Include the original LICENSE file
5. Give credit to Deepak Kumar in all documentation

## Examples of Proper Attribution

### In Your Project README
```markdown
This project is based on [AI Blog Generator](https://github.com/deebak4064/AI-BLOG-GENERATOR) 
by [Deepak Kumar](https://github.com/deebak4064).

**Modifications made:** Added support for OpenAI API, improved UI styling, added database caching.
```

### In Code Files
```python
"""
Modified version of AI Blog Generator
Original: https://github.com/deebak4064/AI-BLOG-GENERATOR
Original Author: Deepak Kumar

Modifications:
- Added OpenAI API support
- Enhanced blog filtering
- Custom theme implementation
"""
```

### In HTML/Footer
```html
<footer>
    Powered by <a href="https://github.com/deebak4064/AI-BLOG-GENERATOR">
        AI Blog Generator</a> by 
    <a href="https://github.com/deebak4064">Deepak Kumar</a>
</footer>
```

## Questions?

If you have questions about attribution or contributions, please open a GitHub issue.

---

**Remember:** Proper attribution takes 30 seconds but keeps the open-source community strong! ❤️
