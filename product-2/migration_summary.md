# Microservice Migration Summary

# TestManagementService Microservice Migration Report

## Overview
The TestManagementService is a microservice that is part of a larger application. It is responsible for managing and executing tests within the application. This report provides a detailed analysis of the microservice's structure and a step-by-step guide on how to migrate it from a monolithic architecture to a microservices architecture.

## File: TestBookStoreApplication.java
**File Path:** `test/TestBookStoreApplication.java`

This file serves as the entry point for the TestManagementService microservice. It contains the main function which runs the BookStoreApplication with TestcontainersConfiguration.

### Function: main
**Description:** The main function which is the entry point of the application. It runs the BookStoreApplication with TestcontainersConfiguration.

**Calls to Other Microservices:** This function calls the ApplicationManagementService microservice.

## File: TestcontainersConfiguration.java
**File Path:** `test/java/com/sivalabs/bookstore/TestcontainersConfiguration.java`

This file contains configurations for various containers used in the application, including PostgreSQL, RabbitMQ, and Zipkin.

### Function: postgresContainer
**Description:** This function returns a PostgreSQL container.

### Function: rabbitmq
**Description:** This function returns a RabbitMQ container.

### Function: zipkinContainer
**Description:** This function returns a Zipkin container.

## Migration from Monolith to Microservices Architecture

1. **Identify Microservice Boundaries:** The first step in migrating from a monolithic architecture to a microservices architecture is to identify the boundaries of the TestManagementService microservice. This involves understanding the responsibilities of the microservice and how it interacts with other parts of the application.

2. **Decouple the Microservice:** Once the boundaries have been identified, the next step is to decouple the TestManagementService microservice from the rest of the application. This involves separating the code, data, and any dependencies of the microservice.

3. **Create a Separate Repository:** After decoupling the microservice, create a separate repository for the TestManagementService microservice. This will allow for independent development and deployment of the microservice.

4. **Update Inter-service Communication:** Update the main function in the TestBookStoreApplication.java file to communicate with the ApplicationManagementService microservice using a method suitable for microservices, such as HTTP/REST or messaging.

5. **Test the Microservice Independently:** After updating the inter-service communication, test the TestManagementService microservice independently to ensure it functions as expected.

6. **Deploy the Microservice:** Once testing is complete, the TestManagementService microservice can be deployed independently from the rest of the application.

## Dependency Hierarchy

```
TestManagementService
|
└── TestBookStoreApplication.java
|   |
|   └── main (calls ApplicationManagementService)
|
└── TestcontainersConfiguration.java
    |
    ├── postgresContainer
    ├── rabbitmq
    └── zipkinContainer
```

---

# Microservice Migration Report

## Microservice Name: ApplicationManagementService

### Overview
The ApplicationManagementService is a microservice that is responsible for managing the application. It contains several files, each with its own set of functions. The files and their respective functions are detailed below.

---

### File: BookStoreApplication.java
**File Path:** application_management/BookStoreApplication.java

This file is the main entry point for the Spring Application.

#### Functions:
- **main:** The main method which starts the Spring Application. It does not call any other microservices.

---

### File: PagedResult.java
**File Path:** application_management/common/models/PagedResult.java

This file is a model class that represents a paged result. It is used to handle paginated data.

#### Functions:
- **PagedResult:** A constructor that takes a Page object and initializes the PagedResult object with the properties of the Page. It does not call any other microservices.
- **of:** A static method that takes a PagedResult object and a Function object. It applies the function to the data of the PagedResult and returns a new PagedResult with the transformed data. It does not call any other microservices.

---

### File: RabbitMQConfig.java
**File Path:** application/config/RabbitMQConfig.java

This file is used to configure RabbitMQ for the application.

