import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

/**
 * HTTP Client
 * Acts as a centralized layer for handling HTTP requests
 * to external microservices.
 *
 * Responsibilities:
 * - Standardize request configuration
 * - Improve code reusability
 * - Simplify service communication
 * - Provide a single point for future enhancements (e.g. interceptors, retries)
 *
 * @param url - Base URL of the target microservice
 */
export class HttpClient {
  private connection: AxiosInstance;

  constructor(baseURL: string) {
    this.connection = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        "Content-Type": "application/json",
        "X-Gateway-Version": "1.0",
      },
    });
  }

  async get(url: string, config?: AxiosRequestConfig) {
    return this.connection.get(url, config);
  }

  async post(url: string, config?: AxiosRequestConfig) {
    return this.connection.post(url, config);
  }

  async patch(url: string, config?: AxiosRequestConfig) {
    return this.connection.patch(url, config);
  }

  async put(url: string, config?: AxiosRequestConfig) {
    return this.connection.put(url, config);
  }
  async delete(url: string, config?: AxiosRequestConfig) {
    return this.connection.delete(url, config);
  }
}
