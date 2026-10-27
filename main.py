from abc import ABC, abstractmethod
from threading import Lock


# ==================================================
# 1. SINGLETON: University Configuration System
# ==================================================

class UniversityConfig:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.university_name = "ABC University"
        self.academic_year = "2026-2027"
        self.semester = "First Semester"
        self.working_hours = "9:00 AM - 5:00 PM"
        self.observers = []
        self._initialized = True

    
def update(self, **details):
    allowed = {
        "university_name",
        "academic_year",
        "semester",
        "working_hours"
    }

    # Validate everything before making changes
    invalid = set(details) - allowed
    if invalid:
        raise ValueError(
            f"Invalid configuration: {', '.join(sorted(invalid))}"
        )

    for key, value in details.items():
        setattr(self, key, value)

    self.notify_observers()


    def display(self):
        print("\n--- University Configuration ---")
        print("University:", self.university_name)
        print("Academic Year:", self.academic_year)
        print("Semester:", self.semester)
        print("Working Hours:", self.working_hours)

    # Observer pattern hooks
    def subscribe(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)


# ============================================
# 2. FACTORY METHOD: Notification System
# ============================================

class Notification(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass


class EmailNotification(Notification):
    def send(self, recipient, message):
        print(f"[EMAIL] To: {recipient} | {message}")


class SMSNotification(Notification):
    def send(self, recipient, message):
        print(f"[SMS] To: {recipient} | {message}")


class PushNotification(Notification):
    def send(self, recipient, message):
        print(f"[PUSH] To: {recipient} | {message}")


class NotificationCreator(ABC):
    @abstractmethod
    def create_notification(self):
        pass

    def notify(self, recipient, message):
        notification = self.create_notification()
        notification.send(recipient, message)


class EmailCreator(NotificationCreator):
    def create_notification(self):
        return EmailNotification()


class SMSCreator(NotificationCreator):
    def create_notification(self):
        return SMSNotification()


class PushCreator(NotificationCreator):
    def create_notification(self):
        return PushNotification()


# ============================================
# 3. ADAPTER: Legacy SMS service integration
# ============================================

class LegacySMSService:
    def send_text(self, phone_number, text):
        print(f"[LEGACY SMS] To: {phone_number} | {text}")


class LegacySMSAdapter(Notification):
    def __init__(self, legacy_service):
        self.legacy_service = legacy_service

    def send(self, recipient, message):
        self.legacy_service.send_text(recipient, message)


# ============================================
# 4. OBSERVER: Configuration change listener
# ============================================

class ConfigurationObserver:
    def __init__(self, name):
        self.name = name

    def update(self, config):
        print(
            f"[OBSERVER] {self.name} notified: "
            f"Semester is now {config.semester}"
        )


# ============================================
# 5. STRATEGY: Interchangeable delivery methods
# ============================================

class DeliveryStrategy(ABC):
    @abstractmethod
    def deliver(self, notification, recipient, message):
        pass


class ImmediateDelivery(DeliveryStrategy):
    def deliver(self, notification, recipient, message):
        notification.send(recipient, message)


class PrefixedDelivery(DeliveryStrategy):
    def deliver(self, notification, recipient, message):
        notification.send(recipient, "[UNIVERSITY NOTICE] " + message)


class NotificationContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute(self, notification, recipient, message):
        self.strategy.deliver(notification, recipient, message)


# ============================================
# 6. COMMAND: Encapsulated application actions
# ============================================

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class UpdateConfigurationCommand(Command):
    def __init__(self, config, **details):
        self.config = config
        self.details = details

    def execute(self):
        self.config.update(**self.details)


class SendNotificationCommand(Command):
    def __init__(self, creator, recipient, message):
        self.creator = creator
        self.recipient = recipient
        self.message = message

    def execute(self):
        self.creator.notify(self.recipient, self.message)


class CommandInvoker:
    def execute(self, command):
        command.execute()


# ============================================
# MAIN: Demonstrate all six design patterns
# ============================================

def main():
    # Singleton
    config = UniversityConfig()
    another_config = UniversityConfig()
    print("Same configuration object:", config is another_config)
    config.display()

    # Observer
    admin = ConfigurationObserver("Admin")
    faculty = ConfigurationObserver("Faculty")
    config.subscribe(admin)
    config.subscribe(faculty)

    # Command + Observer
    invoker = CommandInvoker()
    invoker.execute(
        UpdateConfigurationCommand(
            config,
            semester="Second Semester",
            working_hours="8:30 AM - 4:30 PM"
        )
    )
    config.display()

    # Factory Method + Command
    creators = {
        "email": EmailCreator(),
        "sms": SMSCreator(),
        "push": PushCreator()
    }

    for notification_type, recipient in [
        ("email", "student@university.edu"),
        ("sms", "+911234567890"),
        ("push", "student_device_01")
    ]:
        command = SendNotificationCommand(
            creators[notification_type],
            recipient,
            "University semester information updated."
        )
        invoker.execute(command)

    # Adapter
    legacy_sms = LegacySMSAdapter(LegacySMSService())
    legacy_sms.send("+911234567890", "Exam timetable released.")

    # Strategy
    email = EmailNotification()
    delivery = NotificationContext(ImmediateDelivery())
    delivery.execute(email, "student@university.edu", "Welcome!")

    delivery.set_strategy(PrefixedDelivery())
    delivery.execute(
        email,
        "student@university.edu",
        "Your examination starts Monday."
    )

    # Unsubscribe an observer
    config.unsubscribe(faculty)


if __name__ == "__main__":
    main()
