import {Component, inject, Injectable, input, OnInit} from '@angular/core';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import { CampaignService } from '../services/campaign.service';
import {ApiCampaign} from "../../api/models/campaign";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {Observable} from "rxjs";
import { UserService } from '../services/user.service';
import {CorpusService} from "../services/corpus.service";
import {OriginalText} from "../../api/models/original-text";
import {Summary} from "../../api/models/summary";


@Component({
  selector: 'app-detail-campagne',
  standalone: true,
  imports: [HttpClientModule, FormsModule, NgIf, NgForOf, RouterLink],
  templateUrl: './detail-campagne.component.html',
  styleUrl: './detail-campagne.component.scss'
})
export class DetailCampagneComponent implements OnInit{
  private route = inject(ActivatedRoute)
  id: number = -1
  nomCampagne: string | undefined;
  datePhase1: Date | undefined;
  datePhase2: Date | undefined;
  owner: string | undefined;
  joinedCampaignsIds: number[] = []; // Liste des campagnes rejointes par l'utilisateur
  originalTexts: OriginalText[] = []

  constructor(private campaignService: CampaignService, private userService: UserService, private corpusService: CorpusService) {
    this.route.params.subscribe(params => {
      this.id = +params['id'];
    })

    this.campaignService.getCampaign(this.id).subscribe( data => {
      data = data[0]
      this.nomCampagne = data["name"];
      this.datePhase2 = data["date_phase_2"] ? data["date_phase_2"] : "Non définie";
      this.datePhase1 = data["date_phase_1"] ? data["date_phase_1"] : "Non définie";
      this.owner = data["owner_id"];

    })
  }

  ngOnInit(){
    this.route.params.subscribe(params => {
      this.id = +params['id'];
    })

    this.campaignService.getCampaign(this.id).subscribe( data => {
    })
    this.loadJoinedCampaigns();

    this.corpusService.getTextsByCampaign(this.id).subscribe({
      next: (data) => {
        this.originalTexts = data.map((item: any) => new OriginalText(item))
        this.originalTexts.forEach((text) => {
          this.corpusService.getSummariesByOriginalText(text.idOriginalText).subscribe({
            next: (data) => {
              text.summaries = data.map((item: any) => new Summary(item))
            },
            error: (error) => {
              console.error('Erreur lors de la récupération des données :', error)
            }
          })
        })
      },
      error: (error) => {
        console.error('Erreur lors de la récupération des données :', error);
      }
    });



  }

  //campagne: ApiCampaign
  selectedTab: string = 'arbo'
  repertoireOuvert: number =  -1



  ouvrirRepertoire(index: number): void{
    if(this.repertoireOuvert === index){
      this.repertoireOuvert = -1
    }
    else{
      this.repertoireOuvert = index
    }
  }

  logFile(fichier: any){
    console.log(fichier)
  }

  joinCampaign(): void {
    const localStorage_idUser = localStorage.getItem('id_user');
    const userId = localStorage_idUser ? parseInt(localStorage_idUser, 10) : null;

    const id_campagne = this.id

    const data = {
      campaign_id: id_campagne,
      user_id: userId
    }

    this.campaignService.joinCampaigns(data).subscribe({
      next: (response) => {
        alert('Vous avez rejoint la campagne avec succès !');
        this.loadJoinedCampaigns();
      },
      error: (err) => {
        console.error(err);
        alert('Une erreur est survenue lors de la tentative de rejoindre la campagne.');
      }
    });
  }

  // Méthode pour charger les campagnes rejointes
  loadJoinedCampaigns(): void {
    this.userService.getUserCompaignJoined().subscribe({
      next: (data) => {
        //console.log("Campagnes rejointes :", data);
        this.joinedCampaignsIds = data.map(campaign => campaign.id_campaign); // Stocker les IDs des campagnes
      },
      error: (err) => {
        console.error("Erreur lors du chargement des campagnes rejointes :", err);
      }
    });
  }

  // Méthode pour vérifier si la campagne actuelle est rejointe
  isJoined(): boolean {
    return this.joinedCampaignsIds.includes(this.id);
  }

  leaveCampaign(){
    const localStorage_idUser = localStorage.getItem('id_user');
    const userId = localStorage_idUser ? parseInt(localStorage_idUser, 10) : null;

    const id_campagne = this.id

    const data = {
      campaign_id: id_campagne,
      user_id: userId
    }

    this.campaignService.leaveCampaign(data).subscribe({
      next: (response) => {
        alert('Vous avez quitter la campagne avec succès !');
        this.loadJoinedCampaigns();
      },
      error: (err) => {
        console.error(err);
        alert('Une erreur est survenue lors de la tentative de quitter la campagne.');
      }
    });
  }


}
