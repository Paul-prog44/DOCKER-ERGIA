//campaign-dashboard
import { Component } from '@angular/core';
import { CampaignCardComponent } from '../campaign-card/campaign-card.component';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CampaignService } from '../services/campaign.service';
import { ApiCampaign } from '../../api/models/campaign';
import { UserService } from '../services/user.service';
import {NgFor, NgForOf, NgIf} from "@angular/common";





@Component({
  selector: 'app-campaign-dashboard',
  standalone: true,
  imports: [CampaignCardComponent, ReactiveFormsModule, RouterLink, NgFor, NgIf],
  templateUrl: './campaign-dashboard.component.html',
  styleUrl: './campaign-dashboard.component.scss'
})


export class CampaignDashboardComponent {
  campaigns: ApiCampaign[] = []; // Liste des campagnes affichées
  allCampaigns: ApiCampaign[] = []; // Copie de toutes les campagnes pour réinitialiser si besoin
  currentPage: number = 1; // Page actuelle
  itemsPerPage: number = 9; // Nombre d'éléments par page
  pagination: number[] = []; // Liste des numéros de page
  message: string = "";

  searchForm = new FormGroup({
    searchInput: new FormControl('') // Champ de recherche
  });

  constructor(private router: Router, private campaignService: CampaignService, private userService: UserService) {}

  ngOnInit(): void {
    this.campaignService.getCampaigns().subscribe({
      next: (data) => {
        this.allCampaigns = data; // Stockage des campagnes initiales
        this.updatePagination();
      },
      error: (err) => console.error("Erreur lors du chargement des campagnes :", err)
    });
  }

  updatePagination(): void {
    const totalPages = Math.ceil(this.allCampaigns.length / this.itemsPerPage);
    this.pagination = Array.from({ length: totalPages }, (_, i) => i + 1);
    this.updateCampaignsForCurrentPage();
  }

  updateCampaignsForCurrentPage(): void {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    this.campaigns = this.allCampaigns.slice(startIndex, endIndex);
  }

  changePage(page: number): void {
    this.currentPage = page;
    this.updateCampaignsForCurrentPage();
  }

  handleSubmit(): void {
    const searchInput = this.searchForm.value.searchInput?.trim();
    if (searchInput) {
      this.campaignService.getCampaignByName(searchInput).subscribe({
        next: (data) => {
          this.allCampaigns = Array.isArray(data) ? data : [data];
          this.updatePagination();
        },
        error: (err) => {
          console.error("Erreur lors de la recherche :", err);
          this.allCampaigns = [];
          this.updatePagination();
        }
      });
    } else {
      this.campaigns = this.allCampaigns;
    }
  }

  handleLookCampaign(): void {
    this.userService.getUserCompaignJoined().subscribe({
      next: (data) => {
        this.allCampaigns = data;
        this.updatePagination();
      },
      error: (err) => {
        console.error("Erreur lors du chargement des campagnes :", err);
        alert("Impossible de charger les campagnes. Veuillez réessayer.");
      }
    });
  }

  getCampaignRows(): (ApiCampaign | null)[][] {
    const rows: (ApiCampaign | null)[][] = [];
    for (let i = 0; i < this.campaigns.length; i += 3) {
      const row = this.campaigns.slice(i, i + 3) as (ApiCampaign | null)[];
      while (row.length < 3) {
        row.push(null); // Ajouter des cellules vides pour compléter la ligne
      }
      rows.push(row);
    }
    return rows;
  }
  
  
}
