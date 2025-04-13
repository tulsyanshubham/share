# Microservice Migration Summary

# Microservice Report: ApplicationManagementService

## Overview
The ApplicationManagementService is a microservice that manages the application lifecycle. This microservice is responsible for starting the application and managing its dependencies such as PostgreSQL, RabbitMQ, and Zipkin containers.

## File List

### 1. BookStoreApplication.java

**File Path:** `application_management/domain/BookStoreApplication.java`

**Purpose:** This file contains the main function that starts the Spring Application.

**Functions:**

- `main`: The main function which starts the Spring Application.

### 2. TestBookStoreApplication.java

**File Path:** `applicationmanagement/test/TestBookStoreApplication.java`

**Purpose:** This file contains the main method that runs the application. It uses SpringApplication from Spring Boot to run the BookStoreApplication's main method with TestcontainersConfiguration.

**Functions:**

- `main`: The main method that runs the application. It uses SpringApplication from Spring Boot to run the BookStoreApplication's main method with TestcontainersConfiguration.

### 3. TestcontainersConfiguration.java

**File Path:** `application_management/config/TestcontainersConfiguration.java`

**Purpose:** This file manages the configuration of the test containers for the application.

**Functions:**

- `postgresContainer`: This function returns a PostgreSQL container.
- `rabbitmq`: This function returns a RabbitMQ container.
- `zipkinContainer`: This function returns a Zipkin container.

## Migration to Microservices Architecture

To migrate from a monolithic architecture to a microservices architecture, follow these steps:

1. **Identify Business Capabilities:** Start by identifying the business capabilities of your application. This will help you to define the boundaries of your microservices.

2. **Decompose the Monolith:** Break down the monolith into smaller, manageable microservices. Each microservice should have a single responsibility and should be independently deployable.

3. **Define Communication Protocols:** Define how the microservices will communicate with each other. This could be through HTTP/REST, gRPC, or event-driven communication.

4. **Implement Service Discovery:** Implement a service discovery mechanism to allow microservices to discover and communicate with each other.

5. **Implement API Gateway:** Implement an API Gateway to handle client requests and route them to the appropriate microservice.

6. **Implement Distributed Tracing:** Implement distributed tracing to help debug and monitor your microservices.

7. **Implement CI/CD:** Implement Continuous Integration and Continuous Deployment (CI/CD) to automate the deployment of your microservices.

8. **Test:** Finally, thoroughly test your microservices to ensure they work correctly.

## Dependency Hierarchy

```
ApplicationManagementService
|
|-- BookStoreApplication.java
|
|-- TestBookStoreApplication.java
|
|-- TestcontainersConfiguration.java
    |-- postgresContainer
    |-- rabbitmq
    |-- zipkinContainer
```

Note: None of the functions in these files call other microservices.

---

# Microservice Migration Report

## Microservice Name: CommonUtilityService

### Overview
The CommonUtilityService is a microservice that provides utility functions for other services in the system. It includes two main files: PagedResult.java and RabbitMQConfig.java.

### File Structure

#### 1. PagedResult.java
- **File Path**: common/models/PagedResult.java
- **Purpose**: This file contains the PagedResult class, which is used to handle paginated results in the system.

##### Functions
- **PagedResult**: A constructor that takes a Page object and initializes the PagedResult object with its properties.
- **of**: A static method that takes a PagedResult object and a Function object, applies the function to the data of the PagedResult object, and returns a new PagedResult object with the transformed data.

#### 2. RabbitMQConfig.java
- **File Path**: commonutility/config/RabbitMQConfig.java
- **Purpose**: This file contains the RabbitMQConfig class, which is used to configure RabbitMQ for message queuing.

##### Functions
- **exchange**: This function creates a new TopicExchange with the name 'BookStoreExchange'.
- **newOrdersQueue**: This function creates a new Queue with the name 'new-orders'.
- **newOrdersQueueBinding**: This function binds the newOrdersQueue to the exchange with the routing key 'orders.new'.
- **rabbitTemplate**: This function creates a new RabbitTemplate with the provided ConnectionFactory and sets the message converter to a Jackson2JsonMessageConverter.
- **producerJackson2MessageConverter**: This function creates a new Jackson2JsonMessageConverter with the provided ObjectMapper.