#### Functions:
- **exchange:** This function returns a new TopicExchange with the name 'BookStoreExchange'. It does not call any other microservices.
- **newOrdersQueue:** This function returns a new Queue with the name 'new-orders'. It does not call any other microservices.
- **newOrdersQueueBinding:** This function returns a new Binding that binds the newOrdersQueue to the exchange with the routing key 'orders.new'. It does not call any other microservices.
- **rabbitTemplate:** This function returns a new RabbitTemplate with a specified ConnectionFactory and a message converter set to a Jackson2JsonMessageConverter. It does not call any other microservices.
- **producerJackson2MessageConverter:** This function returns a new Jackson2JsonMessageConverter with a specified ObjectMapper. It does not call any other microservices.

---

## Migration from Monolith to Microservices Architecture

The migration process from a monolithic architecture to a microservices architecture involves several steps:

1. **Identify Business Capabilities:** Identify the business capabilities of your application. These capabilities should be loosely coupled and highly cohesive.

2. **Define Services:** Define services based on the identified business capabilities. Each service should be independent and should have its own database to ensure loose coupling.

3. **Design API Gateway:** Design an API Gateway that will act as a single entry point for all the client requests. The API Gateway will route the requests to the appropriate microservices.

4. **Implement Services:** Implement the services identified in step 2. Each service should be independently deployable.

5. **Test:** Test each service independently and also test the interaction between services.

6. **Deploy:** Deploy the microservices in a containerized environment for isolation and scalability.

The following diagram illustrates the process:

```
Monolithic Application
        |
        v
Identify Business Capabilities
        |
        v
Define Services
        |
        v
Design API Gateway
        |
        v
Implement Services
        |
        v
Test
        |
        v
Deploy
        |
        v
Microservices Architecture
```

Please note that this is a high-level overview of the migration process. The actual process may vary based on the specific requirements and constraints of your project.

---

# Microservice Report: InventoryManagementService

## Overview
The InventoryManagementService is a microservice responsible for managing inventory related operations. It provides functionalities such as getting and setting inventory details, finding inventory by product code, decreasing stock level, and handling order events.

## Migration from Monolith to Microservices
To migrate the InventoryManagementService from a monolithic architecture to a microservices architecture, follow these steps:

1. **Identify the Service Boundaries**: Identify the functionalities that can be separated into the InventoryManagementService. In this case, the functionalities are already identified and separated in the JSON data.

2. **Create the Service**: Create a separate service for the InventoryManagementService. This service will have its own codebase and database.

3. **Decompose the Database**: Decompose the monolithic database into a database that is specific to the InventoryManagementService.

4. **Implement the Service**: Implement the functionalities identified for the InventoryManagementService. The details of the files and functions are given below.

5. **Test the Service**: Test the service thoroughly to ensure that it is working as expected.

6. **Deploy the Service**: Deploy the service in its own container or server.

7. **Update the Clients**: Update the clients to use the InventoryManagementService.

8. **Monitor the Service**: Monitor the service to identify and fix any issues.

## Files and Functions

### File: InventoryEntity.java
**File Path**: inventory/domain/InventoryEntity.java

This file defines the InventoryEntity class, which represents an inventory item in the system. It contains the following functions:

- `getId`: This function returns the id of the inventory entity.
- `setId`: This function sets the id of the inventory entity.
- `getProductCode`: This function returns the product code of the inventory entity.
- `setProductCode`: This function sets the product code of the inventory entity.
- `getQuantity`: This function returns the quantity of the inventory entity.
- `setQuantity`: This function sets the quantity of the inventory entity.

### File: InventoryRepository.java
**File Path**: inventory/domain/InventoryRepository.java

This file defines the InventoryRepository class, which is used to interact with the database. It contains the following function:

- `findByProductCode`: This function is used to find an InventoryEntity by its product code. It returns an Optional that contains the InventoryEntity if it exists, or is empty if it does not.

### File: InventoryService.java
**File Path**: inventory/domain/InventoryService.java

This file defines the InventoryService class, which provides services related to inventory management. It contains the following functions:

- `InventoryService`: Constructor for the InventoryService class. It initializes the inventoryRepository object.
- `decreaseStockLevel`: This function decreases the stock level for a given product code and quantity. If the product code is invalid, it logs a warning.
- `getStockLevel`: This function returns the current stock level for a given product code.

