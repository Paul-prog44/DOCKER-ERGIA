import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CampaignDashboardComponent } from './campaign-dashboard.component';
import { CampaignService } from '../services/campaign.service';
import { UserService } from '../services/user.service';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';


// Mock services
class MockCampaignService {
  getCampaigns() {
    return of([{
      id_campaign: 1,
      name: 'Test Campaign',
      description: 'A test campaign.'
    }]);
  }

  getCampaignByName(name: string) {
    if (name === 'Test Campaign') {
      return of({
        id_campaign: 1,
        name: 'Test Campaign',
        description: 'A test campaign.'
      });
    }
    return throwError('Campaign not found');
  }
}

class MockUserService {
  getUserCompaignJoined() {
    return of([{
      id_campaign: 2,
      name: 'User Campaign',
      description: 'A user-specific campaign.'
    }]);
  }
}

describe('CampaignDashboardComponent', () => {
  let component: CampaignDashboardComponent;
  let fixture: ComponentFixture<CampaignDashboardComponent>;
  let campaignService: CampaignService;
  let userService: UserService;

  beforeEach(async () => {
    TestBed.configureTestingModule({
        imports: [CampaignDashboardComponent, ReactiveFormsModule, RouterTestingModule],
        providers: [
          { provide: CampaignService, useClass: MockCampaignService },
          { provide: UserService, useClass: MockUserService },
          {
            provide: ActivatedRoute,
            useValue: {
              snapshot: { params: {}, queryParams: {} },
              paramMap: of({ get: () => null }),
              queryParamMap: of({ get: () => null }),
            },
          },
        ],
      }).compileComponents();
      

    fixture = TestBed.createComponent(CampaignDashboardComponent);
    component = fixture.componentInstance;
    campaignService = TestBed.inject(CampaignService);
    userService = TestBed.inject(UserService);
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should load campaigns on init', () => {
    spyOn(campaignService, 'getCampaigns').and.callThrough();
    component.ngOnInit();
    expect(campaignService.getCampaigns).toHaveBeenCalled();
    expect(component.campaigns.length).toBe(1);
    expect(component.campaigns[0].name).toBe('Test Campaign');
  });

  it('should search for a campaign by name', () => {
    component.searchForm.setValue({ searchInput: 'Test Campaign' });
    spyOn(campaignService, 'getCampaignByName').and.callThrough();

    component.handleSubmit();
    expect(campaignService.getCampaignByName).toHaveBeenCalledWith('Test Campaign');
    expect(component.campaigns.length).toBe(1);
    expect(component.campaigns[0].name).toBe('Test Campaign');
  });

  it('should handle empty search input by resetting campaigns', () => {
    component.searchForm.setValue({ searchInput: '' });

    component.handleSubmit();
    expect(component.campaigns).toEqual(component.allCampaigns);
  });

  it('should load user-specific campaigns', () => {
    spyOn(userService, 'getUserCompaignJoined').and.callThrough();

    component.handleLookCampaign();
    expect(userService.getUserCompaignJoined).toHaveBeenCalled();
    expect(component.campaigns.length).toBe(1);
    expect(component.campaigns[0].name).toBe('User Campaign');
  });

  it('should handle search error gracefully', () => {
    component.searchForm.setValue({ searchInput: 'Nonexistent Campaign' });
    spyOn(campaignService, 'getCampaignByName').and.returnValue(throwError('Campaign not found'));

    component.handleSubmit();
    expect(component.campaigns.length).toBe(0);
  });
});