### Migration from Monolith to Microservices
The migration process from a monolithic architecture to a microservices architecture for the CommonUtilityService involves the following steps:

1. **Identify the Boundaries**: Identify the functionality provided by the CommonUtilityService in the monolithic application.
2. **Create a Separate Service**: Create a new, separate service for the CommonUtilityService.
3. **Move the Code**: Move the PagedResult.java and RabbitMQConfig.java files to the new service.
4. **Update the Dependencies**: Update any dependencies in the new service to ensure they are correctly pointing to the new location of the files.
5. **Test the Service**: Thoroughly test the new service to ensure it is working correctly.
6. **Update Other Services**: Update any other services in the system that depend on the CommonUtilityService to use the new service.

### Dependency Hierarchy
```
CommonUtilityService
├── PagedResult.java
│   ├── PagedResult()
│   └── of()
└── RabbitMQConfig.java
    ├── exchange()
    ├── newOrdersQueue()
    ├── newOrdersQueueBinding()
    ├── rabbitTemplate()
    └── producerJackson2MessageConverter()
```

**Note**: None of the functions in the CommonUtilityService call other microservices.

---

# Inventory Management Service

## Overview
The Inventory Management Service is a microservice that is responsible for managing the inventory of a business. It provides functionalities such as getting and setting the inventory details, managing the stock levels, and handling order events.

## Migration from Monolith to Microservices
To migrate the Inventory Management Service from a monolithic architecture to a microservices architecture, follow these steps:

1. **Identify the Service Boundaries:** The first step is to identify the service boundaries. In this case, the service boundary is the inventory management functionality.

2. **Decouple the Service:** Decouple the Inventory Management Service from the monolithic application. This involves separating the code, the database, and any other dependencies.

3. **Create a Separate Repository:** Create a separate repository for the Inventory Management Service. This will allow the service to be developed, deployed, and scaled independently.

4. **Implement Communication Mechanisms:** Implement mechanisms for the Inventory Management Service to communicate with other services. This could be through REST APIs, message queues, or any other communication protocol.

5. **Test:** Thoroughly test the Inventory Management Service to ensure that it works correctly in isolation and when communicating with other services.

6. **Deploy:** Deploy the Inventory Management Service independently from the rest of the application.

7. **Monitor:** Monitor the service to ensure that it is performing as expected and to quickly identify and fix any issues.

## Files and Functions

### InventoryEntity.java
**File Path:** inventory/domain/InventoryEntity.java

This file defines the InventoryEntity class, which represents an inventory item in the system. It contains the following functions:

- `getId`: This function returns the id of the inventory entity.
- `setId`: This function sets the id of the inventory entity.
- `getProductCode`: This function returns the product code of the inventory entity.
- `setProductCode`: This function sets the product code of the inventory entity.
- `getQuantity`: This function returns the quantity of the inventory entity.
- `setQuantity`: This function sets the quantity of the inventory entity.

### InventoryRepository.java
**File Path:** inventory/domain/InventoryRepository.java

This file defines the InventoryRepository class, which is used to interact with the database. It contains the following function:

- `findByProductCode`: A function that finds an InventoryEntity by its product code. It returns an Optional that contains the InventoryEntity if it exists, or is empty if it does not.

### InventoryService.java
**File Path:** inventory/service/InventoryService.java

This file defines the InventoryService class, which contains business logic related to inventory management. It contains the following functions:

- `InventoryService`: Constructor for the InventoryService class. It initializes the inventoryRepository object.
- `decreaseStockLevel`: Decreases the stock level for a product by a specified quantity. If the product code is invalid, a warning is logged.
- `getStockLevel`: Returns the current stock level for a product. If the product code is invalid, it returns 0.

### OrderEventInventoryHandler.java
**File Path:** inventory/domain/OrderEventInventoryHandler.java

This file defines the OrderEventInventoryHandler class, which handles events related to orders. It contains the following functions:

- `OrderEventInventoryHandler`: Constructor for the OrderEventInventoryHandler class. It initializes the InventoryService instance.
- `handle`: This function handles the event when an order is created. It logs the event and decreases the stock level of the product. This function calls the OrderManagementService microservice.

---

# Microservice Migration Report

## Microservice Name: ProductManagementService

