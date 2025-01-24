import { Routes } from '@angular/router';
import { AccueilComponent } from './accueil/accueil.component';
import { LoginComponent } from './login/login.component';
import { CampaignCreationComponent } from './campaign-creation/campaign-creation.component';
import { AccountCreationComponent } from './account-creation/account-creation.component'
import { CampaignDashboardComponent } from './campaign-dashboard/campaign-dashboard.component';
import { UserAccountComponent } from './user-account/user-account.component';
import {DetailCampagneComponent} from "./detail-campagne/detail-campagne.component";
import { AuthGuard } from './guard/auth.guard';
import { Component } from '@angular/core';
import { CguComponent } from './cgu/cgu.component';
import { AnnotationPageComponent } from './annotation/annotation-page/annotation-page.component';
import { MycampaignComponent } from './mycampaign/mycampaign.component';

export const routes: Routes = [
    { path: '',     component: AccueilComponent },
    { path: 'login', component: LoginComponent },
    { path: 'createCampaign', component: CampaignCreationComponent,  canActivate: [AuthGuard] },
    { path: 'createAccount', component: AccountCreationComponent},
    { path: 'campagne/:id', component: DetailCampagneComponent},
    { path: 'campaignDashboard', component: CampaignDashboardComponent, canActivate: [AuthGuard]},
    { path: 'userAccount', component: UserAccountComponent, canActivate: [AuthGuard]},
    { path: 'cgu', component: CguComponent},
    { path: 'annotation', component : AnnotationPageComponent, canActivate: [AuthGuard]} ,
    {path: '', redirectTo:'/login', pathMatch: 'full'},
    { path: 'annotation/:id_original_text/:id_summary', component : AnnotationPageComponent},
    { path: 'mycampaign', component: MycampaignComponent, canActivate: [AuthGuard]},
    {path: '', redirectTo:'/login', pathMatch: 'full'},


    // {path: '', redirectTo:'/login', pathMatch: 'full'}
    ]