### File: OrderEventInventoryHandler.java
**File Path**: inventory/domain/OrderEventInventoryHandler.java

This file defines the OrderEventInventoryHandler class, which handles the event of order creation. It contains the following functions:

- `OrderEventInventoryHandler`: Constructor for the OrderEventInventoryHandler class. It initializes the inventoryService object.
- `handle`: This function handles the event of order creation. It logs the event and decreases the stock level according to the product code and quantity in the event. This function calls the OrderManagementService microservice.

---

# Microservice Report: ProductManagementService

## Overview
The `ProductManagementService` is a microservice responsible for managing products in the system. It handles tasks such as fetching product details, handling product exceptions, and managing product repositories.

## Migration from Monolith to Microservices
The migration from a monolithic architecture to a microservices architecture involves breaking down the monolithic application into smaller, independent services that can be developed, deployed, and scaled independently. Here are the steps for migrating the `ProductManagementService`:

1. **Identify the Boundaries**: Identify the functionalities that will be handled by the `ProductManagementService`. In this case, it includes managing product details, handling product exceptions, and managing product repositories.

2. **Create the Microservice**: Create the `ProductManagementService` microservice with its own database and server.

3. **Migrate the Code**: Migrate the relevant code from the monolithic application to the `ProductManagementService`. This includes the code for managing product details, handling product exceptions, and managing product repositories.

4. **Test the Microservice**: Test the `ProductManagementService` independently to ensure it functions as expected.

5. **Deploy the Microservice**: Deploy the `ProductManagementService` and ensure it can communicate with other microservices in the system.

6. **Iterate**: Repeat the process for other functionalities in the monolithic application until all functionalities have been migrated to microservices.

## Files and Functions
Below are the files and functions in the `ProductManagementService`:

### 1. ProductDto.java
- **File Path**: `product/domain/ProductDto.java`
- **Purpose**: This file contains the data transfer object for products.
- **Functions**:
  - `getDisplayName`: Returns the product name if it is 20 characters or less. If it is more than 20 characters, it returns the first 20 characters followed by '...'.

### 2. ProductNotFoundException.java
- **File Path**: `product/domain/ProductNotFoundException.java`
- **Purpose**: This file handles the exception when a product is not found.
- **Functions**:
  - `ProductNotFoundException`: Constructor function that takes a string message as an argument and passes it to the superclass constructor.
  - `forCode`: Static method that takes a string code as an argument, creates a new ProductNotFoundException with a custom message, and returns it.

### 3. ProductRepository.java
- **File Path**: `product/domain/ProductRepository.java`
- **Purpose**: This file manages the product repository.
- **Functions**:
  - `findByCode`: Finds a ProductEntity by its code. Returns an Optional that contains the ProductEntity if found, or is empty if not found.

### 4. ProductEntity.java
- **File Path**: `product/domain/ProductEntity.java`
- **Purpose**: This file represents the product entity.
- **Functions**:
  - `getId`: Returns the id of the product.
  - `setId`: Sets the id of the product.
  - `getCode`: Returns the code of the product.
  - `setCode`: Sets the code of the product.
  - `getName`: Returns the name of the product.
  - `setName`: Sets the name of the product.
  - `getDescription`: Returns the description of the product.
  - `setDescription`: Sets the description of the product.
  - `getImageUrl`: Returns the image URL of the product.
  - `setImageUrl`: Sets the image URL of the product.
  - `getPrice`: Returns the price of the product.
  - `setPrice`: Sets the price of the product.

### 5. ProductMapper.java
- **File Path**: `product/domain/mappers/ProductMapper.java`
- **Purpose**: This file maps a ProductEntity object to a ProductDto object.
- **Functions**:
  - `mapToDto`: Takes a ProductEntity object as input and maps it to a ProductDto object.

### 6. CatalogExceptionHandler.java
- **File Path**: `productmanagement/web/CatalogExceptionHandler.java`
- **Purpose**: This file handles the ProductNotFoundException.
- **Functions**:
  - `handle`: Handles the ProductNotFoundException. It creates a ProblemDetail object with the status NOT_FOUND and the exception message.

