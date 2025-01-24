import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environments';
import { ApiCampaign } from '../../api/models/campaign';


@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = environment.apiUrl


  constructor(private http : HttpClient) {}
  getUser(): Observable<any> {
    
    return this.http.get(`${this.apiUrl}/user`)
  }
  
  updateUser(id: string, data : any): Observable<any> {
    return this.http.put(`${this.apiUrl}/register/${id}`, data)
  }

  deleteUser(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/user/${id}`)
  }
  
  changePassword(userId: string, data: { old_password: string; new_password: string }): Observable<any> {
    return this.http.put(`${this.apiUrl}/register/password/${userId}`, data);
  }
  
  getUserCompaignJoined(): Observable<ApiCampaign[]> {
    return this.http.get<ApiCampaign[]>(`${this.apiUrl}/campaigns/joined`);
  }
  
  getCampaignsByCreator(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/campaigns/created/${userId}`);
  }  
}
