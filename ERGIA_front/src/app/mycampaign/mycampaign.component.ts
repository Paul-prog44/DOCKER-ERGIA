import { Component, OnInit } from '@angular/core';
import { CampaignService } from '../services/campaign.service';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-mycampaign',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './mycampaign.component.html',
  styleUrls: ['./mycampaign.component.scss']
})
export class MycampaignComponent implements OnInit {
  campaigns: any[] = [];
  selectedCampaign: any = null;
  searchForm: FormGroup;

  constructor(private campaignService: CampaignService, private formBuilder: FormBuilder) {
    this.searchForm = this.formBuilder.group({
      searchInput: ['']
    });
  }

  ngOnInit(): void {
    this.loadUserCampaigns();
  }

  isCampaignSelected(campaignId: number): boolean {
    return this.selectedCampaign?.id === campaignId;
  }

  // Exemple de méthode existante pour charger les détails d'une campagne
  loadCampaignDetails(campaignId: number): void {
    // Exemple simplifié de service (ajustez en fonction de votre implémentation réelle)
    this.campaignService.getCampaign(campaignId).subscribe({
      next: (response: any[]) => {
        if (response.length > 0) {
          const campaign = response[0];
          this.selectedCampaign = {
            id: campaign.id_campaign,
            name: campaign.name,
            creationDate: campaign.creation_date
              ? new Date(campaign.creation_date).toLocaleDateString()
              : 'Non spécifiée',
            phase1Date: campaign.date_phase_1
              ? new Date(campaign.date_phase_1).toLocaleDateString()
              : 'Non spécifiée',
            phase2Date: campaign.date_phase_2
              ? new Date(campaign.date_phase_2).toLocaleDateString()
              : 'Non spécifiée',
            statusId: campaign.status_id,
            ownerId: campaign.owner_id
          };
        } else {
          console.error('Aucun détail de campagne trouvé.');
          this.selectedCampaign = null;
        }
      },
      error: (err) => {
        console.error('Erreur lors du chargement des détails de la campagne:', err);
        alert('Impossible de charger les détails de la campagne.');
      }
    });
  }

  toggleDetails(campaignId: number): void {
    if (this.selectedCampaign?.id === campaignId) {
      // Masquer les détails si la même campagne est déjà sélectionnée
      this.selectedCampaign = null;
    } else {
      // Charger les détails de la nouvelle campagne sélectionnée
      this.campaignService.getCampaign(campaignId).subscribe({
        next: (response: any[]) => {
          if (response.length > 0) {
            const campaign = response[0];
            this.selectedCampaign = {
              id: campaign.id_campaign,
              name: campaign.name,
              creationDate: campaign.creation_date
                ? new Date(campaign.creation_date).toLocaleDateString()
                : 'Non spécifiée',
              phase1Date: campaign.date_phase_1
                ? new Date(campaign.date_phase_1).toLocaleDateString()
                : 'Non spécifiée',
              phase2Date: campaign.date_phase_2
                ? new Date(campaign.date_phase_2).toLocaleDateString()
                : 'Non spécifiée',
              statusId: campaign.status_id,
              ownerId: campaign.owner_id
            };
          } else {
            console.error('Aucun détail de campagne trouvé.');
            this.selectedCampaign = null;
          }
        },
        error: (err) => {
          console.error('Erreur lors du chargement des détails de la campagne:', err);
          alert('Impossible de charger les détails de la campagne.');
        }
      });
    }
  }

  // Chargement des campagnes de l'utilisateur connecté
  loadUserCampaigns(): void {
    const userId = localStorage.getItem('id_user');
    if (!userId) {
      alert('Veuillez vous connecter pour accéder à vos campagnes.');
      return;
    }

    this.campaignService.getCampaignsByOwner(userId).subscribe({
      next: (response: any) => {
        const ownedCampaignsIds = response['campagne dont vous étes propriétaire']?.map((campagne: any) => campagne.id_campaign) || [];
        this.campaignService.getCampaigns().subscribe({
          next: (allCampaigns: any[]) => {
            this.campaigns = allCampaigns
              .filter((campaign) => ownedCampaignsIds.includes(campaign.id_campaign))
              .map((campaign) => ({
                ...campaign,
                creation_date: campaign.creation_date ? new Date(campaign.creation_date).toLocaleDateString() : 'Non spécifiée',
                date_phase_1: campaign.date_phase_1 ? new Date(campaign.date_phase_1).toLocaleDateString() : 'Non spécifiée',
                date_phase_2: campaign.date_phase_2 ? new Date(campaign.date_phase_2).toLocaleDateString() : 'Non spécifiée',
                status: this.getStatusText(campaign.status_id)
              }));
          },
          error: (err) => console.error('Erreur lors du chargement des campagnes détaillées:', err)
        });
      },
      error: (err) => console.error('Erreur lors du chargement des campagnes utilisateur:', err)
    });
  }

  // Gérer les statuts des campagnes
  manageCampaignStatus(campaign: any, action: string): void {
    let newStatusId = campaign.status_id;
  
    // Déterminer le nouveau statut en fonction de l'action et de l'état actuel
    if (action === 'startPhase1' && campaign.status_id === 2) newStatusId = 3;
    else if (action === 'endPhase1' && campaign.status_id === 3) newStatusId = 4;
    else if (action === 'startPhase2' && campaign.status_id === 4) newStatusId = 5;
    else if (action === 'endPhase2' && campaign.status_id === 5) newStatusId = 6;
  
    if (newStatusId !== campaign.status_id) {
      // Appel au service pour mettre à jour le statut de la campagne
      this.campaignService.updateCampaignStatus({
        campaign_id: campaign.id_campaign, // Assurez-vous que le paramètre correspond à l'API
        status_id: newStatusId
      }).subscribe({
        next: (response) => {
          // Mise à jour locale en cas de succès
          campaign.status_id = newStatusId;
          campaign.status = this.getStatusText(newStatusId);
          alert('Statut mis à jour avec succès !');
        },
        error: (err) => {
          console.error('Erreur lors de la mise à jour du statut:', err);
          alert('Impossible de mettre à jour le statut de la campagne.');
        }
      });
    } else {
      alert('Action non valide pour l\'état actuel.');
    }
  }
  

  getStatusText(statusId: number): string {
    const statuses: { [key: number]: string } = {
      1: 'Active',
      2: 'Pending',
      3: 'Phase 1 Active',
      4: 'Phase 1 Completed',
      5: 'Phase 2 Active',
      6: 'Phase 2 Completed',
      7: 'Cancelled'
    };
    return statuses[statusId] || 'Pending';
  }

  searchCampaigns(): void {
    const searchValue = this.searchForm.value.searchInput?.toLowerCase() || '';
    this.campaigns = this.campaigns.filter((campaign) => campaign.name.toLowerCase().includes(searchValue));
  }

  trackByCampaignId(index: number, campaign: any): number {
    return campaign.id_campaign;
  }
}
