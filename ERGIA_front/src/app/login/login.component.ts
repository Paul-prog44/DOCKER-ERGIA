import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environments/environments';
import { AuthService } from '../auth.service';
import { Token } from '../../api/models/token';
import { User } from '../../api/models/user';
import { UserService } from '../services/user.service';
import {NgIf} from "@angular/common";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule,  NgIf],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})

export class LoginComponent {

  constructor(private authService: AuthService, private router: Router, private http: HttpClient, private userService: UserService) {}

  get apiUrlValue(): string {
    return this.apiUrl;
  }

  loginForm = new FormGroup({
    email: new FormControl(''),
    password: new FormControl(''),
  });

  private apiUrl = environment.apiUrl


  errorMessage = ""

  handleSubmit() {
    let data = {
      "email": this.loginForm.value.email,
      "password": this.loginForm.value.password
    }

    if(data.email == ""  || data.password == "") {
      this.errorMessage = "Veuillez remplir tous les champs"
      return
    }  
  
  this.http.post<Token>(`${this.apiUrl}/login`, data,
    {observe: 'response'}).subscribe({
      next: response =>{
        localStorage.setItem("id_user", response.body!.id_user)
        this.authService.saveToken(response.body!.token);
        this.authService.login();
        this.router.navigate(['/'])
      },
      error: err => {
        this.errorMessage = "Identifiants incorrectes"
        console.error('Erreur lors de la récupération des données :', err.message);
      }
    });
  }
}
