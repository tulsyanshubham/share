# Microservice Migration Summary

# BaseEntityAuditService Microservice Migration Report

## Overview

The BaseEntityAuditService is a microservice that handles the auditing of base entities in the system. It is responsible for setting the creation and change dates for these entities. This report provides a detailed analysis of the microservice's structure and a step-by-step guide on how to migrate it from a monolithic architecture to a microservices architecture.

## List of Files

### BaseEntityAudit.java

**File Path:** `base_entity_audit/domain/BaseEntityAudit.java`

**File Purpose:** This Java file contains the core logic for the BaseEntityAuditService. It includes functions for setting the creation and change dates for base entities.

#### Functions

1. `setCreationDate`

   - **Description:** This function sets the `createdAt` date before an entity is inserted into the system. It does not call any other microservices.

2. `setChangeDate`

   - **Description:** This function sets the `updatedAt` date before an entity is updated in the system. It does not call any other microservices.

## Migration Process from Monolith to Microservices Architecture

The following steps outline the process of migrating the BaseEntityAuditService from a monolithic architecture to a microservices architecture:

1. **Identify the Service Boundaries:** Identify the functionality provided by the BaseEntityAuditService within the monolithic application.

2. **Decouple the Service:** Decouple the BaseEntityAuditService from the monolithic application. This involves separating the code, data storage, and any other dependencies.

3. **Create a Standalone Service:** Create a standalone microservice for BaseEntityAuditService. This includes setting up its own code repository, database, and any other necessary infrastructure.

4. **Define the API:** Define the API for the BaseEntityAuditService. This includes the endpoints, request/response formats, and error handling.

5. **Implement the Service:** Implement the BaseEntityAuditService using the decoupled code. This includes implementing the `setCreationDate` and `setChangeDate` functions.

6. **Test the Service:** Thoroughly test the BaseEntityAuditService to ensure it works correctly and efficiently.

7. **Deploy the Service:** Deploy the BaseEntityAuditService to a production environment.

8. **Monitor the Service:** Continuously monitor the BaseEntityAuditService to ensure it is performing as expected and to quickly identify and resolve any issues.

## Dependency Hierarchy

```
BaseEntityAuditService
├── BaseEntityAudit.java
│   ├── setCreationDate
│   └── setChangeDate
```

This hierarchy shows that the BaseEntityAuditService is composed of the BaseEntityAudit.java file, which contains two functions: `setCreationDate` and `setChangeDate`.

---

# ValidationService Microservice

## Overview
The ValidationService is a microservice that handles the validation of parameters within the system. It consists of several files, each containing specific functions that contribute to the overall functionality of the service.

## Migration from Monolith to Microservices
The process of migrating from a monolithic architecture to a microservices architecture involves breaking down the monolithic application into smaller, independent services. Each service should have a specific functionality and should be able to operate independently.

For the ValidationService, the migration process would involve the following steps:

1. **Identify the functionality of the ValidationService in the monolithic application:** This involves understanding what the service does and how it interacts with other services.

2. **Design the ValidationService as an independent service:** This involves defining the service's API and data model.

3. **Implement the ValidationService:** This involves writing the code for the service and ensuring that it works as expected.

4. **Test the ValidationService:** This involves testing the service in isolation and in conjunction with other services.

5. **Deploy the ValidationService:** This involves deploying the service in a production environment.

6. **Monitor the ValidationService:** This involves monitoring the service to ensure that it is working as expected and to identify any issues that may arise.

## Files and Functions
### File: ValidParamNumberConstraintValidator.java
**File Path:** validation/constraint/ValidParamNumberConstraintValidator.java

This file contains two functions, `initialize` and `isValid`, which are used to initialize and validate a given Long value according to the constraint.

- **Function: initialize**
  - Description: A function that initializes the ValidParamNumber constraint. It doesn't have any internal dependencies.
  - Calls to other microservices: None

- **Function: isValid**
  - Description: A function that checks if a given Long value is valid according to the constraint. It doesn't have any internal dependencies.
  - Calls to other microservices: None

### File: ValidParamNumber.java
**File Path:** validation/constraint/ValidParamNumber.java