This microservice is responsible for managing all product-related operations. It includes functionalities such as fetching product details, handling product exceptions, and managing product data.

### Migration from Monolith to Microservices

The migration process from a monolithic architecture to a microservice architecture involves several steps. Here's a step-by-step guide:

1. **Identify the Boundaries**: The first step is to identify the boundaries of the microservice. In this case, the ProductManagementService is responsible for all operations related to product management.

2. **Decouple the Database**: Separate the database of the ProductManagementService from the monolithic database.

3. **Create the Microservice**: Create the ProductManagementService with its own codebase, database, and infrastructure.

4. **Implement the Business Logic**: Implement the business logic in the microservice. This includes all the functions present in the ProductManagementService.

5. **Test the Microservice**: Thoroughly test the microservice to ensure it works as expected.

6. **Deploy the Microservice**: Deploy the microservice and ensure it can communicate with other microservices.

7. **Monitor the Microservice**: Monitor the microservice to ensure it operates as expected.

### List of Files

#### File: ProductDto.java
- **Path**: product/domain/ProductDto.java
- **Purpose**: This file is used to transfer data of Product.
- **Functions**:
  - `getDisplayName`: This function returns the product name if its length is less than or equal to 20. If the product name is longer than 20 characters, it returns the first 20 characters followed by '...'.

#### File: ProductNotFoundException.java
- **Path**: product/domain/ProductNotFoundException.java
- **Purpose**: This file defines an exception that is thrown when a product is not found.
- **Functions**:
  - `ProductNotFoundException`: This is a constructor that takes a string message as an argument and passes it to the superclass constructor.
  - `forCode`: This is a static method that takes a string code as an argument, creates a new ProductNotFoundException with a custom message, and returns it.

#### File: ProductWebController.java
- **Path**: productmanagement/web/ProductWebController.java
- **Purpose**: This file is used to handle web requests related to products.

#### File: ProductEntity.java
- **Path**: product/domain/ProductEntity.java
- **Purpose**: This file represents the product entity in the database.
- **Functions**:
  - `getId`: This function returns the id of the product.
  - `setId`: This function sets the id of the product.
  - `getCode`: This function returns the code of the product.
  - `setCode`: This function sets the code of the product.
  - `getName`: This function returns the name of the product.
  - `setName`: This function sets the name of the product.
  - `getDescription`: This function returns the description of the product.
  - `setDescription`: This function sets the description of the product.
  - `getImageUrl`: This function returns the image URL of the product.
  - `setImageUrl`: This function sets the image URL of the product.
  - `getPrice`: This function returns the price of the product.
  - `setPrice`: This function sets the price of the product.

#### File: ProductMapper.java
- **Path**: product/domain/mappers/ProductMapper.java
- **Purpose**: This file is used to map ProductEntity to ProductDto.
- **Functions**:
  - `mapToDto`: This function takes a ProductEntity object as input and returns a new ProductDto object, using the attributes of the input object to initialize the new object.

#### File: ProductRepository.java
- **Path**: product/domain/ProductRepository.java
- **Purpose**: This file is used to interact with the database for product-related operations.
- **Functions**:
  - `findByCode`: A function that returns an Optional of ProductEntity by searching for a given code.

#### File: CatalogExceptionHandler.java
- **Path**: product_management/web/CatalogExceptionHandler.java
- **Purpose**: This file is used to handle exceptions related to the product catalog.
- **Functions**:
  - `handle`: This function handles the ProductNotFoundException. It creates a ProblemDetail object with the status NOT_FOUND and the exception message. It then sets the title of the problem detail to 'Product Not Found' and adds a timestamp property with the current instant. Finally, it returns the problem detail.

#### File: ProductService.java
- **Path**: product/domain/ProductService.java
- **Purpose**: This file is used to handle business logic related to products.
- **Functions**:
  - `ProductService`: Constructor for ProductService. It initializes the ProductRepository instance.
  - `getProducts`: This function retrieves a page of products sorted by name in ascending order. The page size is defined by the constant PRODUCT_PAGE_SIZE.
  - `getByCode`: This function retrieves a product by its code.

