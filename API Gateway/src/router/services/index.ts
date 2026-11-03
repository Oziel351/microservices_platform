import { HttpClient } from "../../class/httpRequest.class";
import config from "../../config";

export const services = {
  users: new HttpClient(config.services.users),
  products: new HttpClient(config.services.products),
};