This file contains three functions, `message`, `groups`, and `payload`, which are used to return a default message, an array of Class objects, and an array of Payload objects, respectively.

- **Function: message**
  - Description: A function that returns a default message 'Must greater than 0 and lower than 2^63-1'.
  - Calls to other microservices: None

- **Function: groups**
  - Description: A function that returns an array of Class objects, default is an empty array.
  - Calls to other microservices: None

- **Function: payload**
  - Description: A function that returns an array of Payload objects, default is an empty array.
  - Calls to other microservices: None

### File: UserController.java
**File Path:** validation/api/UserController.java

This file contains a function, `validatePathVariable`, which is used to validate the path variable id.

- **Function: validatePathVariable**
  - Description: Validates the path variable id.
  - Calls to other microservices: None

## Dependency Hierarchy
The ValidationService does not have any dependencies on other microservices. All functions are self-contained and do not call other microservices.

---

# Microservice Migration Report

## Microservice Name: DocumentationService

### Overview
The DocumentationService is responsible for handling the documentation of the application. This includes serving the Swagger user interface HTML page and configuring the Swagger API Documentation framework.

### File List and Details

#### File: ApiDocsController.java
- **File Path:** documentation/web/ApiDocsController.java
- **Purpose:** This file serves as a controller for handling requests related to API documentation. It is responsible for serving the Swagger user interface HTML page configured to the mapped context path.
- **Functions:**
  - `getSwaggerApiDocsPage`: Request handler to serve the Swagger user interface HTML page configured to the mapped context path.

#### File: SwaggerConfig.java
- **File Path:** documentation/config/SwaggerConfig.java
- **Purpose:** This file is responsible for configuring the Swagger API Documentation framework. It creates the necessary classes (Contact, ApiInfo, Docket) to be used by the framework.
- **Functions:**
  - `contact`: Create a Contact class to be used by Springfox's Swagger API Documentation framework.
  - `apiInfo`: Create an ApiInfo class to be used by Springfox's Swagger API Documentation framework.
  - `docket`: Create a Docket class to be used by Springfox's Swagger API Documentation framework.

### Migration Steps from Monolith to Microservices Architecture

1. **Identify the Service:** Identify the DocumentationService as a separate service in the monolithic architecture.
2. **Decouple the Service:** Decouple the DocumentationService from the monolithic architecture. This involves separating the codebase and the database.
3. **Create a New Microservice:** Create a new microservice for the DocumentationService. This includes setting up a new repository, setting up CI/CD, and deploying the service to a separate server.
4. **Migrate the Code:** Migrate the code for the DocumentationService to the new microservice. This includes the ApiDocsController.java and SwaggerConfig.java files.
5. **Test the Service:** Test the DocumentationService in isolation to ensure it works correctly.
6. **Integrate the Service:** Integrate the DocumentationService with the rest of the application. This involves setting up communication between the microservice and the rest of the application.

### Dependency Hierarchy

```
DocumentationService
├── ApiDocsController.java
│   └── getSwaggerApiDocsPage
└── SwaggerConfig.java
    ├── contact
    ├── apiInfo
    └── docket
```

Note: None of the functions in the DocumentationService call other microservices.

---

# CoreService Microservice Migration Report

## Overview

The CoreService microservice is a crucial component of the application, providing a set of base functionalities that are used across the system. This microservice is composed of several Java files, each serving a specific purpose and containing a set of functions.

## Migration from Monolith to Microservices

The migration process from a monolithic architecture to a microservices architecture involves several steps:

1. **Identify the CoreService functionalities**: Start by understanding the functionalities provided by the CoreService in the monolithic application. This will guide the design and development of the microservice.

2. **Design the CoreService microservice**: Design the microservice, keeping in mind principles such as single responsibility, loose coupling, and high cohesion.

3. **Develop the CoreService microservice**: Implement the microservice based on the design. This involves creating the necessary files and functions.

4. **Test the CoreService microservice**: Conduct thorough testing to ensure that the microservice works as expected.

5. **Deploy the CoreService microservice**: Once testing is complete, deploy the microservice.

6. **Update the monolithic application**: Update the monolithic application to use the CoreService microservice instead of the original code.

