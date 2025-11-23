Arquitectura de Integración Híbrida y Modelo de Datos Unificado
El proyecto implementa una plataforma de gestión académica basada en una Arquitectura Orientada a Servicios (SOA). La solución se distingue por su enfoque heterogéneo (políglota), orquestando la interoperabilidad entre un subsistema administrativo desarrollado en Java (Spring Boot) bajo el estilo arquitectónico REST, y un subsistema transaccional desarrollado en Python (Spyne) utilizando el protocolo estándar SOAP.
Para garantizar la consistencia inmediata de la información y evitar la redundancia de datos (Data Duplication), se diseñó un modelo de Base de Datos Compartida (Shared Database Pattern) sobre MySQL.
La lógica de negocio se ha desacoplado según la naturaleza de las operaciones:

Módulo Administrativo (REST - Java): Responsable de la gestión de entidades maestras (Usuarios, Roles, Carreras). Se priorizó REST por su eficiencia en operaciones CRUD y su facilidad de consumo para clientes ligeros.

Módulo Transaccional (SOAP - Python): Responsable del proceso crítico de negocio (Inscripciones). Se seleccionó SOAP para aprovechar su robustez en la definición de contratos estrictos (WSDL), ideal para procesos de registro formal.
