import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../environments/environments';
import { InterfaceUser } from '../../api/models/interface-user'

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  private apiUrl = environment.apiUrl

  constructor(private http: HttpClient) { }

  register(data : InterfaceUser) {
    const headers = new HttpHeaders({
          "Content-Type": "application/json",
          "Accept": "application/json"
      });
    return this.http.post(`${this.apiUrl}/register`, JSON.stringify(data), {
      headers: headers,
      observe: 'response'} 
  )}
}