7. **Repeat for other functionalities**: Repeat the process for other functionalities until the entire monolithic application has been migrated to a microservices architecture.

## File Structure and Purpose

Below is a list of files in the CoreService microservice, their paths, and their purposes:

- `BaseRepository.java` (`core/BaseRepository.java`): This file does not contain any functions and serves as a base repository.

- `Application.java` (`core/main/Application.java`): This file contains the main method which is the entry point of the application.

- `BaseService.java` (`core/service/BaseService.java`): This file contains several functions for basic CRUD operations.

- `BaseEntity.java` (`core/domain/BaseEntity.java`): This file contains functions for getting and setting entity properties.

- `JacksonConstant.java` (`core/helper/constant/JacksonConstant.java`): This file contains a function that prevents the user from initializing an instance.

- `MapperConfig.java` (`core/config/MapperConfig.java`): This file contains a function that creates and returns a new instance of ModelMapper.

- `MySQLConstant.java` (`core/helper/constant/MySQLConstant.java`): This file does not contain any functions and serves to hold MySQL constants.

- `ListParameterizedType.java` (`core/helper/util/ListParameterizedType.java`): This file contains functions related to parameterized types.

- `ModelMapperUtils.java` (`core/util/ModelMapperUtils.java`): This file contains utility functions for mapping between models.

- `SwaggerConstant.java` (`core/helper/constant/SwaggerConstant.java`): This file contains a function that prevents the user from initializing an instance.

- `HotelController.java` (`core/api/HotelController.java`): This file contains functions related to the hotel controller, including one function that calls the DocumentationService microservice.

## Function Calls to Other Microservices

The `sampleSwagger` function in the `HotelController.java` file calls the `DocumentationService` microservice.

## Dependency Hierarchy

The dependency hierarchy of the CoreService microservice is as follows:

```
CoreService
├── BaseRepository.java
├── Application.java
├── BaseService.java
├── BaseEntity.java
├── JacksonConstant.java
├── MapperConfig.java
├── MySQLConstant.java
├── ListParameterizedType.java
├── ModelMapperUtils.java
├── SwaggerConstant.java
└── HotelController.java
    └── DocumentationService (external microservice)
```

This hierarchy shows that the `HotelController.java` file in the CoreService microservice depends on the external `DocumentationService` microservice.

---

# InfrastructureService Microservice

## Overview
The InfrastructureService is a microservice that provides various functionalities related to the application's infrastructure. It includes functionalities such as logging, handling Cross-Origin requests, and managing success details of the application.

## Files and Functions

### 1. LogInterceptor.java
**File Path:** infrastructure/web/config/LogInterceptor.java

This file contains functions that are executed at various stages of a request lifecycle. The functions include:

- `afterCompletion`: This function is executed after the request has been completed. It prints 'Request Completed!' to the console.
- `postHandle`: This function is executed after the handler execution but before the view rendering. It prints 'Method executed' to the console.
- `preHandle`: This function is executed before the actual handler is executed. It prints 'Before process request' to the console and returns true.

### 2. SimpleCorsFilter.java
**File Path:** infrastructure/web/config/SimpleCorsFilter.java

This file contains a function that intercepts all inbound HTTP requests and handles Cross-Origin requests. The function is:

- `doFilter`: This function intercepts all inbound HTTP requests and sets several Headers on the HTTP response which inform a browser that the web services handle Cross-Origin requests.

### 3. SuccessDetail.java
**File Path:** infrastructure/response/SuccessDetail.java

This file contains functions that manage the success details of the application. The functions include:

- `SuccessDetail`: Construct an ExceptionDetail.
- `getTimestamp`: Returns the timestamp attribute value.
- `setTimestamp`: Sets the timestamp attribute value.
- `getMethod`: Returns the method attribute value.
- `setMethod`: Sets the method attribute value.
- `getPath`: Returns the path attribute value.
- `setPath`: Sets the path attribute value.
- `getStatus`: Returns the status attribute value.
- `setStatus`: Sets the status attribute value.
- `getStatusText`: Returns the statusText attribute value.
- `setStatusText`: Sets the statusText attribute value.
- `getData`: Returns the data value.
- `setData`: Sets the data value.

