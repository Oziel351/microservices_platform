export interface API_RESPONSE<T> {
  data: T;
  message: string;
}

export interface ApiError {
  success: false;
  error: string;
  statusCode: number;
}

export interface Config {
  port: number;
  productServiceUrl: string;
  orderServiceUrl: string;
}