#### File: ProductApi.java
- **Path**: product_management_service/src/main/java/com/sivalabs/bookstore/catalog/ProductApi.java
- **Purpose**: This file is used to expose product-related APIs.
- **Functions**:
  - `ProductApi`: Constructor for the ProductApi class. It initializes the ProductService and ProductMapper objects.
  - `getByCode`: This function retrieves a product by its code. It uses the ProductService to get the product and the ProductMapper to convert it to a DTO.

#### File: ProductRestController.java
- **Path**: product_management/web/ProductRestController.java
- **Purpose**: This file is used to handle REST requests related to products.
- **Functions**:
  - `ProductRestController`: Constructor for the ProductRestController class. It initializes productService and productMapper.
  - `getProducts`: Fetches a page of products. It uses the productService to get the products and the productMapper to map the products to DTOs.
  - `getProductByCode`: Fetches a product by its code. It uses the productService to get the product and the productMapper to map the product to a DTO. If the product is not found, it throws a ProductNotFoundException.

### Microservice Interaction

Based on the provided JSON data, there are no functions that call other microservices.

---

# Microservice Migration Report

## Microservice Name: OrderManagementService

The OrderManagementService is a microservice responsible for managing orders in the system. It contains various files and functions that handle different aspects of order management, such as creating orders, updating orders, handling exceptions, and interacting with other microservices.

### Migration from Monolith to Microservices

The migration from a monolithic architecture to a microservices architecture involves breaking down the monolith into smaller, independent services. In the case of the OrderManagementService, the process would involve the following steps:

1. **Identify the Boundaries:** Identify the functionalities that will be part of the OrderManagementService. These would typically include order creation, order retrieval, order update, and order deletion.

2. **Create the Microservice:** Create a new microservice project for the OrderManagementService. This would involve setting up a new code repository, setting up the development environment, and setting up the deployment pipeline.

3. **Migrate the Code:** Migrate the relevant code from the monolith to the new microservice. This would involve copying the relevant files and functions, and then refactoring the code to ensure that it works in the new microservice.

4. **Test the Microservice:** Test the new microservice to ensure that it works correctly. This would involve unit testing, integration testing, and end-to-end testing.

5. **Deploy the Microservice:** Deploy the new microservice to a staging environment and perform further testing. Once the testing is successful, deploy the microservice to the production environment.

6. **Decommission the Monolith Code:** Once the new microservice is working correctly, the corresponding code in the monolith can be decommissioned.

### List of Files

Below is a list of files in the OrderManagementService, along with their file paths, purposes, and the functions they contain.

#### File: Customer.java
- **File Path:** orders/domain/models/Customer.java
- **Purpose:** This file represents the Customer model in the domain. It does not contain any functions.

#### File: CreateOrderResponse.java
- **File Path:** orders/domain/CreateOrderResponse.java
- **Purpose:** This file represents the response sent after an order is created. It does not contain any functions.

#### File: OrderForm.java
- **File Path:** orders/web/OrderForm.java
- **Purpose:** This file represents the form used for creating orders. It does not contain any functions.

#### File: InvalidOrderException.java
- **File Path:** orders/exceptions/InvalidOrderException.java
- **Purpose:** This file represents an exception that is thrown when an invalid order is created.
- **Functions:**
  - **InvalidOrderException:** Constructor function that takes a string message as an argument and passes it to the superclass constructor.

#### File: OrderItem.java
- **File Path:** orders/domain/models/OrderItem.java
- **Purpose:** This file represents the OrderItem model in the domain. It does not contain any functions.

#### File: OrderStatus.java
- **File Path:** orders/domain/models/OrderStatus.java
- **Purpose:** This file represents the OrderStatus model in the domain. It does not contain any functions.

#### File: OrderWebController.java
- **File Path:** orders/web/OrderWebController.java
- **Purpose:** This file represents the web controller for orders. It does not contain any functions.

#### File: CartController.java
- **File Path:** orders/web/CartController.java
- **Purpose:** This file represents the web controller for the shopping cart.
- **Functions:**
  - **CartController:** Constructor for CartController class. It initializes the ProductApi object. Calls the ProductManagementService.
  - **addProductToCart:** This function adds a product to the cart. It takes a product code and a session as parameters. Calls the ProductManagementService.
  - **showCart:** This function displays the cart. It takes a model and a session as parameters.
  - **updateCart:** This function updates the cart. It takes a product code, quantity, and a session as parameters.

