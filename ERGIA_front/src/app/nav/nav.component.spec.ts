import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NavComponent } from './nav.component';
import { AuthService } from '../auth.service';
import { RouterTestingModule } from '@angular/router/testing';
import { By } from '@angular/platform-browser';

describe('NavComponent', () => {
  let component: NavComponent;
  let fixture: ComponentFixture<NavComponent>;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(async () => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['isLoggedIn', 'logout']);

    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule.withRoutes([
          { path: '', redirectTo: '/', pathMatch: 'full' },
          { path: 'campaignDashboard', redirectTo: '/campaignDashboard' },
          { path: 'login', redirectTo: '/login' },
        ]),
        NavComponent,
      ],
      providers: [
        { provide: AuthService, useValue: authServiceSpy },
      ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display "Se Connecter" if user is not logged in', () => {
    authServiceSpy.isLoggedIn.and.returnValue(false); // Simule que l'utilisateur n'est pas connecté
    fixture.detectChanges();

    const loginLink = fixture.debugElement.query(By.css('.navRight a'));
    expect(loginLink.nativeElement.textContent).toContain('Se Connecter');
    expect(loginLink.attributes['routerLink']).toBe('/login');
  });

  it('should display "Déconnexion" if user is logged in', () => {
    authServiceSpy.isLoggedIn.and.returnValue(true); // Simule que l'utilisateur est connecté
    fixture.detectChanges();

    const logoutButton = fixture.debugElement.query(By.css('.navRight button'));
    expect(logoutButton.nativeElement.textContent).toContain('Déconnexion');
  });

  it('should call logout on AuthService when "Déconnexion" is clicked', () => {
    authServiceSpy.isLoggedIn.and.returnValue(true);
    fixture.detectChanges();

    const logoutButton = fixture.debugElement.query(By.css('.navRight button'));
    logoutButton.triggerEventHandler('click', null);

    expect(authServiceSpy.logout).toHaveBeenCalled();
  });
});
