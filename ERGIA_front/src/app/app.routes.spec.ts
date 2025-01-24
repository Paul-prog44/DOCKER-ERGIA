import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { routes } from './app.routes';
import { Location } from '@angular/common';
import { AccueilComponent } from './accueil/accueil.component';
import { LoginComponent } from './login/login.component';
import { CampaignCreationComponent } from './campaign-creation/campaign-creation.component';
import { AccountCreationComponent } from './account-creation/account-creation.component';
import { CampaignDashboardComponent } from './campaign-dashboard/campaign-dashboard.component';
import { UserAccountComponent } from './user-account/user-account.component';
import { DetailCampagneComponent } from './detail-campagne/detail-campagne.component';
import { CguComponent } from './cgu/cgu.component';
import { AnnotationPageComponent } from './annotation/annotation-page/annotation-page.component';
import { MycampaignComponent } from './mycampaign/mycampaign.component';
import { Component } from '@angular/core'; // Import pour MockComponent
import { CanActivateFn } from '@angular/router';
import { of } from 'rxjs';

@Component({ template: '' })
class MockComponent {}
const MockAuthGuard: CanActivateFn = () => of(true); // Simule l'accès autorisé

describe('App Routes', () => {
  let router: Router;
  let location: Location;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule.withRoutes(
          routes.map(route => ({
            ...route,
            canActivate: route.canActivate ? [MockAuthGuard] : undefined, // Remplace les guards par le mock
          }))
        ),
        AccueilComponent,
        LoginComponent,
        CampaignCreationComponent,
        AccountCreationComponent,
        CampaignDashboardComponent,
        UserAccountComponent,
        DetailCampagneComponent,
        CguComponent,
        AnnotationPageComponent,
        MycampaignComponent,
      ],
    }).compileComponents();
  
    router = TestBed.inject(Router);
    location = TestBed.inject(Location);
    router.initialNavigation();
  });
  


  it('should navigate to AccueilComponent for empty path', async () => {
    await router.navigate(['']);
    expect(location.path()).toBe('/');
  });

  it('should navigate to LoginComponent for /login', async () => {
    await router.navigate(['/login']);
    expect(location.path()).toBe('/login');
  });

  it('should navigate to CampaignCreationComponent for /createCampaign', async () => {
    await router.navigate(['/createCampaign']);
    expect(location.path()).toBe('/createCampaign');
  });

  it('should navigate to AccountCreationComponent for /createAccount', async () => {
    await router.navigate(['/createAccount']);
    expect(location.path()).toBe('/createAccount');
  });

  it('should navigate to DetailCampagneComponent for /campagne/:id', async () => {
    await router.navigate(['/campagne/1']);
    expect(location.path()).toBe('/campagne/1');
  });

  it('should navigate to CampaignDashboardComponent for /campaignDashboard', async () => {
    await router.navigate(['/campaignDashboard']);
    expect(location.path()).toBe('/campaignDashboard');
  });

  it('should navigate to UserAccountComponent for /userAccount', async () => {
    await router.navigate(['/userAccount']);
    expect(location.path()).toBe('/userAccount');
  });

  it('should navigate to CguComponent for /cgu', async () => {
    await router.navigate(['/cgu']);
    expect(location.path()).toBe('/cgu');
  });

  it('should navigate to AnnotationPageComponent for /annotation', async () => {
    await router.navigate(['/annotation']);
    expect(location.path()).toBe('/annotation');
  });

  it('should navigate to MycampaignComponent for /mycampaign', async () => {
    await router.navigate(['/mycampaign']);
    expect(location.path()).toBe('/mycampaign');
  });

  
});