#### File: OrderNotFoundException.java
- **File Path:** orders/exceptions/OrderNotFoundException.java
- **Purpose:** This file represents an exception that is thrown when an order is not found.
- **Functions:**
  - **OrderNotFoundException:** A constructor that takes a message string as an argument and passes it to the superclass constructor.
  - **forOrderNumber:** A static method that takes an order number string as an argument and returns a new instance of OrderNotFoundException with a custom message.

#### File: Cart.java
- **File Path:** orders/domain/Cart.java
- **Purpose:** This file represents the Cart model in the domain.
- **Functions:**
  - **getItem:** Returns the LineItem object stored in the 'item' field.
  - **setItem:** Sets the LineItem object to the 'item' field.
  - **getTotalAmount:** Returns the total amount of the LineItem by multiplying its price and quantity. If the item is null, it returns zero.
  - **removeItem:** Sets the 'item' field to null.
  - **updateItemQuantity:** Updates the quantity of the LineItem. If the quantity is less than or equal to zero, it removes the item.
  - **LineItem:** An inner class representing a line item with fields for code, name, price, and quantity. It includes getters and setters for these fields.

#### File: OrderCreatedEvent.java
- **File Path:** orders/domain/models/OrderCreatedEvent.java
- **Purpose:** This file represents the event that is published when an order is created. It does not contain any functions.

#### File: CreateOrderRequest.java
- **File Path:** orders/domain/CreateOrderRequest.java
- **Purpose:** This file represents the request sent to create an order. It does not contain any functions.

#### File: CartUtil.java
- **File Path:** orders/web/CartUtil.java
- **Purpose:** This file contains utility functions related to the shopping cart.
- **Functions:**
  - **getCart:** This function retrieves the cart object from the session. If the cart object is null, it creates a new cart object.
  - **CartUtil:** This is a private constructor to prevent instantiation of the utility class.

#### File: OrderView.java
- **File Path:** orders/domain/OrderView.java
- **Purpose:** This file represents the view model for orders. It does not contain any functions.

#### File: OrderDto.java
- **File Path:** orders/domain/OrderDto.java
- **Purpose:** This file represents the data transfer object for orders.
- **Functions:**
  - **getTotalAmount:** This function returns the total amount of the order by multiplying the price of the item by its quantity. It uses the BigDecimal class for the multiplication and to hold the return value.

#### File: OrdersExceptionHandler.java
- **File Path:** order_management/web/OrdersExceptionHandler.java
- **Purpose:** This file handles exceptions related to orders.
- **Functions:**
  - **handle:** This function handles the OrderNotFoundException. It creates a ProblemDetail object with the status NOT_FOUND and the exception message, sets the title to 'Order Not Found', sets the timestamp to the current time, and returns the ProblemDetail object.
  - **handle:** This function handles the InvalidOrderException. It creates a ProblemDetail object with the status BAD_REQUEST and the exception message, sets the title to 'Invalid Order Creation Request', sets the timestamp to the current time, and returns the ProblemDetail object.

#### File: OrderEventNotificationHandler.java
- **File Path:** ordermanagement/domain/OrderEventNotificationHandler.java
- **Purpose:** This file handles the event when an order is created.
- **Functions:**
  - **handle:** This function handles the event when an order is created. It logs the information about the event.

#### File: OrderRepository.java
- **File Path:** ordermanagement/domain/OrderRepository.java
- **Purpose:** This file represents the repository for orders.
- **Functions:**
  - **findAllBy:** This function returns a list of all OrderEntity objects, sorted according to the provided Sort object. It uses a custom query to fetch the data, which includes fetching associated order items for each order.
  - **findByOrderNumber:** This function returns an Optional containing the OrderEntity object that matches the provided order number. If no such order exists, the returned Optional is empty. It uses a custom query to fetch the data, which includes fetching associated order items for the order.

#### File: OrderService.java
- **File Path:** orders/domain/OrderService.java
- **Purpose:** This file represents the service for orders.
- **Functions:**
  - **OrderService:** Constructor for the OrderService class. It initializes the OrderRepository and ApplicationEventPublisher instances.
  - **createOrder:** This function creates an order, logs the creation, publishes an event, and returns the saved order.
  - **findOrder:** This function finds and returns an order by its order number.
  - **findOrders:** This function finds and returns all orders sorted by id in descending order.

