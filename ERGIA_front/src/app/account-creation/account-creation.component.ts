import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import { environment } from '../environments/environments';
import { HttpClient } from '@angular/common/http';
import { RegisterService } from '../services/register.service';



@Component({
  selector: 'app-account-creation',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './account-creation.component.html',
  styleUrl: './account-creation.component.scss'
})
export class AccountCreationComponent {

  accountCreationForm = new FormGroup({
    email : new FormControl(''),
    password : new FormControl(''),
    firstname : new FormControl(''),
    lastname : new FormControl(''),
    passwordConfirmation : new FormControl(''),
    acceptCgu : new FormControl(false)
  })

  errorMessage = ""
  emailRegex = new RegExp('[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$')
  constructor(private router: Router, private http: HttpClient, private registerService: RegisterService) {}

  // Fonction de vérification du mdp
  passwordComplexity = (password: string) => {
    const hasDigit = /\d/.test(password); // chiffre
    const hasUpperCase = /[A-Z]/.test(password); // majuscule
    const hasLowerCase = /[a-z]/.test(password); // minuscule
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password); // caractère spécial
    
    // Retourne true si toutes les conditions sont remplies
    return hasDigit && hasUpperCase && hasLowerCase && hasSpecialChar;
  };


  handleSubmit() {
    let data = {
      "email": this.accountCreationForm.value.email,
      "password": this.accountCreationForm.value.password,
      "firstname" : this.accountCreationForm.value.firstname,
      "lastname" : this.accountCreationForm.value.lastname,
      "passwordConfirmation" : this.accountCreationForm.value.passwordConfirmation,
      "acceptCgu" : this.accountCreationForm.value.acceptCgu
    }

    if (!data.email || !data.password || !data.firstname || !data.lastname || !data.passwordConfirmation) {
      this.errorMessage = "Veuillez remplir tous les champs"
      return
    }

    if (data.password !== data.passwordConfirmation) {
      this.errorMessage = "Les mots de passe ne sont pas identiques"
      return
    }
    if (!this.emailRegex.test(data.email)) {
      this.errorMessage = "Adresse email invalide"
      return
    }
    
    if (data.password!.length < 8 ) {
      this.errorMessage = "Votre mot de passe doit fait 8 caractères minimum"
      return
    }
    if (!this.passwordComplexity(data.password!)) {
       this.errorMessage = "Votre mot de passe doit contenir au moins, un caractère spécial, une minuscule, une majuscule et un chiffre"
       return
    }
    if (!this.accountCreationForm.value.acceptCgu) {
      this.errorMessage = "Vous devez accepter les CGU pour pouvoir utiliser le site"
      return
    }

  this.registerService.register({
    email: data.email || '',
    password: data.password || '',
    firstname: data.firstname || '',
    lastname: data.lastname || '',
    acceptCgu: data.acceptCgu || false
  }).subscribe({
    next: (response) => {
      if (response.status == 200) {
        localStorage.setItem("user_id", String(response.body));
        this.router.navigate(['/']);
      }
    },
    error: (err) => {
      if (err.status == 409) {
        this.errorMessage = "Cet email existe déja, veuillez vous connecter"
      }
    }
  });
}}
