import { notFound } from "next/navigation";

export interface Success<T> {
  data: T;
}

export interface Failure {
  error: unknown;
}

interface NetworkSuccess<T> extends Success<T> {
  request: Request;
  response: Response;
}

interface NetworkFailure extends Failure {
  request?: Request;
  response?: Response;
}

export type Result<T> = Success<T> | Failure;
export type NetworkResult<T> = NetworkSuccess<T> | NetworkFailure;

export const isSuccess: <T>(result: Result<T>) => result is Success<T> = (
  result,
) => {
  return "data" in result;
};

export const getDataOrNull: <T extends {}>(
  result: NetworkResult<T>,
) => Promise<T | null> = async (result) => {
  console.debug(result.response?.url, result.response?.status);
  if (isSuccess(result)) return result.data;
  if (result.error) {
    console.warn(result.error);
  }
  return null;
};

export const getDataOrThrow: <T extends {}>(
  result: NetworkResult<T>,
  label: string,
) => Promise<T> = async (result, label) => {
  console.debug(result.response?.url, result.response?.status);
  if (isSuccess(result)) return result.data;
  throw new Error(`Failed to get data: ${label}`);
};

export const getDataOr404: <T extends {}>(
  result: NetworkResult<T>,
) => Promise<T> = async (result) => {
  console.debug(result.response?.url, result.response?.status);
  if (isSuccess(result)) return result.data;
  if (result.error) {
    console.warn(result.error);
  }
  return notFound();
};