### 4. WebConfig.java
**File Path:** infrastructure/config/WebConfig.java

This file contains a function that adds the logInterceptor to the InterceptorRegistry. The function is:

- `addInterceptors`: This function is an override from the WebMvcConfigurerAdapter class. It adds the logInterceptor to the InterceptorRegistry.

### 5. SuccessDetailBuilder.java
**File Path:** infrastructure/response/SuccessDetailBuilder.java

This file contains functions that build the SuccessDetail object. The functions include:

- `SuccessDetailBuilder`: Constructs a new SuccessDetailBuilder.
- `build`: Invoke this method to obtain the SuccessDetail object after using builder methods to populate it.
- `data`: Populate the SuccessDetail attributes with information. Returns this SuccessDetailBuilder to chain method invocations.
- `httpStatus`: Populate the SuccessDetail attributes with information from a HttpStatus. Returns this SuccessDetailBuilder to chain method invocations.
- `webRequest`: Populate the SuccessDetail attributes with information from a WebRequest. Typically use either a WebRequest or HttpServletRequest, but not both. Returns this SuccessDetailBuilder to chain method invocations.
- `httpServletRequest`: Populate the SuccessDetail attributes with information from a HttpServletRequest. Typically use either a WebRequest or HttpServletRequest, but not both. Returns this SuccessDetailBuilder to chain method invocations.

## Migration from Monolith to Microservices
Migrating from a monolithic architecture to a microservices architecture involves several steps. Here is a step-by-step guide on how to migrate the InfrastructureService microservice:

1. **Identify the Functionalities:** Identify the functionalities provided by the InfrastructureService in the monolithic application. This includes logging, handling Cross-Origin requests, and managing success details.

2. **Design the Microservice:** Design the InfrastructureService microservice to provide these functionalities. This includes defining the APIs and the data model.

3. **Implement the Microservice:** Implement the InfrastructureService microservice. This includes writing the code for the APIs and the data model.

4. **Test the Microservice:** Test the InfrastructureService microservice to ensure that it provides the expected functionalities.

5. **Deploy the Microservice:** Deploy the InfrastructureService microservice on a separate server or container.

6. **Update the Monolithic Application:** Update the monolithic application to use the APIs provided by the InfrastructureService microservice instead of the functionalities provided by the monolithic application.

7. **Test the Monolithic Application:** Test the monolithic application to ensure that it works correctly with the InfrastructureService microservice.

8. **Repeat the Process:** Repeat the process for other functionalities in the monolithic application.

Here is a simple text-based flowchart of the process:

```
Monolithic Application
  |
  v
Identify Functionalities -> Design Microservice -> Implement Microservice -> Test Microservice -> Deploy Microservice
  |
  v
Update Monolithic Application -> Test Monolithic Application
  |
  v
Repeat for Other Functionalities
```

Please note that no function in the InfrastructureService microservice calls another microservice.

---

# Microservice Migration Report

## Microservice Name: BaseDtoService

### Overview
The BaseDtoService is a microservice that is part of a larger application. It is responsible for managing the Data Transfer Objects (DTOs) that are used for data transmission between processes. The main file in this microservice is `BaseDto.java`.

### File Details

#### File: BaseDto.java
- **File Path:** dto/domain/BaseDto.java
- **Purpose:** This file is the base class for all DTOs in the system. It does not contain any specific functions.

### Migrating from Monolith to Microservices

The migration from a monolithic architecture to a microservices architecture involves breaking down a large, complex system into smaller, independent services. Here is a step-by-step guide on how to migrate the BaseDtoService:

1. **Identify the Boundaries:** The first step in migrating to a microservices architecture is to identify the boundaries of the BaseDtoService. This involves understanding the responsibilities of the service and how it interacts with other parts of the system.

2. **Create a Separate Service:** Once the boundaries are identified, create a separate service for the BaseDtoService. This involves creating a new project or repository and moving the `BaseDto.java` file to this new service.

3. **Update Dependencies:** Update any dependencies that the BaseDtoService has on other parts of the system. This could involve updating the import statements in the `BaseDto.java` file.

4. **Test the Service:** After the service has been separated and the dependencies have been updated, test the service to ensure that it is functioning correctly.

