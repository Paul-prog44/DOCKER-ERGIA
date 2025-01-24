import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { LoginComponent } from './login.component';
import { AuthService } from '../auth.service';
import { UserService } from '../services/user.service';
import { of } from 'rxjs';
import { environment } from '../environments/environments';
import { Router } from '@angular/router';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let httpMock: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    // Création de mock pour les services
    authServiceSpy = jasmine.createSpyObj('AuthService', ['saveToken', 'login']);
    routerSpy = jasmine.createSpyObj('Router', ['navigate']);
    
    await TestBed.configureTestingModule({
      imports: [LoginComponent, HttpClientTestingModule, RouterTestingModule],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
        { provide: Router, useValue: routerSpy },
        { provide: UserService, useValue: {} }, // Mock UserService si nécessaire
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);

    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should return correct API URL', () => {
    expect(component.apiUrlValue).toBe(environment.apiUrl);
  });

  it('should call the API and navigate when the form is valid', () => {
    const mockToken = { id_user: '123', token: 'valid_token' };
    component.loginForm.setValue({ email: 'user@example.com', password: 'password' });

    // Vérifier que l'API URL est correcte
    expect(component.apiUrlValue).toBe(environment.apiUrl);

    // Simuler la réponse du serveur
    component.handleSubmit();
    const req = httpMock.expectOne(`${component.apiUrlValue}/login`);
    expect(req.request.method).toBe('POST');
    req.flush(mockToken); // Simuler une réponse réussie

    // Vérifier que le service AuthService et Router ont été appelés
    expect(authServiceSpy.saveToken).toHaveBeenCalledWith('valid_token');
    expect(authServiceSpy.login).toHaveBeenCalled();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/']);
  });

  it('should show an error message when the form is invalid', () => {
    component.loginForm.setValue({ email: '', password: '' });
    component.handleSubmit();

    expect(component.errorMessage).toBe('Veuillez remplir tous les champs');
  });

  it('should show an error message when login fails', () => {
    const mockError = { message: 'Unauthorized' };
    component.loginForm.setValue({ email: 'user@example.com', password: 'wrong_password' });

    component.handleSubmit();
    const req = httpMock.expectOne(`${component.apiUrlValue}/login`);
    req.flush(mockError, { status: 401, statusText: 'Unauthorized' });

    expect(component.errorMessage).toBe('Identifiants incorrectes');
  });
});