### 7. ProductApi.java
- **File Path**: `product/domain/ProductApi.java`
- **Purpose**: This file represents the product API.
- **Functions**:
  - `ProductApi`: Constructor for the ProductApi class. It initializes the productService and productMapper.
  - `getByCode`: Retrieves a product by its code.

### 8. ProductService.java
- **File Path**: `productmanagement/domain/ProductService.java`
- **Purpose**: This file represents the product service.
- **Functions**:
  - `ProductService`: Constructor for ProductService. It initializes the ProductRepository instance.
  - `getProducts`: Returns a page of products sorted by name in ascending order.
  - `getByCode`: Returns an Optional of ProductEntity by the product code.

### 9. ProductRestController.java
- **File Path**: `product_management/web/ProductRestController.java`
- **Purpose**: This file represents the product REST controller.
- **Functions**:
  - `ProductRestController`: Constructor for the ProductRestController class. It initializes the productService and productMapper.
  - `getProducts`: Fetches a page of products.
  - `getProductByCode`: Fetches a product by its code.

### 10. ProductWebController.java
- **File Path**: `product_management/web/ProductWebController.java`
- **Purpose**: This file represents the product web controller.
- **Functions**:
  - `ProductWebController`: Constructor for the ProductWebController class. It initializes ProductService and ProductMapper objects.
  - `index`: Redirects to the '/products' URL.
  - `showProducts`: Fetches products for a given page and adds them to the model.

## Dependency Hierarchy
The `ProductManagementService` has a clear dependency hierarchy. The `ProductRestController` and `ProductWebController` depend on the `ProductService` and `ProductMapper`. The `ProductService` depends on the `ProductRepository`. The `ProductMapper` depends on the `ProductDto` and `ProductEntity`. The `ProductEntity` and `ProductDto` are the base entities and do not depend on any other classes or services.

---

# OrderManagementService Microservice

## Overview

The OrderManagementService is a microservice responsible for managing customer orders. It handles order creation, retrieval, and exception handling. It also interacts with the ProductManagementService to validate order requests.

## Migration from Monolith to Microservices

The migration from a monolithic architecture to a microservices architecture involves breaking down the application into smaller, independent services. Here is a step-by-step guide on how to migrate the OrderManagementService:

1. **Identify the Service Boundaries**: Identify the functionalities that can be grouped together as a service. In this case, the OrderManagementService handles all functionalities related to orders.

2. **Create a Separate Codebase**: Create a separate codebase for the OrderManagementService. This includes all the Java files listed below.

3. **Create a Database Schema**: If the monolithic application was using a single database, create a separate database schema for the OrderManagementService.

4. **Implement Communication**: Implement communication between the OrderManagementService and other services. In this case, the OrderManagementService communicates with the ProductManagementService.

5. **Test**: Thoroughly test the OrderManagementService to ensure it works as expected.

6. **Deploy**: Deploy the OrderManagementService independently from the other services.

## Files and Functions

### Customer.java

- **File Path**: orders/domain/models/Customer.java
- **Purpose**: Represents a customer in the system. Does not contain any functions.

### CartController.java

- **File Path**: orders/web/CartController.java
- **Purpose**: Handles web requests related to the shopping cart. Does not contain any functions.

### OrderForm.java

- **File Path**: orders/web/OrderForm.java
- **Purpose**: Represents the form for placing an order. Does not contain any functions.

### CreateOrderResponse.java

- **File Path**: orders/domain/CreateOrderResponse.java
- **Purpose**: Represents the response after creating an order. Does not contain any functions.

### OrderWebController.java

- **File Path**: orders/web/OrderWebController.java
- **Purpose**: Handles web requests related to orders. Does not contain any functions.

### OrderStatus.java

- **File Path**: orders/domain/models/OrderStatus.java
- **Purpose**: Represents the status of an order. Does not contain any functions.

### OrderItem.java

- **File Path**: orders/domain/models/OrderItem.java
- **Purpose**: Represents an item in an order. Does not contain any functions.