5. **Deploy the Service:** Once the service has been tested and verified, it can be deployed. This involves setting up a server or container to host the service and configuring any necessary networking.

6. **Update Other Services:** After the BaseDtoService has been deployed, update any other services that depend on it. This could involve updating the URLs or endpoints that these services use to communicate with the BaseDtoService.

Please note that this microservice does not call any other microservice.

### Functions

The `BaseDto.java` file does not contain any functions.

### Dependencies

The `BaseDto.java` file does not have any dependencies on other files or services.

### Flowchart

Since the `BaseDto.java` file does not contain any functions or dependencies, a flowchart is not applicable in this case.

---

# Microservice Migration Report: UserService

## Overview
The UserService is a microservice that handles all operations related to users. It includes functionalities such as creating, updating, deleting, and retrieving user data. This microservice is composed of several Java files, each with its own specific purpose and functionality.

## Migrating from Monolith to Microservices
The migration process from a monolithic architecture to a microservices architecture for the UserService involves several steps:

1. **Identify the UserService functionality in the monolithic application**: This involves understanding all the operations related to users that are currently being handled by the monolithic application.

2. **Design the UserService microservice**: This includes defining the APIs that the UserService will expose and the data it will handle.

3. **Implement the UserService microservice**: This involves creating the UserService microservice using the identified functionalities and designed APIs.

4. **Test the UserService microservice**: This involves testing the UserService microservice independently to ensure it works as expected.

5. **Integrate the UserService microservice**: This involves integrating the UserService microservice with the rest of the application and ensuring it communicates correctly with other microservices.

6. **Deploy the UserService microservice**: This involves deploying the UserService microservice to the production environment.

7. **Monitor the UserService microservice**: This involves monitoring the UserService microservice to ensure it is working as expected and to identify any issues that may arise.

## Files and Functions
Below is a list of the files in the UserService microservice, their purposes, and the functions they contain.

### UserDto.java
- **File Path**: `user/dto/UserDto.java`
- **Purpose**: This file is used to transfer data about a user between processes or across network connections.

### UserRepositoryCustom.java
- **File Path**: `user/domain/UserRepositoryCustom.java`
- **Purpose**: This file is used to define custom methods for interacting with the user data in the database.

### UserSeeder.java
- **File Path**: `user/seeding/UserSeeder.java`
- **Purpose**: This file is used to populate the database with initial user data.
- **Functions**:
  - `run`: This function creates two User objects, adds them to a list, and saves them in the UserRepository.

### UserController.java
- **File Path**: `user/api/UserController.java`
- **Purpose**: This file is used to handle HTTP requests related to users.
- **Functions**:
  - `findAll`: Returns a paginated list of UserDto objects.
  - `findAll`: Returns a list of all UserDto objects.
  - `findById`: Returns a UserDto object by its id.
  - `create`: Creates a new UserDto object and returns its id. Calls the `ExceptionService` microservice.
  - `update`: Updates a UserDto object by its id. Calls the `ExceptionService` microservice.
  - `deleteById`: Deletes a UserDto object by its id.

### UserService.java
- **File Path**: `user/service/UserService.java`
- **Purpose**: This file defines the interface for the user service.

### UserRepositoryImpl.java
- **File Path**: `user/repository/impl/UserRepositoryImpl.java`
- **Purpose**: This file provides an implementation of the UserRepositoryCustom interface.

### User.java
- **File Path**: `user/domain/User.java`
- **Purpose**: This file defines the User entity.

### Customer.java
- **File Path**: `user/domain/Customer.java`
- **Purpose**: This file defines the Customer entity, which is a type of user.
- **Functions**:
  - `Customer`: This is a default constructor for the Customer class.

### UserValidationImpl.java
- **File Path**: `user/validation/impl/UserValidationImpl.java`
- **Purpose**: This file provides an implementation of the UserValidation interface.
- **Functions**:
  - `isValidateUserId`: This function validates if a user with the given id exists in the UserRepository. If not, it adds an ExceptionDetailMessage to a list and returns it.

