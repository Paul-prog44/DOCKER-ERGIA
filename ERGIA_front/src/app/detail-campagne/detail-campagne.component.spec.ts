import { TestBed, ComponentFixture } from '@angular/core/testing';
import { DetailCampagneComponent } from './detail-campagne.component';
import { CampaignService } from '../services/campaign.service';
import { UserService } from '../services/user.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { FormsModule } from '@angular/forms';

class MockCampaignService {
  getCampaign(id: number) {
    return of([
      {
        name: 'Mock Campaign',
        date_phase_1: '2023-01-01',
        date_phase_2: '2023-02-01',
        owner_id: 'Owner Mock'
      }
    ]);
  }

  getOriginalTexts(id: number) {
    return of([
      { id: 1, content: 'Original Text 1' },
      { id: 2, content: 'Original Text 2' }
    ]);
  }

  joinCampaigns(data: any) {
    return of({ success: true });
  }

  leaveCampaign(data: any) {
    return of({ success: true });
  }
}

class MockUserService {
  getUserCompaignJoined() {
    return of([
      { id_campaign: 1 },
      { id_campaign: 2 }
    ]);
  }
}

describe('DetailCampagneComponent', () => {
  let component: DetailCampagneComponent;
  let fixture: ComponentFixture<DetailCampagneComponent>;
  let campaignService: CampaignService;
  let userService: UserService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        DetailCampagneComponent, // Ajouter ici au lieu de declarations
        HttpClientTestingModule,
        FormsModule,
      ],
      providers: [
        { provide: CampaignService, useClass: MockCampaignService },
        { provide: UserService, useClass: MockUserService },
        {
          provide: ActivatedRoute,
          useValue: {
            params: of({ id: 1 }),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DetailCampagneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    fixture = TestBed.createComponent(DetailCampagneComponent);
    component = fixture.componentInstance;
    campaignService = TestBed.inject(CampaignService);
    userService = TestBed.inject(UserService);
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });
  

  it('should load joined campaigns', () => {
    spyOn(userService, 'getUserCompaignJoined').and.callThrough();
    component.loadJoinedCampaigns();
    fixture.detectChanges();

    expect(userService.getUserCompaignJoined).toHaveBeenCalled();
    expect(component.joinedCampaignsIds).toEqual([1, 2]);
  });

  it('should join a campaign', () => {
    // Simuler localStorage pour retourner un ID utilisateur valide
    spyOn(localStorage, 'getItem').and.returnValue('123');
  
    // Espionner la méthode joinCampaigns
    spyOn(campaignService, 'joinCampaigns').and.callThrough();
    spyOn(component, 'loadJoinedCampaigns');
  
    // Appeler la méthode joinCampaign
    component.joinCampaign();
  
    // Vérifier que le service joinCampaigns a été appelé avec les bons paramètres
    expect(campaignService.joinCampaigns).toHaveBeenCalledWith({
      campaign_id: 1,
      user_id: 123, // Correspond à l'ID utilisateur simulé
    });
  
    // Vérifier que loadJoinedCampaigns a été appelé pour recharger les données
    expect(component.loadJoinedCampaigns).toHaveBeenCalled();
  });
  

  it('should leave a campaign', () => {
    // Simuler localStorage pour retourner un ID utilisateur valide
    spyOn(localStorage, 'getItem').and.returnValue('123');
  
    // Espionner la méthode leaveCampaign
    spyOn(campaignService, 'leaveCampaign').and.callThrough();
    spyOn(component, 'loadJoinedCampaigns');
  
    // Appeler la méthode leaveCampaign
    component.leaveCampaign();
  
    // Vérifier que le service leaveCampaign a été appelé avec les bons paramètres
    expect(campaignService.leaveCampaign).toHaveBeenCalledWith({
      campaign_id: 1,
      user_id: 123, // Correspond à l'ID utilisateur simulé
    });
  
    // Vérifier que loadJoinedCampaigns a été appelé pour recharger les données
    expect(component.loadJoinedCampaigns).toHaveBeenCalled();
  });
  

  it('should check if the campaign is joined', () => {
    component.joinedCampaignsIds = [1, 2];
    component.id = 1;

    expect(component.isJoined()).toBeTrue();

    component.id = 3;
    expect(component.isJoined()).toBeFalse();
  });
});