### InvalidOrderException.java

- **File Path**: orders/exceptions/InvalidOrderException.java
- **Purpose**: Represents an exception thrown when an invalid order is created.

    - `InvalidOrderException`: This is a constructor function for the InvalidOrderException class. It takes a string message as an argument and passes it to the superclass constructor.

### OrderNotFoundException.java

- **File Path**: orders/exceptions/OrderNotFoundException.java
- **Purpose**: Represents an exception thrown when an order is not found.

    - `OrderNotFoundException`: This is a constructor that takes a string message as an argument and passes it to the superclass constructor.
    - `forOrderNumber`: This is a static method that takes a string orderNumber as an argument and returns a new instance of OrderNotFoundException with a custom message.

### OrderCreatedEvent.java

- **File Path**: orders/domain/models/OrderCreatedEvent.java
- **Purpose**: Represents the event of an order being created. Does not contain any functions.

### Cart.java

- **File Path**: orders/web/Cart.java
- **Purpose**: Represents a shopping cart.

    - `getItem`: Returns the LineItem object currently stored in the cart.
    - `setItem`: Sets the LineItem object to be stored in the cart.
    - `getTotalAmount`: Calculates and returns the total amount of the cart by multiplying the price and quantity of the LineItem. If the cart is empty, it returns zero.
    - `removeItem`: Removes the LineItem object from the cart by setting it to null.
    - `updateItemQuantity`: Updates the quantity of the LineItem in the cart. If the quantity is less than or equal to zero, it removes the item from the cart.
    - `LineItem`: Inner class representing an item in the cart. It has fields for code, name, price, and quantity, and corresponding getter and setter methods.

### CartUtil.java

- **File Path**: orders/web/CartUtil.java
- **Purpose**: Provides utility functions for the shopping cart.

    - `getCart`: This function retrieves a Cart object from the HttpSession. If the Cart object does not exist, it creates a new one.

### CreateOrderRequest.java

- **File Path**: orders/domain/CreateOrderRequest.java
- **Purpose**: Represents a request to create an order.

    - `CreateOrderRequest`: A record class that represents a request to create an order. It validates the customer, delivery address, and order item.

### OrderView.java

- **File Path**: orders/domain/OrderView.java
- **Purpose**: Represents a view of an order. Does not contain any functions.

### OrderDto.java

- **File Path**: orders/domain/OrderDto.java
- **Purpose**: Represents a Data Transfer Object (DTO) for an order.

    - `getTotalAmount`: This function returns the total amount of the order by multiplying the price of the item by its quantity. It uses the BigDecimal class for the multiplication and the OrderItem class for accessing the price and quantity of the item.

### OrdersExceptionHandler.java

- **File Path**: order_management/web/OrdersExceptionHandler.java
- **Purpose**: Handles exceptions related to orders.

    - `handle`: Handles the OrderNotFoundException by creating a ProblemDetail object with the status NOT_FOUND and the exception message. It also sets the title of the problem detail to 'Order Not Found' and adds a timestamp.
    - `handle`: Handles the InvalidOrderException by creating a ProblemDetail object with the status BAD_REQUEST and the exception message. It also sets the title of the problem detail to 'Invalid Order Creation Request' and adds a timestamp.

### OrderEventNotificationHandler.java

- **File Path**: ordermanagement/handlers/OrderEventNotificationHandler.java
- **Purpose**: Handles the event of an order being created.

    - `handle`: This function handles the event when an order is created. It logs the information of the created order event.

### OrderRepository.java

- **File Path**: orders/domain/OrderRepository.java
- **Purpose**: Provides functions to interact with the database for orders.

    - `findAllBy`: This function returns a list of all OrderEntity objects, sorted according to the provided Sort object. It uses a custom SQL query to fetch the data.
    - `findByOrderNumber`: This function returns an Optional containing the OrderEntity object that matches the provided order number. If no match is found, the Optional is empty. It uses a custom SQL query to fetch the data.

### OrderMapper.java