### UserServiceImpl.java
- **File Path**: `user/service/impl/UserServiceImpl.java`
- **Purpose**: This file provides an implementation of the UserService interface.
- **Functions**:
  - `findAll`: This function retrieves all users in a pageable format. It uses the UserRepository and ModelMapperUtils.
  - `findAll`: This function retrieves all users. It uses the UserRepository and ModelMapper.
  - `findById`: This function retrieves a user by id. It uses the UserRepository, UserValidation, and ModelMapper.
  - `create`: This function creates a new user. It uses the UserRepository and ModelMapper.
  - `update`: This function updates a user by id. It uses the UserRepository and UserValidation.
  - `deleteById`: This function deletes a user by id. It uses the UserRepository and UserValidation.

---

# Microservice Migration Report

## Microservice Name: ExceptionService

### Overview
The ExceptionService is a microservice that handles exceptions in the system. It contains various files and functions that are responsible for creating, handling, and managing exceptions. The service includes custom exceptions, exception handlers, and utility classes for exception management.

---

### Migration from Monolith to Microservices Architecture

The migration process from a monolithic architecture to a microservices architecture involves several steps:

1. **Identify the Boundaries**: Identify the boundaries of the ExceptionService in the monolithic application. This involves understanding the responsibilities of the service and how it interacts with other services.

2. **Decouple the Service**: Decouple the ExceptionService from the monolithic application. This involves removing dependencies and ensuring that the service can function independently.

3. **Create the Microservice**: Create the ExceptionService as a standalone microservice. This involves setting up the necessary infrastructure, such as databases and servers.

4. **Test the Microservice**: Test the ExceptionService to ensure that it functions correctly. This involves unit testing, integration testing, and end-to-end testing.

5. **Deploy the Microservice**: Deploy the ExceptionService to the production environment. This involves setting up CI/CD pipelines and monitoring systems.

6. **Iterate**: Repeat the process for each service in the monolithic application until the entire application has been migrated to a microservices architecture.

---

### Files and Functions

#### File: CustomNotFoundException.java
- **Path**: exception/domain/CustomNotFoundException.java
- **Purpose**: This file defines a custom exception that is thrown when a requested resource is not found.
- **Functions**:
  - **CustomNotFoundException**: This is a constructor function that takes a string message as an argument and passes it to the superclass constructor.

#### File: DTOInControllerNotValidException.java
- **Path**: exception/DTOInControllerNotValidException.java
- **Purpose**: This file defines a custom exception that is thrown when a DTO in a controller is not valid.
- **Functions**:
  - **DTOInControllerNotValidException**: Constructor for DTOInControllerNotValidException. It initializes the bindingResult field with the provided argument.
  - **getBindingResult**: This function returns the results of the failed validation.

#### File: ExceptionUtils.java
- **Path**: exception/util/ExceptionUtils.java
- **Purpose**: This file contains utility functions for handling exceptions.

#### File: GlobalControllerExceptionHandler.java
- **Path**: exception/GlobalControllerExceptionHandler.java
- **Purpose**: This file defines a global exception handler for controllers.

#### File: DTOInServiceNotValidException.java
- **Path**: exception/domain/DTOInServiceNotValidException.java
- **Purpose**: This file defines a custom exception that is thrown when a DTO in a service is not valid.
- **Functions**:
  - **DTOInServiceNotValidException**: Constructor for DTOInServiceNotValidException. It initializes the errorMsgs with the results of the validation.
  - **getErrorMsgs**: This function returns the results of the failed validation.

#### File: ExceptionDetailMessage.java
- **Path**: exception/response/ExceptionDetailMessage.java
- **Purpose**: This file defines a class for detailed exception messages.
- **Functions**:
  - **ExceptionDetailMessage**: Default constructor for the ExceptionDetailMessage class
  - **ExceptionDetailMessage**: Overloaded constructor for the ExceptionDetailMessage class that accepts field and message as parameters
  - **getField**: Getter method for the field property
  - **setField**: Setter method for the field property
  - **getMessage**: Getter method for the message property
  - **setMessage**: Setter method for the message property

#### File: HotelController.java
- **Path**: exception/api/HotelController.java
- **Purpose**: This file defines a controller for managing hotels.
- **Functions**:
  - **exception**: Throws a custom not found exception
  - **create**: Creates a new hotel
  - **update**: Updates a hotel by its id

