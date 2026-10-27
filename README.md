# University Management System – Design Patterns

A Python project demonstrating six software design patterns.

## Design Patterns Implemented

1. **Singleton:** Maintains a single university configuration manager for academic year, semester, university name, and working hours.
2. **Factory Method:** Creates Email, SMS, and Push notification objects.
3. **Adapter:** Integrates a legacy SMS service with a common notification interface.
4. **Observer:** Notifies subscribed users when university configuration changes.
5. **Strategy:** Allows notification delivery behavior to be changed at runtime.
6. **Command:** Encapsulates configuration updates and notification requests as command objects.

## Technologies
- Python 3
- Object-Oriented Programming
- Design Patterns

## How to Run
Run the main Python file:

```bash
python main.py
```

## Note
This is an educational demonstration. Notifications are printed to the console rather than delivered through real email, SMS, or push services.
