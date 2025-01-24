import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "./environments/environments";
import { jwtDecode } from "jwt-decode";
import { Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = environment.apiUrl;
  private isAuthenticated = false;

  constructor(private router: Router, private http: HttpClient) {}

  login() {
    this.isAuthenticated = true;
    console.log("Authenticated: ", this.isAuthenticated)
  }

  saveToken(token: string): void {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    const token = localStorage.getItem('token')
    return token;
  }

  isTokenExpired(token: string): boolean {
    try {
      const decoded: any = jwtDecode(token);
      const now = Math.floor(Date.now() / 1000);
      return decoded.exp < now; 
    } catch (error) {
      console.error("Erreur lors du décodage du token :", error);
      return true; 
    }
  }

  logout(): void {
    console.log("logged out");
    this.isAuthenticated = false;
    localStorage.removeItem('token')
    localStorage.removeItem('id_user')
  }

  isLoggedIn(): boolean {
    return this.isAuthenticated;
  }
}