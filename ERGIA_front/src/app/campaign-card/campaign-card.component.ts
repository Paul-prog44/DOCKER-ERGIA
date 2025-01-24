import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiCampaign } from '../../api/models/campaign';
import {Router, RouterLink} from "@angular/router";


@Component({
  selector: 'app-campaign-card',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './campaign-card.component.html',
  styleUrl: './campaign-card.component.scss'
})
export class CampaignCardComponent {
  @Input({required:true}) campaign!:ApiCampaign
}
