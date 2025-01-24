import { TestBed, ComponentFixture } from '@angular/core/testing';
import { MycampaignComponent } from './mycampaign.component';
import { CampaignService } from '../services/campaign.service';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { of } from 'rxjs';

// Mock service
class MockCampaignService {
  getCampaign(campaignId: number) {
    return of([
      {
        id_campaign: campaignId,
        name: 'Test Campaign',
        creation_date: '2023-01-01',
        date_phase_1: '2023-02-01',
        date_phase_2: '2023-03-01',
        status_id: 2,
        owner_id: 1,
      },
    ]);
  }

  getCampaignsByOwner(userId: string) {
    return of({ 'campagne dont vous êtes propriétaire': [{ id_campaign: 1 }] });
  }

  getCampaigns() {
    return of([
      {
        id_campaign: 1,
        name: 'Test Campaign',
        creation_date: '2023-01-01',
        date_phase_1: '2023-02-01',
        date_phase_2: '2023-03-01',
        status_id: 2,
        owner_id: 1,
      },
    ]);
  }

  updateCampaignStatus(updateData: any) {
    return of({ success: true });
  }
}

describe('MycampaignComponent', () => {
  let component: MycampaignComponent;
  let fixture: ComponentFixture<MycampaignComponent>;
  let campaignService: CampaignService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MycampaignComponent, ReactiveFormsModule],
      providers: [
        FormBuilder,
        { provide: CampaignService, useClass: MockCampaignService },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(MycampaignComponent);
    component = fixture.componentInstance;
    campaignService = TestBed.inject(CampaignService);
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });
  

  it('should toggle campaign details visibility', () => {
    spyOn(campaignService, 'getCampaign').and.callThrough();
    component.toggleDetails(1);
    fixture.detectChanges();

    expect(campaignService.getCampaign).toHaveBeenCalledWith(1);
    expect(component.selectedCampaign).toBeTruthy();

    component.toggleDetails(1);
    expect(component.selectedCampaign).toBeNull();
  });

  it('should update campaign status', () => {
    const mockCampaign = {
      id_campaign: 1,
      status_id: 2
    };
    spyOn(campaignService, 'updateCampaignStatus').and.callThrough();

    component.manageCampaignStatus(mockCampaign, 'startPhase1');
    fixture.detectChanges();

    expect(campaignService.updateCampaignStatus).toHaveBeenCalledWith({
      campaign_id: 1,
      status_id: 3
    });
    expect(mockCampaign.status_id).toEqual(3);
  });

  it('should filter campaigns by search input', () => {
    component.campaigns = [
      { name: 'First Campaign', id_campaign: 1 },
      { name: 'Second Campaign', id_campaign: 2 }
    ];

    component.searchForm.setValue({ searchInput: 'First' });
    component.searchCampaigns();

    expect(component.campaigns.length).toEqual(1);
    expect(component.campaigns[0].name).toEqual('First Campaign');
  });

  it('should return true if the campaign is selected', () => {
    component.selectedCampaign = { id: 1 };
    expect(component.isCampaignSelected(1)).toBeTrue();
  });
  
  it('should return false if the campaign is not selected', () => {
    component.selectedCampaign = { id: 1 };
    expect(component.isCampaignSelected(2)).toBeFalse();
  });
  
  it('should return false if no campaign is selected', () => {
    component.selectedCampaign = null;
    expect(component.isCampaignSelected(1)).toBeFalse();
  });

  it('should set newStatusId to 3 when action is "startPhase1" and status_id is 2', () => {
    const mockCampaign = { id_campaign: 1, status_id: 2 };
    spyOn(campaignService, 'updateCampaignStatus').and.returnValue(of({ success: true }));
  
    component.manageCampaignStatus(mockCampaign, 'startPhase1');
  
    expect(campaignService.updateCampaignStatus).toHaveBeenCalledWith({
      campaign_id: 1,
      status_id: 3,
    });
    expect(mockCampaign.status_id).toBe(3);
  });
  
  it('should set newStatusId to 4 when action is "endPhase1" and status_id is 3', () => {
    const mockCampaign = { id_campaign: 1, status_id: 3 };
    spyOn(campaignService, 'updateCampaignStatus').and.returnValue(of({ success: true }));
  
    component.manageCampaignStatus(mockCampaign, 'endPhase1');
  
    expect(campaignService.updateCampaignStatus).toHaveBeenCalledWith({
      campaign_id: 1,
      status_id: 4,
    });
    expect(mockCampaign.status_id).toBe(4);
  });
  
  it('should set newStatusId to 5 when action is "startPhase2" and status_id is 4', () => {
    const mockCampaign = { id_campaign: 1, status_id: 4 };
    spyOn(campaignService, 'updateCampaignStatus').and.returnValue(of({ success: true }));
  
    component.manageCampaignStatus(mockCampaign, 'startPhase2');
  
    expect(campaignService.updateCampaignStatus).toHaveBeenCalledWith({
      campaign_id: 1,
      status_id: 5,
    });
    expect(mockCampaign.status_id).toBe(5);
  });
  
  it('should set newStatusId to 6 when action is "endPhase2" and status_id is 5', () => {
    const mockCampaign = { id_campaign: 1, status_id: 5 };
    spyOn(campaignService, 'updateCampaignStatus').and.returnValue(of({ success: true }));
  
    component.manageCampaignStatus(mockCampaign, 'endPhase2');
  
    expect(campaignService.updateCampaignStatus).toHaveBeenCalledWith({
      campaign_id: 1,
      status_id: 6,
    });
    expect(mockCampaign.status_id).toBe(6);
  });
  
  it('should return the id_campaign of the given campaign', () => {
    const campaign = { id_campaign: 42, name: 'Test Campaign' };
  
    const result = component.trackByCampaignId(0, campaign);
  
    expect(result).toBe(42);
  });
  
  
});
