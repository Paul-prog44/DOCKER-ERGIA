import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import {FormControl, FormGroup, ReactiveFormsModule} from '@angular/forms';
import { CampaignService } from '../services/campaign.service';


@Component({
  selector: 'app-campaign-creation',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './campaign-creation.component.html',
  styleUrl: './campaign-creation.component.scss'
})

export class CampaignCreationComponent {
  constructor(private router: Router, private campaignService: CampaignService ) {}


  createCampaignForm = new FormGroup({
    owner_id: new FormControl(localStorage.getItem("id_user")), //TODO : Récuperer l'id de l'utilisateur
    status_id: new FormControl('2'),
    campaign_name: new FormControl(''),
    date_phase_1: new FormControl(''),
    date_phase_2: new FormControl(''),
    file: new FormControl<File | null>(null) 
  })

  errorMessage = ""
  
  //Stockage des fichiers

  //Vérification de la structure du corpus
  onFolderSelected(event: Event) {
    const inputFile = event.target as HTMLInputElement

    if (inputFile?.files?.length) {
      const file = inputFile.files[0];
      this.createCampaignForm.patchValue({
        file: file
      });
    }
  }

  handleSubmit() {
  const formData = new FormData();

  Object.keys(this.createCampaignForm.controls).forEach(key => {
    const value = this.createCampaignForm.get(key)?.value;
    if (value !== null && key !== 'file') {
      formData.append(key, value);
    }
  });

  const file = this.createCampaignForm.get('file')?.value;
  if (file) {
    formData.append('file', file);
  }
    if (this.createCampaignForm.value.campaign_name == "") {
      this.errorMessage = "Le nom est obligatoire"
    }

    if (this.createCampaignForm.value.date_phase_1) {
      if (new Date() > new Date(this.createCampaignForm.value.date_phase_1!)) {
        this.errorMessage = "La date de phase 1 ne peut être dans le passé"
        return
      }
      if (new Date(this.createCampaignForm.value.date_phase_1!) >= new Date(this.createCampaignForm.value.date_phase_2!)) {
        this.errorMessage = "La date de phase 2 ne peut être avant la phase 1"
        return
      }
    }

    this.campaignService.createCampaign(formData).subscribe({
      next: (response) => {
        if (response.status) {this.router.navigate(['/campaignDashboard'], { state: { message : 'Votre campagne a bien été créée !'}})}
      },
      error: (error) => {
        console.error('Status Code:', error.status)
        console.error('Error occurred:', error.message)
      },
    });
  }
}