- **File Path**: orders/mappers/OrderMapper.java
- **Purpose**: Provides functions to convert between different order-related objects.

    - `convertToEntity`: Converts a CreateOrderRequest object into an OrderEntity object. Sets a random UUID as the order number, sets the status to NEW, and copies the customer, delivery address, and order item from the request.
    - `convertToDto`: Converts an OrderEntity object into an OrderDto object. Copies the order number, order item, customer, delivery address, status, and creation time from the entity.
    - `convertToOrderViews`: Converts a list of OrderEntity objects into a list of OrderView objects. For each order entity, creates a new OrderView with the order number, status, and customer, and adds it to the list.

### OrderService.java

- **File Path**: orders/domain/OrderService.java
- **Purpose**: Provides services related to orders.

    - `OrderService`: Constructor for OrderService class. It initializes OrderRepository and ApplicationEventPublisher.
    - `createOrder`: This function creates an order, logs the order creation, creates an OrderCreatedEvent and publishes it, and returns the saved order.
    - `findOrder`: This function finds an order by its order number and returns it.
    - `findOrders`: This function finds all orders, sorts them in descending order by id, and returns them.

### OrderEntity.java

- **File Path**: orders/domain/OrderEntity.java
- **Purpose**: Represents an order in the database.

    - `OrderEntity`: Default constructor
    - `OrderEntity`: Overloaded constructor
    - `getId`: Getter for id
    - `setId`: Setter for id
    - `getOrderNumber`: Getter for orderNumber
    - `setOrderNumber`: Setter for orderNumber
    - `getCustomer`: Getter for customer
    - `setCustomer`: Setter for customer
    - `getDeliveryAddress`: Getter for deliveryAddress
    - `setDeliveryAddress`: Setter for deliveryAddress
    - `getOrderItem`: Getter for orderItem
    - `setOrderItem`: Setter for orderItem
    - `getStatus`: Getter for status
    - `setStatus`: Setter for status
    - `getCreatedAt`: Getter for createdAt
    - `setCreatedAt`: Setter for createdAt
    - `getUpdatedAt`: Getter for updatedAt
    - `setUpdatedAt`: Setter for updatedAt

### OrderWebSupport.java

- **File Path**: orders/web/OrderWebSupport.java
- **Purpose**: Provides support for the web layer of the OrderManagementService.

    - `OrderWebSupport`: This is a constructor function for the OrderWebSupport class. It takes a ProductApi object as an argument and assigns it to the 'productApi' field of the created object. It calls the ProductManagementService.
    - `validate`: This function validates a CreateOrderRequest object. It checks if the product code in the request matches a product in the ProductApi, and if the price of the product in the request matches the price of the product in the ProductApi. If either check fails, it throws an InvalidOrderException. It calls the ProductManagementService.

### OrdersApi.java

- **File Path**: order_management/api/OrdersApi.java
- **Purpose**: Provides an API for interacting with orders.

    - `OrdersApi`: Constructor for OrdersApi class. It initializes the OrderService.
    - `createOrder`: This function takes a CreateOrderRequest object, converts it to an OrderEntity object, creates an order using the OrderService, and returns a CreateOrderResponse object.
    - `findOrder`: This function takes an order number, finds the order using the OrderService, converts the OrderEntity to OrderDto if the order is found, and returns an Optional of OrderDto.
    - `findOrders`: This function finds all orders using the OrderService, converts the list of OrderEntity to OrderView, and returns a list of OrderView.

### OrderRestController.java

- **File Path**: orders/web/OrderRestController.java
- **Purpose**: Provides REST endpoints for interacting with orders.

    - `OrderRestController`: Constructor for the OrderRestController class. It initializes the orderService and productApi. It calls the ProductManagementService.
    - `createOrder`: This function validates the request, converts the request to an OrderEntity, creates the order, and returns a CreateOrderResponse with the order number.
    - `getOrder`: This function fetches an order by its order number, converts it to an OrderDto, and returns it. If the order is not found, it throws an OrderNotFoundException.
    - `getOrders`: This function fetches all orders, converts them to OrderViews, and returns them.

---

