# Contributing to Bluetooth Manager

Thank you for your interest in contributing to the Bluetooth Manager Home Assistant add-on! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** - Describe the issue briefly
2. **Description** - Detailed explanation of the bug
3. **Steps to reproduce** - How to recreate the issue
4. **Expected behavior** - What should happen
5. **Actual behavior** - What actually happens
6. **Environment** - Home Assistant version, hardware, etc.
7. **Logs** - Relevant log excerpts if available

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. **Clear title** - Describe the enhancement
2. **Use case** - Why is this enhancement needed?
3. **Proposed solution** - How should it work?
4. **Alternatives** - Any alternative approaches considered?

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main` for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style guidelines
4. **Test your changes** thoroughly
5. **Commit** with clear, descriptive messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```
6. **Push** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

## Development Setup

### Prerequisites

- Python 3.11+
- Docker (for testing the add-on)
- Git
- A Bluetooth-enabled device for testing

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/burhanyldz/bluetooth-actions.git
   cd bluetooth-actions
   ```

2. Set up Python environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the backend locally:
   ```bash
   python app.py --port 8099 --log-level debug
   ```

4. Open the frontend in your browser:
   ```
   http://localhost:8099
   ```

### Testing with Docker

Build and run the Docker container:

```bash
docker build -t bluetooth-manager .

docker run -it --rm \
  --privileged \
  --network host \
  -v /var/run/dbus:/var/run/dbus \
  bluetooth-manager
```

## Code Style Guidelines

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def connect_device(self, mac_address: str) -> Tuple[bool, str]:
    """
    Connect to a Bluetooth device
    
    Args:
        mac_address: MAC address of the device
        
    Returns:
        Tuple of (success, message)
    """
    # Implementation
```

### JavaScript

- Use modern ES6+ syntax
- Use `const` and `let`, avoid `var`
- Write clear, descriptive function names
- Add comments for complex logic
- Keep functions focused

Example:
```javascript
async connectDevice(mac) {
    try {
        this.showLoading('Connecting...');
        await this.api.connectDevice(mac);
        this.showToast('Connected successfully', 'success');
    } catch (error) {
        this.showToast(`Failed: ${error.message}`, 'error');
    } finally {
        this.hideLoading();
    }
}
```

### CSS

- Use CSS custom properties (variables) for colors
- Follow BEM naming convention where appropriate
- Keep selectors specific but not overly nested
- Group related styles together
- Add comments for complex layouts

## Testing

Before submitting a pull request:

1. **Test all functionality** - Ensure existing features still work
2. **Test your changes** - Verify your new feature/fix works as expected
3. **Test on different devices** - Check responsive design on mobile/tablet
4. **Check console** - No JavaScript errors
5. **Check logs** - No Python exceptions
6. **Test error cases** - How does it handle failures?

### Testing Checklist

- [ ] Adapter power on/off works
- [ ] Scanning discovers devices
- [ ] Pairing works correctly
- [ ] Connecting/disconnecting works
- [ ] Device information displays correctly
- [ ] Trust/untrust functions work
- [ ] Remove device works
- [ ] UI is responsive on mobile
- [ ] Toast notifications appear correctly
- [ ] Loading states show appropriately
- [ ] No console errors
- [ ] No Python exceptions in logs

## Documentation

When adding new features:

1. Update the **README.md** if needed
2. Add docstrings to Python functions
3. Comment complex JavaScript code
4. Update **CHANGELOG.md**
5. Update API documentation if adding endpoints

## Project Structure

```
bluetooth-actions/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── bluetooth_manager.py   # Bluetooth operations
│   ├── utils.py              # Helper functions
│   └── requirements.txt      # Python dependencies
├── web/
│   ├── index.html           # Main HTML
│   ├── css/
│   │   └── style.css       # Styles
│   └── js/
│       ├── api.js          # API client
│       └── app.js          # Main application
├── config.yaml             # Add-on configuration
├── config.json             # Add-on metadata
├── Dockerfile             # Container definition
├── run.sh                # Startup script
└── README.md            # Documentation
```

## Git Commit Messages

Write clear commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests after the first line

Good examples:
```
Add battery level display to device cards

Fix connection timeout error handling

Update README with troubleshooting section

Refactor device scanning for better performance
Closes #123
```

## Questions?

If you have questions about contributing:

1. Check existing issues and pull requests
2. Read the README and documentation
3. Create a new issue with your question

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute! 🎉
