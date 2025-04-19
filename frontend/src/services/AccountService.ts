import type { IResultObject } from '@/types/IResultObject'
import type { IUserInfo } from '@/types/IUserInfo'
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";

export default class AccountService {

  static async loginAsync(username: string, password: string): Promise<IResultObject<IUserInfo>> {
    const loginData = {
      username,
      password
    }
    try {
      const response = await apiClient.post<IUserInfo>('login/', loginData);
      if (response.status < 300) {
        return {
          data: response.data
        }
      }
      return {
        errors: [response.status.toString() + ' ' + response.statusText]
      }
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }


  static async refreshToken(refreshToken: string): Promise<IResultObject<{ access: string }>> {
    try {
      const response = await apiClient.post<{ access: string }>('token/refresh/', {
        refresh: refreshToken
      })

      if (response.status < 300) {
        return {
          data: response.data
        }
      }
      return {
        errors: [response.status.toString() + ' ' + response.statusText]
      }
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }
}