#### File: ExceptionDetailBuilder.java
- **Path**: exception/response/ExceptionDetailBuilder.java
- **Purpose**: This file defines a builder class for creating detailed exception messages.
- **Functions**:
  - **ExceptionDetailBuilder**: Constructs a new ExceptionDetailBuilder.
  - **build**: Invoke this method to obtain the ExceptionDetail object after using builder methods to populate it.
  - **exception**: Populate the ExceptionDetail attributes with information from the Exception. Returns this ExceptionDetailBuilder to chain method invocations.
  - **exceptionDetail**: Populate the ExceptionDetail attributes with information from the List<ExceptionDetailMessage>. Returns this ExceptionDetailBuilder to chain method invocations.
  - **httpStatus**: Populate the ExceptionDetail attributes with information from a HttpStatus. Returns this ExceptionDetailBuilder to chain method invocations.
  - **webRequest**: Populate the ExceptionDetail attributes with information from a WebRequest. Typically use either a WebRequest or HttpServletRequest, but not both. Returns this ExceptionDetailBuilder to chain method invocations.
  - **httpServletRequest**: Populate the ExceptionDetail attributes with information from a HttpServletRequest. Typically use either a WebRequest or HttpServletRequest, but not both. Returns this ExceptionDetailBuilder to chain method invocations.

#### File: ExceptionDetail.java
- **Path**: exception/domain/ExceptionDetail.java
- **Purpose**: This file defines a class for detailed exception messages.
- **Functions**:
  - **ExceptionDetail**: Constructor for the ExceptionDetail class. It sets the timestamp to the current system time in milliseconds.
  - **getTimestamp**: Returns the timestamp attribute value.
  - **setTimestamp**: Sets the timestamp attribute value.
  - **getMethod**: Returns the method attribute value.
  - **setMethod**: Sets the method attribute value.
  - **getPath**: Returns the path attribute value.
  - **setPath**: Sets the path attribute value.
  - **getStatus**: Returns the status attribute value.
  - **setStatus**: Sets the status attribute value.
  - **getStatusText**: Returns the statusText attribute value.
  - **setStatusText**: Sets the statusText attribute value.
  - **getExceptionClass**: Returns the exceptionClass attribute value.
  - **setExceptionClass**: Sets the exceptionClass attribute value.
  - **getExceptionMessage**: Returns the exceptionMessage attribute value.
  - **setExceptionMessage**: Sets the exceptionMessage attribute value.
  - **getExceptionMessageDetail**: Returns the exceptionMessageDetail attribute value.
  - **setExceptionMessageDetail**: Sets the exceptionMessageDetail attribute value.

---

Note: None of the functions in the ExceptionService call other microservices.

---

# Microservice Migration Report: HotelService

## Overview

The HotelService microservice is responsible for managing hotel data. It provides functionality for creating, reading, updating, and deleting hotels. It also validates hotel data and handles exceptions.

## Migrating from Monolith to Microservices

1. **Identify the HotelService functionality in the monolith**: The first step is to identify all the functionality related to HotelService in the monolith application. This includes all the functions, classes, and data models.

2. **Create a new microservice project**: Create a new microservice project for HotelService. This will be a separate application with its own codebase.

3. **Move the HotelService code to the new microservice**: Move the identified HotelService code from the monolith to the new microservice. This includes all the functions, classes, and data models related to HotelService.

4. **Refactor the code**: Refactor the code to make it work in the microservice architecture. This includes changing the way the code interacts with the database and other services.

5. **Test the new microservice**: Test the new microservice to make sure it works correctly. This includes unit tests, integration tests, and end-to-end tests.

6. **Deploy the new microservice**: Deploy the new microservice to the production environment. This includes setting up the necessary infrastructure and configuring the service.

7. **Update the monolith to use the new microservice**: Update the monolith to use the new HotelService microservice. This includes changing the code in the monolith to call the new microservice instead of using the old HotelService code.

8. **Test the updated monolith**: Test the updated monolith to make sure it works correctly with the new microservice.

9. **Deploy the updated monolith**: Deploy the updated monolith to the production environment.

