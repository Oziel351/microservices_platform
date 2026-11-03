import dotenv from "dotenv";
dotenv.config();

/**
 * Configuration Module
 *
 * Centralizes environment variables and microservice
 * endpoints used by the API Gateway.
 *
 * This allows the application to dynamically resolve
 * service URLs without hardcoding them in the codebase,
 * improving scalability and maintainability.
 */

interface ISERVICES {
  users: string;
  products: string;
}

const Services = {
  users: process.env.USER_SERVICE || "http://localhost:8000",
  products: process.env.PRODUCT_SERVICE || "http://localhost:8001",
};

interface Config {
  port: number;
  services: ISERVICES;
  nodeEnv: string;
  jwt: string;
}

const config: Config = {
  port: parseInt(process.env.PORT || "3000", 10),
  services: Services,
  nodeEnv: process.env.NODE_ENV || "development",
  jwt: process.env.JWT_TOKEN || "jwthere",
};

export default config;
