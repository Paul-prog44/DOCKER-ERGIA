import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environments';


@Injectable({
  providedIn: 'root'
})
export class CampaignService {
  private apiUrl = environment.apiUrl

  constructor(private http : HttpClient) { }

  getCampaigns(): Observable<any> {
    return this.http.get(`${this.apiUrl}/campaigns`)
  }

  getCampaign(id : number): Observable<any> {
    return this.http.get(`${this.apiUrl}/campaigns/${id}`)
  }

  getCampaignByName(name: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/campaignsName/${name}`)
  }

  createCampaign(data : any): Observable<any> {
    return this.http.post(`${this.apiUrl}/campaigns`, data, { observe: 'response' })
  }

  deleteCampaign(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/campaigns/${id}`)
  }

  getJoinedCampaigns(userId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/campaigns/user/${userId}`);
  }
  joinCampaigns(data : any): Observable<any> {
    return this.http.post(`${this.apiUrl}/add_user_to_campaign`, data)
  }
  leaveCampaign(data : any): Observable<any> {
    return this.http.post(`${this.apiUrl}/delete_user_to_campaign`, data)
  }

  getOriginalTexts(id : number): Observable<any>{
  return this.http.get(`${this.apiUrl}/campaigns/originalTexts/${id}`)
 }
  getCampaignsByOwner(userId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/campaigns/getOwnerCampagn/${userId}`);
  }
  updateCampaignStatus(data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/campaigns/update_status`, data);
  }
  getStatus(userId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/campaigns/getStatusCampagn/${userId}`);
  }
}