10. **Monitor and optimize the new microservice**: Monitor the new microservice to make sure it's performing well. Optimize the service as necessary.

## Files

### HotelDto.java

- **File Path**: hotel/dto/HotelDto.java
- **Purpose**: This file is used to transfer data of Hotel object. It does not contain any functions.

### HotelRestController.java

- **File Path**: hotel/controller/HotelRestController.java
- **Purpose**: This file is responsible for handling RESTful HTTP requests related to Hotel. It does not contain any functions.

### HotelValidationImpl.java

- **File Path**: service/validation/impl/HotelValidationImpl.java
- **Purpose**: This file is responsible for validating hotel data.
- **Functions**:
  - `isValidateHotelId`: This function checks if a hotel with the given id exists in the repository. If it does not exist, it adds a new ExceptionDetailMessage to a list and returns this list. It calls the `ExceptionDetailMessage` function from the `ExceptionService` microservice.

### HotelController.java

- **File Path**: hotel/api/HotelController.java
- **Purpose**: This file is responsible for handling HTTP requests related to Hotel.
- **Functions**:
  - `findAll`: Returns a paginated list of all hotels.
  - `findAll`: Returns a list of all hotels.
  - `findById`: Returns a hotel by its id.
  - `create`: Creates a new hotel.
  - `update`: Updates a hotel by its id.
  - `deleteById`: Deletes a hotel by its id.
  - `postPublicView`: Returns a hotel DTO with public view.
  - `postInternalView`: Returns a hotel DTO with internal view.

### HotelService.java

- **File Path**: hotel/service/HotelService.java
- **Purpose**: This file is responsible for providing services related to Hotel. It does not contain any functions.

### HotelValidation.java

- **File Path**: hotel/validation/HotelValidation.java
- **Purpose**: This file is responsible for providing validation services for Hotel.
- **Functions**:
  - `isValidateHotelId`: Check exist a hotel.

### HotelRepositoryCustom.java

- **File Path**: hotel/repository/HotelRepositoryCustom.java
- **Purpose**: This file is responsible for providing custom repository services for Hotel.
- **Functions**:
  - `someCustomMethod`: Do something.
  - `allHotels`: Returns list all Hotels.

### HotelRepository.java

- **File Path**: hotel/repository/HotelRepository.java
- **Purpose**: This file is responsible for providing repository services for Hotel. It does not contain any functions.

### Hotel.java

- **File Path**: hotel/domain/Hotel.java
- **Purpose**: This file is responsible for defining the Hotel domain model.
- **Functions**:
  - `getName`: Getter function for 'name' property.
  - `setName`: Setter function for 'name' property.
  - `getClassification`: Getter function for 'classification' property.
  - `setClassification`: Setter function for 'classification' property.
  - `isOpen`: Getter function for 'open' property.
  - `setOpen`: Setter function for 'open' property.

### HotelRepositoryImpl.java

- **File Path**: hotel/repository/impl/HotelRepositoryImpl.java
- **Purpose**: This file is responsible for providing implementation of custom repository services for Hotel.
- **Functions**:
  - `someCustomMethod`: This is a custom method that takes a Hotel object as an argument. The implementation is not provided in this code snippet.
  - `allHotels`: This method returns a list of all Hotel objects. It uses the EntityManager to create a CriteriaBuilder, which is then used to create a CriteriaQuery. The query is executed and the results are returned.

### HotelSeeder.java

- **File Path**: hotel/seeding/HotelSeeder.java
- **Purpose**: This file is responsible for seeding the database with initial Hotel data.
- **Functions**:
  - `run`: This function is an override of the run method from the CommandLineRunner interface. It creates three Hotel objects, adds them to a list, and saves them to the hotelRepository.

### HotelServiceImpl.java

- **File Path**: service/impl/HotelServiceImpl.java
- **Purpose**: This file is responsible for providing implementation of services related to Hotel.
- **Functions**:
  - `findAll`: Returns a paginated list of all hotels.
  - `findAll`: Returns a list of all hotels.
  - `findById`: Returns a hotel by its ID.
  - `create`: Creates a new hotel and returns its ID.
  - `update`: Updates an existing hotel by its ID.
  - `deleteById`: Deletes a hotel by its ID.

---

