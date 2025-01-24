import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AccountCreationComponent } from './account-creation.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { RegisterService } from '../services/register.service';
import { of, throwError } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

describe('AccountCreationComponent', () => {
  let component: AccountCreationComponent;
  let fixture: ComponentFixture<AccountCreationComponent>;
  let registerService: jasmine.SpyObj<RegisterService>;

  beforeEach(async () => {
    const registerServiceSpy = jasmine.createSpyObj('RegisterService', ['register']);

    await TestBed.configureTestingModule({
        imports: [
          HttpClientTestingModule,
          ReactiveFormsModule,
          RouterTestingModule,
          AccountCreationComponent, // Importez le composant standalone ici
        ],
        providers: [
          { provide: RegisterService, useValue: registerServiceSpy },
        ],
      }).compileComponents();
      

    fixture = TestBed.createComponent(AccountCreationComponent);
    component = fixture.componentInstance;
    registerService = TestBed.inject(RegisterService) as jasmine.SpyObj<RegisterService>;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the form with default values', () => {
    const form = component.accountCreationForm;
    expect(form.value).toEqual({
      email: '',
      password: '',
      firstname: '',
      lastname: '',
      passwordConfirmation: '',
      acceptCgu: false,
    });
  });

  it('should show an error if any field is empty', () => {
    component.handleSubmit();
    expect(component.errorMessage).toBe('Veuillez remplir tous les champs');
  });

  it('should show an error if passwords do not match', () => {
    component.accountCreationForm.patchValue({
      email: 'test@example.com',
      firstname: 'John',
      lastname: 'Doe',
      password: 'Password123!',
      passwordConfirmation: 'DifferentPassword123!',
      acceptCgu: true
    });
    component.handleSubmit();
    expect(component.errorMessage).toBe('Les mots de passe ne sont pas identiques');
  });
  

  it('should show an error if email is invalid', () => {
    component.accountCreationForm.patchValue({
      email: 'invalid-email', // Email invalide
      firstname: 'John',
      lastname: 'Doe',
      password: 'Password123!',
      passwordConfirmation: 'Password123!',
      acceptCgu: true
    });
    component.handleSubmit();
    expect(component.errorMessage).toBe('Adresse email invalide');
  });
  

  it('should show an error if password is too short', () => {
    component.accountCreationForm.patchValue({
      email: 'test@example.com',
      firstname: 'John',
      lastname: 'Doe',
      password: 'Short1', // Mot de passe trop court
      passwordConfirmation: 'Short1',
      acceptCgu: true
    });
    component.handleSubmit();
    expect(component.errorMessage).toBe('Votre mot de passe doit fait 8 caractères minimum');
  });
  

  it('should call register service with valid data', () => {
    registerService.register.and.returnValue(of(new HttpResponse({
        status: 200,
        body: '123'
      })));

    component.accountCreationForm.patchValue({
      email: 'test@example.com',
      password: 'Password123!',
      firstname: 'John',
      lastname: 'Doe',
      passwordConfirmation: 'Password123!',
      acceptCgu: true,
    });
    component.handleSubmit();

    expect(registerService.register).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'Password123!',
      firstname: 'John',
      lastname: 'Doe',
      acceptCgu: true,
    });
  });

  it('should handle registration error if email already exists', () => {
    registerService.register.and.returnValue(throwError({ status: 409 }));

    component.accountCreationForm.patchValue({
      email: 'test@example.com',
      password: 'Password123!',
      firstname: 'John',
      lastname: 'Doe',
      passwordConfirmation: 'Password123!',
      acceptCgu: true,
    });
    component.handleSubmit();

    expect(component.errorMessage).toBe('Cet email existe déja, veuillez vous connecter');
  });
});
