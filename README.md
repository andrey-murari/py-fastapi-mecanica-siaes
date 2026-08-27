# py-fastapi-mecanica-siaes


└── py-fastapi-mecanica-siaes/
    ├── src/
    │   ├── security/
    │   │   └── jwt/
    │   ├── application/
    │   │   └── mapper/
    │   ├── domain/
    │   │   ├── customers_and_services/
    │   │   │   ├── __init__.py
    │   │   │   ├── domain_services/
    │   │   │   ├── service_order/
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── entities/
    │   │   │   │       ├── orders.py
    │   │   │   │       ├── order_items.py
    │   │   │   │       └── order_services.py
    │   │   │   ├── relationship/
    │   │   │   │   └── entities/
    │   │   │   │       ├── __init__.py
    │   │   │   │       ├── people.py
    │   │   │   │       ├── addresses.py
    │   │   │   │       ├── customers.py
    │   │   │   │       ├── attendants.py
    │   │   │   │       ├── vehicles.py
    │   │   │   │       └── contacts.py
    │   │   │   └── service/
    │   │   │       ├── value_objects/
    │   │   │       │   └── __init__.py
    │   │   │       ├── commands/
    │   │   │       │   ├── __init__.py
    │   │   │       │   ├── create_service.py
    │   │   │       │   └── alter_service.py
    │   │   │       └── entities/
    │   │   │           ├── __init__.py
    │   │   │           └── services.py
    │   │   └── inventory_and_purchasing/
    │   │       ├── __init__.py
    │   │       ├── inventory/
    │   │       │   ├── services/
    │   │       │   ├── commands/
    │   │       │   ├── entities/
    │   │       │   │   ├── inventory.py
    │   │       │   │   └── operations.py
    │   │       │   └── value_objects/
    │   │       ├── purchasing/
    │   │       │   └── entities/
    │   │       │       ├── supplies.py
    │   │       │       └── parts.py
    │   │       └── domain_services/
    │   │           └── alter_inventory.py
    │   ├── infrastructure/
    │   │   ├── repository/
    │   │   │   ├── port_repository.py
    │   │   │   ├── database.py
    │   │   │   └── in_memory_database.py
    │   │   └── __init__.py
    │   └── __init__.py
    ├── tests/
    │   ├── unit/
    │   └── behavior/
    ├── main.py
    ├── .env
    └── .env.sample