#### File: OrderMapper.java
- **File Path:** orders/mappers/OrderMapper.java
- **Purpose:** This file contains functions to map between different order models.
- **Functions:**
  - **convertToEntity:** Converts a CreateOrderRequest object into an OrderEntity object. It sets the order number, status, customer, delivery address, and order item from the request.
  - **convertToDto:** Converts an OrderEntity object into an OrderDto object. It sets the order number, order item, customer, delivery address, status, and creation time from the order entity.
  - **convertToOrderViews:** Converts a list of OrderEntity objects into a list of OrderView objects. It sets the order number, status, and customer for each order view from the corresponding order entity.

#### File: OrdersApi.java
- **File Path:** ordermanagement/api/OrdersApi.java
- **Purpose:** This file represents the API for orders.
- **Functions:**
  - **OrdersApi:** Constructor for OrdersApi class. It initializes the OrderService.
  - **createOrder:** This function creates a new order. It converts the request to an OrderEntity, creates the order using the OrderService, and returns a CreateOrderResponse with the order number.
  - **findOrder:** This function finds an order by its order number. It uses the OrderService to find the order, converts the OrderEntity to an OrderDto, and returns it wrapped in an Optional.
  - **findOrders:** This function finds all orders. It uses the OrderService to find the orders, converts the list of OrderEntity to a list of OrderView, and returns it.

#### File: OrderWebSupport.java
- **File Path:** orders/web/OrderWebSupport.java
- **Purpose:** This file provides support functions for the web layer of the order management.
- **Functions:**
  - **OrderWebSupport:** Constructor for the OrderWebSupport class. It initializes the ProductApi instance. Calls the ProductManagementService.
  - **validate:** This function validates the CreateOrderRequest. It checks if the product code exists and if the price matches the product's price. If not, it throws an InvalidOrderException. Calls the ProductManagementService.

#### File: OrderRestController.java
- **File Path:** orders/web/OrderRestController.java
- **Purpose:** This file represents the REST controller for orders.
- **Functions:**
  - **OrderRestController:** Constructor for the OrderRestController class. It initializes the OrderService and ProductApi instances. Calls the ProductManagementService.
  - **createOrder:** This function validates the request, converts it to an OrderEntity, creates an order using the OrderService, and returns a CreateOrderResponse with the order number.
  - **getOrder:** This function fetches an order by its order number. If the order is not found, it throws an OrderNotFoundException.
  - **getOrders:** This function fetches all orders and converts them to OrderView objects.

#### File: OrderEntity.java
- **File Path:** orders/domain/OrderEntity.java
- **Purpose:** This file represents the entity for orders.
- **Functions:**
  - **OrderEntity:** Default constructor for OrderEntity class.
  - **OrderEntity:** Overloaded constructor for OrderEntity class.
  - **getId:** Getter method for id.
  - **setId:** Setter method for id.
  - **getOrderNumber:** Getter method for orderNumber.
  - **setOrderNumber:** Setter method for orderNumber.
  - **getCustomer:** Getter method for customer.
  - **setCustomer:** Setter method for customer.
  - **getDeliveryAddress:** Getter method for deliveryAddress.
  - **setDeliveryAddress:** Setter method for deliveryAddress.
  - **getOrderItem:** Getter method for orderItem.
  - **setOrderItem:** Setter method for orderItem.
  - **getStatus:** Getter method for status.
  - **setStatus:** Setter method for status.
  - **getCreatedAt:** Getter method for createdAt.
  - **setCreatedAt:** Setter method for createdAt.
  - **getUpdatedAt:** Getter method for updatedAt.
  - **setUpdatedAt:** Setter method for updatedAt.

### Dependency Hierarchy

The OrderManagementService has dependencies on other microservices. Here is a simple text-based dependency hierarchy:

- OrderManagementService
  - ProductManagementService (called by CartController, OrderWebSupport, and OrderRestController)

### Conclusion

The OrderManagementService is a complex microservice with many files and functions. The migration from a monolithic architecture to a microservices architecture would involve careful planning and execution to ensure that all functionalities are correctly migrated and that the new microservice works correctly.

---

